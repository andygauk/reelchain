// ReelChain analytics read — Cloudflare Pages Function.
// Returns today's + rolling aggregates from KV (binding "RC_ANALYTICS").
// Falls back to { kv:false } when the binding isn't set, so the live app
// can detect "analytics not yet bound" gracefully.
export async function onRequestGet({ request, env }) {
  const kv = env.RC_ANALYTICS;
  if (!kv) return json(200, { ok: true, kv: false });
  const url = new URL(request.url);
  const days = Math.min(30, Math.max(1, parseInt(url.searchParams.get("days") || "7", 10) || 7));
  const out = { ok: true, kv: true, days, total: empty(), byDay: [] };
  for (let i = days - 1; i >= 0; i--) {
    const d = dayOffset(i);
    const raw = await kv.get("stats:" + d);
    let s = raw ? safe(raw) : null;
    if (s) {
      out.byDay.push({ date: d, rounds: s.rounds || 0, roundStart: s.roundStart || 0,
        activePlayers: (s.sessions || []).length, challengeOpened: s.challengeOpened || 0,
        challengeCompleted: s.challengeCompleted || 0, challengeCreated: s.challengeCreated || 0,
        shareCompleted: s.shareCompleted || 0 });
      out.total.rounds += s.rounds || 0;
      out.total.roundStart += s.roundStart || 0;
      out.total.activePlayers = new Set([...(out.total._seen || []), ...(s.sessions || [])]).size;
      out.total._seen = [...(out.total._seen || []), ...(s.sessions || [])];
      out.total.challengeOpened += s.challengeOpened || 0;
      out.total.challengeCompleted += s.challengeCompleted || 0;
      out.total.challengeCreated += s.challengeCreated || 0;
      out.total.shareCompleted += s.shareCompleted || 0;
    }
  }
  delete out.total._seen;
  return json(200, out);
}
function empty() {
  return { rounds: 0, roundStart: 0, activePlayers: 0, challengeOpened: 0,
    challengeCompleted: 0, challengeCreated: 0, shareCompleted: 0 };
}
function dayOffset(i) {
  const d = new Date(Date.now() + i * 86400000);
  return d.toISOString().slice(0, 10);
}
function safe(raw) { try { return JSON.parse(raw); } catch (e) { return null; } }
function json(code, o) {
  return new Response(JSON.stringify(o), {
    status: code,
    headers: { "content-type": "application/json", "access-control-allow-origin": "*", "cache-control": "no-store" },
  });
}
