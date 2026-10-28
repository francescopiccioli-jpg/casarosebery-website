#!/usr/bin/env python3
"""Genera le pagine tematiche del sito, in italiano e in inglese:
  braceria.html            en/steakhouse.html          (tagli letti da menu-src/menu.json)
  serate.html              en/live-music.html          (serate lette da eventi-src/eventi.json)
  vista-mare-posillipo.html en/sea-view-restaurant-naples.html
Rilanciare dopo ogni modifica al menu o alle serate:  python3 pagine-src/genera_pagine.py"""
import datetime as dt
import json
import math
import urllib.parse
from html import escape as e
from pathlib import Path
from zoneinfo import ZoneInfo

RADICE = Path(__file__).resolve().parent.parent
SITO = "https://www.casaroseberyristorante.it"
PRENOTA = "https://casarosebery.plateform.app/reserve"
WA = "390813357572"
MAPPA = "https://www.google.com/maps/dir/?api=1&destination=" + urllib.parse.quote("Casa Rosebery, Via Ferdinando Russo 13, Napoli")
LAT, LON = 40.8132, 14.2018

MENU = json.loads((RADICE / "menu-src" / "menu.json").read_text(encoding="utf-8"))
EVENTI = json.loads((RADICE / "eventi-src" / "eventi.json").read_text(encoding="utf-8"))

COMUNE = {
    "it": {"lang": "it", "rad": "", "home": "/", "back": "← Home", "alt_txt": "English", "alt_lang": "en",
           "prenota": "Prenota un tavolo", "menu": "Menu completo", "vini": "Carta dei vini",
           "dove": "Dove siamo", "indirizzo": "Via Ferdinando Russo 13 · 80123 Posillipo, Napoli",
           "tel": "Telefono", "privacy": "Privacy e cookie", "menu_url": "/menu.html", "vini_url": "/vini.html",
           "altre": "Scopri anche", "eventi_url": "/eventi-privati.html"},
    "en": {"lang": "en", "rad": "/", "home": "/en/", "back": "← Home", "alt_txt": "Italiano", "alt_lang": "it",
           "prenota": "Book a table", "menu": "Full menu", "vini": "Wine list",
           "dove": "Find us", "indirizzo": "Via Ferdinando Russo 13 · 80123 Posillipo, Naples",
           "tel": "Phone", "privacy": "Privacy & cookies", "menu_url": "/en/menu.html", "vini_url": "/en/vini.html",
           "altre": "Discover more", "eventi_url": "/en/private-events.html"},
}

# nome della pagina in ogni lingua: (file IT, file EN, etichetta IT, etichetta EN)
PAGINE = {
    "braceria": ("braceria.html", "en/steakhouse.html", "La braceria", "The steakhouse"),
    "serate": ("serate.html", "en/live-music.html", "Serate con musica dal vivo", "Live music evenings"),
    "vista": ("vista-mare-posillipo.html", "en/sea-view-restaurant-naples.html", "Vista mare e come arrivare", "Sea view & getting here"),
    "eventi": ("eventi-privati.html", "en/private-events.html", "Eventi privati", "Private events"),
}


def url(chiave, lingua):
    return f"{SITO}/{PAGINE[chiave][0 if lingua == 'it' else 1]}"


def tr(o, k, lingua):
    return (o.get(k + "_en") or o.get(k, "")) if lingua == "en" else o.get(k, "")


