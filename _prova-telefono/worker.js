/* Celea · Worker «Mi chiami» (Cloudflare Workers, piano gratuito)
   Riceve dal sito il numero del visitatore, controlla i limiti e chiede a Retell di farlo chiamare
   dall'assistente demo del settore scelto (Sofia, Marco o Elena).

   La cartella inizia con «_»: GitHub Pages non la pubblica sul sito.
   Questo file si incolla nell'editor del Worker su dash.cloudflare.com (Guida 3, PDF).

   Impostazioni del Worker (Settings → Variables and Secrets):
     Segreti (Secret):  RETELL_API_KEY · TURNSTILE_SECRET · SALT (una frase lunga inventata)
     Variabili (Text):  FROM_NUMBER (es. +3909...)  · AGENT_DENTISTA · AGENT_IMMOBILIARE · AGENT_RICETTIVO
                        facoltative: ALLOWED_ORIGINS · MAX_PER_IP (2) · MAX_PER_TEL (1) · MAX_PER_DAY (25)
                                     WINDOW_DAYS (30) · HOURS ("8-21", ora italiana)
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

function romeHourAndDay() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Rome", hour: "2-digit", hour12: false, year: "numeric", month: "2-digit", day: "2-digit"
  }).formatToParts(new Date());
  const g = k => (parts.find(p => p.type === k) || {}).value;
  return { hour: parseInt(g("hour"), 10) % 24, day: g("year") + "-" + g("month") + "-" + g("day") };
}

async function count(kv, key) { return parseInt((await kv.get(key)) || "0", 10); }

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
    if (req.method !== "POST" || url.pathname !== "/callback") return ok({ ok: false, code: "not_found" }, 404, cors);
    if (!cors["Access-Control-Allow-Origin"]) return ok({ ok: false, code: "origin" }, 403);

    let body = {};
    try { body = await req.json(); } catch (e) { return ok({ ok: false, code: "bad_request" }, 400, cors); }

    // 1. Dati del modulo
    const agents = { dentista: env.AGENT_DENTISTA, immobiliare: env.AGENT_IMMOBILIARE, ricettivo: env.AGENT_RICETTIVO };
    const agent = agents[body.niche];
    if (!agent) return ok({ ok: false, code: "niche" }, 400, cors);
    if (body.ok !== true) return ok({ ok: false, code: "consent" }, 400, cors);
    const tel = telIt(body.tel);
    if (!tel) return ok({ ok: false, code: "tel" }, 400, cors);

    // 2. Orario: niente chiamate di notte
    const [h1, h2] = String(env.HOURS || "8-21").split("-").map(n => parseInt(n, 10));
    const now = romeHourAndDay();
    if (now.hour < h1 || now.hour >= h2) return ok({ ok: false, code: "hours" }, 200, cors);

    // 3. Anti-bot (Cloudflare Turnstile)
    const ip = req.headers.get("CF-Connecting-IP") || "0.0.0.0";
    if (env.TURNSTILE_SECRET) {
      const f = new FormData();
      f.append("secret", env.TURNSTILE_SECRET);
      f.append("response", String(body.token || ""));
      f.append("remoteip", ip);
      const v = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: f });
      const vj = await v.json().catch(() => ({}));
      if (!vj.success) return ok({ ok: false, code: "captcha" }, 200, cors);
    }

    // 4. Limiti: per connessione, per numero, per giorno (si salvano solo impronte, mai numeri o IP in chiaro)
    const kv = env.LIMITI;
    const salt = env.SALT || "celea";
    const ttl = 86400 * parseInt(env.WINDOW_DAYS || "30", 10);
    const kIp = "ip:" + (await sha(salt + ip)), kTel = "tel:" + (await sha(salt + tel)), kDay = "day:" + now.day;
    const [cIp, cTel, cDay] = await Promise.all([count(kv, kIp), count(kv, kTel), count(kv, kDay)]);
    if (cDay >= parseInt(env.MAX_PER_DAY || "25", 10)) return ok({ ok: false, code: "day" }, 200, cors);
    if (cIp >= parseInt(env.MAX_PER_IP || "2", 10) || cTel >= parseInt(env.MAX_PER_TEL || "1", 10)) return ok({ ok: false, code: "limit" }, 200, cors);

    // 5. Chiamata con Retell: l'assistente demo del settore chiama il visitatore
    const r = await fetch("https://api.retellai.com/v2/create-phone-call", {
      method: "POST",
      headers: { "Authorization": "Bearer " + env.RETELL_API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({
        from_number: env.FROM_NUMBER,
        to_number: tel,
        override_agent_id: agent,
        metadata: { fonte: "sito-demo-mi-chiami", settore: body.niche, lingua: String(body.lang || "it") }
      })
    });
    if (!r.ok) {
      const txt = await r.text().catch(() => "");
      console.log("Retell error", r.status, txt.slice(0, 300));
      return ok({ ok: false, code: "error" }, 200, cors);
    }

    await Promise.all([
      kv.put(kIp, String(cIp + 1), { expirationTtl: ttl }),
      kv.put(kTel, String(cTel + 1), { expirationTtl: ttl }),
      kv.put(kDay, String(cDay + 1), { expirationTtl: 172800 })
    ]);
    return ok({ ok: true }, 200, cors);
  }
};
