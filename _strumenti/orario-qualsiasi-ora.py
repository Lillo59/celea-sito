# Regola di William (10/11 sera): l'assistente risponde a QUALSIASI ora quando non può rispondere nessuno
# (linea occupata, segreteria impegnata, pausa pranzo, sera, notte, sabato e festivi). Mai «solo la sera» / «solo fuori orario».
# Restano vietati «24 ore su 24», «24/7» e le promesse di risultato. Solo testi: stessi componenti.
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent.parent
def rep(path, pairs):
    p = P / path; s = p.read_text(encoding='utf-8'); n = 0
    for a, b in pairs:
        if b in s and a not in s: continue          # già fatto
        if s.count(a) != 1: sys.exit(f'{path}: trovato {s.count(a)} volte: {a[:70]}')
        s = s.replace(a, b); n += 1
    p.write_text(s, encoding='utf-8'); print(path, n, 'sostituzioni')
rep('index.html', [
 # descrizione per Google, anteprima social, dati strutturati
 ("risponde al telefono, anche fuori orario, e da gennaio 2027 su WhatsApp;", "risponde al telefono a qualsiasi ora, quando in sede non può rispondere nessuno, e da gennaio 2027 su WhatsApp;"),
 ('content="Risponde ai Suoi clienti su WhatsApp e al telefono, anche fuori orario.', 'content="Risponde ai Suoi clienti al telefono quando Lei non può, a qualsiasi ora; su WhatsApp da gennaio 2027.'),
 ('"description":"Receptionist AI su WhatsApp e al telefono, anche fuori orario,', '"description":"Receptionist AI al telefono, a qualsiasi ora quando in sede non risponde nessuno, e su WhatsApp da gennaio 2027,'),
 # apertura
 ('<h1 data-i18n="h-h1">Risponde ai Suoi clienti. <em>Anche fuori orario.</em></h1>', '<h1 data-i18n="h-h1">Risponde ai Suoi clienti. <em>Quando Lei non può.</em></h1>'),
 ('"h-h1":"Your customers get an answer. <em>Even after hours.</em>"', '"h-h1":"Your customers get an answer. <em>When you can\'t.</em>"'),
 ('"h-h1":"Ihre Kunden bekommen eine Antwort. <em>Auch nach Feierabend.</em>"', '"h-h1":"Ihre Kunden bekommen eine Antwort. <em>Wenn Sie nicht können.</em>"'),
 ("Celea è l'assistente che risponde al telefono, anche fuori orario, e da gennaio 2027 anche su WhatsApp:", "Celea è l'assistente che risponde al telefono quando Lei non può, a qualsiasi ora: linea occupata, pausa pranzo, sera, notte, sabato e festivi; da gennaio 2027 anche su WhatsApp. Le urgenze passano subito a Lei o alla reperibilità:"),
 ("Celea is the assistant that answers the phone, also outside opening hours, and from January 2027 on WhatsApp too:", "Celea is the assistant that answers the phone when you can't, at any hour: busy line, lunch break, evening, night, Saturdays and holidays; from January 2027 on WhatsApp too. Emergencies go straight to you or your on-call contact:"),
 ("Celea ist der Assistent, der auch außerhalb der Öffnungszeiten am Telefon antwortet, ab Januar 2027 auch auf WhatsApp:", "Celea ist der Assistent, der am Telefon antwortet, wenn Sie nicht können, zu jeder Uhrzeit: besetzte Leitung, Mittagspause, Abend, Nacht, Samstag und Feiertage; ab Januar 2027 auch auf WhatsApp. Notfälle gehen sofort an Sie oder an den Bereitschaftsdienst:"),
 # come funziona: niente «solo la sera»
 ("<h3>Parte, prima fuori orario</h3><p>I primi 30 giorni sono di prova gratuita (fino a 100 minuti di telefonate). All'inizio risponde solo la sera e nel fine settimana, con un riepilogo quotidiano. Quando è soddisfatto, risponde anche negli altri orari che sceglie Lei.",
  "<h3>Parte quando Lei non può rispondere</h3><p>I primi 30 giorni sono di prova gratuita (fino a 100 minuti di telefonate). Risponde a qualsiasi ora quando in sede non può rispondere nessuno: linea occupata, pausa pranzo, sera, notte, sabato e festivi; ogni giorno riceve un riepilogo. Lei decide quando passargli le chiamate."),
 ("<h3>It starts after hours first</h3><p>The first 30 days are a free trial (up to 100 call minutes). At first it only answers in the evening and at weekends, with a daily summary. When you are happy, it also answers at the other hours you choose.",
  "<h3>It starts when you can\\'t answer</h3><p>The first 30 days are a free trial (up to 100 call minutes). It answers at any hour when nobody can pick up: busy line, lunch break, evening, night, Saturdays and holidays; you get a summary every day. You decide when calls go to it."),
 ("<h3>Er startet, zuerst außerhalb der Öffnungszeiten</h3><p>Die ersten 30 Tage sind eine kostenlose Testphase (bis zu 100 Telefonminuten). Anfangs antwortet er nur abends und am Wochenende, mit einer täglichen Zusammenfassung. Wenn Sie zufrieden sind, antwortet er auch zu den anderen Zeiten, die Sie wählen.",
  "<h3>Er startet, wenn Sie nicht rangehen können</h3><p>Die ersten 30 Tage sind eine kostenlose Testphase (bis zu 100 Telefonminuten). Er antwortet zu jeder Uhrzeit, wenn niemand rangehen kann: besetzte Leitung, Mittagspause, Abend, Nacht, Samstag und Feiertage; jeden Tag erhalten Sie eine Zusammenfassung. Sie entscheiden, wann Anrufe an ihn gehen."),
 # piani
 ("L'assistente risponde al telefono ai Suoi clienti, anche fuori orario negli orari che sceglie Lei:", "L'assistente risponde al telefono ai Suoi clienti quando Lei non può, a qualsiasi ora:"),
 ("Your assistant answers your customers on the phone, also outside opening hours you choose:", "Your assistant answers your customers on the phone when you can't, at any hour:"),
 ("Der Assistent beantwortet die Anrufe Ihrer Kunden, auch außerhalb der Öffnungszeiten, die Sie wählen:", "Der Assistent beantwortet die Anrufe Ihrer Kunden, wenn Sie nicht können, zu jeder Uhrzeit:"),
 # chi siamo
 ("con calma e con cura, anche fuori orario.</p>", "con calma e con cura, a qualsiasi ora.</p>"),
 ("calmly and with care, also outside opening hours.</p>", "calmly and with care, at any hour.</p>"),
 ("ruhig und sorgfältig, auch außerhalb der Öffnungszeiten.</p>", "ruhig und sorgfältig, zu jeder Uhrzeit.</p>"),
])
rep('listino/index.html', [("<h1>L'assistente che risponde ai Suoi clienti. Anche fuori orario.</h1>", "<h1>Risponde ai Suoi clienti quando Lei non può, a qualsiasi ora.</h1>")])
