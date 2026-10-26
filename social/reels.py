"""Reel animati Celea 1080x1920: frame da HTML (Playwright) + musica originale sintetizzata + ffmpeg."""
import os, sys, subprocess, wave
import numpy as np
from playwright.sync_api import sync_playwright

FPS = 30
W, H = 1080, 1920
TEAL, DEEP, CREAM, TERRA, TERRA2, INK, MUTED = "#0F4C5C", "#0A3440", "#F4EDE3", "#E08A6A", "#C8664A", "#1F2D33", "#5B6B70"
OUT = "reels"
os.makedirs(OUT, exist_ok=True)

def mark(big, small, s):
    return f'<svg width="{s}" height="{s}" viewBox="14 12 96 96"><g transform="translate(14 12) scale(0.8)"><path d="M85.71 90.64A40 40 0 1 1 85.71 29.36" fill="none" stroke="{big}" stroke-width="12" stroke-linecap="round"/><path d="M72.86 75.32A20 20 0 1 1 72.86 44.68" fill="none" stroke="{small}" stroke-width="10" stroke-linecap="round"/><circle cx="96" cy="60" r="6" fill="{small}"/></g></svg>'

PHONE = f'<svg width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="{TERRA}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased;position:relative}}
.d{{font-family:'Inter Display',Inter,sans-serif;letter-spacing:-0.03em}}
.a{{position:absolute;left:90px;right:90px;opacity:0;will-change:transform,opacity}}
.brand{{position:absolute;top:150px;left:90px;display:flex;align-items:center;gap:16px;font-size:40px;font-weight:700}}
.big{{font-size:118px;line-height:1.0;font-weight:800}}
.mid{{font-size:84px;line-height:1.04;font-weight:800}}
.sub{{font-size:46px;line-height:1.35;font-weight:500}}
.b{{max-width:84%;padding:30px 36px;border-radius:36px;font-size:40px;line-height:1.32}}
.meta{{font-size:26px;font-weight:600;opacity:.75;margin-bottom:8px}}
.pill{{display:inline-block;padding:26px 46px;border-radius:999px;font-weight:800;font-size:52px}}
.dots span{{display:inline-block;width:18px;height:18px;border-radius:50%;margin:0 6px;background:currentColor}}
"""

JS = """
window.render = function(t){
  document.querySelectorAll('[data-in]').forEach(el=>{
    const a=+el.dataset.in, b=+(el.dataset.out||999), an=el.dataset.anim||'up', d=0.45;
    let p=0;
    if(t>=a && t<b){ p=Math.min(1,(t-a)/d); const q=Math.min(1,(b-t)/0.3); p=Math.min(p,q); }
    const e=1-Math.pow(1-Math.max(0,p),3);
    el.style.opacity=e;
    if(an==='up') el.style.transform=`translateY(${(1-e)*60}px)`;
    else if(an==='pop') el.style.transform=`scale(${0.8+0.2*e})`;
    else if(an==='left') el.style.transform=`translateX(${(1-e)*-80}px)`;
    else if(an==='right') el.style.transform=`translateX(${(1-e)*80}px)`;
    else el.style.transform='none';
    if(el.dataset.shake && t>=a && t<b){ el.style.transform+=` rotate(${Math.sin(t*40)*8*((Math.floor(t*2)%2)?1:0)}deg)`; }
    if(el.classList.contains('dots')){ el.querySelectorAll('span').forEach((s,i)=>{s.style.opacity=0.3+0.7*Math.max(0,Math.sin(t*8-i*0.9));}); }
  });
  const bar=document.getElementById('bar'); if(bar) bar.style.width=(t/window.DUR*100)+'%';
};
"""

def el(html, t_in, t_out=None, anim="up", style="", cls="a", extra=""):
    out = f' data-out="{t_out}"' if t_out is not None else ""
    return f'<div class="{cls}" data-in="{t_in}"{out} data-anim="{anim}" style="{style}" {extra}>{html}</div>'

def bubble(who, meta, text, t_in, top, dark=True, t_out=9.5):
    if who == "me":
        bg, fg, align = ("#1C5E6E" if dark else "#D9E6E6"), (CREAM if dark else INK), "flex-start"
        r = "border-bottom-left-radius:10px"
        anim = "left"
    else:
        bg, fg, align = (TERRA if dark else TEAL), (DEEP if dark else CREAM), "flex-end"
        r = "border-bottom-right-radius:10px"
        anim = "right"
    return el(f'<div style="display:flex;justify-content:{align}"><div class="b" style="background:{bg};color:{fg};{r}"><div class="meta">{meta}</div>{text}</div></div>', t_in, t_out, anim=anim, style=f"top:{top}px")

def typing(t_in, t_out, top, right=True, dark=True):
    col = TERRA if dark else TEAL
    j = "flex-end" if right else "flex-start"
    return el(f'<div style="display:flex;justify-content:{j}"><div class="b dots" data-in="{t_in}" data-out="{t_out}" data-anim="fade" style="background:{"#1C5E6E" if dark else "#fff"};color:{col}"><span></span><span></span><span></span></div></div>', t_in, t_out, anim="fade", style=f"top:{top}px")

def cta(t_in, dark=True, line="Commenti <b>DEMO</b> e Le mandiamo il link"):
    fg = CREAM if dark else TEAL
    acc = TERRA if dark else TERRA2
    return (el(f'<div style="display:flex;justify-content:center">{mark(fg, acc, 220)}</div>', t_in, anim="pop", style="top:430px")
          + el(f'<div class="mid d" style="text-align:center;color:{fg}">Provi la demo<br>gratuita</div>', t_in + 0.3, style="top:720px")
          + el(f'<div style="text-align:center"><span class="pill d" style="background:{acc};color:{DEEP if dark else CREAM}">www.celea.it</span></div>', t_in + 0.6, anim="pop", style="top:960px")
          + el(f'<div class="sub" style="text-align:center;color:{fg}">{line}<br><span style="opacity:.7">oppure link in bio</span></div>', t_in + 0.9, style="top:1130px"))

def page(body, dark, dur):
    bg, fg, acc = (TEAL, CREAM, TERRA) if dark else (CREAM, TEAL, TERRA2)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="background:{bg};color:{fg}">
<div class="brand">{mark(fg, acc, 58)}<span class="d">celea</span></div>
{body}
<div style="position:absolute;left:0;bottom:0;height:10px;width:0;background:{acc}" id="bar"></div>
<script>window.DUR={dur};{JS}render(0);</script></body></html>"""

