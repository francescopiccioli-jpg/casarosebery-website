"""Genera vini.html a partire da vini-src/vini.json.

Uso (dalla cartella del repo):  python3 vini-src/genera_vini.py
Per aggiornare la carta: modificare vini.json e rilanciare lo script.
Campi di ogni vino: sez (bollicine | rossi | bianchi | bianchi-estero | rosati), nome, produttore, regione, prezzo.
"""
import html
import json
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
dati = json.loads((RADICE / "vini-src" / "vini.json").read_text(encoding="utf-8"))
e = html.escape

# ordine delle sezioni; "bianchi-estero" confluisce nei Bianchi (dopo le regioni italiane)
SEZIONI = [("bollicine", "Bollicine"), ("rossi", "Rossi"), ("bianchi", "Bianchi"), ("rosati", "Rosati")]
UNISCI = {"bianchi-estero": "bianchi"}


def ordina_regioni(vini):
    ordine = []
    for v in vini:
        if v["regione"] not in ordine:
            ordine.append(v["regione"])
    if "Campania" in ordine:  # il territorio prima di tutto
        ordine.remove("Campania")
        ordine.insert(0, "Campania")
    return ordine


nav, corpo = [], []
for sid, titolo in SEZIONI:
    vini = [v for v in dati["vini"] if UNISCI.get(v["sez"], v["sez"]) == sid]
    if not vini:
        continue
    nav.append(f'<a href="#{sid}">{e(titolo)}</a>')
    blocchi = []
    for reg in ordina_regioni(vini):
        righe = "".join(
            f'<li class="vino" data-cerca="{e((v["nome"] + " " + v["produttore"] + " " + reg).lower())}">'
            f'<div class="riga"><h4>{e(v["nome"])}</h4><span class="punti"></span>'
            f'<span class="prezzo">€ {e(v["prezzo"])}</span></div>'
            + (f'<p class="prod">{e(v["produttore"])}</p>' if v["produttore"] else "")
            + '</li>'
            for v in vini if v["regione"] == reg)
        blocchi.append(f'<div class="regione"><h3>{e(reg)}</h3><ul>{righe}</ul></div>')
    corpo.append(f'<section id="{sid}" class="sez"><h2>{e(titolo)}</h2>'
                 f'<p class="conta">{len(vini)} etichette</p>{"".join(blocchi)}</section>')

