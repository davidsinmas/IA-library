function setupSections(){
  const nav=document.getElementById('categories');
  const cards=document.getElementById('cards');
  if(!nav||!cards)return;
  const buttons=['Todos','Curso IA 2026','Prompts','Casos prácticos'];
  nav.innerHTML=buttons.map((x,i)=>`<button class="${i===0?'active':''}" data-section="${x}">${x}</button>`).join('');
  const apply=(section)=>{
    let visible=0;
    cards.querySelectorAll('.card').forEach(card=>{
      const badge=card.querySelector('.badge')?.textContent?.trim()||'';
      const title=card.querySelector('h3')?.textContent?.toLowerCase()||'';
      const isCase=title.includes('caso práctico')||title.includes('casos prácticos')||title.includes('excel a informe');
      const show=section==='Todos'||(section==='Curso IA 2026'&&badge==='Curso'&&!isCase)||(section==='Prompts'&&badge==='Prompt'&&!isCase)||(section==='Casos prácticos'&&isCase);
      card.style.display=show?'':'none';
      if(show)visible++;
    });
    nav.querySelectorAll('[data-section]').forEach(b=>b.classList.toggle('active',b.dataset.section===section));
    const heading=document.getElementById('heading');
    const sub=document.getElementById('subheading');
    const count=document.getElementById('count');
    if(heading)heading.textContent=section;
    if(sub)sub.textContent=section==='Todos'?'Biblioteca organizada por áreas de uso':section==='Curso IA 2026'?'Contenido del curso, ordenado para consulta rápida':section==='Prompts'?'Prompts reutilizables listos para copiar y adaptar':'Ejemplos y casos de aplicación';
    if(count)count.textContent=visible;
  };
  nav.querySelectorAll('[data-section]').forEach(b=>b.onclick=()=>apply(b.dataset.section));
  apply('Todos');
}
window.addEventListener('load',()=>setTimeout(setupSections,300));