# Pacchetto 2: eseguito dentro reels.py (usa el, bubble, typing, cta, page, mark, colori).
JS_WAVE = """<script>(function(){const r=window.render;window.render=function(t){r(t);document.querySelectorAll('.wave span').forEach((s,i)=>{s.style.height=(30+150*Math.abs(Math.sin(t*6+i*0.7)*Math.sin(t*2.3+i*0.31)))+'px';});};render(0);})();</script>"""

def kick(txt, t_in, t_out, col):
    return el(f'<div style="font-size:30px;font-weight:700;letter-spacing:.16em;color:{col}">{txt}</div>', t_in, t_out, style="top:300px")

def pillc(txt, t_in, t_out, top, bg=DEEP, fg=CREAM, size=36):
    return el(f'<div style="text-align:center"><span class="pill" style="background:{bg};color:{fg};font-size:{size}px">{txt}</span></div>', t_in, t_out, "pop", f"top:{top}px")

# r7 — spostare un appuntamento
R["r7-spostare-appuntamento"] = (14, True, page(
    kick("STUDI DENTISTICI", 0, 9.4, TERRA)
  + el(f'<div class="mid d">Spostare un<br>appuntamento?<br><span style="color:{TERRA}">Due messaggi.</span></div>', 0.1, 9.4, style="top:370px")
  + bubble("me", "Paziente", "Devo spostare la pulizia di giovedì, si può?", 1.4, 800, t_out=9.4)
  + typing(2.6, 3.6, 1040)
  + bubble("bot", "Celea · assistente virtuale", "Certo! Ho libero venerdì alle 10:00 o lunedì alle 16:30. Quale preferisce?", 3.6, 1040, t_out=9.4)
  + bubble("me", "Paziente", "Venerdì alle 10, grazie.", 5.6, 1330, t_out=9.4)
  + pillc("✓ Richiesta pronta per lo studio", 7.0, 9.4, 1520)
  + cta(9.6), True, 14))

# r8 — le stesse domande ogni giorno
qs = ["È ancora disponibile?", "Quanto sono le spese?", "Si accettano animali?", "Quando posso vederlo?", "Serve una garanzia?"]
b8 = kick("AGENZIE IMMOBILIARI", 0, 6.3, TERRA2)
b8 += el(f'<div class="mid d">Le stesse domande.<br><span style="color:{TERRA2}">Tutti i giorni.</span></div>', 0.1, 6.3, style="top:370px")
for i, q in enumerate(qs):
    b8 += el(f'<div style="display:flex;justify-content:{"flex-start" if i % 2 == 0 else "flex-end"}"><div class="b" style="background:#fff;color:{INK}">{q}</div></div>', 1.2 + i * 0.7, 6.3, "pop", f"top:{700 + i * 165}px")
b8 += el(f'<div class="mid d">Celea risponde<br>a tutte.<br><span style="color:{TERRA2}">Lei pensa<br>alle visite.</span></div>', 6.4, 9.5, style="top:620px")
R["r8-domande-affitto"] = (13.5, False, page(b8 + cta(9.6, dark=False), False, 13.5))

# r9 — parcheggio alle 2 di notte
R["r9-parcheggio-notte"] = (14, True, page(
    kick("B&amp;B · CASE VACANZA · HOTEL", 0, 9.4, TERRA)
  + el(f'<div class="mid d">«C\'è il parcheggio?»<br><span style="color:{TERRA}">alle 2 di notte.</span></div>', 0.1, 9.4, style="top:370px")
  + bubble("me", "Guest · 02:04", "Hi! Is there parking at the B&amp;B? We're driving from Palermo.", 1.5, 760, t_out=9.4)
  + typing(3.0, 4.2, 1050)
  + bubble("bot", "Celea · assistant", "Yes! Free private parking in the courtyard. I'll send you the directions with your check-in details.", 4.2, 1050, t_out=9.4)
  + pillc("Risponde con le informazioni che sceglie Lei", 6.8, 9.4, 1460, size=32)
  + cta(9.6), True, 14))

# r10 — prima e dopo
senza = ["Il telefono squilla mentre lavora", "I messaggi della sera restano lì", "Il cliente va da un altro"]
con = ["Risponde sempre, anche di notte", "Le richieste arrivano in ordine", "Lei lavora senza interruzioni"]
b10 = el(f'<div class="mid d" style="color:#B3261E">Senza Celea</div>', 0.2, 4.6, style="top:420px")
for i, s in enumerate(senza):
    b10 += el(f'<div class="sub" style="display:flex;gap:24px;align-items:center"><span style="color:#B3261E;font-weight:800;font-size:56px">✕</span>{s}</div>', 0.9 + i * 0.8, 4.6, "left", f"top:{640 + i * 150}px")
