# Arma los mapas interactivos a partir de fuente/mapas/:
#   hidrovía (propuesta 44):    mapa-hidrovia.html, mapa-hidrovia-embed.js, mapa-hidrovia.png
#   integración (propuesta 27): mapa-integracion.html, mapa-embed.js, mapa-integracion.png
#   energía (propuesta 35):     mapa-energia.html, mapa-energia-embed.js, mapa-energia.png
#     (usa las provincias del mapa de integración y su proyección; código en fuente/mapas/energia/codigo.js)
# Lo que se edita: fuente/mapas/<mapa>/datos.json (tramos, puertos, lugares, capas, obras).
# Textos fijos, estilos y código: interior.html (lo que va dentro del sitio), pagina.html (página suelta) y embed.js.
# Las imágenes .png son las que usa el PDF del programa.
# Uso: python3 herramientas/mapas.py [hidrovia|integracion|energia] [--sin-imagenes]
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

def energia():
    import re
    d = json.load(open('fuente/mapas/energia/datos.json')); P = d['proyeccion']
    xy = lambda q: proyectar(P, *q)
    pt = lambda q: '%s,%s' % tuple(f1(v) for v in xy(q))
    base = ''.join(re.findall(r'<path class="prov"[^>]*>(?:<title>[^<]*</title>)?</path>', leer('integracion', 'interior.html')))
    if base.count('class="prov"') < 24: raise SystemExit('no encontré las provincias en el mapa de integración')
    for n, lon, lat in d['paises']:
        x, y = xy((lon, lat)); base += f'<text class="pais" x="{f1(x)}" y="{f1(y)}">{n}</text>'
    for n, lon, lat in d['ciudades']:
        x, y = xy((lon, lat)); base += f'<g class="ciu"><circle cx="{f1(x)}" cy="{f1(y)}" r="1.4"/><text x="{f1(x + 3)}" y="{f1(y + 2.2)}">{n}</text></g>'
    orden = {'zona': -1, 'funciona': 0, 'evaluar': 1, 'frenada': 2, 'planificada': 3, 'en_marcha': 4}   # lo más importante arriba
    capas = []
    for o in sorted(d['obras'], key=lambda o: orden[o['estado']]):
        e, g = o['estado'], o['grupo']; c = []
        for li in o.get('lineas', []):
            dd = 'M' + 'L'.join(pt(q) for q in li)
            c.append(f'<path class="hit" d="{dd}"/>')
            if g == 'gas': c.append(f'<path class="ln e-{e} gas" d="{dd}"/><path class="ln gasi" d="{dd}"/>')
            else: c.append(f'<path class="ln e-{e}" d="{dd}"/>')
        if 'zona' in o:
            z = o['zona']; x, y = xy(z['centro'])
            c.append(f'<ellipse class="zn z-{z["tipo"]}" cx="{f1(x)}" cy="{f1(y)}" rx="{f1(z["rx"] * P["x"][0])}" ry="{f1(z["ry"] * -P["y"][0])}"/>')
        for q in o.get('marcas', []):
            x, y = xy(q)
            if o['id'] == 'nucleares': c.append(f'<circle class="mk f-{e}" cx="{f1(x)}" cy="{f1(y)}" r="4.2"/><circle class="mk nuc" cx="{f1(x)}" cy="{f1(y)}" r="1.6"/>')
            elif o['id'] == 'baterias': c.append(f'<rect class="mk f-{e}" x="{f1(x - 4)}" y="{f1(y - 2.6)}" width="8" height="5.2" rx="1"/>')
            elif g == 'represa': c.append(f'<rect class="mk f-{e}" x="{f1(x - 3.6)}" y="{f1(y - 3.6)}" width="7.2" height="7.2" transform="rotate(45 {f1(x)} {f1(y)})"/>')
            else: c.append(f'<circle class="mk f-{e}" cx="{f1(x)}" cy="{f1(y)}" r="3.8"/>')
        capas.append(f'<g class="ob" data-t="{o["id"]}" data-g="{g}"><title>{o["nombre"]}</title>{"".join(c)}</g>')
    interior = leer('energia', 'interior.html').replace('{{VB}}', ' '.join(str(v) for v in d['viewbox'])).replace('{{BASE}}', base).replace('{{CAPAS}}', ''.join(capas))
    Dj = J([{k: v for k, v in o.items() if k not in ('lineas', 'marcas', 'prov', 'zona')} for o in d['obras']], separators=(',', ':'))
    codigo = leer('energia', 'codigo.js').replace('{{D}}', Dj)
    open('mapa-energia-embed.js', 'w').write(leer('energia', 'embed.js').replace('{{INTERIOR}}', J(interior)).replace('{{CODIGO}}', codigo))
    open('mapa-energia.html', 'w').write(leer('energia', 'pagina.html').replace('{{INTERIOR}}', interior).replace('{{CODIGO}}', codigo))

def imagenes(cuales):
    js = """const {chromium}=require('playwright');const {spawn}=require('child_process');const C=JSON.parse(process.argv[1]);
(async()=>{const s=spawn('python3',['-m','http.server','8772'],{stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1400},deviceScaleFactor:2,colorScheme:'light'});
if(C.includes('integracion')){await p.goto('http://localhost:8772/mapa-integracion.html');await p.waitForTimeout(800);await (await p.$('.mapa')).screenshot({path:'mapa-integracion.png'})}
if(C.includes('hidrovia')){await p.goto('http://localhost:8772/mapa-hidrovia.html');await p.waitForTimeout(800);await p.evaluate(()=>document.querySelectorAll('.tr.sel').forEach(e=>e.classList.remove('sel')));await (await p.$('.mp svg')).screenshot({path:'mapa-hidrovia.png'})}
if(C.includes('energia')){await p.goto('http://localhost:8772/mapa-energia.html');await p.waitForTimeout(800);await p.evaluate(()=>document.querySelectorAll('.ob.sel').forEach(e=>e.classList.remove('sel')));await (await p.$('.mp')).screenshot({path:'mapa-energia.png'})}
await b.close();s.kill()})();"""
    subprocess.run(['node', '-e', js, J(cuales)], check=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/npm-tools/node_modules')})
    try:
        from PIL import Image   # más livianas: sin canal de transparencia
        for m in cuales:
            f = {'hidrovia': 'mapa-hidrovia.png', 'integracion': 'mapa-integracion.png', 'energia': 'mapa-energia.png'}[m]
            Image.open(f).convert('RGB').save(f, optimize=True)
    except ImportError: pass

if __name__ == '__main__':
    pedidos = [a for a in sys.argv[1:] if not a.startswith('--')] or ['hidrovia', 'integracion', 'energia']
    for m in pedidos: {'hidrovia': hidrovia, 'integracion': integracion, 'energia': energia}[m]()
    if '--sin-imagenes' not in sys.argv: imagenes(pedidos)
    print('mapas', ' '.join(pedidos))
