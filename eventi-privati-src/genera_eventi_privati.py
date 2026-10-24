#!/usr/bin/env python3
"""Genera la pagina Eventi privati: eventi-privati.html (IT) ed en/private-events.html (EN).
Modificare i testi qui sotto e rilanciare:  python3 eventi-privati-src/genera_eventi_privati.py"""
import json
from html import escape as e
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SITO = "https://www.casaroseberyristorante.it"
WA = "390813357572"
EMAIL = "prenotazioni@casaroseberyristorante.it"

CAPIENZA_SEDUTI, CAPIENZA_PIEDI = 120, 180

FOTO = {
    "hero": "img/IMG_1181.webp",
    "galleria": [
        ("img/IMG_1176.webp", "Tavolo apparecchiato davanti alla finestra con il Vesuvio", "Table set by the window with Mount Vesuvius"),
        ("img/0076581a-c5de-4499-991e-eea7a98d8b48.webp", "Un piatto in terrazza con vista su Napoli e il Vesuvio", "A dish on the terrace overlooking Naples and Vesuvius"),
        ("img/IMG_1179.webp", "Calici sulla tavola apparecchiata", "Wine glasses on the set table"),
        ("img/IMG_5417.webp", "Un tagliere di carne portato in sala", "A board of grilled meat served in the dining room"),
    ],
}

MENU_ESEMPIO = [
    ("Ciabatta Mediterraneo", "Insalatina di puntarelle, alici di Cetara, stracciatella di bufala e dressing di miele e senape.",
     "Puntarelle chicory salad, Cetara anchovies, buffalo stracciatella, honey-mustard dressing."),
    ("Scarpariello secondo Casa Rosebery", "Bombardone ripieno di crema al pecorino e salsa di pomodoro leggermente piccante.",
     "Large pasta tubes filled with pecorino cream, lightly spicy tomato sauce."),
    ("Brasato", "Stracotto di manzo al vino rosso, servito con fonduta di parmigiano.",
     "Beef slow-braised in red wine, with Parmigiano fondue."),
    ("Locena di maiale", "Dalla finitura croccante, con papaccelle saltate in padella e riduzione vellutata alla mela.",
     "Pork loin with a crisp finish, pan-fried papaccelle peppers and apple reduction."),
    ("Tiramisù", "La nostra interpretazione del classico trevigiano.", "Our take on the Treviso classic."),
]

