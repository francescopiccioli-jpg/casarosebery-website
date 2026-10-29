#!/usr/bin/env python3
"""Menu impaginato (PDF A4) + scheda di verifica allergeni per la cucina.
Fonte piatti: menu-src/menu.json del sito. Allergeni: quelli del menu dell'8/10 + proposte da verificare."""
import json, sys, html
from pathlib import Path

SITO = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1])
BOZZA = "--definitivo" not in sys.argv
EN = "--en" in sys.argv  # versione inglese (testi *_en di menu.json)
def tr(o, k, d=""):
    return (o.get(k + "_en") or o.get(k, d)) if EN else o.get(k, d)
X = {"perc": "Tasting menu", "pp": "per person · minimum 2 guests · drinks not included", "carta": "À la carte",
     "gf": "gluten free", "unita": " /100 g", "sotto": "Champagne bar · Restaurant · Steakhouse · Naples",
     "all": "Allergens", "all1": "The numbers next to each dish indicate the allergens present under EU Regulation No 1169/2011.",
     "all2": "If you have any allergy or intolerance, please tell our staff before ordering: some dishes are prepared where other allergens are present and cross-contamination cannot be ruled out."} if EN else \
    {"perc": "Percorso degustazione", "pp": "a persona · minimo 2 persone · bevande escluse", "carta": "Alla carta",
     "gf": "senza glutine", "unita": " /etto", "sotto": "Champagneria · Ristorante · Braceria · Napoli",
     "all": "Allergeni", "all1": "I numeri accanto ai piatti indicano gli allergeni presenti secondo il Regolamento UE n. 1169/2011.",
     "all2": "Per allergie o intolleranze chiedi al nostro personale prima di ordinare: alcune preparazioni avvengono in ambienti dove sono presenti altri allergeni e non possiamo escludere contaminazioni."}
e = html.escape
M = json.loads((SITO / "menu-src/menu.json").read_text(encoding="utf-8"))

LEGENDA_EN = ["Cereals containing gluten", "Crustaceans", "Eggs", "Fish", "Peanuts", "Soybeans", "Milk", "Nuts",
              "Celery", "Mustard", "Sesame seeds", "Sulphites (> 10 mg/kg)", "Lupin", "Molluscs"]
LEGENDA = ["Cereali con glutine", "Crostacei", "Uova", "Pesce", "Arachidi", "Soia", "Latte", "Frutta a guscio",
           "Sedano", "Senape", "Sesamo", "Solfiti (> 10 mg/kg)", "Lupini", "Molluschi"]

# (piatto) -> (proposta, motivo). Chiave: nome nel menu. "" = nessun allergene.
# Solo le voci che cambiano o mancano; le altre restano come nel menu dell'8 ottobre.
PROPOSTE = {
    "Ciabatta Mediterraneo": ("1,4,7,9,10", "aggiunto 7: la stracciatella di bufala contiene latte"),
    "Rosebery": ("1,7,9,12", "aggiunto 7: la provola contiene latte"),
    "Gran crudo in cinque consistenze": ("1,3,6,7,12", "stracciata di bufala = latte (7, non 5); la salsa teriyaki di solito contiene salsa di soia con frumento (1, 6)"),
    "Carpaccio di Wagyu Giappone": ("", "nel menu era indicato 5 (arachidi): verificare se c'è un condimento con arachidi, altrimenti nessun allergene"),
    "Carpaccio di Creekstone Farms": ("", "nel menu era indicato 5 (arachidi): verificare la salsa acidula (spesso senape = 10 o solfiti = 12)"),
    "Tartare al naturale": ("9,12", "mancava: la giardiniera di solito contiene sedano (9) e aceto (12)"),
    "Tagliere salumi e formaggi": ("1,7,12", "formaggi = latte (7, non 5); servito con pane caldo (1)"),
    "Formaggi (al pezzo)": ("7,12", "formaggi = latte (7, non 5)"),
    "Nerano": ("1,7", "mancava: spaghetti (1) e provolone del Monaco (7)"),
    "Stinco di maiale al forno": ("1,12", "aggiunto 1: la riduzione alla birra contiene orzo/glutine"),
    "Misto brace (per due persone)": ("", "mancava: verificare ingredienti della salsiccia e il contorno"),
    "Brisket Casa Rosebery": ("7", "mancava: purea di patate con burro e provola (7); verificare eventuale salsa o marinatura"),
    "Purè di patate (metodo francese)": ("7", "mancava: burro d'alpeggio (7)"),
    "Tortino al cioccolato fondente": ("1,3,7", "mancava: di solito farina, uova e burro; verificare se senza glutine come gli altri dolci"),
}
# tagli alla brace, contorni senza latticini, bevande: nessun allergene (da confermare)
NESSUNO_SEZ = {"Dalla brace", "Bevande"}
NESSUNO_PIATTI = {"Scarola saltata", "Le nostre patate stick artigianali", "Patate al forno alla paprika", "Verdure grigliate di stagione"}
# percorsi: stessi allergeni del piatto alla carta; voci proprie dei percorsi
PERCORSO_PROPRI = {
    "Fassona Piemontese 80 g": ("", "tartare al naturale, senza condimenti"),
    "Wagyu Giapponese A5 80 g": ("", "tartare al naturale, senza condimenti"),
    "Manzetta Prussiana 100 g": ("1", "mini hamburger: pane (1); verificare sesamo (11) sul pane e salse"),
    "Entrecôte Argentina": ("", "carne alla brace; verificare il contorno di stagione"),
    "Ribeye Canada": ("", "carne alla brace; verificare il contorno di stagione"),
    "Maiale affumicato a legno di ciliegio": ("", "carne affumicata; verificare il contorno di stagione"),
}

