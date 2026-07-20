import base64, time, random, itertools
from datetime import datetime, timezone, timedelta
import httpx
from . import config, db

_token = {"v": None, "exp": 0}

async def app_token(client):
    if _token["v"] and time.time() < _token["exp"] - 60:
        return _token["v"]
    auth = base64.b64encode(f"{config.EBAY_CLIENT_ID}:{config.EBAY_CLIENT_SECRET}".encode()).decode()
    r = await client.post(config.TOKEN_URL, headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}, timeout=20)
    r.raise_for_status()
    j = r.json(); _token.update(v=j["access_token"], exp=time.time() + j["expires_in"])
    return _token["v"]

def _norm_item(s):
    price = s.get("currentBidPrice") or s.get("price") or {}
    ship = 0.0
    for o in s.get("shippingOptions", []) or []:
        c = (o.get("shippingCost") or {}).get("value")
        if c is not None: ship = float(c); break
    parts = s["itemId"].split("|")          # REST id "v1|123456789012|0" -> legacy item number
    return {
        "item_id": s["itemId"], "legacy_id": parts[1] if len(parts) > 1 else s["itemId"],
        "title": s.get("title", ""), "url": s.get("itemWebUrl", ""),
        "image": (s.get("image") or {}).get("imageUrl", ""),
        "buying": ",".join(s.get("buyingOptions", [])), "price": float(price.get("value", 0)),
        "shipping": ship, "bids": s.get("bidCount", 0),
        "seller": (s.get("seller") or {}).get("username", ""),
        "fb_pct": float((s.get("seller") or {}).get("feedbackPercentage", 0) or 0),
        "fb_count": int((s.get("seller") or {}).get("feedbackScore", 0) or 0),
        "condition": s.get("condition", ""), "end_time": s.get("itemEndDate", ""),
    }

_FORMATS = {"any": "AUCTION|FIXED_PRICE", "auction": "AUCTION", "bin": "FIXED_PRICE"}
_CONDS = {"used": "conditionIds:{3000|2000|2500},", "new": "conditionIds:{1000},", "any": ""}

def build_query(t):
    q = t.get("keywords", [t["name"]])[0]
    minus = " ".join(f"-{w}" for w in t.get("avoid", [])[:3] if " " not in w)
    return f"{q} {minus}".strip()

async def search(client, t):
    tok = await app_token(client)
    headers = {"Authorization": f"Bearer {tok}", "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"}
    if config.ZIP_CODE:
        headers["X-EBAY-C-ENDUSERCTX"] = f"contextualLocation=country%3DUS%2Czip%3D{config.ZIP_CODE}"
    flt = (f"buyingOptions:{{{_FORMATS[t.get('format', 'any')]}}},"
           f"price:[10..{int(t['max'] * 1.05)}],priceCurrency:USD,"
           f"{_CONDS[t.get('condition', 'any')]}deliveryCountry:US")
    params = {"q": build_query(t), "limit": "50", "sort": "newlyListed", "filter": flt}
    if t.get("category_id"):
        params["category_ids"] = str(t["category_id"])
    r = await client.get(config.SEARCH_URL, headers=headers, params=params, timeout=25)
    db.bump("calls_" + datetime.now(timezone.utc).strftime("%Y%m%d"))
    if r.status_code == 429:
        return "RATE_LIMITED", []
    r.raise_for_status()
    return "OK", [_norm_item(s) for s in r.json().get("itemSummaries", [])]

# ---------- demo generator ----------
_ctr = itertools.count(1)
_FLAVOR = ["great condition", "tested working", "like new", "lightly used", "works perfectly", "mint"]
_JUNK = ["BOX ONLY", "for parts read", "empty box no item"]

def demo_batch(targets, n=3):
    out = []
    for _ in range(n):
        t = random.choice(targets); kw = t.get("keywords", [t["name"]])[0]
        i = next(_ctr); auction = random.random() < 0.6
        junk = random.random() < 0.18
        title = f"{kw} {_JUNK[0] if junk else random.choice(_FLAVOR)}"
        price = round(random.uniform(t["steal"] * 0.6, t["max"] * 1.25), 2)
        out.append({
            "item_id": f"demo{int(time.time())}{i}", "legacy_id": f"10{int(time.time()) % 10**9:09d}{i}",
            "title": title, "url": "https://www.ebay.com/",
            "image": "", "buying": "AUCTION" if auction else "FIXED_PRICE",
            "price": price, "shipping": random.choice([0, 0, 9.99, 14.5]),
            "bids": random.randint(0, 14) if auction else 0,
            "seller": f"demo_seller{i}", "fb_pct": round(random.uniform(94, 100), 1),
            "fb_count": random.choice([3, 45, 220, 1500]), "condition": "Used",
            "end_time": (datetime.now(timezone.utc) + timedelta(minutes=random.randint(8, 4300))).isoformat() if auction else "",
        })
    return out
