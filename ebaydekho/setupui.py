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
.wrap{max-width:680px;margin:0 auto;padding:26px 20px 90px}
.hero{text-align:center;padding:14px 0 4px}
.radar{width:52px;height:52px;border-radius:50%;border:1px solid var(--cyan);position:relative;margin:0 auto 12px;box-shadow:inset 0 0 16px rgba(92,214,255,.3),0 0 20px rgba(92,214,255,.25)}
.radar::before,.radar::after{content:"";position:absolute;border-radius:50%;border:1px solid rgba(92,214,255,.35)}
.radar::before{inset:11px}.radar::after{inset:21px;background:var(--cyan);box-shadow:0 0 10px var(--cyan)}
.radar i{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(92,214,255,.55),transparent 70deg);animation:sweep 2.4s linear infinite}
@keyframes sweep{to{transform:rotate(360deg)}}
h1{font-size:22px;letter-spacing:.2em}
.hero p{color:var(--dim);letter-spacing:.26em;font-size:10px;margin-top:5px}
.dots{display:flex;justify-content:center;gap:26px;margin:22px 0 26px}
.dot{display:flex;align-items:center;gap:8px;color:var(--dim);font:700 10px "JetBrains Mono",monospace;letter-spacing:.14em}
.dot i{width:22px;height:22px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;font-style:normal;transition:.3s}
.dot.on{color:var(--cyan)}
.dot.on i{border-color:var(--cyan);box-shadow:0 0 12px rgba(92,214,255,.4);color:var(--cyan)}
.dot.done{color:var(--green)}
.dot.done i{border-color:var(--green);color:var(--green)}
.pane{display:none;animation:fadein .35s}
.pane.on{display:block}
@keyframes fadein{from{opacity:0;transform:translateY(10px)}}
h2{font-size:16px;letter-spacing:.12em;margin-bottom:4px}
.sub{color:var(--dim);font-size:12px;margin-bottom:16px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;backdrop-filter:blur(8px)}
label{display:block;font:700 10px "JetBrains Mono",monospace;letter-spacing:.18em;color:var(--dim);margin:16px 0 5px}
label:first-child{margin-top:0}
.hint{font:11px "Space Grotesk";color:#5d6c94;margin:4px 0 0}
input,select{width:100%;background:#0b1226;border:1px solid var(--line);border-radius:9px;color:var(--txt);padding:10px 12px;font:14px "Space Grotesk";outline:none;transition:.2s;margin-top:4px}
input:focus,select:focus{border-color:var(--cyan);box-shadow:0 0 14px rgba(92,214,255,.18)}
input::placeholder{color:#3d4a6e}
.presets{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.preset{background:rgba(143,123,255,.08);border:1px solid rgba(143,123,255,.4);color:#c4b5fd;border-radius:999px;padding:8px 14px;font:700 12px "Space Grotesk";cursor:pointer;transition:.2s}
.preset:hover{background:rgba(143,123,255,.18);box-shadow:0 0 16px rgba(143,123,255,.25)}
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
.nav{display:flex;gap:10px;margin-top:22px}
.btn-next,.btn-back{border-radius:12px;padding:14px;font:700 14px "Space Grotesk";letter-spacing:.16em;cursor:pointer;transition:.2s}
.btn-next{flex:2;background:linear-gradient(135deg,#1d3f74,#2b6cb0);border:none;color:#eaf2ff}
.btn-next:hover{filter:brightness(1.2);box-shadow:0 0 24px rgba(43,108,176,.4)}
.btn-back{flex:1;background:none;border:1px solid var(--line);color:var(--dim)}
.btn-back:hover{color:var(--txt)}
.cta{flex:2;background:linear-gradient(135deg,#0e5e43,#2ee6a8);border:none;color:#04120c;border-radius:12px;padding:14px;font:700 15px "Space Grotesk";letter-spacing:.2em;cursor:pointer;transition:.25s;box-shadow:0 0 26px rgba(46,230,168,.25)}
.cta:hover{filter:brightness(1.12);box-shadow:0 0 42px rgba(46,230,168,.45)}
.cta:disabled{opacity:.5;cursor:not-allowed}
.modes{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mode{background:#0b1226;border:1px solid var(--line);border-radius:12px;padding:16px;cursor:pointer;transition:.2s}
.mode:hover{border-color:#35508a}
.mode.on{border-color:var(--violet);box-shadow:0 0 24px rgba(143,123,255,.22)}
.mode h3{font-size:14px;letter-spacing:.08em;margin-bottom:6px}
.mode p{color:var(--dim);font-size:12px}
.mode .ic{font-size:20px;display:block;margin-bottom:8px}
.next-box{margin-top:16px;background:rgba(92,214,255,.05);border:1px solid rgba(92,214,255,.25);border-radius:12px;padding:14px 16px}
.next-box h4{font-size:11px;letter-spacing:.18em;color:var(--cyan);margin-bottom:8px}
.next-box li{color:var(--dim);font-size:12px;margin:5px 0 5px 16px}
.next-box b{color:var(--txt)}
.testbtn{margin-top:8px;background:none;border:1px solid var(--line);color:var(--dim);border-radius:8px;padding:7px 14px;font:700 11px "JetBrains Mono",monospace;cursor:pointer}
.testbtn:hover{color:var(--cyan);border-color:var(--cyan)}
.testresult{font:11px "JetBrains Mono",monospace;margin-top:6px;min-height:14px}
details{margin-top:16px}
summary{cursor:pointer;color:var(--dim);font:700 10px "JetBrains Mono",monospace;letter-spacing:.18em}
summary:hover{color:var(--cyan)}
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
<p>SETUP · THREE QUICK STEPS</p>
</div>
<div class=dots>
<span class="dot on" id=d1><i>1</i>TARGETS</span>
<span class=dot id=d2><i>2</i>ALERTS</span>
<span class=dot id=d3><i>3</i>STRIKE</span>
</div>

<!-- ── STEP 1 ─────────────────────────────────────── -->
<section class="pane on" id=p1>
<h2>What are we hunting?</h2>
<p class=sub>Grab a preset to see how it's done, or build your own below — you can add as many targets as you like.</p>
<div class=panel>
<label>QUICK PRESETS</label>
<div class=presets id=presets></div>
<label>TARGET NAME</label>
<input id=t-name placeholder='RTX 4070 · PS5 disc · Sony A7III…'>
<p class=hint>What you'd type into eBay search.</p>
<label>SEARCH KEYWORDS <span style="opacity:.6">(comma-separated)</span></label>
<input id=t-kw placeholder="rtx 4070, 4070">
<p class=hint>Every spelling counts — include squashed variants like <b>4070rtx</b>. Most specific first.</p>
<label>JUNK WORDS <span style="opacity:.6">(titles with these get trashed)</span></label>
<input id=t-avoid placeholder="ti, box, case, digital">
<p class=hint>Example: hunting a plain RX 6800? Put <b>xt</b> here so XT listings don't sneak in.</p>
<div class=prices>
<div><label>DREAM $</label><input id=t-steal type=number min=1 placeholder="300"></div>
<div><label>GOOD $</label><input id=t-good type=number min=1 placeholder="340"></div>
<div><label>MAX $</label><input id=t-max type=number min=1 placeholder="365"></div>
</div>
<p class=hint>Prices are <b>landed</b> (item + shipping). Dream = instant-buy. Max = walk away, no exceptions.</p>
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
<div class=nav><button class=btn-next id=n1>NEXT: ALERTS →</button></div>
<div class=err id=e1></div>
</section>

<!-- ── STEP 2 ─────────────────────────────────────── -->
<section class=pane id=p2>
<h2>Where do alerts go?</h2>
<p class=sub>Both of these are optional — skip them and EbayDekho runs in demo mode with fake listings so you can explore.</p>
<div class=panel>
<label>DISCORD WEBHOOK URL</label>
<input id=c-hook placeholder="https://discord.com/api/webhooks/…">
<p class=hint>In your Discord server: <b>Settings → Integrations → Webhooks → New Webhook → Copy URL</b>. Takes 30 seconds.</p>
<button class=testbtn id=testhook>SEND TEST PING</button>
<div class=testresult id=hookres></div>
<label style="margin-top:18px">EBAY API KEYS <span style="opacity:.6">(free — unlocks LIVE mode)</span></label>
<input id=c-id placeholder="Client ID">
<input id=c-sec type=password placeholder="Client Secret" style="margin-top:8px">
<p class=hint>Get them free at <b>developer.ebay.com</b> → My Account → Application Keys → Production keyset. ~10 min, no approval needed for search.</p>
<button class=testbtn id=testkeys>CHECK KEYS</button>
<div class=testresult id=keyres></div>
</div>
<div class=nav><button class=btn-back id=b2>← BACK</button><button class=btn-next id=n2>NEXT: STRIKE →</button></div>
<div class=err id=e2></div>
</section>

<!-- ── STEP 3 ─────────────────────────────────────── -->
<section class=pane id=p3>
<h2>How do you want to strike?</h2>
<p class=sub>You can change this later by re-running setup.</p>
<div class=modes>
<div class="mode on" data-m="notify"><span class=ic>🔔</span><h3>NOTIFY</h3><p>Discord pings + dashboard. You click through and buy or bid yourself. Simple, zero-risk, recommended for your first week.</p></div>
<div class=mode data-m="snipe"><span class=ic>🎯</span><h3>SNIPE-ASSIST</h3><p>Everything in Notify, plus: <b>10 minutes before an auction ends</b> you get a warning with your exact max bid and a Gixen-ready item number.</p></div>
</div>
<div class=next-box>
<h4>WHAT HAPPENS AFTER YOU ARM IT</h4>
<li><b>Every ~10 min</b> we sweep eBay for your targets and judge every listing against your price bands.</li>
<li><b>Deal found</b> → Discord ping with landed price, seller score, time left. Steals get an <b>@here</b>.</li>
<li><b>Auction ending?</b> Fire the snipe yourself, or paste the item number into <b>Gixen</b> (free, eBay-authorized) and let their servers bid in the last seconds. Group snipes = <b>first win cancels the rest</b> — perfect when you only need one.</li>
</div>
<div class=nav><button class=btn-back id=b3>← BACK</button><button class=cta id=arm>⚡ ARM THE RADAR</button></div>
<div class=err id=e3></div>
</section>
</div>

<div class=overlay id=overlay><div class=box>
<div class=radar style="width:110px;height:110px"><i></i></div>
<h2 id=ov-title>RADAR ARMED</h2>
<p id=ov-sub>switching to live view…</p>
</div></div>

<script>
const $=id=>document.getElementById(id);
let targets=[],fmt="any",cond="used",mode="notify",step=1;

const PRESETS=[
{label:"🎮 Used GPU ≤ $300",targets:[
{name:"RX 6800 XT",keywords:["rx 6800 xt","6800xt","rx6800xt"],avoid:[],steal:285,good:310,max:345,format:"any",condition:"used",category_id:27386},
{name:"RX 6800",keywords:["rx 6800","rx6800","6800 non xt"],avoid:["xt"],steal:265,good:300,max:330,format:"any",condition:"used",category_id:27386},
{name:"RTX 3080",keywords:["rtx 3080","rtx3080","3080 10gb"],avoid:["ti","12gb","laptop"],steal:265,good:300,max:335,format:"any",condition:"used",category_id:27386},
{name:"RX 6700 XT",keywords:["rx 6700 xt","6700xt","rx6700xt"],avoid:[],steal:185,good:225,max:250,format:"any",condition:"used",category_id:27386}]},
{label:"🕹 PS5 Disc",targets:[
{name:"PS5 Disc",keywords:["ps5 disc","playstation 5 disc"],avoid:["digital","box only","controller"],steal:300,good:350,max:400,format:"any",condition:"used"}]},
{label:"🎧 AirPods Pro 2",targets:[
{name:"AirPods Pro 2",keywords:["airpods pro 2","airpods pro 2nd"],avoid:["clone","replica","fake","case only"],steal:120,good:150,max:175,format:"any",condition:"any"}]}];
$("presets").innerHTML=PRESETS.map((p,i)=>`<button class=preset data-i=${i}>${p.label}</button>`).join("");
$("presets").onclick=e=>{const b=e.target.closest(".preset");if(!b)return;
PRESETS[+b.dataset.i].targets.forEach(t=>{if(!targets.some(x=>x.name===t.name))targets.push({...t})});
renderChips();b.textContent="✓ added";setTimeout(()=>b.textContent=PRESETS[+b.dataset.i].label,1500)};

function show(n){step=n;
[1,2,3].forEach(i=>{$("p"+i).classList.toggle("on",i===n);
$("d"+i).className="dot"+(i===n?" on":i<n?" done":"")})}
$("n1").onclick=()=>{if(!targets.length)return $("e1").textContent="add at least one target (or tap a preset)";show(2)};
$("n2").onclick=()=>show(3); $("b2").onclick=()=>show(1); $("b3").onclick=()=>show(2);

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
'<div style="color:var(--dim);font-size:12px;text-align:center;padding:6px">no targets yet — tap a preset above or build your own</div>';
$("chips").querySelectorAll("button").forEach(b=>b.onclick=()=>{targets.splice(+b.dataset.i,1);renderChips()})}
renderChips();

$("add").onclick=()=>{const[s,g,m]=bands();
const name=$("t-name").value.trim();
$("e1").textContent="";
if(!name)return $("e1").textContent="give your target a name";
if(!s||!m)return $("e1").textContent="dream $ and max $ are required";
if(!(s<=(g||m)&&(g||m)<=m))return $("e1").textContent="keep dream ≤ good ≤ max";
targets.push({name,keywords:($("t-kw").value||name).split(",").map(x=>x.trim()).filter(Boolean),
avoid:$("t-avoid").value.split(",").map(x=>x.trim()).filter(Boolean),
steal:s,good:g||Math.round(s+(m-s)*.55),max:m,format:fmt,condition:cond,
...($("t-cat").value?{category_id:+$("t-cat").value}:{})});
["t-name","t-kw","t-avoid","t-steal","t-good","t-max"].forEach(id=>$(id).value="");preview();renderChips()};

$("testhook").onclick=async()=>{$("hookres").textContent="pinging…";
const r=await fetch("/api/discord-test",{method:"POST",body:JSON.stringify({url:$("c-hook").value})}).then(r=>r.json()).catch(()=>({ok:false}));
$("hookres").style.color=r.ok?"var(--green)":"var(--red)";
$("hookres").textContent=r.ok?"✓ pong! check your channel":"✗ failed — check the URL (or leave blank for console alerts)"};

$("testkeys").onclick=async()=>{$("keyres").textContent="checking…";
const r=await fetch("/api/ebay-test",{method:"POST",body:JSON.stringify({id:$("c-id").value.trim(),secret:$("c-sec").value.trim()})}).then(r=>r.json()).catch(()=>({ok:false}));
$("keyres").style.color=r.ok?"var(--green)":"var(--red)";
$("keyres").textContent=r.ok?"✓ keys work — LIVE mode unlocked":"✗ eBay rejected these — double-check both fields"};

$("arm").onclick=async()=>{$("e3").textContent="";
if(!targets.length){show(1);return $("e1").textContent="add at least one target (or tap a preset)"}
$("arm").disabled=true;$("arm").textContent="ARMING…";
const r=await fetch("/api/setup",{method:"POST",body:JSON.stringify({targets,
discord:$("c-hook").value.trim(),client_id:$("c-id").value.trim(),client_secret:$("c-sec").value.trim(),
mode,poll:600})}).then(r=>r.json()).catch(e=>({ok:false,error:String(e)}));
if(!r.ok){$("arm").disabled=false;$("arm").textContent="⚡ ARM THE RADAR";
return $("e3").textContent=r.error||"setup failed — check the console window"}
$("ov-sub").textContent=(r.demo?"DEMO mode (no eBay keys) · ":"LIVE mode · ")+r.targets+" target"+(r.targets>1?"s":"")+" · "+mode;
$("overlay").classList.add("show");
setTimeout(()=>location.href="/",2600)};
</script>"""
