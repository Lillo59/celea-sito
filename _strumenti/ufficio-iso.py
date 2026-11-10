# Genera l'ufficio isometrico della sezione «L'ufficio di Celea» (restyling 2026-11).
# Uso: python3 _strumenti/ufficio-iso.py > _strumenti/ufficio-iso.html  (poi il blocco va in index.html)
# Disegno leggero in SVG: pavimenti, pareti basse e scrivanie in proiezione isometrica; oggetti come cartellini piatti.
# Stanze in fila per il giro di Celeo: Ingresso → WhatsApp → Marketing → Contabilità → Legale → Vendite → Ingresso.
import json, math

T = 170          # lato della stanza (unità)
H = 54           # altezza delle pareti basse
HL = 118         # altezza della parete del logo all'ingresso
C30, S30 = math.cos(math.radians(30)), 0.5
OX, OY = 2 * T * C30 + 40, 150   # spostamento per far stare tutto nel viewBox

def iso(x, y, z=0):
    return (round((x - y) * C30 + OX, 1), round((x + y) * S30 - z + OY, 1))

def poly(pts, cls='', extra=''):
    return f'<polygon class="{cls}" points="{" ".join(f"{a},{b}" for a, b in pts)}"{extra}/>'

# (riga, colonna) → stanza ; riga 0 = in fondo (in alto a destra), riga 1 = davanti
STANZE = [
    ('ingresso', 1, 0, 'r-iso-ing', 'Ingresso · Segreteria'),
    ('whatsapp', 1, 1, 'r-iso-wa', 'WhatsApp (da gennaio 2027)'),
    ('marketing', 1, 2, 'r-iso-mk', 'Marketing'),
    ('contabilita', 0, 2, 'r-iso-co', 'Contabilità'),
    ('legale', 0, 1, 'r-iso-le', 'Legale'),
    ('vendite', 0, 0, 'r-iso-ve', 'Vendite'),
]
W, Hh = round(5 * T * C30 + 80), round(3 * T * S30 + 2.5 * T * S30 + OY - 40)
VB_W, VB_H = W, 600

def stanza(nome, r, c, key, label):
    x0, y0 = c * T, r * T
    g = [f'<g class="iso-room" data-room="{nome}">']
    floor = [iso(x0, y0), iso(x0 + T, y0), iso(x0 + T, y0 + T), iso(x0, y0 + T)]
    g.append(poly(floor, 'iso-floor'))
    # pareti di fondo: lato y0 (dietro a destra) e lato x0 (dietro a sinistra)
    h = H
    g.append(poly([iso(x0, y0), iso(x0 + T, y0), iso(x0 + T, y0, h), iso(x0, y0, h)], 'iso-wall-r'))
    hl = HL if nome == 'ingresso' else h
    g.append(poly([iso(x0, y0), iso(x0, y0 + T), iso(x0, y0 + T, hl), iso(x0, y0, hl)], 'iso-wall-l' + (' iso-logo-wall' if nome == 'ingresso' else '')))
    # scrivania al centro (scatola isometrica)
    cx, cy = x0 + T * 0.5, y0 + T * 0.42
    dw, dd, dh = 70, 34, 26
    a, b = cx - dw / 2, cy - dd / 2
    top = [iso(a, b, dh), iso(a + dw, b, dh), iso(a + dw, b + dd, dh), iso(a, b + dd, dh)]
    g.append(poly([iso(a, b + dd, dh), iso(a + dw, b + dd, dh), iso(a + dw, b + dd, 0), iso(a, b + dd, 0)], 'iso-desk-f'))
    g.append(poly([iso(a + dw, b, dh), iso(a + dw, b + dd, dh), iso(a + dw, b + dd, 0), iso(a + dw, b, 0)], 'iso-desk-s'))
    g.append(poly(top, 'iso-desk-t'))
    # luce della stanza (si accende quando lavora)
    lx, ly = iso(x0 + T * 0.5, y0 + T * 0.5)
    g.append(f'<ellipse class="iso-glow" cx="{lx}" cy="{ly}" rx="{T * 0.62:.0f}" ry="{T * 0.34:.0f}"/>')
    # cartello col nome: nell'angolo in fondo, disegnato in un livello sopra a tutto (vedi ETICHETTE)
    tx, ty = iso(x0 + T * 0.10, y0 + T * 0.10, h + 22)
    lw = len(label) * 8.2 + 28
    ETICHETTE.append(f'<g class="iso-label" data-for="{nome}" transform="translate({tx} {ty})"><rect x="{-lw/2:.0f}" y="-17" width="{lw:.0f}" height="30" rx="15"/><text y="4" data-i18n="{key}">{label}</text></g>')
    g.append('</g>')
    return '\n'.join(g), iso(x0 + T * 0.30, y0 + T * 0.80), iso(x0 + T * 0.74, y0 + T * 0.56, 44)

