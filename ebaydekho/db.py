import sqlite3
from datetime import datetime, timezone, timedelta
from . import config

DB = config.ROOT / "ebaydekho.db"

def now(): return datetime.now(timezone.utc).isoformat()

def conn():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS items(
            item_id TEXT PRIMARY KEY, title TEXT, target TEXT, url TEXT, image TEXT,
            buying TEXT, price REAL, shipping REAL, landed REAL, bids INTEGER,
            seller TEXT, fb_pct REAL, fb_count INTEGER, condition TEXT,
            end_time TEXT, first_seen TEXT, verdict TEXT, status TEXT, note TEXT,
            steal REAL, good REAL, fair REAL, legacy_id TEXT)""")
        c.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")
        c.execute("""CREATE TABLE IF NOT EXISTS price_history(
            item_id TEXT, price REAL, ts TEXT,
            PRIMARY KEY (item_id, ts))""")
        cols = [r[1] for r in c.execute("PRAGMA table_info(items)")]   # migrate pre-0.3 db
        if "legacy_id" not in cols:
            c.execute("ALTER TABLE items ADD COLUMN legacy_id TEXT")

def record_price(item_id, price):
    with conn() as c:
        c.execute("INSERT OR IGNORE INTO price_history(item_id,price,ts) VALUES(?,?,?)",
            (item_id, price, now()))

def _sparkline(item_id):
    with conn() as c:
        prices = [r["price"] for r in c.execute(
            "SELECT price FROM price_history WHERE item_id=? ORDER BY ts DESC LIMIT 20",
            (item_id,)).fetchall()][::-1]
    if len(prices) < 2:
        return ""
    mn, mx = min(prices), max(prices)
    span = mx - mn or 1
    w, h = 240, 28
    pts = [f"{int(w*i/(len(prices)-1))},{int(h-2-(p-mn)/span*(h-4))}" for i,p in enumerate(prices)]
    d = "M " + " L ".join(pts)
    color = "23,52,80" if len(prices) < 3 else ("46,230,168" if prices[-1] <= prices[0] else "255,90,122")
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><path d="{d}" stroke="rgba({color},.8)"/><path d="{d}" stroke="rgba({color},.35)" stroke-width="5" filter="url(#b)"/><defs><filter id="b"><feGaussianBlur stdDeviation="3"/></filter></defs></svg>'

def save_item(it):
    with conn() as c:
        it.setdefault("legacy_id", "")
        cur = c.execute("INSERT OR IGNORE INTO items VALUES "
            "(:item_id,:title,:target,:url,:image,:buying,:price,:shipping,:landed,:bids,"
            ":seller,:fb_pct,:fb_count,:condition,:end_time,:first_seen,:verdict,:status,:note,"
            ":steal,:good,:fair,:legacy_id)", it)
        if cur.rowcount == 0:
            c.execute("UPDATE items SET price=:price, landed=:landed, bids=:bids WHERE item_id=:item_id", it)
        record_price(it["item_id"], it["price"])
        return cur.rowcount == 1

def set_status(item_id, status):
    with conn() as c: c.execute("UPDATE items SET status=? WHERE item_id=?", (status, item_id))

def pending_hydration(limit=6):
    """Alerted auctions missing an exact end time (scrape source)."""
    with conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT item_id, url FROM items WHERE status='alerted' AND buying LIKE '%AUCTION%' "
            "AND (end_time IS NULL OR end_time='') LIMIT ?", (limit,)).fetchall()]

def update_endtime(item_id, iso):
    with conn() as c:
        c.execute("UPDATE items SET end_time=? WHERE item_id=?", (iso, item_id))

def due_reminders(minutes=10):
    """Alerted auctions ending soon that haven't had a snipe-window reminder."""
    soon = (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat()
    with conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM items WHERE status='alerted' AND buying LIKE '%AUCTION%' "
            "AND end_time!='' AND end_time<? AND verdict IN ('STEAL','GOOD')", (soon,)).fetchall()]

def bump(key, n=1):
    with conn() as c:
        c.execute("INSERT INTO meta(k,v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=CAST(v AS INTEGER)+?", (key, str(n), n))

def get_meta(key, default="0"):
    with conn() as c:
        r = c.execute("SELECT v FROM meta WHERE k=?", (key,)).fetchone()
        return r["v"] if r else default

def recent(limit=120):
    with conn() as c:
        rows = c.execute("SELECT * FROM items WHERE verdict NOT IN ('EXCLUDED','SKIP','OFF_TARGET') ORDER BY first_seen DESC LIMIT ?", (limit,)).fetchall()
        stats = {
            "seen": c.execute("SELECT COUNT(*) n FROM items").fetchone()["n"],
            "alerts": int(get_meta("alerts_sent")),
            "calls": int(get_meta("calls_" + datetime.now(timezone.utc).strftime("%Y%m%d"))),
            "steals": c.execute("SELECT COUNT(*) n FROM items WHERE verdict='STEAL'").fetchone()["n"],
        }
        items = []
        for r in rows:
            d = dict(r)
            d["sparkline"] = _sparkline(d["item_id"])
            items.append(d)
    return {"items": items, "stats": stats}
