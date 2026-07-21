"""Community Mode: keyless discovery via eBay's public search pages.
Polite by design — one request at a time, jittered pacing, backs off hard
when eBay shows a robot check. Uses curl_cffi for browser TLS fingerprinting
(bypasses most bot detection). Falls back to httpx if curl_cffi unavailable.
The official Browse API (with keys) stays the preferred source;
this keeps the app fully functional with zero accounts.
Parses the current 's-card' search-result markup (verified live 2026-07)."""
import asyncio, random, re, time
from datetime import datetime, timezone, timedelta

HAS_CURL = False
try:
    from curl_cffi.requests import AsyncSession
    HAS_CURL = True
except ImportError:
    pass

if not HAS_CURL:
    import httpx

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
]
BLOCK_SIGNS = ("Pardon Our Interruption", "robot-check", "captcha", "sec-cpt")
MIN_INTERVAL = 3.0          # seconds between page fetches, plus jitter
_last_fetch = [0.0]
_NUM = re.compile(r"([\d,]+(?:\.\d+)?)")

_curl_session = None
_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"}

async def _get_session():
    global _curl_session
    if HAS_CURL and _curl_session is None:
        _curl_session = AsyncSession(impersonate="chrome124")
        try:
            await _curl_session.get("https://www.ebay.com", timeout=20)
        except Exception:
            pass
    return _curl_session

def build_url(t):
    base = "https://www.ebay.com/sch"
    if t.get("category_id"):
        base += f"/{t['category_id']}"
    base += "/i.html"
    params = {"_nkw": _query(t), "_sop": "10", "_ipg": "60",   # 10 = newly listed
              "_udlo": "10", "_udhi": str(int(t["max"] * 1.05)),
              "LH_PrefLoc": "1"}                                # located in US
    cond = t.get("condition", "any")
    if cond == "used": params["LH_ItemCondition"] = "3000"
    elif cond == "new": params["LH_ItemCondition"] = "1000"
    fmt = t.get("format", "any")
    if fmt == "auction": params["LH_Auction"] = "1"
    elif fmt == "bin": params["LH_BIN"] = "1"
    return base, params

def _query(t):
    q = t.get("keywords", [t["name"]])[0]
    minus = " ".join(f"-{w}" for w in t.get("avoid", [])[:3] if " " not in w)
    return f"{q} {minus}".strip()

def _money(txt):
    m = _NUM.search(txt or "")
    return float(m.group(1).replace(",", "")) if m else 0.0

def _strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()

def _parse_card(block):
    def grab(pat):
        m = re.search(pat, block, re.S)
        return m.group(1) if m else ""
    lid = grab(r'data-listingid=(\d+)')
    title = _strip_tags(grab(r'class="?s-card__title"?[^>]*>(.*?)</div>'))
    title = re.sub(r"\s*Opens in a new window or tab\s*$", "", title)
    if not lid or not title or title == "Shop on eBay":
        return None
    href = grab(r'href="?(https://(?:www\.)?ebay\.com/itm/[^?\s>"]+)')
    rows = [_strip_tags(r) for r in
            re.findall(r'class="?s-card__attribute-row"?[^>]*>(.*?)</div>', block, re.S)]
    rows = [r for r in rows if r]
    price = _money(rows[0]) if rows else 0.0
    bids = next((int(m.group(1)) for r in rows if (m := re.match(r"(\d+) bids?$", r))), 0)
    ship_row = next((r for r in rows if r.startswith("+$") or "ree delivery" in r), "")
    ship = 0.0 if "ree" in ship_row else _money(ship_row)
    buying = "AUCTION" if bids > 0 else "FIXED_PRICE"
    sm = next((re.match(r"(.+?)\s+([\d.]+)% positive \(([\d,]+)\)", r) for r in rows
               if "positive" in r), None)
    if not price:
        return None
    return {
        "item_id": lid, "legacy_id": lid, "title": title,
        "url": href or f"https://www.ebay.com/itm/{lid}",
        "image": grab(r'class="?s-card__image"?[^>]*src="([^"]+)"'),
        "buying": buying, "price": price, "shipping": ship, "bids": bids,
        "seller": sm.group(1).strip() if sm else "",
        "fb_pct": float(sm.group(2)) if sm else 0.0,
        "fb_count": int(sm.group(3).replace(",", "")) if sm else 0,
        "condition": "", "end_time": "",
    }

def parse_items(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    out = []
    for block in re.split(r'<li class="s-card ', html)[1:]:
        item = _parse_card(block[:15000])
        if item:
            out.append(item)
    return out

async def _get(client, url, params=None):
    wait = MIN_INTERVAL + random.uniform(0, 2) - (time.time() - _last_fetch[0])
    if wait > 0:
        await asyncio.sleep(wait)
    ua = random.choice(UA_POOL)
    try:
        if HAS_CURL:
            sess = await _get_session()
            r = await sess.get(url, params=params, timeout=25,
                headers={"User-Agent": ua, **_headers})
        else:
            r = await client.get(url, params=params, timeout=25, follow_redirects=True,
                headers={"User-Agent": ua, **_headers})
    except Exception:
        return "ERROR", ""
    finally:
        _last_fetch[0] = time.time()
    if r.status_code in (403, 429) or any(sig in r.text for sig in BLOCK_SIGNS):
        return "BLOCKED", ""
    return ("OK", r.text) if r.status_code == 200 else ("ERROR", "")

async def fetch_search(t, client=None):
    url, params = build_url(t)
    status, html = await _get(client, url, params)
    if status == "BLOCKED":
        await asyncio.sleep(5)
        status, html = await _get(client, url, params)
    return (status, parse_items(html)) if status == "OK" else (status, [])

_END_PATTERNS = [
    re.compile(r'"itemEndDate"\s*:\s*"([^"]+)"'),
    re.compile(r'&quot;itemEndDate&quot;:\s*&quot;([^&]+)&quot;'),
    re.compile(r'"endDate"\s*:\s*"([^"]+)"'),
]

async def fetch_end_time(item_url, client=None):
    """Exact auction close from the item page (search cards only carry listed-date)."""
    status, html = await _get(client, item_url)
    if status != "OK":
        return ""
    for pat in _END_PATTERNS:
        m = pat.search(html)
        if m:
            return m.group(1)
    return ""