totale = len(dati["vini"])
pagina = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carta dei vini — Casa Rosebery · Posillipo, Napoli</title>
<meta name="description" content="La carta dei vini di Casa Rosebery a Posillipo: {totale} etichette tra Champagne e Franciacorta, i grandi rossi di Campania, Toscana, Piemonte e Veneto, bianchi vulcanici e rosati.">
<link rel="canonical" href="https://www.casaroseberyristorante.it/vini.html">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="favicon-512.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {{ --nero:#0e0d0a; --carbone:#1a1814; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#8a8070; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; scroll-padding-top:130px; }}
body {{ font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.6; }}
a {{ color:inherit; text-decoration:none; }}
.top {{ position:relative; background:var(--nero); color:#fff; text-align:center; padding:28px 20px 34px; }}
.top .back {{ position:absolute; left:20px; top:24px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.5); }}
.top img {{ width:min(70vw,300px); height:auto; margin:0 auto 14px; display:block; }}
.top .eyebrow {{ font-size:10px; letter-spacing:4px; text-transform:uppercase; color:var(--oro); }}
.top h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(40px,8vw,64px); line-height:1.1; margin-top:6px; }}
.top h1 em {{ color:var(--oro-lt); }}
.top .agg {{ font-size:11px; color:rgba(255,255,255,.4); margin-top:10px; letter-spacing:1px; }}
.barra {{ position:sticky; top:0; z-index:10; background:rgba(14,13,10,.97); backdrop-filter:blur(12px); border-top:1px solid rgba(184,146,58,.2); border-bottom:1px solid rgba(184,146,58,.2); }}
nav.cat {{ display:flex; gap:6px; overflow-x:auto; padding:12px 16px 8px; scrollbar-width:none; }}
nav.cat::-webkit-scrollbar {{ display:none; }}
nav.cat a {{ flex:none; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.65); padding:8px 14px; border:1px solid rgba(184,146,58,.25); }}
nav.cat a:hover, nav.cat a.att {{ color:var(--nero); background:var(--oro); border-color:var(--oro); }}
.cerca {{ padding:0 16px 12px; }}
.cerca input {{ width:100%; max-width:520px; display:block; margin:0 auto; background:transparent; border:0; border-bottom:1px solid rgba(184,146,58,.4);
  color:#fff; font:300 14px 'Inter',sans-serif; padding:8px 2px; outline:none; }}
.cerca input::placeholder {{ color:rgba(255,255,255,.4); }}
main {{ max-width:860px; margin:0 auto; padding:16px 20px 60px; }}
.sez {{ padding-top:48px; }}
.sez h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:38px; text-align:center; }}
.sez h2::after {{ content:''; display:block; width:40px; height:1px; background:var(--oro); margin:14px auto 0; }}
.conta {{ text-align:center; font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--muted); margin-top:10px; }}
.regione h3 {{ font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--oro); font-weight:500; margin:34px 0 6px; }}
.regione ul {{ list-style:none; }}
.vino {{ padding:12px 0; border-bottom:1px solid var(--sabbia); }}
.riga {{ display:flex; align-items:baseline; gap:10px; }}
.riga h4 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:19px; line-height:1.25; }}
.punti {{ flex:1; border-bottom:1px dotted #c9bfa9; transform:translateY(-5px); min-width:16px; }}
.prezzo {{ font-size:14px; font-weight:500; white-space:nowrap; }}
.prod {{ font-size:12.5px; color:#6d6455; margin-top:1px; }}
.vuoto {{ display:none; text-align:center; color:var(--muted); padding:60px 0; }}
.nota {{ margin-top:56px; background:#fff; border:1px solid var(--sabbia); padding:22px 24px; font-size:13px; color:#5d5446; }}
.azioni {{ display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin-top:36px; }}
.btn {{ font-size:10px; letter-spacing:2px; text-transform:uppercase; padding:15px 26px; border:1px solid var(--oro); color:var(--text); font-weight:500; }}
.btn.pieno {{ background:var(--oro); color:var(--nero); }}
footer {{ background:var(--nero); color:rgba(255,255,255,.35); text-align:center; font-size:11px; padding:28px 20px; }}
footer a {{ text-decoration:underline; }}
</style>
</head>
<body>
<header class="top">
  <a class="back" href="/">← Home</a>
  <a href="/"><img src="logo-chiaro.png" alt="Casa Rosebery"></a>
  <span class="eyebrow">Braceria &amp; Ristorante · Posillipo</span>
  <h1>Carta dei <em>vini</em></h1>
  <p class="agg">{totale} etichette · aggiornata a {e(dati["aggiornato"])}</p>
</header>
<div class="barra">
  <nav class="cat" aria-label="Tipologie">{"".join(nav)}</nav>
  <div class="cerca"><input type="search" id="cerca" placeholder="Cerca un vino, un produttore o una regione…" aria-label="Cerca nella carta dei vini"></div>
</div>
<main>
{"".join(corpo)}
<p class="vuoto" id="vuoto">Nessun vino trovato. Chiedi al nostro personale: la cantina riserva sempre qualche sorpresa.</p>
<p class="nota">Prezzi a bottiglia. Annate e disponibilità possono variare: il nostro personale di sala ti consiglia l'abbinamento migliore con i tagli alla brace.</p>
<div class="azioni">
  <a class="btn pieno" href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener">Prenota un tavolo</a>
  <a class="btn" href="menu.html">Sfoglia il menu</a>
</div>
</main>
<footer>© 2026 Casa Rosebery · Nado Advertising S.r.l. · P.IVA 07284940488 · <a href="privacy.html">Privacy e Cookie Policy</a></footer>
<script>
(function () {{
  // ricerca
  var campo = document.getElementById('cerca'), vuoto = document.getElementById('vuoto');
  campo.addEventListener('input', function () {{
    var q = campo.value.trim().toLowerCase(), trovati = 0;
    document.querySelectorAll('.vino').forEach(function (v) {{
      var ok = !q || v.getAttribute('data-cerca').indexOf(q) !== -1;
      v.style.display = ok ? '' : 'none'; if (ok) trovati++;
    }});
    document.querySelectorAll('.regione').forEach(function (r) {{
      r.style.display = r.querySelector('.vino:not([style*="none"])') ? '' : 'none';
    }});
    document.querySelectorAll('.sez').forEach(function (s) {{
      s.style.display = s.querySelector('.regione:not([style*="none"])') ? '' : 'none';
    }});
    vuoto.style.display = trovati ? 'none' : 'block';
  }});
  // categoria attiva nella barra
  var links = document.querySelectorAll('nav.cat a');
  var obs = new IntersectionObserver(function (voci) {{
    voci.forEach(function (v) {{
      if (!v.isIntersecting) return;
      links.forEach(function (l) {{
        var on = l.getAttribute('href') === '#' + v.target.id;
        l.classList.toggle('att', on);
        if (on) l.parentNode.scrollTo({{ left: l.offsetLeft - l.parentNode.clientWidth / 2 + l.clientWidth / 2, behavior: 'smooth' }});
      }});
    }});
  }}, {{ rootMargin: '-140px 0px -70% 0px' }});
  document.querySelectorAll('.sez').forEach(function (s) {{ obs.observe(s); }});
}})();
</script>
</body>
</html>
'''
(RADICE / "vini.html").write_text(pagina, encoding="utf-8")
print(f"vini.html generato: {totale} vini")
