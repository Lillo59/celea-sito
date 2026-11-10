# Listino v2.2 (decisione d20261110-william-listino-v2-2-servizi-nuovi): aggiorna prezzi, piani e disponibilità
# in index.html nelle tre lingue. Solo testi, numeri e voci: stessi componenti e classi di prima.
# Lo Start WhatsApp resta nella pagina ma nascosto (attributo hidden): si riaccende solo se William lo decide.
# Idempotente: se il listino v2.2 c'è già, non fa nulla.
import re, sys, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = P.read_text(encoding='utf-8')
GIA = 'data-listino="2.2"' in s
if GIA: print('listino v2.2 già presente')

def sub1(pat, new, text, flags=0, label=''):
    out, n = re.subn(pat, lambda m: new, text, count=1, flags=flags)
    if n != 1: raise SystemExit(f'NON TROVATO: {label or pat[:80]}')
    return out

def rep(old, new, text, label=''):
    if text.count(old) != 1: raise SystemExit(f'NON TROVATO (o doppio, {text.count(old)}): {label or old[:90]}')
    return text.replace(old, new)

# ---------------------------------------------------------------- testi nuovi per lingua
T = {
'it': dict(
  ph='<h3 class="ph" data-listino="2.2">I tre piani dell\'assistente <small>uguali per studi dentistici, agenzie immobiliari e strutture ricettive. Per gli studi dentistici consigliamo lo Studio.</small></h3>',
  studio='<article class="cat-top"><p class="pk-n">Studio · consigliato per gli studi</p><h4><b>129 €</b>/mese</h4><p>L\'assistente risponde al telefono ai Suoi clienti, anche fuori orario negli orari che sceglie Lei: informazioni, appuntamenti nell\'Agenda, passaggio a una persona quando serve.</p><ul><li>Telefono: 400 minuti di telefonate al mese</li><li>Agenda inclusa: 1 calendario, fino a 2 tipi di appuntamento</li><li>Invio di file e indicazioni su WhatsApp (da gennaio 2027)</li><li>Minuti extra 0,25 €/min</li><li>Italiano, inglese e tedesco inclusi</li><li>Attivazione 190 € (gratis per i clienti fondatori)</li></ul></article>',
  pro='<article><p class="pk-n">Pro</p><h4><b>189 €</b>/mese</h4><p>Lo stesso assistente al telefono e sui canali scritti, con voce standard inclusa.</p><ul><li>Telefono: 600 minuti di telefonate al mese</li><li>500 conversazioni al mese su WhatsApp (da gennaio 2027), Instagram e Messenger (in arrivo nel 2027): i canali scritti si sommano nello stesso tetto</li><li>Agenda Plus inclusa</li><li>Riconoscimento di chi richiama (in arrivo nel 2027)</li><li>Importazione dei contatti da file (CSV) ed esportazione delle richieste su Google Sheets (in arrivo nel 2027)</li><li>Italiano, inglese e tedesco inclusi</li><li>Attivazione 190 € (gratis per i clienti fondatori)</li></ul></article>',
  prosito='<article><p class="pk-n">Pro + sito</p><h4><b>249 €</b>/mese</h4><p>Tutto il Pro con più minuti, più un sito vetrina di 5 pagine per la Sua attività, con l\'assistente già integrato, hosting e manutenzione.</p><ul><li>Telefono: 800 minuti di telefonate al mese</li><li>500 conversazioni sui canali scritti, come nel Pro</li><li>Sito vetrina incluso, con hosting e manutenzione</li><li>Italiano, inglese e tedesco inclusi</li><li>Attivazione 390 € (gratis per i clienti fondatori)</li></ul></article>',
  pdf='<p class="pnote">Il listino completo in un foglio: <a href="listino/Celea-Listino-v2-2.pdf">Scarica il listino (PDF)</a> · <a href="listino/">versione da stampare</a>.</p>',
  min_old='<li><span>Minuti di telefonata oltre quelli inclusi</span><b>0,25 €/min</b></li>',
  min_new='<li><span>Minuti di telefonata oltre quelli inclusi, in ogni piano</span><b>0,25 €/min</b></li>\n            <li><span>Canale in più sullo Studio: Instagram o Messenger (in arrivo nel 2027)</span><b>19 €/mese</b></li>\n            <li><span>Promemoria con telefonata, solo con Pro e Pro + sito: 150 chiamate al mese incluse, oltre 0,15 € a chiamata (in arrivo)</span><b>29 €/mese</b></li>',
  conv_old='<li><span>Conversazioni WhatsApp oltre il limite del piano</span><b>15 € ogni 100</b></li>',
  conv_new='<li><span>Conversazioni sui canali scritti (WhatsApp, Instagram, Messenger) oltre il tetto del piano</span><b>15 € ogni 100</b></li>',
  meta_old='<li><span>Con lo Start (stima)</span><b>da 0 a circa 20 €/mese</b></li>',
  meta_new='<li><span>Con lo Studio, solo invio di file e indicazioni (stima)</span><b>da 0 a pochi euro al mese</b></li>',
  es_old=' Un B&amp;B con lo Start: 79 € più i messaggi Meta, cioè 79–99 € al mese in tutto.',
  es_new=' Uno studio dentistico con lo Studio: 129 € al mese, più pochi euro di messaggi Meta per i file e le indicazioni, quando WhatsApp sarà attivo.',
  att_old='(190 € Start, 190 € Pro, 390 € Pro + sito)', att_new='(190 € Studio, 190 € Pro, 390 € Pro + sito)',
  ann_old='<b>Pagamento annuale:</b> Start 12 mesi al prezzo di 10 (790 € l\'anno); Pro e Pro + sito 12 mesi al prezzo di 11 (2.079 € e 2.739 € l\'anno).',
  ann_new='<b>Pagamento annuale:</b> Studio, Pro e Pro + sito 12 mesi al prezzo di 11 (1.419 €, 2.079 € e 2.739 € l\'anno).',
  sito_old='in aggiunta allo Start o al Pro', sito_new='in aggiunta allo Studio o al Pro',
  fconv_old='<summary>E se supero le conversazioni WhatsApp?</summary><div class="ans"><p>L\'assistente continua a rispondere. Le conversazioni oltre il limite del piano costano 15 € ogni 100.</p>',
  fconv_new='<summary>E se supero le conversazioni scritte?</summary><div class="ans"><p>L\'assistente continua a rispondere. Le conversazioni oltre il tetto del piano (WhatsApp, Instagram e Messenger insieme) costano 15 € ogni 100.</p>',
  fdiff_re=r'<summary>Che differenza c\'è tra Start, Pro e Pro \+ sito\?</summary><div class="ans"><p>.*?</p>',
  fdiff_new='<summary>Che differenza c\'è tra Studio, Pro e Pro + sito?</summary><div class="ans"><p>Lo Studio risponde al telefono, con 400 minuti al mese e l\'Agenda inclusa: è il piano che consigliamo agli studi dentistici. Il Pro aggiunge i canali scritti (WhatsApp da gennaio 2027, Instagram e Messenger in arrivo nel 2027), con 600 minuti e 500 conversazioni al mese e l\'Agenda Plus. Il Pro + sito ha 800 minuti e il sito vetrina compreso. Se non sa quale scegliere, provi la demo e ne parliamo in una breve chiamata.</p>',
  fann_old='Sì: con lo Start paga 10 mesi e ne riceve 12; con il Pro e il Pro + sito paga 11 mesi e ne riceve 12.',
  fann_new='Sì: con lo Studio, il Pro e il Pro + sito paga 11 mesi e ne riceve 12.',
  inizio_old=None, inizio_new=None,
),
'en': dict(
  ph='<h3 class="ph" data-listino="2.2">The three assistant plans <small>the same for dental practices, real estate agencies and hospitality. For dental practices we recommend Studio.</small></h3>',
  studio='<article class="cat-top"><p class="pk-n">Studio · recommended for practices</p><h4><b>€129</b>/month</h4><p>Your assistant answers your customers on the phone, also outside opening hours you choose: information, appointments in the Calendar and hand-over to a person when needed.</p><ul><li>Phone: 400 call minutes a month</li><li>Calendar included: 1 calendar, up to 2 appointment types</li><li>Sending files and directions on WhatsApp (from January 2027)</li><li>Extra minutes €0.25/min</li><li>Italian, English and German included</li><li>Setup €190 (free for founding clients)</li></ul></article>',
  pro='<article><p class="pk-n">Pro</p><h4><b>€189</b>/month</h4><p>The same assistant on the phone and on the written channels, with a standard voice included.</p><ul><li>Phone: 600 call minutes a month</li><li>500 conversations a month on WhatsApp (from January 2027), Instagram and Messenger (coming in 2027): the written channels share the same limit</li><li>Calendar Plus included</li><li>Recognising returning callers (coming in 2027)</li><li>Importing contacts from a file (CSV) and exporting enquiries to Google Sheets (coming in 2027)</li><li>Italian, English and German included</li><li>Setup €190 (free for founding clients)</li></ul></article>',
  prosito='<article><p class="pk-n">Pro + website</p><h4><b>€249</b>/month</h4><p>Everything in Pro with more minutes, plus a 5-page showcase website for your business with the assistant built in, hosting and maintenance.</p><ul><li>Phone: 800 call minutes a month</li><li>500 conversations on the written channels, as in Pro</li><li>Showcase website included, with hosting and maintenance</li><li>Italian, English and German included</li><li>Setup €390 (free for founding clients)</li></ul></article>',
  pdf='<p class="pnote">The full price list on one sheet: <a href="listino/Celea-Listino-v2-2.pdf">Download the price list (PDF, Italian)</a> · <a href="listino/">printable version</a>.</p>',
  min_old='<li><span>Call minutes beyond those included</span><b>€0.25/min</b></li>',
  min_new='<li><span>Call minutes beyond those included, on every plan</span><b>€0.25/min</b></li>\n            <li><span>Extra channel on Studio: Instagram or Messenger (coming in 2027)</span><b>€19/month</b></li>\n            <li><span>Reminders by phone call, only with Pro and Pro + website: 150 calls a month included, then €0.15 per call (coming soon)</span><b>€29/month</b></li>',
  conv_old='<li><span>WhatsApp conversations beyond the plan limit</span><b>€15 per 100</b></li>',
  conv_new='<li><span>Conversations on the written channels (WhatsApp, Instagram, Messenger) beyond the plan limit</span><b>€15 per 100</b></li>',
  meta_old='<li><span>With Start (estimate)</span><b>from €0 to about €20/month</b></li>',
  meta_new='<li><span>With Studio, only sending files and directions (estimate)</span><b>from €0 to a few euros a month</b></li>',
  es_old=' A B&amp;B on Start: €79 plus Meta messages, i.e. €79–99 a month in total.',
  es_new=' A dental practice on Studio: €129 a month, plus a few euros of Meta messages for files and directions, once WhatsApp is active.',
  att_old='(€190 Start, €190 Pro, €390 Pro + website)', att_new='(€190 Studio, €190 Pro, €390 Pro + website)',
  ann_old='<b>Annual payment:</b> Start 12 months for the price of 10 (€790 a year); Pro and Pro + website 12 months for the price of 11 (€2,079 and €2,739 a year).',
  ann_new='<b>Annual payment:</b> Studio, Pro and Pro + website 12 months for the price of 11 (€1,419, €2,079 and €2,739 a year).',
  sito_old='in addition to Start or Pro', sito_new='in addition to Studio or Pro',
  fconv_old='<summary>And if I go over my WhatsApp conversations?</summary><div class="ans"><p>The assistant keeps answering. Conversations beyond the plan limit cost €15 per 100.</p>',
  fconv_new='<summary>And if I go over my written conversations?</summary><div class="ans"><p>The assistant keeps answering. Conversations beyond the plan limit (WhatsApp, Instagram and Messenger together) cost €15 per 100.</p>',
  fdiff_re=r'<summary>What is the difference between Start, Pro and Pro \+ website\?</summary><div class="ans"><p>.*?</p>',
  fdiff_new='<summary>What is the difference between Studio, Pro and Pro + website?</summary><div class="ans"><p>Studio answers the phone, with 400 minutes a month and the Calendar included: it is the plan we recommend for dental practices. Pro adds the written channels (WhatsApp from January 2027, Instagram and Messenger coming in 2027), with 600 minutes and 500 conversations a month and Calendar Plus. Pro + website has 800 minutes and the showcase website included. If you are not sure which to choose, try the demo and let\'s talk in a short call.</p>',
  fann_old='Yes: with Start you pay 10 months and get 12; with Pro and Pro + website you pay 11 months and get 12.',
  fann_new='Yes: with Studio, Pro and Pro + website you pay 11 months and get 12.',
  inizio_old='<li><b>Start:</b> services go live from January 2027.', inizio_new='<li><b>Go-live:</b> services go live from January 2027.',
),
'de': dict(
  ph='<h3 class="ph" data-listino="2.2">Die drei Pläne des Assistenten <small>gleich für Zahnarztpraxen, Immobilienagenturen und Unterkünfte. Für Zahnarztpraxen empfehlen wir Studio.</small></h3>',
  studio='<article class="cat-top"><p class="pk-n">Studio · empfohlen für Praxen</p><h4><b>129 €</b>/Monat</h4><p>Der Assistent beantwortet die Anrufe Ihrer Kunden, auch außerhalb der Öffnungszeiten, die Sie wählen: Informationen, Termine im Kalender und Weitergabe an eine Person, wenn nötig.</p><ul><li>Telefon: 400 Telefonminuten im Monat</li><li>Kalender inklusive: 1 Kalender, bis zu 2 Terminarten</li><li>Versand von Dateien und Wegbeschreibungen auf WhatsApp (ab Januar 2027)</li><li>Zusätzliche Minuten 0,25 €/Min.</li><li>Italienisch, Englisch und Deutsch inklusive</li><li>Einrichtung 190 € (gratis für Gründungskunden)</li></ul></article>',
  pro='<article><p class="pk-n">Pro</p><h4><b>189 €</b>/Monat</h4><p>Derselbe Assistent am Telefon und auf den schriftlichen Kanälen, Standardstimme inklusive.</p><ul><li>Telefon: 600 Telefonminuten im Monat</li><li>500 Gespräche im Monat auf WhatsApp (ab Januar 2027), Instagram und Messenger (kommt 2027): Die schriftlichen Kanäle teilen sich dasselbe Limit</li><li>Kalender Plus inklusive</li><li>Wiedererkennung von Rückrufern (kommt 2027)</li><li>Import von Kontakten aus einer Datei (CSV) und Export der Anfragen nach Google Sheets (kommt 2027)</li><li>Italienisch, Englisch und Deutsch inklusive</li><li>Einrichtung 190 € (gratis für Gründungskunden)</li></ul></article>',
  prosito='<article><p class="pk-n">Pro + Website</p><h4><b>249 €</b>/Monat</h4><p>Alles aus Pro mit mehr Minuten, dazu eine Präsentations-Website mit 5 Seiten für Ihren Betrieb, mit integriertem Assistenten, Hosting und Wartung.</p><ul><li>Telefon: 800 Telefonminuten im Monat</li><li>500 Gespräche auf den schriftlichen Kanälen, wie bei Pro</li><li>Präsentations-Website inklusive, mit Hosting und Wartung</li><li>Italienisch, Englisch und Deutsch inklusive</li><li>Einrichtung 390 € (gratis für Gründungskunden)</li></ul></article>',
  pdf='<p class="pnote">Die vollständige Preisliste auf einem Blatt: <a href="listino/Celea-Listino-v2-2.pdf">Preisliste herunterladen (PDF, Italienisch)</a> · <a href="listino/">Druckversion</a>.</p>',
  min_old='<li><span>Telefonminuten über die enthaltenen hinaus</span><b>0,25 €/Min.</b></li>',
  min_new='<li><span>Telefonminuten über die enthaltenen hinaus, in jedem Plan</span><b>0,25 €/Min.</b></li>\n            <li><span>Zusätzlicher Kanal bei Studio: Instagram oder Messenger (kommt 2027)</span><b>19 €/Monat</b></li>\n            <li><span>Erinnerungen per Anruf, nur mit Pro und Pro + Website: 150 Anrufe im Monat inklusive, danach 0,15 € pro Anruf (kommt bald)</span><b>29 €/Monat</b></li>',
  conv_old='<li><span>WhatsApp-Gespräche über das Limit des Plans hinaus</span><b>15 € je 100</b></li>',
  conv_new='<li><span>Gespräche auf den schriftlichen Kanälen (WhatsApp, Instagram, Messenger) über das Limit des Plans hinaus</span><b>15 € je 100</b></li>',
  meta_old='<li><span>Mit Start (Schätzung)</span><b>0 bis etwa 20 €/Monat</b></li>',
  meta_new='<li><span>Mit Studio, nur Versand von Dateien und Wegbeschreibungen (Schätzung)</span><b>0 bis wenige Euro im Monat</b></li>',
  es_old=' Ein B&amp;B mit Start: 79 € plus Meta-Nachrichten, also 79–99 € im Monat insgesamt.',
  es_new=' Eine Zahnarztpraxis mit Studio: 129 € im Monat, plus wenige Euro Meta-Nachrichten für Dateien und Wegbeschreibungen, sobald WhatsApp aktiv ist.',
  att_old='(190 € Start, 190 € Pro, 390 € Pro + Website)', att_new='(190 € Studio, 190 € Pro, 390 € Pro + Website)',
  ann_old='<b>Jährliche Zahlung:</b> Start 12 Monate zum Preis von 10 (790 € im Jahr); Pro und Pro + Website 12 Monate zum Preis von 11 (2.079 € und 2.739 € im Jahr).',
  ann_new='<b>Jährliche Zahlung:</b> Studio, Pro und Pro + Website 12 Monate zum Preis von 11 (1.419 €, 2.079 € und 2.739 € im Jahr).',
  sito_old='zusätzlich zu Start oder Pro', sito_new='zusätzlich zu Studio oder Pro',
  fconv_old='<summary>Und wenn ich die WhatsApp-Gespräche überschreite?</summary><div class="ans"><p>Der Assistent antwortet weiter. Gespräche über das Limit des Plans hinaus kosten 15 € je 100.</p>',
  fconv_new='<summary>Und wenn ich die schriftlichen Gespräche überschreite?</summary><div class="ans"><p>Der Assistent antwortet weiter. Gespräche über das Limit des Plans hinaus (WhatsApp, Instagram und Messenger zusammen) kosten 15 € je 100.</p>',
  fdiff_re=r'<summary>Was ist der Unterschied zwischen Start, Pro und Pro \+ Website\?</summary><div class="ans"><p>.*?</p>',
  fdiff_new='<summary>Was ist der Unterschied zwischen Studio, Pro und Pro + Website?</summary><div class="ans"><p>Studio beantwortet Anrufe, mit 400 Minuten im Monat und dem Kalender inklusive: Diesen Plan empfehlen wir Zahnarztpraxen. Pro ergänzt die schriftlichen Kanäle (WhatsApp ab Januar 2027, Instagram und Messenger kommen 2027), mit 600 Minuten und 500 Gesprächen im Monat und Kalender Plus. Pro + Website hat 800 Minuten und die Präsentations-Website inklusive. Wenn Sie unsicher sind, testen Sie die Demo, und wir sprechen in einem kurzen Gespräch darüber.</p>',
  fann_old='Ja: Mit Start zahlen Sie 10 Monate und erhalten 12; mit Pro und Pro + Website zahlen Sie 11 Monate und erhalten 12.',
  fann_new='Ja: Mit Studio, Pro und Pro + Website zahlen Sie 11 Monate und erhalten 12.',
  inizio_old='<li><b>Start:</b> Die Dienste starten ab Januar 2027.', inizio_new='<li><b>Beginn:</b> Die Dienste starten ab Januar 2027.',
),
}

