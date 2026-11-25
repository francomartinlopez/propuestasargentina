window.montarMapa=function(host){var R=host.attachShadow({mode:"open"});R.innerHTML={{INTERIOR}};
(function(){
const D={{D}};
const col={nucleo:'var(--nuc)',proveedor:'var(--pro)',puerto:'var(--pue)',paso:'var(--pas)'};
const tipoTxt={nucleo:'Núcleo productivo',proveedor:'Proveedores',puerto:'Puerto o salida',paso:'Paso internacional'};
const NS='http://www.w3.org/2000/svg';
let grupo='complejo',actual=D.capas[0].id;const X={urb:false,inf:false,inl:false};
const ICOL={ferrocarril:'#6b4a2b',ruta:'#e8a400',gasoducto:'#1baf7a',oleoducto:'#111111',hidrovia:'#2a9bd6',electrica:'#e87ba4',puerto:'#e8a400'};
const ITXT={ferrocarril:'Ferrocarril',ruta:'Ruta o autopista',gasoducto:'Gasoducto',oleoducto:'Oleoducto',hidrovia:'Vía navegable',electrica:'Línea eléctrica',puerto:'Puerto o nodo'};
const ETXT={nueva:'nueva',refaccion:'refacción',ampliacion:'ampliación'};
const $=s=>R.querySelector(s);
function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e}
function chips(){const c=$('#chips');c.innerHTML='';if(grupo==='todos'){c.style.display='none';return}c.style.display='';
 D.capas.filter(x=>x.g===grupo).forEach(x=>{const b=document.createElement('button');b.textContent=x.nom;if(x.id===actual)b.className='on';b.onclick=()=>{actual=x.id;render()};c.appendChild(b)})}
function render(){
 if(grupo!=='todos'&&!D.capas.find(x=>x.id===actual&&x.g===grupo))actual=D.capas.find(x=>x.g===grupo).id;
 chips();const capas=grupo==='todos'?D.capas:D.capas.filter(x=>x.id===actual);
 const C=$('#cors'),P=$('#pts'),Lb=$('#lbls'),A=$('#areas'),I=$('#infra');C.innerHTML=P.innerHTML=Lb.innerHTML=A.innerHTML=I.innerHTML='';

 capas.forEach(c=>c.cor.forEach(([n,ps])=>{const pl=el('polyline',{class:'cor',points:ps.map(p=>D.xy[p].join(',')).join(' '),stroke:'var(--muted)'});const t=el('title',{});t.textContent=n;pl.appendChild(t);C.appendChild(pl)}));
 var S=1;const svg=$('#svg');
 if(grupo==='todos'){svg.setAttribute('viewBox','0 0 330 680')}else{const xs=[],ys=[];capas.forEach(c=>{c.pts.forEach(p=>{xs.push(D.xy[p[0]][0]);ys.push(D.xy[p[0]][1])});c.cor.forEach(([,ps])=>ps.forEach(p=>{xs.push(D.xy[p][0]);ys.push(D.xy[p][1])}));
   if(X.inf)c.inf.forEach(n=>D.infra[n].pts.forEach(([x,y])=>{xs.push(x);ys.push(y)}));
   const ds=[...(X.urb?c.urb.flatMap(u=>u.d):[]),...(X.inl?c.loc.concat(c.lej):[])];
   ds.forEach(k=>{const m=D.dp[k].match(/-?[\d.]+,-?[\d.]+/g)||[];m.forEach((q,i)=>{if(i%4)return;const [x,y]=q.split(',').map(Number);xs.push(x);ys.push(y)})})});
  let x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);let w=Math.max(x1-x0,90)+70,h=Math.max(y1-y0,90)+50;const cx=(x0+x1)/2+18,cy=(y0+y1)/2;
  if(w/h>330/680*1.6)h=w/(330/680*1.6);else w=Math.max(w,h*0.75);S=Math.max(w/330,h/680);svg.setAttribute('viewBox',`${cx-w/2} ${cy-h/2} ${w} ${h}`)}
 const dibujados={};const dep=(k,cl,tit)=>{const id=cl+k;if(dibujados[id])return;dibujados[id]=1;const p=el('path',{class:'dep '+cl,d:D.dp[k]});const t=el('title',{});t.textContent=D.dn[k]+' · '+tit;p.appendChild(t);p.onclick=()=>fichaArea(D.dn[k],tit);A.appendChild(p)};
 if(X.inl)capas.forEach(c=>{c.lej.forEach(k=>dep(k,'lej','Área alejada: proveedores'));c.loc.forEach(k=>dep(k,'loc','Área local'))});
 if(X.urb)capas.forEach(c=>c.urb.forEach(u=>u.d.forEach(k=>dep(k,'urb',u.t+': '+u.n))));
 if(X.inf){const vis={};capas.forEach(c=>c.inf.forEach(n=>{if(vis[n])return;vis[n]=1;const f=D.infra[n];
   if(f.pts.length===1){const [x,y]=f.pts[0];const w=grupo==='todos'?5:8*S;const r=el('rect',{class:'inf',x:x-w/2,y:y-w/2,width:w,height:w,fill:ICOL.puerto,stroke:'var(--ink)','stroke-width':1.2});const t=el('title',{});t.textContent=n;r.appendChild(t);r.onclick=()=>fichaInf(n);I.appendChild(r);return}
   const pl=el('polyline',{class:'inf '+f.e,points:f.pts.map(p=>p.join(',')).join(' '),stroke:ICOL[f.t],'stroke-width':f.t==='hidrovia'?4:3.2});const t=el('title',{});t.textContent=n+' ('+ETXT[f.e]+')';pl.appendChild(t);pl.onclick=()=>fichaInf(n);I.appendChild(pl)}))}
 leyenda2(capas);
 const vistos={};capas.forEach(c=>c.pts.forEach(([n,t,d])=>{(vistos[n]=vistos[n]||{t,items:[]}).items.push([c.nom,d]);if(t==='nucleo')vistos[n].t='nucleo'}));
 Object.entries(vistos).forEach(([n,v])=>{const [x,y]=D.xy[n];const r=grupo==='todos'?3.2:5*S;
  const c=el('circle',{class:'pt',cx:x,cy:y,r,fill:col[v.t]});c.onclick=()=>ficha(n,v,c);P.appendChild(c);
  if(grupo!=='todos'){const tx=el('text',{class:'lbl',x:x+7*S,y:y+3*S,'font-size':8.5*S,'stroke-width':2.5*S});tx.textContent=n;Lb.appendChild(tx)}});
 // extremos de corredores que no son puntos de la capa
 capas.forEach(c=>c.cor.forEach(([,ps])=>ps.forEach(p=>{if(vistos[p])return;vistos[p]=1;const [x,y]=D.xy[p];P.appendChild(el('circle',{cx:x,cy:y,r:2.6*S,fill:'var(--muted)'}));
  if(grupo!=='todos'){const tx=el('text',{class:'lbl',x:x+6*S,y:y+3*S,'font-size':8*S,'stroke-width':2.5*S,fill:'var(--muted)'});tx.textContent=p;Lb.appendChild(tx)}})));
 despejar(S);panel(capas)}
function despejar(S){const puestos=[];const hit=(a,b)=>!(a.x+a.width<b.x||b.x+b.width<a.x||a.y+a.height<b.y||b.y+b.height<a.y);
 R.querySelectorAll('#lbls text').forEach(t=>{const x0=+t.getAttribute('x'),y0=+t.getAttribute('y');
  const ops=[[0,0,'start'],[-14*S,0,'end'],[-7*S,-9*S,'middle'],[-7*S,11*S,'middle'],[0,9*S,'start'],[0,-9*S,'start'],[-14*S,9*S,'end'],[-14*S,-9*S,'end']];
  for(const [dx,dy,a] of ops){t.setAttribute('x',x0+dx);t.setAttribute('y',y0+dy);t.setAttribute('text-anchor',a);const b=t.getBBox();if(!puestos.some(p=>hit(p,b))){puestos.push(b);return}}
  t.style.display='none'})}
function panel(capas){const p=$('#panel');
 if(grupo==='todos'){p.innerHTML=`<h2>Todo junto</h2><div class="val">${D.capas.length} capas: complejos y economías regionales</div><h3>Qué muestra</h3><ul><li>Dónde se superponen los complejos: Rosario, Bahía Blanca, Córdoba y Campana–Zárate concentran núcleo, proveedores y puertos a la vez.</li><li>Tocá un punto para ver qué cadenas pasan por ahí.</li></ul>${X.inf?'<h3>Infraestructura</h3><ul><li><span>Todas las obras del programa a la vez. Tocá una línea para ver cuál es.</span></li></ul>':''}<div class="ficha" id="ficha"></div>`;return}
 const c=capas[0],by=t=>c.pts.filter(x=>x[1]===t);
 const li=a=>a.map(([n,,d])=>`<li>${n} <span>· ${d}</span></li>`).join('');
 p.innerHTML=`<h2>${c.nom}</h2><div class="val">${c.val}</div>`+
 (by('nucleo').length?`<h3>Núcleo</h3><ul>${li(by('nucleo'))}</ul>`:'')+
 (by('proveedor').length?`<h3>Proveedores</h3><ul>${li(by('proveedor'))}</ul>`:'')+
 (by('puerto').length+by('paso').length?`<h3>Salidas</h3><ul>${li(by('puerto').concat(by('paso')))}</ul>`:'')+
 (c.cor.length?`<h3>Corredores</h3><ul>${c.cor.map(x=>`<li>${x[0]}</li>`).join('')}</ul>`:'')+
 `<h3>Obras necesarias</h3><ul>${c.obras.map(o=>`<li>${o}</li>`).join('')}</ul>`+extrasPanel(c)+`<div class="ficha" id="ficha"></div>`}
function extrasPanel(c){let h='';const nd=a=>a.map(k=>D.dn[k].replace(/ \(.*\)/,'')).join(', ');
 if(X.urb)h+=`<h3 style="color:#7b4fd6">Desarrollo urbano local</h3><ul>${c.urb.map(u=>`<li><b>${u.t}</b> <span>· ${u.n}.</span></li>`).join('')}</ul>`;
 if(X.inf)h+=`<h3 style="color:#b07d00">Infraestructura de conectividad</h3>`+(c.inf.length?`<ul>${c.inf.map(n=>{const f=D.infra[n];return `<li><span class="sw" style="background:${ICOL[f.t]};width:9px;height:9px;margin-right:4px"></span>${n}<span class="est">${ETXT[f.e]} · ${f.p}</span></li>`}).join('')}</ul>`:'<ul><li><span>No requiere obras de transporte específicas; fibra óptica en los núcleos del interior.</span></li></ul>');
 if(X.inl)h+=`<h3>Área de influencia</h3><ul><li><b style="color:#eb6834">Local:</b> <span>${nd(c.loc)}</span></li>${c.lej.length?`<li><b style="color:#2a78d6">Alejada (proveedores):</b> <span>${nd(c.lej)}</span></li>`:''}</ul>`;
 return h}
function fichaArea(n,t){const f=$('#ficha');if(!f)return;f.style.display='block';f.innerHTML=`<b>${n}</b><span style="color:var(--muted);font-size:13px">${t}</span>`}
function fichaInf(n){const f=$('#ficha');if(!f)return;const i=D.infra[n];f.style.display='block';f.innerHTML=`<b>${n}</b><span style="color:var(--muted);font-size:13px">${ITXT[i.t]} · obra ${ETXT[i.e]} · ${i.p}</span>`}
function leyenda2(capas){const L=$('#leg2');const it=[];
 if(X.urb)it.push('<span><span class="sw" style="background:url(#);background:repeating-linear-gradient(45deg,#7b4fd6 0 2px,transparent 2px 5px);border:1px solid #7b4fd6;vertical-align:-1px;margin-right:5px"></span>Desarrollo urbano local</span>');
 if(X.inl)it.push('<span><span class="sw" style="background:rgba(235,104,52,.35);vertical-align:-1px;margin-right:5px"></span>Influencia local</span><span><span class="sw" style="background:rgba(42,120,214,.32);vertical-align:-1px;margin-right:5px"></span>Influencia alejada</span>');
 if(X.inf){const ts=new Set();capas.forEach(c=>c.inf.forEach(n=>ts.add(D.infra[n].t)));ts.forEach(t=>it.push(t==='puerto'?`<span><span class="sw" style="background:${ICOL.puerto};border:1px solid var(--ink);vertical-align:-1px;margin-right:5px"></span>${ITXT[t]}</span>`:`<span><i class="l" style="border-top-color:${ICOL[t]}"></i>${ITXT[t]}</span>`));it.push('<span><i class="l" style="border-top-style:dashed;border-top-color:var(--muted)"></i>Obra nueva (línea cortada)</span>')}
 L.style.display=it.length?'flex':'none';L.innerHTML=it.join('')}
function ficha(n,v,c){R.querySelectorAll('.pt.sel').forEach(e=>e.classList.remove('sel'));c.classList.add('sel');
 const f=$('#ficha');f.style.display='block';f.innerHTML=`<b>${n}</b><span style="color:var(--muted);font-size:12px">${tipoTxt[v.t]}</span><ul style="margin:6px 0 0;padding-left:18px">${v.items.map(([k,d])=>`<li>${grupo==='todos'?k+': ':''}${d}</li>`).join('')}</ul>`;
 if(innerWidth<820)f.scrollIntoView({behavior:'smooth',block:'nearest'})}
R.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{R.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));grupo=b.dataset.g;render()});
['urb','inf','inl'].forEach(k=>{const i=$('#x-'+k);i.onchange=()=>{X[k]=i.checked;i.parentNode.classList.toggle('on',i.checked);render()}});
render();

})()};