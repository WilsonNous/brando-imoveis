
/* Brando Imóveis / Nous - script.js */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.querySelector('#search-input');
  if (searchInput){
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase();
      document.querySelectorAll('[data-card]').forEach(card => {
        const text = card.getAttribute('data-search') || '';
        card.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }
  const toggle = document.querySelector('#brandinho-toggle');
  const box = document.querySelector('#brandinho-box');
  const messages = document.querySelector('#brandinho-messages');
  const input = document.querySelector('#brandinho-text');
  const sendBtn = document.querySelector('#brandinho-send');
  function appendMessage(text, who='bot'){
    const row = document.createElement('div');
    row.className = `brandinho-msg ${who}`;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }
  if (toggle){
    toggle.addEventListener('click', () => {
      box.style.display = (box.style.display === 'none' || !box.style.display) ? 'block' : 'none';
      if (box.style.display === 'block' && messages.childElementCount === 0){
        appendMessage('Olá! Eu sou o Brandinho 🤖. Posso te ajudar a encontrar um imóvel por bairro, tipo ou faixa de preço. Pergunte!');
      }
    });
  }
  async function talkBrandinho(userText){
    appendMessage(userText, 'user');
    try{
      const r = await fetch('/api/brandinho', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ q: userText })
      });
      const data = await r.json();
      appendMessage(data.answer || 'Estou aqui para ajudar!');
    }catch(e){
      appendMessage('Ops! Não consegui responder agora, tente novamente.');
    }
  }
  if (sendBtn && input){
    sendBtn.addEventListener('click', () => {
      const t = (input.value || '').trim();
      if (!t) return;
      input.value='';
      talkBrandinho(t);
    });
    input.addEventListener('keypress', (e)=>{
      if (e.key === 'Enter'){ sendBtn.click(); }
    });
  }
  document.querySelectorAll('[data-whats]').forEach(btn => {
    btn.addEventListener('click', () => {
      const txt = btn.getAttribute('data-whats');
      navigator.clipboard.writeText(txt).then(()=> toast('Mensagem copiada! Cole no WhatsApp.'));
    });
  });
  const toastEl = document.querySelector('.toast');
  function toast(msg){
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.style.display = 'block';
    setTimeout(()=> toastEl.style.display='none', 2500);
  }
  window.__toast = toast;
});
