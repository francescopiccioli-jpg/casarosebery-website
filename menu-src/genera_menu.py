"""Genera menu.html a partire da menu-src/menu.json.

Uso (dalla cartella del repo):  python3 menu-src/genera_menu.py
Per aggiornare il menu: modificare menu.json e rilanciare lo script.
"""
import html
import json
import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
dati = json.loads((RADICE / "menu-src" / "menu.json").read_text(encoding="utf-8"))
e = html.escape


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def allergeni(p):
    if not p.get("all"):
        return ""
    return f' <span class="all" title="Allergeni">{e(p["all"].replace(",", " · "))}</span>'


def piatto(p, unita=""):
    prezzo = f'<span class="prezzo">€ {e(p["prezzo"])}{e(unita)}</span>' if p.get("prezzo") else ""
    desc = f'<p class="desc">{e(p["desc"])}</p>' if p.get("desc") else ""
    return (f'<li class="piatto"><div class="riga"><h4>{e(p["nome"])}{allergeni(p)}</h4>'
            f'<span class="punti"></span>{prezzo}</div>{desc}</li>')


nav, corpo = [], []

# Percorsi degustazione
nav.append('<a href="#degustazione">Degustazione</a>')
schede = []
for pc in dati["percorsi"]:
    portate = "".join(
        f'<div class="portata"><h5>{e(pt["titolo"])}'
        + (f' <small>({e(pt["nota"])})</small>' if pt.get("nota") else "")
        + "</h5><ul>" + "".join(piatto(p) for p in pt["piatti"]) + "</ul></div>"
        for pt in pc["portate"])
    schede.append(f'<article class="percorso"><header><h3>{e(pc["nome"])}</h3>'
                  f'<p class="pp">€ {e(pc["prezzo"])} <span>a persona · minimo 2 persone</span></p></header>'
                  f'{portate}<p class="escl">Bevande escluse</p></article>')
corpo.append('<section id="degustazione" class="sez"><h2>Percorsi degustazione</h2>'
             f'<div class="percorsi">{"".join(schede)}</div></section>')

# Sezioni alla carta
visti = set()
for s in dati["sezioni"]:
    sid = slug(s["titolo"] + (" " + s["sotto"] if s.get("sotto") else ""))
    if s["titolo"] not in visti:
        nav.append(f'<a href="#{sid}">{e(s["titolo"])}</a>')
        visti.add(s["titolo"])
    sotto = f'<p class="sotto">{e(s["sotto"])} · prezzo all\'etto</p>' if s.get("sotto") else ""
    voci = "".join(piatto(p, s.get("unita", "")) for p in s["piatti"])
    corpo.append(f'<section id="{sid}" class="sez"><h2>{e(s["titolo"])}</h2>{sotto}<ul class="lista">{voci}</ul></section>')

pagina = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Menu — Casa Rosebery · Braceria & Ristorante a Posillipo, Napoli</title>
<meta name="description" content="Il menu di Casa Rosebery a Posillipo: percorsi degustazione, cruderia, carni pregiate alla brace (Wagyu A5, Tomahawk, Black Angus), primi della tradizione napoletana e dolci.">
<link rel="canonical" href="https://www.casaroseberyristorante.it/menu.html">
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {{ --nero:#0e0d0a; --carbone:#1a1814; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#8a8070; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; scroll-padding-top:120px; }}
body {{ font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.6; }}
a {{ color:inherit; text-decoration:none; }}
.top {{ background:var(--nero); color:#fff; text-align:center; padding:28px 20px 34px; }}
.top .back {{ position:absolute; left:20px; top:24px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.5); }}
.top img {{ height:56px; filter:brightness(0) invert(1); margin:0 auto 18px; display:block; }}
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
  <a class="back" href="/">← Home</a>
  <a href="/"><img src="logo.png" alt="Casa Rosebery"></a>
  <span class="eyebrow">Braceria &amp; Ristorante · Posillipo</span>
  <h1>Il nostro <em>menu</em></h1>
  <p class="agg">Aggiornato a {e(dati["aggiornato"])}</p>
</header>
<nav class="cat" aria-label="Sezioni del menu">{"".join(nav)}</nav>
<main>
{"".join(corpo)}
<section class="info" id="allergeni">
  <h3>Allergeni e intolleranze</h3>
  <p>I numeri accanto ai piatti indicano gli allergeni presenti, secondo il Regolamento UE n. 1169/2011. La legenda completa è disponibile in sala: per qualsiasi allergia o intolleranza chiedi al nostro personale prima di ordinare.</p>
</section>
<div class="azioni">
  <a class="btn pieno" href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener">Prenota un tavolo</a>
  <a class="btn" href="menu-casa-rosebery.pdf" target="_blank">Scarica il menu in PDF</a>
</div>
</main>
<footer>© 2026 Casa Rosebery · Nado Advertising S.r.l. · P.IVA 07284940488 · <a href="privacy.html">Privacy e Cookie Policy</a></footer>
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
</body>
</html>
'''

(RADICE / "menu.html").write_text(pagina, encoding="utf-8")
print("menu.html generato")
