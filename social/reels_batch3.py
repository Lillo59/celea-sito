# Pacchetto 3: reel lunghi (24–32 s). Eseguito dentro reels.py.

def label(txt, t_in, t_out, col, top=300):
    return el(f'<div style="font-size:30px;font-weight:700;letter-spacing:.16em;color:{col}">{txt}</div>', t_in, t_out, style=f"top:{top}px")

def chat_pages(pages, start, page_dur, dark=True, top0=640, step=290):
    """pages: liste di (who, meta, text). Ogni pagina resta page_dur secondi."""
    out = ""
    for i, page_ in enumerate(pages):
        s, e = start + i * page_dur, start + (i + 1) * page_dur - 0.1
        t = s + 0.3
        for j, (who, meta, text) in enumerate(page_):
            top = top0 + j * step
            if who == "bot":
                out += typing(t, t + 0.9, top, dark=dark)
                t += 0.9
            out += bubble(who, meta, text, t, top, dark=dark, t_out=e)
            t += 1.7
    return out

def scene_time(clock, sub, s, e, dark=True):
    acc = TERRA if dark else TERRA2
    subc = "#D7E1E1" if dark else MUTED
    return (el(f'<div class="d" style="font-size:150px;font-weight:800;line-height:1;color:{acc}">{clock}</div>', s, e, "pop", "top:330px")
          + el(f'<div class="sub" style="color:{subc}">{sub}</div>', s + 0.2, e, style="top:500px"))

def giornata(hook, scenes, dark, cta_line=None):
    """scenes: (orario, contesto, [(who,meta,text),(...)]). 6,2 s per scena."""
    body = el(f'<div class="big d">{hook}</div>', 0.1, 2.6, style="top:620px")
    t = 2.7
    for clock, sub, msgs in scenes:
        e = t + 6.2
        body += scene_time(clock, sub, t, e - 0.1, dark)
        body += chat_pages([msgs], t, 6.2, dark=dark, top0=700, step=300)
        t = e
    body += el('<div class="tag" style="font-size:24px;opacity:.6">Conversazioni di esempio</div>', 2.7, t, "fade", "top:1760px")
    dur = t + 4.2
    kw = {"dark": dark}
    if cta_line: kw["line"] = cta_line
    return (round(dur, 1), dark, page(body + cta(t + 0.1, **kw), dark, round(dur, 1)))

def faq(question, lines, pill, dark):
    acc = TERRA if dark else TERRA2
    subc = "#D7E1E1" if dark else INK
    body = label("LE DOMANDE CHE CI FANNO", 0, 3.4, acc)
    body += el(f'<div class="mid d">{question}</div>', 0.1, 3.4, style="top:380px")
    body += el(f'<div class="mid d" style="color:{acc}">{question}</div>', 3.4, 17.8, "fade", "top:380px;font-size:60px")
    t = 3.8
    for i, ln in enumerate(lines):
        body += el(f'<div class="sub" style="color:{subc};display:flex;gap:22px"><span style="color:{acc};font-weight:800">→</span><span>{ln}</span></div>', t, 17.8, "left", f"top:{760 + i * 260}px")
        t += 2.8
    body += pillc(pill, t + 0.4, 17.8, 1620, bg=(DEEP if dark else TEAL), fg=CREAM, size=32)
    return (22.2, dark, page(body + cta(18.0, dark=dark), dark, 22.2))

R3 = {}

R3["l1-giornata-dentista"] = giornata("Una giornata<br>in studio.<br><span style='color:#E08A6A'>Con Celea.</span>", [
    ("08:12", "Lo studio apre alle 9.", [("me", "Paziente", "Buongiorno, fate pulizie il sabato?"), ("bot", "Celea · assistente virtuale", "Sì, il sabato mattina dalle 9 alle 13. Vuole che Le proponga un orario?")]),
    ("11:40", "La dottoressa è alla poltrona.", [("me", "Paziente", "Devo disdire domani alle 15, scusate."), ("bot", "Celea · assistente virtuale", "Nessun problema, segnalo la disdetta allo studio. Vuole già fissare un'altra data?")]),
    ("14:05", "Pausa pranzo, segreteria chiusa.", [("me", "Nuovo paziente", "Vorrei una prima visita, è possibile?"), ("bot", "Celea · assistente virtuale", "Certo! Mi lascia nome e numero? La segreteria Le conferma l'orario.")]),
    ("22:47", "Lo studio è chiuso.", [("me", "Paziente", "Ho un dolore fortissimo a un dente."), ("bot", "Celea · assistente virtuale", "Segnalo subito la richiesta come urgenza: domattina lo studio La richiama.")]),
], True)