NASCOSTO = '\n        <!-- Start WhatsApp: nascosto dal listino v2.2 (10/11/2026). Non cancellare: si riaccende solo se William lo decide (togliere «hidden»). -->\n        '

def blocco(text, L):
    t = T[L]
    # 1. i tre piani: Studio (evidenziato), Pro, Pro + sito; lo Start resta in fondo, nascosto
    m = re.search(r'      <h3 class="ph">[^\n]*\n      <div class="pk">\n(.*?)\n      </div>\n', text, re.S)
    if not m: raise SystemExit(f'piani non trovati ({L})')
    righe = m.group(1).split('\n')
    start = [r for r in righe if 'Start WhatsApp' in r]
    if len(start) != 1: raise SystemExit(f'Start non trovato ({L})')
    start_nascosto = start[0].strip().replace('<article>', '<article hidden data-piano="start-whatsapp">', 1)
    nuovo = (f'      {t["ph"]}\n      <div class="pk">\n        {t["studio"]}\n        {t["pro"]}\n        {t["prosito"]}'
             f'{NASCOSTO}{start_nascosto}\n      </div>\n')
    text = text[:m.start()] + nuovo + text[m.end():]
    # link al PDF subito dopo la nota sull'attivazione
    i = text.index(nuovo) + len(nuovo)
    j = text.index('\n', i) + 1  # riga della nota sull'attivazione
    text = text[:j] + '      ' + t['pdf'] + '\n' + text[j:]
    for k in ('min', 'conv', 'meta', 'es', 'att', 'ann', 'sito', 'fconv', 'fann', 'inizio'):
        if t.get(k + '_old'): text = rep(t[k + '_old'], t[k + '_new'], text, f'{k} ({L})')
    text = sub1(t['fdiff_re'], t['fdiff_new'], text, re.S, f'faq differenza ({L})')
    return text

