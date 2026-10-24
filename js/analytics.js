/* Casa Rosebery — consenso cookie + Google Analytics per le pagine secondarie (menu, vini).
   Stessa chiave di consenso della home ('cr_cookie_consenso'): chi ha già scelto in home non rivede il banner.
   Analytics si carica SOLO dopo il consenso. */
(function () {
  var GA = 'G-60070819GQ';
  var CHIAVE = 'cr_cookie_consenso';
  var DURATA = 1000 * 60 * 60 * 24 * 180; // 6 mesi
  var en = (document.documentElement.lang || '').indexOf('en') === 0;
  var T = en ? {
    testo: 'We use technical cookies required for the site to work and, only with your consent, Google Analytics cookies to understand how the site is used. You can change your mind at any time from "Cookie preferences" at the bottom of the page.',
    info: 'More information', rifiuta: 'Decline', accetta: 'Accept', chiudi: 'Close and decline', pref: 'Cookie preferences'
  } : {
    testo: 'Usiamo cookie tecnici necessari al funzionamento del sito e, solo con il tuo consenso, cookie analitici di Google Analytics per capire come viene visitato. Puoi cambiare idea in qualsiasi momento da "Preferenze cookie" in fondo alla pagina.',
    info: 'Maggiori informazioni', rifiuta: 'Rifiuta', accetta: 'Accetta', chiudi: 'Chiudi e rifiuta', pref: 'Preferenze cookie'
  };

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { dataLayer.push(arguments); };
  function caricaAnalytics() {
    if (window.__gaCaricato) return;
    window.__gaCaricato = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA, { anonymize_ip: true });
  }
  function leggi() {
    try { var d = JSON.parse(localStorage.getItem(CHIAVE)); if (d && d.t && Date.now() - d.t < DURATA) return d.v; } catch (e) {}
    return null;
  }
  function salva(v) { try { localStorage.setItem(CHIAVE, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {} }

  // ── banner ──
  var css = '#cookie-banner{display:none;position:fixed;z-index:300;left:12px;right:12px;bottom:calc(16px + env(safe-area-inset-bottom,0px));' +
    'background:#141210;color:rgba(255,255,255,.8);border:1px solid rgba(184,146,58,.35);box-shadow:0 12px 40px rgba(0,0,0,.45);' +
    'padding:22px 20px 18px;font:400 13px/1.6 Jost,system-ui,sans-serif}#cookie-banner.visibile{display:block}' +
    '#cookie-banner p{margin:0 28px 16px 0}#cookie-banner a{color:#d4b06a;text-decoration:underline}' +
    '#cookie-banner .cb-azioni{display:flex;gap:10px}#cookie-banner .cb-btn{flex:1;padding:12px 16px;cursor:pointer;' +
    'font:500 12px/1 Jost,system-ui,sans-serif;letter-spacing:2px;text-transform:uppercase;background:transparent;color:#d4b06a;border:1px solid #b8923a}' +
    '#cookie-banner .cb-btn:hover{background:#b8923a;color:#000}#cookie-banner .cb-chiudi{position:absolute;top:10px;right:12px;background:none;border:0;' +
    'cursor:pointer;color:rgba(255,255,255,.5);font-size:20px;line-height:1;padding:4px}' +
    '@media(min-width:1025px){#cookie-banner{left:28px;right:auto;bottom:28px;max-width:420px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function monta() {
    var b = document.createElement('div');
    b.id = 'cookie-banner'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-live', 'polite');
    b.setAttribute('aria-label', T.pref);
    b.innerHTML = '<button type="button" class="cb-chiudi" aria-label="' + T.chiudi + '">&times;</button>' +
      '<p>' + T.testo + ' <a href="/privacy.html#cookie">' + T.info + '</a></p>' +
      '<div class="cb-azioni"><button type="button" class="cb-btn" data-scelta="rifiutato">' + T.rifiuta + '</button>' +
      '<button type="button" class="cb-btn" data-scelta="accettato">' + T.accetta + '</button></div>';
    document.body.appendChild(b);
    function scegli(v) {
      var prima = leggi(); salva(v); b.classList.remove('visibile');
      if (v === 'accettato') caricaAnalytics(); else if (prima === 'accettato') location.reload();
    }
    b.querySelectorAll('[data-scelta]').forEach(function (x) { x.addEventListener('click', function () { scegli(x.getAttribute('data-scelta')); }); });
    b.querySelector('.cb-chiudi').addEventListener('click', function () { scegli('rifiutato'); });
    // link "Preferenze cookie" nel footer
    var f = document.querySelector('footer');
    if (f) {
      var a = document.createElement('a'); a.href = '#'; a.textContent = T.pref; a.style.cssText = 'color:inherit;text-decoration:underline';
      a.addEventListener('click', function (e) { e.preventDefault(); b.classList.add('visibile'); });
      f.appendChild(document.createTextNode(' · ')); f.appendChild(a);
    }
    var stato = leggi();
    if (stato === 'accettato') caricaAnalytics(); else if (stato === null) b.classList.add('visibile');
  }

  // ── tracciamento clic (stessi nomi evento della home) ──
  function traccia(ev, p) { if (window.__gaCaricato) gtag('event', ev, p || {}); }
  var pagina = /vini/.test(location.pathname) ? 'pagina_vini' : /serata/.test(location.pathname) ? 'pagina_serata' : 'pagina_menu';
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var h = a.getAttribute('href');
    if (h.indexOf('plateform.app') !== -1) traccia('click_prenota', { posizione: pagina });
    else if (h.indexOf('tel:') === 0) traccia('click_telefono', { posizione: pagina });
    else if (h.indexOf('wa.me') !== -1) traccia('click_whatsapp', { motivo: 'generico', posizione: pagina });
    else if (h.indexOf('vini.html') !== -1) traccia('click_vini', { da: pagina });
    else if (h.indexOf('menu.html') !== -1) traccia('click_menu', { da: pagina });
  }, true);

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', monta); else monta();
})();
