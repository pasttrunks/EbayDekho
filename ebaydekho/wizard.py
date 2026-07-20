import json, sys
from pathlib import Path
from . import config

ROOT = config.ROOT

BANNER = r"""
   _____ _             ___      _    _
  | ____| |__  __ _ _|   \ ___| | _| |__ ___
  | _| | '_ \/ _` | | | | / _ \ |/ / '_ \/ _ \
  | |__| |_) | (_| | |__| |  __/   <| | | | (_) |
  |____|_.__/\__,_|\ |___/ \___|_|\_\_| |_|\___/
                  |___/
  ebay dekho — look at ebay. find it. judge it. snipe it.
"""

CATEGORIES = {
    "1": ("All categories (search everywhere)", None),
    "2": ("Graphics/Video Cards", 27386),
    "3": ("CPUs/Processors", 164),
    "4": ("Video Game Consoles", 139971),
    "5": ("Cell Phones & Smartphones", 9355),
    "6": ("Digital Cameras", 31388),
    "7": ("Laptops & Netbooks", 175672),
    "8": ("Computer RAM", 170083),
}

def _ask(prompt, default=None, cast=str):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"  {prompt}{suffix}: ").strip()
    if not raw:
        return default
    try:
        return cast(raw)
    except (ValueError, TypeError):
        print("  ! invalid, try again")
        return _ask(prompt, default, cast)

def _ask_price(prompt, default=None):
    return float(_ask(prompt, default, lambda s: float(s.replace("$", "").replace(",", ""))))

def ask_target(n):
    print(f"\n── Target #{n} " + "─" * (34 - len(str(n))))
    name = _ask("What are you hunting? (e.g. 'RTX 4070', 'PS5 disc', 'Sony A7III')")
    if not name:
        return None
    kw = _ask(f"Search keywords, comma-separated", name.lower())
    avoid = _ask("Words that mean junk, comma-separated (box, parts, case...)", "")
    dream = _ask_price("DREAM price — at or under = STEAL ($)")
    mx = _ask_price("ABSOLUTE MAX landed price, shipping included ($)")
    good_default = round(dream + (mx - dream) * 0.55)
    good = _ask_price("Good-deal price", good_default)
    print("  Buying format: 1) auctions + Buy It Now  2) auctions only  3) BIN only")
    fmt = {"1": "any", "2": "auction", "3": "bin"}[_ask("Format", "1")]
    print("  Condition: 1) used  2) new  3) any")
    cond = {"1": "used", "2": "new", "3": "any"}[_ask("Condition", "1")]
    for k, (label, _) in CATEGORIES.items():
        print(f"    {k}) {label}")
    cat = CATEGORIES[_ask("Category", "1")][1]
    return {
        "name": name,
        "keywords": [k.strip() for k in kw.split(",") if k.strip()],
        "avoid": [a.strip() for a in avoid.split(",") if a.strip()],
        "steal": dream, "good": good, "max": mx,
        "format": fmt, "condition": cond,
        **({"category_id": cat} if cat else {}),
    }

def run():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(BANNER)
    print("  Let's build your hit list. Answer a few questions per item.")
    targets = []
    while True:
        t = ask_target(len(targets) + 1)
        if t:
            targets.append(t)
            print(f"  ✓ {t['name']}: steal ≤ ${t['steal']:.0f} · good ≤ ${t['good']:.0f} · max ${t['max']:.0f}")
        if _ask("\nAdd another target? (y/n)", "n").lower() != "y":
            break
    if not targets:
        print("No targets — nothing to hunt. Bye."); sys.exit(1)

    print("\n── Connections " + "─" * 30)
    cid = _ask("eBay API Client ID (blank = DEMO mode for now)", "")
    csec = _ask("eBay API Client Secret", "") if cid else ""
    hook = _ask("Discord webhook URL (blank = console alerts)", "")

    print("\n── Mode " + "─" * 36)
    print("  1) notify      → Discord pings, you buy by hand (safe, recommended)")
    print("  2) snipe       → + T-10min 'snipe window' reminders w/ suggested max bid")
    mode = {"1": "notify", "2": "snipe"}[_ask("Mode", "1")]
    poll = _ask("Sweep every N seconds", "600", int)

    (ROOT / "targets.json").write_text(json.dumps({"targets": targets}, indent=2))
    env = ROOT / ".env"
    lines = [
        f"EBAY_CLIENT_ID={cid}", f"EBAY_CLIENT_SECRET={csec}",
        f"DISCORD_WEBHOOK_URL={hook}", f"MODE={mode}", f"POLL_SECONDS={poll}",
        "ZIP_CODE=", "MIN_FEEDBACK=10", "PORT=8787",
    ]
    env.write_text("\n".join(lines) + "\n")

    print(f"\n  ✓ wrote targets.json ({len(targets)} targets) and .env")
    if hook:
        import urllib.request
        try:
            req = urllib.request.Request(hook, data=json.dumps(
                {"username": "EbayDekho", "content": f"🎯 EbayDekho armed — hunting {', '.join(t['name'] for t in targets)}"}).encode(),
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
            print("  ✓ Discord test message sent — check your channel")
        except Exception as e:
            print(f"  ! Discord test failed: {e} (check the webhook URL)")
    print("\n  Done. Run:  python ebaydekho.py\n")

if __name__ == "__main__":
    run()
