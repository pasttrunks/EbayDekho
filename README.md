# EbayDekho 🎯

**Your eBay deal radar.** *Dekho* (দেখো) — "look / watch". Tell it what you're hunting and what it's worth — EbayDekho sweeps eBay around the clock, judges every listing against your price bands, pings you on Discord, and (optionally) taps you on the shoulder when it's time to snipe.

> ebay dekho. find it. judge it. snipe it.

![mode](https://img.shields.io/badge/mode-notify%20%7C%20snipe--assist-5cd6ff) ![python](https://img.shields.io/badge/python-3.10%2B-2ee6a8) ![license](https://img.shields.io/badge/license-MIT-8f7bff)

## Why

Good deals on eBay die in minutes. EbayDekho is the always-on spotter:

- **Sweep** — polls the official eBay Browse API for each of your targets (free dev key, 5,000 calls/day)
- **Judge** — matches titles to your targets, computes *landed price* (bid + shipping), scores it STEAL / GOOD / FAIR against your bands, and auto-trashes junk (`box only`, `for parts`, …), scam-priced BINs, and shaky sellers
- **Alert** — rich Discord embeds in seconds, `@here` only on steals
- **Snipe (assist)** — T-10-minute "snipe window" reminders with a suggested max bid, plus a Gixen-friendly workflow for true last-second server-side bidding
- **Dashboard** — a neon radar UI at `http://127.0.0.1:8787` with value meters, ticking countdowns, and filters. Loopback-only: nobody else can see it

## Quickstart (5 minutes)

```bash
git clone https://github.com/pasttrunks/EbayDekho.git
cd EbayDekho
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python ebaydekho.py           # first run = setup wizard, then it hunts
```

The wizard asks, in plain English: what are you hunting, what words mean junk, your dream/good/max prices, auction vs BIN, category, Discord webhook, and whether you want `notify` or `snipe` mode. It writes `targets.json` + `.env` and test-fires your Discord. That's the whole configuration.

No eBay keys yet? It runs in **DEMO mode** with fake listings so you can see everything working. Get free keys at [developer.ebay.com](https://developer.ebay.com/join) (My Account → Application Keys → Production keyset) and paste them into `.env`.

## Modes

| Mode | What it does | Risk |
|---|---|---|
| `notify` | Discord alerts → you click and buy/bid yourself | none |
| `snipe` | everything above + T-10min snipe-window reminders with suggested max bid + Gixen workflow | none |

EbayDekho deliberately **does not place bids for you**. Last-second bidding is 100% allowed by eBay, but unattended automation of your account isn't — so EbayDekho hands you (or [Gixen](https://gixen.com), an eBay-authorized sniping service) a perfectly timed shot instead of taking it itself.

## targets.json reference

```json
{
  "targets": [
    {
      "name": "RX 6800",
      "keywords": ["rx 6800", "rx6800", "6800 non xt"],
      "avoid": ["xt"],
      "steal": 265, "good": 300, "max": 330,
      "format": "any",          // any | auction | bin
      "condition": "used",      // used | new | any
      "category_id": 27386      // optional eBay category
    }
  ]
}
```

- **steal / good / max** — landed-price bands (bid + shipping). Over `max` = silently skipped. Under half of `steal` on a BIN = flagged SUSPICIOUS (scam/broken).
- **keywords** — most specific first. Matching uses word-boundaries, so `rx 6800` won't eat an `RX 6800 XT` listing if you also hunt the XT (list the more specific target first — see `examples/targets.example.json`).
- **avoid** — extra junk words on top of the built-in list (`box only`, `for parts`, `broken`, `preorder`, …).
- Sellers under 10 feedback are downgraded one tier. All knobs (`POLL_SECONDS`, `MIN_FEEDBACK`, `PORT`, …) live in `.env`.

## What it looks like

*(screenshot/GIF here — dark radar UI, value meters, ticking countdowns)*

Dashboard is bound to `127.0.0.1` only — invisible to your LAN and the internet. There are no write endpoints; your API secrets never leave `.env`.

## Roadmap

- [ ] `pipx install ebaydekho` packaging
- [ ] Docker image
- [ ] Web-based config editor
- [ ] Bidder plugin seam (bring-your-own; Gixen first)
- [ ] Price-history sparklines from collected listings
- [ ] Multi-marketplace (EBAY_GB, EBAY_DE…)

## Safety & fair play

- Uses only the official eBay Browse API for reading. Respect the 5k calls/day default quota (EbayDekho budgets and backs off on 429).
- Bids are binding. EbayDekho never bids; when *you* bid, bid your true max — eBay proxy bidding means you pay second-price + one increment.
- Sniping is allowed by eBay. Automating your account via unofficial means isn't — that's why it's not in this repo.

## License

MIT — see [LICENSE](LICENSE). Not affiliated with eBay Inc. or Discord Inc.
