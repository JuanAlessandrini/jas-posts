"""Carrusel de noticias JAS con foto real (Unsplash).

Uso: python3 -I plantilla/gen_foto.py slides.json outdir
slides.json: lista de objetos con
  tag     "Negocios" | "Tecnología"
  photo   ruta local de la foto (jpg) descargada de Unsplash
  credit  nombre del fotógrafo (se muestra "Foto: <credit> / Unsplash")
  kicker  subtema corto (ej. "Argentina", "Inteligencia Artificial")
  title   título; <em>..</em> resalta en verde
  desc    descripción breve; <b>..</b> resalta
  src     fuente de la noticia
  fs      (opcional) tamaño del título en px, default 62
Luego: NODE_PATH=$(npm root -g) node plantilla/shot.js <html...>  (genera PNG 1080x1350)
"""
import base64, json, sys, pathlib, mimetypes

HERE = pathlib.Path(__file__).parent
LOGO = base64.b64encode((HERE / "logo_white.png").read_bytes()).decode()

BADGE = {
    "Negocios": ("#7CE395", "rgba(124,227,149,.18)", "#55C596"),
    "Tecnología": ("#8FE3E4", "rgba(52,157,158,.25)", "#349D9E"),
}

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:#fff;
 background:radial-gradient(900px 600px at -10% 110%, rgba(85,197,150,.20), transparent 60%),linear-gradient(170deg,#0B171D,#162932);}
.hero{position:absolute;left:0;top:0;width:1080px;height:700px;background:url('__PHOTO__') center/cover no-repeat;
 -webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 100%);mask-image:linear-gradient(180deg,#000 62%,transparent 100%)}
.hero:after{content:"";position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(11,23,29,.75) 0%,rgba(11,23,29,.05) 26%,rgba(11,23,29,0) 50%,rgba(14,28,35,.6) 100%)}
.grid{position:absolute;left:0;right:0;top:700px;bottom:0;background-image:radial-gradient(rgba(124,227,149,.10) 1.5px,transparent 1.5px);background-size:36px 36px}
header{position:absolute;left:60px;right:60px;top:52px;display:flex;align-items:center;justify-content:space-between;z-index:2}
header img{height:60px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))}
.chip{display:flex;gap:12px;align-items:center}
.tag{background:__BBG__;border:2px solid __BBR__;color:__BFG__;font-weight:800;font-size:24px;letter-spacing:2px;padding:12px 24px;border-radius:40px;text-transform:uppercase;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);box-shadow:0 6px 20px rgba(0,0,0,.35)}
.num{background:rgba(11,23,29,.7);color:#fff;font-weight:700;font-size:22px;padding:12px 16px;border-radius:14px}
.credit{position:absolute;right:60px;top:640px;font-size:16px;color:rgba(255,255,255,.7);z-index:2}
.body{position:absolute;left:60px;right:60px;top:660px;z-index:2}
.kicker{color:#55C596;font-weight:700;font-size:24px;letter-spacing:3px;text-transform:uppercase}
h1{margin-top:14px;font-weight:800;font-size:__FS__px;line-height:1.07;letter-spacing:-1px}
h1 em{font-style:normal;color:#7CE395}
.bar{width:96px;height:6px;background:#7CE395;border-radius:4px;margin:24px 0 20px}
p{font-size:29px;line-height:1.38;color:#d6e6e2;font-weight:500}
p b{color:#7CE395;font-weight:700}
footer{position:absolute;left:60px;right:60px;bottom:48px;display:flex;align-items:center;justify-content:space-between;z-index:2}
.dots{display:flex;gap:12px;align-items:center}
.dots span{width:14px;height:14px;border-radius:10px;background:rgba(255,255,255,.28)}
.dots span.on{width:46px;background:#7CE395}
.src{font-size:20px;color:#8fb3aa;font-weight:500}
.swipe{color:#7CE395;font-weight:700;font-size:26px}
</style></head><body>
<div class="hero"></div><div class="grid"></div>
<header><img src="data:image/png;base64,__LOGO__"><div class="chip"><span class="tag">__TAG__</span><span class="num">__I__/__N__</span></div></header>
<div class="credit">Foto: __CREDIT__ / Unsplash</div>
<div class="body"><div class="kicker">__KICKER__</div><h1>__TITLE__</h1><div class="bar"></div><p>__DESC__</p></div>
<footer><div class="dots">__DOTS__</div><div class="src">Fuente: __SRC__</div><div class="swipe">__SWIPE__</div></footer>
</body></html>"""


def data_uri(path):
    p = pathlib.Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def build(slides, outdir):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out, n = [], len(slides)
    for i, s in enumerate(slides, 1):
        fg, bg, br = BADGE.get(s["tag"], BADGE["Negocios"])
        dots = "".join(f'<span class="{"on" if j == i else ""}"></span>' for j in range(1, n + 1))
        h = TPL
        for k, v in {
            "__PHOTO__": data_uri(s["photo"]), "__LOGO__": LOGO, "__TAG__": s["tag"],
            "__BFG__": fg, "__BBG__": bg, "__BBR__": br, "__I__": str(i), "__N__": str(n),
            "__CREDIT__": s.get("credit", ""), "__KICKER__": s["kicker"], "__TITLE__": s["title"],
            "__FS__": str(s.get("fs", 62)), "__DESC__": s["desc"], "__DOTS__": dots, "__SRC__": s["src"],
            "__SWIPE__": "Deslizá →" if i < n else "@jas.software",
        }.items():
            h = h.replace(k, v)
        p = outdir / f"slide{i}.html"
        p.write_text(h, encoding="utf-8")
        out.append(str(p.resolve()))
    return out


if __name__ == "__main__":
    slides = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    print("\n".join(build(slides, sys.argv[2])))
