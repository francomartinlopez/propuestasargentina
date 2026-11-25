# Controles antes de publicar. Termina con "Todo en orden" o con la lista de problemas.
# Uso: python3 herramientas/verificar.py [--sin-navegador]
import json, os, re, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
mal = []
P = json.load(open('datos/propuestas.json'))
if sorted(p['n'] for p in P) != list(range(1, 101)): mal.append('datos/propuestas.json no tiene exactamente las propuestas 1 a 100')
normas = {f[:-5] for f in os.listdir('fuente/normas') if f.endswith('.json')}
CAMPOS = ('n', 'area', 'titulo', 'resumen', 'que_ext', 'que_comp', 'porque_ext', 'porque_comp', 'fuentes', 'dato')
VOSEO = r'\b(tenés|podés|querés|sabés|hacés|movés|pagás|estás|corregís|trabajás|firmás|elegís|vivís|cobrás|ganás|decís|irte|quedarte)\b'
for p in P:
    for k in CAMPOS:
        if k not in p: mal.append(f'propuesta {p.get("n")}: falta el campo {k}')
    s = json.dumps({k: v for k, v in p.items() if k not in ('mapa',)}, ensure_ascii=False)
    for m in set(re.findall(VOSEO, s)): mal.append(f'propuesta {p["n"]}: voseo «{m}» en un texto formal')
    if re.search(r'\bsólo\b', s, re.I): mal.append(f'propuesta {p["n"]}: «sólo» con tilde (va «solo»)')
    if re.search(r'\b[BD]\d{2}\b', s): mal.append(f'propuesta {p["n"]}: código interno de decisión (B## o D##)')
    for i in set(re.findall(r'\bN\d{3}[a-z]?\b', s)):
        if i not in normas: mal.append(f'propuesta {p["n"]}: cita {i}, que no existe en fuente/normas')
C = json.load(open('datos/cien_dias.json'))
for t in C['tramos']:
    for x in t['items']:
        for n in x.get('props', []):
            if not 1 <= n <= 100: mal.append(f'100 días: «{x.get("titulo", "")[:50]}» cita la propuesta {n}')
for f in os.listdir('fuente/normas'):
    d = json.load(open('fuente/normas/' + f))
    if not os.path.exists(f'datos/normas/pdf/{d["id"]}.pdf'): mal.append(f'{d["id"]}: falta su PDF (corré pdf_normas.cjs)')
    if f[:-5] != d['id']: mal.append(f'{f}: el nombre del archivo no coincide con su id {d["id"]}')
for f in ('100-propuestas.pdf', '100-propuestas-extendido.pdf', '100-propuestas-resumido.pdf', 'datos/normas/todas-las-normas.pdf'):
    if not os.path.exists(f): mal.append(f'falta {f}')

if '--sin-navegador' not in sys.argv:
    js = r"""const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const s=spawn('python3',['-m','http.server','8771'],{stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
const b=await chromium.launch();const errs=[];
for(const [w,h] of [[1280,900],[390,844]]){const p=await b.newPage({viewport:{width:w,height:h}});
 p.on('pageerror',e=>errs.push(w+': '+e.message));
 await p.goto('http://localhost:8771/');await p.waitForSelector('#p100',{timeout:30000});
 for(const g of ['1','2','3']){await p.evaluate(g=>document.querySelector('[data-g="'+g+'"]').click(),g);await p.waitForTimeout(400)}
 await p.evaluate(()=>{location.hash='#p44-3'});await p.waitForTimeout(1500);
 const t=await p.evaluate(()=>document.body.innerText);if(/undefined|NaN/.test(t))errs.push(w+': aparece undefined o NaN en el texto');
 await p.close()}
for(const u of ['404.html','gracias.html','privacidad.html','mapa-hidrovia.html','mapa-integracion.html']){const p=await b.newPage();p.on('pageerror',e=>errs.push(u+': '+e.message));await p.goto('http://localhost:8771/'+u);await p.waitForTimeout(400);await p.close()}
await b.close();s.kill();console.log(JSON.stringify(errs))})();"""
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/npm-tools/node_modules')})
    try: mal += [f'navegador: {x}' for x in json.loads(r.stdout.strip().splitlines()[-1])]
    except Exception: mal.append('navegador: no se pudo correr la prueba (' + (r.stderr.strip().splitlines() or ['sin detalle'])[-1] + ')')

if mal:
    print('\n'.join('PROBLEMA: ' + m for m in mal)); sys.exit(1)
print('Todo en orden')