TESTI = {
    "it": {
        "file": RADICE / "eventi-privati.html", "lang": "it", "rad": "", "url": f"{SITO}/eventi-privati.html",
        "alt_url": f"{SITO}/en/private-events.html", "alt_lang": "en", "alt_txt": "English", "home": "index.html",
        "title": "Eventi privati e cene aziendali a Posillipo · Casa Rosebery, Napoli",
        "descr": f"Cene aziendali, compleanni, battesimi, feste di laurea e degustazioni private a Posillipo con vista sul Golfo di Napoli: "
                 f"fino a {CAPIENZA_SEDUTI} ospiti seduti o {CAPIENZA_PIEDI} in piedi, menu su misura dalla nostra braceria.",
        "eyebrow": "Eventi privati", "h1": "La vostra occasione, <em>con vista sul Golfo</em>",
        "intro": "Dalla cena aziendale al compleanno, dal battesimo alla festa tra amici: a Casa Rosebery ogni evento ha "
                 "un menu pensato su misura, il servizio della nostra sala e, sullo sfondo, il Golfo di Napoli e il Vesuvio.",
        "cta": "Richiedi un preventivo", "cta_wa": "Scrivici su WhatsApp",
        "cap_tit": "Quanti ospiti", "seduti": "ospiti seduti", "seduti_d": "cena servita al tavolo",
        "piedi": "ospiti in piedi", "piedi_d": "aperitivo, buffet o cocktail dinner",
        "cap_nota": "La capienza dipende dalla formula: con la cena seduta arriviamo a {s} persone, in piedi fino a {p}. Per gruppi più piccoli riserviamo una parte della sala.",
        "occ_tit": "Le occasioni",
        "occasioni": [
            ("Cene aziendali e team building", "Cene con clienti e colleghi, feste di fine anno e team building con sommelier, costruiti su percorsi enologici."),
            ("Compleanni e anniversari", "Dal tavolo riservato alla sala intera, con torta e brindisi."),
            ("Battesimi e comunioni", "Pranzi in famiglia con un menu dedicato anche ai più piccoli."),
            ("Feste di laurea e feste private", "Lauree, rimpatriate, feste tra amici: la sala è vostra."),
            ("Degustazioni private", "Su richiesta, degustazioni di vini e di carni e percorsi di avvicinamento alla degustazione, guidati da sommelier qualificati."),
            ("Presentazioni ed eventi", "Lanci di prodotto, serate a tema, eventi aziendali con musica."),
        ],
        "perche_tit": "Perché da noi",
        "perche": [
            ("Vista sul Golfo", "Grandi vetrate sul mare, il Vesuvio e il porticciolo di Marechiaro."),
            ("Braceria di carni pregiate", "Tagli da tutto il mondo, frollati nella nostra cella e cotti alla brace."),
            ("Menu su misura", "Dalla cena di più portate al buffet: lo costruiamo con voi, anche per esigenze alimentari particolari."),
            ("Carta dei vini", "Oltre 160 etichette, dalle bollicine ai grandi rossi, e abbinamenti consigliati."),
            ("Musica dal vivo", "Su richiesta, artisti per accompagnare la serata."),
            ("Parcheggio riservato", "Gratuito, a disposizione dei vostri ospiti."),
        ],
        "menu_tit": "Un esempio di menu", "menu_nota": "Il menu di una delle nostre serate. Per il vostro evento lo componiamo insieme, anche con i tagli della braceria.",
        "gal_tit": "La sala", "form_tit": "Raccontateci il vostro evento",
        "form_intro": "Vi ricontattiamo per proporvi menu e preventivo. Se preferite, scriveteci direttamente su WhatsApp.",
        "f_nome": "Nome e cognome", "f_tel": "Telefono", "f_email": "Email (facoltativa)", "f_data": "Data dell'evento",
        "f_pers": "Numero di ospiti", "f_form": "Formula", "f_form_opz": ["Cena seduta", "In piedi (aperitivo, buffet)", "Da valutare insieme"],
        "f_tipo": "Tipo di evento", "f_altro": "Altro", "f_note": "Note o richieste particolari",
        "f_note_ph": "Orario, budget indicativo, allergie, musica...", "f_invia": "Invia la richiesta", "oppure": "oppure",
        "esito": 'Si sta aprendo la tua app di posta con la richiesta pronta. Se non si apre, <a href="{wa}" target="_blank" rel="noopener">invia la stessa richiesta su WhatsApp</a>.',
        "wa_testo": "Ciao! Vorrei informazioni per un evento privato a Casa Rosebery.",
        "msg": ["Richiesta evento privato", "Nome", "Telefono", "Email", "Data", "Ospiti", "Formula", "Tipo", "Note"],
        "dove": "Dove siamo", "indirizzo": "Via Ferdinando Russo 13 · 80123 Posillipo, Napoli", "tel_lbl": "Telefono",
        "privacy": "Privacy e cookie", "back": "← Home",
    },
    "en": {
        "file": RADICE / "en" / "private-events.html", "lang": "en", "rad": "/", "url": f"{SITO}/en/private-events.html",
        "alt_url": f"{SITO}/eventi-privati.html", "alt_lang": "it", "alt_txt": "Italiano", "home": "/en/",
        "title": "Private events & corporate dinners in Posillipo, Naples · Casa Rosebery",
        "descr": f"Corporate dinners, birthdays, christenings, graduation parties and private tastings in Posillipo overlooking the Bay of Naples: "
                 f"up to {CAPIENZA_SEDUTI} seated guests or {CAPIENZA_PIEDI} standing, tailor-made menus from our steakhouse.",
        "eyebrow": "Private events", "h1": "Your occasion, <em>overlooking the Bay</em>",
        "intro": "From corporate dinners to birthdays, christenings and parties with friends: at Casa Rosebery every event gets a "
                 "tailor-made menu, our dining-room service and, as a backdrop, the Bay of Naples and Mount Vesuvius.",
        "cta": "Request a quote", "cta_wa": "Message us on WhatsApp",
        "cap_tit": "How many guests", "seduti": "seated guests", "seduti_d": "dinner served at the table",
        "piedi": "standing guests", "piedi_d": "aperitivo, buffet or cocktail dinner",
        "cap_nota": "Capacity depends on the format: up to {s} guests for a seated dinner, up to {p} standing. For smaller groups we reserve part of the dining room.",
        "occ_tit": "Occasions",
        "occasioni": [
            ("Corporate dinners & team building", "Client and team dinners, end-of-year parties and team building with a sommelier, built around wine journeys."),
            ("Birthdays & anniversaries", "From a reserved table to the whole room, with cake and a toast."),
            ("Christenings & communions", "Family lunches with a dedicated menu for children too."),
            ("Graduation & private parties", "Graduations, reunions, parties with friends: the room is yours."),
            ("Private tastings", "On request, wine and meat tastings and introductory tasting courses led by qualified sommeliers."),
            ("Launches & events", "Product launches, themed evenings, corporate events with music."),
        ],
        "perche_tit": "Why Casa Rosebery",
        "perche": [
            ("Sea view", "Large windows over the sea, Mount Vesuvius and the Marechiaro harbour."),
            ("Premium steakhouse", "Cuts from around the world, dry-aged in our own cellar and grilled over embers."),
            ("Tailor-made menus", "From a multi-course dinner to a buffet, built with you, dietary needs included."),
            ("Wine list", "Over 160 labels, from sparkling wines to great reds, with suggested pairings."),
            ("Live music", "On request, artists to accompany your evening."),
            ("Reserved parking", "Free, for your guests."),
        ],
        "menu_tit": "A sample menu", "menu_nota": "The menu from one of our evenings. For your event we design it together, steakhouse cuts included.",
        "gal_tit": "The dining room", "form_tit": "Tell us about your event",
        "form_intro": "We will get back to you with a menu proposal and a quote. Or message us directly on WhatsApp.",
        "f_nome": "Full name", "f_tel": "Phone", "f_email": "Email (optional)", "f_data": "Event date",
        "f_pers": "Number of guests", "f_form": "Format", "f_form_opz": ["Seated dinner", "Standing (aperitivo, buffet)", "To be discussed"],
        "f_tipo": "Type of event", "f_altro": "Other", "f_note": "Notes or special requests",
        "f_note_ph": "Time, indicative budget, allergies, music...", "f_invia": "Send request", "oppure": "or",
        "esito": 'Your email app should open with the request ready to send. If it doesn’t, <a href="{wa}" target="_blank" rel="noopener">send the same request on WhatsApp</a>.',
        "wa_testo": "Hi! I'd like information about a private event at Casa Rosebery.",
        "msg": ["Private event request", "Name", "Phone", "Email", "Date", "Guests", "Format", "Type", "Notes"],
        "dove": "Find us", "indirizzo": "Via Ferdinando Russo 13 · 80123 Posillipo, Naples", "tel_lbl": "Phone",
        "privacy": "Privacy & cookies", "back": "← Home",
    },
}


