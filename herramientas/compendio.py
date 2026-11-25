# Arma datos/normas/todas-las-normas.pdf: tapa, índice con enlaces, todas las normas
# (cada una una sola vez, en la primera propuesta que la usa) y contratapa.
# Usa los PDF de datos/normas/pdf (hacelos antes con pdf_normas.cjs).
# Uso: python3 herramientas/compendio.py   (desde la raíz del repositorio)
import json, os, subprocess, html, datetime
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, ArrayObject, DictionaryObject

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
e = html.escape
TIPO = {'ley_nacional': 'Ley', 'decreto': 'Decreto', 'resolucion': 'Resolución', 'acuerdo_federal': 'Acuerdo federal',
        'ley_provincial': 'Modelo de ley provincial', 'tratado': 'Tratado', 'ley_aprobatoria': 'Ley aprobatoria',
        'ordenanza_modelo': 'Ordenanza modelo', 'invitacion': 'Invitación'}
props = {p['n']: p for p in json.load(open('datos/propuestas.json'))}
orden = {int(k): v for k, v in json.load(open('fuente/normas_por_propuesta.json'))['normas_por_propuesta'].items()}
N = {f[:-5]: json.load(open('fuente/normas/' + f)) for f in os.listdir('fuente/normas') if f.endswith('.json')}
hoy = datetime.date.today()
MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'][hoy.month - 1] + f' de {hoy.year}'
F = ''.join(f"@font-face{{font-family:PJS;font-weight:{w};src:url(file://{R}/fuentes/plus-jakarta-sans-latin-{w}-normal.woff2)}}" for w in (400, 500, 700, 800))

primera, secuencia = {}, []
for n in range(1, 101):
    for i in orden[n]:
        if i not in primera: primera[i] = n; secuencia.append(i)
paginas = {i: len(PdfReader(f'datos/normas/pdf/{i}.pdf').pages) for i in secuencia}

def front(inicio):
    filas = ''
    for n in range(1, 101):
        filas += f'<h2>{n}. {e(props[n]["titulo"])}</h2>'
        for i in orden[n]:
            d = N[i]; lab = f'{e(TIPO.get(d["tipo"], d["tipo"]))} · {e(d["titulo"])}'
            der = f'ver propuesta {primera[i]}' if primera[i] != n else (str(inicio[i]) if inicio else '0000')
            filas += f'<a class="r" href="http://ir.local/{i}"><span>{lab}</span><b>{der}</b></a>'
    return f"""<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><style>{F}
@page{{size:A4;margin:16mm 16mm 18mm}}body{{margin:0;font-family:PJS,sans-serif;color:#111}}
.tapa{{height:261mm;display:flex;flex-direction:column;justify-content:center;break-after:page}}
.tapa i{{display:block;width:16mm;height:2mm;background:#e8641e;margin-bottom:5mm}}
.tapa .k{{font-weight:800;font-size:8pt;letter-spacing:.12em;color:#cc5214;margin:0}}
.tapa h1{{font-weight:800;font-size:34pt;letter-spacing:-.02em;margin:3mm 0 8mm}}
.tapa p{{font-size:11pt;line-height:1.6;max-width:130mm;color:#333;margin:0 0 5mm}}
h1.ix{{font-weight:800;font-size:18pt;margin:0 0 4mm}}
h2{{font-weight:700;font-size:9pt;color:#cc5214;margin:9px 0 3px;break-after:avoid}}
a.r{{display:flex;gap:10px;font-size:7.6pt;line-height:1.35;color:inherit;text-decoration:none;padding:1px 0 1px 8px;break-inside:avoid}}
a.r span{{flex:1}}a.r b{{font-weight:500;white-space:nowrap}}
</style></head><body><div class="tapa"><i></i><p class="k">100 PROPUESTAS PARA LA ARGENTINA</p><h1>Todas las normas</h1>
<p>{len(N)} textos de trabajo —leyes, decretos, resoluciones, acuerdos federales, tratados y modelos provinciales y municipales— ordenados por propuesta y, dentro de cada una, por fase.</p>
<p>Son modelos para discutir y mejorar. propuestasargentina.netlify.app</p></div>
<h1 class="ix">Índice</h1>{filas}</body></html>"""

