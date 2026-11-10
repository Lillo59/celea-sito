# Decisioni di William (10/11/2026): indirizzo email info@celea.it ovunque (al posto di team.celea@gmail.com);
# piè di pagina «Celea · William Balletta · Librizzi (ME) · info@celea.it»; nessuna partita IVA e nessun segnaposto finché non è attiva.
# Idempotente.
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent.parent
FOOT = 'Celea · William Balletta · Librizzi (ME) · info@celea.it'
def rep(path, pairs):
    p = P / path; s = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in s: continue
        s = s.replace(a, b)
    p.write_text(s, encoding='utf-8')
# 1. titolare e segnaposti (prima del cambio di indirizzo, che cambia le frasi)
rep('index.html', [
 ('Celea, di William. Contatto: team.celea@gmail.com. Ragione sociale, partita IVA e indirizzo completi saranno indicati qui e nella pagina privacy prima della messa online definitiva.', 'Celea, di William Balletta, Librizzi (ME). Contatto: info@celea.it.'),
 ('Celea, by William. Contact: team.celea@gmail.com. Full business name, VAT number and address will be shown here and on the privacy page before the final launch.', 'Celea, by William Balletta, Librizzi (ME), Italy. Contact: info@celea.it.'),
 ('Celea, von William. Kontakt: team.celea@gmail.com. Vollständiger Firmenname, USt-IdNr. und Anschrift werden hier und auf der Datenschutzseite vor dem endgültigen Start angegeben.', 'Celea, von William Balletta, Librizzi (ME), Italien. Kontakt: info@celea.it.'),
 # piè di pagina
 ("Receptionist AI su WhatsApp e al telefono per studi dentistici, agenzie immobiliari e strutture ricettive, in Italia e all'estero. Contatti: team.celea@gmail.com · ", FOOT + ' · '),
 ("AI receptionist on WhatsApp and phone for dental practices, real estate agencies and hospitality businesses, in Italy and abroad. Contact: team.celea@gmail.com · ", FOOT + ' · '),
 ("KI-Rezeption auf WhatsApp und am Telefon für Zahnarztpraxen, Immobilienagenturen und Beherbergungsbetriebe, in Italien und im Ausland. Kontakt: team.celea@gmail.com · ", FOOT + ' · '),
])
rep('privacy/index.html', [
 ('Celea, ditta individuale di William. Contatto: team.celea@gmail.com. Ragione sociale, partita IVA e indirizzo completi saranno indicati qui prima della messa online definitiva.', 'Celea, ditta individuale di William Balletta, Librizzi (ME). Contatto: info@celea.it.'),
 ('Celea, sole proprietorship of William. Contact: team.celea@gmail.com. Full business name, VAT number and address will be shown here before the final launch.', 'Celea, sole proprietorship of William Balletta, Librizzi (ME), Italy. Contact: info@celea.it.'),
 ('Celea, Einzelunternehmen von William. Kontakt: team.celea@gmail.com. Vollständiger Firmenname, USt-IdNr. und Anschrift werden hier vor dem endgültigen Start angegeben.', 'Celea, Einzelunternehmen von William Balletta, Librizzi (ME), Italien. Kontakt: info@celea.it.'),
 ('Google (la casella di posta team.celea@gmail.com, Google Ireland Ltd)', 'Google (la casella di posta di Celea, Google Ireland Ltd)'),
 ('Google (the team.celea@gmail.com mailbox, Google Ireland Ltd)', "Google (Celea's mailbox, Google Ireland Ltd)"),
 ('Google (das Postfach team.celea@gmail.com, Google Ireland Ltd)', 'Google (das Postfach von Celea, Google Ireland Ltd)'),
 ('<footer><div class="wrap">Celea · risponde sempre, con cura. · team.celea@gmail.com · ', '<footer><div class="wrap">' + FOOT + ' · '),
])
rep('uffici/index.html', [('<footer><div class="wrap">Celea Uffici · un progetto di Celea · team.celea@gmail.com · ', '<footer><div class="wrap">' + FOOT + ' · ')])
# 2. tutti gli altri punti: indirizzo nuovo (testi, mailto, JSON-LD, PDF)
for f in ['index.html', 'privacy/index.html', 'uffici/index.html', 'listino/index.html']:
    rep(f, [('team.celea@gmail.com', 'info@celea.it')])
# 3. dati strutturati: nome e località del titolare
rep('index.html', [('"founder":{"@type":"Person","name":"William"},"address":{"@type":"PostalAddress","addressRegion":"Sicilia","addressCountry":"IT"}',
                    '"founder":{"@type":"Person","name":"William Balletta"},"address":{"@type":"PostalAddress","addressLocality":"Librizzi","addressRegion":"ME","addressCountry":"IT"}')])
left = [f for f in ['index.html', 'privacy/index.html', 'uffici/index.html', 'listino/index.html'] if 'team.celea' in (P / f).read_text(encoding='utf-8')]
print('resta team.celea in:', left or 'nessun file')