def jsonld(L):
    d = {
        "@context": "https://schema.org", "@type": "EventVenue",
        "name": "Casa Rosebery — " + ("Eventi privati" if L["lang"] == "it" else "Private events"),
        "description": L["descr"], "url": L["url"],
        "maximumAttendeeCapacity": CAPIENZA_PIEDI,
        "telephone": "+390813357572", "email": EMAIL,
        "image": f"{SITO}/{FOTO['hero']}",
        "address": {"@type": "PostalAddress", "streetAddress": "Via Ferdinando Russo 13", "addressLocality": "Napoli",
                    "addressRegion": "Campania", "postalCode": "80123", "addressCountry": "IT"},
        "geo": {"@type": "GeoCoordinates", "latitude": "40.8132", "longitude": "14.2018"},
        "containedInPlace": {"@type": "Restaurant", "name": "Casa Rosebery", "url": f"{SITO}/"},
    }
    return json.dumps(d, ensure_ascii=False, indent=1)


def pagina(L):
    r = L["rad"]
    en = L["lang"] == "en"
    tipi = [o[0] for o in L["occasioni"]] + [L["f_altro"]]
    occ = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in L["occasioni"])
    per = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in L["perche"])
    menu = "".join(f'<li><h4>{e(n)}</h4><p>{e(den if en else dit)}</p></li>' for n, dit, den in MENU_ESEMPIO)
    gal = "".join(f'<img src="{r}{f}" alt="{e(aen if en else ait)}" loading="lazy">' for f, ait, aen in FOTO["galleria"])
    wa_link = f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(L["wa_testo"])
    cfg = json.dumps({"wa": WA, "email": EMAIL, "msg": L["msg"], "esito": L["esito"]}, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{L["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(L["title"])}</title>
<meta name="description" content="{e(L["descr"])}">
<link rel="canonical" href="{L["url"]}">
<link rel="alternate" hreflang="it" href="{SITO}/eventi-privati.html">
<link rel="alternate" hreflang="en" href="{SITO}/en/private-events.html">
<link rel="alternate" hreflang="x-default" href="{SITO}/eventi-privati.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(L["title"])}">
<meta property="og:description" content="{e(L["descr"])}">
<meta property="og:url" content="{L["url"]}">
<meta property="og:image" content="{SITO}/{FOTO["hero"].replace(".webp", ".jpg")}">
<link rel="icon" href="{r}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<link rel="preload" as="image" href="{r}{FOTO["hero"]}" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {{ --nero:#0e0d0a; --carbone:#1a1814; --oro:#b8923a; --oro-lt:#d4aa5a; --crema:#faf8f3; --sabbia:#e8e0d0; --text:#1a1208; --muted:#6f6656; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; }}
body {{ font-family:'Inter',sans-serif; font-weight:300; background:var(--crema); color:var(--text); line-height:1.65; }}
a {{ color:inherit; }}
.serif {{ font-family:'Cormorant Garamond',serif; }}
.top {{ position:relative; min-height:78vh; display:flex; flex-direction:column; justify-content:flex-end; color:#fff;
  background:linear-gradient(to bottom, rgba(14,13,10,.75) 0, rgba(14,13,10,.15) 30%, rgba(14,13,10,.85) 100%), url('{r}{FOTO["hero"]}') center/cover; padding:24px 20px 56px; }}
.barra {{ position:absolute; top:0; left:0; right:0; display:flex; justify-content:space-between; align-items:center; padding:18px 20px; font-size:11px; letter-spacing:2px; text-transform:uppercase; }}
.barra a {{ text-decoration:none; color:rgba(255,255,255,.8); }}
.barra img {{ height:44px; width:auto; }}
.top .eyebrow {{ color:var(--oro-lt); font-size:11px; letter-spacing:4px; text-transform:uppercase; }}
.top h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(36px,7vw,64px); line-height:1.1; margin:10px 0 16px; max-width:820px; }}
.top h1 em {{ color:var(--oro-lt); }}
.top p {{ max-width:620px; color:rgba(255,255,255,.85); font-size:15px; }}
.azioni {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:26px; }}
.btn {{ display:inline-block; padding:14px 26px; font-size:11px; letter-spacing:2.5px; text-transform:uppercase; text-decoration:none; border:1px solid var(--oro); color:var(--oro-lt); background:transparent; cursor:pointer; font-family:inherit; }}
.btn.pieno {{ background:var(--oro); color:var(--nero); }}
.wrap {{ max-width:1040px; margin:0 auto; padding:0 20px; }}
section {{ padding:72px 0 0; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:clamp(30px,5vw,42px); text-align:center; }}
h2::after {{ content:''; display:block; width:40px; height:1px; background:var(--oro); margin:14px auto 0; }}
.lead {{ text-align:center; color:var(--muted); max-width:640px; margin:18px auto 0; font-size:14px; }}
.cap {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:34px; }}
.cap div {{ background:var(--nero); color:#fff; text-align:center; padding:30px 16px; border:1px solid rgba(184,146,58,.35); }}
.cap b {{ display:block; font-family:'Cormorant Garamond',serif; font-weight:400; font-size:58px; line-height:1; color:var(--oro-lt); }}
.cap span {{ display:block; font-size:11px; letter-spacing:2px; text-transform:uppercase; margin-top:8px; }}
.cap small {{ display:block; color:rgba(255,255,255,.6); font-size:12px; margin-top:6px; }}
.griglia {{ list-style:none; display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px; margin-top:34px; }}
.griglia li {{ background:#fff; border:1px solid var(--sabbia); border-top:2px solid var(--oro); padding:24px 22px; }}
.griglia h3 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:22px; margin-bottom:6px; }}
.griglia p {{ font-size:13.5px; color:var(--muted); }}
.menu {{ background:var(--nero); color:#fff; padding:40px 26px; margin-top:34px; border:1px solid rgba(184,146,58,.35); }}
.menu ul {{ list-style:none; max-width:560px; margin:0 auto; }}
.menu li {{ text-align:center; padding:14px 0; border-bottom:1px solid rgba(255,255,255,.08); }}
.menu li:last-child {{ border:0; }}
.menu h4 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:21px; }}
.menu p {{ color:rgba(255,255,255,.6); font-size:13px; }}
.galleria {{ display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-top:34px; }}
.galleria img {{ width:100%; aspect-ratio:4/5; object-fit:cover; display:block; }}
form {{ max-width:680px; margin:30px auto 0; display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.campo {{ display:flex; flex-direction:column; gap:6px; }}
.campo.pieno {{ grid-column:1 / -1; }}
label {{ font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); }}
input, select, textarea {{ font:inherit; font-size:15px; padding:12px 14px; border:1px solid var(--sabbia); background:#fff; color:var(--text); border-radius:0; }}
textarea {{ min-height:110px; resize:vertical; }}
input:focus, select:focus, textarea:focus {{ outline:2px solid var(--oro); outline-offset:-1px; }}
.invio {{ grid-column:1 / -1; display:flex; gap:14px; align-items:center; flex-wrap:wrap; justify-content:center; margin-top:6px; }}
.invio .btn {{ color:var(--nero); }}
.invio .btn.pieno {{ color:var(--nero); }}
.invio span {{ color:var(--muted); font-size:12px; }}
.esito {{ grid-column:1 / -1; background:#fff; border:1px solid var(--oro); padding:14px; font-size:14px; text-align:center; }}
.esito a {{ color:var(--oro); }}
.dove {{ text-align:center; padding:72px 20px; }}
.dove p {{ color:var(--muted); margin-top:16px; }}
.dove a {{ color:var(--text); }}
footer {{ background:var(--nero); color:rgba(255,255,255,.45); font-size:11px; text-align:center; padding:24px 20px; }}
footer a {{ color:inherit; }}
@media (max-width:600px) {{
  form {{ grid-template-columns:1fr; }}
  .cap b {{ font-size:46px; }}
  .barra img {{ height:36px; }}
}}
@media (min-width:900px) {{ .galleria {{ grid-template-columns:repeat(4,1fr); }} }}
</style>
<script type="application/ld+json">
{jsonld(L)}
</script>
</head>
<body>
<header class="top">
  <div class="barra">
    <a href="{L["home"]}">{L["back"]}</a>
    <a href="{L["home"]}"><img src="{r}logo-chiaro.png" alt="Casa Rosebery"></a>
    <a href="{L["alt_url"]}" hreflang="{L["alt_lang"]}" lang="{L["alt_lang"]}">{L["alt_txt"]}</a>
  </div>
  <div class="wrap" style="width:100%;padding:0">
    <span class="eyebrow">{L["eyebrow"]}</span>
    <h1>{L["h1"]}</h1>
    <p>{e(L["intro"])}</p>
    <div class="azioni">
      <a class="btn pieno" href="#richiesta">{L["cta"]}</a>
      <a class="btn" href="{wa_link}" target="_blank" rel="noopener">{L["cta_wa"]}</a>
    </div>
  </div>
</header>

<main class="wrap">
  <section>
    <h2>{L["cap_tit"]}</h2>
    <div class="cap">
      <div><b>{CAPIENZA_SEDUTI}</b><span>{L["seduti"]}</span><small>{L["seduti_d"]}</small></div>
      <div><b>{CAPIENZA_PIEDI}</b><span>{L["piedi"]}</span><small>{L["piedi_d"]}</small></div>
    </div>
    <p class="lead">{e(L["cap_nota"].format(s=CAPIENZA_SEDUTI, p=CAPIENZA_PIEDI))}</p>
  </section>

  <section>
    <h2>{L["occ_tit"]}</h2>
    <ul class="griglia">{occ}</ul>
  </section>

  <section>
    <h2>{L["perche_tit"]}</h2>
    <ul class="griglia">{per}</ul>
  </section>

  <section>
    <h2>{L["menu_tit"]}</h2>
    <p class="lead">{e(L["menu_nota"])}</p>
    <div class="menu"><ul>{menu}</ul></div>
  </section>

  <section>
    <h2>{L["gal_tit"]}</h2>
    <div class="galleria">{gal}</div>
  </section>

  <section id="richiesta">
    <h2>{L["form_tit"]}</h2>
    <p class="lead">{e(L["form_intro"])}</p>
    <form id="form-evento">
      <div class="campo"><label for="f-nome">{L["f_nome"]}</label><input id="f-nome" autocomplete="name" required></div>
      <div class="campo"><label for="f-tel">{L["f_tel"]}</label><input id="f-tel" type="tel" autocomplete="tel" required></div>
      <div class="campo"><label for="f-email">{L["f_email"]}</label><input id="f-email" type="email" autocomplete="email"></div>
      <div class="campo"><label for="f-data">{L["f_data"]}</label><input id="f-data" type="date" required></div>
      <div class="campo"><label for="f-pers">{L["f_pers"]}</label><input id="f-pers" type="number" min="2" max="{CAPIENZA_PIEDI}" inputmode="numeric" required></div>
      <div class="campo"><label for="f-form">{L["f_form"]}</label><select id="f-form">{"".join(f"<option>{e(o)}</option>" for o in L["f_form_opz"])}</select></div>
      <div class="campo pieno"><label for="f-tipo">{L["f_tipo"]}</label><select id="f-tipo">{"".join(f"<option>{e(t)}</option>" for t in tipi)}</select></div>
      <div class="campo pieno"><label for="f-note">{L["f_note"]}</label><textarea id="f-note" placeholder="{e(L["f_note_ph"])}"></textarea></div>
      <div class="invio">
        <button type="submit" class="btn pieno">{L["f_invia"]}</button>
        <span>{L["oppure"]}</span>
        <a class="btn" href="{wa_link}" target="_blank" rel="noopener">{L["cta_wa"]}</a>
      </div>
      <p class="esito" id="esito" role="status" hidden></p>
    </form>
  </section>
</main>

<div class="dove">
  <h2>{L["dove"]}</h2>
  <p>{e(L["indirizzo"])}<br>{L["tel_lbl"]}: <a href="tel:0813357572">081 335 7572</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<footer>© 2026 Casa Rosebery · Nado Advertising S.r.l. · P.IVA 07284940488 · <a href="{r}privacy.html">{L["privacy"]}</a></footer>

<script id="cfg-evento" type="application/json">{cfg}</script>
<script>
(function () {{
  var C = JSON.parse(document.getElementById('cfg-evento').textContent);
  var f = document.getElementById('form-evento');
  f.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var v = function (id) {{ return document.getElementById(id).value.trim(); }};
    var m = C.msg;
    var testo = m[0] + '\\n' + m[1] + ': ' + v('f-nome') + '\\n' + m[2] + ': ' + v('f-tel') +
      (v('f-email') ? '\\n' + m[3] + ': ' + v('f-email') : '') + '\\n' + m[4] + ': ' + v('f-data') +
      '\\n' + m[5] + ': ' + v('f-pers') + '\\n' + m[6] + ': ' + v('f-form') + '\\n' + m[7] + ': ' + v('f-tipo') +
      (v('f-note') ? '\\n' + m[8] + ': ' + v('f-note') : '');
    var enc = encodeURIComponent(testo);
    var wa = 'https://wa.me/' + C.wa + '?text=' + enc;
    var es = document.getElementById('esito');
    es.innerHTML = C.esito.replace('{{wa}}', wa); es.hidden = false;
    if (window.__gaCaricato && window.gtag) gtag('event', 'richiesta_evento', {{ tipo_evento: v('f-tipo'), persone: v('f-pers'), formula: v('f-form'), pagina: 'eventi_privati' }});
    window.location.href = 'mailto:' + C.email + '?subject=' + encodeURIComponent(m[0] + ' - Casa Rosebery') + '&body=' + enc;
  }});
}})();
</script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''


for L in TESTI.values():
    L["file"].write_text(pagina(L), encoding="utf-8")
    print(L["file"].relative_to(RADICE), "generato")