R3["l2-giornata-agenzia"] = giornata("Una giornata<br>in agenzia.<br><span style='color:#C8664A'>Con Celea.</span>", [
    ("07:58", "L'agenzia apre alle 9.", [("me", "Cliente", "Il bilocale al mare è ancora libero?"), ("bot", "Celea · assistente virtuale", "Sì, è disponibile. Vuole che Le proponga una visita?")]),
    ("12:30", "L'agente è a un rogito.", [("me", "Proprietario", "Vorrei far valutare la mia casa."), ("bot", "Celea · assistente virtuale", "Con piacere. Mi lascia indirizzo e numero? L'agente La richiama oggi.")]),
    ("16:15", "Visite in corso.", [("me", "Cliente", "Quanto sono le spese condominiali?"), ("bot", "Celea · assistente virtuale", "Circa 60 € al mese, riscaldamento escluso. Le serve altro?")]),
    ("21:20", "L'agenzia è chiusa.", [("me", "Cliente", "Posso vederlo sabato mattina?"), ("bot", "Celea · assistente virtuale", "Registro la richiesta per sabato mattina: l'agente La conferma domani.")]),
], False)

R3["l3-giornata-bnb"] = giornata("Una giornata<br>in B&amp;B.<br><span style='color:#E08A6A'>Con Celea.</span>", [
    ("07:30", "Colazioni in sala.", [("me", "Ospite", "A che ora è il check-out?"), ("bot", "Celea · assistente virtuale", "Entro le 11. Se Le serve lasciare i bagagli, possiamo tenerli noi.")]),
    ("13:10", "Camere da sistemare.", [("me", "Guest", "Do you have a room for two nights next week?"), ("bot", "Celea · assistant", "Here's our booking link with live availability. Happy to help with anything else!")]),
    ("18:45", "Lei è in giro per la spesa.", [("me", "Gast", "Gibt es einen Parkplatz?"), ("bot", "Celea · Assistent", "Ja, kostenlos im Innenhof. Die Wegbeschreibung schicke ich Ihnen gleich.")]),
    ("23:55", "Lei dorme.", [("me", "Ospite", "Arriviamo all'1, è un problema?"), ("bot", "Celea · assistente virtuale", "Nessun problema: avviso la struttura e Le mando i dettagli per entrare.")]),
], True)

R3["l4-faq-ai"] = faq("I miei clienti sanno<br>che parlano con<br>un'intelligenza artificiale?", [
    "Sì. L'assistente si presenta sempre come assistente virtuale.",
    "È quello che chiedono le regole europee sull'AI (AI Act).",
    "In qualsiasi momento il cliente può chiedere una persona.",
], "Trasparenza, sempre", True)

R3["l5-faq-non-sa"] = faq("E se l'assistente<br>non sa rispondere?", [
    "Non inventa. Dice che verificherà.",
    "Raccoglie la richiesta e la passa alla persona che indica Lei.",
    "Le domande senza risposta Le arrivano nel riepilogo: le aggiungiamo.",
], "La volta dopo sa rispondere", False)

R3["l6-faq-gdpr"] = faq("E i dati dei<br>miei clienti?<br>È a norma GDPR?", [
    "Celea tratta i dati per Suo conto, come responsabile del trattamento.",
    "Firmiamo l'accordo secondo l'art. 28 del GDPR prima di iniziare.",
    "I dati servono solo a rispondere e fissare appuntamenti.",
], "Privacy messa per iscritto", True)

R3["l7-faq-numero"] = faq("Devo cambiare<br>numero o<br>gestionale?", [
    "No. Usiamo il WhatsApp e il telefono che ha già.",
    "Le chiamate a cui non risponde possono passare all'assistente.",
    "Le richieste arrivano alla segreteria come scheda da confermare.",
], "Nessun cambio di gestionale", False)

# l8 — come funziona (flusso + scheda)
steps4 = [("Il cliente scrive o chiama", "WhatsApp o telefono, a qualsiasi ora."),
          ("Celea risponde", "Con le regole e il tono che decide Lei."),
          ("Arriva la scheda", "Nome, motivo, preferenza: tutto in ordine."),
          ("Lei conferma", "Con un tocco, quando ha un minuto.")]
b = el(f'<div class="big d">Come funziona.<br><span style="color:{TERRA}">In 30 secondi.</span></div>', 0.1, 2.8, style="top:620px")
for i, (a, d_) in enumerate(steps4):
    s = 2.9 + i * 3.0
    b += el(f'<div style="display:flex;gap:30px;align-items:flex-start"><div class="d" style="width:96px;height:96px;border-radius:50%;background:{TERRA};color:{DEEP};display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;flex:none">{i+1}</div><div><div class="d" style="font-size:54px;font-weight:800;line-height:1.1">{a}</div><div class="sub" style="color:#D7E1E1;font-size:38px;margin-top:10px">{d_}</div></div></div>', s, 15.2, "left", f"top:{420 + i * 280}px")
