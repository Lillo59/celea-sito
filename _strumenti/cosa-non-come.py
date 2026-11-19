# d20261119-william-guide-cosa-non-come: sul sito si dice COSA ottiene il cliente, mai COME lavoriamo.
# 1) /uffici/ riscritta sui risultati (niente direttrice, reparti, memoria, turni, manuali, AI sostituibile).
# 2) Home: niente nomi dei fornitori fuori da /privacy/ (categorie al posto dei nomi); sezione ufficio senza «reparti».
# Idempotente: se il testo nuovo c'è già, salta. La pagina /privacy/ NON si tocca.
import pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
def edit(f, pairs):
    p = R / f; s = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a in s: s = s.replace(a, b); print(f, '·', a[:60].replace('\n', ' '))
        elif b not in s: sys.exit(f'{f}: non trovato: {a[:100]}')
    p.write_text(s, encoding='utf-8')
ELENCO = {'it': " L'elenco completo dei fornitori è nell'informativa privacy.",
          'en': " The full list of providers is in the privacy notice.",
          'de': " Die vollständige Liste der Dienstleister finden Sie in der Datenschutzerklärung."}

# ---------- /uffici/ ----------
U = R / 'uffici/index.html'; s = U.read_text(encoding='utf-8')
s = s.replace('<title>Celea Uffici · un ufficio di assistenti AI per la Sua azienda</title>',
              '<title>Celea Uffici · il lavoro d\'ufficio che va avanti per Lei</title>')
s = s.replace('content="Celea Uffici: una direttrice e dei reparti di assistenti AI, con una memoria condivisa e regole chiare, che lavorano per la Sua azienda. Lei decide spese, firme e contatti."',
              'content="Celea Uffici: il lavoro d\'ufficio va avanti anche quando Lei non c\'è, con documenti e risposte pronti. Lei decide, l\'ufficio esegue. Fase pilota, prezzo su misura."')
NUOVO = '''<main>
  <div class="wrap hero">
    <p class="eyebrow">Celea Uffici · progetto pilota</p>
    <h1>Il lavoro d'ufficio va avanti, <em>anche quando Lei non c'è</em>.</h1>
    <p class="lead">Documenti e risposte pronti quando servono. Meno ore perse in cose ripetitive. Lei decide, l'ufficio esegue.</p>
    <div class="cta"><a class="btn" href="#parliamone">Chieda una chiamata di 30 minuti</a><a class="btn btn-ghost" href="#cosa">Cosa ottiene</a></div>
    <p class="note">Gli assistenti di Celea Uffici sono intelligenze artificiali. Quando scrivono o parlano a qualcuno fuori dall'azienda lo dichiarano sempre.</p>
  </div>

  <section id="cosa" class="alt"><div class="wrap">
    <p class="eyebrow">Cosa ottiene</p>
    <h2>Più tempo per il Suo lavoro</h2>
    <div class="grid">
      <div class="card"><span class="n">01</span><h3>Il lavoro va avanti</h3><p>Richieste, promemoria e pratiche di tutti i giorni procedono anche quando Lei è fuori sede o in ferie.</p></div>
      <div class="card"><span class="n">02</span><h3>Documenti e risposte pronti</h3><p>Trova già preparati preventivi, risposte e documenti. Lei li rilegge e li approva.</p></div>
      <div class="card"><span class="n">03</span><h3>Meno ore perse</h3><p>Le cose ripetitive che oggi fa a mano ogni settimana Le arrivano già pronte.</p></div>
      <div class="card"><span class="n">04</span><h3>Decide sempre Lei</h3><p>Nessuna spesa, nessun invio a clienti e nessuna firma senza il Suo sì. Lei decide, l'ufficio esegue.</p></div>
    </div>
  </div></section>

  <section><div class="wrap">
    <p class="eyebrow">Perché fidarsi</p>
    <h2>Si parte in piccolo, con regole chiare</h2>
    <div class="grid">
      <div class="card"><h3>Fase pilota</h3><p>Partiamo con poche aziende. Si comincia da un lavoro alla volta e il risultato lo guardiamo insieme.</p></div>
      <div class="card"><h3>Il lavoro resta Suo</h3><p>Ciò che l'ufficio prepara per Lei è Suo. Lo può portare con sé quando vuole.</p></div>
      <div class="card"><h3>Regole chiare</h3><p>Dichiarazione AI, privacy e limiti scritti dall'inizio. Le attività con regole speciali, come quelle sanitarie o legali, le valutiamo prima di partire.</p></div>
    </div>
  </div></section>

  <section class="alt"><div class="wrap">
    <p class="eyebrow">Per chi</p>
    <h2>A chi serve</h2>
    <div class="grid">
      <div class="card"><h3>Piccole e medie imprese</h3><p>Aziende con lavoro ripetitivo (contatti, preventivi, documenti, comunicazione) che vogliono più ordine senza assumere subito.</p></div>
      <div class="card"><h3>Studi e professionisti</h3><p>Chi ha poco tempo per la parte organizzativa e vuole un ufficio che prepari, ricordi e segnali.</p></div>
      <div class="card"><h3>Consulenti e agenzie</h3><p>Chi vuole offrire Celea Uffici ai propri clienti, come partner.</p></div>
    </div>
  </div></section>

  <section><div class="wrap">
    <p class="eyebrow">Come si parte</p>
    <h2>Tre passi, senza impegno</h2>
    <ol class="steps">
      <li><strong>Chiamata di 30 minuti.</strong> Ci racconta come lavora e cosa vorrebbe affidare.</li>
      <li><strong>Proposta su misura.</strong> Le diciamo cosa farà l'ufficio, cosa non farà e quanto costa.</li>
      <li><strong>Prova prima di decidere.</strong> Vede l'ufficio al lavoro sul Suo caso prima di firmare.</li>
    </ol>
    <p class="note" style="margin-top:14px">Prezzo su misura: dipende dal lavoro che ci affida. Non promettiamo risultati che non possiamo misurare insieme.</p>
  </div></section>
'''
i = s.index('<main>'); j = s.index('  <section id="parliamone"')
if 'Il lavoro d\'ufficio va avanti' not in s: s = s[:i] + NUOVO + '\n' + s[j:]; print('uffici: corpo riscritto')
U.write_text(s, encoding='utf-8')

