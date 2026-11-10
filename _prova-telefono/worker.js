/* Celea · Worker «Ti richiama Sofia» (Cloudflare Workers, piano gratuito) · versione 10/11/2026 sera
   Due compiti, con un solo tetto di demo al giorno (decisione di William: 20 al giorno in tutto):
     POST /callback  il visitatore lascia il numero: l'assistente demo del settore lo chiama (Sofia dentisti, Marco
                     immobiliare, Elena strutture ricettive), con la stessa apertura con avviso AI e il nome della Sua attività;
     POST /posto     prima di aprire «Parla ora» dal browser il sito chiede un posto: conta nello stesso tetto giornaliero.
   SPENTO finché William non scrive «accendi richiamata» (nel sito: LIVE.endpoint vuoto e LIVE.richiamata = false).

   Regole: solo numeri italiani (+39); una chiamata per numero al giorno; solo dalle 9 alle 20 (ora italiana);
   chiamata al massimo 3 minuti (agent_override.agent.max_call_duration_ms = 180000); blocco contro invii ripetuti
   (Turnstile + limite per connessione); nessun dato oltre il necessario: nel KV solo impronte (SHA-256 con SALT),
   mai numeri o IP in chiaro, e scadono da sole entro 2 giorni (comunque mai oltre 30). Su Retell gli assistenti demo
   tengono registrazioni e dati della chiamata 1 giorno (data_storage_retention_days = 1).
   ATTENZIONE: i numeri comprati su Retell chiamano solo numeri degli Stati Uniti: FROM_NUMBER deve essere un numero
   italiano importato in Retell (per esempio da Telnyx, collegamento SIP).

   La cartella inizia con «_»: GitHub Pages non la pubblica sul sito.
   Questo file si incolla nell'editor del Worker su dash.cloudflare.com (Guida 3, PDF).

   Impostazioni del Worker (Settings → Variables and Secrets):
     Segreti (Secret):  RETELL_API_KEY · TURNSTILE_SECRET · SALT (una frase lunga inventata)
     Variabili (Text):  FROM_NUMBER (il numero demo, +39…)
                        facoltative: AGENT_DENTISTA · AGENT_IMMOBILIARE · AGENT_RICETTIVO (predefiniti: Sofia, Marco, Elena)
                                     ALLOWED_ORIGINS · MAX_PER_DAY (20) · MAX_PER_IP (3 al giorno) · MAX_PER_TEL (1 al giorno)
                                     HOURS ("9-20", ora italiana)
   Collegamento KV (Settings → Bindings → KV namespace):  nome della variabile  LIMITI
*/

const ok = (body, status, cors) => new Response(JSON.stringify(body), {
  status: status || 200,
  headers: Object.assign({ "Content-Type": "application/json; charset=utf-8" }, cors || {})
});

async function sha(text) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, "0")).join("");
}

// Accetta solo numeri italiani: cellulari (+39 3…) e fissi (+39 0…).
function telIt(v) {
  let t = String(v || "").replace(/[\s.\-\/()]/g, "");
  if (/^0039/.test(t)) t = "+" + t.slice(2);
  else if (/^39\d{9,11}$/.test(t)) t = "+" + t;
  else if (/^[03]\d{5,11}$/.test(t)) t = "+39" + t;
  return /^\+39(3\d{8,9}|0\d{5,10})$/.test(t) ? t : null;
}

// Nome dell'attività (facoltativo): il filtro completo (parole offensive, aziende famose) è nel sito; qui solo la forma.
function nomeAttivita(v) {
  const n = String(v || "").replace(/\s+/g, " ").trim();
  if (!n) return "";
  return n.length >= 2 && n.length <= 40 && /^[\p{L}\p{N} &'’.,\-]+$/u.test(n) && !/https?|www\.|@/i.test(n) ? n : null;
}

function romeHourAndDay() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Rome", hour: "2-digit", hour12: false, year: "numeric", month: "2-digit", day: "2-digit"
  }).formatToParts(new Date());
  const g = k => (parts.find(p => p.type === k) || {}).value;
  return { hour: parseInt(g("hour"), 10) % 24, day: g("year") + "-" + g("month") + "-" + g("day") };
}

async function count(kv, key) { return parseInt((await kv.get(key)) || "0", 10); }
const DUE_GIORNI = 172800; // le impronte scadono da sole (mai oltre 30 giorni)

