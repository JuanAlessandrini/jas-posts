import base64, json, sys, pathlib

HERE = pathlib.Path(__file__).parent
logo = base64.b64encode((HERE / "logo_white.png").read_bytes()).decode()

C = dict(bg1="#0B171D", bg2="#162932", g1="#55C596", g2="#7CE395", teal="#349D9E", ink="#162932")

ILL = {}

ILL["ai"] = """
<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">
 <defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7CE395" stop-opacity=".55"/><stop offset="1" stop-color="#7CE395" stop-opacity="0"/></radialGradient>
  <linearGradient id="star" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7CE395"/><stop offset="1" stop-color="#349D9E"/></linearGradient>
 </defs>
 <g stroke="#349D9E" stroke-opacity=".55" stroke-width="2">
  __EDGES__
 </g>
 <g>__NODES__</g>
 <circle cx="480" cy="260" r="210" fill="url(#glow)"/>
 <path d="M480 120 C495 215 525 245 620 260 C525 275 495 305 480 400 C465 305 435 275 340 260 C435 245 465 215 480 120Z" fill="url(#star)"/>
 <path d="M480 175 C489 233 507 251 565 260 C507 269 489 287 480 345 C471 287 453 269 395 260 C453 251 471 233 480 175Z" fill="#0B171D" opacity=".35"/>
 <g font-family="Inter" font-weight="700" fill="#7CE395" font-size="22">
  <rect x="700" y="70" rx="14" width="200" height="56" fill="#162932" stroke="#55C596"/>
  <text x="800" y="106" text-anchor="middle">1M tokens</text>
  <rect x="60" y="390" rx="14" width="220" height="56" fill="#162932" stroke="#55C596"/>
  <text x="170" y="426" text-anchor="middle">DeepSWE 77,9%</text>
 </g>
</svg>"""

import random
random.seed(7)
nodes = [(random.randint(40, 920), random.randint(30, 490)) for _ in range(26)]
nodes = [n for n in nodes if (n[0]-480)**2 + (n[1]-260)**2 > 170**2]
edges = []
for i, a in enumerate(nodes):
    d = sorted(nodes, key=lambda b: (a[0]-b[0])**2 + (a[1]-b[1])**2)[1:3]
    for b in d:
        edges.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
    edges.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="480" y2="260" stroke-opacity=".18"/>') if i % 3 == 0 else None
ILL["ai"] = ILL["ai"].replace("__EDGES__", "".join(edges)).replace(
    "__NODES__", "".join(f'<circle cx="{x}" cy="{y}" r="{6 if i%4 else 9}" fill="{"#7CE395" if i%3 else "#55C596"}"/>' for i, (x, y) in enumerate(nodes)))

# Wafer + rising bars (ASML)
cells = []
for r in range(-6, 7):
    for c in range(-6, 7):
        x, y = 300 + c*30, 260 + r*30
        if (c*30)**2 + (r*30)**2 < 190**2:
            op = .35 + .6*((c+r) % 3 == 0)
            cells.append(f'<rect x="{x-13}" y="{y-13}" width="26" height="26" rx="3" fill="#55C596" opacity="{op:.2f}"/>')
bars = []
vals = [120, 160, 185, 230, 300]
for i, v in enumerate(vals):
    x = 600 + i*62
    bars.append(f'<rect x="{x}" y="{440-v}" width="44" height="{v}" rx="8" fill="{"#7CE395" if i==4 else "#349D9E"}"/>')
ILL["chip"] = f"""
<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">
 <defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7CE395" stop-opacity="0"/><stop offset="1" stop-color="#7CE395" stop-opacity=".55"/></linearGradient></defs>
 <polygon points="270,0 330,0 360,250 240,250" fill="url(#beam)"/>
 <circle cx="300" cy="260" r="205" fill="#162932" stroke="#55C596" stroke-width="4"/>
 <path d="M282 462 h36 l-18 10z" fill="#55C596"/>
 {''.join(cells)}
 <line x1="580" y1="440" x2="920" y2="440" stroke="#55C596" stroke-opacity=".5" stroke-width="2"/>
 {''.join(bars)}
 <polyline points="622,300 684,262 746,236 808,190 870,120" fill="none" stroke="#7CE395" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M870 120 l-26 4 l18 18z" fill="#7CE395"/>
 <text x="750" y="490" text-anchor="middle" font-family="Inter" font-weight="700" font-size="24" fill="#7CE395">€11,7 mil M · récord Q3</text>
</svg>"""

