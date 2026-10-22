"""Genera menu.html (italiano) e en/menu.html (inglese) a partire da menu-src/menu.json.

Uso (dalla cartella del repo):  python3 menu-src/genera_menu.py
Per aggiornare il menu: modificare menu.json e rilanciare lo script.
Inglese: campi con suffisso _en (titolo_en, sotto_en, nota_en, desc_en, nome_en). Se mancano,
la pagina inglese mostra il testo italiano (i nomi dei piatti possono restare in italiano).
"""
import html
import json
import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
dati = json.loads((RADICE / "menu-src" / "menu.json").read_text(encoding="utf-8"))
_vs = RADICE / "menu-src" / "vista_serata.json"
vista = json.loads(_vs.read_text(encoding="utf-8")) if _vs.exists() else {}


def vista_serata_html():
    """Vista limitata per una serata (solo pagina italiana): nascosta di default, la attiva lo script nelle date indicate."""
    if not vista.get("date"):
        return ""
    m = vista["menu"]
    voce = lambda n, d, pr="": (f'<li class="piatto"><div class="riga"><h4>{e(n)}</h4><span class="punti"></span>'
                                + (f'<span class="prezzo">{e(pr)}</span>' if pr else "") + f'</div><p class="desc">{e(d)}</p></li>')
    integ = m.get("integrazione")
    perc = (f'<article class="percorso"><header><h3>{e(m["titolo"])}</h3><p class="pp">€ {e(m["prezzo"])} <span>{e(m["nota"])}</span></p></header>'
            f'<div class="portata"><ul>{"".join(voce(n, d) for n, d in m["piatti"])}</ul></div>'
            + (f'<div class="portata"><h5>{e(integ[0])}</h5><ul>{voce(integ[1], integ[2])}</ul></div>' if integ else "")
            + '</article>')
    sez = "".join(f'<section class="sez"><h2>{e(x["titolo"])}</h2><ul class="lista">{"".join(voce(*v) for v in x["voci"])}</ul></section>'
                  for x in vista.get("sezioni", []))
    return (f'<section id="vista-serata" data-mostra-il="{",".join(vista["date"])}" hidden>'
            f'<section class="sez"><h2>{e(vista.get("titolo", "Menu della serata"))}</h2><div class="percorsi">{perc}</div></section>{sez}</section>')
e = html.escape
SITO = "https://www.casaroseberyristorante.it"

TESTI = {
    "it": {"lang": "it", "file": RADICE / "menu.html", "rad": "", "home": "/", "link": "/en/menu.html", "link_lang": "en", "link_txt": "EN",
           "degu_nav": "Degustazione", "degu_tit": "Percorsi degustazione", "pp": "a persona · minimo 2 persone",
           "escl": "Bevande escluse", "etto": " · prezzo all'etto", "all_title": "Allergeni",
           "title": "Menu — Casa Rosebery · Braceria & Ristorante a Posillipo, Napoli",
           "descr": "Il menu di Casa Rosebery a Posillipo: percorsi degustazione, cruderia, carni pregiate alla brace (Wagyu A5, Tomahawk, Black Angus), primi della tradizione napoletana e dolci.",
           "eyebrow": "Braceria &amp; Ristorante · Posillipo", "h1": "Il nostro <em>menu</em>", "agg": "Aggiornato a",
           "nav_aria": "Sezioni del menu", "all_h": "Allergeni e intolleranze",
           "all_1": ("I numeri accanto ai piatti indicano gli allergeni presenti secondo il Regolamento UE n. 1169/2011. "
                     "Per qualsiasi allergia o intolleranza chiedi al nostro personale prima di ordinare."),
           "all_0": ("Alcuni piatti possono contenere allergeni (Regolamento UE n. 1169/2011). "
                     "Prima di ordinare, comunica al nostro personale qualsiasi allergia o intolleranza: "
                     "ti indicheremo con precisione gli ingredienti di ogni piatto."),
           "prenota": "Prenota un tavolo", "vini": "Carta dei vini", "vini_url": "vini.html", "pdf": "Scarica il menu in PDF",
           "privacy": "Privacy e Cookie Policy"},
    "en": {"lang": "en", "file": RADICE / "en" / "menu.html", "rad": "/", "home": "/en/", "link": "/menu.html", "link_lang": "it", "link_txt": "IT",
           "degu_nav": "Tasting menus", "degu_tit": "Tasting menus", "pp": "per person · minimum 2 people",
           "escl": "Drinks not included", "etto": " · price per 100 g", "all_title": "Allergens",
           "title": "Menu — Casa Rosebery · Steakhouse & Restaurant in Posillipo, Naples",
           "descr": "The Casa Rosebery menu in Posillipo, Naples: tasting menus, raw bar, prime grilled steaks (A5 Wagyu, Tomahawk, Black Angus), traditional Neapolitan pasta and desserts.",
           "eyebrow": "Steakhouse &amp; Restaurant · Posillipo", "h1": "Our <em>menu</em>", "agg": "Updated",
           "nav_aria": "Menu sections", "all_h": "Allergies and intolerances",
           "all_1": ("The numbers next to each dish indicate the allergens present under EU Regulation No 1169/2011. "
                     "If you have any allergy or intolerance, please ask our staff before ordering."),
           "all_0": ("Some dishes may contain allergens (EU Regulation No 1169/2011). "
                     "Before ordering, please tell our staff about any allergy or intolerance: "
                     "we will tell you exactly what goes into each dish."),
           "prenota": "Book a table", "vini": "Wine list", "vini_url": "vini.html", "pdf": "Download the menu (PDF, Italian)",
           "privacy": "Privacy &amp; Cookie Policy (Italian)"},
}


