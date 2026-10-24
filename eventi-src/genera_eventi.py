"""Inserisce la sezione "Prossime serate" in index.html (italiano) e in en/index.html (inglese)
a partire da eventi-src/eventi.json.

Uso (dalla cartella del repo):
  python3 eventi-src/genera_eventi.py              -> solo serate con "pubblica": true
  python3 eventi-src/genera_eventi.py --anteprima  -> include anche le bozze (NON fare commit di questo risultato)

Testi inglesi: per ogni campo di testo si può aggiungere la versione inglese con il suffisso _en
(titolo_en, sottotitolo_en, nota_menu_en, extra_titolo_en; nei piatti desc_en, nome_en, gruppo_en).
Se manca, la pagina inglese usa il testo italiano.
"""
import datetime as dt
import html
import json
import pathlib
import sys
import urllib.parse
from zoneinfo import ZoneInfo

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://www.casaroseberyristorante.it"
INIZIO, FINE = "<!-- EVENTI:INIZIO -->", "<!-- EVENTI:FINE -->"
ANTEPRIMA = "--anteprima" in sys.argv
e = html.escape

TESTI = {
    "it": {
        "file": RADICE / "index.html", "url": f"{SITO}/",
        "giorni": ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"],
        "mesi": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
                 "settembre", "ottobre", "novembre", "dicembre"],
        "ore": "ore", "bozza": "BOZZA – non pubblicata", "integr": "Integrazione · + € {p} a persona",
        "alla_carta": "Alla carta", "pp": "a persona · menu fisso", "menu_carta": "Menu alla carta",
        "nota_default": "nessun minimo di spesa", "avviso": "Prenotazione obbligatoria via WhatsApp",
        "cta": "Prenota su WhatsApp", "cta_carta": "Prenota un tavolo", "locandina": "Locandina",
        "oggi": "Stasera", "domani": "Domani",
        "wa": "Ciao! Vorrei prenotare per la serata del {g} {m} ({t}). Siamo in ",
        "eyebrow": "In programma", "titolo": "Prossime <em>serate</em>",
        "intro": "Cene con musica dal vivo e ospiti speciali. Le serate a menu fisso hanno posti limitati e si prenotano solo via WhatsApp; le serate alla carta si prenotano come sempre.",
        "menu_fisso": " Menu fisso a {p} € a persona.", "descr_default": "{t} a Casa Rosebery, Napoli.",
        "nav": "Serate",
    },
    "en": {
        "file": RADICE / "en" / "index.html", "url": f"{SITO}/en/",
        "giorni": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "mesi": ["January", "February", "March", "April", "May", "June", "July", "August",
                 "September", "October", "November", "December"],
        "ore": "", "bozza": "DRAFT – not published", "integr": "Upgrade · + € {p} per person",
        "alla_carta": "À la carte", "pp": "per person · set menu", "menu_carta": "À la carte menu",
        "nota_default": "no minimum spend", "avviso": "Booking required via WhatsApp",
        "cta": "Book on WhatsApp", "cta_carta": "Book a table", "locandina": "Poster",
        "oggi": "Tonight", "domani": "Tomorrow",
        "wa": "Hi! I'd like to book for the {t} evening on {m} {g}. We are ",
        "eyebrow": "Coming up", "titolo": "Upcoming <em>evenings</em>",
        "intro": "Dinners with live music and special guests. Set-menu evenings have limited seating and can only be booked via WhatsApp; à la carte evenings are booked as usual.",
        "menu_fisso": " Set menu at €{p} per person.", "descr_default": "{t} at Casa Rosebery, Naples.",
        "nav": "Live",
    },
}

dati = json.loads((RADICE / "eventi-src" / "eventi.json").read_text(encoding="utf-8"))
oggi = dt.date.today()
serate = sorted(
    (s for s in dati["serate"]
     if (s.get("pubblica") or ANTEPRIMA) and dt.date.fromisoformat(s["data"]) >= oggi),
    key=lambda s: (s["data"], s.get("ora", "")))


def tr(obj, campo, lingua, default=""):
    """Testo nella lingua richiesta, con ripiego sull'italiano."""
    if lingua != "it" and obj.get(f"{campo}_{lingua}"):
        return obj[f"{campo}_{lingua}"]
    return obj.get(campo, default)


def ora_en(hhmm):
    h, m = map(int, hhmm.split(":"))
    return f"{(h - 1) % 12 + 1}{':%02d' % m if m else ''} {'pm' if h >= 12 else 'am'}"


