import json, threading, urllib.request, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from . import db, config
from .setupui import SETUP_PAGE

PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>EbayDekho // Deal Radar</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel=stylesheet>
<style>
:root{--bg:#070b16;--panel:rgba(19,26,45,.78);--line:#233052;--txt:#e8eefb;--dim:#7f8cb0;
--green:#2ee6a8;--yellow:#ffd166;--orange:#ff9f5a;--red:#ff5a7a;--cyan:#5cd6ff;--violet:#8f7bff}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--txt);font:14px/1.5 "Space Grotesk",system-ui,sans-serif;min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-2;background:radial-gradient(900px 480px at 85% -10%,rgba(143,123,255,.16),transparent 60%),radial-gradient(820px 520px at -10% 110%,rgba(46,230,168,.10),transparent 60%),var(--bg)}
body::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:linear-gradient(rgba(92,124,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(92,124,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 50% -5%,#000 25%,transparent 78%)}
header{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:16px 22px 12px}
.radar{width:36px;height:36px;border-radius:50%;border:1px solid var(--cyan);position:relative;flex:none;box-shadow:inset 0 0 14px rgba(92,214,255,.3),0 0 12px rgba(92,214,255,.2)}
.radar::before,.radar::after{content:"";position:absolute;border-radius:50%;border:1px solid rgba(92,214,255,.35)}
.radar::before{inset:8px}.radar::after{inset:15px;background:var(--cyan);box-shadow:0 0 8px var(--cyan)}
.radar i{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(92,214,255,.55),transparent 70deg);animation:sweep 2.4s linear infinite}
@keyframes sweep{to{transform:rotate(360deg)}}
h1{font-size:17px;letter-spacing:.14em}
h1 small{display:block;font-size:10px;letter-spacing:.3em;color:var(--dim);font-weight:500}
.badge{margin-left:auto;font:700 11px "JetBrains Mono",monospace;letter-spacing:.12em;padding:5px 12px;border-radius:6px;display:flex;align-items:center;gap:7px;border:1px solid var(--line)}
.badge i{width:7px;height:7px;border-radius:50%;background:currentColor;box-shadow:0 0 8px currentColor;animation:blink 1.6s infinite}
.badge.LIVE{color:var(--green)}.badge.DEMO{color:var(--yellow)}
@keyframes blink{50%{opacity:.25}}
.stats{display:flex;gap:10px;flex-wrap:wrap;padding:0 22px 12px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px 16px;min-width:96px;backdrop-filter:blur(8px)}
.stat b{display:block;font:700 20px "JetBrains Mono",monospace;color:var(--txt)}
.stat span{font-size:10px;letter-spacing:.22em;color:var(--dim)}
.stat.hot b{color:var(--green)}
.cap{margin-left:auto;align-self:center;font:11px "JetBrains Mono",monospace;color:var(--dim);border:1px dashed var(--line);border-radius:999px;padding:5px 12px}
.ticker{overflow:hidden;border-block:1px solid var(--line);background:rgba(9,13,25,.65)}
.ticker-track{display:inline-flex;gap:56px;white-space:nowrap;padding:7px 0;font:11px "JetBrains Mono",monospace;color:var(--dim);animation:scroll 45s linear infinite}
.ticker-track b{color:var(--cyan);font-weight:400}
@keyframes scroll{to{transform:translateX(-50%)}}
.tabs{display:flex;gap:8px;flex-wrap:wrap;padding:14px 22px 0}
.tabs button{background:none;border:1px solid var(--line);color:var(--dim);border-radius:8px;padding:6px 16px;font:700 11px "Space Grotesk";letter-spacing:.14em;cursor:pointer;transition:.2s}
.tabs button:hover{color:var(--txt)}
.tabs button.on{color:var(--bg);background:var(--cyan);border-color:var(--cyan)}
.tabs .sep{width:1px;background:var(--line);margin:0 4px}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;padding:16px 22px 30px}
.card{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:10px;backdrop-filter:blur(8px);animation:pop .45s both;transition:border-color .3s}
.card:hover{border-color:#35508a}
@keyframes pop{from{opacity:0;transform:translateY(14px) scale(.97)}}
.card.new{border-color:var(--cyan);box-shadow:0 0 34px rgba(92,214,255,.22)}
.card.STEAL{border-color:rgba(46,230,168,.5);animation:pop .45s both,glow 2.4s ease-in-out .5s infinite}
@keyframes glow{50%{box-shadow:0 0 30px rgba(46,230,168,.20)}}
.row{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.model{font-weight:700;font-size:15px}
.vram{color:var(--dim);font-size:11px;font-weight:500}
.pill{flex:none;border-radius:6px;padding:3px 9px;font:700 10px "JetBrains Mono",monospace;letter-spacing:.1em}
.pill.STEAL{background:rgba(46,230,168,.14);color:var(--green);box-shadow:inset 0 0 0 1px rgba(46,230,168,.4)}
.pill.GOOD{background:rgba(255,209,102,.12);color:var(--yellow);box-shadow:inset 0 0 0 1px rgba(255,209,102,.35)}
.pill.FAIR{background:rgba(255,159,90,.12);color:var(--orange);box-shadow:inset 0 0 0 1px rgba(255,159,90,.35)}
.pill.SUSPICIOUS{background:rgba(255,90,122,.12);color:var(--red);box-shadow:inset 0 0 0 1px rgba(255,90,122,.35)}
.title{color:var(--dim);font-size:12px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.landed{font:700 26px "JetBrains Mono",monospace}
.sub{font:11px "JetBrains Mono",monospace;color:var(--dim);align-self:flex-end}
.meter{position:relative;height:8px;border-radius:99px;margin-top:2px}
.meter .track{position:absolute;inset:0;border-radius:99px;opacity:.85}
.meter .mark{position:absolute;top:-3px;width:2px;height:14px;background:rgba(232,238,251,.55);border-radius:2px}
.meter .dot{position:absolute;top:50%;width:14px;height:14px;border-radius:50%;transform:translate(-50%,-50%);background:#fff;border:2px solid var(--bg)}
.scale{display:flex;justify-content:space-between;font:10px "JetBrains Mono",monospace;color:var(--dim)}
.scale span:nth-child(1){color:var(--green)}.scale span:nth-child(2){color:var(--yellow)}.scale span:nth-child(3){color:var(--orange)}
.meta{display:flex;justify-content:space-between;font:11px "JetBrains Mono",monospace;color:var(--dim)}
.ends{color:var(--cyan);font-variant-numeric:tabular-nums}
.ends.urgent{color:var(--red);animation:blink 1s infinite}
.note{font-size:11px;color:var(--violet)}
a.btn{background:linear-gradient(135deg,#1d3f74,#2b6cb0);color:#eaf2ff;text-decoration:none;text-align:center;border-radius:9px;padding:9px;font-weight:700;font-size:12px;letter-spacing:.08em;transition:.2s}
a.btn:hover{filter:brightness(1.25);box-shadow:0 4px 18px rgba(43,108,176,.4)}
a.ghost{background:#0b1226!important;border:1px solid var(--line);color:var(--cyan)!important}
a.ghost:hover{border-color:var(--cyan);box-shadow:0 0 14px rgba(92,214,255,.25)}
.btns{display:flex;gap:8px}.btns .btn,.btns .ghost{flex:1}
.bar{display:flex;align-items:center;gap:10px;margin:0 22px 10px;padding:9px 14px;border-radius:10px;font:12px "JetBrains Mono",monospace}
.bar.demo{background:rgba(255,209,102,.08);border:1px solid rgba(255,209,102,.35);color:var(--yellow)}
.bar.help{background:rgba(92,214,255,.06);border:1px solid rgba(92,214,255,.3);color:var(--dim)}
.bar a{color:var(--cyan)}
.bar .x{margin-left:auto;cursor:pointer;color:var(--dim)}
.setuplink{margin-left:10px;font:700 10px "JetBrains Mono",monospace;letter-spacing:.12em;color:var(--dim);text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:5px 10px}
.setuplink:hover{color:var(--cyan);border-color:var(--cyan)}
.empty{grid-column:1/-1;text-align:center;padding:80px 0;color:var(--dim)}
.empty .big{width:120px;height:120px;margin:0 auto 18px}
#toasts{position:fixed;top:16px;right:16px;display:flex;flex-direction:column;gap:8px;z-index:9}
.toast{background:#0d1425;border:1px solid var(--line);border-left:3px solid var(--green);border-radius:10px;padding:10px 14px;font:12px "JetBrains Mono",monospace;box-shadow:0 8px 30px rgba(0,0,0,.5);animation:tin .3s}
.toast b{color:var(--green)}
@keyframes tin{from{opacity:0;transform:translateX(30px)}}
</style>
<header>
<div class=radar><i></i></div>
<h1>EBAYDEKHO<small>EBAY DEAL RADAR</small></h1>
<span class="badge DEMO" id=mode><i></i>DEMO</span>
<a class=setuplink href="/setup">⚙ SETUP</a>
</header>
<div class=stats>
<div class=stat><b id=seen>0</b><span>SCANNED</span></div>
<div class=stat><b id=alerts>0</b><span>ALERTS</span></div>
<div class="stat hot"><b id=steals>0</b><span>STEALS</span></div>
<div class=stat><b id=calls>0</b><span>API CALLS</span></div>
<span class=cap id=modechip></span>
</div>
<div id=bars></div>
<div class=ticker><div class=ticker-track id=ticker><b>///&nbsp;&nbsp;BOOTING RADAR …</b></div></div>
<nav class=tabs id=tabs></nav>
<main id=grid></main>
<div id=toasts></div>
<script>
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=n=>"$"+Number(n).toFixed(2), fmt0=n=>"$"+Math.round(n);
let known=new Set(), first=true, last={items:[],stats:{}}, fVerdict="ALL", fTarget="ALL";

function leftMs(iso){return iso?new Date(iso)-Date.now():null}
function fmtLeft(ms){if(ms==null)return"BIN";if(ms<=0)return"ENDED";
const s=ms/1e3,d=~~(s/86400),h=~~(s%86400/3600),m=~~(s%3600/60),sec=~~(s%60);
return d?d+"d "+h+"h":h?h+"h "+m+"m":m+":"+String(sec).padStart(2,"0")}
function toast(html){const t=document.createElement("div");t.className="toast";t.innerHTML=html;
toasts.appendChild(t);setTimeout(()=>t.remove(),6500)}

function buildTabs(targets){
let h=`<button data-v=ALL class=on>ALL</button><button data-v=STEAL>STEALS</button><button data-v=GOOD>GOOD</button><button data-v=FAIR>FAIR</button>`;
if(targets.length>1)h+=`<span class=sep></span><button data-t=ALL class=on>ALL TARGETS</button>`+targets.map(t=>`<button data-t="${esc(t)}">${esc(t.toUpperCase())}</button>`).join("");
tabs.innerHTML=h}
tabs.onclick=e=>{const b=e.target.closest("button");if(!b)return;
if(b.dataset.v){fVerdict=b.dataset.v;document.querySelectorAll("[data-v]").forEach(x=>x.classList.toggle("on",x==b))}
if(b.dataset.t){fTarget=b.dataset.t;document.querySelectorAll("[data-t]").forEach(x=>x.classList.toggle("on",x==b))}
render()};

function card(i,idx){
const max=i.fair*1.22||400, pc=v=>Math.min(100,v/max*100), dot=Math.min(100,i.landed/max*100);
const col={STEAL:"var(--green)",GOOD:"var(--yellow)",FAIR:"var(--orange)",SUSPICIOUS:"var(--red)"}[i.verdict]||"var(--cyan)";
const grad=`linear-gradient(90deg,var(--green) 0 ${pc(i.steal)}%,var(--yellow) ${pc(i.steal)}% ${pc(i.good)}%,var(--orange) ${pc(i.good)}% ${pc(i.fair)}%,rgba(255,90,122,.30) ${pc(i.fair)}% 100%)`;
const isNew=!first&&!known.has(i.item_id);
if(isNew&&(i.verdict=="STEAL"||i.verdict=="GOOD"))toast(`<b>${i.verdict}</b> · ${esc(i.target)} — ${fmt(i.landed)} landed`);
return`<div class="card ${i.verdict}${isNew?" new":""}" style="animation-delay:${idx*45}ms">
<div class=row><div><div class=model>${esc(i.target)}</div><div class=vram>${esc(i.buying.replace(/,/g," + "))} · ${esc(i.condition||"")}</div></div>
<span class="pill ${i.verdict}">${i.verdict}</span></div>
<div class=title>${esc(i.title)}</div>
<div class=row><span class=landed>${fmt(i.landed)}</span><span class=sub>${fmt(i.price)} + ${fmt(i.shipping)} ship</span></div>
<div><div class=meter><div class=track style="background:${grad}"></div>
<i class=mark style="left:${pc(i.steal)}%"></i><i class=mark style="left:${pc(i.good)}%"></i><i class=mark style="left:${pc(i.fair)}%"></i>
<i class=dot style="left:${dot}%;background:${col};box-shadow:0 0 10px ${col}"></i></div>
<div class=scale><span>steal ${fmt0(i.steal)}</span><span>good ${fmt0(i.good)}</span><span>max ${fmt0(i.fair)}</span></div></div>
<div class=meta><span class="ends${leftMs(i.end_time)!=null&&leftMs(i.end_time)<6e5?" urgent":""}" data-end="${i.end_time||""}">${fmtLeft(leftMs(i.end_time))}</span>
<span>${i.bids?i.bids+" bids · ":""}${i.fb_pct}% · ${i.fb_count}fb</span></div>
${i.note?`<div class=note>◈ ${esc(i.note)}</div>`:""}
<div class=btns><a class=btn href="${esc(i.url)}" target=_blank>OPEN ON EBAY ↗</a>
${i.buying.includes("AUCTION")&&i.end_time?`<a class="btn ghost" href="#" onclick="copyGixen(event,'${esc(i.legacy_id||i.item_id)}',${(Math.min(i.fair-i.shipping,i.fair)-0.01).toFixed(2)})">⌁ GIXEN</a>`:""}</div></div>`}

function copyGixen(e,id,max){e.preventDefault();
navigator.clipboard.writeText(id);
toast(`⌁ item # <b>${id}</b> copied — set max <b>$${max}</b> at gixen.com · group it = first win cancels the rest`)}

function render(){
const items=last.items.filter(i=>(fVerdict=="ALL"||i.verdict==fVerdict)&&(fTarget=="ALL"||i.target==fTarget));
grid.innerHTML=items.length?items.map(card).join(""):`<div class=empty><div class="radar big"><i></i></div>SWEEPING THE BAY — no qualifying deals yet.</div>`;
const t=last.items.slice(0,8).map(i=>`<b>${i.verdict}</b> ${esc(i.target)} ${fmt(i.landed)}`).join("&nbsp;&nbsp;///&nbsp;&nbsp;");
ticker.innerHTML=(t||"<b>///&nbsp;&nbsp;SCANNING …</b>")+"&nbsp;&nbsp;///&nbsp;&nbsp;"+(t||"<b>SCANNING …</b>");
document.title=(last.stats.steals?`(${last.stats.steals}) `:"")+"EbayDekho // Deal Radar"}

let tabsBuilt=false;
async function tick(){try{const j=await(await fetch("/api/items")).json();
if(!j.configured){location.reload();return}
mode.textContent=j.mode;mode.className="badge "+j.mode;mode.innerHTML="<i></i>"+j.mode;
modechip.textContent=j.mode_label;
bars.innerHTML=(j.mode=="DEMO"?`<div class="bar demo">⚠ DEMO MODE — listings are fake. Add your free eBay keys in <a href="/setup">SETUP</a> to go live.</div>`:"")
+(!localStorage.ed_help?`<div class="bar help">HOW IT WORKS ▸ we sweep eBay every ~10 min → Discord ping when a deal matches your bands → auctions: be in the Discord thread at the snipe window.<span class=x onclick="localStorage.ed_help=1;this.parentElement.remove()">✕</span></div>`:"");
seen.textContent=j.stats.seen;alerts.textContent=j.stats.alerts;steals.textContent=j.stats.steals;calls.textContent=j.stats.calls;
if(!tabsBuilt){buildTabs(j.targets);tabsBuilt=true}
last=j;render();j.items.forEach(i=>known.add(i.item_id));first=false}catch(e){}}
setInterval(()=>{document.querySelectorAll(".ends[data-end]").forEach(el=>{const ms=leftMs(el.dataset.end||null);
el.textContent=fmtLeft(ms);el.classList.toggle("urgent",ms!=null&&ms<6e5&&ms>0)})},1000);
tick();setInterval(tick,15000);
</script>"""

def _configured():
    return bool(config.load_targets())

def _write_config(p):
    (config.TARGETS_FILE).write_text(json.dumps({"targets": p["targets"]}, indent=2))
    env = config.ROOT / ".env"
    env.write_text("\n".join([
        f"EBAY_CLIENT_ID={p.get('client_id', '')}", f"EBAY_CLIENT_SECRET={p.get('client_secret', '')}",
        f"DISCORD_WEBHOOK_URL={p.get('discord', '')}", f"MODE={p.get('mode', 'notify')}",
        f"POLL_SECONDS={int(p.get('poll', 600))}", "ZIP_CODE=", "MIN_FEEDBACK=10", "PORT=8787",
    ]) + "\n")
    # hot-apply to the running process
    config.EBAY_CLIENT_ID = p.get("client_id", "")
    config.EBAY_CLIENT_SECRET = p.get("client_secret", "")
    config.DISCORD_WEBHOOK_URL = p.get("discord", "")
    config.MODE = p.get("mode", "notify")
    config.DEMO = not (config.EBAY_CLIENT_ID and config.EBAY_CLIENT_SECRET)

def _validate_targets(targets):
    if not isinstance(targets, list) or not targets:
        return "need at least one target"
    for t in targets:
        if not t.get("name"): return "every target needs a name"
        try:
            s, m = float(t["steal"]), float(t["max"])
            g = float(t.get("good") or m)
        except (KeyError, ValueError, TypeError):
            return f"bad prices on {t.get('name', '?')}"
        if not (0 < s <= g <= m): return f"keep dream ≤ good ≤ max on {t['name']}"
        t["steal"], t["good"], t["max"] = s, g, m
        t.setdefault("keywords", [t["name"]]); t.setdefault("avoid", [])
        t.setdefault("format", "any"); t.setdefault("condition", "any")
    return None

class H(BaseHTTPRequestHandler):
    log_message = lambda *a: None

    def _send(self, body, ctype="application/json", code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/items"):
            targets = config.load_targets()
            data = db.recent()
            data.update(configured=_configured(),
                mode="DEMO" if config.DEMO else "LIVE",
                mode_label=f"{len(targets)} TARGETS · MODE: {config.MODE.upper()}" + (" · SNIPE-ASSIST ON" if config.MODE == "snipe" else ""),
                targets=sorted({t["name"] for t in targets}))
            self._send(json.dumps(data).encode())
        elif self.path.startswith("/api/state"):
            self._send(json.dumps({"configured": _configured()}).encode())
        elif self.path.startswith("/setup"):
            self._send(SETUP_PAGE.encode(), "text/html; charset=utf-8")
        elif _configured():
            self._send(PAGE.encode(), "text/html; charset=utf-8")
        else:
            self._send(SETUP_PAGE.encode(), "text/html; charset=utf-8")

    def do_POST(self):
        try:
            p = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except Exception:
            return self._send(b'{"ok":false,"error":"bad json"}', code=400)
        if self.path.startswith("/api/ebay-test"):
            import base64, httpx as _h
            auth = base64.b64encode(f"{p.get('id', '')}:{p.get('secret', '')}".encode()).decode()
            try:
                r = _h.post(config.TOKEN_URL, headers={"Authorization": f"Basic {auth}"},
                    data={"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}, timeout=12)
                return self._send(json.dumps({"ok": r.status_code == 200}).encode())
            except Exception:
                return self._send(b'{"ok":false}')
        if self.path.startswith("/api/discord-test"):
            url = p.get("url", "")
            if not url.startswith("https://discord.com/api/webhooks/"):
                return self._send(b'{"ok":false}')
            try:
                req = urllib.request.Request(url, headers={"Content-Type": "application/json"},
                    data=json.dumps({"username": "EbayDekho", "content": "🎯 EbayDekho connected — alerts will land here."}).encode())
                urllib.request.urlopen(req, timeout=10)
                return self._send(b'{"ok":true}')
            except Exception:
                return self._send(b'{"ok":false}')
        if self.path.startswith("/api/setup"):
            err = _validate_targets(p.get("targets"))
            if err: return self._send(json.dumps({"ok": False, "error": err}).encode(), code=400)
            try:
                _write_config(p)
            except Exception as e:
                return self._send(json.dumps({"ok": False, "error": str(e)}).encode(), code=500)
            print(f"[setup] {len(p['targets'])} targets armed via web UI · mode={config.MODE} · demo={config.DEMO}", flush=True)
            return self._send(json.dumps({"ok": True, "demo": config.DEMO, "targets": len(p["targets"])}).encode())
        self._send(b'{"ok":false}', code=404)

def start(open_browser=True):
    server = ThreadingHTTPServer(("127.0.0.1", config.PORT), H)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{config.PORT}")).start()
    return config.PORT
