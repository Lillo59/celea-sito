"""Post statici settimana 3 (2–8 novembre). Riusa frame() e stili di gen.py."""
import os
src = open("gen.py").read().split("S = {}")[0]
exec(src.replace('OUT = sys.argv[1] if len(sys.argv) > 1 else "out"', 'OUT = "out3"'))
from playwright.sync_api import sync_playwright
os.makedirs("out3", exist_ok=True)
S = {}

def rows(items, acc, mute, mark="✓", size=46):
    return "".join(f'''<div style="display:flex;gap:28px;align-items:flex-start;padding:30px 0;border-top:2px solid {"#E3D8C7" if mute == MUTED else "#22606F"}">
 <div style="width:60px;height:60px;border-radius:50%;background:{acc};color:{CREAM if mute == MUTED else DEEP};display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:800;flex:none">{mark if mark else i+1}</div>
 <div><div class="d" style="font-size:{size}px;font-weight:800;line-height:1.12">{a}</div>
 <div style="font-size:30px;line-height:1.4;color:{mute};margin-top:8px">{b}</div></div></div>''' for i, (a, b) in enumerate(items))

# Q1 carosello: come funziona
steps = [("Il cliente scrive o chiama", "Su WhatsApp o al telefono, a qualsiasi ora."), ("Celea risponde", "Con le informazioni e il tono che decide Lei."), ("Arriva la scheda", "Nome, motivo e preferenza, già in ordine."), ("Lei conferma", "Quando ha un minuto, senza interruzioni.")]
S["q1-1"] = frame(f'''<div style="margin-top:auto;margin-bottom:150px"><div class="kicker" style="color:{TERRA};margin-bottom:36px">Come funziona</div>
<h1 class="d" style="font-size:120px;line-height:1.0;font-weight:800">Quattro<br>passaggi.<br><span style="color:{TERRA}">Zero lavoro<br>tecnico.</span></h1></div>''', dark=True, swipe="Scorra →", page="1/3")
S["q1-2"] = frame(f'''<div style="margin-top:80px"><div class="kicker" style="color:{TERRA2};margin-bottom:24px">Ogni giorno</div>
<h1 class="d" style="font-size:76px;line-height:1.05;font-weight:800;margin-bottom:36px">Dal messaggio<br>all'appuntamento.</h1>{rows(steps, TEAL, MUTED, mark=None)}</div>''', dark=False, swipe="Scorra →", page="2/3")
S["q1-3"] = frame(f'''<div style="margin-top:auto;margin-bottom:150px"><div class="kicker" style="color:{TERRA};margin-bottom:36px">Provi adesso</div>
<h1 class="d" style="font-size:100px;line-height:1.02;font-weight:800">Attivo in<br>due settimane.</h1>
<p style="font-size:36px;line-height:1.45;margin-top:40px;color:#D7E1E1">Lo configuriamo noi, lo proviamo insieme,<br>parte prima fuori orario.</p>
<div class="pill d" style="background:{TERRA};color:{DEEP};font-size:44px;padding:26px 46px;margin-top:48px">www.celea.it</div></div>''', dark=True, page="3/3")

# Q2 prezzi
plans = [("Start WhatsApp", "79 €", "WhatsApp 24 ore su 24 · fino a 300 conversazioni al mese"), ("Pro", "189 €", "Telefono e WhatsApp · 600 minuti di telefonate al mese"), ("Pro + sito", "249 €", "Tutto il Pro · sito vetrina di 5 pagine incluso")]
cards = "".join(f'''<div style="background:#fff;border-radius:28px;padding:30px 36px;display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:22px">
<div style="min-width:0"><div class="d" style="font-size:44px;font-weight:800">{n}</div><div style="font-size:27px;color:{MUTED};margin-top:6px;line-height:1.35">{d}</div></div>
<div style="text-align:right;flex:none"><div class="d" style="font-size:64px;font-weight:800;color:{TERRA2}">{p}</div><div style="font-size:24px;color:{MUTED}">al mese</div></div></div>''' for n, p, d in plans)
S["q2"] = frame(f'''<div style="margin-top:70px"><div class="kicker" style="color:{TERRA2};margin-bottom:24px">Prezzi</div>
<h1 class="d" style="font-size:84px;line-height:1.03;font-weight:800;margin-bottom:40px">Tutto quello<br>che paga, <span style="color:{TERRA2}">scritto.</span></h1>{cards}
<div style="font-size:30px;font-weight:600;margin-top:20px">✓ Attivazione gratis per i clienti fondatori &nbsp; ✓ 30 giorni di prova</div></div>''', dark=False)

