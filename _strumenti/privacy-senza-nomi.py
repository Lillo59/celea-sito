# Decisione di William del 19/11 (lezione l20261119-personale-mai-fornitori-sul-sito): in /privacy/ anche l'hosting e la posta
# diventano categorie; versione 1.1 del 19 novembre 2026. Idempotente.
import pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
p = R / 'privacy/index.html'; s = p.read_text(encoding='utf-8')
P = [
 ('versione 1.0 del 22 ottobre 2026', 'versione 1.1 del 19 novembre 2026'),
 ('version 1.0 of 22 October 2026', 'version 1.1 of 19 November 2026'),
 ('Version 1.0 vom 22. Oktober 2026', 'Version 1.1 vom 19. November 2026'),
 ("Il sito è ospitato su GitHub Pages (GitHub, Inc., Stati Uniti): per consegnare le pagine il server riceve l'indirizzo IP del Suo dispositivo e può tenerne registri tecnici di sicurezza secondo le regole di GitHub.",
  "Il sito è ospitato da un servizio di hosting del sito, con sede negli Stati Uniti: per consegnare le pagine il server riceve l'indirizzo IP del Suo dispositivo e può tenerne registri tecnici di sicurezza secondo le proprie regole."),
 ("GitHub (hosting del sito) e Google (la casella di posta di Celea, Google Ireland Ltd).", "un servizio di hosting del sito e un servizio di posta elettronica (la casella di posta di Celea)."),
 ("The site is hosted on GitHub Pages (GitHub, Inc., USA): to deliver the pages the server receives your device's IP address and may keep technical security logs under GitHub's rules.",
  "The site is hosted by a website hosting service based in the United States: to deliver the pages the server receives your device's IP address and may keep technical security logs under its own rules."),
 ("GitHub (website hosting) and Google (Celea's mailbox, Google Ireland Ltd).", "a website hosting service and an email service (Celea's mailbox)."),
 ("Die Website wird auf GitHub Pages (GitHub, Inc., USA) gehostet: Um die Seiten auszuliefern, erhält der Server die IP-Adresse Ihres Geräts und kann nach den Regeln von GitHub technische Sicherheitsprotokolle führen.",
  "Die Website wird von einem Hosting-Dienst mit Sitz in den USA gehostet: Um die Seiten auszuliefern, erhält der Server die IP-Adresse Ihres Geräts und kann nach eigenen Regeln technische Sicherheitsprotokolle führen."),
 ("GitHub (Hosting der Website) und Google (das Postfach von Celea, Google Ireland Ltd).", "ein Hosting-Dienst für die Website und ein E-Mail-Dienst (das Postfach von Celea)."),
 # sezione 7: le due categorie in più, in testa all'elenco
 ("    <ul>\n      <li><b>Un fornitore di servizi di voce",
  "    <ul>\n      <li><b>Un servizio di hosting del sito.</b> Per consegnare le pagine riceve l'indirizzo IP e i dati tecnici del navigatore.</li>\n      <li><b>Un servizio di posta elettronica.</b> Riceve ciò che Lei ci scrive per email o con il modulo.</li>\n      <li><b>Un fornitore di servizi di voce"),
 ("    <ul>\n      <li><b>A voice and artificial intelligence",
  "    <ul>\n      <li><b>A website hosting service.</b> To deliver the pages it receives the IP address and the technical data of your browser.</li>\n      <li><b>An email service.</b> It receives what you write to us by email or through the form.</li>\n      <li><b>A voice and artificial intelligence"),
 ("    <ul>\n      <li><b>Ein Dienstleister für Sprach- und KI-Dienste",
  "    <ul>\n      <li><b>Ein Hosting-Dienst für die Website.</b> Um die Seiten auszuliefern, erhält er die IP-Adresse und die technischen Daten Ihres Browsers.</li>\n      <li><b>Ein E-Mail-Dienst.</b> Er erhält, was Sie uns per E-Mail oder über das Formular schreiben.</li>\n      <li><b>Ein Dienstleister für Sprach- und KI-Dienste"),
]
for a, b in P:
    if a in s: s = s.replace(a, b); print('·', b[:70])
    elif b not in s: sys.exit('non trovato: ' + a[:90])
p.write_text(s, encoding='utf-8')
