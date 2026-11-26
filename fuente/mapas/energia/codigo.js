var D={{D}};var lst=R.getElementById?R.getElementById('lst'):R.querySelector('#lst');var ch=R.getElementById?R.getElementById('chips'):R.querySelector('#chips');
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var EST=[['en_marcha','En marcha o por arrancar','--em'],['planificada','Planificadas, sin hacer','--pl'],['frenada','Frenadas','--fr'],['evaluar','A evaluar','--ev'],['funciona','Ya funcionan','--fu']];
var GR=[['todo','Todo'],['electricidad','Líneas eléctricas'],['internacional','Con otros países'],['represa','Represas'],['gas','Gas con otros países']];
EST.forEach(function(e){var o=D.filter(function(t){return t.estado===e[0]});if(!o.length)return;var h=document.createElement('h6');h.textContent=e[1];h.setAttribute('data-e',e[0]);lst.appendChild(h);
o.forEach(function(t){var b=document.createElement('button');b.className='it';b.setAttribute('data-t',t.id);b.setAttribute('data-g',t.grupo);
b.innerHTML='<h5><b style="background:var('+e[2]+')"></b>'+esc(t.nombre)+'</h5><div class="km">'+esc(t.dato)+'</div><dl class="det"><dt>Hoy</dt><dd>'+esc(t.hoy)+'</dd><dt>Propuesta</dt><dd class="p">'+esc(t.prop)+'</dd><dt>Fuente</dt><dd class="s">'+esc(t.fuente)+'</dd></dl>';
b.addEventListener('click',function(){sel(t.id===cur?null:t.id)});lst.appendChild(b)})});
var cur=null;function sel(id){cur=id;R.querySelectorAll('.it').forEach(function(e){e.classList.toggle('on',e.getAttribute('data-t')===id)});
R.querySelectorAll('.ob').forEach(function(e){e.classList.toggle('sel',e.getAttribute('data-t')===id)})}
R.querySelectorAll('.ob').forEach(function(e){e.addEventListener('click',function(){var id=e.getAttribute('data-t');sel(id);var b=R.querySelector('.it[data-t="'+id+'"]');if(b)b.scrollIntoView({block:'nearest',behavior:'smooth'})})});
var gcur='todo';GR.forEach(function(g){var b=document.createElement('button');b.textContent=g[1];b.setAttribute('data-g',g[0]);if(g[0]===gcur)b.className='on';
b.addEventListener('click',function(){gcur=g[0];ch.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});filtrar()});ch.appendChild(b)});
function filtrar(){function ve(g){return gcur==='todo'||g===gcur}
R.querySelectorAll('.ob').forEach(function(e){e.classList.toggle('off',!ve(e.getAttribute('data-g')))});
R.querySelectorAll('.it').forEach(function(e){e.classList.toggle('off',!ve(e.getAttribute('data-g')))});
R.querySelectorAll('.lst h6').forEach(function(h){var s=h.nextElementSibling,v=false;while(s&&s.tagName!=='H6'){if(!s.classList.contains('off'))v=true;s=s.nextElementSibling}h.style.display=v?'':'none'})}
sel('amba1');
