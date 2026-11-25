// Genera los tres PDF del programa: 100-propuestas.pdf (completo), 100-propuestas-extendido.pdf y 100-propuestas-resumido.pdf.
// Imprime la portada del sitio en modo PDF (?pdf=1): índice con números de página, marcadores, título y autor,
// tapa, contenido y contratapa; total de páginas par.
// Uso (desde la raíz del repositorio): node herramientas/pdf_programa.cjs [completo|extendido|resumido]   (sin argumento, los tres)
const {chromium}=require('playwright');
const {execSync,spawn}=require('child_process');
const fs=require('fs'),path=require('path');
const R=path.resolve(__dirname,'..');process.chdir(R);
const PORT=8765,BASE='http://localhost:'+PORT+'/';
const VERS={completo:{g:3,out:'100-propuestas.pdf',nom:''},extendido:{g:2,out:'100-propuestas-extendido.pdf',nom:'Versión extendida'},resumido:{g:1,out:'100-propuestas-resumido.pdf',nom:'Versión resumida'}};
const foot=t=>'<div style="font-size:8px;width:100%;text-align:center;color:#777">100 propuestas para la Argentina · <span class="pageNumber"></span>'+(t?'/'+t:'')+'</div>';
const MES=(()=>{const d=new Date();return ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][d.getMonth()]+' de '+d.getFullYear()})();
const CONTRA=`<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{font-family:'PJS';font-weight:500;src:url(${BASE}fuentes/plus-jakarta-sans-latin-500-normal.woff2) format('woff2')}
@font-face{font-family:'PJS';font-weight:800;src:url(${BASE}fuentes/plus-jakarta-sans-latin-800-normal.woff2) format('woff2')}
@page{size:A4;margin:0}html,body{margin:0;height:100%}
body{font-family:'PJS',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.p{width:210mm;height:297mm;box-sizing:border-box;background:linear-gradient(115deg,#f9b50f 0%,#eb671c 34%,#e84f2b 68%,#e84b49 100%);color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:28mm 24mm;position:relative;overflow:hidden}
.p::after{content:"";position:absolute;width:150mm;height:150mm;border-radius:50%;background:rgba(255,255,255,.10);right:-40mm;top:70mm}
.top,.bot{position:relative;z-index:1}
.lema{font-weight:800;font-size:26pt;line-height:1.2;margin:0}.lema em{font-style:normal;color:#111}
h1{font-weight:800;font-size:34pt;line-height:1.05;margin:14mm 0 0;letter-spacing:-.02em}h1 em{font-style:normal;color:#111}
p.l{font-weight:500;font-size:12.5pt;line-height:1.55;max-width:140mm;margin:10mm 0 0}
.bot{border-top:2px solid rgba(255,255,255,.7);padding-top:6mm;font-weight:500;font-size:11pt;line-height:1.6}
.bot b{font-weight:800;font-size:13pt;color:#111}
</style></head><body><div class="p"><div class="top">
<p class="lema">Una patria. Un pueblo.<br><em>Bajo un mismo cielo.</em></p>
<h1>100 propuestas para <em>la Argentina</em></h1>
<p class="l">Qué se propone, por qué y cómo se hace, con su costo, sus plazos y la forma de medir si se cumplió. Para planificar, invertir y terminar lo que se empieza; abrir con tiempo; bajar los impuestos que frenan el trabajo; modernizar la educación; y que todo poder rinda cuentas.</p>
</div><div class="bot"><b>propuestasargentina.netlify.app</b><br>Programa técnico de Franco Martín López · Actualizado en ${MES}</div></div></body></html>`;

