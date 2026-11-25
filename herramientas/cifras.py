# Pone al día en index.html las cifras que dependen de los archivos: cantidad de normas, páginas de los PDF,
# peso del PDF de normas y fecha de actualización. Así no queda ninguna cifra escrita a mano.
# Uso: python3 herramientas/cifras.py   (después de armar los PDF)
import os, re, json, datetime
from pypdf import PdfReader

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
pg = lambda f: len(PdfReader(f).pages)
mil = lambda n: f'{n:,}'.replace(',', '.')
comp, ext, res = pg('100-propuestas.pdf'), pg('100-propuestas-extendido.pdf'), pg('100-propuestas-resumido.pdf')
nor = pg('datos/normas/todas-las-normas.pdf')
nn = len([f for f in os.listdir('fuente/normas') if f.endswith('.json')])
mb = os.path.getsize('datos/normas/todas-las-normas.pdf') / 1e6
hoy = datetime.date.today().strftime('%d/%m/%Y')
h = open('index.html').read()
def sub(pat, rep):
    global h
    h2, k = re.subn(pat, rep, h)
    if not k: raise SystemExit(f'no se encontró en index.html: {pat}')
    h = h2
sub(r'(id="cf-normas">)[\d.]+', rf'\g<1>{mil(nn)}')
sub(r'(id="cf-pags">)[\d.]+', rf'\g<1>{mil(comp + nor)}')
sub(r'(id="cf-pdet">)[^<]*', rf'\g<1>{mil(comp)} del programa y {mil(nor)} de normas')
sub(r'Programa completo \(PDF, \d+ páginas\)', f'Programa completo (PDF, {comp} páginas)')
sub(r'Programa extendido \(PDF, \d+ páginas\)', f'Programa extendido (PDF, {ext} páginas)')
sub(r'Programa resumido \(PDF, \d+ páginas\)', f'Programa resumido (PDF, {res} páginas)')
sub(r'(<span id="cf-nmb">)[^<]*', rf'\g<1>{round(mb):d} MB')
sub(r'(<span class="cf-fecha">)[^<]*', rf'\g<1>{hoy}')
open('index.html', 'w').write(h)
print(f'normas {nn} · programa {comp}/{ext}/{res} · normas {nor} páginas, {round(mb)} MB · fecha {hoy}')
