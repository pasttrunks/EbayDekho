import re
from . import config

def _norm(t): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", t.lower())).strip()

class Matcher:
    """Title -> target. Longest keyword wins; word-boundary or squashed matching."""
    def __init__(self, targets):
        self.targets = targets
        self.rows = []  # (kw_norm, kw_squash, target_index)
        for i, t in enumerate(targets):
            for kw in [t["name"], *t.get("keywords", [])]:
                self.rows.append((_norm(kw), kw.lower().replace(" ", ""), i))
        self.rows.sort(key=lambda r: -len(r[1]))

    def match(self, title):
        tn = _norm(title); ts = tn.replace(" ", "")
        for kw_norm, kw_sq, i in self.rows:
            if (" " in kw_norm and re.search(rf"\b{re.escape(kw_norm)}\b", tn)) or kw_sq in ts:
                return self.targets[i]
        return None

def evaluate(item, target, cfg=config):
    """-> (verdict, note). item: price, shipping, buying, fb_count, title."""
    title_n = _norm(item["title"])
    avoids = cfg.GLOBAL_EXCLUDE + [w.lower() for w in target.get("avoid", [])]
    if any(w in title_n for w in avoids):
        return "EXCLUDED", "junk/keyword"
    landed = item["price"] + (item["shipping"] or 0)
    steal, good, mx = target["steal"], target["good"], target["max"]
    if "AUCTION" not in item["buying"] and landed < steal * 0.5:
        return "SUSPICIOUS", "too cheap = scam/broken"
    if landed > mx:
        return "SKIP", f"over ${mx:.0f} cap"
    verdict = "STEAL" if landed <= steal else "GOOD" if landed <= good else "FAIR"
    note = f"target: {target['name']}"
    if item["fb_count"] < cfg.MIN_FEEDBACK:
        verdict = {"STEAL": "GOOD", "GOOD": "FAIR", "FAIR": "SKIP"}[verdict]
        note = f"seller fb {item['fb_count']} -> downgraded"
    return verdict, note

def bands(target):
    return {"steal": target["steal"], "good": target["good"], "fair": target["max"]}
