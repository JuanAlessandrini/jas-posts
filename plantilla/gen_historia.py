"""Historias de Instagram (9:16, 1080x1920) de JAS Software a partir de tendencias.

Uso: python3 -I plantilla/gen_historia.py historias.json outdir
     NODE_PATH=$(npm root -g) node plantilla/shot_story.js $(ls $PWD/outdir/*.html)

historias.json: lista de objetos. Campos comunes:
  layout   "titular" | "tweet" | "meme" | "encuesta" | "dato" | "split"
  trend    texto del chip de tendencia (ej. "#LasVegasGP")
  kicker   (opcional) línea chica sobre el hook
  hook     frase principal (máx ~60 caracteres); <em>..</em> resalta
  punch    remate que conecta con JAS (máx ~110); <b>..</b> resalta
  cta      mini CTA (ej. "Escribinos 👉 353-4764036")
  product  (opcional) producto/servicio JAS que se destaca (ej. "distri")
  fs       (opcional) tamaño del hook en px
  photo / credit (recomendado) foto realista local (Unsplash, 1080x1920) + nombre del fotógrafo
  photo_style (opcional) cómo se integra la foto: "full" (fondo completo con velo),
           "hero" (foto protagonista, texto abajo), "top" (foto arriba que se funde),
           "split" (foto arriba con corte diagonal). Default según layout.
Campos por layout:
  titular: bigword (palabra gigante de fondo)
  tweet:   time (ej. "11:42 · 22 nov. 2026")
  meme:    rows [{label, value, hot}] (comparación), stamp (sticker girado)
  encuesta: options [{text, pct}]
  dato:    number, label
  split:   art ("eq" ecualizador | "rings" | "bars")

Zonas seguras: todo el contenido vive entre y=250 y y=1580 (1920-340).
Las franjas de arriba/abajo solo llevan fondo y decoración.
"""
import base64, json, sys, pathlib, mimetypes, random, html