def quando(s, L, lingua):
    d = dt.date.fromisoformat(s["data"])
    if lingua == "en":
        q = f'{L["giorni"][d.weekday()]} {d.day} {L["mesi"][d.month - 1]}'
        return q + (f' · {ora_en(s["ora"])}' if s.get("ora") else "")
    q = f'{L["giorni"][d.weekday()]} {d.day} {L["mesi"][d.month - 1]}'
    return q + (f' · {L["ore"]} {e(s["ora"])}' if s.get("ora") else "")


def carta(s, lingua):
    L = TESTI[lingua]
    d = dt.date.fromisoformat(s["data"])
    titolo = tr(s, "titolo", lingua)
    bozza = '' if s.get("pubblica") else f'<span class="serata-bozza">{L["bozza"]}</span>'
    artista = f'<p class="serata-artista">{e(s["artista"])}</p>' if s.get("artista") else ""
    sotto_t = tr(s, "sottotitolo", lingua)
    sotto = f'<p class="serata-sotto">{e(sotto_t)}</p>' if sotto_t else ""
    portate = "".join(f'<li><b>{e(tr(p, "nome", lingua))}</b><span>{e(tr(p, "desc", lingua))}</span></li>'
                      for p in s.get("menu", []))
    integr = ""
    if s.get("integrazione"):
        i = s["integrazione"]
        integr = (f'<div class="serata-integr"><span>{e(L["integr"].format(p=i["prezzo"]))}</span>'
                  f'<b>{e(tr(i, "nome", lingua))}</b><em>{e(tr(i, "desc", lingua))}</em></div>')
    extra = ""
    if s.get("extra"):
        gruppi = {}
        for x in s["extra"]:
            gruppi.setdefault(tr(x, "gruppo", lingua), []).append(x)
        blocchi = "".join(
            f'<h4>{e(g)}</h4><ul>' + "".join(
                f'<li><div><b>{e(tr(x, "nome", lingua))}</b><span>{e(tr(x, "desc", lingua))}</span></div>'
                f'<i>€ {e(x["prezzo"])}</i></li>'
                for x in xs) + '</ul>'
            for g, xs in gruppi.items())
        extra = (f'<details class="serata-extra"><summary>{e(tr(s, "extra_titolo", lingua, L["alla_carta"]))}'
                 f'</summary>{blocchi}</details>')
    if s.get("prezzo") and s.get("menu"):
        menu_html = (f'<div class="serata-menu"><div class="serata-prezzo"><b>€ {e(s["prezzo"])}</b>'
                     f'<span>{L["pp"]}</span></div><ul class="serata-portate">{portate}</ul>{integr}</div>')
    else:
        menu_html = (f'<div class="serata-menu"><div class="serata-prezzo"><b>{L["menu_carta"]}</b>'
                     f'<span>{e(tr(s, "nota_menu", lingua, L["nota_default"]))}</span></div></div>')
    testo_wa = L["wa"].format(g=d.day, m=L["mesi"][d.month - 1], t=titolo)
    wa = "https://wa.me/390813357572?text=" + urllib.parse.quote(testo_wa)
    if s.get("prezzo"):
        # menu fisso: posti limitati, solo WhatsApp
        prenota = (f'<p class="serata-avviso">{L["avviso"]}</p>\n        <div class="serata-cta">'
                   f'<a href="{wa}" target="_blank" rel="noopener" class="btn-gold serata-wa" data-serata="{e(s["data"])}">{L["cta"]}</a></div>')
    else:
        # alla carta: prenotazione libera dai canali abituali
        prenota = (f'<div class="serata-cta"><a href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener" '
                   f'class="btn-gold" data-serata="{e(s["data"])}">{L["cta_carta"]}</a></div>')
    foto_src = s.get("foto", "")
    if foto_src and lingua != "it":
        foto_src = "/" + foto_src
    foto = (f'<div class="serata-foto"><img src="{e(foto_src)}" alt="{L["locandina"]}: {e(titolo)}'
            + (f' – {e(s["artista"])}' if s.get("artista") else "") + '" loading="lazy"></div>') if foto_src else ""
    return f'''
    <article class="serata" data-data="{e(s["data"])}">
      {foto}
      <div class="serata-corpo">
        {bozza}
        <p class="serata-quando">{quando(s, L, lingua)}</p>
        <h3 class="serata-titolo">{e(titolo)}</h3>
        {artista}{sotto}
        {menu_html}
        {extra}
        {prenota}
      </div>
    </article>'''


