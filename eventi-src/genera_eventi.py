"""Inserisce in index.html la sezione "Prossime serate" a partire da eventi-src/eventi.json.

Uso (dalla cartella del repo):
  python3 eventi-src/genera_eventi.py              -> solo serate con "pubblica": true
  python3 eventi-src/genera_eventi.py --anteprima  -> include anche le bozze (NON fare commit di questo risultato)
"""
import datetime as dt
import html
import json
import pathlib
import sys
import urllib.parse
from zoneinfo import ZoneInfo

RADICE = pathlib.Path(__file__).resolve().parent.parent
INDEX = RADICE / "index.html"
INIZIO, FINE = "<!-- EVENTI:INIZIO -->", "<!-- EVENTI:FINE -->"
ANTEPRIMA = "--anteprima" in sys.argv
e = html.escape

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]

dati = json.loads((RADICE / "eventi-src" / "eventi.json").read_text(encoding="utf-8"))
oggi = dt.date.today()
serate = sorted(
    (s for s in dati["serate"]
     if (s.get("pubblica") or ANTEPRIMA) and dt.date.fromisoformat(s["data"]) >= oggi),
    key=lambda s: (s["data"], s.get("ora", "")))


def carta(s):
    d = dt.date.fromisoformat(s["data"])
    quando = f'{GIORNI[d.weekday()]} {d.day} {MESI[d.month - 1]}' + (f' · ore {e(s["ora"])}' if s.get("ora") else "")
    bozza = '' if s.get("pubblica") else '<span class="serata-bozza">BOZZA – non pubblicata</span>'
    artista = f'<p class="serata-artista">{e(s["artista"])}</p>' if s.get("artista") else ""
    sotto = f'<p class="serata-sotto">{e(s["sottotitolo"])}</p>' if s.get("sottotitolo") else ""
    portate = "".join(f'<li><b>{e(p["nome"])}</b><span>{e(p.get("desc", ""))}</span></li>' for p in s["menu"])
    integr = ""
    if s.get("integrazione"):
        i = s["integrazione"]
        integr = (f'<div class="serata-integr"><span>Integrazione · + € {e(i["prezzo"])} a persona</span>'
                  f'<b>{e(i["nome"])}</b><em>{e(i.get("desc", ""))}</em></div>')
    extra = ""
    if s.get("extra"):
        gruppi = {}
        for x in s["extra"]:
            gruppi.setdefault(x.get("gruppo", ""), []).append(x)
        blocchi = "".join(
            f'<h5>{e(g)}</h5><ul>' + "".join(
                f'<li><div><b>{e(x["nome"])}</b><span>{e(x.get("desc", ""))}</span></div><i>€ {e(x["prezzo"])}</i></li>'
                for x in xs) + '</ul>'
            for g, xs in gruppi.items())
        extra = f'<details class="serata-extra"><summary>{e(s.get("extra_titolo", "Alla carta"))}</summary>{blocchi}</details>'
    testo_wa = f"Ciao! Vorrei prenotare per la serata del {d.day} {MESI[d.month - 1]} ({s['titolo']}). Siamo in "
    wa = "https://wa.me/390813357572?text=" + urllib.parse.quote(testo_wa)
    foto = f'<div class="serata-foto" style="background-image:url(\'{e(s["foto"])}\')"></div>' if s.get("foto") else ""
    return f'''
    <article class="serata" data-data="{e(s["data"])}">
      {foto}
      <div class="serata-corpo">
        {bozza}
        <p class="serata-quando">{quando}</p>
        <h3 class="serata-titolo">{e(s["titolo"])}</h3>
        {artista}{sotto}
        <div class="serata-menu">
          <div class="serata-prezzo"><b>€ {e(s["prezzo"])}</b><span>a persona · menu fisso</span></div>
          <ul class="serata-portate">{portate}</ul>
          {integr}
        </div>
        {extra}
        <div class="serata-cta">
          <a href="https://casarosebery.plateform.app/reserve" target="_blank" rel="noopener" class="btn-gold" data-serata="{e(s["data"])}">Prenota la serata</a>
          <a href="{wa}" target="_blank" rel="noopener" class="btn-ghost serata-wa" data-serata="{e(s["data"])}">Prenota su WhatsApp</a>
        </div>
      </div>
    </article>'''


def jsonld(s):
    if s.get("ora"):
        inizio = dt.datetime.fromisoformat(f'{s["data"]}T{s["ora"]}').replace(tzinfo=ZoneInfo("Europe/Rome")).isoformat()
    else:
        inizio = s["data"]
    ev = {
        "@context": "https://schema.org", "@type": "Event",
        "name": s["titolo"] + (f' – {s["artista"]}' if s.get("artista") else ""),
        "startDate": inizio, "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {"@type": "Restaurant", "name": "Casa Rosebery",
                     "address": {"@type": "PostalAddress", "streetAddress": "Via Ferdinando Russo 13",
                                 "postalCode": "80123", "addressLocality": "Napoli", "addressCountry": "IT"}},
        "offers": {"@type": "Offer", "price": s["prezzo"], "priceCurrency": "EUR",
                   "url": "https://www.casaroseberyristorante.it/#serate", "availability": "https://schema.org/InStock"},
        "organizer": {"@type": "Organization", "name": "Casa Rosebery", "url": "https://www.casaroseberyristorante.it/"},
    }
    if s.get("foto"):
        ev["image"] = "https://www.casaroseberyristorante.it/" + s["foto"]
    if s.get("artista"):
        ev["performer"] = {"@type": "Person", "name": s["artista"]}
    return json.dumps(ev, ensure_ascii=False)


if serate:
    blocco = f'''{INIZIO}
<section class="section-serate" id="serate">
  <div class="section-header">
    <span class="section-eyebrow">In programma</span>
    <h2 class="section-title">Prossime <em>serate</em></h2>
    <p class="serate-intro">Cene a menu fisso con musica dal vivo e ospiti speciali. I posti sono limitati: prenota in anticipo.</p>
  </div>
  <div class="serate-lista">{"".join(carta(s) for s in serate)}
  </div>
</section>
{"".join(f'<script type="application/ld+json">{jsonld(s)}</script>' for s in serate if s.get("pubblica"))}
<script>
// nasconde le serate già passate e, se non ne resta nessuna, l'intera sezione
(function () {{
  var oggi = new Date(); oggi.setHours(0, 0, 0, 0);
  var vis = 0;
  document.querySelectorAll('.serata[data-data]').forEach(function (s) {{
    if (new Date(s.getAttribute('data-data') + 'T23:59:59') < oggi) s.remove(); else vis++;
  }});
  if (!vis) {{ var sec = document.getElementById('serate'); if (sec) sec.remove(); }}
}})();
</script>
{FINE}'''
else:
    blocco = f"{INIZIO}\n{FINE}"

testo = INDEX.read_text(encoding="utf-8")
a, b = testo.index(INIZIO), testo.index(FINE) + len(FINE)
testo = testo[:a] + blocco + testo[b:]
# il link "Serate & Eventi" del menu punta alle serate solo se ce ne sono
if serate:
    testo = testo.replace('href="#eventi">Serate', 'href="#serate">Serate')
else:
    testo = testo.replace('href="#serate">Serate', 'href="#eventi">Serate')
INDEX.write_text(testo, encoding="utf-8")
print(f"{len(serate)} serate inserite" + (" (ANTEPRIMA, non pubblicare)" if ANTEPRIMA else ""))
