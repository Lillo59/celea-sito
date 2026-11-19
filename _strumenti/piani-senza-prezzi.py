# Decisione d20261119-william-prova-10-giorni-niente-prezzi-pubblici: nessun prezzo in pubblico, prova gratis per 10 giorni.
# Riscrive la sezione «Prezzi» (ora «Piani») di index.html in IT, EN e DE: restano piani, opzioni, pacchetti e servizi
# con la loro descrizione; al posto degli importi «Preventivo su misura» / «su preventivo». Idempotente.
# Le versioni con i prezzi restano nel ramo con-prezzi-2026-11-19.
import pathlib, sys

P = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = P.read_text(encoding='utf-8')
if 'data-piani="senza-prezzi"' in s:
    print('sezione Piani già senza prezzi'); sys.exit(0)

T = {
'it': dict(
 eyebrow='Piani', h2='Tre piani, un preventivo su misura.',
 lead="Ogni attività è diversa: Le prepariamo un preventivo scritto su misura, senza impegno. Ci scriva a info@celea.it oppure chieda la prova gratuita.",
 start="Le attivazioni partono da gennaio 2027; la demo si prova da subito.",
 trial_k='Prova gratuita', trial_h='Prova gratis per 10 giorni.',
 trial_p="Prova gratuita di 10 giorni, fino a 100 minuti di telefonate. Non chiediamo carta né pagamento e alla fine non si rinnova da sola: continua solo se firma il contratto. Configuriamo l'assistente sulla Sua attività; la prova si prenota da subito e parte da gennaio 2027.",
 fond_k='Clienti fondatori · 20 posti', fond_h='Cerchiamo 20 attività con cui partire.',
 fond_p="Clienti fondatori: i primi 20 clienti non pagano l'attivazione e tengono lo stesso prezzo per 24 mesi. Per ogni nuova attività che ci presenta riceve un mese gratis (fino a 3 all'anno). Valida fino al 31 marzo 2027 o fino al ventesimo cliente. Se vuole, ci lascia un breve parere: solo se lo desidera, mai in cambio del prezzo. Si candida con il modulo «Prenoti la prova gratuita» in fondo alla pagina, scrivendo «cliente fondatore».",
 ph='I tre piani dell\'assistente <small>uguali per tutti i settori: studi dentistici, cliniche veterinarie, agenzie immobiliari, strutture ricettive e impiantisti.</small>',
 quote='Preventivo su misura',
 studio="L'assistente risponde al telefono ai Suoi clienti quando Lei non può, anche fuori orario, negli orari che sceglie Lei: informazioni, appuntamenti nell'Agenda, passaggio a una persona quando serve.",
 studio_li=["Telefono: 400 minuti di telefonate al mese", "Agenda inclusa: 1 calendario, fino a 2 tipi di appuntamento", "Invio di file e indicazioni su WhatsApp (da gennaio 2027)", "Italiano, inglese e tedesco inclusi"],
 pro="Lo stesso assistente al telefono e, da gennaio 2027, sui canali scritti, con voce standard inclusa.",
 pro_li=["Telefono: 600 minuti di telefonate al mese", "500 conversazioni al mese su WhatsApp (da gennaio 2027), Instagram e Messenger (in arrivo nel 2027): i canali scritti si sommano nello stesso tetto", "Agenda Plus inclusa", "Riconoscimento di chi richiama (in arrivo nel 2027)", "Importazione dei contatti da file (CSV) ed esportazione delle richieste su Google Sheets (in arrivo nel 2027)", "Italiano, inglese e tedesco inclusi"],
 prosito="Tutto il Pro con più minuti, più un sito vetrina di 5 pagine per la Sua attività, con l'assistente già integrato, hosting e manutenzione.",
 prosito_li=["Telefono: 800 minuti di telefonate al mese", "500 conversazioni sui canali scritti, come nel Pro (da gennaio 2027)", "Sito vetrina incluso, con hosting e manutenzione", "Italiano, inglese e tedesco inclusi"],
 btn_q='Chieda un preventivo su misura', btn_t='Prova gratis per 10 giorni',
 note="L'attivazione comprende la configurazione dell'assistente sulle regole della Sua attività e la prova insieme prima della partenza.",
 opz_h='Opzioni a scelta, nel preventivo <small>solo se le usa o le sceglie Lei</small>',
 opz=["Minuti di telefonata oltre quelli inclusi, in ogni piano", "Canale in più sullo Studio: Instagram o Messenger (in arrivo nel 2027)", "Promemoria con telefonata, solo con Pro e Pro + sito (in arrivo)", "Voce premium con il Pro e con il Pro + sito, ancora più naturale, da scegliere dopo averla ascoltata (la voce standard resta inclusa)", "Seconda sede o secondo numero, con gli stessi minuti e conversazioni inclusi", "Conversazioni sui canali scritti oltre il tetto del piano (WhatsApp da gennaio 2027, Instagram e Messenger in arrivo nel 2027)"],
 opz_note="Altre lingue oltre a italiano, inglese e tedesco: le aggiungiamo senza costi in più, solo dopo una nostra prova che ne garantisca la qualità.",
 meta_h='I messaggi WhatsApp li paga a Meta, senza nostri ricarichi.',
 meta_p="WhatsApp appartiene a Meta. Da gennaio 2027, con WhatsApp attivo, i messaggi li paga Lei direttamente a Meta con la Sua carta, senza ricarico da parte nostra. Le diremo la stima per la Sua attività prima di partire, sul tariffario di Meta in vigore.",
 cond_h='Le condizioni, chiare',
 cond=["<b>Prova gratuita:</b> 10 giorni, fino a 100 minuti di telefonate, con l'assistente configurato sulla Sua attività. Non chiediamo carta né pagamento e alla fine non si rinnova da sola: continua solo se firma il contratto. Parte da gennaio 2027.", "<b>Preventivo:</b> scritto, su misura e senza impegno, con tutto ciò che è compreso e le opzioni scelte.", "<b>Durata:</b> mese per mese. Dopo il terzo mese si può smettere con 30 giorni di preavviso.", "<b>Pausa stagionale:</b> Pausa stagionale per le strutture ricettive: nei mesi di chiusura resta acceso solo WhatsApp (da gennaio 2027). Condizioni nel preventivo.", "<b>Partenza:</b> le attivazioni partono da gennaio 2027. La demo si prova subito."],
 pac_h="Pacchetti completi: l'assistente con i servizi digitali <small>su preventivo</small>",
 sp='su preventivo',
 pac=[("Pro + Google", "Tutti i settori", "Assistente Pro e Google &amp; Recensioni: scheda Google curata, 6 post al mese, risposta alle recensioni."), ("Pro + Social", "Tutti i settori", "Assistente Pro e Social Start: 1 canale, 12 post con grafica, 8 storie e 2 video brevi al mese."), ("Pro Crescita · Ospitalità Crescita", "Tutti i settori · B&amp;B, case vacanza e hotel", "Assistente Pro, Google &amp; Recensioni e Social Start."), ("Studio Sorridente", "Studi dentistici", "Assistente Pro, Google &amp; Recensioni, Social Start e campagne WhatsApp di richiamo (da gennaio 2027)."), ("Agenzia Crescita", "Agenzie immobiliari", "Assistente Pro, ricontatto automatico delle richieste, social su 2 canali con 4 video brevi al mese, assistente anche sul sito.")],
 pac_note="Ogni pacchetto si compone nel preventivo, insieme ai servizi scelti. I messaggi Meta (da gennaio 2027) restano a parte, senza ricarichi.",
 svc_h='Servizi digitali singoli <small>su preventivo</small>',
 svc=[("Social", ["Social Start · 1 canale, 12 post, 8 storie, 2 video brevi", "Social Plus · 2 canali, 16 post, 12 storie, 4 video brevi", "Social Pro · 3 canali, 24 post, 16 storie, 8 video brevi"]), ("Siti web", ["Landing page · 1 pagina, hosting e collegamento del Suo dominio", "Sito vetrina · 5 pagine, SEO di base", "Sito premium · 10 pagine in italiano, inglese e tedesco"]), ("Google e recensioni", ["Google &amp; Recensioni · scheda Google, 6 post al mese, risposte alle recensioni", "SEO locale completo · 2 articoli al mese"]), ("Clienti già acquisiti", ["Newsletter mensile", "Campagne WhatsApp ai clienti (da gennaio 2027; i messaggi li paga Lei direttamente a Meta)", "Ricontatto automatico delle richieste", "Assistente anche sul sito, in aggiunta allo Studio o al Pro"])],
 svc_note="Il dominio è sempre intestato a Lei. Per i clienti fondatori il prezzo dei servizi resta bloccato 24 mesi e il primo mese del Social Start è gratis. Il preventivo su misura lo prepariamo per email.",
 faq_h='Domande sulla prova e sul preventivo',
 faq=[("Posso provarlo prima di decidere?", "Sì. Oltre alla demo che prova qui subito, c'è una prova gratuita di 10 giorni con l'assistente configurato sulla Sua attività, fino a 100 minuti di telefonate. Non chiediamo carta né pagamento e alla fine non si rinnova da sola: continua solo se firma il contratto. Parte da gennaio 2027."),
      ("Chi sono i clienti fondatori?", "Le prime 20 attività che partono con Celea, entro il 31 marzo 2027: non pagano l'attivazione e tengono lo stesso prezzo per 24 mesi. Ci si candida con il modulo «Prenoti la prova gratuita» in fondo alla pagina."),
      ("Quanto costa? Ci sono costi nascosti?", "Ogni attività è diversa: Le prepariamo un preventivo scritto su misura, senza impegno. Ci scriva a info@celea.it oppure chieda la prova gratuita. Nel preventivo trova tutto ciò che paga: niente costi nascosti."),
      ("Cosa succede se supero i minuti di telefonata?", "L'assistente continua a rispondere: ogni richiesta riceve una risposta o passa a una persona. I minuti oltre quelli inclusi sono indicati nel preventivo e li trova nel report mensile."),
      ("E se supero le conversazioni scritte?", "L'assistente continua a rispondere. Le conversazioni oltre il tetto del piano (WhatsApp da gennaio 2027, Instagram e Messenger in arrivo nel 2027) sono indicate nel preventivo."),
      ("Perché i messaggi WhatsApp li pagherò a Meta e non a voi?", "Da gennaio 2027, con WhatsApp attivo, i messaggi li paga Lei direttamente a Meta con la Sua carta, senza ricarico da parte nostra: così paga il prezzo di Meta e vede la spesa esatta nel Suo account. Le diremo la stima per la Sua attività prima di partire, sul tariffario di Meta in vigore."),
      ("Che differenza c'è tra Studio, Pro e Pro + sito?", "Lo Studio risponde al telefono, con 400 minuti al mese e l'Agenda inclusa. Il Pro aggiunge i canali scritti (WhatsApp da gennaio 2027, Instagram e Messenger in arrivo nel 2027), con 600 minuti e 500 conversazioni al mese e l'Agenda Plus. Il Pro + sito ha 800 minuti e il sito vetrina compreso. Se non sa quale scegliere, provi la demo e ne parliamo in una breve chiamata."),
      ("Le lingue straniere costano in più?", "No. Italiano, inglese e tedesco sono inclusi in ogni piano. Altre lingue le aggiungiamo senza costi in più, solo dopo una nostra prova che ne garantisca la qualità."),
      ("Quanto devo restare? Posso fermarmi d'estate o d'inverno?", "Si paga mese per mese; dopo il terzo mese può smettere con 30 giorni di preavviso. Pausa stagionale per le strutture ricettive: nei mesi di chiusura resta acceso solo WhatsApp (da gennaio 2027). Condizioni nel preventivo.")],
 pend_h='Prima di decidere, provi come risponde.',
 pend_p="La demo qui sopra si prova subito. Poi può chiedere la prova gratis per 10 giorni sulla Sua attività (da gennaio 2027) o un preventivo su misura. Per parlarne, una breve chiamata con William.",
 pend_a='Prova la demo', pend_b='Prenoti una breve chiamata'),
'en': dict(
 eyebrow='Plans', h2='Three plans, a tailored quote.',
 lead="Every business is different: we prepare a written, tailored quote with no obligation. Write to info@celea.it or ask for the free trial.",
 start="Services go live from January 2027; the demo is available right away.",
 trial_k='Free trial', trial_h='Free 10-day trial.',
 trial_p="10-day free trial, up to 100 minutes of calls. No card, no payment, no automatic renewal: it continues only if you sign the contract. We set up the assistant for your business; you can book the trial right away and it starts from January 2027.",
 fond_k='Founding customers · 20 places', fond_h='We are looking for 20 businesses to start with.',
 fond_p="Founding customers: the first 20 customers pay no set-up fee and keep the same price for 24 months. For every new business you introduce to us you get one month free (up to 3 a year). Valid until 31 March 2027 or until the twentieth customer. If you like, you leave us a short review: only if you want to, never in exchange for the price. Apply with the «Book your free trial» form at the bottom of the page, writing «founding customer».",
 ph='The three assistant plans <small>the same for every sector: dental practices, veterinary clinics, real estate agencies, hospitality and plumbing and electrical firms.</small>',
 quote='Tailored quote',
 studio="Your assistant answers your customers on the phone when you can't, also outside opening hours, at the times you choose: information, appointments in the Calendar and hand-over to a person when needed.",
 studio_li=["Phone: 400 call minutes a month", "Calendar included: 1 calendar, up to 2 appointment types", "Sending files and directions on WhatsApp (from January 2027)", "Italian, English and German included"],
 pro="The same assistant on the phone and, from January 2027, on the written channels, with a standard voice included.",
 pro_li=["Phone: 600 call minutes a month", "500 conversations a month on WhatsApp (from January 2027), Instagram and Messenger (coming in 2027): the written channels share the same limit", "Calendar Plus included", "Recognising returning callers (coming in 2027)", "Importing contacts from a file (CSV) and exporting enquiries to Google Sheets (coming in 2027)", "Italian, English and German included"],
 prosito="Everything in Pro with more minutes, plus a 5-page showcase website for your business with the assistant built in, hosting and maintenance.",
 prosito_li=["Phone: 800 call minutes a month", "500 conversations on the written channels, as in Pro (from January 2027)", "Showcase website included, with hosting and maintenance", "Italian, English and German included"],
 btn_q='Ask for a tailored quote', btn_t='Free trial for 10 days',
 note="Set-up includes configuring the assistant to your business rules and a joint test before going live.",
 opz_h='Optional extras, in your quote <small>only if you use or choose them</small>',
 opz=["Call minutes beyond those included, on every plan", "Extra channel on Studio: Instagram or Messenger (coming in 2027)", "Reminders by phone call, only with Pro and Pro + website (coming soon)", "Premium voice with Pro and Pro + website, even more natural, chosen after you have heard it (the standard voice stays included)", "Second location or second number, with the same included minutes and conversations", "Conversations on the written channels beyond the plan limit (WhatsApp from January 2027, Instagram and Messenger coming in 2027)"],
 opz_note="Languages other than Italian, English and German: we add them at no extra cost, only after our own test confirms the quality.",
 meta_h='You pay WhatsApp messages to Meta, with no mark-up from us.',
 meta_p="WhatsApp belongs to Meta. From January 2027, with WhatsApp active, you pay Meta directly for messages with your own card, with no mark-up from us. We will give you an estimate for your business before you start, based on Meta's current rates.",
 cond_h='The terms, clearly',
 cond=["<b>Free trial:</b> 10 days, up to 100 minutes of calls, with the assistant set up for your business. No card, no payment, no automatic renewal: it continues only if you sign the contract. It starts from January 2027.", "<b>Quote:</b> written, tailored and with no obligation, with everything included and the extras you choose.", "<b>Term:</b> month by month. After the third month you can stop with 30 days' notice.", "<b>Seasonal pause:</b> Seasonal pause for accommodation: in closed months only WhatsApp stays on (from January 2027). Terms in your quote.", "<b>Go-live:</b> services go live from January 2027. The demo is available right away."],
 pac_h='Complete packages: the assistant with digital services <small>on quote</small>',
 sp='on quote',
 pac=[("Pro + Google", "All sectors", "Pro assistant and Google &amp; Reviews: Google profile management, 6 posts a month, replies to reviews."), ("Pro + Social", "All sectors", "Pro assistant and Social Start: 1 channel, 12 designed posts, 8 stories and 2 short videos a month."), ("Pro Growth · Hospitality Growth", "All sectors · B&amp;Bs, holiday homes and hotels", "Pro assistant, Google &amp; Reviews and Social Start."), ("Studio Sorridente", "Dental practices", "Pro assistant, Google &amp; Reviews, Social Start and WhatsApp recall campaigns (from January 2027)."), ("Agenzia Crescita", "Real estate agencies", "Pro assistant, automatic follow-up of enquiries, social media on 2 channels with 4 short videos a month, assistant on your website too.")],
 pac_note="Each package is put together in your quote, with the services you choose. Meta messages (from January 2027) remain separate, with no mark-up.",
 svc_h='Individual digital services <small>on quote</small>',
 svc=[("Social media", ["Social Start · 1 channel, 12 posts, 8 stories, 2 short videos", "Social Plus · 2 channels, 16 posts, 12 stories, 4 short videos", "Social Pro · 3 channels, 24 posts, 16 stories, 8 short videos"]), ("Websites", ["Landing page · 1 page, hosting and connection of your domain", "Showcase website · 5 pages, basic SEO", "Premium website · 10 pages in Italian, English and German"]), ("Google and reviews", ["Google &amp; Reviews · Google profile, 6 posts a month, replies to reviews", "Full local SEO · 2 articles a month"]), ("Existing customers", ["Monthly newsletter", "WhatsApp campaigns to your customers (from January 2027; you pay the messages directly to Meta)", "Automatic follow-up of enquiries", "Assistant on your website too, in addition to Studio or Pro"])],
 svc_note="The domain is always registered in your name. For founding customers service prices stay locked for 24 months and the first month of Social Start is free. We prepare the tailored quote by email.",
 faq_h='Questions about the trial and the quote',
 faq=[("Can I try it before deciding?", "Yes. Besides the demo you can try here right away, there is a 10-day free trial with the assistant set up for your business, up to 100 minutes of calls. No card, no payment, no automatic renewal: it continues only if you sign the contract. It starts from January 2027."),
      ("Who are the founding customers?", "The first 20 businesses that start with Celea, by 31 March 2027: they pay no set-up fee and keep the same price for 24 months. Apply with the «Book your free trial» form at the bottom of the page."),
      ("How much does it cost? Are there hidden costs?", "Every business is different: we prepare a written, tailored quote with no obligation. Write to info@celea.it or ask for the free trial. Your quote shows everything you pay: no hidden costs."),
      ("What happens if I go over my call minutes?", "The assistant keeps answering: every enquiry gets an answer or goes to a person. Minutes beyond those included are shown in your quote and in your monthly report."),
      ("And if I go over my written conversations?", "The assistant keeps answering. Conversations beyond the plan limit (WhatsApp from January 2027, Instagram and Messenger coming in 2027) are shown in your quote."),
      ("Why will I pay WhatsApp messages to Meta and not to you?", "From January 2027, with WhatsApp active, you pay Meta directly for messages with your own card, with no mark-up from us: you pay Meta's price and see the exact spend in your own account. We will give you an estimate for your business before you start, based on Meta's current rates."),
      ("What is the difference between Studio, Pro and Pro + website?", "Studio answers the phone, with 400 minutes a month and the Calendar included. Pro adds the written channels (WhatsApp from January 2027, Instagram and Messenger coming in 2027), with 600 minutes and 500 conversations a month and Calendar Plus. Pro + website has 800 minutes and the showcase website included. If you are not sure which to choose, try the demo and let's talk in a short call."),
      ("Do foreign languages cost extra?", "No. Italian, English and German are included in every plan. We add other languages at no extra cost, only after our own test confirms the quality."),
      ("How long do I have to stay? Can I pause in summer or winter?", "You pay month by month; after the third month you can stop with 30 days' notice. Seasonal pause for accommodation: in closed months only WhatsApp stays on (from January 2027). Terms in your quote.")],
 pend_h='Before you decide, see how it answers.',
 pend_p="The demo above works right away. Then you can ask for the free 10-day trial for your business (from January 2027) or for a tailored quote. To talk it through, a short call with William.",
 pend_a='Try the demo', pend_b='Book a short call'),
'de': dict(
 eyebrow='Tarife', h2='Drei Tarife, ein Angebot nach Maß.',
 lead="Jeder Betrieb ist anders: Wir erstellen Ihnen ein schriftliches, unverbindliches Angebot nach Maß. Schreiben Sie an info@celea.it oder fragen Sie den kostenlosen Test an.",
 start="Die Dienste starten ab Januar 2027; die Demo können Sie sofort testen.",
 trial_k='Kostenloser Test', trial_h='10 Tage kostenlos testen.',
 trial_p="10 Tage kostenlos testen, bis zu 100 Gesprächsminuten. Keine Karte, keine Zahlung, keine automatische Verlängerung: Es geht nur weiter, wenn Sie den Vertrag unterschreiben. Wir richten den Assistenten für Ihren Betrieb ein; der Test ist ab sofort buchbar und beginnt ab Januar 2027.",
 fond_k='Gründungskunden · 20 Plätze', fond_h='Wir suchen 20 Betriebe für den Start.',
 fond_p="Gründungskunden: Die ersten 20 Kunden zahlen keine Einrichtungsgebühr und behalten 24 Monate lang denselben Preis. Für jeden neuen Betrieb, den Sie uns vorstellen, erhalten Sie einen Monat gratis (bis zu 3 pro Jahr). Gültig bis 31. März 2027 oder bis zum zwanzigsten Kunden. Wenn Sie möchten, hinterlassen Sie uns eine kurze Bewertung: nur wenn Sie es wollen, nie im Tausch gegen den Preis. Bewerbung mit dem Formular «Kostenlose Testphase buchen» unten auf der Seite, mit dem Hinweis «Gründungskunde».",
 ph='Die drei Tarife des Assistenten <small>gleich für alle Branchen: Zahnarztpraxen, Tierarztpraxen, Immobilienagenturen, Unterkünfte und Installateure.</small>',
 quote='Angebot nach Maß',
 studio="Der Assistent beantwortet die Anrufe Ihrer Kunden, wenn Sie nicht können, auch außerhalb der Öffnungszeiten, zu den Zeiten, die Sie festlegen: Informationen, Termine im Kalender und Weitergabe an eine Person, wenn nötig.",
 studio_li=["Telefon: 400 Telefonminuten im Monat", "Kalender inklusive: 1 Kalender, bis zu 2 Terminarten", "Versand von Dateien und Wegbeschreibungen auf WhatsApp (ab Januar 2027)", "Italienisch, Englisch und Deutsch inklusive"],
 pro="Derselbe Assistent am Telefon und, ab Januar 2027, auf den schriftlichen Kanälen, Standardstimme inklusive.",
 pro_li=["Telefon: 600 Telefonminuten im Monat", "500 Gespräche im Monat auf WhatsApp (ab Januar 2027), Instagram und Messenger (kommt 2027): Die schriftlichen Kanäle teilen sich dasselbe Limit", "Kalender Plus inklusive", "Wiedererkennung von Rückrufern (kommt 2027)", "Import von Kontakten aus einer Datei (CSV) und Export der Anfragen nach Google Sheets (kommt 2027)", "Italienisch, Englisch und Deutsch inklusive"],
 prosito="Alles aus Pro mit mehr Minuten, dazu eine Präsentations-Website mit 5 Seiten für Ihren Betrieb, mit integriertem Assistenten, Hosting und Wartung.",
 prosito_li=["Telefon: 800 Telefonminuten im Monat", "500 Gespräche auf den schriftlichen Kanälen, wie bei Pro (ab Januar 2027)", "Präsentations-Website inklusive, mit Hosting und Wartung", "Italienisch, Englisch und Deutsch inklusive"],
 btn_q='Angebot nach Maß anfragen', btn_t='10 Tage kostenlos testen',
 note="Die Einrichtung umfasst die Konfiguration des Assistenten nach den Regeln Ihres Betriebs und einen gemeinsamen Test vor dem Start.",
 opz_h='Optionen auf Wunsch, im Angebot <small>nur wenn Sie sie nutzen oder wählen</small>',
 opz=["Telefonminuten über die enthaltenen hinaus, in jedem Tarif", "Zusätzlicher Kanal bei Studio: Instagram oder Messenger (kommt 2027)", "Erinnerungen per Anruf, nur mit Pro und Pro + Website (kommt bald)", "Premium-Stimme mit Pro und Pro + Website, noch natürlicher, wählbar nach dem Probehören (die Standardstimme bleibt inklusive)", "Zweiter Standort oder zweite Nummer, mit denselben enthaltenen Minuten und Gesprächen", "Gespräche auf den schriftlichen Kanälen über das Limit des Tarifs hinaus (WhatsApp ab Januar 2027, Instagram und Messenger kommen 2027)"],
 opz_note="Weitere Sprachen außer Italienisch, Englisch und Deutsch: Wir fügen sie ohne Aufpreis hinzu, erst nachdem ein eigener Test die Qualität bestätigt hat.",
 meta_h='WhatsApp-Nachrichten zahlen Sie an Meta, ohne Aufschlag von uns.',
 meta_p="WhatsApp gehört Meta. Ab Januar 2027, mit aktivem WhatsApp, zahlen Sie die Nachrichten direkt an Meta mit Ihrer Karte, ohne Aufschlag von uns. Vor dem Start nennen wir Ihnen eine Schätzung für Ihren Betrieb nach den dann gültigen Meta-Tarifen.",
 cond_h='Die Bedingungen, klar',
 cond=["<b>Kostenloser Test:</b> 10 Tage, bis zu 100 Gesprächsminuten, mit dem Assistenten für Ihren Betrieb eingerichtet. Keine Karte, keine Zahlung, keine automatische Verlängerung: Es geht nur weiter, wenn Sie den Vertrag unterschreiben. Beginn ab Januar 2027.", "<b>Angebot:</b> schriftlich, nach Maß und unverbindlich, mit allem, was enthalten ist, und den gewählten Optionen.", "<b>Laufzeit:</b> monatlich. Nach dem dritten Monat können Sie mit 30 Tagen Frist kündigen.", "<b>Saisonpause:</b> Saisonpause für Unterkünfte: In den geschlossenen Monaten bleibt nur WhatsApp aktiv (ab Januar 2027). Bedingungen im Angebot.", "<b>Beginn:</b> Die Dienste starten ab Januar 2027. Die Demo können Sie sofort testen."],
 pac_h='Komplettpakete: der Assistent mit digitalen Diensten <small>auf Anfrage</small>',
 sp='auf Anfrage',
 pac=[("Pro + Google", "Alle Branchen", "Pro-Assistent und Google &amp; Bewertungen: Pflege des Google-Profils, 6 Beiträge im Monat, Antworten auf Bewertungen."), ("Pro + Social", "Alle Branchen", "Pro-Assistent und Social Start: 1 Kanal, 12 gestaltete Beiträge, 8 Storys und 2 kurze Videos im Monat."), ("Pro Wachstum · Gastgeber Wachstum", "Alle Branchen · B&amp;B, Ferienwohnungen und Hotels", "Pro-Assistent, Google &amp; Bewertungen und Social Start."), ("Studio Sorridente", "Zahnarztpraxen", "Pro-Assistent, Google &amp; Bewertungen, Social Start und WhatsApp-Recall-Kampagnen (ab Januar 2027)."), ("Agenzia Crescita", "Immobilienagenturen", "Pro-Assistent, automatisches Nachfassen von Anfragen, Social Media auf 2 Kanälen mit 4 kurzen Videos im Monat, Assistent auch auf Ihrer Website.")],
 pac_note="Jedes Paket wird im Angebot zusammengestellt, mit den gewählten Diensten. Meta-Nachrichten (ab Januar 2027) bleiben separat, ohne Aufschlag.",
 svc_h='Einzelne digitale Dienste <small>auf Anfrage</small>',
 svc=[("Social Media", ["Social Start · 1 Kanal, 12 Beiträge, 8 Storys, 2 kurze Videos", "Social Plus · 2 Kanäle, 16 Beiträge, 12 Storys, 4 kurze Videos", "Social Pro · 3 Kanäle, 24 Beiträge, 16 Storys, 8 kurze Videos"]), ("Websites", ["Landingpage · 1 Seite, Hosting und Verbindung Ihrer Domain", "Präsentations-Website · 5 Seiten, Basis-SEO", "Premium-Website · 10 Seiten auf Italienisch, Englisch und Deutsch"]), ("Google und Bewertungen", ["Google &amp; Bewertungen · Google-Profil, 6 Beiträge im Monat, Antworten auf Bewertungen", "Komplettes lokales SEO · 2 Artikel im Monat"]), ("Bestehende Kunden", ["Monatlicher Newsletter", "WhatsApp-Kampagnen an Ihre Kunden (ab Januar 2027; die Nachrichten zahlen Sie direkt an Meta)", "Automatisches Nachfassen von Anfragen", "Assistent auch auf Ihrer Website, zusätzlich zu Studio oder Pro"])],
 svc_note="Die Domain läuft immer auf Ihren Namen. Für Gründungskunden bleiben die Preise der Dienste 24 Monate fest, und der erste Monat Social Start ist gratis. Das Angebot nach Maß erstellen wir per E-Mail.",
 faq_h='Fragen zum Test und zum Angebot',
 faq=[("Kann ich es testen, bevor ich mich entscheide?", "Ja. Neben der Demo, die Sie hier sofort testen, gibt es einen kostenlosen 10-Tage-Test mit dem für Ihren Betrieb eingerichteten Assistenten, bis zu 100 Gesprächsminuten. Keine Karte, keine Zahlung, keine automatische Verlängerung: Es geht nur weiter, wenn Sie den Vertrag unterschreiben. Beginn ab Januar 2027."),
      ("Wer sind die Gründungskunden?", "Die ersten 20 Betriebe, die bis zum 31. März 2027 mit Celea starten: Sie zahlen keine Einrichtungsgebühr und behalten 24 Monate lang denselben Preis. Bewerbung mit dem Formular «Kostenlose Testphase buchen» unten auf der Seite."),
      ("Was kostet es? Gibt es versteckte Kosten?", "Jeder Betrieb ist anders: Wir erstellen Ihnen ein schriftliches, unverbindliches Angebot nach Maß. Schreiben Sie an info@celea.it oder fragen Sie den kostenlosen Test an. Im Angebot steht alles, was Sie zahlen: keine versteckten Kosten."),
      ("Was passiert, wenn ich die Telefonminuten überschreite?", "Der Assistent antwortet weiter: Jede Anfrage bekommt eine Antwort oder geht an einen Menschen. Minuten über die enthaltenen hinaus stehen im Angebot und in Ihrem Monatsbericht."),
      ("Und wenn ich die schriftlichen Gespräche überschreite?", "Der Assistent antwortet weiter. Gespräche über das Limit des Tarifs hinaus (WhatsApp ab Januar 2027, Instagram und Messenger kommen 2027) stehen im Angebot."),
      ("Warum zahle ich die WhatsApp-Nachrichten künftig an Meta und nicht an Sie?", "Ab Januar 2027, mit aktivem WhatsApp, zahlen Sie die Nachrichten direkt an Meta mit Ihrer Karte, ohne Aufschlag von uns: So zahlen Sie den Preis von Meta und sehen die genauen Ausgaben in Ihrem eigenen Konto. Vor dem Start nennen wir Ihnen eine Schätzung für Ihren Betrieb nach den dann gültigen Meta-Tarifen."),
      ("Was ist der Unterschied zwischen Studio, Pro und Pro + Website?", "Studio beantwortet Anrufe, mit 400 Minuten im Monat und dem Kalender inklusive. Pro ergänzt die schriftlichen Kanäle (WhatsApp ab Januar 2027, Instagram und Messenger kommen 2027), mit 600 Minuten und 500 Gesprächen im Monat und Kalender Plus. Pro + Website hat 800 Minuten und die Präsentations-Website inklusive. Wenn Sie unsicher sind, testen Sie die Demo, und wir sprechen in einem kurzen Gespräch darüber."),
      ("Kosten Fremdsprachen extra?", "Nein. Italienisch, Englisch und Deutsch sind in jedem Tarif enthalten. Weitere Sprachen fügen wir ohne Aufpreis hinzu, erst nachdem ein eigener Test die Qualität bestätigt hat."),
      ("Wie lange muss ich bleiben? Kann ich im Sommer oder Winter pausieren?", "Sie zahlen monatlich; nach dem dritten Monat können Sie mit 30 Tagen Frist kündigen. Saisonpause für Unterkünfte: In den geschlossenen Monaten bleibt nur WhatsApp aktiv (ab Januar 2027). Bedingungen im Angebot.")],
 pend_h='Bevor Sie sich entscheiden, testen Sie, wie er antwortet.',
 pend_p="Die Demo oben funktioniert sofort. Danach können Sie den kostenlosen 10-Tage-Test für Ihren Betrieb (ab Januar 2027) oder ein Angebot nach Maß anfragen. Für Fragen: ein kurzes Gespräch mit William.",
 pend_a='Demo testen', pend_b='Kurzes Gespräch buchen'),
}

