# Pulizia del sito (richiesta di William, 10/11/2026). Solo testi, posizioni e voci nascoste: grafica invariata,
# niente cancellato (ciò che si toglie resta nel codice, nascosto con «hidden» o in un commento). Idempotente.
import pathlib, re, sys
P = pathlib.Path(__file__).resolve().parent.parent
def edit(path, fn):
    p = P / path; s = p.read_text(encoding='utf-8'); t = fn(s); p.write_text(t, encoding='utf-8'); return s != t
def rep(s, a, b, label=''):
    if b in s and a not in s: return s
    if s.count(a) != 1: sys.exit(f'non trovato ({s.count(a)}): {label or a[:70]}')
    return s.replace(a, b)

def home(s):
    # 2. WhatsApp: niente «numero in arrivo / attivo a breve», solo «da gennaio 2027», senza numero
    s = rep(s, '<span class="v">Numero in arrivo</span>\n          <span class="soon">Il numero WhatsApp di Celea sarà attivo a breve. Nel frattempo ci scriva per email.</span>',
               '<span class="v">Da gennaio 2027</span>\n          <span class="soon">Fino ad allora ci scriva per email.</span>')
    s = rep(s, '<span class="v">Number coming soon</span><span class="soon">Celea\\\'s WhatsApp number will be active soon. In the meantime, please email us.</span>',
               '<span class="v">From January 2027</span><span class="soon">Until then, please email us.</span>')
    s = rep(s, '<span class="v">Nummer folgt in Kürze</span><span class="soon">Die WhatsApp-Nummer von Celea ist bald aktiv. Schreiben Sie uns bis dahin per E-Mail.</span>',
               '<span class="v">Ab Januar 2027</span><span class="soon">Bis dahin schreiben Sie uns bitte per E-Mail.</span>')
    s = s.replace('solo numeri italiani · dalle 8 alle 21 ·', 'solo numeri italiani · dalle 9 alle 20 ·').replace('Italian numbers only · 8 am to 9 pm ·', 'Italian numbers only · 9 am to 8 pm ·').replace('nur italienische Nummern · 8 bis 21 Uhr ·', 'nur italienische Nummern · 9 bis 20 Uhr ·')
    # 3. pacchetti sopra i 1.000 €/mese (Celea Concierge, 2.490 €): nascosti, restano nel codice
    s = s.replace('<article class="cat-top"><h4>Celea Concierge</h4>', '<article class="cat-top" hidden data-nascosto="pulizia-2026-11-10: sopra 1.000 €/mese"><h4>Celea Concierge</h4>')
    # 4. Celea Uffici: progetto pilota, una sola azione, sotto la parte principale (dopo le domande, prima dei contatti)
    s = rep(s, '<a class="mob-uffici" href="uffici/" data-i18n="mobu">', '<a class="mob-uffici" href="uffici/" data-i18n="mobu" hidden data-nascosto="pulizia-2026-11-10: la parte principale parla solo dell\'assistente al telefono">')
    s = rep(s, '<p class="eyebrow">L\'ufficio di Celea</p>', '<p class="eyebrow">Celea Uffici · progetto pilota</p>')
    s = rep(s, '<a class="btn btn-ghost" href="uffici/" data-i18n="r-u-cta">Scopra Celea Uffici</a>', '<a class="btn btn-ghost" href="#contatti" data-i18n="r-u-cta">Vuole provarlo nella Sua azienda? Ci scriva</a>')
    m = re.search(r'  <section class="ufficio" id="ufficio".*?\n  </section>\n\n', s, re.S)
    if m and s.index('id="ufficio"') < s.index('id="domande"'):
        blocco = m.group(0); s = s[:m.start()] + s[m.end():]
        i = s.index('  <section class="alt" id="contatti"'); s = s[:i] + blocco + s[i:]
    # 5. la parte principale: l'assistente al telefono per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive
    for a, b in [
        ('Per studi dentistici, agenzie immobiliari e strutture ricettive.', 'Per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive.'),
        ('For dental practices, real estate agencies and hotels, B&amp;Bs and holiday rentals.', 'For dental practices, veterinary clinics, real estate agencies and hotels, B&amp;Bs and holiday rentals.'),
        ('Für Zahnarztpraxen, Immobilienagenturen sowie Hotels, B&amp;Bs und Ferienwohnungen.', 'Für Zahnarztpraxen, Tierarztpraxen, Immobilienagenturen sowie Hotels, B&amp;Bs und Ferienwohnungen.'),
        ('uguali per studi dentistici, agenzie immobiliari e strutture ricettive.', 'uguali per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive.'),
        ('the same for dental practices, real estate agencies and hospitality.', 'the same for dental practices, veterinary clinics, real estate agencies and hospitality.'),
        ('gleich für Zahnarztpraxen, Immobilienagenturen und Unterkünfte.', 'gleich für Zahnarztpraxen, Tierarztpraxen, Immobilienagenturen und Unterkünfte.'),
        ('Studi dentistici, agenzie immobiliari e strutture ricettive, in Italia e all\'estero.', 'Studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive, in Italia e all\'estero.'),
    ]: s = rep(s, a, b)
    s = s.replace('per studi dentistici, agenzie immobiliari e strutture ricettive', 'per studi dentistici, cliniche veterinarie, agenzie immobiliari e strutture ricettive')
    return s

def testi(s):
    s = rep(s, '"r-u-head":"<p class=\\"eyebrow\\">Celea\'s office</p>', '"r-u-head":"<p class=\\"eyebrow\\">Celea Uffici · pilot project</p>')
    s = rep(s, '"r-u-head":"<p class=\\"eyebrow\\">Das Büro von Celea</p>', '"r-u-head":"<p class=\\"eyebrow\\">Celea Uffici · Pilotprojekt</p>')
    s = rep(s, '"r-u-cta":"Discover Celea Uffici"', '"r-u-cta":"Would you like to try it in your business? Write to us"')
    s = rep(s, '"r-u-cta":"Celea Uffici entdecken"', '"r-u-cta":"Möchten Sie es in Ihrem Betrieb ausprobieren? Schreiben Sie uns"')
    return s

def listino(s):
    # il PDF del listino segue la pagina principale: Concierge nascosto anche lì
    if '[hidden]{display:none!important}' not in s: s = s.replace('*{box-sizing:border-box}', '*{box-sizing:border-box}\n[hidden]{display:none!important}', 1)
    return s.replace('<div class="box"><h3>Celea Concierge</h3>', '<div class="box" hidden data-nascosto="pulizia-2026-11-10: sopra 1.000 €/mese"><h3>Celea Concierge</h3>')

print('home', edit('index.html', home)); print('testi', edit('restyling-testi.js', testi)); print('listino', edit('listino/index.html', listino))
