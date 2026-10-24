#!/usr/bin/env python3
"""Genera serata.html: la pagina a cui punta il QR code delle serate evento.
Durante la serata mostra SOLO il menu della serata (fisso o carta dedicata), senza link al menu alla carta.
Mostra il menu della serata di oggi (fino alle 4 del mattino dopo), preso da serata-src/serate.json.
Rilanciare dopo ogni modifica:  python3 serata-src/genera_serata.py"""
import json
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
dati = json.loads((RADICE / "serata-src" / "serate.json").read_text(encoding="utf-8"))
serate = json.dumps(dati["serate"], ensure_ascii=False).replace("</", "<\\/")

HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Menu della serata — Casa Rosebery</title>
<meta name="description" content="Il menu della serata evento di stasera a Casa Rosebery, Posillipo.">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root { --nero:#0e0d0a; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#5d5446; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.6; }
a { color:inherit; }
.top { background:var(--nero); color:#fff; text-align:center; padding:26px 20px 30px; }
.top img { height:64px; width:auto; }
.top .eyebrow { display:block; color:var(--oro-lt); font-size:10px; letter-spacing:4px; text-transform:uppercase; margin-top:14px; }
.top h1 { font-family:'Cormorant Garamond',serif; font-weight:400; font-size:34px; margin-top:6px; }
main { max-width:720px; margin:0 auto; padding:0 18px 60px; }
.sez { padding-top:42px; }
.sez h2 { font-family:'Cormorant Garamond',serif; font-weight:400; font-size:32px; text-align:center; }
.sez h2::after { content:''; display:block; width:40px; height:1px; background:var(--oro); margin:12px auto 0; }
.percorso { background:var(--nero); color:#fff; padding:28px 22px; margin-top:24px; border:1px solid rgba(184,146,58,.35); }
.percorso h3 { font-family:'Cormorant Garamond',serif; font-weight:400; font-style:italic; font-size:30px; color:var(--oro-lt); text-align:center; }
.pp { text-align:center; font-size:20px; margin-top:4px; }
.pp span { display:block; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.55); margin-top:4px; }
.percorso ul, .lista { list-style:none; margin-top:18px; }
.piatto { padding:14px 0; border-bottom:1px solid var(--sabbia); }
.percorso .piatto { border-color:rgba(255,255,255,.08); text-align:center; }
.riga { display:flex; align-items:baseline; gap:10px; }
.percorso .riga { justify-content:center; }
.riga h4 { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:20px; line-height:1.25; }
.punti { flex:1; border-bottom:1px dotted #c9bfa9; transform:translateY(-4px); }
.percorso .punti { display:none; }
.prezzo { font-size:14px; font-weight:500; white-space:nowrap; }
.desc { font-size:13.5px; color:var(--muted); margin-top:3px; }
.percorso .desc { color:rgba(255,255,255,.6); }
.integr { margin-top:18px; color:var(--oro-lt); font-size:11px; letter-spacing:2px; text-transform:uppercase; text-align:center; }
.vuota { text-align:center; padding:60px 10px; }
.vuota h2 { font-family:'Cormorant Garamond',serif; font-weight:400; font-size:30px; }
.vuota p { color:var(--muted); margin:14px 0 26px; }
.btn { display:inline-block; padding:13px 22px; font-size:11px; letter-spacing:2px; text-transform:uppercase; text-decoration:none; border:1px solid var(--oro); color:var(--text); margin:4px; }
.btn.pieno { background:var(--oro); color:var(--nero); }
.anteprima { background:#fff3c4; color:#5a4a00; text-align:center; font-size:12px; padding:8px; }
footer { text-align:center; font-size:11px; color:var(--muted); padding:30px 20px; }
</style>
</head>
<body>
<div id="anteprima" class="anteprima" hidden></div>
<header class="top">
  <img src="/logo-chiaro.png" alt="Casa Rosebery">
  <span class="eyebrow">Stasera a Casa Rosebery</span>
  <h1 id="titolo">Menu della serata</h1>
</header>
<main id="contenuto"></main>
<footer id="piede" hidden><a href="/menu.html">Menu alla carta</a> · <a href="/vini.html">Carta dei vini</a> · <a href="/">casaroseberyristorante.it</a></footer>
<script id="serate" type="application/json">__SERATE__</script>
<script>
(function () {
  var serate = JSON.parse(document.getElementById('serate').textContent);
  var e = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var q = new URLSearchParams(location.search).get('data');
  var oggi = q && /^\\d{4}-\\d{2}-\\d{2}$/.test(q) ? q
    : new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome' }).format(new Date(Date.now() - 4 * 3600 * 1000));
  if (q) { var a = document.getElementById('anteprima'); a.textContent = 'Anteprima della serata del ' + q.split('-').reverse().join('/'); a.hidden = false; }
  var s = serate.filter(function (x) { return x.data === oggi; })[0];
  var out = document.getElementById('contenuto');
  var voce = function (n, d, p) {
    return '<li class="piatto"><div class="riga"><h4>' + e(n) + '</h4><span class="punti"></span>' + (p ? '<span class="prezzo">' + e(p) + '</span>' : '') +
      '</div>' + (d ? '<p class="desc">' + e(d) + '</p>' : '') + '</li>';
  };
  if (!s) {
    document.getElementById('piede').hidden = false;
    out.innerHTML = '<div class="vuota"><h2>Stasera nessuna serata evento</h2><p>Il menu delle serate compare qui il giorno dell\\u2019evento.</p>' +
      '<a class="btn pieno" href="/menu.html">Menu alla carta</a><a class="btn" href="/#serate">Prossime serate</a></div>';
    return;
  }
  document.getElementById('titolo').textContent = s.titolo || 'Menu della serata';
  document.title = (s.titolo || 'Menu della serata') + ' — Casa Rosebery';
  var h = '';
  if (s.menu) {
    var m = s.menu;
    h += '<section class="sez"><div class="percorso"><h3>' + e(m.titolo || 'Menu della serata') + '</h3>' +
      (m.prezzo ? '<p class="pp">\\u20ac ' + e(m.prezzo) + (m.nota ? '<span>' + e(m.nota) + '</span>' : '') + '</p>' : '') +
      '<ul>' + (m.piatti || []).map(function (p) { return voce(p[0], p[1]); }).join('') + '</ul>' +
      (m.integrazione ? '<p class="integr">' + e(m.integrazione[0]) + '</p><ul>' + voce(m.integrazione[1], m.integrazione[2]) + '</ul>' : '') +
      '</div></section>';
  }
  (s.sezioni || []).forEach(function (x) {
    h += '<section class="sez"><h2>' + e(x.titolo) + '</h2><ul class="lista">' + x.voci.map(function (v) { return voce(v[0], v[1], v[2]); }).join('') + '</ul></section>';
  });
  out.innerHTML = h;
})();
</script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
"""

(RADICE / "serata.html").write_text(HTML.replace("__SERATE__", serate), encoding="utf-8")
print("serata.html generato:", len(dati["serate"]), "serate in archivio")