# blocchi: IT nella sezione #prezzi, EN e DE nei template
if not GIA:
    a = s.index('<section class="alt" id="prezzi"'); b = s.index('<template id="tpl-price-en">')
    c = s.index('<template id="tpl-price-de">'); d = s.index('</template>', c)
    s = s[:a] + blocco(s[a:b], 'it') + blocco(s[b:c], 'en') + blocco(s[c:d], 'de') + s[d:]

# ---------------------------------------------------------------- agende (IT nel DOM, EN/DE nel dizionario)
AG = [
 ('<p class="ag-price">Start, Pro e Pro + sito</p>', '<p class="ag-price">Studio, Pro e Pro + sito</p>'),
 ('Inclusa in Pro e Pro + sito · 29 €/mese con lo Start', 'Inclusa in Pro e Pro + sito · 29 €/mese con lo Studio'),
 ('<p class="ag-fine">Con lo Start: attivazione 49 €', '<p class="ag-fine">Con lo Studio: attivazione 49 €'),
 ('<p class=\\"ag-price\\">Start, Pro and Pro + website</p>', '<p class=\\"ag-price\\">Studio, Pro and Pro + website</p>'),
 ('Included in Pro and Pro + website · €29/month with Start', 'Included in Pro and Pro + website · €29/month with Studio'),
 ('<p class=\\"ag-fine\\">With Start: one-off activation €49', '<p class=\\"ag-fine\\">With Studio: one-off activation €49'),
 ('<p class=\\"ag-price\\">Start, Pro und Pro + Website</p>', '<p class=\\"ag-price\\">Studio, Pro und Pro + Website</p>'),
 ('Pro und Pro + Website enthalten · 29 €/Monat mit Start', 'Pro und Pro + Website enthalten · 29 €/Monat mit Studio'),
 ('<p class=\\"ag-fine\\">Mit Start: einmalige Aktivierung 49 €', '<p class=\\"ag-fine\\">Mit Studio: einmalige Aktivierung 49 €'),
 # calcolatore delle richieste perse: confronto con il piano d'ingresso nuovo
 ('cCmp:"Per confronto, il piano Pro costa 189 € al mese."', 'cCmp:"Per confronto, il piano Studio costa 129 € al mese e il Pro 189 €."'),
 ('cCmp:"For comparison, the Pro plan costs €189 a month."', 'cCmp:"For comparison, the Studio plan costs €129 a month and Pro €189."'),
 ('cCmp:"Zum Vergleich: der Pro-Tarif kostet 189 € im Monat."', 'cCmp:"Zum Vergleich: Der Studio-Tarif kostet 129 € im Monat, Pro 189 €."'),
 # dati strutturati per Google
 ('"priceRange":"da 79 €/mese, prezzo finale senza IVA (regime forfettario)"', '"priceRange":"da 129 €/mese, prezzo finale, IVA non applicata (regime forfettario)"'),
]
if not GIA:
    for o, n in AG: s = rep(o, n, s)
    P.write_text(s, encoding='utf-8')
    print('listino v2.2 applicato')

