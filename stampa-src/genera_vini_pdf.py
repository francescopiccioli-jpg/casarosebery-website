#!/usr/bin/env python3
"""Carta dei vini impaginata per la stampa, dalla stessa fonte del sito (vini-src/vini.json).

Uso (dalla cartella del sito):
  python3 stampa-src/genera_vini_pdf.py <cartella>          # raccoglitore 23x30, dorso a viti
  python3 stampa-src/genera_vini_pdf.py <cartella> --web    # A4 simmetrico
  node stampa-src/pdf.js <cartella> --vini [--web]
Ordine come sul sito: Bollicine, Rossi, Bianchi (esteri in coda), Rosati; Campania prima delle altre regioni.
"""
import json, sys, html
from pathlib import Path

SITO = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1])
WEB = "--web" in sys.argv
e = html.escape
D = json.loads((SITO / "vini-src/vini.json").read_text(encoding="utf-8"))

SEZIONI = [("bollicine", "Bollicine"), ("rossi", "Rossi"), ("bianchi", "Bianchi"), ("rosati", "Rosati")]
UNISCI = {"bianchi-estero": "bianchi"}


def regioni(vini):
    ordine = []
    for v in vini:
        if v["regione"] not in ordine:
            ordine.append(v["regione"])
    if "Campania" in ordine:
        ordine.remove("Campania")
        ordine.insert(0, "Campania")
    # gli esteri dopo le regioni italiane
    esteri = [r for r in ordine if any(v["regione"] == r and v["sez"] == "bianchi-estero" for v in vini)]
    return [r for r in ordine if r not in esteri] + esteri


def prezzo(p):
    p = str(p or "").strip()
    return f"€ {e(p)}" if p else ""


corpo = []
for sid, titolo in SEZIONI:
    vini = [v for v in D["vini"] if UNISCI.get(v["sez"], v["sez"]) == sid]
    if not vini:
        continue
    blocchi = []
    for reg in regioni(vini):
        righe = "".join(
            f'<div class="voce"><div class="r"><b>{e(v["nome"])}</b><i></i><em>{prezzo(v.get("prezzo"))}</em></div>'
            + (f'<span class="d">{e(v["produttore"])}</span>' if v.get("produttore") else "")
            + "</div>"
            for v in vini if v["regione"] == reg)
        blocchi.append(f'<div class="regione"><h3>{e(reg)}</h3>{righe}</div>')
    corpo.append(f'<section class="sez"><h2>{e(titolo)}</h2>{"".join(blocchi)}</section>')

n = len(D["vini"])
logo = (SITO / "logo.png").as_uri()
if WEB:
    PAGINA = "@page { size:210mm 297mm; margin:18mm 18mm 20mm; }"
else:
    # raccoglitore 23x30 con fascia a viti di 2,5 cm sul dorso: margine interno 38 mm, esterno 14 mm
    PAGINA = ("@page { size:230mm 300mm; margin:16mm 14mm 20mm 38mm; }\n"
              "@page :left { margin:16mm 38mm 20mm 14mm; }")

HTML = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
{PAGINA}
@page :first {{ margin-bottom:16mm; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Inter, sans-serif; font-weight:300; color:#1a1208; font-size:9.4pt; line-height:1.4; }}
.cover {{ height:{"259" if WEB else "268"}mm; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; break-after:page; }}
.cover img {{ width:62mm; }}
.cover h1 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:34pt; margin-top:14mm; letter-spacing:2px; }}
.cover p {{ color:#6f6656; margin-top:4mm; letter-spacing:3px; text-transform:uppercase; font-size:8pt; }}
.sez {{ break-before:page; }}
.sez:first-of-type {{ break-before:auto; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:400; font-size:24pt; text-align:center; margin:2mm 0 2mm; break-after:avoid; }}
h2::after {{ content:''; display:block; width:12mm; height:.4mm; background:#b8923a; margin:2.5mm auto 0; }}
h3 {{ font-size:7.5pt; letter-spacing:3px; text-transform:uppercase; color:#8a6d2c; font-weight:500; margin:7mm 0 1mm; break-after:avoid; }}
.voce {{ padding:1.7mm 0; border-bottom:.2mm solid #e8e0d0; break-inside:avoid; }}
.r {{ display:flex; align-items:baseline; gap:2mm; }}
.r b {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12pt; }}
.r i {{ flex:1; border-bottom:.25mm dotted #c9bfa9; transform:translateY(-1mm); min-width:6mm; }}
.r em {{ font-style:normal; font-weight:500; white-space:nowrap; }}
.d {{ display:block; color:#5d5446; font-size:8.4pt; margin-top:.4mm; }}
.nota {{ margin-top:8mm; text-align:center; color:#6f6656; font-size:8pt; }}
</style></head><body>
<div class="cover"><img src="{logo}" alt="Casa Rosebery"><h1>Carta dei vini</h1><p>Champagneria · Ristorante · Braceria · Napoli</p><p>{n} etichette · {e(D.get("aggiornato", ""))}</p></div>
{"".join(corpo)}
<p class="nota">Prezzi a bottiglia. Annate e disponibilità possono variare: chiedi al nostro personale.</p>
</body></html>'''
(OUT / "vini.html").write_text(HTML, encoding="utf-8")
print(n, "vini")
