// Global utilities for CyberAI web pages (no module system required)
(function(){
  function escapeHtml(s){
    return String(s)
      .replace(/&/g,'&amp;')
      .replace(/</g,'&lt;')
      .replace(/>/g,'&gt;');
  }

  function formatResponse(text){
    if(!text) return '';
    const re=/```(\w+)?\n([\s\S]*?)```/g; 
    let html=''; let last=0; let m;
    while((m=re.exec(text))){
      const before=text.slice(last,m.index);
      html+=escapeHtml(before).replace(/\n/g,'<br>');
      const lang=m[1]||''; const code=m[2];
      html+=`<pre class="bg-black/60 p-3 rounded overflow-x-auto"><code class="language-${lang}">${escapeHtml(code)}</code></pre>`;
      last=re.lastIndex;
    }
    html+=escapeHtml(text.slice(last)).replace(/\n/g,'<br>');
    return html;
  }

  async function detectApiBase(){
    if (window.API_BASE) return window.API_BASE;
    const candidates = [];
    if (location.origin.startsWith('http')) {
      candidates.push('/api');
      candidates.push(`${location.protocol}//${location.hostname}:8000`);
      candidates.push('http://127.0.0.1:8000');
    } else {
      candidates.push('http://localhost:8000');
      candidates.push('http://127.0.0.1:8000');
    }
    for (const base of candidates){
      try{
        const r = await fetch(`${base}/techniques`, { method: 'GET' });
        if (r.ok){ window.API_BASE = base; break; }
      }catch(_){ /* try next */ }
    }
    if (!window.API_BASE) window.API_BASE = 'http://localhost:8000';
    return window.API_BASE;
  }

  function applyHighlight(){
    try { if (window.hljs && typeof window.hljs.highlightAll === 'function') window.hljs.highlightAll(); } catch(_){ }
  }

  // expose to global
  window.escapeHtml = escapeHtml;
  window.formatResponse = formatResponse;
  window.detectApiBase = detectApiBase;
  window.applyHighlight = applyHighlight;
})();
