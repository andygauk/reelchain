// ReelChain analytics ingest — Cloudflare Pages Function.
// Captures client events to KV (binding "RC_ANALYTICS") when bound.
// If KV is NOT yet bound, events still log (visible in Pages → Functions → Logs)
// so the pipeline is live before any dashboard setup.
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "POST, GET, OPTIONS",
      "access-control-allow-headers": "content-type",
    },
  });
}
export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json(400, { ok: false, error: "bad json" }); }
  const ev = body && body.event;
  const props = (body && body.props) || {};
  if (!ev || typeof ev !== "string") return json(400, { ok: false, error: "missing event" });
  const rec = { event: ev, props, ts: props.ts || Date.now() };
  // Always visible in function logs (works even before KV is bound).
  console.log("rc_event " + ev + " " + JSON.stringify(props));
  const kv = env.RC_ANALYTICS;
  if (kv) {
    try {
      const day = new Date().toISOString().slice(0, 10);
      await updateStats(kv, day, rec);
      await pushRecent(kv, day, rec);
    } catch (e) { console.log("rc_kv_err " + e.message); }
  }
  return json(202, { ok: true, kv: !!kv });
}
function json(code, o) {
  return new Response(JSON.stringify(o), {
    status: code,
    headers: { "content-type": "application/json", "access-control-allow-origin": "*" },
  });
}
export async function updateStats(kv, day, rec) {
  const key = "stats:" + day;
  let s = {};
  const raw = await kv.get(key);
  if (raw) { try { s = JSON.parse(raw); } catch (e) {} }
  s.rounds = s.rounds || 0;
  s.roundStart = s.roundStart || 0;
  s.sessions = s.sessions || [];
  s.challengeOpened = s.challengeOpened || 0;
  s.challengeCompleted = s.challengeCompleted || 0;
  s.challengeCreated = s.challengeCreated || 0;
  s.shareCompleted = s.shareCompleted || 0;
  if (rec.event === "round_completed") s.rounds++;
  else if (rec.event === "round_start") s.roundStart++;
  else if (rec.event === "session_start") {
    const id = rec.props.anonId;
    if (id && !s.sessions.includes(id) && s.sessions.length < 8000) s.sessions.push(id);
  } else if (rec.event === "challenge_landed" || rec.event === "challenge_opened") s.challengeOpened++;
  else if (rec.event === "challenge_completed") s.challengeCompleted++;
  else if (rec.event === "challenge_created") s.challengeCreated++;
  else if (rec.event === "share_completed") s.shareCompleted++;
  await kv.put(key, JSON.stringify(s));
}
export async function pushRecent(kv, day, rec) {
  const key = "recent:" + day;
  let arr = [];
  const raw = await kv.get(key);
  if (raw) { try { arr = JSON.parse(raw); } catch (e) {} }
  arr.push(rec);
  if (arr.length > 100) arr = arr.slice(-100);
  await kv.put(key, JSON.stringify(arr));
}
