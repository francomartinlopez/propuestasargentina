# Arma datos-informe.json para la web de informes de Plexum (especificación «Datos que cada web publica», v1.2).
# 100 Propuestas publica cada propuesta como novedad «otro», contenido permanente (fecha_dato null).
# No cambia nada visible del sitio. El id de cada propuesta es estable: se guarda en datos/propuestas.json
# (campo id_informe) la primera vez y no se cambia aunque cambie el número o el título.
# Uso: python3 herramientas/datos_informe.py
import json, os, re, unicodedata, datetime

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
SITE = 'https://propuestasargentina.netlify.app/'
RUBROS = [('Industria', r'industri|fábrica|manufactur|metalmec|siderur|petroquím|automotr|textil|astiller|química|urea|fertilizant'),
          ('Agro', r'\bagro|campo\b|granos|soja|trigo|maíz|ganad|lecher|rural|cosecha|biocombustib|semilla|forestal|pesca|riego|economías regionales'),
          ('Minería', r'miner|litio|cobre|uranio|potasio|fosfat'),
          ('Energía', r'energ|\bgas\b|gasoduct|petróle|electric|nuclear|vaca muerta|renovable|hidroeléctr|represa|combustible'),
          ('Construcción', r'vivienda|obra|ruta|camino|construcc|infraestructura|acueduct|cloaca|ferrocarril|tren|puerto|hidrovía|canal'),
          ('Comercio y servicios', r'comercio|turismo|servicios|conocimiento|software|transporte|logístic|banco|crédito|consumo|alquiler')]
EXPOSICION = [('Exporta', r'export'), ('Importa insumos', r'import|insumo'), ('Deuda en dólares', r'deuda en dólares|endeudamiento externo|deuda externa'),
              ('Energía intensiva', r'tarifa|electrointensiv|costo de la energía'), ('Mano de obra intensiva', r'empleo|trabajo|laboral|trabajador'),
              ('Vende al Estado', r'compras? públicas|contrataciones|licitaci|proveedores del estado'),
              ('Vende a minería y energía', r'proveedor|contenido nacional|compre local')]

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def recorte(texto, maximo=60):
    palabras = texto.split()
    if len(palabras) <= maximo: return texto
    frases, out = re.split(r'(?<=[.;])\s+', texto), []
    for f in frases:
        if len(' '.join(out + [f]).split()) > maximo: break
        out.append(f)
    return ' '.join(out) if out else ' '.join(palabras[:maximo]).rstrip(',;:') + '…'

D = json.load(open('datos/propuestas.json'))
cambio = False
for p in D:
    if not p.get('id_informe'):
        p['id_informe'] = 'propuesta-' + slug(p['titulo'])[:60].rstrip('-'); cambio = True
ids = [p['id_informe'] for p in D]
assert len(set(ids)) == len(ids), 'id_informe repetido'
if cambio: json.dump(D, open('datos/propuestas.json', 'w'), ensure_ascii=False, indent=2)


nov = []
for p in sorted(D, key=lambda x: x['n']):
    base = p['titulo'] + ' ' + p['resumen']
    alcance = {'nivel': 'nacional', 'provincia': '', 'localidad': '', 'pais': 'Argentina'}   # el programa es nacional
    nov.append({'id': p['id_informe'], 'fecha_dato': None, 'titulo': f'Propuesta {p["n"]}: {p["titulo"]}',
                'resumen': recorte(p['resumen']), 'tipo': 'otro', 'eje': 'Región y rubro', 'alcance': alcance,
                'rubros': [r for r, pat in RUBROS if re.search(pat, base, re.I)], 'subrubros': [],
                'exposicion': [x for x, pat in EXPOSICION if re.search(pat, base, re.I)],
                'url': f'{SITE}p/{p["n"]}/'})

ahora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).replace(microsecond=0)
out = {'web': '100 Propuestas', 'version': '1.0', 'generado': ahora.isoformat(),
       'indicadores': [], 'novedades': nov, 'agenda': [], 'faltantes': []}
json.dump(out, open('datos-informe.json', 'w'), ensure_ascii=False, indent=1)
print(f'datos-informe.json: {len(nov)} propuestas')
