const labels={draft:'Черновик',review:'На проверке',published:'Опубликовано'};
let payload={articles:[],media:[]}, selected=null;
const esc=v=>String(v??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

function renderList(){
  const filter=document.querySelector('#filter').value;
  const items=payload.articles.filter(a=>filter==='all'||a.status===filter);
  document.querySelector('#article-list').innerHTML=items.map(a=>`<button class="queue-item ${selected?.id===a.id?'active':''}" data-id="${esc(a.id)}"><strong>${esc(a.title_ru)}</strong><span class="meta"><span>${labels[a.status]}</span><span>${esc(a.updated_at)}</span></span></button>`).join('')||'<p class="empty">Нет материалов.</p>';
  document.querySelectorAll('.queue-item').forEach(el=>el.onclick=()=>selectArticle(el.dataset.id));
}

function articlePreview(a){
  const media=payload.media.filter(m=>a.media_ids.includes(m.id));
  return `<h1>${esc(a.title_ru)}</h1><p class="subtitle">${esc(a.subtitle_ru)}</p><p class="summary">${esc(a.summary_ru)}</p>${a.sections.map(s=>`<section><h3>${esc(s.heading_ru)}</h3>${s.paragraphs_ru.map(p=>`<p>${esc(p)}</p>`).join('')}</section>`).join('')}<div class="source"><b>Источник:</b> <a href="${esc(a.source.revision_url)}" target="_blank" rel="noopener">${esc(a.source.title)}</a> · ${esc(a.source.license)}<br>${esc(a.source.adaptation_notice_ru)}</div>${media.map(m=>`<div class="media-card ${m.verification_status==='verified'?'':'warning'}">Фото: ${esc(m.caption_ru)}<br>Проверка: ${esc(m.verification_status)}</div>`).join('')}`;
}

function selectArticle(id){
  selected=payload.articles.find(a=>a.id===id);
  renderList();
  const root=document.querySelector('#workspace');
  root.innerHTML=''; root.append(document.querySelector('#editor-template').content.cloneNode(true));
  root.querySelector('[data-field="title"]').textContent=selected.title_ru;
  root.querySelector('[data-field="badge"]').textContent=labels[selected.status];
  root.querySelector('[data-input="status"]').value=selected.status;
  root.querySelector('[data-input="editorial"]').checked=selected.review.editorial_approved;
  root.querySelector('[data-input="license"]').checked=selected.review.license_approved;
  root.querySelector('[data-field="preview"]').innerHTML=articlePreview(selected);
  root.querySelector('[data-input="status"]').onchange=event=>root.querySelector('[data-field="badge"]').textContent=labels[event.target.value];
  root.querySelector('[data-action="preview"]').onclick=()=>root.querySelector('[data-field="preview"]').scrollIntoView({behavior:'smooth'});
  root.querySelector('[data-action="download"]').onclick=download;
}

function download(){
  const root=document.querySelector('#workspace');
  const status=root.querySelector('[data-input="status"]').value;
  const editorial=root.querySelector('[data-input="editorial"]').checked;
  const license=root.querySelector('[data-input="license"]').checked;
  if(status==='published'&&(!editorial||!license)){alert('Для публикации нужны оба одобрения.');return;}
  const media=payload.media.filter(m=>selected.media_ids.includes(m.id));
  if(status==='published'&&media.some(m=>m.verification_status!=='verified')){alert('В статье есть непроверенное изображение.');return;}
  const result=structuredClone(selected); result.status=status; result.review.editorial_approved=editorial; result.review.license_approved=license; result.updated_at=new Date().toISOString().slice(0,10);
  const blob=new Blob([JSON.stringify(result,null,2)+'\n'],{type:'application/json'}), url=URL.createObjectURL(blob), link=document.createElement('a');
  link.href=url; link.download=`${result.id}.json`; link.click(); URL.revokeObjectURL(url);
}

fetch('../data/generated/articles-admin.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(data=>{payload=data;renderList();if(data.articles[0])selectArticle(data.articles[0].id)}).catch(()=>document.querySelector('#article-list').innerHTML='<p class="warning">Не удалось загрузить данные. Сначала запустите сборку статей.</p>');
document.querySelector('#filter').onchange=renderList;
