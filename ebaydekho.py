#!/usr/bin/env python3
"""EbayDekho — eBay deal radar. Usage:
  python ebaydekho.py          run the radar (auto-setup on first run)
  python ebaydekho.py setup    re-run the configuration wizard
  python ebaydekho.py demo     force demo mode (fake listings)
"""
import asyncio, sys, random
from datetime import datetime, timezone

sys.dont_write_bytecode = True

from ebaydekho import config, db, ebay, notify, updater, webui, wizard
from ebaydekho.valuator import Matcher, evaluate

FORCE_DEMO = "demo" in sys.argv

async def process(client, items, matcher):
    alerts = 0
    for raw in items:
        target = matcher.match(raw["title"])
        if not target:
            continue
        verdict, note = evaluate(raw, target)
        raw.update(target=target["name"], verdict=verdict, note=note,
                   landed=round(raw["price"] + (raw["shipping"] or 0), 2),
                   first_seen=datetime.now(timezone.utc).isoformat(),
                   status="alerted" if verdict in config.ALERT_VERDICTS else "skipped",
                   steal=target["steal"], good=target["good"], fair=target["max"])
        is_new = db.save_item(raw)
        if is_new and verdict in config.ALERT_VERDICTS:
            if await notify.send_alert(client, raw):
                db.bump("alerts_sent"); alerts += 1
    return alerts

async def snipe_reminders(client):
    for it in db.due_reminders(minutes=10):
        if await notify.send_snipe_reminder(client, it):
            db.set_status(it["item_id"], "reminded")
            print(f"  [snipe-window] {it['target']} ends soon — ${it['landed']:.2f}", flush=True)

async def scout_loop():
    matcher, armed_on = None, None
    async with httpx_client() as client:
        while True:
            targets = config.load_targets()
            if not targets:
                if armed_on != "waiting":
                    print("[idle] no targets yet — finish setup in the browser tab", flush=True)
                    armed_on = "waiting"
                await asyncio.sleep(5); continue
            if repr(targets) != armed_on:
                matcher, armed_on = Matcher(targets), repr(targets)
            demo = FORCE_DEMO or config.DEMO
            try:
                if demo:
                    alerts = await process(client, ebay.demo_batch(targets, random.randint(2, 4)), matcher)
                    print(f"[demo] {datetime.now():%H:%M:%S} sweep — {alerts} alerts", flush=True)
                else:
                    alerts = 0
                    for t in targets:
                        status, items = await ebay.search(client, t)
                        if status == "RATE_LIMITED":
                            print("[live] rate limited — backing off 15 min", flush=True)
                            await asyncio.sleep(900); break
                        alerts += await process(client, items, matcher)
                        await asyncio.sleep(2)
                    print(f"[live] {datetime.now():%H:%M:%S} sweep — {alerts} alerts", flush=True)
                if config.MODE == "snipe":
                    await snipe_reminders(client)
            except Exception as e:
                print(f"[error] {type(e).__name__}: {e}", flush=True)
            await asyncio.sleep(45 if demo else config.POLL_SECONDS)

def httpx_client():
    import httpx
    return httpx.AsyncClient()

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "setup" in sys.argv:
        wizard.run(); return
    updater.maybe_update()
    db.init()
    port = webui.start()
    state = "radar" if config.load_targets() else "setup"
    print(f"EbayDekho v{__import__('ebaydekho').__version__} · opening http://127.0.0.1:{port} ({state}) — "
          "this console is just a log, do everything in the browser tab", flush=True)
    try:
        asyncio.run(scout_loop())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
