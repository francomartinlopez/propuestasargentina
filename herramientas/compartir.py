# Genera las imágenes para compartir (og.jpg, icono-180.png) y una página por propuesta en p/N/
# con su propia tarjeta para WhatsApp (p/N/og.jpg). Lee datos/propuestas.json.
# Uso: python3 herramientas/compartir.py            todas
#      python3 herramientas/compartir.py 44 87      solo esas (más og.jpg e icono)
import json, html, os, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
SITE = 'https://propuestasargentina.netlify.app/'
AREAS = {"I": "Moneda, cuentas y deuda", "II": "Impuestos y federalismo", "III": "Producción, comercio e inversión",
         "IV": "Energía, infraestructura y ambiente", "V": "Trabajo", "VI": "Estado, transparencia y justicia", "VII": "Seguridad",
         "VIII": "Ingreso, salud, educación y vivienda", "IX": "Mundo, defensa y soberanía", "X": "Memoria, democracia y convivencia"}
NIVEL_LINK = {27: 3}   # propuestas que se abren siempre en el nivel completo
e = html.escape
D = json.load(open('datos/propuestas.json'))
pedidas = {int(x) for x in sys.argv[1:]}
FONT = ''.join(f"@font-face{{font-family:J;font-weight:{w};src:url(file://{R}/fuentes/plus-jakarta-sans-latin-{w}-normal.woff2)}}" for w in (500, 600, 700, 800))
BASE = FONT + """html,body{margin:0}body{width:1200px;height:630px;overflow:hidden;font-family:J,sans-serif}
.c{position:relative;width:1200px;height:630px;box-sizing:border-box;padding:70px 80px;color:#fff;background:linear-gradient(115deg,#f9b50f 0%,#eb671c 34%,#e84f2b 68%,#e84b49 100%);overflow:hidden;display:flex;flex-direction:column}
.c::after{content:"";position:absolute;width:760px;height:760px;border-radius:50%;background:rgba(255,255,255,.10);right:-200px;top:-80px}
.c>*{position:relative;z-index:1}
.k{font-weight:600;font-size:24px;letter-spacing:.14em;text-transform:uppercase}
.sol{position:absolute;z-index:1;right:80px;bottom:62px;width:120px;height:60px;border-radius:120px 120px 0 0;background:#fff;opacity:.95}
.sol::after{content:"";position:absolute;left:-10px;right:-10px;bottom:-14px;height:8px;border-radius:4px;background:#111}
em{font-style:normal;color:#111}
"""
def pagina_og():
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}
h1{{font-weight:800;font-size:96px;line-height:1.02;letter-spacing:-.03em;margin:22px 0 0}}
.lema{{margin-top:auto;font-weight:800;font-size:40px;line-height:1.2}}
</style></head><body><div class="c"><div class="k">Programa para la Argentina</div><h1>100 propuestas<br>para <em>la Argentina</em></h1>
<div class="lema">Una patria. Un pueblo.<br><em>Bajo un mismo cielo.</em></div><div class="sol"></div></div></body></html>"""
def pagina_prop(p):
    t = p['titulo']; fs = 64 if len(t) < 45 else 56 if len(t) < 70 else 48 if len(t) < 95 else 42
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}
.n{{font-weight:800;font-size:150px;line-height:.9;letter-spacing:-.04em;margin-top:26px;color:#111}}
h1{{font-weight:800;font-size:{fs}px;line-height:1.08;letter-spacing:-.02em;margin:18px 0 0;max-width:900px}}
.pie{{margin-top:auto;font-weight:700;font-size:26px;max-width:860px}}.pie span{{font-weight:600;opacity:.9}}
</style></head><body><div class="c"><div class="k">{e(p['area'])} · {e(AREAS[p['area']])}</div>
<div class="n">{p['n']}</div><h1>{e(t)}</h1>
<div class="pie">100 propuestas para la Argentina<br><span>Qué, por qué y cómo · propuestasargentina.netlify.app</span></div><div class="sol"></div></div></body></html>"""
ICON = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0}}body{{width:180px;height:180px;background:#fff;display:grid;place-items:center}}</style></head><body>{open('favicon.svg').read().replace("viewBox='0 0 40 40'", "viewBox='-4 -6 48 48' width='180' height='180'")}</body></html>"""

os.makedirs('/tmp/og', exist_ok=True)
trabajos = [('/tmp/og/og.html', f'{R}/og.jpg', 1200, 630), ('/tmp/og/icono.html', f'{R}/icono-180.png', 180, 180)]
open('/tmp/og/og.html', 'w').write(pagina_og()); open('/tmp/og/icono.html', 'w').write(ICON)
for p in D:
    n = p['n']
    if pedidas and n not in pedidas: continue
    d = f'{R}/p/{n}/'; os.makedirs(d, exist_ok=True)
    open(f'/tmp/og/p{n}.html', 'w').write(pagina_prop(p)); trabajos.append((f'/tmp/og/p{n}.html', d + 'og.jpg', 1200, 630))
    nv = NIVEL_LINK.get(n, 2); desc = p.get('resumen') or ''; tit = f'Propuesta {n}: {p["titulo"]}'
    open(d + 'index.html', 'w').write(f"""<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(tit)} · 100 propuestas para la Argentina</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}p/{n}/"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:locale" content="es_AR"><meta property="og:type" content="article"><meta property="og:site_name" content="100 propuestas para la Argentina">
<meta property="og:title" content="{e(tit)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}p/{n}/"><meta property="og:image" content="{SITE}p/{n}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>var q=/[?&]n=3/.test(location.search)?3:{nv};location.replace('/#p{n}-'+q);</script>
<noscript><meta http-equiv="refresh" content="0;url=/#p{n}-{nv}"></noscript>
<style>body{{font:16px/1.6 system-ui,sans-serif;max-width:640px;margin:60px auto;padding:0 20px;color:#111}}a{{color:#b8470f;font-weight:700}}</style>
</head><body><p><a href="/#p{n}-{nv}">{e(tit)}</a></p><p>{e(desc)}</p></body></html>""")
json.dump(trabajos, open('/tmp/og/trabajos.json', 'w'))
subprocess.run(['node', '-e', """const {chromium}=require('playwright');const T=require('/tmp/og/trabajos.json');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [src,out,w,h] of T){await p.setViewportSize({width:w,height:h});await p.goto('file://'+src);await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:out,type:out.endsWith('.png')?'png':'jpeg',quality:out.endsWith('.png')?undefined:86})}
await b.close();console.log('imagenes',T.length)})();"""], check=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/npm-tools/node_modules')})
