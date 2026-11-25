# Arma los dos mapas interactivos a partir de fuente/mapas/:
#   hidrovía (propuesta 44):    mapa-hidrovia.html, mapa-hidrovia-embed.js, mapa-hidrovia.png
#   integración (propuesta 27): mapa-integracion.html, mapa-embed.js, mapa-integracion.png
# Lo que se edita: fuente/mapas/<mapa>/datos.json (tramos, puertos, lugares, capas, obras).
# Textos fijos, estilos y código: interior.html (lo que va dentro del sitio), pagina.html (página suelta) y embed.js.
# Las imágenes .png son las que usa el PDF del programa.
# Uso: python3 herramientas/mapas.py [hidrovia|integracion] [--sin-imagenes]
import json, os, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
J = lambda o, **k: json.dumps(o, ensure_ascii=False, **k)
f1 = lambda v: f'{v:.1f}'

def proyectar(p, lon, lat):
    return p['x'][0] * lon + p['x'][1], p['y'][0] * lat + p['y'][1]

def leer(m, a): return open(f'fuente/mapas/{m}/{a}').read()

def hidrovia():
    d = json.load(open('fuente/mapas/hidrovia/datos.json')); P = d['proyeccion']; capas = []
    for t in d['tramos']:
        g = t.get('d') or 'M' + 'L'.join(f'{f1(x)},{f1(y)}' for x, y in (proyectar(P, *q) for q in t['puntos']))
        capas.append(f'<path class="tr-hit" data-t="{t["id"]}" d="{g}"/><path class="tr{" nueva" if t.get("nueva") else ""}" data-t="{t["id"]}" style="stroke:{t["c"]}" d="{g}"/>')
    for p in d['puertos']:
        x, y = (p['x'], p['y']) if 'x' in p else proyectar(P, *p['lonlat'])
        r = p.get('r', 4.2 if p['tipo'] == 'u' else 3.6)
        tx = p.get('texto') or {'x': x + 8, 'y': y + 4, 'ancla': 'start'}
        capas.append(f'<g class="pu {p["tipo"]}{" grk" if p.get("gran_rosario") else ""}"><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}"/>'
                     f'<text x="{f1(tx["x"])}" y="{f1(tx["y"])}" text-anchor="{tx["ancla"]}">{p["nombre"]}</text></g>')
    g = d['grupo']
    capas.append(f'<text class="grp" x="{f1(g["x"])}" y="{f1(g["y"])}" text-anchor="{g["ancla"]}">{g["texto"]}</text>')
    capas = ''.join(capas)
    D = J([{k: v for k, v in t.items() if k not in ('d', 'puntos')} for t in d['tramos']])
    interior = leer('hidrovia', 'interior.html').replace('{{CAPAS}}', capas)
    open('mapa-hidrovia-embed.js', 'w').write(leer('hidrovia', 'embed.js').replace('{{INTERIOR}}', J(interior)).replace('{{D}}', D))
    open('mapa-hidrovia.html', 'w').write(leer('hidrovia', 'pagina.html').replace('{{CAPAS}}', capas).replace('{{D}}', D))

def integracion():
    d = json.load(open('fuente/mapas/integracion/datos.json')); D = d['D']
    for nom, ll in d.get('xy_lonlat', {}).items():
        x, y = proyectar(d['proyeccion'], *ll); D['xy'][nom] = [round(x, 1), round(y, 1)]
    faltan = sorted({p[0] for c in D['capas'] for p in c['pts']} - set(D['xy']))
    if faltan: raise SystemExit('lugares sin posición en el mapa de integración: ' + ', '.join(faltan))
    Dj = J(D, separators=(',', ':'))
    open('mapa-embed.js', 'w').write(leer('integracion', 'embed.js').replace('{{INTERIOR}}', J(leer('integracion', 'interior.html'))).replace('{{D}}', Dj))
    open('mapa-integracion.html', 'w').write(leer('integracion', 'pagina.html').replace('{{D}}', Dj))

def imagenes(cuales):
    js = """const {chromium}=require('playwright');const {spawn}=require('child_process');const C=JSON.parse(process.argv[1]);
(async()=>{const s=spawn('python3',['-m','http.server','8772'],{stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1400},deviceScaleFactor:2,colorScheme:'light'});
if(C.includes('integracion')){await p.goto('http://localhost:8772/mapa-integracion.html');await p.waitForTimeout(800);await (await p.$('.mapa')).screenshot({path:'mapa-integracion.png'})}
if(C.includes('hidrovia')){await p.goto('http://localhost:8772/mapa-hidrovia.html');await p.waitForTimeout(800);await p.evaluate(()=>document.querySelectorAll('.tr.sel').forEach(e=>e.classList.remove('sel')));await (await p.$('.mp svg')).screenshot({path:'mapa-hidrovia.png'})}
await b.close();s.kill()})();"""
    subprocess.run(['node', '-e', js, J(cuales)], check=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/npm-tools/node_modules')})
    try:
        from PIL import Image   # más livianas: sin canal de transparencia
        for m in cuales:
            f = 'mapa-hidrovia.png' if m == 'hidrovia' else 'mapa-integracion.png'
            Image.open(f).convert('RGB').save(f, optimize=True)
    except ImportError: pass

if __name__ == '__main__':
    pedidos = [a for a in sys.argv[1:] if not a.startswith('--')] or ['hidrovia', 'integracion']
    for m in pedidos: {'hidrovia': hidrovia, 'integracion': integracion}[m]()
    if '--sin-imagenes' not in sys.argv: imagenes(pedidos)
    print('mapas', ' '.join(pedidos))
