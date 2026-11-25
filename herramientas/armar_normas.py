# Arma los datos de normas del sitio a partir de las fuentes únicas.
#   fuente/normas/N###.json            una norma por archivo (sin el campo "otras")
#   fuente/normas_por_propuesta.json   qué normas lleva cada propuesta y en qué orden
#   fuente/organismos/<n>.json         organismos de cada propuesta (árbol y externos)
# Produce: datos/normas/<n>.json, datos/normas/lista.json, datos/normas/indice.json,
#          datos/anexo.json (normas por propuesta) y datos/anexo_org.json (organismos por propuesta).
# Uso: python3 herramientas/armar_normas.py   (desde la raíz del repositorio)
import json, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
TIPO = {'ley_nacional': 'Ley', 'decreto': 'Decreto', 'resolucion': 'Resolución', 'acuerdo_federal': 'Acuerdo federal',
        'ley_provincial': 'Modelo de ley provincial', 'tratado': 'Tratado', 'ley_aprobatoria': 'Ley aprobatoria',
        'ordenanza_modelo': 'Ordenanza modelo', 'invitacion': 'Invitación'}
GRUPOS = [('nuevo', 'Se crean'), ('modificado', 'Cambian'), ('suprimido', 'Se suprimen'), ('existente', 'Intervienen')]

props = {p['n']: p for p in json.load(open('datos/propuestas.json'))}
orden = {int(k): v for k, v in json.load(open('fuente/normas_por_propuesta.json'))['normas_por_propuesta'].items()}
normas = {}
for f in sorted(os.listdir('fuente/normas')):
    if f.endswith('.json'):
        d = json.load(open('fuente/normas/' + f)); normas[d['id']] = d

errores = []
usadas = {}
for n, ids in orden.items():
    for i in ids:
        if i not in normas: errores.append(f'la propuesta {n} pide {i}, que no existe en fuente/normas')
        usadas.setdefault(i, []).append(n)
for i in normas:
    if i not in usadas: errores.append(f'{i} no está en ninguna propuesta (sumala a fuente/normas_por_propuesta.json o borrala)')
for i, d in normas.items():
    if d.get('tipo') not in TIPO: errores.append(f'{i}: tipo desconocido {d.get("tipo")!r}')
    for k in ('id', 'tipo', 'titulo', 'sumilla', 'cuando', 'cuando_breve'):
        if not d.get(k): errores.append(f'{i}: falta {k}')
    if re.search(r'\b[BD]\d{2}\b', json.dumps(d, ensure_ascii=False)): errores.append(f'{i}: quedó un código interno de decisión (B## o D##)')
if set(orden) != set(range(1, 101)): errores.append('fuente/normas_por_propuesta.json no tiene exactamente las propuestas 1 a 100')
if errores:
    print('\n'.join('ERROR: ' + e for e in errores)); sys.exit(1)

def fase(w):
    w = w or ''
    if re.search(r'Fase III', w): return 'III'
    if re.search(r'Fase II\b', w): return 'II'
    if re.search(r'Fase I\b|Semana|Días|Año 1|año 1', w): return 'I'
    return ''

anexo, anexo_org = [], []
for n in range(1, 101):
    lst = []
    for i in orden[n]:
        d = {k: v for k, v in normas[i].items() if k != 'cuando_breve'}; otras = sorted(p for p in usadas[i] if p != n)
        d['otras'] = otras
        lst.append(d)
    org = json.load(open(f'fuente/organismos/{n}.json'))
    json.dump({'n': n, 'normas': lst, 'organismos': org}, open(f'datos/normas/{n}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    anexo.append({'n': n, 't': props[n]['titulo'], 'l': [[TIPO[d['tipo']], d['titulo'], normas[d['id']].get('cuando_breve') or d['cuando'].split(':')[0]] for d in lst]})
    g = {k: [] for k, _ in GRUPOS}
    def w(x, raiz=False):
        if not raiz and x.get('estado') in g:
            nom = x['nombre']; hoy = (x.get('hoy') or '').strip()
            if x['estado'] in ('modificado', 'suprimido') and hoy and not hoy.lower().startswith(nom.lower()): nom += f' (hoy: {hoy})'
            if nom not in g[x['estado']]: g[x['estado']].append(nom)
        for h in x.get('hijos', []): w(h)
    w(org['arbol'], True)
    gr = [[lab, g[k]] for k, lab in GRUPOS if g[k]]
    ext = [e['nombre'] for e in org.get('externos', [])]
    if ext: gr.append(['Fuera del Poder Ejecutivo', ext])
    anexo_org.append({'n': n, 't': props[n]['titulo'], 'g': gr})
json.dump(anexo, open('datos/anexo.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(anexo_org, open('datos/anexo_org.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(list(range(1, 101)), open('datos/normas/indice.json', 'w'))
lista = []
for i in sorted(normas):
    d = normas[i]
    lista.append({'id': i, 'tipo': d['tipo'], 'titulo': d['titulo'], 'sumilla': d.get('sumilla') or '', 'cuando': d.get('cuando') or '',
                  'props': sorted(usadas[i]), 'fase': fase(d.get('cuando')), 'cien': bool(re.match(r'(Semana 1|Días )', d.get('cuando') or ''))})
json.dump(lista, open('datos/normas/lista.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'normas {len(normas)} · propuestas 100 · compartidas {sum(len(v) > 1 for v in usadas.values())}')