# Memory module + falling line (CXMT)
chips = "".join(f'<rect x="{150+i*112}" y="190" width="86" height="96" rx="8" fill="#0B171D" stroke="#349D9E" stroke-width="3"/><rect x="{165+i*112}" y="205" width="56" height="12" rx="3" fill="#55C596" opacity=".6"/>' for i in range(6))
pins = "".join(f'<rect x="{150+i*16}" y="318" width="9" height="30" fill="#7CE395"/>' for i in range(42) if i != 20)
ILL["mem"] = f"""
<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">
 <rect x="120" y="160" width="720" height="190" rx="18" fill="#162932" stroke="#55C596" stroke-width="4"/>
 {chips}{pins}
 <rect x="465" y="318" width="20" height="40" fill="#162932"/>
 <polyline points="600,40 680,75 740,60 820,110 900,130" fill="none" stroke="#7CE395" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M905 132 l-18 -26 l-14 26z" fill="#7CE395"/>
 <g font-family="Inter" font-weight="800" font-size="30" fill="#7CE395">
  <text x="140" y="430">MU −4%</text><text x="400" y="430">SK Hynix −4%</text><text x="720" y="430">WDC −2%</text>
 </g>
 <text x="140" y="105" font-family="Inter" font-weight="800" font-size="40" fill="#fff">DRAM</text>
 <text x="140" y="138" font-family="Inter" font-weight="500" font-size="22" fill="#55C596">memoria para servidores de IA</text>
</svg>"""