async function una(b,v){
const ctx=await b.newContext({viewport:{width:900,height:1200}});const q=await ctx.newPage();
await q.goto(BASE+'?pdf=1');await q.waitForSelector('#p100');
await q.evaluate(g=>{document.querySelector('[data-g="'+g+'"]').click();document.body.dataset.pn=g;const cg=document.querySelector('.cargos');if(cg)cg.dataset.pn=g;document.querySelectorAll('.faq details').forEach(d=>d.open=true);document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager')},v.g);
if(v.g===3){await q.waitForSelector('.anx-p',{timeout:60000}).catch(()=>{});await q.waitForSelector('.anx-o',{timeout:60000}).catch(()=>{});}
await q.waitForFunction(()=>[...document.images].every(i=>i.complete),null,{timeout:60000}).catch(()=>{});
await q.waitForTimeout(800);
// índice impreso: 1) índice con números provisorios y marcas invisibles, 2) se ubica cada marca en el PDF, 3) se completan los números
const CL=await q.evaluate(g=>{const ks={};const areas=["I","II","III","IV","V","VI","VII","VIII","IX","X"];
 const T=a=>{const el=document.getElementById('a'+a);const h=el&&el.querySelector('h2');return h?h.textContent.trim():a};
 areas.forEach(a=>{if(document.getElementById('a'+a))ks['a'+a]={t:a+'. '+T(a),l:0}});
 document.querySelectorAll('.prop').forEach(el=>{ks[el.id]={t:el.id.slice(1)+'. '+el.querySelector('h3').textContent.trim(),l:1,a:'a'+el.getAttribute('data-area')}});
 [["cuenta","La cuenta: cómo se paga"],["cargos","Los cargos"],["cierre","Las etapas"],["porque","El porqué"],["preguntas","Preguntas difíciles"],["cien","Los primeros 100 días"],["anexo","Anexo I: las normas"],["anexo2","Anexo II: los organismos"],["autor","Quién escribe"]].forEach(x=>{if(document.getElementById(x[0])&&!(g<3&&/^anexo/.test(x[0])))ks[x[0]]={t:x[1],l:0}});
 window.PAGS={};Object.keys(ks).forEach(k=>window.PAGS[k]='000');window.pIndice();
 Object.keys(ks).forEach(k=>{const el=document.getElementById(k);const m=document.createElement('span');m.className='__mk';m.textContent='QQMK'+k+'QQ';m.style.cssText='position:absolute;font-size:3px;color:#fff;line-height:1';el.insertBefore(m,el.firstChild)});
 return ks},v.g);
const opt=t=>({format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:foot(t)});
await q.pdf({path:'/tmp/_marcas.pdf',...opt(null)});
const PAG={};execSync('pdftotext /tmp/_marcas.pdf /tmp/_marcas.txt');fs.readFileSync('/tmp/_marcas.txt','utf8').split('\f').forEach((tx,i)=>{for(const m of tx.matchAll(/QQMK(\w+?)QQ/g))if(!PAG[m[1]])PAG[m[1]]=i+1});
const falt=Object.keys(CL).filter(k=>!PAG[k]);if(falt.length)console.log('sin página:',falt.join(' '));
await q.evaluate(P=>{window.PAGS=P;window.pIndice();document.querySelectorAll('.__mk').forEach(m=>m.remove())},PAG);
fs.writeFileSync('/tmp/_pags.json',JSON.stringify({cl:CL,pag:PAG}));
await q.pdf({path:'/tmp/_cuerpo.pdf',...opt(null)});
const n=parseInt(execSync("pdfinfo /tmp/_cuerpo.pdf | awk '/Pages/{print $2}'").toString());
let total=n+1, blanco=false; if(total%2){total++;blanco=true}
await q.pdf({path:'/tmp/_cuerpo.pdf',...opt(total)});
const c=await ctx.newPage();await c.setContent(CONTRA,{waitUntil:'networkidle'});
await c.pdf({path:'/tmp/_contra.pdf',format:'A4',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
const partes=['/tmp/_cuerpo.pdf'];
if(blanco){const w=await ctx.newPage();await w.setContent('<html><body></body></html>');await w.pdf({path:'/tmp/_blanco.pdf',format:'A4'});partes.push('/tmp/_blanco.pdf')}
partes.push('/tmp/_contra.pdf');
execSync('pdfunite '+partes.join(' ')+' /tmp/_unido.pdf');
execSync('python3 herramientas/marcadores.py /tmp/_unido.pdf '+v.out+' /tmp/_pags.json "'+v.nom+'"');
console.log(v.out,'paginas',total,'cuerpo',n,'blanco',blanco);
await ctx.close();}
(async()=>{
const srv=spawn('python3',['-m','http.server',String(PORT)],{cwd:R,stdio:'ignore'});
await new Promise(r=>setTimeout(r,1200));
try{const b=await chromium.launch();
 const pedidas=process.argv.slice(2);const lista=pedidas.length?pedidas:['completo','extendido','resumido'];
 for(const k of lista){if(!VERS[k])throw new Error('versión desconocida: '+k);await una(b,VERS[k]);}
 await b.close();}finally{srv.kill();}
})().catch(e=>{console.error(e);process.exit(1)});