def tr(obj, campo, lingua):
    if lingua != "it" and obj.get(f"{campo}_{lingua}"):
        return obj[f"{campo}_{lingua}"]
    return obj.get(campo, "")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def allergeni(p, L):
    # numeri nascosti finché la cucina non verifica gli allergeni (vedi menu.json: mostra_allergeni)
    if not dati.get("mostra_allergeni", True) or not p.get("all"):
        return ""
    return f' <span class="all" title="{L["all_title"]}">{e(p["all"].replace(",", " · "))}</span>'


def piatto(p, L, unita=""):
    lg = L["lang"]
    prezzo = f'<span class="prezzo">€ {e(p["prezzo"])}{e(unita)}</span>' if p.get("prezzo") else ""
    desc = f'<p class="desc">{e(tr(p, "desc", lg))}</p>' if p.get("desc") else ""
    return (f'<li class="piatto"><div class="riga"><h4>{e(tr(p, "nome", lg))}{allergeni(p, L)}</h4>'
            f'<span class="punti"></span>{prezzo}</div>{desc}</li>')


def contenuto(L):
    lg = L["lang"]
    nav, corpo = [], []
    # Percorsi degustazione
    nav.append(f'<a href="#degustazione">{L["degu_nav"]}</a>')
    schede = []
    for pc in dati["percorsi"]:
        portate = "".join(
            f'<div class="portata"><h5>{e(tr(pt, "titolo", lg))}'
            + (f' <small>({e(tr(pt, "nota", lg))})</small>' if pt.get("nota") else "")
            + "</h5><ul>" + "".join(piatto(p, L) for p in pt["piatti"]) + "</ul></div>"
            for pt in pc["portate"])
        nasc = f' data-nascondi-il="{",".join(pc["nascondi_il"])}"' if pc.get("nascondi_il") else ""
        schede.append(f'<article class="percorso"{nasc}><header><h3>{e(pc["nome"])}</h3>'
                      f'<p class="pp">€ {e(pc["prezzo"])} <span>{L["pp"]}</span></p></header>'
                      f'{portate}<p class="escl">{L["escl"]}</p></article>')
    corpo.append(f'<section id="degustazione" class="sez"><h2>{L["degu_tit"]}</h2>'
                 f'<div class="percorsi">{"".join(schede)}</div></section>')
    # Sezioni alla carta (gli id restano quelli italiani, così i link funzionano in entrambe le lingue)
    visti = set()
    for s in dati["sezioni"]:
        sid = slug(s["titolo"] + (" " + s["sotto"] if s.get("sotto") else ""))
        if s["titolo"] not in visti:
            nav.append(f'<a href="#{sid}">{e(tr(s, "titolo", lg))}</a>')
            visti.add(s["titolo"])
        sotto = f'<p class="sotto">{e(tr(s, "sotto", lg))}{L["etto"]}</p>' if s.get("sotto") else ""
        unita = s.get("unita", "")
        if lg == "en" and unita.strip() == "/etto":
            unita = " / 100 g"
        voci = "".join(piatto(p, L, unita) for p in s["piatti"])
        corpo.append(f'<section id="{sid}" class="sez"><h2>{e(tr(s, "titolo", lg))}</h2>{sotto}<ul class="lista">{voci}</ul></section>')
    return nav, corpo