# Obelisco + calendar (Tecweek)
win = "".join(f'<rect x="{x}" y="{y}" width="14" height="20" rx="2" fill="#55C596" opacity="{.25 + .5*((x+y)%3==0):.2f}"/>' for x in range(70, 330, 40) for y in range(250, 460, 44))
win2 = "".join(f'<rect x="{x}" y="{y}" width="14" height="20" rx="2" fill="#55C596" opacity="{.25 + .5*((x*y)%5==0):.2f}"/>' for x in range(660, 900, 40) for y in range(220, 460, 44))
ILL["event"] = f"""
<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">
 <defs><linearGradient id="ob" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#55C596"/><stop offset="1" stop-color="#349D9E"/></linearGradient>
 <radialGradient id="g2" cx="50%" cy="40%" r="50%"><stop offset="0" stop-color="#7CE395" stop-opacity=".35"/><stop offset="1" stop-color="#7CE395" stop-opacity="0"/></radialGradient></defs>
 <circle cx="480" cy="210" r="260" fill="url(#g2)"/>
 <rect x="50" y="230" width="300" height="250" rx="6" fill="#162932"/>{win}
 <rect x="640" y="200" width="280" height="280" rx="6" fill="#162932"/>{win2}
 <polygon points="480,30 505,80 520,480 440,480 455,80" fill="url(#ob)"/>
 <polygon points="480,30 505,80 455,80" fill="#7CE395"/>
 <rect x="455" y="300" width="50" height="40" fill="#0B171D" opacity=".35"/>
 <line x1="20" y1="480" x2="940" y2="480" stroke="#55C596" stroke-width="3"/>
 <g transform="translate(560,40)">
  <rect width="170" height="150" rx="16" fill="#0B171D" stroke="#7CE395" stroke-width="3"/>
  <rect width="170" height="44" rx="16" fill="#7CE395"/><rect y="28" width="170" height="16" fill="#7CE395"/>
  <text x="85" y="32" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" fill="#0B171D">OCTUBRE</text>
  <text x="85" y="118" text-anchor="middle" font-family="Inter" font-weight="800" font-size="52" fill="#fff">20–31</text>
 </g>
</svg>"""

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:#fff;
 background:radial-gradient(1200px 700px at 85% -10%, rgba(52,157,158,.35), transparent 60%),
 radial-gradient(900px 600px at -10% 110%, rgba(85,197,150,.22), transparent 60%), linear-gradient(160deg,#0B171D,#162932);}
.grid{position:absolute;inset:0;background-image:radial-gradient(rgba(124,227,149,.13) 1.5px,transparent 1.5px);background-size:36px 36px;}
.wrap{position:relative;padding:56px 60px 0 60px;height:100%}
header{display:flex;align-items:center;justify-content:space-between}
header img{height:60px}
.chip{display:flex;gap:12px;align-items:center}
.tag{background:rgba(124,227,149,.14);border:2px solid #55C596;color:#7CE395;font-weight:800;font-size:22px;letter-spacing:2px;padding:10px 20px;border-radius:40px;text-transform:uppercase}
.num{background:#1d3a3b;color:#fff;font-weight:700;font-size:22px;padding:10px 16px;border-radius:14px}
.ill{margin-top:40px;height:520px;border-radius:32px;background:linear-gradient(180deg,rgba(22,41,50,.9),rgba(11,23,29,.9));border:2px solid rgba(85,197,150,.35);overflow:hidden;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.ill svg{width:100%;height:100%}
.kicker{margin-top:44px;color:#55C596;font-weight:700;font-size:24px;letter-spacing:3px;text-transform:uppercase}
h1{margin-top:14px;font-family:'Inter Display',Inter;font-weight:800;font-size:__FS__px;line-height:1.06;letter-spacing:-1px}
h1 em{font-style:normal;color:#7CE395}
.bar{width:96px;height:6px;background:#7CE395;border-radius:4px;margin:26px 0 22px}
p{font-size:30px;line-height:1.38;color:#d6e6e2;font-weight:500;max-width:940px}
p b{color:#7CE395;font-weight:700}
footer{position:absolute;left:60px;right:60px;bottom:52px;display:flex;align-items:center;justify-content:space-between}
.dots{display:flex;gap:12px;align-items:center}
.dots span{width:14px;height:14px;border-radius:10px;background:rgba(255,255,255,.28)}
.dots span.on{width:46px;background:#7CE395}
.src{font-size:20px;color:#8fb3aa;font-weight:500}
.swipe{color:#7CE395;font-weight:700;font-size:26px}
</style></head><body><div class="grid"></div><div class="wrap">
<header><img src="data:image/png;base64,__LOGO__"><div class="chip"><span class="tag">__TAG__</span><span class="num">__I__/4</span></div></header>
<div class="ill">__ILL__</div>
<div class="kicker">__KICKER__</div>
<h1>__TITLE__</h1><div class="bar"></div>
<p>__DESC__</p>
<footer><div class="dots">__DOTS__</div><div class="src">Fuente: __SRC__</div><div class="swipe">__SWIPE__</div></footer>
</div></body></html>"""


def build(slides, outdir):
    out = []
    for i, s in enumerate(slides, 1):
        dots = "".join(f'<span class="{"on" if j==i else ""}"></span>' for j in range(1, len(slides)+1))
        h = (TPL.replace("__LOGO__", logo).replace("__TAG__", s["tag"]).replace("__I__", str(i))
             .replace("__ILL__", ILL[s["ill"]]).replace("__KICKER__", s["kicker"]).replace("__TITLE__", s["title"])
             .replace("__FS__", str(s.get("fs", 64))).replace("__DESC__", s["desc"]).replace("__DOTS__", dots)
             .replace("__SRC__", s["src"]).replace("__SWIPE__", "Deslizá →" if i < len(slides) else "@jas.software"))
        p = pathlib.Path(outdir) / f"slide{i}.html"
        p.write_text(h, encoding="utf-8")
        out.append(str(p))
    return out


if __name__ == "__main__":
    slides = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    print("\n".join(build(slides, sys.argv[2])))