export default {
  async fetch(req, env) {
    const origins = (env.ALLOWED_ORIGINS || "https://www.celea.it,https://celea.it").split(",").map(s => s.trim());
    const origin = req.headers.get("Origin") || "";
    const cors = origins.includes(origin) ? {
      "Access-Control-Allow-Origin": origin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin"
    } : {};

    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(req.url);
    if (req.method !== "POST" || !["/callback", "/posto"].includes(url.pathname)) return ok({ ok: false, code: "not_found" }, 404, cors);
    if (!cors["Access-Control-Allow-Origin"]) return ok({ ok: false, code: "origin" }, 403);

    let body = {};
    try { body = await req.json(); } catch (e) { return ok({ ok: false, code: "bad_request" }, 400, cors); }

    const kv = env.LIMITI, salt = env.SALT || "celea", now = romeHourAndDay();
    const ip = req.headers.get("CF-Connecting-IP") || "0.0.0.0";
    const kDay = "day:" + now.day, kIp = "ip:" + now.day + ":" + (await sha(salt + ip));
    const maxDay = parseInt(env.MAX_PER_DAY || "20", 10), maxIp = parseInt(env.MAX_PER_IP || "3", 10);

    // Demo dal browser («Parla ora»): solo il posto nel tetto giornaliero comune
    if (url.pathname === "/posto") {
      const [cDay, cIp] = await Promise.all([count(kv, kDay), count(kv, kIp)]);
      if (cDay >= maxDay) return ok({ ok: false, code: "day" }, 200, cors);
      if (cIp >= maxIp) return ok({ ok: false, code: "limit" }, 200, cors);
      await Promise.all([kv.put(kDay, String(cDay + 1), { expirationTtl: DUE_GIORNI }), kv.put(kIp, String(cIp + 1), { expirationTtl: DUE_GIORNI })]);
      return ok({ ok: true }, 200, cors);
    }

    // 1. Dati del modulo «Ti richiama»
    const agents = {
      dentista: env.AGENT_DENTISTA || "agent_d707460b8b0bc2d50382aa3aa9",     // Sofia
      immobiliare: env.AGENT_IMMOBILIARE || "agent_665333f44ade1c0d48ed000a7d", // Marco
      ricettivo: env.AGENT_RICETTIVO || "agent_9f88879b0f2fd82c7a074dd2e6"      // Elena
    };
    const agent = agents[body.niche];
    if (!agent) return ok({ ok: false, code: "niche" }, 400, cors);
    if (body.ok !== true) return ok({ ok: false, code: "consent" }, 400, cors);
    const tel = telIt(body.tel);
    if (!tel) return ok({ ok: false, code: "tel" }, 400, cors);
    const nome = nomeAttivita(body.nome);
    if (nome === null) return ok({ ok: false, code: "nome" }, 400, cors);

    // 2. Orario: solo dalle 9 alle 20
    const [h1, h2] = String(env.HOURS || "9-20").split("-").map(n => parseInt(n, 10));
    if (now.hour < h1 || now.hour >= h2) return ok({ ok: false, code: "hours" }, 200, cors);

    // 3. Anti-bot (Cloudflare Turnstile)
    if (env.TURNSTILE_SECRET) {
      const f = new FormData();
      f.append("secret", env.TURNSTILE_SECRET);
      f.append("response", String(body.token || ""));
      f.append("remoteip", ip);
      const v = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: f });
      const vj = await v.json().catch(() => ({}));
      if (!vj.success) return ok({ ok: false, code: "captcha" }, 200, cors);
    }

    // 4. Limiti: tetto del giorno (comune con «Parla ora»), per connessione, una chiamata per numero al giorno
    const kTel = "tel:" + now.day + ":" + (await sha(salt + tel));
    const [cDay, cIp, cTel] = await Promise.all([count(kv, kDay), count(kv, kIp), count(kv, kTel)]);
    if (cDay >= maxDay) return ok({ ok: false, code: "day" }, 200, cors);
    if (cIp >= maxIp || cTel >= parseInt(env.MAX_PER_TEL || "1", 10)) return ok({ ok: false, code: "limit" }, 200, cors);
    // il posto si prende PRIMA della chiamata: due invii ravvicinati non passano entrambi
    await Promise.all([
      kv.put(kDay, String(cDay + 1), { expirationTtl: DUE_GIORNI }),
      kv.put(kIp, String(cIp + 1), { expirationTtl: DUE_GIORNI }),
      kv.put(kTel, String(cTel + 1), { expirationTtl: DUE_GIORNI })
    ]);

    // 5. Chiamata con Retell: l'assistente demo del settore chiama il visitatore, al massimo 3 minuti
    const r = await fetch("https://api.retellai.com/v2/create-phone-call", {
      method: "POST",
      headers: { "Authorization": "Bearer " + env.RETELL_API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({
        from_number: env.FROM_NUMBER,
        to_number: tel,
        override_agent_id: agent,
        agent_override: { agent: { max_call_duration_ms: 180000 } },
        ...(nome ? { retell_llm_dynamic_variables: { nome_attivita: nome } } : {}),
        metadata: { fonte: "sito-demo-ti-richiama", settore: body.niche, lingua: String(body.lang || "it") }
      })
    });
    if (!r.ok) {
      const txt = await r.text().catch(() => "");
      console.log("Retell error", r.status, txt.slice(0, 300));
      return ok({ ok: false, code: "error" }, 200, cors);
    }
    return ok({ ok: true }, 200, cors);
  }
};