CSS = """
:root { --nero:#0e0d0a; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#6f6656; }
* { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; }
body { font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.65; }
a { color:inherit; }
.top { position:relative; min-height:72vh; display:flex; flex-direction:column; justify-content:flex-end; color:#fff; padding:24px 20px 56px;
  background:linear-gradient(to bottom, rgba(14,13,10,.78) 0, rgba(14,13,10,.25) 28%, rgba(14,13,10,.55) 55%, rgba(14,13,10,.92) 100%), var(--hero) center/cover; }
.barra { position:absolute; top:0; left:0; right:0; display:flex; justify-content:space-between; align-items:center; padding:18px 20px; font-size:11px; letter-spacing:2px; text-transform:uppercase; }
.barra a { text-decoration:none; color:rgba(255,255,255,.85); }
.barra img { height:44px; width:auto; }
.eyebrow { color:var(--oro-lt); font-size:11px; letter-spacing:4px; text-transform:uppercase; }
.top h1 { font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(36px,7vw,62px); line-height:1.1; margin:10px 0 16px; max-width:820px; }
.top h1 em { color:var(--oro-lt); }
.top p { max-width:640px; color:rgba(255,255,255,.88); font-size:15px; }
.azioni { display:flex; gap:12px; flex-wrap:wrap; margin-top:26px; }
.btn { display:inline-block; padding:14px 24px; font-size:11px; letter-spacing:2.5px; text-transform:uppercase; text-decoration:none; border:1px solid var(--oro); color:var(--oro-lt); }
.btn.pieno { background:var(--oro); color:var(--nero); }
.chiaro .btn { color:var(--text); }
.chiaro .btn.pieno { color:var(--nero); }
.wrap { max-width:1040px; margin:0 auto; padding:0 20px; }
section { padding:68px 0 0; }
h2 { font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(30px,5vw,42px); text-align:center; }
h2::after { content:''; display:block; width:40px; height:1px; background:var(--oro); margin:14px auto 0; }
.lead { text-align:center; color:var(--muted); max-width:660px; margin:18px auto 0; font-size:14.5px; }
.testo { max-width:700px; margin:22px auto 0; font-size:15px; }
.testo p + p { margin-top:14px; }
h3.sotto { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:24px; margin:34px 0 4px; text-align:center; }
.tagli { list-style:none; margin-top:14px; display:grid; grid-template-columns:1fr; gap:0 40px; }
@media (min-width:860px) { .tagli { grid-template-columns:1fr 1fr; } }
.tagli li { padding:16px 0; border-bottom:1px solid var(--sabbia); }
.riga { display:flex; align-items:baseline; gap:10px; }
.riga h4 { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:20px; line-height:1.25; }
.punti { flex:1; border-bottom:1px dotted #c9bfa9; transform:translateY(-4px); min-width:12px; }
.prezzo { font-size:14px; font-weight:500; white-space:nowrap; }
.tagli p { font-size:13.5px; color:var(--muted); margin-top:3px; }
.nota { text-align:center; font-size:12px; color:var(--muted); margin-top:12px; }
.griglia { list-style:none; display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin-top:30px; }
.griglia li { background:#fff; border:1px solid var(--sabbia); border-top:2px solid var(--oro); padding:22px 20px; }
.griglia h3 { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:22px; margin-bottom:6px; }
.griglia p { font-size:13.5px; color:var(--muted); }
.scuro { background:var(--nero); color:#fff; padding:38px 24px; margin-top:30px; border:1px solid rgba(184,146,58,.35); }
.scuro ul { list-style:none; max-width:580px; margin:0 auto; }
.scuro li { text-align:center; padding:12px 0; border-bottom:1px solid rgba(255,255,255,.08); }
.scuro li:last-child { border:0; }
.scuro h4 { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:20px; }
.scuro p { color:rgba(255,255,255,.62); font-size:13px; }
.scuro .pp { text-align:center; font-family:'Cormorant Garamond',serif; font-size:40px; color:var(--oro-lt); line-height:1; }
.scuro .pp span { display:block; font-family:'Inter',sans-serif; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.55); margin-top:8px; }
.galleria { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-top:30px; }
@media (min-width:900px) { .galleria { grid-template-columns:repeat(4,1fr); } }
.galleria img { width:100%; aspect-ratio:4/5; object-fit:cover; display:block; }
.serate { display:grid; gap:18px; margin-top:30px; }
.serata { display:grid; grid-template-columns:1fr; background:#fff; border:1px solid var(--sabbia); }
@media (min-width:760px) { .serata { grid-template-columns:300px 1fr; } }
.serata img { width:100%; height:100%; max-height:360px; object-fit:cover; display:block; }
.serata .corpo { padding:24px 22px; }
.quando { color:var(--oro); font-size:11px; letter-spacing:3px; text-transform:uppercase; }
.serata h3 { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:26px; line-height:1.2; margin:6px 0 2px; }
.serata .artista { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:21px; color:var(--oro); }
.serata p { font-size:14px; color:var(--muted); margin-top:10px; }
.serata .formula { color:var(--text); font-weight:500; }
.serata .btn { margin-top:16px; color:var(--text); }
.vuoto { text-align:center; background:#fff; border:1px solid var(--sabbia); padding:34px 20px; margin-top:30px; }
table { width:100%; max-width:560px; margin:24px auto 0; border-collapse:collapse; font-size:14px; }
th, td { padding:9px 12px; border-bottom:1px solid var(--sabbia); text-align:left; }
th { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); font-weight:500; }
td.si { color:var(--oro); font-weight:500; }
.faq { max-width:700px; margin:26px auto 0; }
.faq details { border-bottom:1px solid var(--sabbia); padding:16px 0; }
.faq summary { cursor:pointer; font-family:'Cormorant Garamond',serif; font-weight:600; font-size:21px; }
.faq p { margin-top:10px; font-size:14.5px; color:var(--muted); }
.altre { list-style:none; display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; margin-top:26px; }
.altre a { display:block; text-align:center; text-decoration:none; padding:18px; border:1px solid var(--oro); font-family:'Cormorant Garamond',serif; font-size:20px; }
.chiaro { text-align:center; margin-top:30px; }
.chiaro .azioni { justify-content:center; }
.dove { text-align:center; padding:68px 20px; }
.dove p { color:var(--muted); margin-top:16px; }
footer { background:var(--nero); color:rgba(255,255,255,.5); font-size:11px; text-align:center; padding:24px 20px; }
@media (max-width:600px) { .barra img { height:36px; } }
"""


