function setupSections(){
  const nav=document.getElementById('categories');
  const cards=document.getElementById('cards');
  if(!nav||!cards)return;
  const buttons=['Todos','Curso IA 2026','Día 2 · De idea a primera versión','Métodos y agentes','Prompts','Casos prácticos'];
  const descriptions={
    'Todos':'Toda la biblioteca, organizada para consulta rápida',
    'Curso IA 2026':'Conceptos y fundamentos del curso',
    'Día 2 · De idea a primera versión':'Construcción de aplicaciones, agentes, Sites, conectores y creación audiovisual',
    'Métodos y agentes':'Goal Engineering, instrucciones, agentes, skills y autonomía',
    'Prompts':'Prompts reutilizables listos para copiar y adaptar',
    'Casos prácticos':'Ejemplos de aplicación y demostraciones'
  };
  nav.innerHTML=buttons.map((x,i)=>`<button class="${i===0?'active':''}" data-section="${x}">${x}</button>`).join('');
  const matches=(section,card)=>{
    const badge=card.querySelector('.badge')?.textContent?.trim()||'';
    const title=card.querySelector('h3')?.textContent?.toLowerCase()||'';
    const tags=card.querySelector('.tags')?.textContent?.toLowerCase()||'';
    const isCase=title.includes('caso práctico')||title.includes('casos prácticos')||title.includes('excel a informe')||tags.includes('casos prácticos');
    if(section==='Todos')return true;
    if(section==='Curso IA 2026')return badge==='Curso'&&!isCase;
    if(section==='Día 2 · De idea a primera versión')return badge.startsWith('Curso · Día 2');
    if(section==='Métodos y agentes')return /goal|agente|agent|skill|instruccion|autonomía|autonomia|shit in/.test((title+' '+tags).normalize('NFD').replace(/[\u0300-\u036f]/g,''));
    if(section==='Prompts')return badge==='Prompt'&&!isCase;
    if(section==='Casos prácticos')return isCase;
    return false;
  };
  const apply=(section)=>{
    let visible=0;
    cards.querySelectorAll('.card').forEach(card=>{
      const show=matches(section,card);
      card.style.display=show?'':'none';
      if(show)visible++;
    });
    nav.querySelectorAll('[data-section]').forEach(b=>b.classList.toggle('active',b.dataset.section===section));
    const heading=document.getElementById('heading');
    const sub=document.getElementById('subheading');
    const count=document.getElementById('count');
    if(heading)heading.textContent=section;
    if(sub)sub.textContent=descriptions[section];
    if(count)count.textContent=visible;
  };
  nav.querySelectorAll('[data-section]').forEach(b=>b.onclick=()=>apply(b.dataset.section));
  apply('Todos');
}
window.addEventListener('load',()=>setTimeout(setupSections,300));