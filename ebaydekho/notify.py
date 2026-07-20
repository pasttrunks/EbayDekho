import httpx
from datetime import datetime, timezone
from . import config

COLORS = {"STEAL": 0x2ECC71, "GOOD": 0xF1C40F, "FAIR": 0xE67E22, "SNIPE": 0x9B59B6}

def _ts(iso):
    try: return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())
    except Exception: return None

async def _post(client, payload):
    if not config.DISCORD_WEBHOOK_URL:
        e = payload["embeds"][0]
        print(f"  [alert] {e['title']} — {e['fields'][0]['value']}", flush=True)
        return True
    r = await client.post(config.DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    return r.status_code in (200, 204)

async def send_alert(client, it):
    left = _ts(it["end_time"])
    embed = {
        "title": f"{it['verdict']}: {it['target']}", "url": it["url"],
        "color": COLORS.get(it["verdict"], 0x95A5A6), "description": it["title"][:200],
        "fields": [
            {"name": "Landed", "value": f"**${it['landed']:.2f}**", "inline": True},
            {"name": "Bid + ship", "value": f"${it['price']:.2f} + ${it['shipping']:.2f}", "inline": True},
            {"name": "Ends", "value": f"<t:{left}:R>" if left else "Buy It Now", "inline": True},
            {"name": "Bids", "value": str(it["bids"]), "inline": True},
            {"name": "Seller", "value": f"{it['fb_pct']}% ({it['fb_count']})", "inline": True},
            {"name": "Bands", "value": f"steal ${it['steal']:.0f} · good ${it['good']:.0f} · max ${it['fair']:.0f}", "inline": True},
        ],
        "footer": {"text": f"ebaydekho · {it['note']}"},
    }
    if it["image"]: embed["thumbnail"] = {"url": it["image"]}
    payload = {"username": "EbayDekho", "embeds": [embed]}
    if it["verdict"] == "STEAL": payload["content"] = "@here STEAL detected"
    return await _post(client, payload)

async def send_snipe_reminder(client, it, minutes=10):
    left = _ts(it["end_time"])
    max_bid = round(min(it["fair"] - it["shipping"], it["fair"]) - 0.01, 2)
    embed = {
        "title": f"SNIPE WINDOW: {it['target']}", "url": it["url"], "color": COLORS["SNIPE"],
        "description": (f"{it['title'][:150]}\n\n**Suggested max bid: ${max_bid:.2f}** "
                        f"(your max ${it['fair']:.0f} − ${it['shipping']:.2f} ship)\n"
                        f"Ends <t:{left}:R> · currently ${it['price']:.2f} with {it['bids']} bids\n\n"
                        "Manual: open the link and bid in the last 10 seconds.\n"
                        "Gixen: schedule item `" + it["item_id"][-12:] + "` at your max — group it so first win cancels the rest."),
        "footer": {"text": f"ebaydekho snipe-assist · fires ~{minutes} min before close"},
    }
    payload = {"username": "EbayDekho", "content": "@here snipe window", "embeds": [embed]}
    return await _post(client, payload)