card = f'''<div style="background:{CREAM};color:{INK};border-radius:36px;padding:44px 44px">
<div style="font-size:26px;font-weight:700;letter-spacing:.12em;color:{TERRA2}">SCHEDA PER LA SEGRETERIA · ESEMPIO</div>
<div class="d" style="font-size:52px;font-weight:800;margin:18px 0 26px;color:{TEAL}">Nuovo appuntamento</div>
<div style="font-size:38px;line-height:1.7"><b>Nome</b> Giulia (esempio)<br><b>Canale</b> WhatsApp · 22:47<br><b>Motivo</b> igiene<br><b>Preferenza</b> martedì pomeriggio<br><b>Priorità</b> normale</div>
<div style="display:flex;gap:16px;margin-top:30px"><span class="pill" style="background:{TEAL};color:{CREAM};font-size:34px">Conferma</span><span class="pill" style="background:#E3D8C7;color:{TEAL};font-size:34px">Modifica</span></div></div>'''
b += el(card, 15.4, 24.4, "pop", "top:520px")
b += el(f'<div class="mid d">Ecco cosa riceve<br><span style="color:{TERRA}">la Sua segreteria.</span></div>', 15.3, 24.4, style="top:300px;font-size:64px")
R3["l8-come-funziona"] = (28.6, True, page(b + cta(24.5), True, 28.6))

# l9 — prezzi
plans = [("Start WhatsApp", "79 €", "/mese", "Risponde su WhatsApp, 24 ore su 24. Fino a 300 conversazioni al mese."),
         ("Pro", "189 €", "/mese", "Telefono e WhatsApp. 600 minuti di telefonate al mese."),
         ("Pro + sito", "249 €", "/mese", "Tutto il Pro, più un sito vetrina di 5 pagine.")]
b = el(f'<div class="big d">Quanto costa?<br><span style="color:{TERRA2}">Scritto chiaro.</span></div>', 0.1, 2.9, style="top:620px")
for i, (n, p, u, d_) in enumerate(plans):
    s = 3.0 + i * 2.6
    b += el(f'<div style="background:#fff;border-radius:32px;padding:34px 40px;display:flex;justify-content:space-between;gap:24px;align-items:center"><div style="min-width:0"><div class="d" style="font-size:46px;font-weight:800;color:{TEAL}">{n}</div><div style="font-size:30px;color:{MUTED};margin-top:6px;line-height:1.35">{d_}</div></div><div style="text-align:right;flex:none"><span class="d" style="font-size:72px;font-weight:800;color:{TERRA2}">{p}</span><div style="font-size:28px;color:{MUTED}">{u}</div></div></div>', s, 15.6, "up", f"top:{340 + i * 330}px")
b += pillc("Attivazione gratis per i clienti fondatori", 10.8, 15.6, 1380, bg=TEAL, fg=CREAM, size=34)
b += pillc("Prima di pagare: 30 giorni di prova", 12.0, 15.6, 1520, bg=TERRA2, fg=CREAM, size=34)
b += el(f'<div style="font-size:26px;color:{MUTED};text-align:center">Tutti i prezzi e i costi extra su www.celea.it</div>', 12.6, 15.6, "fade", "top:1680px")
R3["l9-prezzi"] = (19.8, False, page(b + cta(15.7, dark=False), False, 19.8))

# l10–l12 — conversazioni complete
def full_chat(kicker, hook, pages, dark, pill):
    acc = TERRA if dark else TERRA2
    body = label(kicker, 0, 2.6 + len(pages) * 8.0, acc)
    body += el(f'<div class="mid d">{hook}</div>', 0.1, 2.6 + len(pages) * 8.0, style="top:370px")
    body += chat_pages(pages, 2.4, 8.0, dark=dark, top0=720, step=300)
    end = 2.4 + len(pages) * 8.0
    body += el('<div class="tag" style="font-size:24px;opacity:.6">Conversazione di esempio · dati inventati</div>', 2.4, end, "fade", "top:1760px")
    body += pillc(pill, end - 2.4, end, 1640, bg=(DEEP if dark else TEAL), fg=CREAM, size=32)
    dur = end + 4.3
    return (round(dur, 1), dark, page(body + cta(end + 0.1, dark=dark), dark, round(dur, 1)))

