# A13 · Piede legale del sito (Legale s20261118-legale-1, documenti/legale-sito-aggiunte-28-10 v1.2; bozza da far rivedere a un avvocato).
# PRONTO MA SPENTO: si accende solo se ci sono via, CAP e partita IVA. Senza questi dati non scrive niente nelle pagine.
# Uso: python3 _strumenti/piede-legale.py --nome "Nome Cognome" --via "Via Esempio 1" --cap 98060 --piva 01234567890 [--rea ME-123456] [--tel "..."]
# Mette il piede in index, privacy, uffici, listino (pagina «Preventivo su misura»), dentro <footer> con data-piede="legale".
# I link a Cookie e Termini compaiono solo quando esistono le pagine /cookie/ e /termini/.
import argparse, html, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
a = argparse.ArgumentParser()
for k in ('nome', 'via', 'cap', 'piva', 'rea', 'tel'): a.add_argument('--' + k, default='')
o = a.parse_args()
if not (o.via.strip() and re.fullmatch(r'\d{5}', o.cap.strip()) and re.fullmatch(r'\d{11}', o.piva.strip()) and o.nome.strip()):
    print('Piede legale SPENTO: mancano nome, via, CAP (5 cifre) o partita IVA (11 cifre). Nessuna pagina modificata.')
    sys.exit(0)
e = {k: html.escape(getattr(o, k).strip()) for k in ('nome', 'via', 'cap', 'piva', 'rea', 'tel')}
pagine = {'index.html': '', 'privacy/index.html': '../', 'uffici/index.html': '../', 'listino/index.html': '../'}
def links(base, lingua):
    L = {'it': ('Privacy', 'Cookie', 'Termini'), 'en': ('Privacy', 'Cookies', 'Terms'), 'de': ('Datenschutz', 'Cookies', 'AGB')}[lingua]
    out = [f'<a href="{base}privacy/">{L[0]}</a>']
    if (R / 'cookie/index.html').exists(): out.append(f'<a href="{base}cookie/">{L[1]}</a>')
    if (R / 'termini/index.html').exists(): out.append(f'<a href="{base}termini/">{L[2]}</a>')
    return ' · '.join(out)
def riga(base, lingua):
    rea = f' · REA {e["rea"]}' if e['rea'] else ''
    tel = f' · {e["tel"]}' if e['tel'] else ''
    t = {'it': f'Celea · ditta individuale di {e["nome"]} · {e["via"]}, {e["cap"]} Librizzi (ME) · P. IVA {e["piva"]}',
         'en': f'Celea · sole proprietorship of {e["nome"]} · {e["via"]}, {e["cap"]} Librizzi (ME), Italy · VAT no. {e["piva"]}',
         'de': f'Celea · Einzelunternehmen von {e["nome"]} · {e["via"]}, {e["cap"]} Librizzi (ME), Italien · USt-IdNr. {e["piva"]}'}[lingua]
    return f'<p class="piede-legale" data-piede="legale" data-piede-lang="{lingua}"{"" if lingua == "it" else " hidden"} lang="{lingua}">{t}{rea} · info@celea.it{tel} · {links(base, lingua)}</p>'
for f, base in pagine.items():
    p = R / f; s = p.read_text(encoding='utf-8')
    s = re.sub(r'\s*<p class="piede-legale" data-piede="legale".*?</p>', '', s, flags=re.S)
    blocco = '\n' + '\n'.join(riga(base, l) for l in ('it', 'en', 'de'))
    s, n = re.subn(r'(<footer\b[^>]*>)', r'\1' + blocco.replace('\\', '\\\\'), s, count=1)
    if not n: sys.exit(f'{f}: <footer> non trovato')
    p.write_text(s, encoding='utf-8'); print('piede acceso in', f)
print('Da fare a mano dopo l\'accensione: mostrare la riga della lingua scelta (data-piede-lang) nello script delle lingue di ogni pagina.')
