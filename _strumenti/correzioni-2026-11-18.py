# Correzioni del testo per Code v5 (parte A) + regole del 19/11 (settori alla pari, WhatsApp «da gennaio 2027»).
# Solo testi. Idempotente: se una frase nuova c'è già, la salta.
import pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
log = []
def edit(path, pairs, regex=False):
    p = R / path; s = p.read_text(encoding='utf-8')
    for a, b in pairs:
        n = s.count(a)
        if n == 0:
            if b in s: continue
            sys.exit(f'{path}: non trovato: {a[:90]}')
        s = s.replace(a, b); log.append((path, n, a[:70]))
    p.write_text(s, encoding='utf-8')

SETTORI_IT = 'studi dentistici, cliniche veterinarie, agenzie immobiliari, strutture ricettive e impiantisti'
edit('index.html', [
 # A4 · «a qualsiasi ora» → formula del 3/11; descrizione Google entro 160 caratteri; settori alla pari
 ('<meta name="description" content="Celea è la receptionist AI per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive in tutta Italia e all\'estero: risponde al telefono a qualsiasi ora, quando in sede non può rispondere nessuno, e da gennaio 2027 su WhatsApp; fissa appuntamenti e passa a una persona quando serve. Provi subito la demo e chieda la prova gratuita di 10 giorni."',
  '<meta name="description" content="Receptionist AI al telefono, anche fuori orario, per studi dentistici, veterinari, agenzie, strutture ricettive e impiantisti. Prova gratuita di 10 giorni."'),
 ('content="Risponde ai Suoi clienti al telefono quando Lei non può, a qualsiasi ora; su WhatsApp da gennaio 2027. Studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive, in Italia e all\'estero. Provi la demo."',
  f'content="Risponde ai Suoi clienti al telefono quando Lei non può, anche fuori orario, negli orari che sceglie Lei; su WhatsApp da gennaio 2027. Per {SETTORI_IT}, in Italia e all\'estero. Provi la demo."'),
 ('"description":"Receptionist AI al telefono, a qualsiasi ora quando in sede non risponde nessuno, e su WhatsApp da gennaio 2027, per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive. Siti web come servizio aggiuntivo."',
  f'"description":"Receptionist AI al telefono, anche fuori orario, negli orari che sceglie il titolare, e su WhatsApp da gennaio 2027, per {SETTORI_IT}. Siti web come servizio aggiuntivo."'),
 ("Celea è l'assistente che risponde al telefono quando Lei non può, a qualsiasi ora: linea occupata,", "Celea è l'assistente che risponde al telefono quando Lei non può, anche fuori orario, negli orari che sceglie Lei: linea occupata,"),
 ("Celea is the assistant that answers the phone when you can't, at any hour: busy line,", "Celea is the assistant that answers the phone when you can't, also outside opening hours, at the times you choose: busy line,"),
 ("Celea ist der Assistent, der am Telefon antwortet, wenn Sie nicht können, zu jeder Uhrzeit: besetzte Leitung,", "Celea ist der Assistent, der am Telefon antwortet, wenn Sie nicht können, auch außerhalb der Öffnungszeiten, zu den Zeiten, die Sie festlegen: besetzte Leitung,"),
 ('(regola di William: risponde a qualsiasi ora quando non può rispondere nessuno)', '(regola di William del 10/11 sull\'orario)'),
 ('Risponde a qualsiasi ora quando in sede non può rispondere nessuno:', 'Risponde anche fuori orario, negli orari che sceglie Lei, quando in sede non può rispondere nessuno:'),
 ('It answers at any hour when nobody can pick up:', 'It answers also outside opening hours, at the times you choose, when nobody can pick up:'),
 ('Er antwortet zu jeder Uhrzeit, wenn niemand rangehen kann:', 'Er antwortet auch außerhalb der Öffnungszeiten, zu den Zeiten, die Sie festlegen, wenn niemand rangehen kann:'),
 ('con calma e con cura, a qualsiasi ora.', 'con calma e con cura, anche fuori orario, negli orari che sceglie Lei.'),
 ('calmly and with care, at any hour.', 'calmly and with care, also outside opening hours, at the times you choose.'),
 ('ruhig und sorgfältig, zu jeder Uhrzeit.', 'ruhig und sorgfältig, auch außerhalb der Öffnungszeiten, zu den Zeiten, die Sie festlegen.'),
 # settori alla pari nell'apertura
 ('Per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive.', 'Per studi dentistici, cliniche veterinarie, agenzie immobiliari, strutture ricettive e impiantisti.'),
 ('For dental practices, veterinary clinics, real estate agencies and hotels, B&amp;Bs and holiday rentals.', 'For dental practices, veterinary clinics, real estate agencies, hotels, B&amp;Bs and holiday rentals, and plumbing and electrical firms.'),
 ('Für Zahnarztpraxen, Tierarztpraxen, Immobilienagenturen sowie Hotels, B&amp;Bs und Ferienwohnungen.', 'Für Zahnarztpraxen, Tierarztpraxen, Immobilienagenturen, Hotels, B&amp;Bs und Ferienwohnungen sowie Installateure.'),
 # A5 · durata della demo
 ('chiamata breve, al massimo 3 minuti', 'chiamata di prova'),
 ('short call, 3 minutes max', 'trial call'),
 ('kurzer Anruf, höchstens 3 Minuten', 'Probeanruf'),
 ("Accetto di essere chiamato una sola volta dall'assistente demo di Celea; la chiamata dura al massimo 3 minuti.", "Accetto di essere chiamato una sola volta dall'assistente demo di Celea, per una chiamata di prova."),
 ("I agree to be called once by Celea's demo assistant; the call lasts at most 3 minutes.", "I agree to be called once by Celea's demo assistant, for a trial call."),
 ("Ich bin einverstanden, einmal vom Demo-Assistenten von Celea angerufen zu werden; der Anruf dauert höchstens 3 Minuten.", "Ich bin einverstanden, einmal vom Demo-Assistenten von Celea angerufen zu werden, für einen Probeanruf."),
 # A6 d · Telefono e WhatsApp insieme
 ('<p>Con il Pro lo stesso assistente risponde ai messaggi e alle chiamate, con le stesse informazioni e lo stesso tono.', '<p>Con il Pro lo stesso assistente risponde alle chiamate e, da gennaio 2027, ai messaggi WhatsApp, con le stesse informazioni e lo stesso tono.'),
 ('<p>With Pro the same assistant answers messages and calls, with the same information and the same tone.', '<p>With Pro the same assistant answers calls and, from January 2027, WhatsApp messages, with the same information and the same tone.'),
 ('<p>Mit Pro beantwortet derselbe Assistent Nachrichten und Anrufe, mit denselben Informationen und demselben Ton.', '<p>Mit Pro beantwortet derselbe Assistent Anrufe und, ab Januar 2027, WhatsApp-Nachrichten, mit denselben Informationen und demselben Ton.'),
 # A6 e · agende
 ('Al telefono e su WhatsApp propone solo gli orari liberi,', 'Al telefono propone solo gli orari liberi (su WhatsApp da gennaio 2027),'),
 ('On the phone and on WhatsApp it only offers free times,', 'On the phone it only offers free times (on WhatsApp from January 2027),'),
 ('Am Telefon und auf WhatsApp bietet sie nur freie Zeiten an,', 'Am Telefon bietet sie nur freie Zeiten an (auf WhatsApp ab Januar 2027),'),
 # A6 f · come funziona
 ("Configuriamo l'assistente su WhatsApp e al telefono.", "Configuriamo l'assistente al telefono e, da gennaio 2027, su WhatsApp."),
 ('We set up the assistant on WhatsApp and on the phone.', 'We set up the assistant on the phone and, from January 2027, on WhatsApp.'),
 ('Wir richten den Assistenten auf WhatsApp und am Telefon ein.', 'Wir richten den Assistenten am Telefon und, ab Januar 2027, auf WhatsApp ein.'),
 # A6 g · dentisti
 ('Spostamenti e disdette su WhatsApp', 'Spostamenti e disdette al telefono e, da gennaio 2027, su WhatsApp'),
 ('Rescheduling and cancellations on WhatsApp', 'Rescheduling and cancellations by phone and, from January 2027, on WhatsApp'),
 ('Verschiebungen und Absagen per WhatsApp', 'Verschiebungen und Absagen am Telefon und, ab Januar 2027, per WhatsApp'),
 # A6 h · demo
 ("con le stesse regole dell'assistente al telefono e su WhatsApp.", "con le stesse regole dell'assistente al telefono e, da gennaio 2027, su WhatsApp."),
 ('following the same rules as the assistant on the phone and on WhatsApp.', 'following the same rules as the assistant on the phone and, from January 2027, on WhatsApp.'),
 ('nach denselben Regeln wie die Assistenz am Telefon und auf WhatsApp.', 'nach denselben Regeln wie die Assistenz am Telefon und, ab Januar 2027, auf WhatsApp.'),
 # A6 i · assistenza
 ('assistenza su WhatsApp e in videochiamata,', 'assistenza in videochiamata e per email (WhatsApp da gennaio 2027),'),
 ('in videochiamata e su WhatsApp.', 'in videochiamata e per email (WhatsApp da gennaio 2027).'),
 ('support on WhatsApp and by video call,', 'support by video call and email (WhatsApp from January 2027),'),
 ('by video call and on WhatsApp.', 'by video call and email (WhatsApp from January 2027).'),
 ('Support per WhatsApp und Videocall,', 'Support per Videocall und E-Mail (WhatsApp ab Januar 2027),'),
 ('per Videocall und WhatsApp.', 'per Videocall und E-Mail (WhatsApp ab Januar 2027).'),
 # A6 j · FAQ e scheda d'esempio
 ('Valutiamo insieme come collegare WhatsApp e il telefono che già usa:', 'Valutiamo insieme come collegare il telefono che già usa e, da gennaio 2027, WhatsApp:'),
 ('We look together at how to connect the WhatsApp and phone you already use:', 'We look together at how to connect the phone you already use and, from January 2027, WhatsApp:'),
 ('Wir prüfen gemeinsam, wie WhatsApp und das Telefon, die Sie schon nutzen, angebunden werden:', 'Wir prüfen gemeinsam, wie das Telefon, das Sie schon nutzen, und ab Januar 2027 WhatsApp angebunden werden:'),
 ('chiede conferma su WhatsApp', 'chiede conferma per messaggio'),
 ('asks for confirmation on WhatsApp', 'asks for confirmation by message'),
 ('bittet um Bestätigung per WhatsApp', 'bittet um Bestätigung per Nachricht'),
 # A6 k · contatti e consenso
 ('con il modulo di questa pagina, per email o su WhatsApp (', 'con il modulo di questa pagina o per email ('),
 ('through the form on this page, by email or on WhatsApp (', 'through the form on this page or by email ('),
 ('über das Formular auf dieser Seite, per E-Mail oder WhatsApp (', 'über das Formular auf dieser Seite oder per E-Mail ('),
 ('Acconsento a ricevere da Celea informazioni commerciali via email e WhatsApp;', 'Acconsento a ricevere da Celea informazioni commerciali via email (e, da gennaio 2027, su WhatsApp);'),
 ('I agree to receive commercial information from Celea by email and WhatsApp;', 'I agree to receive commercial information from Celea by email (and, from January 2027, on WhatsApp);'),
 ('Ich bin einverstanden, von Celea Werbeinformationen per E-Mail und WhatsApp zu erhalten;', 'Ich bin einverstanden, von Celea Werbeinformationen per E-Mail (und ab Januar 2027 per WhatsApp) zu erhalten;'),
 # A7 · claude.ai nel commento
 (" e l'artifact claude.ai", ''),
 # A10 · lingue: incluse ma non garantite (decisione dell'8/11)
 ('Italiano, inglese e tedesco sono provati nei nostri collaudi; le altre lingue le attiviamo dopo una nostra prova.', 'Italiano, inglese e tedesco sono provati e garantiti; le altre lingue sono incluse ma non garantite.'),
 ('Altre lingue oltre a italiano, inglese e tedesco: le aggiungiamo senza costi in più, solo dopo una nostra prova che ne garantisca la qualità.', 'Altre lingue oltre a italiano, inglese e tedesco: sono incluse senza costi in più, ma non garantite.'),
 ('Languages other than Italian, English and German: we add them at no extra cost, only after our own test confirms the quality.', 'Languages other than Italian, English and German: included at no extra cost, but not guaranteed.'),
 ('Weitere Sprachen außer Italienisch, Englisch und Deutsch: Wir fügen sie ohne Aufpreis hinzu, erst nachdem ein eigener Test die Qualität bestätigt hat.', 'Weitere Sprachen außer Italienisch, Englisch und Deutsch: ohne Aufpreis enthalten, aber nicht garantiert.'),
 ('Altre lingue le aggiungiamo senza costi in più, solo dopo una nostra prova che ne garantisca la qualità.', 'Le altre lingue sono incluse senza costi in più, ma non garantite.'),
 ('We add other languages at no extra cost, only after our own test confirms the quality.', 'Other languages are included at no extra cost, but not guaranteed.'),
 ('Weitere Sprachen fügen wir ohne Aufpreis hinzu, erst nachdem ein eigener Test die Qualität bestätigt hat.', 'Weitere Sprachen sind ohne Aufpreis enthalten, aber nicht garantiert.'),
 ('Altre lingue si aggiungono senza costi in più, solo dopo una nostra prova che ne garantisca la qualità.', 'Le altre lingue sono incluse senza costi in più, ma non garantite.'),
 ('Other languages can be added at no extra cost, only after our own test confirms the quality.', 'Other languages are included at no extra cost, but not guaranteed.'),
])
edit('restyling-testi.js', [
 ('Italian, English and German are tested in our trials; we switch on other languages after our own test.', 'Italian, English and German are tested and guaranteed; other languages are included but not guaranteed.'),
 ('Italienisch, Englisch und Deutsch sind in unseren Tests geprüft; weitere Sprachen schalten wir nach einem eigenen Test frei.', 'Italienisch, Englisch und Deutsch sind geprüft und garantiert; weitere Sprachen sind enthalten, aber nicht garantiert.'),
])
# A12 · un solo invito verso Celea Uffici: via la frase finale di «Nuovi settori» (IT nel DOM, EN/DE nei dizionari)
p = R / 'index.html'; s = p.read_text(encoding='utf-8')
s2 = re.sub(r'\s*<p class="lead" style="margin-top:22px" data-i18n="nv4">.*?</p>', '', s, count=1, flags=re.S)
s2 = re.sub(r' "nv4":\'<strong>New for companies: Celea Uffici\..*?</a>\',', '', s2, count=1, flags=re.S)
s2 = re.sub(r' "nv4":\'<strong>Neu für Unternehmen: Celea Uffici\..*?</a>\',', '', s2, count=1, flags=re.S)
if s2 != s: log.append(('index.html', s.count('"nv4"') + s.count('data-i18n="nv4"') - s2.count('"nv4"') - s2.count('data-i18n="nv4"'), 'A12: tolto «Novità per le aziende: Celea Uffici… Scopra Celea Uffici»'))
p.write_text(s2, encoding='utf-8')
# A6 m · chat d'esempio
edit('demo-scenari.js', [('qui su WhatsApp', 'qui in chat'), ('here on WhatsApp', 'here in chat'), ('hier auf WhatsApp', 'hier im Chat'),
                         ('la manda su WhatsApp', 'la manda in chat'), ('sent on WhatsApp', 'sent in the chat'), ('per WhatsApp geschickt', 'im Chat geschickt')])
