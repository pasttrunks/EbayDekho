import os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def _load_dotenv():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_load_dotenv()

EBAY_CLIENT_ID = os.environ.get("EBAY_CLIENT_ID", "")
EBAY_CLIENT_SECRET = os.environ.get("EBAY_CLIENT_SECRET", "")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
ZIP_CODE = os.environ.get("ZIP_CODE", "")
POLL_SECONDS = int(os.environ.get("POLL_SECONDS", "600"))
MODE = os.environ.get("MODE", "notify")            # notify | snipe
MIN_FEEDBACK = int(os.environ.get("MIN_FEEDBACK", "10"))
PORT = int(os.environ.get("PORT", "8787"))

DEMO = not (EBAY_CLIENT_ID and EBAY_CLIENT_SECRET)

API_BASE = "https://api.ebay.com"
TOKEN_URL = f"{API_BASE}/identity/v1/oauth2/token"
SEARCH_URL = f"{API_BASE}/buy/browse/v1/item_summary/search"

TARGETS_FILE = ROOT / "targets.json"

def load_targets():
    if not TARGETS_FILE.exists():
        return []
    return json.loads(TARGETS_FILE.read_text())["targets"]

# junk that almost never is the item itself
GLOBAL_EXCLUDE = [
    "box only", "empty box", "picture", "jpeg", "digital download", "read description",
    "for parts", "parts only", "not working", "as-is", "as is", "broken", "for repair",
    "sticker", "lego", "framed", "preorder", "pre-order", "manual only", "case only",
]

ALERT_VERDICTS = {"STEAL", "GOOD"}   # FAIR -> dashboard only