def pagina(L):
    nav, corpo = contenuto(L)
    TESTO_ALLERGENI = L["all_1"] if dati.get("mostra_allergeni", True) else L["all_0"]
    LINK_PDF = (f'  <a class="btn" href="{L["rad"]}menu-casa-rosebery.pdf" target="_blank">{L["pdf"]}</a>\n'
                if dati.get("mostra_pdf", False) else "")
    rad = L["rad"]
    agg = dati.get("aggiornato_en", dati["aggiornato"]) if L["lang"] == "en" else dati["aggiornato"]
    canon = f'{SITO}/menu.html' if L["lang"] == "it" else f'{SITO}/en/menu.html'
    return f'''<!DOCTYPE html>
<html lang="{L["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{L["title"]}</title>
<meta name="description" content="{L["descr"]}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="it" href="{SITO}/menu.html">
<link rel="alternate" hreflang="en" href="{SITO}/en/menu.html">
<link rel="alternate" hreflang="x-default" href="{SITO}/menu.html">
<link rel="icon" href="{rad}favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{rad}favicon-512.png">
<link rel="apple-touch-icon" href="{rad}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {{ --nero:#0e0d0a; --carbone:#1a1814; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#8a8070; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; scroll-padding-top:120px; }}
body {{ font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.6; }}
a {{ color:inherit; text-decoration:none; }}
.top {{ background:var(--nero); color:#fff; text-align:center; padding:28px 20px 34px; }}
.top .lang {{ position:absolute; right:20px; top:24px; font-size:10px; letter-spacing:2px; color:rgba(255,255,255,.6); }}
.top .back {{ position:absolute; left:20px; top:24px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.5); }}
.top img {{ width:min(70vw,300px); height:auto; margin:0 auto 14px; display:block; }}
.top .eyebrow {{ font-size:10px; letter-spacing:4px; text-transform:uppercase; color:var(--oro); }}
.top h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(40px,8vw,64px); line-height:1.1; margin-top:6px; }}
.top h1 em {{ color:var(--oro-lt); }}
.top .agg {{ font-size:11px; color:rgba(255,255,255,.4); margin-top:10px; letter-spacing:1px; }}
nav.cat {{ position:sticky; top:0; z-index:10; background:rgba(14,13,10,.97); backdrop-filter:blur(12px); border-top:1px solid rgba(184,146,58,.2); border-bottom:1px solid rgba(184,146,58,.2);
  display:flex; gap:6px; overflow-x:auto; padding:12px 16px; scrollbar-width:none; }}
nav.cat::-webkit-scrollbar {{ display:none; }}
nav.cat a {{ flex:none; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.65); padding:8px 14px; border:1px solid rgba(184,146,58,.25); }}
nav.cat a:hover, nav.cat a.att {{ color:var(--nero); background:var(--oro); border-color:var(--oro); }}
main {{ max-width:860px; margin:0 auto; padding:16px 20px 60px; }}
.sez {{ padding-top:48px; }}
.sez h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:36px; text-align:center; }}
.sez h2::after {{ content:''; display:block; width:40px; height:1px; background:var(--oro); margin:14px auto 0; }}
.sotto {{ text-align:center; font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--oro); margin-top:12px; }}
.lista, .portata ul {{ list-style:none; margin-top:26px; }}
.piatto {{ padding:16px 0; border-bottom:1px solid var(--sabbia); }}
.riga {{ display:flex; align-items:baseline; gap:10px; }}
.riga h4 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:21px; line-height:1.25; }}
.punti {{ flex:1; border-bottom:1px dotted #c9bfa9; transform:translateY(-5px); min-width:16px; }}
.prezzo {{ font-size:14px; font-weight:500; white-space:nowrap; color:var(--text); }}
.all {{ font-family:'Inter',sans-serif; font-size:10px; font-weight:400; color:var(--oro); letter-spacing:1px; vertical-align:middle; margin-left:4px; }}
.desc {{ font-size:13.5px; color:#5d5446; margin-top:4px; max-width:640px; }}
.percorsi {{ display:grid; gap:20px; margin-top:28px; }}
.percorso {{ background:var(--nero); color:#fff; padding:28px 24px; border:1px solid rgba(184,146,58,.35); }}
.percorso header {{ text-align:center; margin-bottom:8px; }}
.percorso h3 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-style:italic; font-size:30px; color:var(--oro-lt); }}
.pp {{ font-size:20px; margin-top:4px; }}
.pp span {{ display:block; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.45); }}
.portata h5 {{ font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--oro); margin-top:22px; font-weight:500; }}
.portata h5 small {{ letter-spacing:0; text-transform:none; color:rgba(255,255,255,.45); font-size:11px; }}
.portata ul {{ margin-top:6px; }}
.percorso .piatto {{ border-color:rgba(255,255,255,.08); padding:10px 0; }}
.percorso .riga h4 {{ font-size:19px; }}
.percorso .desc {{ color:rgba(255,255,255,.55); font-size:13px; }}
.percorso .punti {{ display:none; }}
.escl {{ text-align:center; font-size:11px; color:rgba(255,255,255,.4); margin-top:18px; font-style:italic; }}
.info {{ margin-top:56px; background:#fff; border:1px solid var(--sabbia); padding:24px; font-size:13px; color:#5d5446; }}
.info h3 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:22px; color:var(--text); margin-bottom:8px; }}
.azioni {{ display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin-top:36px; }}
.btn {{ font-size:10px; letter-spacing:2px; text-transform:uppercase; padding:15px 26px; border:1px solid var(--oro); color:var(--text); font-weight:500; }}
.btn.pieno {{ background:var(--oro); color:var(--nero); }}
footer {{ background:var(--nero); color:rgba(255,255,255,.35); text-align:center; font-size:11px; padding:28px 20px; }}
footer a {{ text-decoration:underline; }}
@media (min-width:760px) {{ .percorsi {{ grid-template-columns:1fr; }} .percorso {{ padding:36px 48px; }} }}
</style>
</head>
<body>
<header class="top" style="position:relative">
  <a class="back" href="{L["home"]}">← Home</a>
  <a class="lang" href="{L["link"]}" hreflang="{L["link_lang"]}" lang="{L["link_lang"]}">{L["link_txt"]}</a>
  <a href="{L["home"]}"><img src="{rad}logo-chiaro.png" alt="Casa Rosebery"></a>
  <span class="eyebrow">{L["eyebrow"]}</span>
  <h1>{L["h1"]}</h1>
  <p class="agg">{L["agg"]} {e(agg)}</p>
</header>
<nav class="cat" aria-label="{L["nav_aria"]}">{"".join(nav)}</nav>
<main>
{vista_serata_html() if L["lang"] == "it" else ""}
{"".join(corpo)}
<section class="info" id="allergeni">
  <h3>{L["all_h"]}</h3>
  <p>{TESTO_ALLERGENI}</p>
</section>
<div class="azioni">
  <a class="btn pieno" href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener">{L["prenota"]}</a>
  <a class="btn" href="{L["vini_url"]}">{L["vini"]}</a>
{LINK_PDF}</div>
</main>
<footer>© 2026 Casa Rosebery · Nado Advertising S.r.l. · P.IVA 07284940488 · <a href="{rad}privacy.html">{L["privacy"]}</a></footer>
<script>
(function () {{
  var links = document.querySelectorAll('nav.cat a');
  var mappa = {{}};
  links.forEach(function (a) {{ mappa[a.getAttribute('href').slice(1)] = a; }});
  var obs = new IntersectionObserver(function (voci) {{
    voci.forEach(function (v) {{
      if (!v.isIntersecting) return;
      var id = v.target.id, a = mappa[id];
      if (!a) {{ var t = v.target.querySelector('h2'); if (!t) return;
        links.forEach(function (l) {{ if (l.textContent === t.textContent) a = l; }}); }}
      if (!a) return;
      links.forEach(function (l) {{ l.classList.remove('att'); }});
      a.classList.add('att');
      var nav = a.parentNode; // scorre solo la barra, senza interrompere lo scroll della pagina
      nav.scrollTo({{ left: a.offsetLeft - nav.clientWidth / 2 + a.clientWidth / 2, behavior: 'smooth' }});
    }});
  }}, {{ rootMargin: '-130px 0px -70% 0px' }});
  document.querySelectorAll('.sez').forEach(function (s) {{ obs.observe(s); }});
}})();
</script>
<script>
// Vista limitata della serata: nelle date indicate mostra solo #vista-serata (fino alle 4 del mattino dopo)
(function () {{
  var v = document.getElementById('vista-serata'); if (!v) return;
  var d = new Date(Date.now() - 4 * 3600 * 1000);
  var oggi = new Intl.DateTimeFormat('en-CA', {{ timeZone: 'Europe/Rome' }}).format(d);
  if (v.getAttribute('data-mostra-il').split(',').indexOf(oggi) < 0) return;
  v.hidden = false;
  document.querySelectorAll('nav.cat, main > .sez, main > .info, .azioni a[href*="vini"], .top .lang, .top .agg').forEach(function (el) {{ el.style.display = 'none'; }});
}})();
// Nasconde gli elementi con data-nascondi-il="AAAA-MM-GG" in quella data (ora di Roma; la serata vale fino alle 4 del mattino dopo)
(function () {{
  var d = new Date(Date.now() - 4 * 3600 * 1000);
  var oggi = new Intl.DateTimeFormat('en-CA', {{ timeZone: 'Europe/Rome' }}).format(d);
  document.querySelectorAll('[data-nascondi-il]').forEach(function (el) {{
    if (el.getAttribute('data-nascondi-il').split(',').indexOf(oggi) >= 0) el.style.display = 'none';
  }});
}})();
</script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''

for L in TESTI.values():
    L["file"].parent.mkdir(exist_ok=True)
    L["file"].write_text(pagina(L), encoding="utf-8")
    print(f'{L["file"].relative_to(RADICE)} generato')