R = {}

# R1 — La chiamata persa (13s)
R["r1-chiamata-persa"] = (13, True, page(
    el(f'<div style="display:flex;justify-content:center">{PHONE}</div>', 0.0, 5.0, "pop", "top:420px", extra='data-shake="1"')
  + el(f'<div class="big d" style="text-align:center">Squilla.</div>', 0.2, 2.6, style="top:700px")
  + el(f'<div class="sub" style="text-align:center;color:#D7E1E1">Lei è con un cliente.</div>', 0.8, 2.6, style="top:850px")
  + el(f'<div class="big d" style="text-align:center">Squilla<br>ancora.</div>', 2.6, 5.0, style="top:700px")
  + el(f'<div style="text-align:center"><span class="pill" style="background:#B3261E;color:#fff;font-size:40px">✕ Chiamata persa</span></div>', 3.6, 5.0, "pop", "top:1000px")
  + el(f'<div class="mid d">Quel cliente<br>adesso chiama<br><span style="color:{TERRA}">un altro.</span></div>', 5.2, 8.2, style="top:620px")
  + el(f'<div class="mid d">Con Celea<br><span style="color:{TERRA}">risponde sempre.</span></div>', 8.2, 10.0, style="top:620px")
  + el(f'<div class="sub" style="color:#D7E1E1">WhatsApp e telefono, 24 ore su 24.</div>', 8.6, 10.0, style="top:900px")
  + cta(10.0), True, 13))

# R2 — Dentista ore 22:47 (14s)
R["r2-dentista"] = (14, True, page(
    el('<div class="kick" style="font-size:30px;font-weight:700;letter-spacing:.16em;color:#E08A6A">STUDI DENTISTICI</div>', 0, 9.5, style="top:300px")
  + el(f'<div class="mid d">Ore 22:47.<br>Lo studio è chiuso.</div>', 0.1, 9.5, style="top:370px")
  + bubble("me", "Paziente · 22:47", "Ho un dolore fortissimo a un dente. Domani potete vedermi?", 1.6, 720)
  + typing(3.2, 4.6, 1020)
  + bubble("bot", "Celea · assistente virtuale", "Mi dispiace. Segnalo subito la richiesta come urgenza: domattina lo studio La richiama appena apre. Mi lascia nome e numero?", 4.6, 1020)
  + el(f'<div style="text-align:center"><span class="pill" style="background:{DEEP};color:{CREAM};font-size:36px">✓ Urgenza segnalata allo studio</span></div>', 7.2, 9.5, "pop", "top:1460px")
  + cta(9.6), True, 14))

