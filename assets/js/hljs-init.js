document.addEventListener('DOMContentLoaded', function () {
  var langNames = {
    bash:'bash', sh:'shell', zsh:'zsh',
    python:'python', py:'python',
    javascript:'javascript', js:'javascript',
    typescript:'typescript', ts:'typescript',
    cpp:'c++', c:'c', java:'java',
    kotlin:'kotlin', kt:'kotlin',
    rust:'rust', go:'go',
    html:'html', css:'css',
    json:'json', yaml:'yaml', yml:'yaml',
    xml:'xml', sql:'sql',
    makefile:'makefile', nix:'nix',
    plaintext:'text', text:'text',
  };

  document.querySelectorAll('code[class*="language-"]').forEach(function (b) {
    var m = b.className.match(/language-(\S+)/);
    if (m) b.classList.add(m[1]);
  });

  hljs.highlightAll();
  if (typeof hljs.initLineNumbersOnLoad === 'function') hljs.initLineNumbersOnLoad();

  document.querySelectorAll('pre').forEach(function (pre) {
    var code = pre.querySelector('code');
    if (!code) return;

    if (!pre.hasAttribute('data-filename')) {
      var lang = '';
      var m = code.className.match(/language-(\S+)/);
      if (m) lang = m[1];
      if (!lang) {
        code.className.split(/\s+/).some(function (c) {
          if (c && c !== 'hljs' && !c.startsWith('hljs-')) { lang = c; return true; }
        });
      }
      if (lang) {
        var bar = document.createElement('div');
        bar.className = 'code-tab-bar';
        var tab = document.createElement('span');
        tab.className = 'code-tab';
        tab.textContent = langNames[lang] || lang;
        bar.appendChild(tab);
        pre.insertBefore(bar, pre.firstChild);
      }
    }

    if (pre.querySelector('.code-copy-btn')) return;
    var btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.title = 'Copy code';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 19a2 2 0 0 1-1-2V2a2 2 0 0 1 1-1h13a2 2 0 0 1 2 1"/><rect x="6" y="5" width="16" height="18" rx="1.5"/></svg>';
    btn.addEventListener('click', function () {
      var text = '';
      var cells = code.querySelectorAll('.hljs-ln-code');
      if (cells.length) { cells.forEach(function (c) { text += c.textContent + '\n'; }); text = text.replace(/\n$/, ''); }
      else text = code.textContent;
      navigator.clipboard.writeText(text).then(function () {
        btn.classList.add('copied');
        btn.innerHTML = '<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>';
        setTimeout(function () {
          btn.classList.remove('copied');
          btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 19a2 2 0 0 1-1-2V2a2 2 0 0 1 1-1h13a2 2 0 0 1 2 1"/><rect x="6" y="5" width="16" height="18" rx="1.5"/></svg>';
        }, 2000);
      });
    });
    pre.appendChild(btn);
  });
});