# Q3 AI Act
S["q3"] = frame(f'''<div style="margin-top:auto;margin-bottom:150px"><div class="kicker" style="color:{TERRA};margin-bottom:36px">Le domande che ci fanno</div>
<h1 class="d" style="font-size:80px;line-height:1.05;font-weight:800">«I miei clienti sanno<br>che parlano con<br>un'intelligenza<br>artificiale?»</h1>
<p class="d" style="font-size:96px;font-weight:800;color:{TERRA};margin-top:44px">Sì.</p>
<p style="font-size:34px;line-height:1.45;margin-top:20px;color:#D7E1E1">Si presenta sempre come assistente virtuale,<br>come chiede l'AI Act europeo. E il cliente può<br>chiedere una persona in qualsiasi momento.</p></div>''', dark=True)

# Q4 scheda segreteria
S["q4"] = frame(f'''<div style="margin-top:60px"><div class="kicker" style="color:{TERRA2};margin-bottom:24px">Cosa riceve la segreteria</div>
<h1 class="d" style="font-size:80px;line-height:1.04;font-weight:800;margin-bottom:44px">Una scheda,<br><span style="color:{TERRA2}">già compilata.</span></h1>
<div style="background:#fff;border-radius:36px;padding:44px">
<div style="font-size:24px;font-weight:700;letter-spacing:.12em;color:{TERRA2}">STUDIO DENTISTICO · ESEMPIO</div>
<div class="d" style="font-size:50px;font-weight:800;margin:14px 0 22px">Nuovo appuntamento</div>
<div style="font-size:34px;line-height:1.75;color:{INK}"><b>Nome</b> Giulia (esempio)<br><b>Canale</b> WhatsApp · ore 22:47<br><b>Motivo</b> igiene<br><b>Preferenza</b> martedì pomeriggio<br><b>Priorità</b> normale</div>
<div style="display:flex;gap:16px;margin-top:28px"><span class="pill" style="background:{TEAL};color:{CREAM}">Conferma</span><span class="pill" style="background:#E3D8C7;color:{TEAL}">Modifica</span></div></div></div>''', dark=False)

# Q5 GDPR
gd = [("Responsabile del trattamento", "Celea tratta i dati per Suo conto, non per sé."), ("Accordo art. 28 GDPR", "Lo firmiamo prima di iniziare."), ("Solo i dati necessari", "Per rispondere, fissare appuntamenti e passare le richieste.")]
S["q5"] = frame(f'''<div style="margin-top:70px"><div class="kicker" style="color:{TERRA};margin-bottom:24px">Privacy</div>
<h1 class="d" style="font-size:84px;line-height:1.03;font-weight:800;margin-bottom:40px">I dati dei Suoi<br>clienti, <span style="color:{TERRA}">messi<br>per iscritto.</span></h1>{rows(gd, TERRA, "#D7E1E1")}</div>''', dark=True)

# Q6 niente da cambiare
nc = [("Stesso numero", "Le chiamate a cui non risponde possono passare all'assistente."), ("Stesso WhatsApp", "Colleghiamo quello che usa già."), ("Stesso gestionale", "Le richieste arrivano come scheda da confermare.")]
S["q6"] = frame(f'''<div style="margin-top:70px"><div class="kicker" style="color:{TERRA2};margin-bottom:24px">Nessun cambio</div>
<h1 class="d" style="font-size:84px;line-height:1.03;font-weight:800;margin-bottom:40px">Non deve<br>cambiare <span style="color:{TERRA2}">niente.</span></h1>{rows(nc, TERRA2, MUTED)}</div>''', dark=False)

# Q7 fondatori
pk = [("Attivazione gratuita", "Per le prime 20 attività."), ("30 giorni di prova", "Prima di pagare qualsiasi cosa."), ("Configurazione insieme", "E correzioni finché risponde come vuole Lei.")]
S["q7"] = frame(f'''<div style="margin-top:70px"><div class="kicker" style="color:{TERRA};margin-bottom:24px">Clienti fondatori</div>
<h1 class="d" style="font-size:90px;line-height:1.02;font-weight:800;margin-bottom:40px">Cosa ricevono<br><span style="color:{TERRA}">i primi 20.</span></h1>{rows(pk, TERRA, "#D7E1E1")}
<div style="font-size:32px;font-weight:600;margin-top:24px;color:#D7E1E1">Scriva FONDATORE nei commenti.</div></div>''', dark=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for name, htm in S.items():
        pg.set_content(htm); pg.wait_for_timeout(150)
        pg.screenshot(path=f"out3/{name}.png"); print("ok", name)
    b.close()