# A6 k · privacy e Uffici (solo le parole su WhatsApp; nessun altro cambio di sostanza)
edit('privacy/index.html', [
 ('<b>Modulo «Prenota la prova gratuita» e contatti per email o WhatsApp.</b>', '<b>Modulo «Prenota la prova gratuita» e contatti per email (WhatsApp da gennaio 2027).</b>'),
 ('Le inviamo novità e offerte di Celea via email o WhatsApp solo se', 'Le inviamo novità e offerte di Celea via email (e, da gennaio 2027, su WhatsApp) solo se'),
 ('<b>«Book your free trial» form and contacts by email or WhatsApp.</b>', '<b>«Book your free trial» form and contacts by email (WhatsApp from January 2027).</b>'),
 ('We send you Celea news and offers by email or WhatsApp only if', 'We send you Celea news and offers by email (and, from January 2027, on WhatsApp) only if'),
 ('<b>Formular «Kostenlose Testphase buchen» und Kontakt per E-Mail oder WhatsApp.</b>', '<b>Formular «Kostenlose Testphase buchen» und Kontakt per E-Mail (WhatsApp ab Januar 2027).</b>'),
 ('Neuigkeiten und Angebote von Celea senden wir Ihnen per E-Mail oder WhatsApp nur, wenn', 'Neuigkeiten und Angebote von Celea senden wir Ihnen per E-Mail (und ab Januar 2027 per WhatsApp) nur, wenn'),
])
edit('uffici/index.html', [('Accetto di ricevere informazioni commerciali da Celea via email e WhatsApp;', 'Accetto di ricevere informazioni commerciali da Celea via email (e, da gennaio 2027, su WhatsApp);')])
for x in log: print(*x, sep=' | ')
