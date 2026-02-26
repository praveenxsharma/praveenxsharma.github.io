document.addEventListener('DOMContentLoaded', function () {
  var article      = document.querySelector('article');
  var tocContainer = document.querySelector('.toc');
  if (!article || !tocContainer) return;

  var headings = article.querySelectorAll('h1, h2, h3');
  if (headings.length < 3) { tocContainer.style.display = 'none'; return; }

  var nav = document.createElement('nav');
  nav.className = 'toc-nav';
  nav.setAttribute('aria-label', 'Table of contents');

  var title = document.createElement('span');
  title.className = 'toc-title';
  title.textContent = 'Contents';
  nav.appendChild(title);

  var list = document.createElement('ul');
  list.className = 'toc-list';

  var idx = 0;
  headings.forEach(function (h, i) {
    if (i === 0 && h.tagName === 'H1' && h.closest('header')) return;
    if (!h.id) h.id = 'h-' + (idx++);

    var li = document.createElement('li');
    li.className = 'toc-item toc-' + h.tagName.toLowerCase();

    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.className = 'toc-link';
    a.textContent = h.textContent;
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var t = document.getElementById(h.id);
      if (t) { window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' }); history.pushState(null, '', '#' + h.id); }
    });

    li.appendChild(a);
    list.appendChild(li);
  });

  nav.appendChild(list);
  tocContainer.appendChild(nav);

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        list.querySelectorAll('.toc-link').forEach(function (l) { l.classList.remove('active'); });
        var a = list.querySelector('a[href="#' + e.target.id + '"]');
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });

  headings.forEach(function (h, i) {
    if (i === 0 && h.tagName === 'H1' && h.closest('header')) return;
    observer.observe(h);
  });

  if (window.location.hash) {
    var t = document.querySelector(window.location.hash);
    if (t) setTimeout(function () {
      window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
    }, 120);
  }
});