if not BOZZA:  # allergeni verificati: si usano quelli di menu.json così come sono
    PROPOSTE, NESSUNO_SEZ, NESSUNO_PIATTI, PERCORSO_PROPRI = {}, set(), set(), {}
carta = {}
for s in M["sezioni"]:
    for p in s["piatti"]:
        carta[p["nome"]] = (s["titolo"], p)

verifica = []  # (sezione, piatto, attuale, proposta, motivo)


def allerg(nome, sez, attuale):
    if nome in PROPOSTE:
        prop, mot = PROPOSTE[nome]
    elif sez in NESSUNO_SEZ or nome in NESSUNO_PIATTI:
        prop, mot = "", "nessun allergene atteso (" + ("carne alla brace" if sez == "Dalla brace" else "ingredienti indicati") + ")"
    else:
        return attuale or ""
    verifica.append((sez, nome, attuale or "—", prop or "nessuno", mot))
    return prop


def numeri(a):
    return f'<span class="all">{" ".join(a.split(","))}</span>' if a else ""


def prezzo(v, unita=""):
    return f"€ {e(v)}{e(unita)}" if v else ""


# allergeni finali dei piatti alla carta (una sola voce di verifica per piatto)
FINAL = {}
for s_ in M["sezioni"]:
    for p_ in s_["piatti"]:
        FINAL[p_["nome"]] = allerg(p_["nome"], s_["titolo"], p_.get("all", ""))

# ── percorsi
perc_html = ""
for pc in M["percorsi"]:
    righe = ""
    for po in pc["portate"]:
        righe += f'<h4 class="portata">{e(tr(po, "titolo"))}</h4>'
        if po.get("nota"):
            righe += f'<p class="nota-p">{e(tr(po, "nota"))}</p>'
        for p in po["piatti"]:
            n = p["nome"]
            base = n.replace("Locena di maiale CBT", "Locena di maiale")
            if n in carta:
                a = FINAL[n]
                a_attuale = p.get("all", "")
                if a_attuale != a:
                    verifica.append((f"Percorso {pc['nome']}", n, a_attuale or "—", a or "nessuno", "allineato al piatto alla carta"))
            elif n in PERCORSO_PROPRI:
                a, mot = PERCORSO_PROPRI[n]
                verifica.append((f"Percorso {pc['nome']}", n, p.get("all", "") or "—", a or "nessuno", mot))
            else:
                a = p.get("all", "")
            righe += f'<div class="pp"><b>{e(tr(p, "nome"))}{numeri(a)}</b><span>{e(tr(p, "desc"))}</span></div>'
    perc_html += f'''<div class="pagina"><div class="cont"><section class="percorso"><p class="occhiello">{X["perc"]}</p><h3>{e(pc["nome"])}</h3>
      <p class="prezzo-p">€ {e(pc["prezzo"])} <small>{X["pp"]}</small></p>{righe}</section></div></div>'''

