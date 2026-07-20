SETUP_PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>EbayDekho — Setup</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel=stylesheet>
<style>
:root{--bg:#070b16;--panel:rgba(19,26,45,.78);--line:#233052;--txt:#e8eefb;--dim:#7f8cb0;
--green:#2ee6a8;--yellow:#ffd166;--orange:#ff9f5a;--red:#ff5a7a;--cyan:#5cd6ff;--violet:#8f7bff}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--txt);font:14px/1.55 "Space Grotesk",system-ui,sans-serif;min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-2;background:radial-gradient(900px 480px at 85% -10%,rgba(143,123,255,.18),transparent 60%),radial-gradient(820px 520px at -10% 110%,rgba(46,230,168,.12),transparent 60%),var(--bg)}
body::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:linear-gradient(rgba(92,124,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(92,124,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 50% -5%,#000 25%,transparent 78%)}
.wrap{max-width:720px;margin:0 auto;padding:28px 20px 90px}
.hero{text-align:center;padding:26px 0 8px}
.radar{width:64px;height:64px;border-radius:50%;border:1px solid var(--cyan);position:relative;margin:0 auto 14px;box-shadow:inset 0 0 20px rgba(92,214,255,.3),0 0 24px rgba(92,214,255,.25)}
.radar::before,.radar::after{content:"";position:absolute;border-radius:50%;border:1px solid rgba(92,214,255,.35)}
.radar::before{inset:14px}.radar::after{inset:26px;background:var(--cyan);box-shadow:0 0 12px var(--cyan)}
.radar i{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(92,214,255,.55),transparent 70deg);animation:sweep 2.4s linear infinite}
@keyframes sweep{to{transform:rotate(360deg)}}
h1{font-size:26px;letter-spacing:.2em}
.hero p{color:var(--dim);letter-spacing:.28em;font-size:11px;margin-top:6px}
.step{margin-top:34px}
.step-head{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.step-num{width:28px;height:28px;flex:none;border-radius:8px;border:1px solid var(--cyan);color:var(--cyan);display:grid;place-items:center;font:700 13px "JetBrains Mono",monospace;box-shadow:0 0 12px rgba(92,214,255,.25)}
.step-head h2{font-size:15px;letter-spacing:.14em}
.step-head span{color:var(--dim);font-size:12px;margin-left:auto}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;backdrop-filter:blur(8px)}
label{display:block;font:700 10px "JetBrains Mono",monospace;letter-spacing:.18em;color:var(--dim);margin:14px 0 5px}
label:first-child{margin-top:0}
input,select{width:100%;background:#0b1226;border:1px solid var(--line);border-radius:9px;color:var(--txt);padding:10px 12px;font:14px "Space Grotesk";outline:none;transition:.2s}
input:focus,select:focus{border-color:var(--cyan);box-shadow:0 0 14px rgba(92,214,255,.18)}
input::placeholder{color:#3d4a6e}
.prices{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.prices label{margin-top:0}
.prices input{font:700 15px "JetBrains Mono",monospace}
.bandprev{margin-top:16px}
.meter{position:relative;height:10px;border-radius:99px;background:linear-gradient(90deg,var(--green) 0 var(--ps,30%),var(--yellow) var(--ps,30%) var(--pg,60%),var(--orange) var(--pg,60%) var(--pm,85%),rgba(255,90,122,.3) var(--pm,85%) 100%)}
.meter .mark{position:absolute;top:-4px;width:2px;height:18px;background:rgba(232,238,251,.6);border-radius:2px}
.bandlabels{display:flex;justify-content:space-between;font:10px "JetBrains Mono",monospace;color:var(--dim);margin-top:6px}
.bandlabels span:nth-child(1){color:var(--green)}.bandlabels span:nth-child(2){color:var(--yellow)}.bandlabels span:nth-child(3){color:var(--orange)}
.seg{display:flex;gap:8px}
.seg button{flex:1;background:#0b1226;border:1px solid var(--line);color:var(--dim);border-radius:9px;padding:9px;font:700 11px "Space Grotesk";letter-spacing:.1em;cursor:pointer;transition:.15s}
.seg button.on{color:var(--bg);background:var(--cyan);border-color:var(--cyan)}
.addbtn{width:100%;margin-top:16px;background:none;border:1px dashed var(--cyan);color:var(--cyan);border-radius:10px;padding:11px;font:700 12px "Space Grotesk";letter-spacing:.12em;cursor:pointer;transition:.2s}
.addbtn:hover{background:rgba(92,214,255,.08);box-shadow:0 0 18px rgba(92,214,255,.15)}
.chips{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.chip{display:flex;align-items:center;gap:10px;background:rgba(46,230,168,.06);border:1px solid rgba(46,230,168,.35);border-radius:10px;padding:10px 14px;animation:pop .3s}
@keyframes pop{from{opacity:0;transform:translateY(8px)}}
.chip b{flex:1}.chip span{font:11px "JetBrains Mono",monospace;color:var(--dim)}
.chip button{background:none;border:none;color:var(--red);font-size:16px;cursor:pointer}
.modes{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mode{background:#0b1226;border:1px solid var(--line);border-radius:12px;padding:16px;cursor:pointer;transition:.2s}
.mode:hover{border-color:#35508a}
.mode.on{border-color:var(--violet);box-shadow:0 0 24px rgba(143,123,255,.22)}
.mode h3{font-size:14px;letter-spacing:.08em;margin-bottom:6px}
.mode p{color:var(--dim);font-size:12px}
.mode .ic{font-size:20px;display:block;margin-bottom:8px}
.testbtn{margin-top:6px;background:none;border:1px solid var(--line);color:var(--dim);border-radius:8px;padding:7px 14px;font:700 11px "JetBrains Mono",monospace;cursor:pointer}
.testbtn:hover{color:var(--cyan);border-color:var(--cyan)}
.testresult{font:11px "JetBrains Mono",monospace;margin-top:6px;min-height:14px}
details{margin-top:14px}
summary{cursor:pointer;color:var(--dim);font:700 10px "JetBrains Mono",monospace;letter-spacing:.18em}
summary:hover{color:var(--cyan)}
.cta{width:100%;margin-top:36px;background:linear-gradient(135deg,#0e5e43,#2ee6a8);border:none;color:#04120c;border-radius:14px;padding:18px;font:700 17px "Space Grotesk";letter-spacing:.22em;cursor:pointer;transition:.25s;box-shadow:0 0 30px rgba(46,230,168,.25)}
.cta:hover{filter:brightness(1.12);box-shadow:0 0 46px rgba(46,230,168,.45);transform:translateY(-1px)}
.cta:disabled{opacity:.5;cursor:not-allowed;transform:none}
.err{color:var(--red);font:12px "JetBrains Mono",monospace;margin-top:10px;text-align:center;min-height:16px}
.overlay{position:fixed;inset:0;background:rgba(7,11,22,.92);display:none;place-items:center;z-index:9;backdrop-filter:blur(6px)}
.overlay.show{display:grid}
.overlay .box{text-align:center}
.overlay h2{margin:18px 0 6px;letter-spacing:.2em}
.overlay p{color:var(--dim);font:12px "JetBrains Mono",monospace}
</style>
<div class=wrap>
<div class=hero>
<div class=radar><i></i></div>
<h1>EBAY DEKHO</h1>
<p>LET'S BUILD YOUR HIT LIST</p>
</div>

<div class=step>
<div class=step-head><span class=step-num>1</span><h2>WHAT ARE YOU HUNTING?</h2><span>add as many as you like</span></div>
<div class=panel>
<label>TARGET NAME</label>
<input id=t-name placeholder='RTX 4070 · PS5 disc · Sony A7III · Jordan 1 Chicago…'>
<label>SEARCH KEYWORDS <span style="opacity:.6">(comma-separated, most specific first)</span></label>
<input id=t-kw placeholder="rtx 4070, 4070">
<label>JUNK WORDS <span style="opacity:.6">(titles containing these get trashed)</span></label>
<input id=t-avoid placeholder="ti, box, case, digital">
<div class=prices>
<div><label>DREAM $</label><input id=t-steal type=number min=1 placeholder="300"></div>
<div><label>GOOD $</label><input id=t-good type=number min=1 placeholder="340"></div>
<div><label>MAX $</label><input id=t-max type=number min=1 placeholder="365"></div>
</div>
<div class=bandprev><div class=meter id=meter>
<i class=mark id=m1></i><i class=mark id=m2></i><i class=mark id=m3></i></div>
<div class=bandlabels><span>◂ steal zone</span><span>good zone</span><span>walk away ▸</span></div></div>
<label>BUYING FORMAT</label>
<div class=seg id=seg-fmt><button data-v="any" class=on>ANYTHING</button><button data-v="auction">AUCTIONS</button><button data-v="bin">BUY IT NOW</button></div>
<label>CONDITION</label>
<div class=seg id=seg-cond><button data-v="used" class=on>USED</button><button data-v="new">NEW</button><button data-v="any">ANY</button></div>
<label>CATEGORY</label>
<select id=t-cat>
<option value="">All categories</option>
<option value=27386>Graphics / Video Cards</option>
<option value=164>CPUs / Processors</option>
<option value=139971>Video Game Consoles</option>
<option value=9355>Cell Phones</option>
<option value=31388>Digital Cameras</option>
<option value=175672>Laptops</option>
<option value=170083>Computer RAM</option>
</select>
<button class=addbtn id=add>+ ADD THIS TARGET</button>
<div class=chips id=chips></div>
</div>
</div>

<div class=step>
<div class=step-head><span class=step-num>2</span><h2>CONNECTIONS</h2><span>both optional</span></div>
<div class=panel>
<label>DISCORD WEBHOOK URL <span style="opacity:.6">(alerts land here)</span></label>
<input id=c-hook placeholder="https://discord.com/api/webhooks/…">
<button class=testbtn id=testhook>SEND TEST PING</button>
<div class=testresult id=hookres></div>
<details><summary>EBAY API KEYS — blank = DEMO MODE</summary>
<label>CLIENT ID</label><input id=c-id placeholder="leave blank for demo mode">
<label>CLIENT SECRET</label><input id=c-sec type=password>
<p style="color:var(--dim);font-size:11px;margin-top:8px">Free at developer.ebay.com → My Account → Application Keys → Production keyset.</p>
</details>
</div>
</div>

<div class=step>
<div class=step-head><span class=step-num>3</span><h2>HOW DO YOU WANT TO STRIKE?</h2></div>
<div class=modes>
<div class="mode on" data-m="notify"><span class=ic>🔔</span><h3>NOTIFY</h3><p>Discord pings + dashboard. You click, you buy. Safe &amp; simple.</p></div>
<div class=mode data-m="snipe"><span class=ic>🎯</span><h3>SNIPE-ASSIST</h3><p>Plus a T-10min warning with your exact max bid, ready to fire.</p></div>
</div>
</div>

<button class=cta id=arm>⚡ ARM THE RADAR</button>
<div class=err id=err></div>
</div>

<div class=overlay id=overlay><div class=box>
<div class=radar style="width:110px;height:110px"><i></i></div>
<h2 id=ov-title>RADAR ARMED</h2>
<p id=ov-sub>switching to live view…</p>
</div></div>

<script>
const $=id=>document.getElementById(id);
let targets=[],fmt="any",cond="used",mode="notify";

function seg(el,cb){el.querySelectorAll("button").forEach(b=>b.onclick=()=>{
el.querySelectorAll("button").forEach(x=>x.classList.remove("on"));b.classList.add("on");cb(b.dataset.v)})}
seg($("seg-fmt"),v=>fmt=v); seg($("seg-cond"),v=>cond=v);
document.querySelectorAll(".mode").forEach(m=>m.onclick=()=>{
document.querySelectorAll(".mode").forEach(x=>x.classList.remove("on"));m.classList.add("on");mode=m.dataset.m});

function bands(){return[+($("t-steal").value||0),+($("t-good").value||0),+($("t-max").value||0)]}
function preview(){const[s,g,m]=bands(),top=Math.max(m,1)*1.18;
$("meter").style.setProperty("--ps",s/top*100+"%");$("meter").style.setProperty("--pg",g/top*100+"%");$("meter").style.setProperty("--pm",m/top*100+"%");
$("m1").style.left=s/top*100+"%";$("m2").style.left=g/top*100+"%";$("m3").style.left=m/top*100+"%"}
["t-steal","t-good","t-max"].forEach(id=>$(id).oninput=preview);preview();

function renderChips(){$("chips").innerHTML=targets.map((t,i)=>
`<div class=chip><b>${t.name}</b><span>steal $${t.steal} · good $${t.good} · max $${t.max}</span>
<span>${t.format} · ${t.condition}</span><button data-i=${i}>×</button></div>`).join("")||
'<div style="color:var(--dim);font-size:12px;text-align:center;padding:6px">no targets yet — the radar hunts nothing without them</div>';
$("chips").querySelectorAll("button").forEach(b=>b.onclick=()=>{targets.splice(+b.dataset.i,1);renderChips()})}
renderChips();

$("add").onclick=()=>{const[s,g,m]=bands();
const name=$("t-name").value.trim();
$("err").textContent="";
if(!name)return $("err").textContent="give your target a name";
if(!s||!m)return $("err").textContent="dream $ and max $ are required";
if(!(s<=(g||m)&& (g||m)<=m))return $("err").textContent="keep dream ≤ good ≤ max";
targets.push({name,keywords:($("t-kw").value||name).split(",").map(x=>x.trim()).filter(Boolean),
avoid:$("t-avoid").value.split(",").map(x=>x.trim()).filter(Boolean),
steal:s,good:g||Math.round(s+(m-s)*.55),max:m,format:fmt,condition:cond,
...($("t-cat").value?{category_id:+$("t-cat").value}:{})});
["t-name","t-kw","t-avoid","t-steal","t-good","t-max"].forEach(id=>$(id).value="");preview();renderChips()};

$("testhook").onclick=async()=>{$("hookres").textContent="pinging…";
const r=await fetch("/api/discord-test",{method:"POST",body:JSON.stringify({url:$("c-hook").value})}).then(r=>r.json()).catch(()=>({ok:false}));
$("hookres").style.color=r.ok?"var(--green)":"var(--red)";
$("hookres").textContent=r.ok?"✓ pong! check your channel":"✗ failed — check the URL (or leave blank)"};

$("arm").onclick=async()=>{$("err").textContent="";
if(!targets.length)return $("err").textContent="add at least one target first";
$("arm").disabled=true;$("arm").textContent="ARMING…";
const r=await fetch("/api/setup",{method:"POST",body:JSON.stringify({targets,
discord:$("c-hook").value.trim(),client_id:$("c-id").value.trim(),client_secret:$("c-sec").value.trim(),
mode,poll:600})}).then(r=>r.json()).catch(e=>({ok:false,error:String(e)}));
if(!r.ok){$("arm").disabled=false;$("arm").textContent="⚡ ARM THE RADAR";
return $("err").textContent=r.error||"setup failed — check the console window"}
$("ov-sub").textContent=(r.demo?"DEMO mode (no eBay keys) · ":"LIVE mode · ")+r.targets+" target"+(r.targets>1?"s":"")+" · mode: "+mode;
$("overlay").classList.add("show");
setTimeout(()=>location.href="/",2400)};
</script>"""