# ---------- home: privacy senza nomi dei fornitori ----------
edit('index.html', [
 ("il Suo browser si collega a Retell AI (il nostro fornitore di voce e intelligenza artificiale) per una conversazione a voce con l'assistente dimostrativo, e a Google reCAPTCHA per il controllo anti-bot.",
  "il Suo browser si collega a un fornitore di servizi di voce e intelligenza artificiale, per una conversazione a voce con l'assistente dimostrativo, e a un servizio di protezione dei moduli contro lo spam."),
 ("dal fornitore della voce, Retell AI, con sede negli Stati Uniti:", "dal fornitore della voce, con sede negli Stati Uniti:"),
 ("Base giuridica: la Sua richiesta (art. 6.1.b GDPR).</p>\n          <h4>La prova «Mi chiami»</h4>",
  "Base giuridica: la Sua richiesta (art. 6.1.b GDPR)." + ELENCO['it'] + "</p>\n          <h4>La prova «Mi chiami»</h4>"),
 ("tramite i nostri fornitori di telefonia e intelligenza artificiale (Retell AI, con sede negli Stati Uniti, e il nostro operatore telefonico) e per il controllo anti-bot (Cloudflare Turnstile).",
  "tramite un fornitore di servizi di voce e intelligenza artificiale, con sede negli Stati Uniti, e un operatore telefonico, e passa da un servizio di protezione dei moduli contro lo spam."),
 ("Solo se clicca «Parla ora» vengono caricati Retell AI e Google reCAPTCHA, che possono usare",
  "Solo se clicca «Parla ora» vengono caricati il servizio di voce e il servizio di protezione contro lo spam, che possono usare"),
 # EN
 ("does your browser connect to Retell AI (our voice and AI provider) for a spoken conversation with the demo assistant, and to Google reCAPTCHA for the anti-bot check.",
  "does your browser connect to a voice and artificial intelligence service provider, for a spoken conversation with the demo assistant, and to a service that protects forms against spam."),
 ("by the voice provider, Retell AI, based in the United States:", "by the voice provider, based in the United States:"),
 ("Legal basis: your request (Art. 6.1.b GDPR).</p><h4>The “Call me” trial</h4>",
  "Legal basis: your request (Art. 6.1.b GDPR)." + ELENCO['en'] + "</p><h4>The “Call me” trial</h4>"),
 ("through our telephony and AI providers (Retell AI, based in the United States, and our telephone carrier) and for the anti-bot check (Cloudflare Turnstile).",
  "through a voice and artificial intelligence service provider, based in the United States, and a telephone carrier, and goes through a service that protects forms against spam."),
 ("are Retell AI and Google reCAPTCHA loaded, which may use", "are the voice service and the anti-spam service loaded, which may use"),
 # DE
 ("verbindet sich Ihr Browser mit Retell AI (unserem Dienstleister für Stimme und KI) für ein Gespräch mit der Demo-Assistenz sowie mit Google reCAPTCHA für die Anti-Bot-Prüfung.",
  "verbindet sich Ihr Browser mit einem Dienstleister für Sprach- und KI-Dienste, für ein Gespräch mit der Demo-Assistenz, sowie mit einem Dienst, der Formulare vor Spam schützt."),
 ("vom Sprachanbieter Retell AI mit Sitz in den USA", "vom Sprachanbieter mit Sitz in den USA"),
 ("Rechtsgrundlage: Ihre Anfrage (Art. 6.1.b DSGVO).</p><h4>Der Test „Rufen Sie mich an“</h4>",
  "Rechtsgrundlage: Ihre Anfrage (Art. 6.1.b DSGVO)." + ELENCO['de'] + "</p><h4>Der Test „Rufen Sie mich an“</h4>"),
 ("über unsere Telefonie- und KI-Dienstleister (Retell AI mit Sitz in den USA und unser Telefonanbieter) und für die Anti-Bot-Prüfung (Cloudflare Turnstile) verwendet.",
  "über einen Dienstleister für Sprach- und KI-Dienste mit Sitz in den USA und einen Telefonanbieter verwendet und läuft über einen Dienst, der Formulare vor Spam schützt."),
 ("werden Retell AI und Google reCAPTCHA geladen, die", "werden der Sprachdienst und der Spamschutz-Dienst geladen, die"),
 # sezione ufficio della home: COSA, non COME
 ("Non un chatbot: un ufficio, con i suoi reparti.", "Non un chatbot: un ufficio che lavora per Lei."),
 ("Dietro, ogni reparto ha un compito preciso e prepara il lavoro.", "Dietro, il lavoro d'ufficio va avanti e Le prepara documenti e risposte."),
 ("Illustrazione: i reparti si scelgono insieme, in base al Suo lavoro.", "Illustrazione: cosa fa l'ufficio si sceglie insieme, in base al Suo lavoro."),
 ("Illustrazione dell'ufficio: i reparti si scelgono insieme, in base al Suo lavoro.", "Illustrazione dell'ufficio: cosa fa si sceglie insieme, in base al Suo lavoro."),
 ("Celeo in apertura, il motto, la telefonata a Sofia, l'ufficio con i reparti,", "Celeo in apertura, il motto, la telefonata a Sofia, l'ufficio,"),
 ("/* ---------- L'ufficio di Celea: i reparti ---------- */", "/* ---------- L'ufficio di Celea ---------- */"),
 # codice: commenti e nomi interni senza nomi di fornitori (restano solo gli indirizzi che il browser deve chiamare)
 ('  // endpoint: es. "https://prova.celea.it"  ·  turnstile: la «Site Key» di Cloudflare Turnstile (anti-bot), pubblica.',
  '  // endpoint: es. "https://prova.celea.it"  ·  antispam: la chiave pubblica del servizio contro lo spam del modulo.'),
 ('var LIVE = { endpoint:"", turnstile:"", richiamata:false };', 'var LIVE = { endpoint:"", antispam:"", richiamata:false };'),
 ('widget di Retell, caricato solo al clic.', 'widget del fornitore della voce, caricato solo al clic.'),
 ('i domini ammessi si impostano in Retell.', 'i domini ammessi si impostano dal fornitore della voce.'),
 ('recaptcha:"6Lc2O_4tAAAAAMUHuzb58YLXZ14f1q23lMZsPcz4"', 'antispam:"6Lc2O_4tAAAAAMUHuzb58YLXZ14f1q23lMZsPcz4"'),
 ('assistenti su Retell aggiornati con', 'assistenti aggiornati con'),
 ('solo quando gli assistenti su Retell usano la variabile', 'solo quando gli assistenti usano la variabile'),
 ('(impostato su Retell)', '(impostato dal fornitore della voce)'),
 ('tetto giornaliero complessivo da impostare su Retell.', 'tetto giornaliero complessivo da impostare dal fornitore della voce.'),
 ('// Il widget di Retell resta legato', '// Il widget della voce resta legato'),
 ('if(TALK.recaptcha) addScript("https://www.google.com/recaptcha/api.js?render="+encodeURIComponent(TALK.recaptcha), {async:""});',
  'if(TALK.antispam) addScript(VOCE.antispam+encodeURIComponent(TALK.antispam), {async:""});'),
 ('var w=addScript("https://dashboard.retellai.com/retell-widget-v2.js", {id:"retell-widget", type:"module",',
  'var w=addScript(VOCE.widget, {id:VOCE.id, type:"module",'),
 ('"data-recaptcha-key":TALK.recaptcha,', '[VOCE.attrAntispam]:TALK.antispam,'),
 ('retellGuardia(out);', 'vocePausa(out);'),
 ('il widget parte ma Retell rifiuta la chiamata', 'il widget parte ma il fornitore della voce rifiuta la chiamata'),
 ('si guardano le risposte di Retell (HTTP 4xx/5xx)', 'si guardano le sue risposte (HTTP 4xx/5xx)'),
 ('function retellGuardia(out){', 'function vocePausa(out){'),
 ('suRetell=function(u){ return /retellai\\.com/i.test(String(u||"")); };', 'suVoce=function(u){ return String(u||"").indexOf(VOCE.host)>=0; };'),
 ('if(suRetell(u)) pr.then', 'if(suVoce(u)) pr.then'),
 ('if(o0) X.open=function(m,u){ if(suRetell(u))', 'if(o0) X.open=function(m,u){ if(suVoce(u))'),
 ('if(/retell|web ?call|livekit/i.test(t)) pausa();', 'if(t.indexOf(VOCE.host)>=0 || /web ?call|livekit/i.test(t)) pausa();'),
 ('["retell-error","error"].forEach(function(n){ document.addEventListener(n, function(e){ var t=e.target; if(t && t!==document && /retell/i.test((t.id||"")+" "+(t.tagName||""))) pausa(); }, true); });',
  '[VOCE.id.replace("-widget","-error"),"error"].forEach(function(n){ document.addEventListener(n, function(e){ var t=e.target; if(t && t!==document && (t.id===VOCE.id || String(t.tagName||"").toLowerCase().indexOf(VOCE.id.split("-")[0])===0)) pausa(); }, true); });'),
 ('if(LIVE.turnstile){\n      window.celeaCf', 'if(LIVE.antispam){\n      window.celeaCf'),
 ('{sitekey:LIVE.turnstile, language:lang}', '{sitekey:LIVE.antispam, language:lang}'),
 ('if(LIVE.turnstile){ try{ token=', 'if(LIVE.antispam){ try{ token='),
])
# indirizzi tecnici dei fornitori in un solo punto (servono al browser per caricare la demo vocale)
s = (R / 'index.html').read_text(encoding='utf-8')
if 'var VOCE =' not in s:
    a = '  var TALK = { key:'
    s = s.replace(a, '  // Indirizzi tecnici che il browser deve chiamare (non è testo per il visitatore). I fornitori sono nell\'informativa privacy.\n'
        '  var VOCE = { widget:"https://dashboard.retellai.com/retell-widget-v2.js", id:"retell-widget", host:"retellai.com",\n'
        '    antispam:"https://www.google.com/recaptcha/api.js?render=", attrAntispam:"data-recaptcha-key" };\n' + a, 1)
    (R / 'index.html').write_text(s, encoding='utf-8'); print('index · VOCE')
