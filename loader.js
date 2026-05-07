(function () {
  var placeholder = document.getElementById('nav-placeholder');
  if (!placeholder) return;

  fetch('nav.html')
    .then(function (r) {
      if (!r.ok) throw new Error('nav.html ' + r.status);
      return r.text();
    })
    .then(function (html) {
      placeholder.innerHTML = html;

      // Highlight the link that matches the current page filename
      var current = window.location.pathname.split('/').pop();
      if (!current || current === '') current = 'index.html';

      var links = placeholder.querySelectorAll('a[href]');
      links.forEach(function (a) {
        if (a.getAttribute('href') === current) {
          a.style.fontWeight = '600';
          a.style.color = '#fff';
          a.style.borderLeftColor = 'var(--accent)';
        }
      });
    })
    .catch(function (e) {
      console.warn('MPRC nav loader failed:', e);
    });
})();