# ── carta: una sezione per blocco, poi pagine bilanciate
blocchi = []
for s in M["sezioni"]:
    tit = tr(s, "titolo")
    unita = X["unita"] if s.get("unita") else ""
    voci = ""
    for p in s["piatti"]:
        a = FINAL[p["nome"]]
        gf = ' <span class="gf">{X["gf"]}</span>' if p.get("senza_glutine") else ""
        desc = f'<span class="d">{e(tr(p, "desc"))}</span>' if p.get("desc") else ""
        voci += f'<div class="voce"><div class="r"><b>{e(tr(p, "nome"))}{numeri(a)}{gf}</b><i></i><em>{prezzo(p.get("prezzo"), unita)}</em></div>{desc}</div>'
    blocchi.append((tit, tr(s, "sotto") or None, voci))
GRUPPI = [[0, 1], [2, 3], [4, 5], [6], [7, 8], [9, 10]]
assert sorted(sum(GRUPPI, [])) == list(range(len(blocchi))), "aggiornare GRUPPI: sono cambiate le sezioni del menu"
pagine_carta = []
for gi, g_ in enumerate(GRUPPI):
    h = f'<p class="occhiello">{X["carta"]}</p>' if gi == 0 else ""
    prec = None
    for i in g_:
        tit, sotto, voci = blocchi[i]
        h += (f'<h2>{e(tit)}</h2>' if tit != prec else "") + (f'<p class="sotto">{e(sotto)}</p>' if sotto else "") + voci
        prec = tit
    pagine_carta.append(h)

leg = "".join(f"<li><b>{i}</b> {e(t)}</li>" for i, t in enumerate(LEGENDA_EN if EN else LEGENDA, 1))
banda = ""
logo = (SITO / "logo.png").as_uri()

HTML = f'''<!doctype html><html lang="{"en" if EN else "it"}"><head><meta charset="utf-8"><style>
@page {{ size:A4; margin:0 0 9mm 0; }}
.pagina {{ width:210mm; height:288mm; padding:14mm 18mm 8mm; display:flex; flex-direction:column; justify-content:center; break-after:page; overflow:hidden; }}
.pagina:last-child {{ break-after:auto; }}
.cont {{ width:100%; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Inter, sans-serif; font-weight:300; color:#1a1208; font-size:9.6pt; line-height:1.45; }}
.bozza {{ position:fixed; top:-12mm; left:0; right:0; text-align:center; font-size:7.5pt; letter-spacing:2px; color:#a3412b; text-transform:uppercase; }}
.cover {{ text-align:center; }}
.cover img {{ width:62mm; }}
.cover h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:34pt; margin-top:14mm; letter-spacing:2px; }}
.cover p {{ color:#6f6656; margin-top:4mm; letter-spacing:3px; text-transform:uppercase; font-size:8pt; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:21pt; text-align:center; margin:9mm 0 3mm; break-after:avoid; }}
h2::after {{ content:''; display:block; width:12mm; height:.4mm; background:#b8923a; margin:2.5mm auto 0; }}
.sotto {{ text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-size:12.5pt; color:#8a6d2c; margin:3mm 0 1mm; break-after:avoid; }}
h2:first-child, .occhiello + h2 {{ margin-top:2mm; }}
.cont > .occhiello {{ text-align:center; }}
.voce {{ padding:2.2mm 0; border-bottom:.2mm solid #e8e0d0; break-inside:avoid; }}
.r {{ display:flex; align-items:baseline; gap:2mm; }}
.r b {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; }}
.r i {{ flex:1; border-bottom:.25mm dotted #c9bfa9; transform:translateY(-1mm); }}
.r em {{ font-style:normal; font-weight:500; white-space:nowrap; }}
.d {{ display:block; color:#5d5446; font-size:8.8pt; margin-top:.6mm; }}
.all {{ font-family:Inter,sans-serif; font-weight:500; font-size:6.8pt; color:#b8923a; margin-left:1.5mm; letter-spacing:.5px; vertical-align:super; }}
.gf {{ font-family:Inter,sans-serif; font-size:6.5pt; letter-spacing:1px; text-transform:uppercase; color:#4f7a52; border:.2mm solid #4f7a52; padding:0 1mm; margin-left:1.5mm; vertical-align:middle; }}
.percorso {{ border:.3mm solid #b8923a; padding:11mm 10mm 10mm; text-align:center; }}
.occhiello {{ font-size:7.5pt; letter-spacing:3px; text-transform:uppercase; color:#8a6d2c; }}
.percorso h3 {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:24pt; margin:1mm 0; }}
.prezzo-p {{ font-family:'Cormorant Garamond',serif; font-size:15pt; }}
.prezzo-p small {{ display:block; font-family:Inter,sans-serif; font-size:7.5pt; color:#6f6656; letter-spacing:1px; }}
.portata {{ font-size:7.5pt; letter-spacing:2.5px; text-transform:uppercase; color:#8a6d2c; margin:5mm 0 1mm; }}
.nota-p {{ font-size:8pt; color:#6f6656; font-style:italic; }}
.pp {{ margin:1.8mm auto; max-width:140mm; }}
.pp b {{ display:block; font-family:'Cormorant Garamond',serif; font-weight:600; font-size:13pt; }}
.pp span {{ color:#5d5446; font-size:8.6pt; }}
.info ol {{ list-style:none; columns:2; column-gap:10mm; margin-top:4mm; }}
.info li {{ padding:1.2mm 0; border-bottom:.2mm solid #e8e0d0; }}
.info li b {{ display:inline-block; width:7mm; color:#b8923a; }}
.info p {{ margin-top:5mm; color:#5d5446; text-align:center; }}
</style></head><body>{banda}
<div class="pagina"><div class="cont cover"><img src="{logo}" alt="Casa Rosebery"><h1>Menu</h1><p>{X["sotto"]}</p><p>{e(tr(M, "aggiornato"))}</p></div></div>
{perc_html}
{"".join(f'<div class="pagina"><div class="cont">{h}</div></div>' for h in pagine_carta)}
<div class="pagina"><div class="cont info"><h2>{X["all"]}</h2>
<p>{X["all1"]}</p>
<ol>{leg}</ol>
<p>{X["all2"]}</p></div></div>
<script>
// se una pagina non entra, riduce un poco quella pagina (mai sotto l'80%)
document.querySelectorAll('.pagina').forEach(function (p) {{
  var c = p.querySelector('.cont'), z = 1, max = p.clientHeight - 22 * 3.78;
  while (c.scrollHeight * z > max && z > 0.8) {{ z -= 0.02; c.style.zoom = z; }}
  // i percorsi (pagine corte) si ingrandiscono fino a riempire bene la pagina, al massimo +30%
  if (c.querySelector('.percorso')) {{ while (c.scrollHeight * (z + 0.02) < max * 0.86 && z < 1.3) {{ z += 0.02; c.style.zoom = z; }} }}
}});
</script>
</body></html>'''
(OUT / ("menu_en.html" if EN else "menu.html")).write_text(HTML, encoding="utf-8")

