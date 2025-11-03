// Persistencia simple del contador en localStorage
const grid = document.getElementById('grid');
const btnAdd = document.getElementById('btnAdd');
const btnClear = document.getElementById('btnClear');
const countSpan = document.getElementById('count');

function getCount(){ return Number(localStorage.getItem('count') || 0); }
function setCount(n){ localStorage.setItem('count', String(n)); countSpan.textContent = 'Tarjetas: ' + n; }

function addCard(i){
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `<h3>Tarjeta #${i}</h3><p>Generada dinámicamente.</p>`;
  grid.appendChild(card);
}

function renderFromCount(){
  grid.innerHTML = '';
  const n = getCount();
  for(let i=1;i<=n;i++) addCard(i);
  setCount(n);
}

btnAdd.addEventListener('click', ()=>{
  const n = getCount() + 1;
  setCount(n);
  addCard(n);
});

btnClear.addEventListener('click', ()=>{
  setCount(0);
  grid.innerHTML = '';
});

renderFromCount();

// Cursor con teclas + colisión simple
const cursor = document.getElementById('cursor');
const playArea = document.getElementById('playArea');
let cx=8, cy=8, step=8;

document.addEventListener('keydown', (e)=>{
  const r = playArea.getBoundingClientRect();
  if(e.key==='ArrowRight') cx = Math.min(cx+step, r.width-24);
  if(e.key==='ArrowLeft')  cx = Math.max(cx-step, 0);
  if(e.key==='ArrowDown')  cy = Math.min(cy+step, r.height-24);
  if(e.key==='ArrowUp')    cy = Math.max(cy-step, 0);
  cursor.style.left = cx+'px';
  cursor.style.top  = cy+'px';
  document.querySelectorAll('.block').forEach(b=>{
    const br = b.getBoundingClientRect();
    const cr = cursor.getBoundingClientRect();
    const hit = !(cr.right < br.left || cr.left > br.right || cr.bottom < br.top || cr.top > br.bottom);
    b.classList.toggle('highlight', hit);
  });
});
