window.montarHidrovia=function(host){var R=host.attachShadow({mode:"open"});R.innerHTML={{INTERIOR}};
(function(){
var D={{D}};var lst=R.getElementById?R.getElementById('lst'):R.querySelector('#lst');
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
D.forEach(function(t){var b=document.createElement('button');b.className='it';b.setAttribute('data-t',t.id);
b.innerHTML='<h5><b style="background:'+t.c+'"></b>'+esc(t.nombre)+'</h5><div class="km">'+esc(t.km)+'</div><dl class="det"><dt>Hoy</dt><dd>'+esc(t.hoy)+'</dd><dt>Contrato vigente</dt><dd>'+esc(t.contrato)+'</dd><dt>Propuesta</dt><dd class="p">'+esc(t.prop)+'</dd><dt>Quién lo usa</dt><dd>'+esc(t.uso)+'</dd></dl>';
b.addEventListener('click',function(){sel(t.id===cur?null:t.id)});lst.appendChild(b)});
var cur=null;function sel(id){cur=id;R.querySelectorAll('.it').forEach(function(e){e.classList.toggle('on',e.getAttribute('data-t')===id)});
R.querySelectorAll('.tr').forEach(function(e){e.classList.toggle('sel',e.getAttribute('data-t')===id)})}
R.querySelectorAll('.tr-hit').forEach(function(e){e.addEventListener('click',function(){var id=e.getAttribute('data-t');sel(id);var b=R.querySelector('.it[data-t="'+id+'"]');if(b&&window.innerWidth<820)b.scrollIntoView({block:'nearest',behavior:'smooth'})})});
sel('gr');

})()};