# ── scheda di verifica
righe = "".join(f"<tr><td>{e(a)}</td><td><b>{e(b)}</b></td><td>{e(c)}</td><td class='p'>{e(d)}</td><td>{e(m)}</td><td class='ok'>☐ ok&nbsp;&nbsp; correzione: ________</td></tr>"
                for a, b, c, d, m in verifica)
leg2 = " · ".join(f"{i} {t}" for i, t in enumerate(LEGENDA, 1))
V = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
@page {{ size:A4 landscape; margin:12mm; }}
body {{ font-family:Inter,sans-serif; font-size:8.6pt; color:#1a1208; }}
h1 {{ font-family:'Cormorant Garamond',serif; font-size:20pt; font-weight:600; }}
p {{ margin:2mm 0 4mm; color:#5d5446; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ border:.2mm solid #d8cfbc; padding:1.6mm 2mm; text-align:left; vertical-align:top; }}
th {{ background:#f3eee3; font-size:7.5pt; letter-spacing:1px; text-transform:uppercase; }}
td.p {{ font-weight:600; color:#8a5a12; white-space:nowrap; }}
td.ok {{ white-space:nowrap; width:48mm; }}
tr {{ break-inside:avoid; }}
</style></head><body>
<h1>Verifica allergeni · menu {e(M.get("aggiornato", ""))}</h1>
<p>Solo i piatti da controllare: allergeni mancanti, numeri incoerenti tra percorsi e carta, o indicati con il 5 (arachidi) dove il piatto sembra contenere latte (7). Gli altri piatti restano come nel menu dell'8 ottobre.<br>Legenda UE 1169/2011: {leg2}.</p>
<table><thead><tr><th>Sezione</th><th>Piatto</th><th>Oggi</th><th>Proposta</th><th>Motivo</th><th>Cucina</th></tr></thead><tbody>{righe}</tbody></table>
</body></html>'''
(OUT / "verifica.html").write_text(V, encoding="utf-8")
print(len(verifica), "voci da verificare")
