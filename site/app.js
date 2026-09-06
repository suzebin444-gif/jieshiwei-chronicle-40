const root = window.JIESHIWEI_DATA || {};
const chapters = root.chapters?.chapters || [];
const images = root.images?.images || [];
const eraFilter = document.querySelector('#eraFilter');
const search = document.querySelector('#search');
const timeline = document.querySelector('#timeline');
const gallery = document.querySelector('#gallery');
const candidateGallery = document.querySelector('#candidateGallery');

const approved = images.filter(x => x.review_status === 'approved');
const mapped = images.filter(x => Number.isInteger(x.chapter) && Number.isInteger(x.page));
document.querySelector('#metrics').innerHTML = [
  ['40','章时间线'],['434','页总规划'],[String(images.length),'张已归档'],[String(approved.length),'张已审核']
].map(([n,l]) => `<div class="metric"><b>${n}</b>${l}</div>`).join('');

[...new Set(chapters.map(c => c.era))].forEach(era => {
  const option = document.createElement('option'); option.value = era; option.textContent = era; eraFilter.append(option);
});

function escapeHtml(value){return String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function visibleChapters(){
  const q = search.value.trim().toLowerCase();
  return chapters.filter(c => (!eraFilter.value || c.era === eraFilter.value) && (!q || `${c.number} ${c.title} ${c.period} ${c.focus} ${c.era}`.toLowerCase().includes(q)));
}
function render(){
  const visible = visibleChapters();
  document.querySelector('#resultCount').textContent = `显示 ${visible.length} / 40 章`;
  timeline.innerHTML = visible.map(c => `<article class="chapter">
    <span class="chapter-number">${String(c.number).padStart(2,'0')}</span>
    <div class="period">${escapeHtml(c.period)}</div><h3>${escapeHtml(c.title)}</h3>
    <p>${escapeHtml(c.focus)}</p><div class="tags"><span class="tag">${c.pages}页</span><span class="tag">${escapeHtml(c.era)}</span><span class="tag">提示词：${c.prompt_status === 'complete' ? '完整' : '概要'}</span></div>
  </article>`).join('') || '<div class="empty">没有匹配的章节。</div>';
  const numbers = new Set(visible.map(c=>c.number));
  const selected = mapped.filter(x=>numbers.has(x.chapter) && x.review_status !== 'superseded').slice(0,120);
  gallery.innerHTML = selected.map(x => `<figure class="asset"><img loading="lazy" src="../${escapeHtml(x.file)}" alt="${escapeHtml(x.title || x.id)}"><figcaption><b>${escapeHtml(x.title || x.id)}</b><small>第${x.chapter}章 · 第${x.page}页 · ${escapeHtml(x.review_status)}</small></figcaption></figure>`).join('') || '<div class="empty">当前筛选范围没有已可靠对应章页的图片。</div>';
  const candidates = images.filter(x => x.review_status === 'needs_mapping');
  candidateGallery.innerHTML = candidates.slice(0,120).map(x => `<figure class="asset"><img loading="lazy" src="../${escapeHtml(x.file)}" alt="${escapeHtml(x.title || x.id)}"><figcaption><b>${escapeHtml(x.title || x.id)}</b><small>${escapeHtml(x.id)} · 待人工对应章页</small></figcaption></figure>`).join('') || '<div class="empty">没有待对应素材。</div>';
}
[eraFilter,search].forEach(el=>el.addEventListener('input',render));
document.querySelector('#reset').addEventListener('click',()=>{eraFilter.value='';search.value='';render();});
render();