b10 += el(f'<div class="mid d" style="color:{TERRA2}">Con Celea</div>', 4.8, 9.4, style="top:420px")
for i, s in enumerate(con):
    b10 += el(f'<div class="sub" style="display:flex;gap:24px;align-items:center"><span style="color:{TERRA2};font-weight:800;font-size:56px">✓</span>{s}</div>', 5.4 + i * 0.8, 9.4, "right", f"top:{640 + i * 150}px")
R["r10-prima-dopo"] = (13.5, False, page(b10 + cta(9.6, dark=False), False, 13.5))

# r11 — risponde anche al telefono
bars = "".join('<span style="display:inline-block;width:22px;margin:0 7px;border-radius:11px;background:#E08A6A;height:40px;vertical-align:middle"></span>' for _ in range(22))
b11 = el(f'<div class="mid d">Non solo WhatsApp.<br><span style="color:{TERRA}">Risponde anche<br>al telefono.</span></div>', 0.1, 3.2, style="top:520px")
b11 += el(f'<div class="wave" style="height:220px;display:flex;align-items:center;justify-content:center">{bars}</div>', 3.2, 9.4, "fade", "top:420px")
b11 += el(f'<div class="b" style="background:{DEEP};color:{CREAM};max-width:100%"><div class="meta">Celea · al telefono</div>«Buongiorno, sono l\'assistente virtuale dello studio. Come posso aiutarla?»</div>', 3.6, 9.4, "up", "top:760px")
b11 += el(f'<div class="b" style="background:#1C5E6E;color:{CREAM};max-width:100%"><div class="meta">Paziente</div>«Vorrei prenotare una visita di controllo.»</div>', 5.4, 9.4, "up", "top:1080px")
b11 += pillc("Voce naturale · italiano, inglese, tedesco", 7.0, 9.4, 1380, size=32)
R["r11-al-telefono"] = (14, True, page(b11 + cta(9.6), True, 14) .replace("</body>", JS_WAVE + "</body>"))

# r12 — attivo in due settimane
steps3 = [("Ci racconta la Sua attività", "Una chiamata di 45 minuti."), ("Lo prepariamo e lo proviamo insieme", "Lei fa le domande difficili, noi correggiamo."), ("Parte, prima fuori orario", "La sera e nel weekend, poi quando vuole Lei.")]
b12 = el(f'<div class="mid d">Attivo in<br><span style="color:{TERRA2}">due settimane.</span></div>', 0.1, 9.4, style="top:380px")
b12 += el(f'<div class="sub" style="color:{MUTED}">Senza lavoro tecnico per Lei.</div>', 0.6, 9.4, style="top:600px")
for i, (a, b_) in enumerate(steps3):
    s = 1.6 + i * 2.2
    b12 += el(f'<div style="display:flex;gap:30px;align-items:flex-start"><div class="d" style="width:96px;height:96px;border-radius:50%;background:{TEAL};color:{CREAM};display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;flex:none">{i+1}</div><div><div class="d" style="font-size:52px;font-weight:800;line-height:1.1">{a}</div><div class="sub" style="color:{MUTED};font-size:38px;margin-top:10px">{b_}</div></div></div>', s, 9.4, "left", f"top:{760 + i * 270}px")
R["r12-tre-passi"] = (13.5, False, page(b12 + cta(9.6, dark=False), False, 13.5))

# r13 — passa a una persona
R["r13-una-persona"] = (14, True, page(
    el(f'<div class="mid d">E se la domanda<br><span style="color:{TERRA}">è difficile?</span></div>', 0.1, 9.4, style="top:380px")
  + bubble("me", "Paziente", "Ho un preventivo da discutere, posso parlare con il dottore?", 1.4, 720, t_out=9.4)
  + typing(2.9, 4.0, 1010)
  + bubble("bot", "Celea · assistente virtuale", "Certo. Avviso subito lo studio con la Sua richiesta: La ricontattano loro appena possibile.", 4.0, 1010, t_out=9.4)
  + pillc("Una persona, quando serve", 6.6, 9.4, 1420, bg=TERRA, fg=DEEP, size=40)
  + cta(9.6), True, 14))

