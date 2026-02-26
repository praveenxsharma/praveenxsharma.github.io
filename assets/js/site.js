// site.js — nav fade + misc
(function () {
  function wireNavFade() {
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || href.startsWith('#') || /^https?:\/\//.test(href) || href.startsWith('mailto:')) return;
      if (a.getAttribute('aria-current') === 'page') return;

      a.addEventListener('click', function (e) {
        e.preventDefault();
        var target = href;
        document.body.classList.add('is-fading');
        setTimeout(function () {
          window.location.href = target;
        }, 160);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    wireNavFade();
  });

  // Remove fading class on pageshow (back/forward cache)
  window.addEventListener('pageshow', function () {
    document.body.classList.remove('is-fading');
  });
})();