parti, centri, sopra = [], {}, {}
ETICHETTE = []
order = sorted(STANZE, key=lambda s: (s[1] + s[2], s[2]))   # da dietro a davanti
for nome, r, c, key, label in order:
    svg, cen, top = stanza(nome, r, c, key, label)
    parti.append(svg); centri[nome] = cen; sopra[nome] = top

# logo sulla parete dell'ingresso (piano x = 0): asse lungo -y, cioè verso destra e in su
ax, ay = iso(0, T * 2 - 22, 0)
logo = (f'<g class="iso-logo" transform="matrix(0.866,-0.5,0,1,{ax},{ay - HL + 26})">'
        '<g transform="scale(0.42)"><path d="M85.71 90.64A40 40 0 1 1 85.71 29.36" fill="none" stroke="#F4EDE3" stroke-width="12" stroke-linecap="round"/>'
        '<path d="M72.86 75.32A20 20 0 1 1 72.86 44.68" fill="none" stroke="#E08A6A" stroke-width="10" stroke-linecap="round"/><circle cx="96" cy="60" r="6" fill="#E08A6A"/>'
        '<text x="122" y="78" font-family="Manrope, Helvetica, Arial, sans-serif" font-size="54" font-weight="800" letter-spacing="-1.5" fill="#F4EDE3">celea</text></g></g>')
# calendario sulla parete di destra dell'ingresso (piano y = T): asse +x, verso destra e in giù
cx0, cy0 = iso(T * 0.18, T, 0)
cal = (f'<g class="iso-cal" transform="matrix(0.866,0.5,0,1,{cx0},{cy0 - H + 6})">'
       '<rect width="58" height="44" rx="4" class="iso-cal-bg"/><rect width="58" height="10" rx="3" class="iso-cal-top"/>'
       + ''.join(f'<rect x="{6 + (i % 4) * 13}" y="{15 + (i // 4) * 9}" width="9" height="6" rx="1.5" class="iso-cal-d"/>' for i in range(12))
       + '<rect x="32" y="24" width="9" height="6" rx="1.5" class="iso-cal-new" data-at="3"/></g>')

def card(nome, cls, inner, at, dx=0, dy=0):
    x, y = sopra[nome]
    return f'<g class="iso-card {cls}" data-at="{at}" transform="translate({x + dx} {y + dy})">{inner}</g>'

