// toc.js — auto-generate TOC from article headings
document.addEventListener('DOMContentLoaded', function () {
  var article = document.querySelector('article');
  var tocContainer = document.querySelector('.toc');
  if (!article || !tocContainer) return;

  var headings = article.querySelectorAll('h1, h2, h3');
  if (headings.length < 3) {
    tocContainer.style.display = 'none';
    return;
  }

  var tocNav = document.createElement('nav');
  tocNav.className = 'toc-nav';
  tocNav.setAttribute('aria-label', 'Table of contents');

  var tocTitle = document.createElement('span');
  tocTitle.className = 'toc-title';
  tocTitle.textContent = 'Contents';
  tocNav.appendChild(tocTitle);

  var tocList = document.createElement('ul');
  tocList.className = 'toc-list';

  var idx = 0;
  headings.forEach(function (h, i) {
    // Skip the very first H1 (post title in header)
    if (i === 0 && h.tagName === 'H1' && h.closest('header')) return;

    if (!h.id) h.id = 'section-' + (idx++);

    var li = document.createElement('li');
    li.className = 'toc-item toc-' + h.tagName.toLowerCase();

    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.className = 'toc-link';
    a.textContent = h.textContent;

    a.addEventListener('click', function (e) {
      e.preventDefault();
      var target = document.getElementById(h.id);
      if (target) {
        var top = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: top, behavior: 'smooth' });
        history.pushState(null, '', '#' + h.id);
      }
    });

    li.appendChild(a);
    tocList.appendChild(li);
  });

  tocNav.appendChild(tocList);
  tocContainer.appendChild(tocNav);

  // Intersection observer for active highlight
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        tocList.querySelectorAll('.toc-link').forEach(function (l) { l.classList.remove('active'); });
        var active = tocList.querySelector('a[href="#' + entry.target.id + '"]');
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });

  headings.forEach(function (h, i) {
    if (i === 0 && h.tagName === 'H1' && h.closest('header')) return;
    observer.observe(h);
  });

  // Handle initial hash
  if (window.location.hash) {
    var target = document.querySelector(window.location.hash);
    if (target) {
      setTimeout(function () {
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
      }, 120);
    }
  }
});