# r14 — «ai clienti non piacciono i bot»
R["r14-bot"] = (13.5, False, page(
    el(f'<div class="mid d" style="color:{MUTED}">«Ai clienti<br>non piacciono<br>i bot.»</div>', 0.1, 3.0, style="top:560px")
  + el(f'<div class="mid d">Ai clienti<br>non piace<br><span style="color:{TERRA2}">restare senza<br>risposta.</span></div>', 3.1, 6.4, style="top:520px")
  + el(f'<div class="sub">Celea si presenta come<br><b style="color:{TEAL}">assistente virtuale</b>, risponde<br>subito e passa a una persona<br>quando serve.</div>', 6.5, 9.4, style="top:620px")
  + cta(9.6, dark=False), False, 13.5))

# r15 — 62 ore chiusi
R["r15-weekend"] = (14, True, page(
    el(f'<div class="sub" style="color:#D7E1E1">Venerdì 19:00 → lunedì 9:00</div>', 0.2, 6.6, style="top:460px")
  + el(f'<div class="d" style="font-size:300px;font-weight:800;line-height:1;color:{TERRA}">62</div>', 0.6, 6.6, "pop", "top:560px")
  + el(f'<div class="mid d">ore con l\'attività<br>chiusa.</div>', 1.4, 6.6, style="top:900px")
  + el(f'<div class="sub" style="color:#D7E1E1">I clienti, intanto, scrivono lo stesso.</div>', 3.2, 6.6, style="top:1140px")
  + el(f'<div class="mid d">Celea risponde<br><span style="color:{TERRA}">a tutti, anche<br>nel weekend.</span></div>', 6.7, 9.4, style="top:620px")
  + cta(9.6), True, 14))

# r16 — 30 giorni gratis
R["r16-prova-gratis"] = (13.5, False, page(
    el(f'<div class="mid d">Prima di pagare,</div>', 0.1, 9.4, style="top:440px")
  + el(f'<div class="d" style="font-size:250px;font-weight:800;line-height:1;color:{TERRA2}">30</div>', 0.6, 9.4, "pop", "top:560px")
  + el(f'<div class="mid d">giorni gratis.</div>', 1.0, 9.4, style="top:830px")
  + el(f'<div class="sub" style="display:flex;gap:20px"><span style="color:{TERRA2};font-weight:800">✓</span>Fino a 100 minuti di telefonate</div>', 2.6, 9.4, "left", "top:1040px")
  + el(f'<div class="sub" style="display:flex;gap:20px"><span style="color:{TERRA2};font-weight:800">✓</span>Lo configuriamo noi</div>', 3.3, 9.4, "left", "top:1140px")
  + el(f'<div class="sub" style="display:flex;gap:20px"><span style="color:{TERRA2};font-weight:800">✓</span>Parte prima fuori orario</div>', 4.0, 9.4, "left", "top:1240px")
  + cta(9.6, dark=False), False, 13.5))

# r17 — tre mestieri
mest = [("Studi dentistici", "Prime visite, controlli, spostamenti. Le urgenze vanno subito allo studio."),
        ("Agenzie immobiliari", "Disponibilità, spese, richieste di visita. Anche la domenica."),
        ("B&amp;B e hotel", "Check-in, parcheggio, servizi. In italiano, inglese e tedesco.")]
b17 = el(f'<div class="mid d">Pensato per<br><span style="color:{TERRA}">tre mestieri.</span></div>', 0.1, 1.8, style="top:620px")
for i, (a, b_) in enumerate(mest):
    s, e = 1.8 + i * 2.6, 1.8 + (i + 1) * 2.6
    b17 += el(f'<div class="d" style="font-size:180px;font-weight:800;line-height:1;color:{TERRA}">0{i+1}</div>', s, e, "pop", "top:420px")
    b17 += el(f'<div class="mid d">{a}</div>', s + 0.15, e, style="top:680px")
    b17 += el(f'<div class="sub" style="color:#D7E1E1">{b_}</div>', s + 0.5, e, style="top:820px")
R["r17-tre-mestieri"] = (13.5, True, page(b17 + cta(9.7), True, 13.5))

# r18 — dalla Sicilia
R["r18-sicilia"] = (13.5, False, page(
    el(f'<div class="big d">Da Patti,<br><span style="color:{TERRA2}">in Sicilia.</span></div>', 0.1, 3.4, style="top:560px")
  + el(f'<div class="mid d">Per le piccole<br>attività di<br><span style="color:{TERRA2}">tutta Italia.</span></div>', 3.5, 6.6, style="top:560px")
  + el(f'<div class="mid d">Siamo all\'inizio.<br><span style="color:{TERRA2}">Cerchiamo<br>i primi 20.</span></div>', 6.7, 9.6, style="top:560px")
  + cta(9.7, dark=False, line="Scriva <b>FONDATORE</b> nei commenti"), False, 13.5))