def jsonld(s, lingua):
    L = TESTI[lingua]
    tz = ZoneInfo("Europe/Rome")
    if s.get("ora"):
        inizio = dt.datetime.fromisoformat(f'{s["data"]}T{s["ora"]}').replace(tzinfo=tz).isoformat()
        # fine: "ora_fine" se indicata, altrimenti chiusura cucina (23:30)
        fine = dt.datetime.fromisoformat(f'{s["data"]}T{s.get("ora_fine", "23:30")}').replace(tzinfo=tz).isoformat()
    else:
        inizio = fine = s["data"]
    titolo = tr(s, "titolo", lingua)
    ev = {
        "@context": "https://schema.org", "@type": "Event",
        "name": titolo + (f' – {s["artista"]}' if s.get("artista") else ""),
        "startDate": inizio, "endDate": fine, "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {"@type": "Restaurant", "name": "Casa Rosebery",
                     "address": {"@type": "PostalAddress", "streetAddress": "Via Ferdinando Russo 13",
                                 "postalCode": "80123", "addressLocality": "Napoli", "addressCountry": "IT"}},
        "organizer": {"@type": "Organization", "name": "Casa Rosebery", "url": L["url"]},
    }
    descr = tr(s, "sottotitolo", lingua) or L["descr_default"].format(t=titolo)
    if s.get("prezzo") and s.get("menu"):
        descr += L["menu_fisso"].format(p=s["prezzo"])
    ev["description"] = descr
    # "offers" sempre presente (Search Console lo segnala se manca):
    # menu fisso = prezzo a persona; serata alla carta = ingresso libero (price 0)
    ev["offers"] = {"@type": "Offer", "price": s["prezzo"] if s.get("prezzo") else "0", "priceCurrency": "EUR",
                    "url": L["url"] + "#serate", "availability": "https://schema.org/InStock"}
    if not s.get("prezzo"):
        ev["offers"]["description"] = ("Ingresso libero, menu alla carta" if lingua == "it"
                                       else "Free entry, à la carte menu")
    if s.get("prenotabile_dal"):
        ev["offers"]["validFrom"] = s["prenotabile_dal"]
    if s.get("foto"):
        ev["image"] = f"{SITO}/" + s["foto"]
    if s.get("artista"):
        ev["performer"] = {"@type": "Person", "name": s["artista"]}
    return json.dumps(ev, ensure_ascii=False)


def blocco(lingua):
    L = TESTI[lingua]
    if not serate:
        return f"{INIZIO}\n{FINE}"
    return f'''{INIZIO}
<section class="section-serate" id="serate">
  <div class="section-header">
    <span class="section-eyebrow">{L["eyebrow"]}</span>
    <h2 class="section-title">{L["titolo"]}</h2>
    <p class="serate-intro">{L["intro"]}</p>
  </div>
  <div class="serate-lista">{"".join(carta(s, lingua) for s in serate)}
  </div>
</section>
{"".join(f'<script type="application/ld+json">{jsonld(s, lingua)}</script>' for s in serate if s.get("pubblica"))}
<script>
// nasconde le serate già passate e, se non ne resta nessuna, l'intera sezione;
// segna con un'etichetta la serata di stasera e quella di domani
(function () {{
  var oggi = new Date(); oggi.setHours(0, 0, 0, 0);
  var GIORNO = 86400000, vis = 0;
  document.querySelectorAll('.serata[data-data]').forEach(function (s) {{
    var d = new Date(s.getAttribute('data-data') + 'T00:00:00');
    if (d < oggi) {{ s.remove(); return; }}
    vis++;
    var diff = Math.round((d - oggi) / GIORNO);
    var quando = s.querySelector('.serata-quando');
    if (diff <= 1 && quando) {{
      var tag = document.createElement('span');
      tag.className = 'serata-oggi';
      tag.textContent = diff === 0 ? '{L["oggi"]}' : '{L["domani"]}';
      quando.insertBefore(tag, quando.firstChild);
    }}
  }});
  if (!vis) {{ var sec = document.getElementById('serate'); if (sec) sec.remove(); }}
}})();
</script>
{FINE}'''


for lingua, L in TESTI.items():
    f = L["file"]
    if not f.exists():
        continue
    testo = f.read_text(encoding="utf-8")
    a, b = testo.index(INIZIO), testo.index(FINE) + len(FINE)
    testo = testo[:a] + blocco(lingua) + testo[b:]
    # il link "Serate & Eventi" del menu punta alle serate solo se ce ne sono
    if serate:
        testo = testo.replace(f'href="#eventi">{L["nav"]}', f'href="#serate">{L["nav"]}')
    else:
        testo = testo.replace(f'href="#serate">{L["nav"]}', f'href="#eventi">{L["nav"]}')
    f.write_text(testo, encoding="utf-8")
    print(f"{f.relative_to(RADICE)}: {len(serate)} serate inserite" + (" (ANTEPRIMA, non pubblicare)" if ANTEPRIMA else ""))
