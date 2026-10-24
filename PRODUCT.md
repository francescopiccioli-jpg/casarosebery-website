# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Un pubblico misto, con lo stesso peso:

- **Napoletani** che scelgono dove andare per una cena speciale (coppia, amici, famiglia) e tornano per le serate con musica dal vivo.
- **Turisti e visitatori** a Napoli che cercano un ristorante vista mare a Posillipo e una braceria di livello; sono serviti dalla versione inglese (`/en/`).

Un pubblico secondario chiede cene aziendali, compleanni ed eventi privati tramite il form apposito.

## Product Purpose

Il sito è la vetrina di Casa Rosebery, braceria premium e ristorante a Posillipo (Via Ferdinando Russo 13, Napoli). Racconta le due anime del locale (braceria e cucina napoletana), mostra menu, carta dei vini e serate in programma, e porta l'ospite a prenotare.

Il successo si misura in due azioni:

1. **Prenotazione del tavolo** su Plateform (`https://casarosebery.plateform.app/reserve`).
2. **Prenotazione via WhatsApp** delle serate a menu fisso, che hanno posti limitati e si prenotano solo così.

Telefono e form per eventi privati restano canali secondari.

## Positioning

Una braceria con carni da undici provenienze (Wagyu A5 di Kagoshima, Black Angus, Marchigiana, Kobe, Red Dan…) frollate nella cella di casa e vendute all'etto, insieme a una cucina napoletana rivisitata con il flambé al tavolo. Tutto questo a Posillipo, con vista sul Golfo, a pochi passi da Villa Rosebery (da cui viene il nome), con parcheggio gratuito e riservato e fuori dalla ZTL.

## Operating Context

- I visitatori arrivano soprattutto da telefono (Instagram, Google, TripAdvisor, link condivisi); il layout parte dal mobile.
- Le serate cambiano ogni settimana: musica dal vivo ogni sabato più serate speciali con artisti e menu fisso (prezzo a persona, integrazioni, grill alla carta, dolci).
- Menu e carta dei vini cambiano con le stagioni; la sera di un evento il menu può passare a una "vista serata" ridotta.
- Lingue: italiano principale, inglese secondario. Se manca un testo `_en`, la pagina inglese mostra quello italiano.

## Capabilities and Constraints

- **Stack:** HTML/CSS statico scritto a mano, nessun framework. Pagine: `index.html`, `menu.html`, `vini.html`, `privacy.html`, `en/`.
- **Contenuti generati da JSON tramite script Python:** `menu-src/` (menu.json, vista_serata.json), `vini-src/`, `eventi-src/` (eventi.json; le serate passate spariscono da sole, `pubblica: false` le nasconde), `en-src/`. Le modifiche ai contenuti si fanno nel JSON, poi si rigenera l'HTML; non si modifica a mano l'HTML generato.
- **Deploy:** GitHub Actions carica via FTP su hosting Aruba a ogni push su `main` (solo i file cambiati, nessuna cancellazione). `.htaccess` gestisce le intestazioni di sicurezza.
- **Analytics:** Google Analytics caricato solo dopo il consenso cookie; la chiave di consenso è condivisa tra home, menu e vini (`js/analytics.js`).
- **Dati strutturati:** JSON-LD `Restaurant` in homepage (orari, indirizzo, link di prenotazione, menu). Va tenuto allineato al contenuto visibile.
- **Orari:** cena lun–sab 19:30–23:30; pranzo sab–dom 12:30–15:30.
- **Immagini:** foto reali in `img/` (JPG + WebP); foto degli artisti in `img/eventi/`. Nell'ambiente non c'è un convertitore di immagini.

## Brand Commitments

- **Nome:** Casa Rosebery. Società: Nado Advertising S.r.l., P.IVA 07284940488.
- **Loghi:** `logo.png`, `logo-chiaro.png`, le favicon.
- **Voce:** italiano caldo e misurato, un po' evocativo ("La brace come arte", "pochi gesti, nessuna scorciatoia"), concreto su provenienze, frollatura e prezzi.
- **Struttura del racconto:** due anime, Braceria (I) e Ristorante/Cucina (II).
- **Contatti ufficiali:** 081 335 7572 · prenotazioni@casaroseberyristorante.it · Instagram @casarosebery · Facebook · TripAdvisor.

## Evidence on Hand

- **Recensioni:** le tre citazioni in homepage (Google e TripAdvisor, 2025–2026) sono reali e testuali, confermate dal titolare. Valutazione Google mostrata: 4.8/5.
- **Prova social:** conteggio follower Instagram mostrato in pagina (4.716 follower · 112 post); è un dato statico che invecchia.
- **Foto:** circa 38 foto reali del locale, dei piatti, della brace e di Posillipo in `img/`.
- **Contenuti reali:** menu, oltre 160 etichette in carta dei vini, prezzi dei tagli e dei percorsi, programma delle serate con biografie degli artisti.
- **Da non inventare:** recensioni, premi, stampa, numero di coperti, nomi dello chef o dello staff, o altri dati che non sono già nel sito.
- **Nomi dei piatti (testi alternativi delle foto, didascalie, descrizioni):** un piatto si nomina solo con il nome identico a una voce di `menu-src/menu.json`. In italiano si usa il campo `nome`; in inglese `nome_en` oppure, se manca, lo stesso `nome`. Se la foto non corrisponde con certezza a una voce del menu, si usa una descrizione generica senza nome del piatto (es. "Piatto di carne con salsa").

## Product Principles

1. **Prenotare per primo.** Ogni pagina porta in uno o due tocchi a Plateform (tavolo) o a WhatsApp (serate a menu fisso). Gli altri contenuti sostengono questa scelta.
2. **Specifico, mai generico.** Provenienze, grammature, prezzi all'etto, nomi dei piatti e degli artisti convincono più di qualsiasi aggettivo.
3. **Il luogo è parte del piatto.** Posillipo, il Golfo e Villa Rosebery sono fatti, non decorazione: raccontali con foto vere.
4. **Contenuti vivi e affidabili.** Serate, menu e vini cambiano spesso: passano dal JSON, e quello che è scaduto sparisce invece di restare in pagina.
5. **Due lingue, un solo locale.** Il turista in inglese ha le stesse informazioni e le stesse strade per prenotare del cliente napoletano.

## Accessibility & Inclusion

Nessuno standard formale è stato richiesto. Il codice esistente cura già i target touch di almeno 44px, i testi `sr-only`, il contrasto (vedi il commit "Qualità: leggibilità, contrasto") e il consenso cookie conforme al GDPR.
