"""Genera le grafiche social di Celea (settimana 1) in PNG 1080x1350."""
import os, sys
from playwright.sync_api import sync_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)

TEAL, DEEP, CREAM, TERRA, TERRA2, INK, MUTED = "#0F4C5C", "#0A3440", "#F4EDE3", "#E08A6A", "#C8664A", "#1F2D33", "#5B6B70"

def logo(fg_big, fg_small, size=64):
    return f'''<svg width="{size}" height="{size}" viewBox="14 12 96 96" xmlns="http://www.w3.org/2000/svg"><g transform="translate(14 12) scale(0.8)"><path d="M85.71 90.64A40 40 0 1 1 85.71 29.36" fill="none" stroke="{fg_big}" stroke-width="12" stroke-linecap="round"/><path d="M72.86 75.32A20 20 0 1 1 72.86 44.68" fill="none" stroke="{fg_small}" stroke-width="10" stroke-linecap="round"/><circle cx="96" cy="60" r="6" fill="{fg_small}"/></g></svg>'''

BASE_CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px}}
body{{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;position:relative;overflow:hidden}}
.d{{font-family:'Inter Display','Inter',sans-serif;letter-spacing:-0.025em}}
.page{{position:absolute;inset:0;padding:96px 88px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:center;gap:18px;font-weight:700;font-size:40px;letter-spacing:-0.02em}}
.kicker{{font-size:24px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase}}
.foot{{position:absolute;left:88px;right:88px;bottom:80px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:600}}
.pill{{display:inline-block;padding:18px 34px;border-radius:999px;font-weight:700;font-size:30px}}
.chat{{border-radius:40px;padding:40px 36px;display:flex;flex-direction:column;gap:22px}}
.b{{max-width:80%;padding:24px 30px;border-radius:30px;font-size:31px;line-height:1.35}}
.me{{align-self:flex-start;border-bottom-left-radius:10px}}
.bot{{align-self:flex-end;border-bottom-right-radius:10px}}
.meta{{font-size:22px;font-weight:600;opacity:.75;margin-bottom:8px}}
.tag{{font-size:21px;font-weight:600;opacity:.65}}
"""

def theme(dark):
    if dark:
        return dict(bg=TEAL, fg=CREAM, sub="#B9C6C6", acc=TERRA, big=CREAM, small=TERRA)
    return dict(bg=CREAM, fg=TEAL, sub=MUTED, acc=TERRA2, big=TEAL, small=TERRA2)

def frame(body, dark, swipe=None, page=None):
    t = theme(dark)
    right = f'<span style="color:{t["acc"]}">{swipe}</span>' if swipe else '<span>www.celea.it</span>'
    num = f'<span style="opacity:.6">{page}</span>' if page else ''
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
body{{background:{t['bg']};color:{t['fg']}}}</style></head><body>
<div class="page">
 <div class="brand">{logo(t['big'], t['small'], 60)}<span class="d">celea</span></div>
 {body}
</div>
<div class="foot" style="color:{t['sub']}">{num or '<span>Receptionist AI · Sicilia → ovunque</span>'}{right}</div>
</body></html>"""

def chat(lines, dark_card=True):
    bg = DEEP if dark_card else "#FFFFFF"
    me_bg = "#1C5E6E" if dark_card else "#D9E6E6"
    bot_bg = TEAL if dark_card else "#FFFFFF"
    fg = CREAM if dark_card else INK
    out = []
    for who, meta, text in lines:
        if who == "me":
            out.append(f'<div class="b me" style="background:{me_bg};color:{fg}"><div class="meta">{meta}</div>{text}</div>')
        else:
            out.append(f'<div class="b bot" style="background:{TERRA if dark_card else TEAL};color:{"#0A3440" if dark_card else CREAM}"><div class="meta">{meta}</div>{text}</div>')
    return f'<div class="chat" style="background:{bg}">{"".join(out)}</div>'

S = {}

# ---------- POST 1: carosello di lancio ----------
S["p1-1"] = frame(f"""
<div style="margin-top:auto;margin-bottom:150px">
 <div class="kicker" style="color:{TERRA2};margin-bottom:36px">Nasce Celea</div>
 <h1 class="d" style="font-size:112px;line-height:1.0;font-weight:800">Il telefono<br>squilla.<br><span style="color:{TERRA2}">Lei è occupato.</span></h1>
 <p style="font-size:38px;line-height:1.4;margin-top:44px;color:{MUTED};font-weight:500">Con un paziente. Con un cliente.<br>Con gli ospiti a colazione.</p>
</div>""", dark=False, swipe="Scorra →", page="1/4")