CONTRA = f"""<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><style>{F}
@page{{size:A4;margin:0}}html,body{{margin:0}}body{{font-family:PJS,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{position:relative;overflow:hidden;width:210mm;height:297mm;box-sizing:border-box;padding:28mm 22mm 24mm;background:linear-gradient(115deg,#f9b50f 0%,#eb671c 34%,#e84f2b 68%,#e84b49 100%);color:#fff;display:flex;flex-direction:column;justify-content:space-between}}
.p::after{{content:"";position:absolute;width:150mm;height:150mm;border-radius:50%;background:rgba(255,255,255,.10);right:-40mm;top:70mm}}
.top,.bot{{position:relative;z-index:1}}.lema{{font-weight:800;font-size:24pt;line-height:1.2;margin:0}}em{{font-style:normal;color:#111}}
h1{{font-weight:800;font-size:32pt;line-height:1.08;margin:16mm 0 0}}p.l{{font-weight:500;font-size:12pt;line-height:1.55;max-width:130mm;margin:10mm 0 0}}
.bot{{border-top:2px solid rgba(255,255,255,.7);padding-top:6mm;font-size:10.5pt;line-height:1.6}}.bot b{{font-weight:800;font-size:12.5pt;color:#111}}
</style></head><body><div class="p"><div class="top"><p class="lema">Una patria. Un pueblo.<br><em>Bajo un mismo cielo.</em></p>
<h1>Las normas de<br>las 100 propuestas</h1>
<p class="l">{len(N)} textos de trabajo —leyes, decretos, resoluciones, acuerdos federales, tratados y modelos provinciales y municipales— para poner en marcha el programa: qué se aprueba, cuándo y con qué trámite. Son modelos para discutir y mejorar, con sus citas cotejadas con el texto oficial.</p></div>
<div class="bot"><b>propuestasargentina.netlify.app</b><br>Programa técnico de Franco Martín López · Actualizado en {MES}</div></div></body></html>"""

def imprimir(htm, out):
    open('/tmp/_c.html', 'w').write(htm)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const q=await b.newPage();
await q.goto('file:///tmp/_c.html');await q.evaluate(()=>document.fonts.ready);
await q.pdf({{path:'{out}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/npm-tools/node_modules')})

imprimir(front(None), '/tmp/_front.pdf')
nf = len(PdfReader('/tmp/_front.pdf').pages)
inicio, pos = {}, nf
for i in secuencia: inicio[i] = pos + 1; pos += paginas[i]
imprimir(front(inicio), '/tmp/_front.pdf')
assert len(PdfReader('/tmp/_front.pdf').pages) == nf, 'el índice cambió de largo al completar los números'
imprimir(CONTRA, '/tmp/_contra.pdf')

w = PdfWriter(); w.append(PdfReader('/tmp/_front.pdf'))
for i in secuencia: w.append(PdfReader(f'datos/normas/pdf/{i}.pdf'))
if (len(w.pages) + 1) % 2: w.add_blank_page()   # total par: la contratapa cae atrás
w.append(PdfReader('/tmp/_contra.pdf'))
# índice: los vínculos http://ir.local/Nxxx pasan a saltos dentro del PDF
for pi in range(nf):
    for a in w.pages[pi].get('/Annots', []) or []:
        a = a.get_object(); act = a.get('/A')
        if not act: continue
        u = str(act.get_object().get('/URI', ''))
        if u.startswith('http://ir.local/'):
            i = u.rsplit('/', 1)[1]
            a[NameObject('/A')] = DictionaryObject({NameObject('/S'): NameObject('/GoTo'),
                NameObject('/D'): ArrayObject([w.pages[inicio[i] - 1].indirect_reference, NameObject('/Fit')])})
w.add_outline_item('Índice', 1)
for n in range(1, 101):
    propias = [i for i in orden[n] if primera[i] == n]
    destino = inicio[propias[0]] - 1 if propias else inicio[orden[n][0]] - 1
    padre = w.add_outline_item(f'{n}. {props[n]["titulo"]}', destino)
    for i in propias: w.add_outline_item(N[i]['titulo'], inicio[i] - 1, parent=padre)
w.add_metadata({'/Title': 'Todas las normas · 100 propuestas para la Argentina', '/Author': 'Franco Martín López',
                '/Subject': 'Leyes, decretos, resoluciones, acuerdos y modelos que ponen en marcha el programa.', '/Creator': 'propuestasargentina.netlify.app'})
w.page_mode = '/UseOutlines'
w.write('datos/normas/todas-las-normas.pdf')
print(f'normas {len(N)} paginas {len(w.pages)} indice {nf}')
