// Genera el PDF de cada norma en datos/normas/pdf/N###.pdf a partir de fuente/normas/.
// Uso (desde la raíz del repositorio):
//   node herramientas/pdf_normas.cjs            todas las normas
//   node herramientas/pdf_normas.cjs N444 N448  solo esas
// Necesita Playwright (chromium). Las fuentes salen de fuentes/.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const R = path.resolve(__dirname, '..');
process.chdir(R);

const TIPO = { ley_nacional: 'Proyecto de ley', decreto: 'Proyecto de decreto', resolucion: 'Proyecto de resolución',
  acuerdo_federal: 'Modelo de acuerdo federal', ley_provincial: 'Modelo de ley provincial', tratado: 'Proyecto de tratado',
  ley_aprobatoria: 'Proyecto de ley aprobatoria', ordenanza_modelo: 'Modelo de ordenanza', invitacion: 'Invitación y texto modelo' };
const e = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const pars = s => String(s || '').split(/\n+/).filter(x => x.trim()).map(x => `<p>${e(x)}</p>`).join('');
const F = w => `@font-face{font-family:PJS;font-weight:${w};src:url(file://${R}/fuentes/plus-jakarta-sans-latin-${w}-normal.woff2) format('woff2')}`;

const props = Object.fromEntries(JSON.parse(fs.readFileSync('datos/propuestas.json')).map(p => [p.n, p]));
const orden = JSON.parse(fs.readFileSync('fuente/normas_por_propuesta.json')).normas_por_propuesta;
const deProp = {};
for (const [n, ids] of Object.entries(orden)) for (const i of ids) (deProp[i] = deProp[i] || []).push(+n);

const CSS = `${F(400)}${F(500)}${F(700)}${F(800)}
@page{size:A4;margin:18mm 18mm 20mm}
body{margin:0;font-family:'Liberation Serif','Times New Roman',serif;font-size:10.5pt;line-height:1.62;color:#111}
.hd{font-family:PJS;font-weight:800;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;color:#cc5214;border-bottom:1.5px solid #cc5214;padding-bottom:4px;margin-bottom:14px}
.k{font-family:PJS;font-weight:700;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:#444;margin:0 0 4px}
h1{font-family:PJS;font-weight:800;font-size:15pt;line-height:1.2;text-align:center;margin:0 6% 6px}
.su{font-family:PJS;font-weight:400;font-size:8.5pt;line-height:1.45;color:#444;text-align:center;margin:0 2% 12px}
.meta{font-family:PJS;font-size:8pt;line-height:1.45;color:#333;border:1px solid #ddd;border-radius:4px;padding:6px 8px;margin-bottom:14px}
.meta div{margin:0}
h2{font-family:PJS;font-weight:800;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;margin:16px 0 6px;break-after:avoid}
h3{font-family:PJS;font-weight:700;font-size:9.5pt;margin:14px 0 6px;break-after:avoid}
p{margin:0 0 8px;text-align:justify}
.fo{text-align:center;font-weight:700;margin:12px 0}
.art b{font-weight:700}
.fin{font-family:PJS;font-size:8pt;color:#666;margin-top:18px;border-top:1px solid #ddd;padding-top:6px}
.var{font-size:9.5pt}`;

function html(d) {
  const ps = (deProp[d.id] || []).slice().sort((a, b) => a - b)
    .map(n => `Propuesta ${n}: ${e(props[n] ? props[n].titulo : '')}`).join(' · ');
  let h = `<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><style>${CSS}</style></head><body>
<div class="hd">100 propuestas para la Argentina · Modelo de trabajo · ${e(d.id)}</div>
<p class="k">${e(TIPO[d.tipo] || d.tipo)}</p><h1>${e(d.titulo)}</h1><p class="su">${e(d.sumilla)}</p>
<div class="meta"><div>${ps}</div><div>Cuándo: ${e(d.cuando)}</div>${d.tramite ? `<div>Trámite: ${e(d.tramite)}</div>` : ''}</div>`;
  if (d.motivos) h += `<h2>${d.tipo === 'tratado' ? 'Preámbulo' : 'Fundamentos'}</h2>${pars(d.motivos)}`;
  if (d.visto) h += `<h2>Visto</h2>${pars(d.visto)}`;
  if (d.considerando && d.considerando.length) h += `<h2>Considerando:</h2>${d.considerando.map(x => `<p>${e(x)}</p>`).join('')}`;
  if (d.formula) h += (/^(TRATADO|ACUERDO|CONVENIO|COMUNICACIÓN)/.test(d.formula) ? '<h2>Preámbulo</h2>' + pars(d.formula) : String(d.formula).split(/\n+/).filter(x => x.trim()).map(x => `<p class="fo">${e(x)}</p>`).join(''));
  for (const c of d.capitulos || []) {
    if (c.titulo) h += `<h3>${e(c.titulo)}</h3>`;
    for (const a of c.articulos || []) {
      const t = String(a.texto || '').split(/\n+/);
      h += `<p class="art"><b>ARTÍCULO ${e(a.n)}°.-${a.epigrafe ? ' ' + e(a.epigrafe) + '.' : ''}</b> ${e(t[0])}</p>` + t.slice(1).filter(x => x.trim()).map(x => `<p>${e(x)}</p>`).join('');
    }
  }
  if (d.variantes && d.variantes.length) {
    h += `<h2>Variantes según cómo esté la norma vigente al enviarse</h2>`;
    for (const v of d.variantes) h += `<p class="var"><b>Variante ${e(v.variante)}.</b> Si ${e(String(v.condicion || '').replace(/^./, c => c.toLowerCase()))} ${e(v.texto)}</p>`;
  }
  return h + `<p class="fin">Texto de trabajo para discutir y mejorar. propuestasargentina.netlify.app</p></body></html>`;
}

(async () => {
  let ids = process.argv.slice(2);
  if (!ids.length) ids = fs.readdirSync('fuente/normas').filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)).sort();
  fs.mkdirSync('datos/normas/pdf', { recursive: true });
  const b = await chromium.launch(); const q = await b.newPage();
  for (const id of ids) {
    const d = JSON.parse(fs.readFileSync(`fuente/normas/${id}.json`));
    const tmp = `/tmp/_norma_${id}.html`; fs.writeFileSync(tmp, html(d));
    await q.goto('file://' + tmp); await q.evaluate(() => document.fonts.ready);
    await q.pdf({ path: `datos/normas/pdf/${id}.pdf`, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#555"><span class="pageNumber"></span>/<span class="totalPages"></span></div>' });
    fs.unlinkSync(tmp);
  }
  // sin PDF de normas que ya no existen
  const vivas = new Set(fs.readdirSync('fuente/normas').map(f => f.replace('.json', '.pdf')));
  for (const f of fs.readdirSync('datos/normas/pdf')) if (!vivas.has(f)) { fs.unlinkSync('datos/normas/pdf/' + f); console.log('borrado', f); }
  await b.close(); console.log('pdf de normas', ids.length);
})();