HERE = pathlib.Path(__file__).parent
LOGO = "data:image/png;base64," + base64.b64encode((HERE / "logo_white.png").read_bytes()).decode()
SAFE_TOP, SAFE_BOTTOM = 250, 340

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:Inter,'Noto Color Emoji',sans-serif;color:#fff;
 background:radial-gradient(1000px 800px at 110% -5%, rgba(124,227,149,.22), transparent 60%),
 radial-gradient(900px 700px at -15% 105%, rgba(52,157,158,.30), transparent 60%),linear-gradient(170deg,#0B171D,#162932 60%,#0E1C23)}
.deco{position:absolute;inset:0;overflow:hidden;z-index:0}
.photo{position:absolute;inset:0;background-size:cover;background-position:center;z-index:0}
.photo:after{content:"";position:absolute;inset:0}
.ph-full .photo:after{background:linear-gradient(180deg,rgba(11,23,29,.55),rgba(11,23,29,.40) 30%,rgba(11,23,29,.62) 60%,rgba(11,23,29,.90))}
.ph-hero .photo:after{background:linear-gradient(180deg,rgba(11,23,29,.55),rgba(11,23,29,.05) 17%,rgba(11,23,29,.5) 30%,rgba(11,23,29,.9) 45%,rgba(11,23,29,.97))}
.ph-full.tweet .photo:after{background:linear-gradient(180deg,rgba(11,23,29,.5),rgba(11,23,29,.15) 35%,rgba(11,23,29,.2) 60%,rgba(11,23,29,.7))}
.ph-top .photo{bottom:auto;height:1080px;-webkit-mask-image:linear-gradient(180deg,#000 60%,transparent)}
.ph-top .photo:after{background:linear-gradient(180deg,rgba(11,23,29,.5),rgba(11,23,29,0) 28%,rgba(11,23,29,.3))}
.ph-split .photo{bottom:auto;height:760px;z-index:1;clip-path:polygon(0 0,100% 0,100% 100%,0 80%)}
.ph-split .photo:after{background:linear-gradient(180deg,rgba(11,23,29,.55),rgba(11,23,29,.0) 35%,rgba(11,23,29,.15))}
.ph-hero main,.ph-top main,.ph-split main{justify-content:flex-end;padding-bottom:40px}
.has-photo h1,.has-photo .kicker,.has-photo .punch{text-shadow:0 3px 22px rgba(0,0,0,.6)}
.has-photo .kicker{color:#8FF0A8}
.has-photo header img{background:rgba(11,23,29,.6);padding:12px 18px;border-radius:16px;height:74px}
.safe{position:absolute;left:72px;right:72px;top:__ST__px;bottom:__SB__px;display:flex;flex-direction:column;z-index:2}
header{display:flex;align-items:center;justify-content:space-between;padding-top:22px}
header img{height:50px}
.chip{border:2px solid rgba(124,227,149,.7);color:#7CE395;background:rgba(11,23,29,.55);font-weight:800;font-size:23px;letter-spacing:2px;
 text-transform:uppercase;padding:12px 22px;border-radius:40px;max-width:600px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chip i{font-style:normal;color:#fff;opacity:.75;margin-right:8px}
main{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
footer{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-bottom:18px}
.cta{background:#7CE395;color:#0B171D;font-weight:800;font-size:36px;padding:22px 34px;border-radius:60px;box-shadow:0 12px 40px rgba(124,227,149,.28);white-space:nowrap}
.handle{font-weight:700;font-size:30px;color:#cfe3dd;white-space:nowrap;text-align:right;text-shadow:0 2px 10px rgba(0,0,0,.5)}
.handle small{display:block;font-weight:500;font-size:17px;color:rgba(255,255,255,.7);margin-top:6px}
.kicker{color:#55C596;font-weight:800;font-size:30px;letter-spacing:3px;text-transform:uppercase;margin-bottom:22px}
h1{font-weight:900;line-height:1.0;letter-spacing:-3px}
h1 em,.punch b{font-style:normal;color:#7CE395}
.punch{font-size:44px;line-height:1.3;font-weight:500;color:#dcebe7}
.punch b{font-weight:800}
.bar{width:120px;height:8px;border-radius:6px;background:#7CE395;margin:40px 0 36px}
.prod{display:inline-flex;align-items:center;gap:14px;margin-top:40px;align-self:flex-start;background:rgba(124,227,149,.12);
 border:2px solid rgba(124,227,149,.45);border-radius:20px;padding:14px 24px;font-size:30px;font-weight:600;color:#cfe3dd}
.prod b{color:#7CE395;font-weight:900;font-size:36px}
body.dato header img{background:#0B171D;padding:14px 20px;border-radius:18px;height:78px}
body.dato .chip{background:#0B171D;border-color:#0B171D}
body.dato .cta{background:#0B171D;color:#7CE395;box-shadow:0 12px 40px rgba(0,0,0,.3)}
body.dato .prod{background:rgba(11,23,29,.55);border-color:rgba(11,23,29,.2)}
"""

def esc(s):
    return s  # el JSON ya trae HTML controlado (<em>, <b>)

def prod_tag(s):
    if not s.get("product"):
        return ""
    return f'<div class="prod">Solución JAS <b>{s["product"]}</b></div>'

# ---------------- layouts ----------------

def L_titular(s, rnd):
    word = s.get("bigword", "")
    conf = "".join(
        f'<span style="position:absolute;left:{rnd.randint(0,1060)}px;top:{rnd.choice([rnd.randint(0,220), rnd.randint(1610,1900)])}px;'
        f'width:{w}px;height:{w*rnd.choice([1,2.6])}px;background:{rnd.choice(["#7CE395","#55C596","#349D9E","#8FE3E4"])};opacity:{rnd.uniform(.25,.7):.2f};'
        f'border-radius:{rnd.choice([3,20])}px;transform:rotate({rnd.randint(0,180)}deg)"></span>'
        for w in [rnd.randint(10, 22) for _ in range(46)])
    deco = f"""<div class="deco">{conf}
    <div style="position:absolute;left:-40px;top:1600px;font-weight:900;font-size:300px;letter-spacing:-12px;color:transparent;
      -webkit-text-stroke:3px rgba(124,227,149,.16);white-space:nowrap;transform:rotate(-8deg)">{word}</div></div>"""
    main = f"""<div class="kicker">{s.get('kicker','')}</div>
    <h1 style="font-size:{s.get('fs',124)}px">{s['hook']}</h1><div class="bar"></div>
    <div class="punch">{s['punch']}</div>{prod_tag(s)}"""
    return deco, main


def L_tweet(s, rnd):
    stripes = "".join(f'<rect x="{x}" y="{y}" width="60" height="60" fill="#fff" opacity=".07"/>'
                      for i, x in enumerate(range(0, 1080, 60)) for j, y in enumerate((0, 60)) if (i + j) % 2 == 0)
    lines = "".join(f'<div style="position:absolute;right:-60px;top:{y}px;width:{w}px;height:6px;border-radius:6px;background:#7CE395;opacity:{o}"></div>'
                    for y, w, o in [(1640, 520, .5), (1680, 360, .35), (1720, 640, .25), (1760, 300, .4), (40, 260, .25), (70, 420, .15)])
    deco = f'<div class="deco"><svg width="1080" height="120" style="position:absolute;left:0;top:120px">{stripes}</svg>{lines}</div>'
    check = '<svg width="38" height="38" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#55C596"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#0B171D" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>'
    ic = lambda d: f'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#5f7a74" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
    icons = [ic('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>'),
             ic('<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>'),
             ic('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>'),
             ic('<path d="M4 12v8h16v-8"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v13"/>')]
    main = f"""<div class="kicker">{s.get('kicker','')}</div>
    <div style="background:#F4FAF7;color:#0B171D;border-radius:40px;padding:52px 52px 40px;box-shadow:0 30px 80px rgba(0,0,0,.45);transform:rotate(-1.5deg)">
      <div style="display:flex;align-items:center;gap:22px">
        <div style="width:104px;height:104px;border-radius:52px;background:#162932;display:flex;align-items:center;justify-content:center;flex:none">
          <div style="width:77px;height:58px;overflow:hidden"><img src="{LOGO}" style="height:58px;display:block"></div></div>
        <div><div style="display:flex;align-items:center;gap:10px;font-weight:800;font-size:38px">JAS Software {check}</div>
        <div style="color:#5f7a74;font-size:30px;font-weight:500">@jas.software</div></div></div>
      <div style="font-weight:800;font-size:{s.get('fs',62)}px;line-height:1.12;letter-spacing:-1.5px;margin-top:36px">{s['hook']}</div>
      <div style="font-size:40px;line-height:1.32;margin-top:24px;color:#22363e">{s['punch'].replace('<b>','<b style="color:#2a8f6a">')}</div>
      <div style="color:#5f7a74;font-size:28px;margin-top:30px">{s.get('time','')}</div>
      <div style="border-top:2px solid #dbe8e3;margin-top:24px;padding-top:24px;display:flex;justify-content:space-between">{''.join(icons)}</div>
    </div>{prod_tag(s)}"""
    return deco, main


def L_meme(s, rnd):
    deco = """<div class="deco">
      <div style="position:absolute;left:-200px;top:-180px;width:640px;height:640px;border-radius:50%;border:70px solid rgba(124,227,149,.08)"></div>
      <div style="position:absolute;right:-220px;bottom:-200px;width:700px;height:700px;border-radius:50%;border:80px solid rgba(52,157,158,.14)"></div></div>"""
    rows = ""
    for r in s["rows"]:
        hot = r.get("hot")
        col = "#FF8A65" if hot else "#7CE395"
        rows += f"""<div style="display:flex;align-items:center;justify-content:space-between;gap:24px;padding:34px 40px;border-radius:30px;
          background:{'rgba(255,138,101,.10)' if hot else 'rgba(124,227,149,.10)'};border:3px solid {col};margin-bottom:22px">
          <div style="font-size:38px;font-weight:700;line-height:1.2;color:#eaf3f0">{r['label']}</div>
          <div style="font-size:92px;font-weight:900;color:{col};white-space:nowrap;letter-spacing:-3px">{r['value']}</div></div>"""
    main = f"""<div class="kicker">{s.get('kicker','')}</div>
    <h1 style="font-size:{s.get('fs',84)}px;margin-bottom:44px">{s['hook']}</h1>
    <div style="position:relative">{rows}
      <div style="position:absolute;right:-18px;bottom:-56px;background:#7CE395;color:#0B171D;font-weight:900;font-size:36px;padding:18px 30px;
        border-radius:16px;transform:rotate(-6deg);box-shadow:0 14px 36px rgba(0,0,0,.4)">{s.get('stamp','')}</div></div>
    <div class="punch" style="margin-top:84px">{s['punch']}</div>"""
    return deco, main


def L_encuesta(s, rnd):
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#7CE395" opacity=".18"/>' for x in range(20, 1080, 44) for y in range(20, 1920, 44))
    deco = f'<div class="deco"><svg width="1080" height="1920" style="position:absolute;inset:0">{dots}</svg></div>'
    opts = ""
    for o in s["options"]:
        opts += f"""<div style="position:relative;border-radius:24px;background:#EEF4F2;overflow:hidden;margin-top:20px;height:104px">
          <div style="position:absolute;left:0;top:0;bottom:0;width:{o['pct']}%;background:linear-gradient(90deg,#7CE395,#55C596)"></div>
          <div style="position:relative;display:flex;justify-content:space-between;align-items:center;height:100%;padding:0 32px;font-size:36px;font-weight:800;color:#0B171D">
          <span>{o['text']}</span><span>{o['pct']}%</span></div></div>"""
    main = f"""<div class="kicker">{s.get('kicker','')}</div>
    <h1 style="font-size:{s.get('fs',88)}px">{s['hook']}</h1>
    <div style="background:#fff;border-radius:36px;padding:36px 36px 40px;margin:52px 0 48px;box-shadow:0 30px 80px rgba(0,0,0,.45);transform:rotate(1.5deg)">
      <div style="text-align:center;font-weight:900;font-size:30px;letter-spacing:2px;color:#349D9E">ENCUESTA</div>{opts}</div>
    <div class="punch">{s['punch']}</div>"""
    return deco, main


def L_dato(s, rnd):
    deco = """<div class="deco" style="background:linear-gradient(160deg,#7CE395 0%,#55C596 30%,#349D9E 58%,#162932 100%)">
      <div style="position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.06) 0 2px,transparent 2px 46px)"></div>
      <div style="position:absolute;right:-260px;top:120px;width:820px;height:820px;border-radius:50%;background:rgba(255,255,255,.10)"></div></div>"""
    main = f"""<div style="display:flex;align-items:flex-end;gap:28px;margin-top:-20px">
      <div style="font-weight:900;font-size:{s.get('nfs',400)}px;line-height:.8;letter-spacing:-20px;color:#0B171D">{s['number']}</div>
      <div style="font-weight:800;font-size:46px;line-height:1.1;color:#0B171D;padding-bottom:20px">{s['label']}</div></div>
    <h1 style="font-size:{s.get('fs',86)}px;margin-top:70px;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.25)">{s['hook']}</h1>
    <div class="bar" style="background:#fff"></div>
    <div class="punch" style="color:#fff">{s['punch']}</div>{prod_tag(s)}"""
    return deco, main


def L_split(s, rnd):
    art = s.get("art", "eq")
    if art == "eq":
        bars = "".join(
            f'<rect x="{40+i*52}" y="{300-h}" width="36" height="{h}" rx="18" fill="{"#7CE395" if i%3 else "#8FE3E4"}" opacity="{.5+.5*(i%2)}"/>'
            for i, h in enumerate([rnd.randint(40, 280) for _ in range(18)]))
        svg = f'<svg viewBox="0 0 980 320" width="936">{bars}</svg>'
    elif art == "rings":
        svg = '<svg viewBox="0 0 980 320" width="936">' + "".join(
            f'<circle cx="490" cy="160" r="{r}" fill="none" stroke="#7CE395" stroke-width="10" opacity="{1-r/200:.2f}"/>' for r in range(30, 190, 32)) + '</svg>'
    else:
        svg = '<svg viewBox="0 0 980 320" width="936">' + "".join(
            f'<rect x="{60+i*120}" y="{300-v}" width="80" height="{v}" rx="12" fill="#55C596"/>' for i, v in enumerate([80, 120, 110, 170, 220, 260, 300])) + '</svg>'
    deco = """<div class="deco"><div style="position:absolute;left:0;right:0;top:0;height:980px;background:linear-gradient(180deg,#1d3a40,#162932);
      clip-path:polygon(0 0,100% 0,100% 82%,0 100%)"></div></div>"""
    main = f"""<div style="display:flex;justify-content:center;margin-bottom:90px">{svg}</div>
    <div class="kicker">{s.get('kicker','')}</div>
    <h1 style="font-size:{s.get('fs',100)}px">{s['hook']}</h1><div class="bar"></div>
    <div class="punch">{s['punch']}</div>{prod_tag(s)}"""
    return deco, main


LAYOUTS = dict(titular=L_titular, tweet=L_tweet, meme=L_meme, encuesta=L_encuesta, dato=L_dato, split=L_split)


def data_uri(path):
    p = pathlib.Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


PHOTO_STYLE = dict(titular="hero", tweet="full", meme="top", encuesta="full", dato="split", split="top")


def page(s, i):
    rnd = random.Random(1000 + i)
    deco, main = LAYOUTS[s["layout"]](s, rnd)
    photo = credit = ""
    cls = s["layout"]
    if s.get("photo"):
        st = s.get("photo_style") or PHOTO_STYLE[s["layout"]]
        cls += f" has-photo ph-{st}"
        if st in ("full", "hero") and s["layout"] != "dato":
            deco = ""  # la foto es el fondo: sin decoración encima
        photo = f'<div class="photo" style="background-image:url(\'{data_uri(s["photo"])}\');background-position:{s.get("photo_pos","center")}"></div>'
        credit = f'<small>Foto: {html.escape(s.get("credit",""))} / Unsplash</small>'
    css = CSS.replace("__ST__", str(SAFE_TOP)).replace("__SB__", str(SAFE_BOTTOM))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}">
{photo}{deco}
<div class="safe">
 <header><img src="{LOGO}"><div class="chip"><i>Tendencia ·</i>{s.get('trend','')}</div></header>
 <main>{main}</main>
 <footer><div class="cta">{s.get('cta','Escribinos 👉 353-4764036')}</div><div class="handle">@jas.software{credit}</div></footer>
</div>
</body></html>"""


def build(items, outdir):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out = []
    for i, s in enumerate(items, 1):
        p = outdir / f"historia{i}.html"
        p.write_text(page(s, i), encoding="utf-8")
        out.append(str(p.resolve()))
    return out


if __name__ == "__main__":
    items = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    print("\n".join(build(items, sys.argv[2])))
