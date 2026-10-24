"""Genera la home inglese en/index.html a partire da index.html (italiano).

Uso (dalla cartella del repo):  python3 en-src/genera_en.py
Va rilanciato ogni volta che si modifica index.html (testi, foto, orari...).
Le serate in inglese le inserisce genera_eventi.py (chiamato in fondo a questo script).

Se si cambia un testo italiano qui sotto elencato, lo script si ferma e indica la frase
da aggiornare: così la versione inglese non resta mai indietro senza che ce ne accorgiamo.
"""
import pathlib
import re
import subprocess
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://www.casaroseberyristorante.it"

# (italiano, inglese) — ogni frase italiana deve comparire in index.html
T = [
    # ── <head> ──
    ('<html lang="it">', '<html lang="en">'),
    ('content="Casa Rosebery, braceria e ristorante a Posillipo, a due passi da Marechiaro: carni pregiate alla brace da tutto il mondo, cucina della tradizione napoletana e vista sul Golfo di Napoli. Prenota il tuo tavolo."',
     'content="Casa Rosebery, steakhouse and restaurant in Posillipo, steps from Marechiaro: prime cuts from around the world grilled over embers, traditional Neapolitan cuisine and views over the Bay of Naples. Book your table."'),
    ('content="ristorante Posillipo Napoli, braceria Napoli, ristorante fine dining Napoli, carne alla brace Napoli, ristorante vista mare Napoli, steakhouse Napoli, wagyu Napoli, braceria premium Napoli"',
     'content="restaurant Posillipo Naples, steakhouse Naples, fine dining Naples, grill restaurant Naples, sea view restaurant Naples, wagyu Naples, best steak Naples, Neapolitan cuisine"'),
    ('<meta property="og:title" content="Casa Rosebery — Braceria & Ristorante Fine Dining · Posillipo, Napoli">',
     '<meta property="og:title" content="Casa Rosebery — Steakhouse & Fine Dining Restaurant · Posillipo, Naples">'),
    ('<meta property="og:description" content="Braceria premium e ristorante fine dining a Posillipo. Carni pregiate da tutto il mondo, cucina della tradizione napoletana e vista sul Golfo di Napoli.">',
     '<meta property="og:description" content="Premium steakhouse and fine dining restaurant in Posillipo. Prime cuts from around the world, traditional Neapolitan cuisine and views over the Bay of Naples.">'),
    (f'<meta property="og:url" content="{SITO}/">', f'<meta property="og:url" content="{SITO}/en/">'),
    ('<meta property="og:locale" content="it_IT">', '<meta property="og:locale" content="en_GB">\n<meta property="og:locale:alternate" content="it_IT">'),
    ('<meta name="twitter:title" content="Casa Rosebery — Braceria & Ristorante · Napoli">',
     '<meta name="twitter:title" content="Casa Rosebery — Steakhouse & Restaurant · Naples">'),
    ('<meta name="twitter:description" content="Braceria premium e ristorante fine dining a Posillipo, Napoli.">',
     '<meta name="twitter:description" content="Premium steakhouse and fine dining restaurant in Posillipo, Naples.">'),
    (f'<link rel="canonical" href="{SITO}/">', f'<link rel="canonical" href="{SITO}/en/">'),
    ('"description": "Braceria premium e ristorante fine dining a Posillipo, Napoli. Carni pregiate da tutto il mondo, cucina della tradizione napoletana e vista sul Golfo.",',
     '"description": "Premium steakhouse and fine dining restaurant in Posillipo, Naples. Prime cuts from around the world, traditional Neapolitan cuisine and views over the Bay.",'),
    ('"servesCuisine": ["Italiana", "Napoletana", "Braceria", "Steakhouse"],', '"servesCuisine": ["Italian", "Neapolitan", "Steakhouse", "Grill"],'),
    (f'"menu": "{SITO}/#menu",', f'"menu": "{SITO}/en/menu.html",'),
    ('<h1 class="sr-only">Casa Rosebery — Braceria e ristorante vista mare a Posillipo, Napoli</h1>',
     '<h1 class="sr-only">Casa Rosebery — Steakhouse and sea-view restaurant in Posillipo, Naples</h1>'),
    ('{"@type": "LocationFeatureSpecification", "name": "Parcheggio gratuito", "value": true},',
     '{"@type": "LocationFeatureSpecification", "name": "Free parking", "value": true},'),
    ('{"@type": "LocationFeatureSpecification", "name": "Vista mare", "value": true}',
     '{"@type": "LocationFeatureSpecification", "name": "Sea view", "value": true}'),
    ('<title>Casa Rosebery — Braceria e Ristorante vista mare · Posillipo, Marechiaro (Napoli)</title>',
     '<title>Casa Rosebery — Steakhouse & Sea-View Restaurant · Posillipo, Marechiaro (Naples)</title>'),

    # ── nav ──
    ('<a href="/en/" class="nav-lang" hreflang="en" lang="en" title="English version">EN</a>',
     '<a href="/" class="nav-lang" hreflang="it" lang="it" title="Versione italiana">IT</a>'),
    ('alt="Casa Rosebery — Champagneria, Ristorante, Braceria · Napoli"', 'alt="Casa Rosebery — Champagne bar, Restaurant, Steakhouse · Naples"'),
    ('<li><a href="#anime">Il Ristorante</a></li>', '<li><a href="#anime">The Restaurant</a></li>'),
    ('<li><a href="#storia">La Nostra Storia</a></li>', '<li><a href="#storia">Our Story</a></li>'),
    ('<li><a href="#serate">Serate & Eventi</a></li>', '<li><a href="#serate">Live Music & Events</a></li>'),
    ('<li><a href="#eventi">Serate & Eventi</a></li>', '<li><a href="#eventi">Live Music & Events</a></li>'),
    ('<li><a href="#recensioni">Recensioni</a></li>', '<li><a href="#recensioni">Reviews</a></li>'),
    ('<li><a href="#contatti">Contatti</a></li>', '<li><a href="#contatti">Contact</a></li>'),
    ('class="nav-cta" target="_blank">Prenota</a>', 'class="nav-cta" target="_blank">Book</a>'),

    # ── hero ──
    ('<span class="hero-eyebrow">Braceria Premium</span>', '<span class="hero-eyebrow">Premium Steakhouse</span>'),
    ('<h2 class="hero-title">La brace<br>come <em>arte</em></h2>', '<h2 class="hero-title">The grill<br>as an <em>art</em></h2>'),
    ('Carni pregiate da tutto il mondo, frollature studiate, cotture millimetriche. La Braceria di Casa Rosebery è un rito.',
     'Prime cuts from around the world, carefully dry-aged and cooked to the minute. The Casa Rosebery Steakhouse is a ritual.'),
    ('class="btn-ghost">Scopri la Braceria</a>', 'class="btn-ghost">Discover the Steakhouse</a>'),
    ('<h2 class="hero-title">Cucina<br>di <em>territorio</em></h2>', '<h2 class="hero-title">A taste<br>of <em>Naples</em></h2>'),
    ('La tradizione napoletana rivisitata, i prodotti di stagione e un pizzico di spettacolo al tavolo.',
     'Neapolitan tradition reimagined, seasonal produce and a touch of tableside theatre.'),
    ('class="btn-ghost">Scopri la Cucina</a>', 'class="btn-ghost">Discover the Kitchen</a>'),

    # ── claim ──
    ('"Il profumo della brace, il tintinnio dei calici, la luce sul mare di <em>Posillipo</em>."<br>Benvenuti a',
     '"The scent of the grill, the clink of glasses, the light on the sea of <em>Posillipo</em>."<br>Welcome to'),
    ('<cite>Via Ferdinando Russo 13, Napoli</cite>', '<cite>Via Ferdinando Russo 13, Naples</cite>'),

    # ── due anime ──
    ('<span class="section-eyebrow">La nostra identità</span>', '<span class="section-eyebrow">Who we are</span>'),
    ('<h2 class="section-title">Due <em>anime</em>, un\'unica esperienza</h2>', '<h2 class="section-title">Two <em>souls</em>, one experience</h2>'),
    ('<h3 class="anime-card-title">Braceria</h3>', '<h3 class="anime-card-title">Steakhouse</h3>'),
    ('Eccellenze italiane e internazionali — Wagyu, Black Angus, Marchigiana — frollate in casa e cotte alla brace per esaltare ogni fibra.',
     'The finest Italian and international beef — Wagyu, Black Angus, Marchigiana — dry-aged in house and cooked over the grill to bring out every fibre.'),
    ('<span class="anime-card-link">Scopri la Braceria →</span>', '<span class="anime-card-link">Discover the Steakhouse →</span>'),
    ('<h3 class="anime-card-title">Ristorante</h3>', '<h3 class="anime-card-title">Restaurant</h3>'),
    ('Menu stagionali che reinterpretano la tradizione napoletana: dalla Genovese allo Scarpariello, fino ai flambé preparati al tavolo.',
     'Seasonal menus that reinterpret Neapolitan tradition: from Genovese to Scarpariello, all the way to flambé dishes finished at your table.'),
    ('<span class="anime-card-link">Scopri la Cucina →</span>', '<span class="anime-card-link">Discover the Kitchen →</span>'),

    # ── braceria ──
    ('aria-label="La Braceria di Casa Rosebery"', 'aria-label="The Casa Rosebery Steakhouse"'),
    ('<span class="num">I · La Braceria</span>', '<span class="num">I · The Steakhouse</span>'),
    ('<h2>Undici provenienze,<br>un\'unica <em>brace</em></h2>', '<h2>Eleven origins,<br>one <em>grill</em></h2>'),
    ('Selezioniamo i tagli dai migliori allevamenti del mondo e li lasciamo frollare in casa, il tempo necessario perché la carne guadagni tenerezza e profondità di sapore. Poi la brace fa il resto: pochi gesti, nessuna scorciatoia.',
     'We select our cuts from the finest farms in the world and dry-age them in house for as long as it takes for the meat to gain tenderness and depth of flavour. Then the grill does the rest: few gestures, no shortcuts.'),
    ('aria-label="Provenienze delle carni"', 'aria-label="Where our beef comes from"'),
    ('<span>Italia</span><span>Giappone</span><span>Stati Uniti</span><span>Canada</span><span>Argentina</span><span>Australia</span><span>Irlanda</span><span>Danimarca</span><span>Austria</span><span>Spagna</span><span>Nord Europa</span>',
     '<span>Italy</span><span>Japan</span><span>United States</span><span>Canada</span><span>Argentina</span><span>Australia</span><span>Ireland</span><span>Denmark</span><span>Austria</span><span>Spain</span><span>Northern Europe</span>'),
    ('<p class="sottotitolo">I tagli simbolo</p>', '<p class="sottotitolo">Signature cuts</p>'),
    ('<span class="origine">Giappone · Kagoshima</span>', '<span class="origine">Japan · Kagoshima</span>'),
    ('Manzo Kuroge dalla prefettura premiata alle Olimpiadi del Wagyu. Il grado A5 è il massimo della marezzatura: una consistenza che si scioglie al palato.',
     'Kuroge beef from the prefecture crowned at the Wagyu Olympics. A5 is the highest marbling grade: a texture that melts in the mouth.'),
    ('<span class="prezzo-etto">€ 40 / etto</span>', '<span class="prezzo-etto">€ 40 / 100 g</span>'),
    ('<span class="origine">Stati Uniti · Black Angus</span>', '<span class="origine">United States · Black Angus</span>'),
    ('Il taglio-rituale, con l\'osso scalzato e la consistenza burrosa data dalla finitura a mais. Servito su pietra o tagliere per conservarne calore e succhi.',
     'The ritual cut, with its frenched bone and the buttery texture that comes from corn finishing. Served on a hot stone or board to keep in the heat and juices.'),
    ('<span class="prezzo-etto">€ 14 / etto</span>', '<span class="prezzo-etto">€ 14 / 100 g</span>'),
    ('<span class="origine">Stati Uniti · Creekstone Farms</span>', '<span class="origine">United States · Creekstone Farms</span>'),
    ('Black Angus certificato, 120 giorni di finitura a grano e il celebre cuore di grasso che si fonde in cottura. Dolce, burroso, inconfondibile.',
     'Certified Black Angus, 120 days of grain finishing and the famous fat eye that melts as it cooks. Sweet, buttery, unmistakable.'),
    ('<span class="prezzo-etto">€ 18 / etto</span>', '<span class="prezzo-etto">€ 18 / 100 g</span>'),
    ('<p class="sottotitolo">Come funziona</p>', '<p class="sottotitolo">How it works</p>'),
    ('<h4>Scegli il taglio</h4><p>Con osso o senza osso, dalla Marchigiana Bio al Wagyu giapponese. Il prezzo è all\'etto: la sala ti aiuta a trovare il peso giusto per il tavolo.</p>',
     '<h4>Choose your cut</h4><p>Bone-in or boneless, from organic Marchigiana to Japanese Wagyu. Prices are per 100 g: our staff will help you find the right weight for your table.</p>'),
    ('<h4>La frollatura</h4><p>Ogni taglio matura nella nostra cella fino al punto ideale, per una carne più tenera e un sapore più intenso.</p>',
     '<h4>Dry-ageing</h4><p>Every cut matures in our ageing room until it reaches its ideal point, for more tender meat and a deeper flavour.</p>'),
    ('<h4>La cottura</h4><p>Alla brace, con la cottura consigliata per ogni taglio. Completa con un contorno o con la nostra cruderia e i salumi iberici.</p>',
     '<h4>The cooking</h4><p>Over the grill, to the doneness we recommend for each cut. Complete it with a side, our raw bar or Iberian charcuterie.</p>'),
    ('class="btn-gold">Carta delle carni</a>', 'class="btn-gold">Steak menu</a>'),
    ('class="btn-ghost">Percorso Tagli d\'Oro · € 80</a>', 'class="btn-ghost">"Tagli d\'Oro" tasting menu · € 80</a>'),

    # ── cucina ──
    ('aria-label="La Cucina di Casa Rosebery"', 'aria-label="The Casa Rosebery Kitchen"'),
    ('<span class="num">II · La Cucina</span>', '<span class="num">II · The Kitchen</span>'),
    ('<h2>La tradizione,<br><em>rivisitata</em></h2>', '<h2>Tradition,<br><em>reimagined</em></h2>'),
    ('Accanto alla brace, una cucina che parte dalle ricette napoletane di casa e le racconta con tecnica e leggerezza. Il menu segue le stagioni e alcuni piatti si completano davanti a te.',
     'Alongside the grill, a kitchen that starts from home-style Neapolitan recipes and tells them with technique and a light touch. The menu follows the seasons, and some dishes are finished right in front of you.'),
    ('<span class="origine">Tradizione napoletana</span>', '<span class="origine">Neapolitan tradition</span>'),
    ('<h3>I primi di casa</h3>', '<h3>Our house pastas</h3>'),
    ('La Genovese con lo zito, lo Scarpariello secondo Casa Rosebery, i Manfredi al ragù mantecati con ricotta fresca. Ricette che conosci, con la nostra firma.',
     'Genovese with zito pasta, Scarpariello the Casa Rosebery way, Manfredi with ragù finished with fresh ricotta. Recipes you know, with our signature.'),
    ('<span class="origine">Il menu d\'autunno</span>', '<span class="origine">Autumn menu</span>'),
    ('<h3>La stagione</h3>', '<h3>The season</h3>'),
    ('Vellutata di zucca al mascarpone, risotto ai funghi porcini, pappardelle mantecate al carrello con tartufo bianco, quando la stagione lo concede.',
     'Pumpkin velouté with mascarpone, porcini mushroom risotto, pappardelle tossed tableside with white truffle when the season allows.'),
    ('<span class="origine">Al tavolo</span>', '<span class="origine">At your table</span>'),
    ('<h3>Lo spettacolo del flambé</h3>', '<h3>The flambé show</h3>'),
    ('La Tagliata flambè e la Crêpe Suzette al Grand Marnier vengono ultimate in sala, davanti ai tuoi occhi.',
     'The flambéed Tagliata and the Crêpe Suzette with Grand Marnier are finished in the dining room, before your eyes.'),
    ('<p class="sottotitolo">Percorsi degustazione · minimo 2 persone</p>', '<p class="sottotitolo">Tasting menus · minimum 2 people</p>'),
    ('<span>Antipasti, primo, secondo e dessert</span>', '<span>Starters, pasta, main course and dessert</span>'),
    ('<span>Brasato, Genovese, Tagliata flambè</span>', '<span>Braised beef, Genovese, flambéed Tagliata</span>'),
    ('class="btn-gold">Sfoglia il menu</a>', 'class="btn-gold">Browse the menu</a>'),
    ('class="btn-ghost">Prenota un tavolo</a>', 'class="btn-ghost">Book a table</a>'),

    # ── posillipo ──
    ('<span class="section-eyebrow">Posillipo, Napoli</span>', '<span class="section-eyebrow">Posillipo, Naples</span>'),
    ('<h2 class="posillipo-title">Una cornice<br><em>senza tempo</em></h2>', '<h2 class="posillipo-title">A timeless<br><em>setting</em></h2>'),
    ('Casa Rosebery nasce a Posillipo, uno dei luoghi più suggestivi del Golfo di Napoli. Un ristorante dove l\'eleganza dell\'ambiente si unisce alla passione per la cucina autentica — ogni dettaglio pensato per rendere indimenticabile ogni visita.',
     'Casa Rosebery was born in Posillipo, one of the most enchanting spots on the Bay of Naples. A restaurant where elegant surroundings meet a passion for authentic cooking — every detail designed to make each visit unforgettable.'),
    ('Il nome evoca la Villa Rosebery, residenza del Presidente della Repubblica a pochi passi da noi: storia, bellezza e raffinatezza come fondamenta di tutto quello che facciamo.',
     'Our name recalls Villa Rosebery, the residence of the President of the Italian Republic just a few steps away: history, beauty and refinement as the foundations of everything we do.'),
    ('<span class="posillipo-detail-label">Dove siamo</span>', '<span class="posillipo-detail-label">Where we are</span>'),
    ('Via Ferdinando Russo 13<br>Posillipo, Napoli</span>', 'Via Ferdinando Russo 13<br>Posillipo, Naples</span>'),
    ('<span class="posillipo-detail-label">Parcheggio</span>', '<span class="posillipo-detail-label">Parking</span>'),
    ('Gratuito e riservato<br>Nessuna ZTL</span>', 'Free and reserved<br>No limited-traffic zone (ZTL)</span>'),

    # ── menu ──
    ('<span class="section-eyebrow">Esplora</span>', '<span class="section-eyebrow">Explore</span>'),
    ('<h2 class="section-title">Il nostro <em>menu</em></h2>', '<h2 class="section-title">Our <em>menu</em></h2>'),
    ('<span class="menu-card-label">Cucina & Braceria</span>', '<span class="menu-card-label">Kitchen & Steakhouse</span>'),
    ('<h3 class="menu-card-title">Menu del Ristorante</h3>', '<h3 class="menu-card-title">Restaurant Menu</h3>'),
    ('Antipasti, primi, carni pregiate alla brace e specialità della casa. Aggiornato stagionalmente.',
     'Starters, pasta, prime grilled meats and house specialities. Updated every season.'),
    ('        Sfoglia il Menu\n', '        Browse the Menu\n'),
    ('<span class="menu-card-label">Vini & Bollicine</span>', '<span class="menu-card-label">Wines & Sparkling</span>'),
    ('<h3 class="menu-card-title">Carta dei Vini</h3>', '<h3 class="menu-card-title">Wine List</h3>'),
    ('Oltre 160 etichette: Champagne e Franciacorta, i grandi rossi italiani per la brace, bianchi vulcanici della Campania.',
     'Over 160 labels: Champagne and Franciacorta, great Italian reds for the grill, volcanic whites from Campania.'),
    ('        Sfoglia la Carta\n', '        Browse the Wine List\n'),

    # ── eventi privati ──
    ('<span class="section-eyebrow">Serate & Cene Private</span>', '<span class="section-eyebrow">Evenings & Private Dining</span>'),
    ('<h2 class="section-title">Un\'esperienza <em>su misura</em></h2>', '<h2 class="section-title">A <em>tailor-made</em> experience</h2>'),
    ('<span class="live-eyebrow">Ogni sabato sera</span>', '<span class="live-eyebrow">Every Saturday night</span>'),
    ('<div class="live-titolo">Musica <em>dal vivo</em></div>', '<div class="live-titolo"><em>Live</em> music</div>'),
    ('<p>Ogni sabato, a cena, la serata è accompagnata da musica dal vivo.</p>', '<p>Every Saturday, dinner is accompanied by live music.</p>'),
    ('Organizziamo cene aziendali, eventi privati, serate a tema e compleanni.<br>\n      Raccontaci la tua occasione — creiamo qualcosa di indimenticabile insieme.',
     'We host corporate dinners, private events, themed evenings and birthdays.<br>\n      Tell us about your occasion — let\'s create something unforgettable together.'),
    ('<label for="ev-nome">Nome e cognome</label>', '<label for="ev-nome">Full name</label>'),
    ('placeholder="Mario Rossi"', 'placeholder="John Smith"'),
    ('<label for="ev-tel">Telefono</label>', '<label for="ev-tel">Phone</label>'),
    ('placeholder="+39 000 0000000"', 'placeholder="+44 0000 000000"'),
    ('<label for="ev-data">Data dell\'evento</label>', '<label for="ev-data">Event date</label>'),
    ('<label for="ev-persone">Numero di persone</label>', '<label for="ev-persone">Number of guests</label>'),
    ('placeholder="Es. 20"', 'placeholder="e.g. 20"'),
    ('<label for="ev-tipo">Tipo di evento</label>', '<label for="ev-tipo">Type of event</label>'),
    ('title="Mappa: Casa Rosebery, Via Ferdinando Russo 13, Napoli"', 'title="Map: Casa Rosebery, Via Ferdinando Russo 13, Naples"'),
    ('<option value="">Seleziona...</option>', '<option value="">Select...</option>'),
    ('<option>Cena aziendale</option>', '<option>Corporate dinner</option>'),
    ('<option>Compleanno / Anniversario</option>', '<option>Birthday / Anniversary</option>'),
    ('<option>Evento privato</option>', '<option>Private event</option>'),
    ('<option>Serata a tema</option>', '<option>Themed evening</option>'),
    ('<option>Altro</option>', '<option>Other</option>'),
    ('<label for="ev-note">Note o richieste particolari</label>', '<label for="ev-note">Notes or special requests</label>'),
    ('placeholder="Descrivi la tua occasione..."', 'placeholder="Tell us about your occasion..."'),
    ('class="btn-dark">Invia richiesta</button>', 'class="btn-dark">Send request</button>'),
    ('<span class="divider-or">oppure</span>', '<span class="divider-or">or</span>'),
    ('https://wa.me/390813357572?text=Ciao!%20Vorrei%20informazioni%20per%20un%20evento%20a%20Casa%20Rosebery.',
     'https://wa.me/390813357572?text=Hi!%20I%27d%20like%20some%20information%20about%20an%20event%20at%20Casa%20Rosebery.'),
    ('          Scrivici su WhatsApp\n', '          Message us on WhatsApp\n'),

    # ── contatti ──
    ('<h2 class="contatti-title">Come raggiungerci</h2>', '<h2 class="contatti-title">How to find us</h2>'),
    ('<span class="info-label">Indirizzo</span>', '<span class="info-label">Address</span>'),
    ('80123 Posillipo, Napoli<br>', '80123 Posillipo, Naples, Italy<br>'),
    ('padding-bottom:2px">Indicazioni stradali →</a>', 'padding-bottom:2px">Get directions →</a>'),
    ('<span class="info-label">Telefono & Prenotazioni</span>', '<span class="info-label">Phone & Reservations</span>'),
    ('<a href="tel:0813357572">081 335 7572</a>', '<a href="tel:+390813357572">+39 081 335 7572</a>'),
    ('<span class="info-label">Orari di apertura</span>', '<span class="info-label">Opening hours</span>'),
    ('<span class="info-label">Parcheggio</span>', '<span class="info-label">Parking</span>'),
    ('Gratuito e riservato ai clienti<br><span style="font-size:12px;opacity:0.6">Nessun vincolo ZTL</span>',
     'Free and reserved for guests<br><span style="font-size:12px;opacity:0.6">Outside the limited-traffic zone (ZTL)</span>'),
    ('!5e0!3m2!1sit!2sit!4v1', '!5e0!3m2!1sen!2sit!4v1'),

    # ── gallery ──
    ('<h2 class="section-title">Casa Rosebery in <em>immagini</em></h2>', '<h2 class="section-title">Casa Rosebery in <em>pictures</em></h2>'),
    ("onclick=\"filterGallery('all',this)\">Tutto</button>", "onclick=\"filterGallery('all',this)\">All</button>"),
    ("onclick=\"filterGallery('braceria',this)\">Braceria</button>", "onclick=\"filterGallery('braceria',this)\">Steakhouse</button>"),
    ("onclick=\"filterGallery('cucina',this)\">Cucina</button>", "onclick=\"filterGallery('cucina',this)\">Kitchen</button>"),
    ("onclick=\"filterGallery('locale',this)\">Il Locale</button>", "onclick=\"filterGallery('locale',this)\">The Venue</button>"),

    # descrizioni delle foto (alt)


    # ── social ──
    ('<h2 class="social-strip-title">Seguici su <em>Instagram</em></h2>', '<h2 class="social-strip-title">Follow us on <em>Instagram</em></h2>'),
    ('<p class="social-strip-sub">@casarosebery · Napoli, Posillipo</p>', '<p class="social-strip-sub">@casarosebery · Posillipo, Naples</p>'),
    ('<p class="social-tag">4.716 follower · 112 post</p>', '<p class="social-tag">4,716 followers · 112 posts</p>'),

    # ── recensioni ──
    ('<span class="section-eyebrow">La voce dei nostri ospiti</span>', '<span class="section-eyebrow">What our guests say</span>'),
    ('<h2 class="section-title">Cosa dicono <em>di noi</em></h2>', '<h2 class="section-title">Guest <em>reviews</em></h2>'),
    ('<div class="badge-info">su Google Reviews</div>', '<div class="badge-info">on Google Reviews</div>'),
    ('locationId=32726215&lang=it&', 'locationId=32726215&lang=en_UK&'),
    ('Il posto è molto accogliente, si sta tranquilli e la vista di Napoli è veramente meravigliosa. Il cibo ottimo. Un voto speciale oltre alla carne lo abbiamo dato ai ravioli ripieni al ragù di Anatra — una vera goduria.',
     'The place is very welcoming and relaxing, and the view of Naples is truly wonderful. Excellent food. Besides the meat, a special mention goes to the ravioli filled with duck ragù — a real treat.'),
    ('<div class="review-author">Ospite TripAdvisor</div>', '<div class="review-author">TripAdvisor guest</div>'),
    ('<div class="review-source">TripAdvisor · 2025</div>', '<div class="review-source">TripAdvisor · 2025 · translated from Italian</div>'),
    ('Esperienza straordinaria. La carne è di qualità eccezionale, cucinata alla perfezione. L\'atmosfera è elegante ma accogliente, e il personale è attento e professionale. Torneremo sicuramente.',
     'An extraordinary experience. The meat is of exceptional quality, cooked to perfection. The atmosphere is elegant yet welcoming, and the staff are attentive and professional. We will definitely be back.'),
    ('<div class="review-author">Ospite Google</div>', '<div class="review-author">Google guest</div>', 2),
    ('<div class="review-source">Google Reviews · 2025</div>', '<div class="review-source">Google Reviews · 2025 · translated from Italian</div>'),
    ('Una serata indimenticabile a Posillipo. La qualità della carne è straordinaria e il servizio impeccabile. Il panorama sul Golfo completa un\'esperienza che vale ogni euro.',
     'An unforgettable evening in Posillipo. The quality of the meat is outstanding and the service impeccable. The view over the Bay completes an experience worth every euro.'),
    ('<div class="review-source">Google Reviews · 2026</div>', '<div class="review-source">Google Reviews · 2026 · translated from Italian</div>'),
    ('https://www.tripadvisor.it/Restaurant_Review', 'https://www.tripadvisor.com/Restaurant_Review', 3),
    ('      Leggi tutte le recensioni →\n', '      Read all reviews →\n'),

    # ── footer, sticky, cookie ──
    ('Privacy e Cookie Policy</a> · <a href="#" id="apri-preferenze-cookie" style="color:rgba(255,255,255,0.65);text-decoration:underline">Preferenze cookie</a>',
     'Privacy & Cookie Policy (Italian)</a> · <a href="#" id="apri-preferenze-cookie" style="color:rgba(255,255,255,0.65);text-decoration:underline">Cookie preferences</a>'),
    ('class="prenota-sticky" target="_blank">\n  Prenota ora\n</a>', 'class="prenota-sticky" target="_blank">\n  Book now\n</a>'),
    ('aria-label="Preferenze cookie"', 'aria-label="Cookie preferences"'),
    ('aria-label="Chiudi e rifiuta"', 'aria-label="Close and reject"'),
    ('<p>Usiamo cookie tecnici necessari al funzionamento del sito e, solo con il tuo consenso, cookie analitici di Google Analytics per capire come viene visitato. Puoi cambiare idea in qualsiasi momento da "Preferenze cookie" in fondo alla pagina. <a href="privacy.html#cookie">Maggiori informazioni</a></p>',
     '<p>We use technical cookies that the site needs to work and, only with your consent, Google Analytics cookies to understand how it is used. You can change your mind at any time via "Cookie preferences" at the bottom of the page. <a href="privacy.html#cookie">More information (Italian)</a></p>'),
    ('data-scelta="rifiutato">Rifiuta</button>', 'data-scelta="rifiutato">Reject</button>'),
    ('data-scelta="accettato">Accetta</button>', 'data-scelta="accettato">Accept</button>'),

    # ── orari (config + script) ──
    ('{ "giorni": "Lunedì – Venerdì", "pranzo": "—", "cena": "19:30 – 23:30" },',
     '{ "giorni": "Monday – Friday", "pranzo": "—", "cena": "7:30 pm – 11:30 pm" },'),
    ('{ "giorni": "Sabato", "pranzo": "12:30 – 15:30", "cena": "19:30 – 23:30", "nota": "Sabato sera musica dal vivo" },',
     '{ "giorni": "Saturday", "pranzo": "12:30 pm – 3:30 pm", "cena": "7:30 pm – 11:30 pm", "nota": "Live music on Saturday night" },'),
    ('{ "giorni": "Domenica", "pranzo": "12:30 – 15:30", "cena": "—" }',
     '{ "giorni": "Sunday", "pranzo": "12:30 pm – 3:30 pm", "cena": "—" }'),
    ('<span style="opacity:0.4">Chiuso</span>', '<span style="opacity:0.4">Closed</span>'),
    ("fasce.push('Pranzo ' + o.pranzo);", "fasce.push('Lunch ' + o.pranzo);"),
    ("fasce.push('Cena ' + o.cena);", "fasce.push('Dinner ' + o.cena);"),

    # ── modulo eventi (email) ──
    ('`Richiesta evento da ${nome}\\n` +\n    `Tel: ${tel}\\n` +\n    `Data: ${data}\\n` +\n    `Persone: ${pax}\\n` +\n    `Tipo: ${tipo}\\n` +\n    `Note: ${note}`',
     '`Event request (EN site) from ${nome}\\n` +\n    `Phone: ${tel}\\n` +\n    `Date: ${data}\\n` +\n    `Guests: ${pax}\\n` +\n    `Type: ${tipo}\\n` +\n    `Notes: ${note}`'),
    ('?subject=Richiesta%20evento%20Casa%20Rosebery&', '?subject=Event%20request%20Casa%20Rosebery%20(EN)&'),

    # ── barra mobile ──
    ('<span style="color:var(--oro);font-weight:600">Prenota</span>', '<span style="color:var(--oro);font-weight:600">Book</span>'),
    ('<span>Contatti</span>', '<span>Contact</span>'),
    ('<span>Serate</span>', '<span>Events</span>'),
    ('alt="Bistecche con osso frollate nella nostra cella, pronte per la brace"', 'alt="Bone-in steaks dry-aged in our ageing room, ready for the grill"'),
    ('alt="Brisket Casa Rosebery su purea di patate, con il porticciolo e il Golfo di Napoli sullo sfondo"', 'alt="Brisket Casa Rosebery on mashed potato, with the marina and the Bay of Naples in the background"'),
    ('alt="Medaglioni di manzo alla brace con peperoni e germogli, su ardesia"', 'alt="Grilled beef medallions with peppers and microgreens on slate"'),
    ('alt="Carne al sangue tagliata a fette, su piatto nero"', 'alt="Rare beef cut into slices, on a black plate"'),
    ('alt="Bistecca alla brace con sale grosso"', 'alt="Grilled steak with coarse salt"'),
    ('alt="Costata con l\'osso tagliata a fette e servita su pietra"', 'alt="Bone-in steak sliced and served on a stone"'),
    ('alt="Tagli di manzo con l\'osso in esposizione"', 'alt="Bone-in beef cuts on display"'),
    ('alt="Il macellaio con la mannaia dietro ai tagli di manzo"', 'alt="Our butcher with a cleaver behind the beef cuts"'),
    ('alt="Taglio di manzo frollato in primo piano"', 'alt="Close-up of a dry-aged beef cut"'),
    ('alt="Lo chef al lavoro alla piastra, in bianco e nero"', 'alt="The chef at work at the griddle, in black and white"'),
    ('alt="Un tagliere di carne portato in sala"', 'alt="A board of meat carried into the dining room"'),
    ('alt="Pane farcito con friarielli, stracciatella e prosciutto croccante, Vesuvio al tramonto sullo sfondo"', 'alt="Bread filled with friarielli, stracciatella and crispy prosciutto, Mount Vesuvius at sunset in the background"'),
    ('alt="Verza ripiena con provola filante e salsiccia croccante, Vesuvio al tramonto sullo sfondo"', 'alt="Stuffed savoy cabbage with melted provola and crispy sausage, Mount Vesuvius at sunset in the background"'),
    ('alt="Piatto di carne glassata con salsa, su piatto turchese"', 'alt="Glazed meat dish with sauce, on a turquoise plate"'),
    ('alt="Pasta al pomodoro con crema di formaggio"', 'alt="Pasta with tomato and a cheese cream"'),
    ('alt="Fettine sottili di manzo crudo"', 'alt="Thin slices of raw beef"'),
    ('alt="Piatto di carne sfilacciata con olio alle erbe, accanto alla vetrata"', 'alt="Pulled meat dish with herb oil, by the window"'),
    ('alt="Dolce con crema e frutti di bosco"', 'alt="Dessert with custard and berries"'),
    ('alt="Dolce monoporzione alla crema su base di biscotto"', 'alt="Single-serve cream dessert on a biscuit base"'),
    ('alt="Piatto di carne sfilacciata con salsa verde, sullo sfondo una barca"', 'alt="Pulled meat dish with green sauce, a boat in the background"'),
    ('alt="Genovese, sullo sfondo il mare"', 'alt="Genovese, the sea in the background"'),
    ('alt="Polpettine alla gricia"', 'alt="Polpettine alla gricia (meatballs)"'),
    ('alt="Piatto di carni crude e salumi con salse"', 'alt="Platter of raw and cured meats with sauces"'),
    ('alt="Panino con carne e formaggio fuso"', 'alt="Sandwich with meat and melted cheese"'),
    ('alt="Nerano, in primo piano"', 'alt="Nerano, close-up"'),
    ('alt="Polpettine alla gricia, in primo piano"', 'alt="Polpettine alla gricia (meatballs), close-up"'),
    ('alt="Dolce su stecco con granella e ribes"', 'alt="Dessert on a stick with crumble and redcurrants"'),
    ('alt="Dolce al cioccolato con pistacchi"', 'alt="Chocolate dessert with pistachios"'),
    ('alt="Genovese, in primo piano"', 'alt="Genovese, close-up"'),
    ('alt="Tavolo apparecchiato davanti alla finestra con il Vesuvio"', 'alt="Table set by the window with Vesuvius in view"'),
    ('alt="Scaffali con vini, olio e prodotti della dispensa"', 'alt="Shelves of wine, olive oil and pantry products"'),
    ('alt="Calici sulla tavola apparecchiata"', 'alt="Wine glasses on a set table"'),
    ('alt="La sala con le grandi finestre sul Golfo"', 'alt="The dining room with large windows over the Gulf"'),
    ('alt="Posate con il logo Casa Rosebery"', 'alt="Cutlery with the Casa Rosebery logo"'),
    ('alt="Nicchia con vini, olio e pasta"', 'alt="Niche with wine, olive oil and pasta"'),
    ('alt="Un piatto in terrazza con vista su Napoli e il Vesuvio"', 'alt="A dish on the terrace overlooking Naples and Vesuvius"'),
    ('alt="Il Vesuvio e il Golfo al tramonto, visti dagli scogli"', 'alt="Vesuvius and the Gulf at dusk, seen from the rocks"'),
]