S["p1-2"] = frame(f"""
<div style="margin-top:auto;margin-bottom:150px">
 <h1 class="d" style="font-size:104px;line-height:1.02;font-weight:800">Celea risponde<br><span style="color:{TERRA}">al posto Suo.</span></h1>
 <p style="font-size:40px;line-height:1.4;margin-top:48px;color:#D7E1E1;font-weight:500">Su WhatsApp e al telefono,<br>24 ore su 24, anche la domenica.</p>
 <div style="display:flex;gap:18px;margin-top:56px">
  <span class="pill" style="background:{DEEP};color:{CREAM}">WhatsApp</span>
  <span class="pill" style="background:{DEEP};color:{CREAM}">Telefono</span>
  <span class="pill" style="background:{TERRA};color:{DEEP}">24/7</span>
 </div>
</div>""", dark=True, swipe="Scorra →", page="2/4")

items = [("Dà informazioni", "Orari, prezzi, servizi: risponde come gli dice Lei."),
         ("Fissa gli appuntamenti", "Raccoglie nome, motivo e preferenze, senza cambiare gestionale."),
         ("Passa a una persona", "Quando serve, la conversazione arriva a Lei o al Suo staff.")]
rows = "".join(f'''<div style="display:flex;gap:30px;align-items:flex-start;padding:38px 0;border-top:2px solid #E3D8C7">
 <div class="d" style="font-size:56px;font-weight:800;color:{TERRA2};width:70px">{i+1}</div>
 <div><div class="d" style="font-size:50px;font-weight:800;line-height:1.1">{a}</div>
 <div style="font-size:31px;line-height:1.4;color:{MUTED};margin-top:12px">{b}</div></div></div>''' for i, (a, b) in enumerate(items))
S["p1-3"] = frame(f"""
<div style="margin-top:70px">
 <div class="kicker" style="color:{TERRA2};margin-bottom:24px">Cosa fa</div>
 <h1 class="d" style="font-size:78px;line-height:1.05;font-weight:800;margin-bottom:40px">Una receptionist<br>che non stacca mai.</h1>
 {rows}
</div>""", dark=False, swipe="Scorra →", page="3/4")

S["p1-4"] = frame(f"""
<div style="margin-top:auto;margin-bottom:150px">
 <div class="kicker" style="color:{TERRA};margin-bottom:36px">Provi adesso</div>
 <h1 class="d" style="font-size:108px;line-height:1.0;font-weight:800">Veda come<br>risponde ai<br>Suoi clienti.</h1>
 <div class="pill d" style="background:{TERRA};color:{DEEP};font-size:44px;padding:26px 46px;margin-top:56px">www.celea.it</div>
 <p style="font-size:32px;line-height:1.4;margin-top:40px;color:#D7E1E1">Demo gratuita, senza registrazione.<br>Per studi dentistici, agenzie immobiliari, B&amp;B e hotel.</p>
</div>""", dark=True, page="4/4")

# ---------- POST 2: studi dentistici ----------
S["p2"] = frame(f"""
<div style="margin-top:56px">
 <div class="kicker" style="color:{TERRA};margin-bottom:22px">Studi dentistici</div>
 <h1 class="d" style="font-size:84px;line-height:1.02;font-weight:800">Ore 22:47.<br>Lo studio è chiuso.<br><span style="color:{TERRA}">Celea no.</span></h1>
 <div style="margin-top:52px">{chat([
   ("me", "Paziente · 22:47", "Buonasera, ho un dolore fortissimo a un dente. Domani potete vedermi?"),
   ("bot", "Celea · assistente virtuale", "Mi dispiace molto. Segnalo subito la Sua richiesta come urgenza allo studio: domattina la richiamano appena apre. Mi lascia nome e numero?"),
 ])}</div>
 <div class="tag" style="margin-top:22px;color:#B9C6C6">Conversazione di esempio · nessun consiglio medico, mai</div>
</div>""", dark=True)

# ---------- POST 3: agenzie immobiliari ----------
S["p3"] = frame(f"""
<div style="margin-top:56px">
 <div class="kicker" style="color:{TERRA2};margin-bottom:22px">Agenzie immobiliari</div>
 <h1 class="d" style="font-size:84px;line-height:1.02;font-weight:800">Domenica, 15:10.<br>L'agenzia è chiusa.<br><span style="color:{TERRA2}">Il cliente no.</span></h1>
 <div style="margin-top:52px">{chat([
   ("me", "Cliente · domenica 15:10", "Buongiorno, il trilocale in centro è ancora disponibile? Vorrei vederlo."),
   ("bot", "Celea · assistente virtuale", "Sì, è ancora disponibile. Le propongo una visita: preferisce martedì mattina o mercoledì pomeriggio?"),
 ], dark_card=False)}</div>
 <div class="tag" style="margin-top:22px;color:{MUTED}">Conversazione di esempio · l'agente conferma lunedì</div>
</div>""", dark=False)