# R3 — Agenzia immobiliare domenica (14s)
R["r3-immobiliare"] = (14, False, page(
    el(f'<div style="font-size:30px;font-weight:700;letter-spacing:.16em;color:{TERRA2}">AGENZIE IMMOBILIARI</div>', 0, 9.5, style="top:300px")
  + el(f'<div class="mid d">Domenica, 15:10.<br><span style="color:{TERRA2}">L\'agenzia è chiusa.</span></div>', 0.1, 9.5, style="top:370px")
  + bubble("me", "Cliente · domenica", "Il trilocale in centro è ancora disponibile? Vorrei vederlo.", 1.6, 720, dark=False)
  + typing(3.2, 4.5, 1000, dark=False)
  + bubble("bot", "Celea · assistente virtuale", "Sì, è disponibile. Le propongo una visita: martedì mattina o mercoledì pomeriggio?", 4.5, 1000, dark=False)
  + el(f'<div class="sub" style="text-align:center;color:{MUTED}">Lunedì l\'agente trova la visita pronta da confermare.</div>', 7.0, 9.5, style="top:1400px")
  + cta(9.6, dark=False), False, 14))

# R4 — Ospiti in tre lingue (14s)
langs = [("Italiano", "Arriviamo verso mezzanotte, è un problema?", "Nessun problema! Avviso subito la struttura e Le mando i dettagli del check-in."),
         ("English", "We'll arrive around midnight, is that ok?", "No problem! I'll let the host know right away and send you the check-in details."),
         ("Deutsch", "Wir kommen erst gegen Mitternacht an. Geht das?", "Kein Problem! Ich informiere die Unterkunft und schicke Ihnen die Check-in-Details.")]
b4 = el('<div style="font-size:30px;font-weight:700;letter-spacing:.16em;color:#E08A6A">B&amp;B · CASE VACANZA · HOTEL</div>', 0, 10.4, style="top:300px")
b4 += el(f'<div class="mid d">Ospiti da ovunque.<br><span style="color:{TERRA}">Risposte nella<br>loro lingua.</span></div>', 0.1, 10.4, style="top:370px")
for i, (lg, q, a) in enumerate(langs):
    s, e = 1.6 + i * 2.9, 1.6 + (i + 1) * 2.9
    b4 += el(f'<div style="text-align:center"><span class="pill" style="background:{DEEP};color:{CREAM};font-size:34px">{lg}</span></div>', s, e, "pop", "top:760px")
    b4 += el(f'<div style="display:flex"><div class="b" style="background:#1C5E6E;color:{CREAM};border-bottom-left-radius:10px">{q}</div></div>', s + 0.2, e, "left", "top:900px")
    b4 += el(f'<div style="display:flex;justify-content:flex-end"><div class="b" style="background:{TERRA};color:{DEEP};border-bottom-right-radius:10px">{a}</div></div>', s + 1.0, e, "right", "top:1140px")
R["r4-ospiti-lingue"] = (14.5, True, page(b4 + cta(10.5), True, 14.5))

# R5 — Tre cose che non fa mai (14s)
nev = [("Non finge di essere<br>una persona.", "Si presenta sempre come<br>assistente virtuale."),
       ("Non dà consigli<br>medici.", "Le urgenze vanno<br>subito allo studio."),
       ("Non dice ciò che<br>Lei non vuole.", "Orari, prezzi, tono:<br>decide Lei.")]
b5 = el(f'<div class="mid d">Tre cose che<br>Celea <span style="color:{TERRA2}">non fa mai.</span></div>', 0.1, 1.9, style="top:620px")
for i, (a, b) in enumerate(nev):
    s, e = 1.9 + i * 2.6, 1.9 + (i + 1) * 2.6
    b5 += el(f'<div class="d" style="font-size:220px;font-weight:800;color:{TERRA2};line-height:1">{i+1}</div>', s, e, "pop", "top:420px")
    b5 += el(f'<div class="mid d">{a}</div>', s + 0.15, e, style="top:720px")
    b5 += el(f'<div class="sub" style="color:{MUTED}">{b}</div>', s + 0.5, e, style="top:960px")
