# Agrega marcadores (áreas y propuestas), título, autor y tema al PDF del programa.
# Lo llama pdf_programa.cjs: python3 marcadores.py entrada.pdf salida.pdf paginas.json "Nombre de la versión"
import sys, json
from pypdf import PdfReader, PdfWriter

src, out, pj, vn = sys.argv[1:5]
J = json.load(open(pj)); CL, PAG = J['cl'], J['pag']
w = PdfWriter(); w.append(PdfReader(src))
tit = '100 propuestas para la Argentina' + (' · ' + vn if vn else '')
w.add_metadata({'/Title': tit, '/Author': 'Franco Martín López',
                '/Subject': 'Programa técnico: qué se propone, por qué y cómo, con costo, plazos y forma de medir.',
                '/Keywords': 'Argentina, propuestas, programa, políticas públicas', '/Creator': 'propuestasargentina.netlify.app'})
par = {}
for k, v in CL.items():
    if k in PAG and v['l'] == 0: par[k] = w.add_outline_item(v['t'], PAG[k] - 1)
for k, v in CL.items():
    if k in PAG and v['l'] == 1: w.add_outline_item(v['t'], PAG[k] - 1, parent=par.get(v.get('a')))
w.page_mode = '/UseOutlines'
w.write(out); print('marcadores', len(PAG))