# ---------- POST 4: strutture ricettive ----------
S["p4"] = frame(f"""
<div style="margin-top:56px">
 <div class="kicker" style="color:{TERRA};margin-bottom:22px">B&amp;B, case vacanza e hotel</div>
 <h1 class="d" style="font-size:80px;line-height:1.03;font-weight:800">Ospiti da ovunque.<br><span style="color:{TERRA}">Risposte nella<br>loro lingua.</span></h1>
 <div style="margin-top:46px">{chat([
   ("me", "Ospite · 23:15", "Hallo! Wir kommen erst gegen Mitternacht an. Ist das ein Problem?"),
   ("bot", "Celea · Assistent", "Kein Problem! Ich gebe die Info sofort an die Unterkunft weiter. Sie erhalten die Check-in-Details per WhatsApp."),
 ])}</div>
 <div style="display:flex;gap:16px;margin-top:30px">
  <span class="pill" style="background:{DEEP};color:{CREAM};font-size:26px">Italiano</span>
  <span class="pill" style="background:{DEEP};color:{CREAM};font-size:26px">English</span>
  <span class="pill" style="background:{DEEP};color:{CREAM};font-size:26px">Deutsch</span>
 </div>
</div>""", dark=True)

# ---------- POST 5: clienti fondatori ----------
S["p5"] = frame(f"""
<div style="margin-top:auto;margin-bottom:150px">
 <div class="kicker" style="color:{TERRA2};margin-bottom:36px">Clienti fondatori</div>
 <h1 class="d" style="font-size:120px;line-height:0.98;font-weight:800">Cerchiamo<br><span style="color:{TERRA2}">20 attività</span><br>con cui partire.</h1>
 <p style="font-size:36px;line-height:1.45;margin-top:48px;color:{MUTED};font-weight:500">Studi dentistici, agenzie immobiliari,<br>B&amp;B e hotel. In tutta Italia.</p>
 <div style="margin-top:48px;display:flex;flex-direction:column;gap:14px;font-size:32px;font-weight:600">
  <div>✓&nbsp; Attivazione gratuita per i fondatori</div>
  <div>✓&nbsp; Lo configuriamo noi, su misura</div>
  <div>✓&nbsp; Prima di tutto, provi la demo</div>
 </div>
</div>""", dark=False)

# ---------- POST 6: dietro le quinte ----------
S["p6"] = frame(f"""
<div style="margin-top:auto;margin-bottom:150px">
 <div class="kicker" style="color:{TERRA};margin-bottom:36px">Chi siamo</div>
 <h1 class="d" style="font-size:112px;line-height:1.0;font-weight:800">Nata in Sicilia.<br><span style="color:{TERRA}">Al lavoro<br>ovunque.</span></h1>
 <p style="font-size:36px;line-height:1.45;margin-top:48px;color:#D7E1E1;font-weight:500">Celea nasce a Patti, in provincia di Messina,<br>per dare alle piccole attività italiane<br>una receptionist che non si ferma mai.</p>
</div>""", dark=True)

# ---------- POST 7: fiducia ----------
nevers = [("Non finge di essere una persona.", "Si presenta sempre come assistente virtuale."),
          ("Non dà consigli medici.", "Negli studi dentistici le urgenze vanno subito allo studio."),
          ("Non dice ciò che Lei non vuole.", "Orari, prezzi, tono: decide Lei cosa risponde.")]
rows7 = "".join(f'''<div style="display:flex;gap:28px;align-items:flex-start;padding:36px 0;border-top:2px solid #E3D8C7">
 <div style="width:64px;height:64px;border-radius:50%;background:{TERRA2};color:{CREAM};display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800;flex:none">✕</div>
 <div><div class="d" style="font-size:46px;font-weight:800;line-height:1.12">{a}</div>
 <div style="font-size:30px;line-height:1.4;color:{MUTED};margin-top:10px">{b}</div></div></div>''' for a, b in nevers)
S["p7"] = frame(f"""
<div style="margin-top:70px">
 <div class="kicker" style="color:{TERRA2};margin-bottom:24px">Trasparenza</div>
 <h1 class="d" style="font-size:86px;line-height:1.03;font-weight:800;margin-bottom:44px">Tre cose che Celea<br><span style="color:{TERRA2}">non fa mai.</span></h1>
 {rows7}
</div>""", dark=False)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for name, htm in S.items():
        pg.set_content(htm)
        pg.wait_for_timeout(150)
        pg.screenshot(path=f"{OUT}/{name}.png")
        print("ok", name)
    b.close()
