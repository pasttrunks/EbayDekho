#!/usr/bin/env python3
"""EbayDekho — eBay deal radar. Usage:
  python ebaydekho.py          run the radar (auto-setup on first run)
  python ebaydekho.py setup    re-run the configuration wizard
  python ebaydekho.py demo     force demo mode (fake listings)
"""
import asyncio, sys, random
from datetime import datetime, timezone

sys.dont_write_bytecode = True

from ebaydekho import config, db, ebay, notify, scraper, updater, webui, wizard
from ebaydekho.valuator import Matcher, evaluate

FORCE_DEMO = "demo" in sys.argv

async def process(client, items, matcher, alert=True):
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
        if alert and is_new and verdict in config.ALERT_VERDICTS:
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
            source = ("demo" if FORCE_DEMO else
                      "api" if (config.EBAY_CLIENT_ID and config.EBAY_CLIENT_SECRET) else "scrape")
            try:
                if source == "demo":
                    alerts = await process(client, ebay.demo_batch(targets, random.randint(2, 4)), matcher)
                    print(f"[demo] {datetime.now():%H:%M:%S} sweep — {alerts} alerts", flush=True)
                else:
                    alerts = 0
                    for t in targets:
                        if source == "api":
                            status, items = await ebay.search(client, t)
                        else:
                            status, items = await scraper.fetch_search(t)
                        if status in ("RATE_LIMITED", "BLOCKED"):
                            print(f"[{source}] throttled — backing off 15 min", flush=True)
                            await asyncio.sleep(900); break
                        if status == "ERROR":
                            continue
                        seed_key = "seeded_" + t["name"]
                        first = db.get_meta(seed_key) == "0"
                        alerts += await process(client, items, matcher, alert=not first)
                        if first:
                            db.bump(seed_key)
                            print(f"[seed] {t['name']}: baseline captured, alerts start now", flush=True)
                        await asyncio.sleep(2)
                    print(f"[{source}] {datetime.now():%H:%M:%S} sweep — {alerts} alerts", flush=True)
                if config.MODE == "snipe":
                    if source == "scrape":
                        for it in db.pending_hydration():
                            iso = await scraper.fetch_end_time(it["url"])
                            if iso:
                                db.update_endtime(it["item_id"], iso)
                    await snipe_reminders(client)
            except Exception as e:
                print(f"[error] {type(e).__name__}: {e}", flush=True)
            await asyncio.sleep(45 if source == "demo" else
                                max(config.POLL_SECONDS, 900) if source == "scrape" else config.POLL_SECONDS)

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
    from ebaydekho import desktop
    port = webui.start(open_browser=False)
    threading.Thread(target=lambda: asyncio.run(scout_loop()), daemon=True).start()
    desktop.start(port)

if __name__ == "__main__":
    main()