R["r5-non-fa-mai"] = (13.5, False, page(b5 + cta(9.8, dark=False), False, 13.5))

# R6 — Cerchiamo 20 fondatori (13s)
dots = "".join(f'<div style="width:120px;height:120px;border-radius:50%;border:6px solid {TERRA2};opacity:0" data-in="{1.8 + i*0.12}" data-anim="pop"></div>' for i in range(20))
b6 = el(f'<div class="big d">Cerchiamo<br><span style="color:{TERRA2}">20 attività</span><br>con cui partire.</div>', 0.1, 6.6, style="top:420px")
b6 += f'<div class="a" data-in="1.6" data-out="6.6" data-anim="fade" style="top:900px"><div style="display:grid;grid-template-columns:repeat(5,120px);gap:40px;justify-content:center">{dots}</div></div>'
b6 += el(f'<div class="sub" style="color:{MUTED}">Studi dentistici, agenzie immobiliari,<br>B&amp;B e hotel. In tutta Italia.</div>', 4.2, 6.6, style="top:1560px")
b6 += el(f'<div class="mid d">Per i fondatori<br><span style="color:{TERRA2}">l\'attivazione<br>è gratuita.</span></div>', 6.7, 9.6, style="top:620px")
b6 += el(f'<div class="sub" style="color:{MUTED}">Lo configuriamo noi, su misura.</div>', 7.1, 9.6, style="top:1000px")
R["r6-fondatori"] = (13.5, False, page(b6 + cta(9.7, dark=False, line="Scriva <b>FONDATORE</b> nei commenti"), False, 13.5))


def music(path, dur, bpm=122, seed=0):
    """Loop techno minimale originale: cassa, hi-hat, basso, pad. Volume basso, fade in/out."""
    sr = 44100
    n = int(sr * dur)
    t = np.arange(n) / sr
    beat = 60 / bpm
    out = np.zeros(n)
    def add(sig, start):
        i = int(start * sr)
        if i >= n: return
        j = min(n, i + len(sig)); out[i:j] += sig[: j - i]
    kt = np.arange(int(sr * 0.35)) / sr
    kick = np.sin(2 * np.pi * (45 + 110 * np.exp(-kt * 28)) * kt) * np.exp(-kt * 9)
    rng = np.random.default_rng(seed)
    ht = np.arange(int(sr * 0.06)) / sr
    hat = rng.standard_normal(len(ht)) * np.exp(-ht * 70)
    hat = np.diff(hat, prepend=0) * 0.5
    notes = [55.0, 55.0, 65.41, 49.0]
    bt = np.arange(int(sr * beat * 0.45)) / sr
    k = 0
    while k * beat < dur:
        st = k * beat
        add(kick * 0.9, st)
        add(hat * 0.25, st + beat / 2)
        f = notes[(k // 4) % 4]
        bass = np.sign(np.sin(2 * np.pi * f * bt)) * 0.12 * np.exp(-bt * 6)
        add(bass, st + beat / 2)
        k += 1
    pad = (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 277.18 * t) + np.sin(2 * np.pi * 329.63 * t)) * 0.025
    pad *= 0.6 + 0.4 * np.sin(2 * np.pi * t / (beat * 8))
    out += pad
    out = np.convolve(out, np.ones(3) / 3, mode="same")
    fade = np.minimum(1, np.minimum(t / 0.6, (dur - t) / 1.2))
    out *= np.clip(fade, 0, 1)
    out = out / np.max(np.abs(out)) * 0.55
    data = (out * 32767).astype(np.int16)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.tobytes())


only = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H})
    for idx, (name, (dur, dark, htm)) in enumerate(R.items()):
        if only and name not in only:
            continue
        fdir = f"/tmp/claude-0/frames/{name}"
        os.makedirs(fdir, exist_ok=True)
        pg.set_content(htm)
        pg.wait_for_timeout(200)
        nf = int(dur * FPS)
        for i in range(nf):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=f"{fdir}/{i:04d}.jpg", type="jpeg", quality=92)
        wav = f"{fdir}/a.wav"
        music(wav, dur, bpm=120 + idx * 2, seed=idx)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{fdir}/%04d.jpg", "-i", wav,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", f"{OUT}/{name}.mp4"], check=True)
        print("ok", name, nf, "frames", flush=True)
    b.close()
