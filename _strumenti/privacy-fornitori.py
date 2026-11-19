# Correzione di William del 19/11: nessun nome di fornitore nel testo del sito; in /privacy/ una sezione nuova
# «Fornitori che trattano dati per nostro conto», solo per categorie. Non toglie niente di ciò che c'è. Idempotente.
import pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
SEZ = {
'it': ('  <a class="back" href="../">Torna al sito</a>', '''  <h2>7. Fornitori che trattano dati per nostro conto</h2>
  <div class="box" data-sezione="fornitori">
    <p>Per alcune funzioni del sito usiamo fornitori esterni, che trattano i dati solo per nostro conto:</p>
    <ul>
      <li><b>Un fornitore di servizi di voce e intelligenza artificiale per la demo.</b> Solo se clicca «Parla ora», riceve la voce e il testo della conversazione dimostrativa e i dati tecnici del navigatore (browser).</li>
      <li><b>Servizi di protezione dei moduli contro lo spam.</b> Ricevono i dati tecnici del navigatore, per distinguere le persone dai programmi automatici.</li>
      <li><b>Un operatore telefonico.</b> Solo quando la prova con richiamata è attiva e Lei lascia il Suo numero, riceve quel numero per fare la chiamata dimostrativa.</li>
    </ul>
    <p>Alcuni di questi fornitori hanno sede o trattano i dati fuori dall'Unione europea, per esempio negli Stati Uniti.</p>
    <p>L'elenco nominativo dei fornitori è disponibile su richiesta scrivendo a info@celea.it.</p>
  </div>

'''),
'en': ('  <a class="back" href="../#en">', '''  <h2>7. Providers that process data on our behalf</h2>
  <div class="box" data-sezione="fornitori">
    <p>For some functions of the site we use external providers, which process data only on our behalf:</p>
    <ul>
      <li><b>A voice and artificial intelligence service provider for the demo.</b> Only if you click “Talk now”, it receives the voice and text of the demo conversation and the technical data of your browser.</li>
      <li><b>Services that protect forms against spam.</b> They receive the technical data of your browser, to tell people from automated programs.</li>
      <li><b>A telephone carrier.</b> Only when the call-back trial is active and you leave your number, it receives that number to make the demo call.</li>
    </ul>
    <p>Some of these providers are based or process data outside the European Union, for example in the United States.</p>
    <p>The list of providers by name is available on request by writing to info@celea.it.</p>
  </div>

'''),
'de': ('  <a class="back" href="../#de">', '''  <h2>7. Dienstleister, die Daten in unserem Auftrag verarbeiten</h2>
  <div class="box" data-sezione="fornitori">
    <p>Für einige Funktionen der Website nutzen wir externe Dienstleister, die Daten nur in unserem Auftrag verarbeiten:</p>
    <ul>
      <li><b>Ein Dienstleister für Sprach- und KI-Dienste für die Demo.</b> Nur wenn Sie auf „Jetzt sprechen“ klicken, erhält er Stimme und Text des Demo-Gesprächs sowie die technischen Daten Ihres Browsers.</li>
      <li><b>Dienste, die Formulare vor Spam schützen.</b> Sie erhalten die technischen Daten Ihres Browsers, um Menschen von automatischen Programmen zu unterscheiden.</li>
      <li><b>Ein Telefonanbieter.</b> Nur wenn der Test mit Rückruf aktiv ist und Sie Ihre Nummer hinterlassen, erhält er diese Nummer für den Demo-Anruf.</li>
    </ul>
    <p>Einige dieser Dienstleister haben ihren Sitz außerhalb der Europäischen Union oder verarbeiten Daten dort, zum Beispiel in den USA.</p>
    <p>Die namentliche Liste der Dienstleister erhalten Sie auf Anfrage unter info@celea.it.</p>
  </div>

'''),
}
p = R / 'privacy/index.html'; s = p.read_text(encoding='utf-8')
if 'data-sezione="fornitori"' not in s:
    for l, (ancora, blocco) in SEZ.items():
        if s.count(ancora) != 1: sys.exit(f'privacy {l}: ancora non trovata ({s.count(ancora)}): {ancora}')
        s = s.replace(ancora, blocco + ancora)
    p.write_text(s, encoding='utf-8'); print('privacy: sezione 7 aggiunta in IT/EN/DE')
for f in ('index.html', '_strumenti/cosa-non-come.py'):
    p = R / f; s = p.read_text(encoding='utf-8')
    for a, b in [("L'elenco completo dei fornitori è nell'informativa privacy.", "I dettagli sono nell'informativa privacy."),
                 ("The full list of providers is in the privacy notice.", "The details are in the privacy notice."),
                 ("Die vollständige Liste der Dienstleister finden Sie in der Datenschutzerklärung.", "Die Einzelheiten finden Sie in der Datenschutzerklärung.")]:
        if a in s: s = s.replace(a, b); print(f, '·', b)
    p.write_text(s, encoding='utf-8')
