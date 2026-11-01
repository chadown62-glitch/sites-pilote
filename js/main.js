/* Menu mobile + formulaire de démonstration. Aucune requête réseau, aucun stockage. */
(function () {
  document.documentElement.classList.add('js');
  var btn = document.querySelector('.menu-btn');
  var list = document.getElementById('menu');
  if (btn && list) {
    btn.addEventListener('click', function () {
      var open = list.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && list.classList.contains('open')) {
        list.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }
  var form = document.getElementById('demo-form');
  if (form) {
    form.addEventListener('submit', function (e) { e.preventDefault(); });
  }
})();

