"""Auto-updater: checks GitHub Releases at startup, shows release notes
for every version between current and latest, then (exe only) asks
before downloading, swapping, and restarting itself."""
import os, subprocess, sys, time
from pathlib import Path

import httpx

from . import __version__

REPO = "pasttrunks/EbayDekho"
API = f"https://api.github.com/repos/{REPO}/releases"
EXE_NAME = "EbayDekho.exe"
FALLBACK_URL = f"https://github.com/{REPO}/releases/latest/download/{EXE_NAME}"

def _ver(tag):
    for tok in "".join(c if c.isdigit() or c == "." else " " for c in tag).split():
        parts = tok.strip(".").split(".")
        if parts and all(p.isdigit() for p in parts):
            return tuple(int(p) for p in parts)
    return (0,)

def _enabled():
    return os.environ.get("AUTO_UPDATE", "1").lower() not in ("0", "false", "off", "no")

def _pending(current):
    """Releases newer than current, oldest first."""
    try:
        r = httpx.get(API, params={"per_page": 10}, timeout=10,
                      headers={"Accept": "application/vnd.github+json"})
        r.raise_for_status()
        out = []
        for rel in r.json():
            if rel.get("draft") or rel.get("prerelease"):
                continue
            if _ver(rel.get("tag_name", "")) > current:
                url = next((a["browser_download_url"] for a in rel.get("assets", [])
                            if a.get("name") == EXE_NAME), FALLBACK_URL)
                out.append({"version": rel["tag_name"], "date": rel.get("published_at", "")[:10],
                            "notes": (rel.get("body") or "").strip(), "url": url})
        return sorted(out, key=lambda p: _ver(p["version"]))
    except Exception as e:
        print(f"[update] check failed ({type(e).__name__}) — continuing anyway", flush=True)
        return []

def _show(pending):
    print("\n  ============================================", flush=True)
    print("    EbayDekho update available — what's new:", flush=True)
    print("  ============================================", flush=True)
    for p in pending:
        print(f"\n  -- {p['version']}  ({p['date']}) " + "-" * 18, flush=True)
        for line in (p["notes"] or "(no release notes)").splitlines()[:24]:
            print("   " + line, flush=True)
    print("", flush=True)

def maybe_update():
    if not _enabled():
        return
    pending = _pending(_ver(__version__))
    if not pending:
        return
    _show(pending)
    if not getattr(sys, "frozen", False):
        print("  Source install — update with:  git pull   (or re-run install.ps1)\n", flush=True)
        return
    if sys.stdin.isatty():
        if input("  Update now? [Y/n] ").strip().lower() in ("n", "no"):
            print("  Skipped — staying on this version.\n", flush=True)
            return
    elif os.environ.get("AUTO_UPDATE", "").lower() != "force":
        print("  Run EbayDekho from a terminal to apply this update.\n", flush=True)
        return
    _apply(pending[-1])

def _apply(latest):
    exe = Path(sys.executable).resolve()
    new = exe.with_name(exe.stem + ".new.exe")
    print(f"  Downloading {latest['version']}...", flush=True)
    with httpx.stream("GET", latest["url"], follow_redirects=True, timeout=180) as r:
        r.raise_for_status()
        with open(new, "wb") as f:
            for chunk in r.iter_bytes(1 << 16):
                f.write(chunk)
    cmd = exe.with_name("_ebaydekho_update.cmd")
    cmd.write_text(
        "@echo off\r\nset TRIES=0\r\n:try\r\n"
        f'move /y "{new.name}" "{exe.name}" >nul 2>&1\r\n'
        "if errorlevel 1 (timeout /t 1 >nul & set /a TRIES+=1 & if %TRIES% lss 30 goto try)\r\n"
        f'start "" "{exe.name}"\r\n(goto) 2>nul & del "%~f0"\r\n')
    print("  Applying update — EbayDekho will restart itself...", flush=True)
    time.sleep(0.5)
    os.startfile(str(cmd))  # visible little console, self-deletes after swap
    os._exit(0)