def tagli_html(piatti, lingua, unita=""):
    out = []
    for p in piatti:
        prezzo = f'<span class="prezzo">€ {e(p["prezzo"])}{e(unita)}</span>' if p.get("prezzo") else ""
        desc = tr(p, "desc", lingua)
        out.append(f'<li><div class="riga"><h4>{e(tr(p, "nome", lingua))}</h4><span class="punti"></span>{prezzo}</div>'
                   + (f'<p>{e(desc)}</p>' if desc else "") + '</li>')
    return f'<ul class="tagli">{"".join(out)}</ul>'


def ristorante_ld(L, descr, extra=None):
    d = {"@context": "https://schema.org", "@type": "Restaurant", "name": "Casa Rosebery", "url": f"{SITO}/",
         "description": descr, "telephone": "+390813357572", "image": f"{SITO}/img/og-casa-rosebery.jpg",
         "servesCuisine": ["Steakhouse", "Braceria", "Italiana", "Napoletana"], "priceRange": "€€€",
         "acceptsReservations": PRENOTA, "hasMenu": f"{SITO}{L['menu_url']}",
         "address": {"@type": "PostalAddress", "streetAddress": "Via Ferdinando Russo 13", "addressLocality": "Napoli",
                     "addressRegion": "Campania", "postalCode": "80123", "addressCountry": "IT"},
         "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON}}
    d.update(extra or {})
    return d


def pagina(chiave, lingua, P, corpo, ld):
    L = COMUNE[lingua]
    r = L["rad"]
    it_url, en_url = url(chiave, "it"), url(chiave, "en")
    proprio, altro = (it_url, en_url) if lingua == "it" else (en_url, it_url)
    altre = "".join(f'<li><a href="/{PAGINE[k][0 if lingua == "it" else 1]}">{e(PAGINE[k][2 if lingua == "it" else 3])}</a></li>'
                    for k in PAGINE if k != chiave)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    return f'''<!DOCTYPE html>
<html lang="{lingua}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(P["title"])}</title>
<meta name="description" content="{e(P["descr"])}">
<link rel="canonical" href="{proprio}">
<link rel="alternate" hreflang="it" href="{it_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{it_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(P["title"])}">
<meta property="og:description" content="{e(P["descr"])}">
<meta property="og:url" content="{proprio}">
<meta property="og:image" content="{SITO}/{P["hero"].replace(".webp", ".jpg")}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" as="image" href="/{P["hero"]}" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
{lds}</head>
<body>
<header class="top" style="--hero:url('/{P["hero"]}')">
  <div class="barra">
    <a href="{L["home"]}">{L["back"]}</a>
    <a href="{L["home"]}"><img src="/logo-chiaro.png" alt="Casa Rosebery" width="120" height="44"></a>
    <a href="{altro}" hreflang="{L["alt_lang"]}" lang="{L["alt_lang"]}">{L["alt_txt"]}</a>
  </div>
  <div class="wrap" style="width:100%;padding:0">
    <span class="eyebrow">{P["eyebrow"]}</span>
    <h1>{P["h1"]}</h1>
    <p>{e(P["intro"])}</p>
    <div class="azioni">{P["azioni"]}</div>
  </div>
</header>
<main class="wrap">
{corpo}
  <section>
    <h2>{L["altre"]}</h2>
    <ul class="altre">{altre}</ul>
  </section>
</main>
<div class="dove">
  <h2>{L["dove"]}</h2>
  <p>{e(L["indirizzo"])}<br>{L["tel"]}: <a href="tel:0813357572">081 335 7572</a></p>
</div>
<footer>{"© 2026 Casa Rosebery is a trademark of Nado Advertising S.r.l. · VAT no. 07284940488" if L["lang"] == "en" else "© 2026 Casa Rosebery è un marchio di Nado Advertising S.r.l. · P. IVA 07284940488"} · <a href="/privacy.html">{L["privacy"]}</a></footer>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''


def bottoni(lingua, *extra):
    L = COMUNE[lingua]
    b = [f'<a class="btn pieno" href="{PRENOTA}" target="_blank" rel="noopener">{L["prenota"]}</a>']
    return "".join(b + list(extra))


# ───────────────────────── BRACERIA ─────────────────────────
def braceria(lingua):
    L = COMUNE[lingua]
    en = lingua == "en"
    sez = {s["titolo"]: s for s in MENU["sezioni"]}
    brace = [s for s in MENU["sezioni"] if s["titolo"] == "Dalla brace"]
    secondi = [p for p in sez["Secondi"]["piatti"] if p["nome"] in ("Misto brace (per due persone)", "Brisket Casa Rosebery", "Tagliata Flambè")]
    cruderia = [p for p in sez["Cruderia"]["piatti"] if "Wagyu" in p["nome"] or "Tartare al naturale" in p["nome"] or "Creekstone" in p["nome"]]
    tagli_oro = next(p for p in MENU["percorsi"] if p["nome"] == "Tagli d'Oro")
    unita = brace[0].get("unita", " /etto") if not en else " /100 g"
    blocchi = "".join(f'<h3 class="sotto">{e(tr(s, "sotto", lingua))}</h3>{tagli_html(s["piatti"], lingua, unita)}' for s in brace)
    n_tagli = sum(len(s["piatti"]) for s in brace)
    portate = "".join(
        f'<li><h4>{e(tr(po, "titolo", lingua))}</h4><p>{e(" · ".join(tr(pi, "nome", lingua) for pi in po["piatti"]))}</p></li>'
        for po in tagli_oro["portate"])
    T = {
        "it": dict(
            title="Braceria a Napoli, Posillipo · Carni pregiate alla brace · Casa Rosebery",
            descr=f"La braceria di Casa Rosebery a Posillipo, Napoli: {n_tagli} tagli alla brace da Italia, Europa, Americhe, Australia e Giappone, "
                  "dal Wagyu A5 al Tomahawk Black Angus, con vista sul Golfo.",
            eyebrow="Braceria · Posillipo, Napoli", h1="La braceria <em>sul Golfo di Napoli</em>",
            intro="Carni pregiate da tutto il mondo, frollate nella nostra cella e cotte alla brace: si sceglie il taglio, "
                  "si paga a peso, e la cottura la decidete voi con la sala. Davanti, il Golfo e il Vesuvio.",
            t1="I tagli alla brace", l1="La carta cambia con le disponibilità delle carni: questi sono i tagli in carta oggi, con il prezzo all'etto.",
            nota_prezzi="Prezzi all'etto, contorni a parte. Aggiornato: " + MENU.get("aggiornato", ""),
            t2="Dalla brace e dal forno", l2="Per chi vuole condividere, o preferisce una cottura lenta.",
            t3="Crudi di carne", l3="Gli stessi tagli pregiati, al naturale.",
            t4="Il percorso Tagli d'Oro", l4="Un menu degustazione dedicato alla carne, per tutto il tavolo.",
            pp="a persona", t5="Perché la nostra brace",
            perche=[("Da tutto il mondo", "Italia, Spagna, Irlanda, Danimarca, Austria, Nord Europa, Stati Uniti, Canada, Argentina, Australia e Giappone."),
                    ("Frollatura in cella", "Le carni riposano nella nostra cella prima di arrivare sulla brace."),
                    ("A peso, al tavolo", "Si sceglie il taglio, si paga all'etto: nessuna porzione fissa."),
                    ("Con i vini giusti", "Oltre 160 etichette in carta, dai rossi importanti alle bollicine.")],
            gal="Dalla cella alla brace",
            alt=["Tagli di carne frollati sul banco", "Il maestro della brace con i tagli in sala", "Tomahawk tagliato e servito", "Bistecca alla brace"]),
        "en": dict(
            title="Steakhouse in Naples, Posillipo · Premium grilled meat · Casa Rosebery",
            descr=f"Casa Rosebery's steakhouse in Posillipo, Naples: {n_tagli} cuts grilled over embers from Italy, Europe, the Americas, Australia and Japan, "
                  "from A5 Wagyu to Black Angus Tomahawk, overlooking the Bay of Naples.",
            eyebrow="Steakhouse · Posillipo, Naples", h1="A steakhouse <em>on the Bay of Naples</em>",
            intro="Premium meat from around the world, dry-aged in our own cellar and grilled over embers: choose the cut, "
                  "pay by weight and decide the doneness with our staff. In front of you, the Bay and Mount Vesuvius.",
            t1="Cuts from the grill", l1="The list changes with availability: these are today's cuts, priced per 100 g.",
            nota_prezzi="Prices per 100 g, sides extra. Updated: " + MENU.get("aggiornato_en", MENU.get("aggiornato", "")),
            t2="From the grill and the oven", l2="To share, or for those who prefer slow cooking.",
            t3="Raw beef", l3="The same premium cuts, served raw.",
            t4="The Tagli d'Oro tasting menu", l4="A tasting menu devoted to meat, for the whole table.",
            pp="per person", t5="Why our grill",
            perche=[("From around the world", "Italy, Spain, Ireland, Denmark, Austria, Northern Europe, the USA, Canada, Argentina, Australia and Japan."),
                    ("Aged in our cellar", "The meat rests in our own ageing cellar before it reaches the grill."),
                    ("By weight, at your table", "Choose the cut and pay per 100 g: no fixed portions."),
                    ("With the right wine", "Over 160 labels, from big reds to sparkling wines.")],
            gal="From the cellar to the grill",
            alt=["Dry-aged cuts on the counter", "Our grill master with the cuts in the dining room", "Sliced tomahawk served at the table", "Grilled steak"]),
    }[lingua]
    foto = ["img/IMG_1623.webp", "img/IMG_2744.webp", "img/IMG_1504.webp", "img/IMG_0414.webp"]
    gal = "".join(f'<img src="/{f}" alt="{e(a)}" loading="lazy">' for f, a in zip(foto, T["alt"]))
    per = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in T["perche"])
    corpo = f'''
  <section>
    <h2>{T["t1"]}</h2>
    <p class="lead">{e(T["l1"])}</p>
    {blocchi}
    <p class="nota">{e(T["nota_prezzi"])}</p>
  </section>
  <section>
    <h2>{T["t2"]}</h2>
    <p class="lead">{e(T["l2"])}</p>
    {tagli_html(secondi, lingua)}
  </section>
  <section>
    <h2>{T["t3"]}</h2>
    <p class="lead">{e(T["l3"])}</p>
    {tagli_html(cruderia, lingua)}
  </section>
  <section>
    <h2>{T["t4"]}</h2>
    <p class="lead">{e(T["l4"])}</p>
    <div class="scuro"><p class="pp">€ {e(tagli_oro["prezzo"])}<span>{T["pp"]}</span></p><ul>{portate}</ul></div>
  </section>
  <section>
    <h2>{T["t5"]}</h2>
    <ul class="griglia">{per}</ul>
  </section>
  <section>
    <h2>{T["gal"]}</h2>
    <div class="galleria">{gal}</div>
    <div class="chiaro"><div class="azioni">{bottoni(lingua, f'<a class="btn" href="{L["menu_url"]}">{L["menu"]}</a>', f'<a class="btn" href="{L["vini_url"]}">{L["vini"]}</a>')}</div></div>
  </section>'''
    T.update(hero="img/IMG_1623.webp", azioni=bottoni(lingua, f'<a class="btn" href="{L["menu_url"]}">{L["menu"]}</a>'))
    ld = [ristorante_ld(L, T["descr"])]
    return pagina("braceria", lingua, T, corpo, ld)


# ───────────────────────── SERATE ─────────────────────────
GIORNI = {"it": ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"],
          "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
MESI = {"it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
        "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def quando(s, lingua):
    d = dt.date.fromisoformat(s["data"])
    g, m = GIORNI[lingua][d.weekday()], MESI[lingua][d.month - 1]
    ora = s.get("ora", "")
    return f"{g} {d.day} {m} · ore {ora}" if lingua == "it" else f"{g}, {m} {d.day} · {ora}"


def serate(lingua):
    L = COMUNE[lingua]
    en = lingua == "en"
    oggi = dt.date.today()
    lista = sorted((s for s in EVENTI["serate"] if s.get("pubblica") and dt.date.fromisoformat(s["data"]) >= oggi),
                   key=lambda s: s["data"])
    T = {
        "it": dict(title="Cena con musica dal vivo a Napoli, Posillipo · Serate a Casa Rosebery",
                   descr="Cene con musica dal vivo a Posillipo, Napoli, con vista sul Golfo: il sabato sera alla carta senza minimo di spesa, "
                         "e serate speciali a menu fisso con artisti e orchestre. Calendario e prenotazioni.",
                   eyebrow="Serate · Posillipo, Napoli", h1="Cena con <em>musica dal vivo</em>",
                   intro="Il sabato sera la cena a Casa Rosebery ha una colonna sonora dal vivo, e durante l'anno ospitiamo serate speciali "
                         "a menu fisso con artisti e orchestre. Davanti, il Golfo di Napoli.",
                   cal="Prossime serate", cal_l="Il calendario si aggiorna appena fissiamo una nuova data.",
                   carta="Alla carta, nessun minimo di spesa", fisso="Menu fisso € {p} a persona · posti limitati",
                   cta_carta="Prenota un tavolo", cta_fisso="Prenota su WhatsApp",
                   wa="Ciao! Vorrei prenotare per la serata del {d} ({t}). Siamo in ",
                   vuoto="Nuove serate in arrivo. Seguiteci su Instagram per le prossime date, o prenotate un tavolo per il sabato sera.",
                   come="Come si prenota",
                   regole=[("Serate alla carta", "Si prenota online come sempre. Ordinate dal menu, senza minimo di spesa."),
                           ("Serate a menu fisso", "Posti limitati: si prenota solo su WhatsApp, indicando data e numero di persone."),
                           ("Una serata tutta vostra", "Per un evento privato con musica dal vivo, scriveteci: componiamo menu e serata insieme.")],
                   priv="Eventi privati"),
        "en": dict(title="Dinner with live music in Naples, Posillipo · Evenings at Casa Rosebery",
                   descr="Dinners with live music in Posillipo, Naples, overlooking the Bay: Saturday nights à la carte with no minimum spend, "
                         "and special set-menu evenings with artists and orchestras. Calendar and bookings.",
                   eyebrow="Live music · Posillipo, Naples", h1="Dinner with <em>live music</em>",
                   intro="On Saturday nights dinner at Casa Rosebery comes with a live soundtrack, and through the year we host special "
                         "set-menu evenings with artists and orchestras. In front of you, the Bay of Naples.",
                   cal="Upcoming evenings", cal_l="The calendar is updated as soon as we set a new date.",
                   carta="À la carte, no minimum spend", fisso="Set menu €{p} per person · limited seating",
                   cta_carta="Book a table", cta_fisso="Book on WhatsApp",
                   wa="Hi! I'd like to book for the evening of {d} ({t}). We are ",
                   vuoto="New evenings coming soon. Follow us on Instagram for the next dates, or book a table for Saturday night.",
                   come="How to book",
                   regole=[("À la carte evenings", "Book online as usual and order from the menu, no minimum spend."),
                           ("Set-menu evenings", "Limited seating: bookings on WhatsApp only, with date and number of guests."),
                           ("An evening of your own", "For a private event with live music, get in touch: we plan menu and evening together.")],
                   priv="Private events"),
    }[lingua]
    carte, ld = [], []
    for s in lista:
        titolo = tr(s, "titolo", lingua)
        q = quando(s, lingua)
        if s.get("prezzo"):
            formula = T["fisso"].format(p=s["prezzo"])
            msg = T["wa"].format(d=q.split(" ·")[0], t=titolo)
            cta = f'<a class="btn" href="https://wa.me/{WA}?text={urllib.parse.quote(msg)}" target="_blank" rel="noopener">{T["cta_fisso"]}</a>'
        else:
            formula = T["carta"]
            cta = f'<a class="btn" href="{PRENOTA}" target="_blank" rel="noopener">{T["cta_carta"]}</a>'
        foto = s.get("foto") or "img/eventi/serata-esempio.jpg"
        carte.append(f'''<article class="serata" data-data="{s["data"]}"><img src="/{foto}" alt="{e(s.get("artista", ""))}" loading="lazy">
      <div class="corpo"><span class="quando">{e(q)}</span><h3>{e(titolo)}</h3><span class="artista">{e(s.get("artista", ""))}</span>
      <p>{e(tr(s, "sottotitolo", lingua))}</p><p class="formula">{e(formula)}</p>{cta}</div></article>''')
        ev = {"@context": "https://schema.org", "@type": "Event", "name": f"{titolo} · {s.get('artista', '')}".strip(" ·"),
              "startDate": dt.datetime.fromisoformat(f'{s["data"]}T{s.get("ora", "21:00")}').replace(tzinfo=ZoneInfo("Europe/Rome")).isoformat(),
              "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "description": tr(s, "sottotitolo", lingua), "image": f"{SITO}/{foto}", "url": url("serate", lingua),
              "location": {"@type": "Restaurant", "name": "Casa Rosebery", "address": {"@type": "PostalAddress",
                           "streetAddress": "Via Ferdinando Russo 13", "addressLocality": "Napoli", "postalCode": "80123", "addressCountry": "IT"}},
              "organizer": {"@type": "Organization", "name": "Casa Rosebery", "url": f"{SITO}/"}}
        if s.get("artista"):
            ev["performer"] = {"@type": "PerformingGroup" if "&" in s["artista"] else "Person", "name": s["artista"]}
        if s.get("prezzo"):
            ev["offers"] = {"@type": "Offer", "price": s["prezzo"], "priceCurrency": "EUR", "url": url("serate", lingua),
                            "availability": "https://schema.org/LimitedAvailability"}
        ld.append(ev)
    vuoto = f'<div class="vuoto" id="vuoto"{" hidden" if carte else ""}><p>{e(T["vuoto"])}</p><div class="azioni" style="justify-content:center">{bottoni(lingua, "<a class=\"btn\" style=\"color:var(--text)\" href=\"https://www.instagram.com/casarosebery\" target=\"_blank\" rel=\"noopener\">Instagram</a>")}</div></div>'
    regole = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in T["regole"])
    corpo = f'''
  <section id="calendario">
    <h2>{T["cal"]}</h2>
    <p class="lead">{e(T["cal_l"])}</p>
    <div class="serate">{"".join(carte)}</div>
    {vuoto}
  </section>
  <section>
    <h2>{T["come"]}</h2>
    <ul class="griglia">{regole}</ul>
    <div class="chiaro"><div class="azioni">{bottoni(lingua, f'<a class="btn" href="{L["eventi_url"]}">{T["priv"]}</a>')}</div></div>
  </section>
  <script>
  // nasconde le serate passate (dalle 4 del mattino dopo, ora italiana)
  (function () {{
    var oggi = new Intl.DateTimeFormat('en-CA', {{ timeZone: 'Europe/Rome' }}).format(new Date(Date.now() - 4 * 3600 * 1000));
    var vis = 0;
    document.querySelectorAll('.serata[data-data]').forEach(function (s) {{ if (s.getAttribute('data-data') < oggi) s.remove(); else vis++; }});
    if (!vis) document.getElementById('vuoto').hidden = false;
  }})();
  </script>'''
    T.update(hero="img/IMG_1181.webp", azioni=bottoni(lingua, f'<a class="btn" href="#calendario">{T["cal"]}</a>'))
    return pagina("serate", lingua, T, corpo, [ristorante_ld(L, T["descr"])] + ld)


# ───────────────────────── VISTA MARE E COME ARRIVARE ─────────────────────────
def tramonto(mese):
    d = dt.date(2027, mese, 15)
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 0.5)
    eq = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dec = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
           - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(LAT)) * math.cos(dec))
                                - math.tan(math.radians(LAT)) * math.tan(dec)))
    t = dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc) + dt.timedelta(minutes=720 - 4 * (LON - ha) - eq)
    t = t.astimezone(ZoneInfo("Europe/Rome"))
    return t.strftime("%H:%M"), t.hour * 60 + t.minute >= 19 * 60 + 30


def vista(lingua):
    L = COMUNE[lingua]
    T = {
        "it": dict(title="Ristorante con vista mare a Posillipo, Napoli · Riva Fiorita · Casa Rosebery",
                   descr="Ristorante con vista sul Golfo di Napoli e sul Vesuvio a Riva Fiorita, Posillipo, a due passi da Marechiaro: "
                         "orari del tramonto mese per mese, come arrivare, parcheggio riservato gratuito e Villa Rosebery.",
                   eyebrow="Riva Fiorita · Posillipo, Napoli", h1="Una tavola <em>davanti al Golfo</em>",
                   intro="Casa Rosebery è a Riva Fiorita, sulla costa di Posillipo, a due passi da Marechiaro: dalle vetrate della sala "
                         "si vedono il Golfo di Napoli, il Vesuvio e il porticciolo.",
                   t1="La vista", p1=["Dalla sala e dalla terrazza lo sguardo va dal Vesuvio al mare aperto: di giorno la luce sul Golfo, la sera le luci della città lungo la costa.",
                                      "Questo tratto di costa ha una lunga storia a tavola: per generazioni qui c'è stato Giuseppone a Mare, e molti napoletani chiamano ancora così Riva Fiorita. Casa Rosebery è un progetto nuovo, con un'altra cucina, la braceria, e lo stesso mare davanti."],
                   t2="A che ora prenotare per il tramonto", l2="Da {a} {ab} {b} il tramonto cade durante la cena, che inizia alle 19:30: prenotate per l'apertura per vederlo dal tavolo. Negli altri mesi si cena dopo il tramonto, con le luci della costa.",
                   th=["Mese", "Tramonto (circa)", "Durante la cena"], si="sì", no="—",
                   nota_t="Orari calcolati per il giorno 15 di ogni mese, ora italiana.",
                   t3="Come arrivare", come=[("In auto", "Via Ferdinando Russo 13, Posillipo. Parcheggio riservato e gratuito per i clienti, nessuna ZTL."),
                                             ("In taxi", "Indicate Via Ferdinando Russo 13, Posillipo: il taxi vi lascia all'ingresso."),
                                             ("Con il navigatore", "Cercate \"Casa Rosebery\" su Google Maps: l'indirizzo è quello corretto, a Riva Fiorita.")],
                   mappa="Apri il percorso su Google Maps",
                   t4="Villa Rosebery, a pochi passi da noi",
                   faq=[("Cos'è Villa Rosebery?", "È la residenza estiva del Presidente della Repubblica, a Posillipo: un parco di circa 6,6 ettari che scende fino al mare. Prende il nome da Lord Rosebery, lo statista britannico che la acquistò nel 1897, ed è nel patrimonio della Presidenza della Repubblica dal 1957."),
                        ("Villa Rosebery è visitabile?", "Non è aperta al pubblico tutto l'anno. Si visita solo in occasioni speciali, per esempio durante le Giornate FAI o nelle aperture annunciate dalla Presidenza della Repubblica sul sito quirinale.it."),
                        ("Il ristorante si chiama così per la villa?", "Sì: il nome Casa Rosebery richiama la villa, a pochi passi dal ristorante. Non abbiamo legami con la residenza presidenziale.")],
                   gal="La sala e la vista",
                   alt=["La sala con le vetrate sul mare", "Un tavolo davanti alla finestra con il Vesuvio", "Un piatto in terrazza con vista su Napoli e il Vesuvio", "Il Vesuvio al tramonto dalla tavola"]),
        "en": dict(title="Sea view restaurant in Posillipo, Naples · Riva Fiorita · Casa Rosebery",
                   descr="Restaurant overlooking the Bay of Naples and Mount Vesuvius at Riva Fiorita, Posillipo, a short walk from Marechiaro: "
                         "sunset times month by month, how to get here, free reserved parking and Villa Rosebery.",
                   eyebrow="Riva Fiorita · Posillipo, Naples", h1="A table <em>facing the Bay</em>",
                   intro="Casa Rosebery stands at Riva Fiorita, on the Posillipo coast, a short walk from Marechiaro: from the dining-room "
                         "windows you see the Bay of Naples, Mount Vesuvius and the little harbour.",
                   t1="The view", p1=["From the dining room and the terrace the view runs from Vesuvius to the open sea: light on the Bay by day, the city lights along the coast at night.",
                                      "This stretch of coast has a long history at the table: for generations it was home to Giuseppone a Mare, and many Neapolitans still call Riva Fiorita by that name. Casa Rosebery is a new venture, with a different cuisine, the grill, and the same sea in front of it."],
                   t2="When to book for sunset", l2="From {a} to {b} sunset falls during dinner, which starts at 7:30 pm: book for opening time to watch it from your table. In the other months dinner starts after sunset, with the lights along the coast.",
                   th=["Month", "Sunset (approx.)", "During dinner"], si="yes", no="—",
                   nota_t="Times calculated for the 15th of each month, Italian time.",
                   t3="Getting here", come=[("By car", "Via Ferdinando Russo 13, Posillipo. Free reserved parking for guests, no restricted traffic zone."),
                                            ("By taxi", "Ask for Via Ferdinando Russo 13, Posillipo: the taxi drops you at the entrance."),
                                            ("With navigation", "Search \"Casa Rosebery\" on Google Maps: the address is correct, at Riva Fiorita.")],
                   mappa="Open directions in Google Maps",
                   t4="Villa Rosebery, a short walk away",
                   faq=[("What is Villa Rosebery?", "It is the summer residence of the President of the Italian Republic, in Posillipo: a park of about 6.6 hectares running down to the sea. It is named after Lord Rosebery, the British statesman who bought it in 1897, and has belonged to the Presidency since 1957."),
                        ("Can you visit Villa Rosebery?", "It is not open to the public all year. Visits are possible only on special occasions, such as the FAI Days or openings announced by the Presidency on quirinale.it."),
                        ("Is the restaurant named after the villa?", "Yes: the name Casa Rosebery recalls the villa, a short walk from the restaurant. We have no connection with the presidential residence.")],
                   gal="The dining room and the view",
                   alt=["The dining room with windows on the sea", "A table by the window with Mount Vesuvius", "A dish on the terrace overlooking Naples and Vesuvius", "Mount Vesuvius at sunset from the table"]),
    }[lingua]
    righe = ""
    mesi_cena = [m for m in range(1, 13) if tramonto(m)[1]]
    b = MESI[lingua][mesi_cena[-1] - 1]
    T["l2"] = T["l2"].format(a=MESI[lingua][mesi_cena[0] - 1], b=b, ab="ad" if b[0] in "aeiou" else "a")
    for m in range(1, 13):
        ora, cena = tramonto(m)
        if lingua == "en":
            h, mi = map(int, ora.split(":"))
            ora = f"{(h - 1) % 12 + 1}:{mi:02d} {'pm' if h >= 12 else 'am'}"
        righe += f'<tr><td>{MESI[lingua][m - 1].capitalize()}</td><td>{ora}</td><td class="{"si" if cena else ""}">{T["si"] if cena else T["no"]}</td></tr>'
    come = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in T["come"])
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in T["faq"])
    foto = ["img/IMG_1181.webp", "img/IMG_1176.webp", "img/0076581a-c5de-4499-991e-eea7a98d8b48.webp", "img/cucina-involtini-verza-vesuvio.webp"]
    gal = "".join(f'<img src="/{f}" alt="{e(a)}" loading="lazy">' for f, a in zip(foto, T["alt"]))
    corpo = f'''
  <section>
    <h2>{T["t1"]}</h2>
    <div class="testo">{"".join(f"<p>{e(p)}</p>" for p in T["p1"])}</div>
    <div class="galleria">{gal}</div>
  </section>
  <section>
    <h2>{T["t2"]}</h2>
    <p class="lead">{e(T["l2"])}</p>
    <table><thead><tr>{"".join(f"<th>{h}</th>" for h in T["th"])}</tr></thead><tbody>{righe}</tbody></table>
    <p class="nota">{e(T["nota_t"])}</p>
  </section>
  <section id="come-arrivare">
    <h2>{T["t3"]}</h2>
    <ul class="griglia">{come}</ul>
    <div class="chiaro"><div class="azioni"><a class="btn pieno" href="{MAPPA}" target="_blank" rel="noopener">{T["mappa"]}</a>{bottoni(lingua).replace("btn pieno", "btn")}</div></div>
  </section>
  <section id="villa-rosebery">
    <h2>{T["t4"]}</h2>
    <div class="faq">{faq}</div>
  </section>'''
    T.update(hero="img/IMG_1154.webp", azioni=bottoni(lingua, f'<a class="btn" href="#come-arrivare">{T["t3"]}</a>'))
    return pagina("vista", lingua, T, corpo, [ristorante_ld(L, T["descr"])])


for chiave, fn in (("braceria", braceria), ("serate", serate), ("vista", vista)):
    for lingua in ("it", "en"):
        f = RADICE / PAGINE[chiave][0 if lingua == "it" else 1]
        f.write_text(fn(lingua), encoding="utf-8")
        print(f.relative_to(RADICE), "generato")