CARTE = [
    card('ingresso', 'iso-phone', '<g class="iso-ring"><circle r="19"/><path d="M-7 -8h4l2 5-2.5 1.5a11 11 0 0 0 6 6L4 2l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1-9 -6a2 2 0 0 1 2-2z" transform="scale(.9)"/></g>', 1, -6, 34),
    card('ingresso', 'iso-bubble', '<rect x="-12" y="-42" width="168" height="36" rx="12"/><text x="74" y="-19" data-i18n="r-iso-ai">Sofia · assistente AI</text>', 2, -176, 26),
    card('ingresso', 'iso-appt', '<rect x="-30" y="-14" width="60" height="26" rx="6"/><text y="4" data-i18n="r-iso-app">gio 17:00</text>', 3, 46, 58),
    card('whatsapp', 'iso-wa', '<rect x="-46" y="-34" width="74" height="24" rx="10"/><rect x="-20" y="-4" width="66" height="24" rx="10" class="me"/><text x="-9" y="-17" data-i18n="r-iso-wa1">Promemoria</text><text x="13" y="13" data-i18n="r-iso-wa3">Grazie!</text>', 4),
    card('marketing', 'iso-post', '<rect x="-34" y="-46" width="68" height="76" rx="7"/><rect x="-26" y="-38" width="52" height="34" rx="4" class="img"/><rect x="-26" y="2" width="40" height="5" rx="2.5" class="ln"/><rect x="-26" y="12" width="28" height="5" rx="2.5" class="ln"/><text y="46" data-i18n="r-iso-mk2">post da approvare</text>', 5),
    card('contabilita', 'iso-scad', '<rect x="-40" y="-42" width="80" height="68" rx="7"/><rect x="-30" y="-32" width="60" height="9" rx="3" class="s3"/><rect x="-30" y="-17" width="46" height="9" rx="3" class="s1"/><rect x="-30" y="-2" width="34" height="9" rx="3" class="s2"/><text y="42" data-i18n="r-iso-co2">scadenze in ordine</text>', 6),
    card('legale', 'iso-doc', '<rect x="-30" y="-44" width="60" height="72" rx="6"/><rect x="-21" y="-34" width="42" height="5" rx="2.5" class="ln"/><rect x="-21" y="-24" width="36" height="5" rx="2.5" class="ln"/><rect x="-21" y="-14" width="40" height="5" rx="2.5" class="ln"/><circle cx="16" cy="12" r="11" class="ok"/><path d="M11 12l4 4 7-8" class="okv"/><text y="44" data-i18n="r-iso-le2">testo riletto</text>', 7, -40, -34),
    card('vendite', 'iso-quote', '<rect x="-32" y="-40" width="64" height="62" rx="6"/><rect x="-23" y="-30" width="46" height="5" rx="2.5" class="ln"/><rect x="-23" y="-20" width="30" height="5" rx="2.5" class="ln"/><rect x="-23" y="4" width="46" height="10" rx="3" class="tot"/><text y="40" data-i18n="r-iso-ve2">preventivo pronto</text>', 8),
]

def pc(p): return [round(p[0] / VB_W * 100, 2), round(p[1] / VB_H * 100, 2)]
percorso = {k: pc(v) for k, v in centri.items()}

svg = (f'<svg class="iso-svg" viewBox="0 0 {VB_W} {VB_H}" role="presentation" aria-hidden="true">'
       + '\n'.join(parti) + logo + cal + '\n' + '\n'.join(CARTE) + '\n' + '\n'.join(ETICHETTE) + '</svg>')
html = f'''<div class="iso-ufficio stage" data-scene="ufficio" data-percorso='{json.dumps(percorso)}' aria-hidden="true">
  <div class="iso-vista"><div class="iso-cam">
  {svg}
  <img class="iso-celeo" src="img/celeo/celeo-figura-360.webp" width="360" height="637" alt="" decoding="async" loading="lazy" style="left:{percorso['ingresso'][0]}%;top:{percorso['ingresso'][1]}%">
  </div></div>
  <div class="iso-titolare" data-at="9"><span class="iso-t-h"><svg><use href="#i-logo"/></svg><b data-i18n="r-iso-t1">Riepilogo di oggi</b><small data-i18n="r-iso-t0">sul telefono del titolare</small></span><span data-i18n="r-iso-t2">3 chiamate · 1 appuntamento fissato · 1 post da approvare</span></div>
</div>'''
print(html)
