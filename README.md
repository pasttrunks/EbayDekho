# EbayDekho 🎯

**Your eBay deal radar.** *Dekho* (দেখো) — "look / watch". Tell it what you're hunting and what it's worth — EbayDekho sweeps eBay around the clock, judges every listing against your price bands, pings you on Discord, and (optionally) taps you on the shoulder when it's time to snipe.

> ebay dekho. find it. judge it. snipe it.

![mode](https://img.shields.io/badge/mode-notify%20%7C%20snipe--assist-5cd6ff) ![python](https://img.shields.io/badge/python-3.10%2B-2ee6a8) ![license](https://img.shields.io/badge/license-MIT-8f7bff)

## Why

Good deals on eBay die in minutes. EbayDekho is the always-on spotter:

- **Browser setup** — double-click and a neon setup page opens in your browser; configure everything without touching a terminal
- **Zero-account start** — Community Mode reads eBay's public search pages: no API keys, no developer signup, no rejection letters. Works the second you finish setup
- **Sweep** — polls eBay for each of your targets: official Browse API if you add free keys (preferred), polite keyless scraping otherwise. First sweep per target silently seeds a baseline — no alert tsunami
- **Judge** — matches titles to your targets, computes *landed price* (bid + shipping), scores it STEAL / GOOD / FAIR against your bands, and auto-trashes junk (`box only`, `for parts`, …), scam-priced BINs, and shaky sellers
- **Alert** — rich Discord embeds in seconds, `@here` only on steals
- **Snipe (assist)** — T-10-minute "snipe window" reminders with a suggested max bid, plus a Gixen-friendly workflow for true last-second server-side bidding
- **Dashboard** — a neon radar UI at `http://127.0.0.1:8787` with value meters, ticking countdowns, and filters. Loopback-only: nobody else can see it
- **Auto-updates** — checks GitHub Releases on startup, shows you the release notes for every new version, and updates itself only after you say yes (`AUTO_UPDATE=off` in `.env` to disable)

## Install

<p align="center">
  <a href="https://github.com/pasttrunks/EbayDekho/releases/latest/download/EbayDekho.exe">
    <img src="https://img.shields.io/badge/%E2%AC%87%EF%B8%8F%20INSTALL%20NOW-EbayDekho.exe-2ee6a8?style=for-the-badge" alt="Install Now" height="56">
  </a>
</p>

**Windows — the easy way:** download `EbayDekho.exe`, put it wherever you want it to live, double-click. SmartScreen will say "unrecognized app" (unsigned open-source build) → **More info → Run anyway**. Your browser opens to the setup page — no terminal questions, no Python.

**Windows — one-liner (source install):** paste into PowerShell:
```powershell
irm https://raw.githubusercontent.com/pasttrunks/EbayDekho/main/install.ps1 | iex
```
Installs Python if needed, puts EbayDekho in `%USERPROFILE%\EbayDekho`, adds a Desktop shortcut, opens the setup page.

**From source (any OS):**
```bash
git clone https://github.com/pasttrunks/EbayDekho.git
cd EbayDekho
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python ebaydekho.py           # opens the setup page in your browser, then it hunts
```

**Setup happens in your browser.** First run opens a setup page at `127.0.0.1:8787`: name your targets, set dream/good/max prices on a live band preview, list junk words, pick auction vs BIN and category, paste a Discord webhook (there's a test-ping button), choose `notify` or `snipe` mode — then hit **ARM THE RADAR**. It writes `targets.json` + `.env` and the dashboard fades in. That's the whole configuration. (Prefer terminals? `python ebaydekho.py setup` gives you the CLI wizard.)

**No eBay keys?** That's the default, not a problem — Community Mode hunts *real* listings immediately with zero accounts. Free keys from [developer.ebay.com](https://developer.ebay.com/join) are an optional upgrade for officially-sanctioned data (paste into `.env`). Got rejected by the developer program? You're exactly who Community Mode is for. (Want fake listings for a UI demo anyway? `python ebaydekho.py demo`.)

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

- **Reading:** official Browse API when keys exist (5k calls/day budgeted, backs off on 429). Community Mode is read-only, one page at a time with human-ish jitter, ≥15-min sweeps, and a hard 15-min backoff on any robot check — keep it that way; aggressive scraping gets IPs flagged.
- Dashboard binds `127.0.0.1` only; write endpoints are localhost-only; secrets never leave `.env`.
- Bids are binding. EbayDekho never bids; when *you* bid, bid your true max — eBay proxy bidding means you pay second-price + one increment.
- Sniping is allowed by eBay. Automating your account via unofficial means isn't — that's why it's not in this repo.

## License

MIT — see [LICENSE](LICENSE). Not affiliated with eBay Inc. or Discord Inc.
