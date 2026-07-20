"""Plain-assert tests, no pytest needed:  python tests/test_valuator.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.dont_write_bytecode = True

from ebaydekho.valuator import Matcher, evaluate

TARGETS = [
    {"name": "RX 6800 XT", "keywords": ["rx 6800 xt", "6800xt"], "avoid": [],
     "steal": 285, "good": 310, "max": 345, "format": "any", "condition": "used"},
    {"name": "RX 6800", "keywords": ["rx 6800", "rx6800"], "avoid": ["xt"],
     "steal": 265, "good": 300, "max": 330, "format": "any", "condition": "used"},
    {"name": "RTX 3080", "keywords": ["rtx 3080", "rtx3080"], "avoid": ["ti"],
     "steal": 265, "good": 300, "max": 335, "format": "any", "condition": "used"},
]

m = Matcher(TARGETS)

def item(**kw):
    d = dict(title="x", price=200, shipping=0, bids=3, buying="AUCTION", fb_pct=99.0, fb_count=500)
    d.update(kw); return d

cases = [
    ("XT title -> XT target",            m.match("PowerColor Radeon RX 6800 XT 16GB")["name"], "RX 6800 XT"),
    ("base title -> base target",        m.match("AMD Radeon RX 6800 16GB GDDR6")["name"], "RX 6800"),
    ("squashed alias",                   m.match("RX6800XT Red Devil")["name"], "RX 6800 XT"),
    ("no match -> None",                 m.match("gaming pc i5 bundle"), None),
    ("avoid word kills base target",     evaluate(item(title="RX 6800 XT 16gb", price=300), TARGETS[1])[0], "EXCLUDED"),
    ("steal band",                       evaluate(item(price=260), TARGETS[1])[0], "STEAL"),
    ("good band",                        evaluate(item(price=280), TARGETS[1])[0], "GOOD"),
    ("fair band",                        evaluate(item(price=320), TARGETS[1])[0], "FAIR"),
    ("over max -> SKIP",                 evaluate(item(price=340), TARGETS[1])[0], "SKIP"),
    ("global junk excluded",             evaluate(item(title="RX 6800 BOX ONLY", price=99, buying="FIXED_PRICE"), TARGETS[1])[0], "EXCLUDED"),
    ("suspiciously cheap BIN",           evaluate(item(title="RTX 3080", price=90, buying="FIXED_PRICE"), TARGETS[2])[0], "SUSPICIOUS"),
    ("cheap auction is fine",            evaluate(item(title="RTX 3080", price=90), TARGETS[2])[0], "STEAL"),
    ("low feedback downgrades",          evaluate(item(price=260, fb_count=3), TARGETS[1])[0], "GOOD"),
    ("landed math incl shipping",        evaluate(item(price=260, shipping=25), TARGETS[1])[0], "GOOD"),
]

fails = 0
for name, got, want in cases:
    ok = got == want
    fails += not ok
    print(("OK  " if ok else "FAIL"), name, "->", got, "" if ok else f"(want {want})")
print(f"\n{len(cases) - fails}/{len(cases)} passed")
sys.exit(1 if fails else 0)