# ---------------------------------------------------------------- sezione «canali» (stesse classi: sec-head, cat, cat-who)
s = P.read_text(encoding='utf-8')
if 'id="canali"' not in s:
    CANALI = '''  <section id="canali" aria-labelledby="canali-t">
    <div class="wrap">
      <div class="sec-head" data-i18n="can-head"><p class="eyebrow">Canali</p><h2 id="canali-t">Dove risponde l'assistente</h2><p class="lead">Lo stesso assistente, con le stesse regole, sui canali che usano i Suoi clienti. Accanto a ogni canale trova quando è disponibile.</p></div>
      <div class="cat" data-i18n="can-cards"><article><h4>Telefono</h4><p class="cat-who">Disponibile · attivazioni da gennaio 2027</p><p>Risponde alle chiamate, fissa gli appuntamenti nell'Agenda e passa a una persona quando serve. In tutti i piani: Studio, Pro e Pro + sito.</p></article><article><h4>WhatsApp</h4><p class="cat-who">Da gennaio 2027</p><p>Conversazioni con i clienti nel Pro e nel Pro + sito. Con lo Studio: invio di file e indicazioni.</p></article><article><h4>Instagram</h4><p class="cat-who">In arrivo nel 2027 · serve l'approvazione di Meta</p><p>Risposte ai messaggi diretti nel Pro e nel Pro + sito. Sullo Studio come canale in più, a 19 €/mese.</p></article><article><h4>Messenger</h4><p class="cat-who">In arrivo nel 2027 · serve l'approvazione di Meta</p><p>Risposte ai messaggi della pagina Facebook nel Pro e nel Pro + sito. Sullo Studio come canale in più, a 19 €/mese.</p></article></div>
    </div>
  </section>

'''
    s = rep('  <section id="agende" aria-labelledby="agende-t">', CANALI + '  <section id="agende" aria-labelledby="agende-t">', s)
    P.write_text(s, encoding='utf-8'); print('sezione canali aggiunta')