def traduci(testo):
    mancanti = []
    for voce in T:
        it, en = voce[0], voce[1]
        n = voce[2] if len(voce) > 2 else None
        trovate = testo.count(it)
        if trovate == 0 or (n is not None and trovate != n):
            mancanti.append(it[:90])
            continue
        testo = testo.replace(it, en)
    # il link del menu "Serate & Eventi" esiste in una sola delle due forme (#serate o #eventi)
    mancanti = [m for m in mancanti if not m.startswith('<li><a href="#serate">') and not m.startswith('<li><a href="#eventi">')]
    if mancanti:
        sys.exit("Testi italiani non trovati in index.html (aggiornare en-src/genera_en.py):\n- " + "\n- ".join(mancanti))
    return testo


def percorsi_assoluti(testo):
    # la pagina vive in /en/: le risorse condivise puntano alla radice, menu e vini alle versioni inglesi
    def attr(m):
        nome, url = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|tel:|#|/|data:|javascript:)", url):
            return m.group(0)
        if url.startswith(("menu.html", "vini.html")):
            return f'{nome}="/en/{url}"'
        return f'{nome}="/{url}"'
    testo = re.sub(r'\b(src|href)="([^"]*)"', attr, testo)
    testo = re.sub(r"url\('(img/[^']+)'\)", r"url('/\1')", testo)
    return testo


it = (RADICE / "index.html").read_text(encoding="utf-8")
en = percorsi_assoluti(traduci(it))
# controllo: nessuna parola italiana evidente rimasta fuori dal blocco serate
fuori = re.sub(r"<!-- EVENTI:INIZIO -->.*?<!-- EVENTI:FINE -->|<script.*?</script>|<style.*?</style>", "", en, flags=re.S)
for parola in ["Prenota", "Scopri", "Sfoglia", "Recensioni", "Contatti"]:
    if re.search(rf">\s*[^<]*\b{parola}\b", fuori):
        sys.exit(f"Attenzione: '{parola}' è ancora presente nella versione inglese")
(RADICE / "en").mkdir(exist_ok=True)
(RADICE / "en" / "index.html").write_text(en, encoding="utf-8")
print("en/index.html generato")
# serate in inglese
subprocess.run([sys.executable, str(RADICE / "eventi-src" / "genera_eventi.py")] + sys.argv[1:], check=True)
