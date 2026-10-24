"""Genera vini.html (italiano) e en/vini.html (inglese) a partire da vini-src/vini.json.

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


SITO = "https://www.casaroseberyristorante.it"
TESTI = {
    "it": {"lang": "it", "file": RADICE / "vini.html", "rad": "", "home": "/", "link": "/en/vini.html", "link_lang": "en", "link_txt": "EN",
           "sez": dict(SEZIONI), "regioni": {}, "etichette": "etichette",
           "title": "Carta dei vini — Casa Rosebery · Posillipo, Napoli",
           "descr": "La carta dei vini di Casa Rosebery a Posillipo: {n} etichette tra Champagne e Franciacorta, i grandi rossi di Campania, Toscana, Piemonte e Veneto, bianchi vulcanici e rosati.",
           "eyebrow": "Braceria &amp; Ristorante · Posillipo", "h1": "Carta dei <em>vini</em>", "agg": "{n} etichette · aggiornata a {d}",
           "tip": "Tipologie", "cerca": "Cerca un vino, un produttore o una regione…", "cerca_aria": "Cerca nella carta dei vini",
           "vuoto": "Nessun vino trovato. Chiedi al nostro personale: la cantina riserva sempre qualche sorpresa.",
           "nota": "Prezzi a bottiglia. Annate e disponibilità possono variare: il nostro personale di sala ti consiglia l'abbinamento migliore con i tagli alla brace.",
           "prenota": "Prenota un tavolo", "menu": "Sfoglia il menu", "privacy": "Privacy e Cookie Policy"},
    "en": {"lang": "en", "file": RADICE / "en" / "vini.html", "rad": "/", "home": "/en/", "link": "/vini.html", "link_lang": "it", "link_txt": "IT",
           "sez": {"bollicine": "Sparkling", "rossi": "Reds", "bianchi": "Whites", "rosati": "Rosés"},
           "regioni": {"Francia": "France", "Germania": "Germany", "Lombardia": "Lombardy", "Piemonte": "Piedmont",
                       "Sardegna": "Sardinia", "Sicilia": "Sicily", "Toscana": "Tuscany", "Puglia": "Apulia"},
           "etichette": "labels",
           "title": "Wine List — Casa Rosebery · Posillipo, Naples",
           "descr": "The Casa Rosebery wine list in Posillipo, Naples: {n} labels including Champagne and Franciacorta, great reds from Campania, Tuscany, Piedmont and Veneto, volcanic whites and rosés.",
           "eyebrow": "Steakhouse &amp; Restaurant · Posillipo", "h1": "Wine <em>list</em>", "agg": "{n} labels · updated {d}",
           "tip": "Wine types", "cerca": "Search for a wine, producer or region…", "cerca_aria": "Search the wine list",
           "vuoto": "No wines found. Ask our staff: the cellar always has a few surprises in store.",
           "nota": "Prices are per bottle. Vintages and availability may vary: our dining room staff will suggest the best pairing for your grilled cuts.",
           "prenota": "Book a table", "menu": "Browse the menu", "privacy": "Privacy &amp; Cookie Policy (Italian)"},
}


def contenuto(L):
    nav, corpo = [], []
    for sid, _ in SEZIONI:
        titolo = L["sez"][sid]
        vini = [v for v in dati["vini"] if UNISCI.get(v["sez"], v["sez"]) == sid]
        if not vini:
            continue
        nav.append(f'<a href="#{sid}">{e(titolo)}</a>')
        blocchi = []
        for reg in ordina_regioni(vini):
            nome_reg = L["regioni"].get(reg, reg)
            cerca_reg = reg + (" " + nome_reg if nome_reg != reg else "")
            righe = "".join(
                f'<li class="vino" data-cerca="{e((v["nome"] + " " + v["produttore"] + " " + cerca_reg).lower())}">'
                f'<div class="riga"><h4>{e(v["nome"])}</h4><span class="punti"></span>'
                f'<span class="prezzo">€ {e(v["prezzo"])}</span></div>'
                + (f'<p class="prod">{e(v["produttore"])}</p>' if v["produttore"] else "")
                + '</li>'
                for v in vini if v["regione"] == reg)
            blocchi.append(f'<div class="regione"><h3>{e(nome_reg)}</h3><ul>{righe}</ul></div>')
        corpo.append(f'<section id="{sid}" class="sez"><h2>{e(titolo)}</h2>'
                     f'<p class="conta">{len(vini)} {L["etichette"]}</p>{"".join(blocchi)}</section>')
    return nav, corpo


totale = len(dati["vini"])
MESI_EN = {"Gennaio": "January", "Febbraio": "February", "Marzo": "March", "Aprile": "April", "Maggio": "May", "Giugno": "June",
           "Luglio": "July", "Agosto": "August", "Settembre": "September", "Ottobre": "October", "Novembre": "November", "Dicembre": "December"}


def pagina(L):
    nav, corpo = contenuto(L)
    rad = L["rad"]
    agg = dati["aggiornato"]
    if L["lang"] == "en":
        m, _, a = agg.partition(" ")
        agg = f"{MESI_EN.get(m.capitalize(), m)} {a}".strip()
    canon = f'{SITO}/vini.html' if L["lang"] == "it" else f'{SITO}/en/vini.html'
    return f'''<!DOCTYPE html>
<html lang="{L["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{L["title"]}</title>
<meta name="description" content="{L["descr"].format(n=totale)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="it" href="{SITO}/vini.html">
<link rel="alternate" hreflang="en" href="{SITO}/en/vini.html">
<link rel="alternate" hreflang="x-default" href="{SITO}/vini.html">
<link rel="icon" href="{rad}favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{rad}favicon-512.png">
<link rel="apple-touch-icon" href="{rad}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {{ --nero:#0e0d0a; --carbone:#1a1814; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#8a8070; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; scroll-padding-top:130px; }}
body {{ font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.6; }}
a {{ color:inherit; text-decoration:none; }}
.top {{ position:relative; background:var(--nero); color:#fff; text-align:center; padding:28px 20px 34px; }}
.top .lang {{ position:absolute; right:20px; top:24px; font-size:11px; letter-spacing:2px; color:rgba(255,255,255,0.72); }}
.top .back {{ position:absolute; left:20px; top:24px; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.72); }}
.top img {{ width:min(70vw,300px); height:auto; margin:0 auto 14px; display:block; }}
.top .eyebrow {{ font-size:11px; letter-spacing:4px; text-transform:uppercase; color:var(--oro); }}
.top h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(40px,8vw,64px); line-height:1.1; margin-top:6px; }}
.top h1 em {{ color:var(--oro-lt); }}
.top .agg {{ font-size:11px; color:rgba(255,255,255,0.65); margin-top:10px; letter-spacing:1px; }}
.barra {{ position:sticky; top:0; z-index:10; background:rgba(14,13,10,.97); backdrop-filter:blur(12px); border-top:1px solid rgba(184,146,58,.2); border-bottom:1px solid rgba(184,146,58,.2); }}
nav.cat {{ display:flex; gap:6px; overflow-x:auto; padding:12px 16px 8px; scrollbar-width:none; }}
nav.cat::-webkit-scrollbar {{ display:none; }}
nav.cat a {{ flex:none; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.65); padding:8px 14px; border:1px solid rgba(184,146,58,.25); }}
nav.cat a:hover, nav.cat a.att {{ color:var(--nero); background:var(--oro); border-color:var(--oro); }}
.cerca {{ padding:0 16px 12px; }}
.cerca input {{ width:100%; max-width:520px; display:block; margin:0 auto; background:transparent; border:0; border-bottom:1px solid rgba(184,146,58,.4);
  color:#fff; font:300 14px 'Inter',sans-serif; padding:8px 2px; outline:none; }}
.cerca input::placeholder {{ color:rgba(255,255,255,0.65); }}
main {{ max-width:860px; margin:0 auto; padding:16px 20px 60px; }}
.sez {{ padding-top:48px; }}
.sez h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:38px; text-align:center; }}
.sez h2::after {{ content:''; display:block; width:40px; height:1px; background:var(--oro); margin:14px auto 0; }}
.conta {{ text-align:center; font-size:11px; letter-spacing:3px; text-transform:uppercase; color:var(--muted); margin-top:10px; }}
.regione h3 {{ font-size:11px; letter-spacing:3px; text-transform:uppercase; color:var(--oro); font-weight:500; margin:34px 0 6px; }}
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
.btn {{ font-size:11px; letter-spacing:2px; text-transform:uppercase; padding:15px 26px; border:1px solid var(--oro); color:var(--text); font-weight:500; }}
.btn.pieno {{ background:var(--oro); color:var(--nero); }}
footer {{ background:var(--nero); color:rgba(255,255,255,0.65); text-align:center; font-size:11px; padding:28px 20px; }}
footer a {{ text-decoration:underline; }}
</style>
</head>
<body>
<header class="top">
  <a class="back" href="{L["home"]}">← Home</a>
  <a class="lang" href="{L["link"]}" hreflang="{L["link_lang"]}" lang="{L["link_lang"]}">{L["link_txt"]}</a>
  <a href="{L["home"]}"><img src="{rad}logo-chiaro.png" alt="Casa Rosebery"></a>
  <span class="eyebrow">{L["eyebrow"]}</span>
  <h1>{L["h1"]}</h1>
  <p class="agg">{L["agg"].format(n=totale, d=e(agg))}</p>
</header>
<div class="barra">
  <nav class="cat" aria-label="{L["tip"]}">{"".join(nav)}</nav>
  <div class="cerca"><input type="search" id="cerca" placeholder="{L["cerca"]}" aria-label="{L["cerca_aria"]}"></div>
</div>
<main>
{"".join(corpo)}
<p class="vuoto" id="vuoto">{L["vuoto"]}</p>
<p class="nota">{L["nota"]}</p>
<div class="azioni">
  <a class="btn pieno" href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener">{L["prenota"]}</a>
  <a class="btn" href="menu.html">{L["menu"]}</a>
</div>
</main>
<footer>© 2026 Casa Rosebery · Nado Advertising S.r.l. · P.IVA 07284940488 · <a href="{rad}privacy.html">{L["privacy"]}</a></footer>
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
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''
for L in TESTI.values():
    L["file"].parent.mkdir(exist_ok=True)
    L["file"].write_text(pagina(L), encoding="utf-8")
    print(f'{L["file"].relative_to(RADICE)} generato: {totale} vini')
