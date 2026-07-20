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
            steal REAL, good REAL, fair REAL)""")
        c.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")

def save_item(it):
    with conn() as c:
        cur = c.execute("INSERT OR IGNORE INTO items VALUES "
            "(:item_id,:title,:target,:url,:image,:buying,:price,:shipping,:landed,:bids,"
            ":seller,:fb_pct,:fb_count,:condition,:end_time,:first_seen,:verdict,:status,:note,"
            ":steal,:good,:fair)", it)
        if cur.rowcount == 0:
            c.execute("UPDATE items SET price=:price, landed=:landed, bids=:bids WHERE item_id=:item_id", it)
        return cur.rowcount == 1

def set_status(item_id, status):
    with conn() as c: c.execute("UPDATE items SET status=? WHERE item_id=?", (status, item_id))

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
    return {"items": [dict(r) for r in rows], "stats": stats}
