"""Parser test against current eBay 's-card' markup:  python tests/test_scraper.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.dont_write_bytecode = True

from ebaydekho.scraper import parse_items, build_url, _money

# fixture mirrors live 2026-07 s-card structure (trimmed)
HTML = """
<ul><li class="s-card s-card--horizontal" data-listingid=2500219655424533>
<div role=heading aria-level=3 class=s-card__title>Shop on eBay</div>
<div class=s-card__attribute-row><span class="su-styled-text s-card__price">$20.00</span></div>
<a class=s-card__link href=https://ebay.com/itm/123456></a></li>
<li class="s-card s-card--horizontal" data-listingid=407082523803>
<div role=heading aria-level=3 class=s-card__title>PowerColor Red Dragon AMD Radeon RX 6800 16GB GDDR6 Graphic Card Opens in a new window or tab</div>
<div class=s-card__attribute-row>$340.00</div>
<div class=s-card__attribute-row>or Best Offer</div>
<div class=s-card__attribute-row>+$49.74 delivery</div>
<div class=s-card__attribute-row>Located in United States</div>
<div class=s-card__attribute-row>fireflies1002_9 100% positive (23)</div>
<a class=s-card__link href=https://www.ebay.com/itm/407082523803?_skw=rx+6800></a></li>
<li class="s-card s-card--horizontal" data-listingid=278187575444>
<div role=heading aria-level=3 class=s-card__title>AMD Radeon RX 6800 16GB GDDR6 Graphics Card Opens in a new window or tab</div>
<div class=s-card__attribute-row>$290.00</div>
<div class=s-card__attribute-row>10 bids</div>
<div class=s-card__attribute-row>+$20.00 delivery</div>
<div class=s-card__attribute-row>ethanhero 99.1% positive (1,220)</div>
<a class=s-card__link href=https://www.ebay.com/itm/278187575444></a></li>
</ul>
"""

items = parse_items(HTML)
cases = [
    ("ghost card skipped",            len(items), 2),
    ("legacy id",                     items[0]["legacy_id"], "407082523803"),
    ("title cleaned",                 items[0]["title"].endswith("Opens in a new window"), False),
    ("price",                         items[0]["price"], 340.0),
    ("shipping",                      items[0]["shipping"], 49.74),
    ("bin detected",                  items[0]["buying"], "FIXED_PRICE"),
    ("seller name",                   items[0]["seller"], "fireflies1002_9"),
    ("auction via bids",              items[1]["buying"], "AUCTION"),
    ("bid count",                     items[1]["bids"], 10),
    ("fb pct",                        items[1]["fb_pct"], 99.1),
    ("fb count with comma",           items[1]["fb_count"], 1220),
    ("money range takes first",       _money("$100.00 to $200.00"), 100.0),
    ("url has filters",               build_url({"name": "RX 6800", "keywords": ["rx 6800"], "avoid": ["xt"],
                                                 "steal": 265, "good": 300, "max": 330,
                                                 "format": "auction", "condition": "used",
                                                 "category_id": 27386})[1]["LH_Auction"], "1"),
]

fails = 0
for name, got, want in cases:
    ok = got == want
    fails += not ok
    print(("OK  " if ok else "FAIL"), name, "->", got, "" if ok else f"(want {want})")
print(f"\n{len(cases) - fails}/{len(cases)} passed")
sys.exit(1 if fails else 0)