R3["l10-chat-prima-visita"] = full_chat("STUDI DENTISTICI · CONVERSAZIONE COMPLETA", "Una prima visita,<br><span style='color:#E08A6A'>dall'inizio alla fine.</span>", [
    [("me", "Nuovo paziente", "Buongiorno, vorrei prenotare una prima visita."), ("bot", "Celea · assistente virtuale", "Buongiorno! Con piacere. Preferisce mattina o pomeriggio?"), ("me", "Nuovo paziente", "Pomeriggio, dopo le 17 se si può.")],
    [("bot", "Celea · assistente virtuale", "Perfetto. Mi lascia nome, cognome e numero di telefono?"), ("me", "Nuovo paziente", "Marco Bianchi, 333 000 0000 (esempio)"), ("bot", "Celea · assistente virtuale", "Grazie Marco! La segreteria Le conferma l'orario entro domani mattina.")],
], True, "La segreteria riceve la scheda già compilata")

R3["l11-chat-visita-casa"] = full_chat("AGENZIE IMMOBILIARI · CONVERSAZIONE COMPLETA", "Una richiesta di visita,<br><span style='color:#C8664A'>dall'inizio alla fine.</span>", [
    [("me", "Cliente", "Salve, il trilocale con terrazzo è ancora disponibile?"), ("bot", "Celea · assistente virtuale", "Sì, è disponibile. È in affitto a 650 € al mese, spese escluse."), ("me", "Cliente", "Perfetto, si può vedere questa settimana?")],
    [("bot", "Celea · assistente virtuale", "Certo! Giovedì alle 18 o sabato alle 10: quale preferisce?"), ("me", "Cliente", "Sabato alle 10."), ("bot", "Celea · assistente virtuale", "Registrato. L'agente Le conferma la visita entro 2 ore lavorative.")],
], False, "Prezzo e dati dell'immobile: li decide Lei")

R3["l12-chat-ospite"] = full_chat("B&amp;B · CONVERSAZIONE COMPLETA", "Un ospite straniero,<br><span style='color:#E08A6A'>dall'inizio alla fine.</span>", [
    [("me", "Guest", "Hi! We booked for Friday. Is breakfast included?"), ("bot", "Celea · assistant", "Hi! Yes, breakfast is included, served from 7:30 to 10:30."), ("me", "Guest", "Great. We might arrive late, around 11 pm.")],
    [("bot", "Celea · assistant", "No problem at all. I'll let the host know right away."), ("bot", "Celea · assistant", "On Friday you'll get the self check-in details here on WhatsApp."), ("me", "Guest", "Perfect, thank you!")],
], True, "Risponde in italiano, inglese e tedesco")

# l13 — tre miti
miti = [("«È complicato da attivare.»", "Lo configuriamo noi. Lei ci racconta la Sua attività."),
        ("«Costa come una segretaria.»", "Da 79 € al mese, con 30 giorni di prova prima di pagare."),
        ("«Risponde a caso.»", "Dice solo quello che decide Lei. Se non sa, non inventa.")]
b = el(f'<div class="big d">Tre cose che<br>si dicono<br><span style="color:{TERRA2}">sull\'AI.</span></div>', 0.1, 2.8, style="top:600px")
for i, (m, r) in enumerate(miti):
    s, e = 2.9 + i * 5.2, 2.9 + (i + 1) * 5.2 - 0.1
    b += el(f'<div style="font-size:28px;font-weight:700;letter-spacing:.16em;color:#B3261E">MITO</div>', s, e, "fade", "top:430px")
    b += el(f'<div class="mid d" style="color:{MUTED}">{m}</div>', s + 0.1, e, style="top:490px")
    b += el(f'<div style="font-size:28px;font-weight:700;letter-spacing:.16em;color:{TERRA2}">REALTÀ</div>', s + 1.8, e, "fade", "top:860px")
    b += el(f'<div class="mid d">{r}</div>', s + 1.9, e, style="top:920px;font-size:64px")
R3["l13-tre-miti"] = (22.6, False, page(b + cta(18.5, dark=False), False, 22.6))

# l14 — cosa ricevono i fondatori
perks = ["Attivazione gratuita", "30 giorni di prova prima di pagare", "Configurazione su misura, fatta insieme", "Correzioni finché risponde come vuole Lei"]
b = el(f'<div class="big d">Le prime 20<br>attività<br><span style="color:{TERRA}">ricevono:</span></div>', 0.1, 14.6, style="top:380px")
for i, p_ in enumerate(perks):
    b += el(f'<div class="sub" style="display:flex;gap:22px;font-size:48px;font-weight:600"><span style="color:{TERRA};font-weight:800">✓</span>{p_}</div>', 2.6 + i * 2.2, 14.6, "left", f"top:{820 + i * 170}px")
b += pillc("Studi dentistici · agenzie · B&amp;B e hotel", 11.6, 14.6, 1560, bg=DEEP, fg=CREAM, size=32)
R3["l14-fondatori"] = (18.8, True, page(b + cta(14.7, line="Scriva <b>FONDATORE</b> nei commenti"), True, 18.8))

R.update(R3)