def card(nome, t, desc, li):
    return (f'<article><p class="pk-n">{nome}</p><h4><b>{t["quote"]}</b></h4><p>{desc}</p><ul>'
            + ''.join(f'<li>{x}</li>' for x in li) + '</ul></article>')

def blocco(L):
    t = T[L]
    nomi = {'it': ('Studio', 'Pro', 'Pro + sito'), 'en': ('Studio', 'Pro', 'Pro + website'), 'de': ('Studio', 'Pro', 'Pro + Website')}[L]
    h = []
    h.append(f'      <div class="sec-head">\n        <p class="eyebrow">{t["eyebrow"]}</p>\n        <h2 id="prezzi-t">{t["h2"]}</h2>\n        <p class="lead">{t["lead"]}</p>\n        <p class="start"><span>{t["start"]}</span></p>\n      </div>\n')
    h.append(f'      <div class="pbox trial">\n        <p class="pk-n">{t["trial_k"]}</p>\n        <h3>{t["trial_h"]}</h3>\n        <p>{t["trial_p"]}</p>\n      </div>\n')
    h.append(f'      <div class="pbox trial">\n        <p class="pk-n">{t["fond_k"]}</p>\n        <h3>{t["fond_h"]}</h3>\n        <p>{t["fond_p"]}</p>\n      </div>\n')
    h.append(f'      <h3 class="ph" data-piani="senza-prezzi">{t["ph"]}</h3>\n      <div class="pk">\n'
             f'        {card(nomi[0], t, t["studio"], t["studio_li"])}\n        {card(nomi[1], t, t["pro"], t["pro_li"])}\n        {card(nomi[2], t, t["prosito"], t["prosito_li"])}\n      </div>\n')
    h.append(f'      <div class="cta-row"><a class="btn btn-accent" href="#contatti">{t["btn_q"]}</a><a class="btn btn-ghost" href="#contatti">{t["btn_t"]}</a></div>\n')
    h.append(f'      <p class="pnote">{t["note"]}</p>\n')
    h.append('      <div class="pcols">\n        <div class="pbox">\n          <h3>' + t['opz_h'] + '</h3>\n          <ul class="plist">\n'
             + ''.join(f'            <li><span>{x}</span></li>\n' for x in t['opz'])
             + f'          </ul>\n          <p class="pnote">{t["opz_note"]}</p>\n        </div>\n'
             + f'        <div class="pbox meta">\n          <h3>{t["meta_h"]}</h3>\n          <p>{t["meta_p"]}</p>\n        </div>\n      </div>\n')
    h.append('      <div class="pbox">\n        <h3>' + t['cond_h'] + '</h3>\n        <ul class="terms">\n' + ''.join(f'          <li>{x}</li>\n' for x in t['cond']) + '        </ul>\n      </div>\n')
    h.append(f'      <h3 class="ph">{t["pac_h"]}</h3>\n      <div class="cat">\n'
             + ''.join(f'        <article><h4>{a}</h4><p class="cat-who">{b}</p><p class="cat-p"><b>{t["sp"]}</b></p><p>{c}</p></article>\n' for a, b, c in t['pac'])
             + f'      </div>\n      <p class="pnote">{t["pac_note"]}</p>\n')
    h.append(f'      <h3 class="ph">{t["svc_h"]}</h3>\n      <div class="svc">\n'
             + ''.join('        <div><h4>' + g + '</h4><ul class="plist">' + ''.join(f'<li><span>{x}</span><b>{t["sp"]}</b></li>' for x in li) + '</ul></div>\n' for g, li in t['svc'])
             + f'      </div>\n      <p class="pnote">{t["svc_note"]}</p>\n')
    h.append(f'      <div class="faq pfaq">\n        <h3 class="ph">{t["faq_h"]}</h3>\n'
             + ''.join(f'        <details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>\n' for q, a in t['faq'])
             + '      </div>\n')
    h.append(f'      <div class="pend">\n        <h3>{t["pend_h"]}</h3>\n        <p>{t["pend_p"]}</p>\n        <div class="cta-row"><a class="btn btn-accent" href="#demo">{t["pend_a"]}</a><a class="btn btn-ghost" href="#contatti">{t["pend_b"]}</a></div>\n      </div>\n')
    return '\n'.join(h)

def sostituisci(s, inizio, fine, nuovo):
    a = s.index(inizio) + len(inizio); b = s.index(fine, a)
    return s[:a] + '\n' + nuovo + s[b:]

# IT: dentro la sezione #prezzi, tra l'apertura del contenitore e la chiusura della sezione
a = s.index('<div class="wrap pwrap" data-i18n="price">')
s = sostituisci(s, '<div class="wrap pwrap" data-i18n="price">', '    </div>\n  </section>\n  <template id="tpl-price-en">', blocco('it'))
s = sostituisci(s, '<template id="tpl-price-en">', '  </template>', blocco('en'))
s = sostituisci(s, '<template id="tpl-price-de">', '  </template>', blocco('de'))
P.write_text(s, encoding='utf-8')
print('sezione Piani riscritta senza prezzi (IT, EN, DE)')