edit('restyling-testi.js', [
 ('Not a chatbot: an office, with its departments.', 'Not a chatbot: an office that works for you.'),
 ('Behind it, each department has a precise task and prepares the work.', 'Behind it, the office work keeps going and prepares documents and replies for you.'),
 ('Illustration: departments are chosen together, based on your work.', 'Illustration: what the office does is chosen together, based on your work.'),
 ('Illustration of the office: departments are chosen together, based on your work.', 'Illustration of the office: what it does is chosen together, based on your work.'),
 ('Kein Chatbot: ein Büro, mit seinen Abteilungen.', 'Kein Chatbot: ein Büro, das für Sie arbeitet.'),
 ('Dahinter hat jede Abteilung eine klare Aufgabe und bereitet die Arbeit vor.', 'Dahinter läuft die Büroarbeit weiter und bereitet Ihnen Dokumente und Antworten vor.'),
 ('Darstellung: Die Abteilungen wählen wir gemeinsam, passend zu Ihrer Arbeit.', 'Darstellung: Was das Büro macht, wählen wir gemeinsam, passend zu Ihrer Arbeit.'),
 ('Darstellung des Büros: Die Abteilungen wählen wir gemeinsam, passend zu Ihrer Arbeit.', 'Darstellung des Büros: Was es macht, wählen wir gemeinsam, passend zu Ihrer Arbeit.'),
])
edit('restyling.js', [('// 3) Reparti al lavoro: ogni reparto mostra a turno cosa sta facendo', '// 3) Ufficio al lavoro: ogni stanza mostra, una alla volta, cosa sta facendo')])
edit('demo-scenari.js', [('passato al personale di turno', 'passato al personale in servizio'), ('al personale di turno, che', 'al personale in servizio, che'),
                         ('via del Porto 10, di turno, telefono', 'via del Porto 10, telefono')])
# classe CSS «reparto» → «stanza» (solo nome interno)
p = R / 'index.html'; s = p.read_text(encoding='utf-8'); n = len(re.findall(r'\breparto\b', s))
s = re.sub(r'\.reparto\b', '.stanza', s); s = s.replace('class="reparto"', 'class="stanza"'); p.write_text(s, encoding='utf-8'); print('classe reparto →', n)
