#!/usr/bin/env python3
"""Build a self-contained, server-free ReelChain GAME (reelchain_game.html).

Reads data.json (the real film<->cast bipartite graph) and emits a single
HTML file with the graph embedded + an interactive puzzle game. No Flask,
no network, no dependencies -- just open the file in a browser.
"""
import json

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReelChain — Connect Two Films</title>
<style>
  :root{
    --bg:#0d0f17; --panel:#161a26; --panel2:#1e2333; --accent:#ff4d6d; --accent2:#ffb84d;
    --film:#5b8cff; --actor:#ffb84d; --text:#e8eaf2; --muted:#8a90a6; --good:#39d98a; --bad:#ff5470;
  }
  .rc-app *{box-sizing:border-box}
  .rc-app{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       background:radial-gradient(1200px 600px at 50% -10%,#1b2030,#0d0f17);color:var(--text);padding:22px 16px 80px}
  .rc-app h1{font-size:30px;margin:0 0 2px;letter-spacing:.5px}
  .rc-app h1 .rc-c{color:var(--accent)}
  .rc-app .rc-tag{color:var(--muted);font-size:14px;margin-bottom:16px}

  .rc-app .rc-toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
  .rc-app .rc-seg{display:inline-flex;background:var(--panel2);border:1px solid #2b3142;border-radius:10px;overflow:hidden}
  .rc-app .rc-seg button{background:none;border:none;color:var(--muted);padding:9px 13px;font-size:13px;font-weight:600;cursor:pointer}
  .rc-app .rc-seg button.rc-active{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#1a1320}
  .rc-app .rc-btn{cursor:pointer;border:none;border-radius:10px;padding:10px 15px;font-size:14px;font-weight:600;
       background:linear-gradient(135deg,var(--accent),var(--accent2));color:#1a1320;transition:transform .06s}
  .rc-app .rc-btn:active{transform:translateY(1px)}
  .rc-app .rc-btn.ghost{background:var(--panel2);color:var(--text);border:1px solid #2b3142}
  .rc-app .rc-spacer{flex:1}
  .rc-app .rc-modebar{font-size:13px;color:var(--muted);margin:-6px 0 12px;min-height:18px}
  .rc-app .rc-modebar b{color:var(--accent2)}
  .rc-app .rc-modebar .rc-done{color:var(--good);font-weight:600}

  .rc-app .rc-puzzle{display:flex;align-items:stretch;gap:10px;margin-bottom:14px}
  .rc-app .rc-card{flex:1;background:linear-gradient(160deg,#20283e,#141826);border:1px solid #2b3142;border-radius:16px;
        padding:16px;position:relative;min-height:96px;display:flex;flex-direction:column;justify-content:center}
  .rc-app .rc-card .rc-lbl{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
  .rc-app .rc-card .rc-name{font-size:20px;font-weight:700;line-height:1.2}
  .rc-app .rc-card.rc-target{background:linear-gradient(160deg,#3a1f33,#21141f);border-color:#7a3550}
  .rc-app .rc-card .rc-emoji{position:absolute;top:12px;right:14px;font-size:22px;opacity:.6}
  .rc-app .rc-connector{display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);font-size:12px;min-width:64px}
  .rc-app .rc-connector .rc-dot{width:10px;height:10px;border-radius:50%;background:var(--accent);margin:4px 0}
  .rc-app .rc-connector .rc-line{width:2px;flex:1;background:linear-gradient(var(--accent),var(--accent2));min-height:18px}

  .rc-app .rc-panel{background:var(--panel);border:1px solid #232838;border-radius:14px;padding:16px;margin-bottom:14px}
  .rc-app .rc-panel h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted)}

  .rc-app .rc-chips{display:flex;flex-wrap:wrap;gap:8px}
  .rc-app .rc-chip{cursor:pointer;border:none;border-radius:999px;padding:8px 13px;font-size:14px;font-weight:600;
        background:var(--panel2);color:var(--text);border:1px solid #2b3142;transition:.08s}
  .rc-app .rc-chip:hover{border-color:var(--accent);transform:translateY(-1px)}
  .rc-app .rc-chip.rc-actor{background:rgba(255,184,77,.14);color:#ffce8a;border-color:rgba(255,184,77,.4)}
  .rc-app .rc-chip.rc-film{background:rgba(91,140,255,.14);color:#9db8ff;border-color:rgba(91,140,255,.4)}
  .rc-app .rc-chip.rc-dim{opacity:.35;cursor:default}
  .rc-app .rc-chip.rc-dim:hover{transform:none;border-color:#2b3142}
  .rc-app .rc-chip.rc-picked{outline:2px solid var(--accent2)}

  .rc-app .rc-pickhint{font-size:13px;color:var(--muted);margin-bottom:8px}
  .rc-app .rc-pickhint b{color:var(--actor)}

  .rc-app .rc-chain{display:flex;flex-wrap:wrap;align-items:center;gap:7px}
  .rc-app .rc-node{padding:7px 11px;border-radius:999px;font-size:13px;font-weight:600;white-space:nowrap}
  .rc-app .rc-node.rc-film{background:rgba(91,140,255,.15);color:#9db8ff;border:1px solid rgba(91,140,255,.4)}
  .rc-app .rc-node.rc-actor{background:rgba(255,184,77,.15);color:#ffce8a;border:1px solid rgba(255,184,77,.4)}
  .rc-app .rc-node.rc-current{outline:2px solid var(--accent);box-shadow:0 0 0 3px rgba(255,77,109,.25)}
  .rc-app .rc-arrow{color:var(--muted);font-size:15px}

  .rc-app .rc-meta{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin-top:4px}
  .rc-app .rc-meta b{color:var(--accent2)}
  .rc-app .rc-msg{padding:11px 13px;border-radius:10px;font-size:14px;margin-top:10px}
  .rc-app .rc-msg.rc-ok{background:rgba(57,217,138,.12);color:var(--good);border:1px solid rgba(57,217,138,.35)}
  .rc-app .rc-msg.rc-err{background:rgba(255,84,112,.12);color:var(--bad);border:1px solid rgba(255,84,112,.35)}
  .rc-app .rc-msg.rc-info{background:rgba(91,140,255,.1);color:#9db8ff;border:1px solid rgba(91,140,255,.35)}

  .rc-app .rc-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
  .rc-app select{background:var(--panel2);color:var(--text);border:1px solid #2b3142;border-radius:9px;padding:9px 10px;font-size:14px}
  .rc-app label.rc-lbl2{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}

  .rc-app .rc-stats{display:flex;gap:18px;font-size:13px;color:var(--muted)}
  .rc-app .rc-stats b{color:var(--text)}

  .rc-overlay{position:fixed;inset:0;background:rgba(8,10,16,.85);display:none;align-items:center;justify-content:center;z-index:2147483647;
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--text);line-height:1.5}
  .rc-overlay.rc-open{display:flex}
  .rc-modal{background:var(--panel);border:1px solid #2b3142;border-radius:18px;padding:26px;max-width:440px;width:calc(100% - 40px);text-align:center;
         box-shadow:0 30px 80px rgba(0,0,0,.6);color:var(--text);font-family:inherit}
  .rc-modal h2{margin:0 0 6px;font-size:26px;font-family:inherit;font-weight:800;color:var(--text)}
  .rc-modal .rc-big{font-size:46px;margin:6px 0;font-family:inherit;font-weight:800;color:var(--text)}
  .rc-modal .rc-sub{color:var(--muted);font-size:14px;margin-bottom:16px;font-family:inherit}
  .rc-modal .rc-chain{justify-content:center;margin:14px 0}

  /* Unscoped button so the win modal's button is styled even though the
     overlay sits (by design) outside .rc-app. */
  .rc-btn{cursor:pointer;border:none;border-radius:10px;padding:10px 15px;font-size:14px;font-weight:600;
       background:linear-gradient(135deg,var(--accent),var(--accent2));color:#1a1320;transition:transform .06s;font-family:inherit}
  .rc-btn:active{transform:translateY(1px)}
  .rc-btn.ghost{background:var(--panel2);color:var(--text);border:1px solid #2b3142}

  .rc-app .rc-help{font-size:13px;color:var(--muted);line-height:1.6}
  .rc-app .rc-help b{color:var(--text)}
  .rc-app details summary{cursor:pointer;color:var(--accent2);font-size:13px;font-weight:600;margin-bottom:8px}
</style>
</head>
<body>
<div class="rc-app">
  <h1>Reel<span class="rc-c">Chain</span></h1>
  <div class="rc-tag">Two films. One bridge. Connect them through the actors they share.</div>

  <div class="rc-toolbar">
    <div class="rc-seg" id="diff">
      <button data-d="easy" class="rc-active">Easy</button>
      <button data-d="medium">Medium</button>
      <button data-d="hard">Hard</button>
      <button data-d="any">Surprise</button>
    </div>
    <button class="rc-btn" id="newBtn">🎲 New Puzzle</button>
    <button class="rc-btn ghost" id="hintBtn">💡 Hint</button>
    <button class="rc-btn ghost" id="revealBtn">👁 Reveal</button>
    <button class="rc-btn ghost" id="shareBtn">📤 Share</button>
    <button class="rc-btn ghost" id="flipBtn">🔄 Flip</button>
    <span class="rc-spacer"></span>
    <span class="rc-clock" id="clock">00:00</span>
  </div>

  <div class="rc-puzzle">
    <div class="rc-card rc-start">
      <span class="rc-emoji">🎬</span>
      <div class="rc-lbl">Start film</div>
      <div class="rc-name" id="startName">—</div>
    </div>
    <div class="rc-connector">
      <div class="rc-dot"></div><div class="rc-line"></div><div class="rc-dot"></div>
    </div>
    <div class="rc-card rc-target">
      <span class="rc-emoji">🏁</span>
      <div class="rc-lbl">Target film</div>
      <div class="rc-name" id="targetName">—</div>
    </div>
  </div>
  <div class="rc-modebar" id="modeBar"></div>

  <div class="rc-panel">
    <h3>You are at</h3>
    <div class="rc-chain" id="pathChain"></div>
    <div class="rc-meta">
      <span>Steps taken: <b id="stepsTaken">0</b></span>
      <span>Best possible: <b id="optimal">?</b></span>
      <span>Optimal from here: <b id="optRemaining">?</b></span>
    </div>
    <div id="msg"></div>
  </div>

  <div class="rc-panel">
    <div class="rc-pickhint" id="pickHint">Pick an actor who links <b id="curName">this film</b> to another:</div>
    <div class="rc-chips" id="castChips"></div>
    <div id="actorPanel" style="display:none;margin-top:14px">
      <div class="rc-pickhint" id="filmHint"></div>
      <div class="rc-chips" id="filmChips"></div>
    </div>
  </div>

  <div class="rc-row">
    <button class="rc-btn ghost" id="undoBtn">↩ Undo</button>
    <button class="rc-btn ghost" id="resetBtn">⟲ Reset</button>
    <span class="rc-spacer"></span>
    <div class="rc-stats">
      <span>Won: <b id="statWon">0</b></span>
      <span>Best time: <b id="statBest">—</b></span>
    </div>
  </div>

  <div class="rc-panel" style="margin-top:14px">
    <details>
      <summary>How to play / Custom pair</summary>
      <div class="rc-help">
        <p><b>Goal:</b> get from the <b>start film</b> to the <b>target film</b> using the smallest number of actor links.</p>
        <p><b>Each link:</b> pick an actor who is in your <i>current</i> film, then pick one of the other films that actor is in. That film becomes your new position. Keep going until you land on the target.</p>
        <p><b>Example:</b> The Godfather → <i>Al Pacino</i> → Once Upon a Time in Hollywood → <i>Tim Roth</i> → Pulp Fiction. (2 links.)</p>
        <p>Two films with no shared actor still connect through a chain of linked performers — that's the puzzle.</p>
        <div class="rc-row" style="margin-top:14px">
          <span class="rc-lbl2">Custom pair:</span>
          <select id="customA"></select>
          <span style="color:var(--muted)">→</span>
          <select id="customB"></select>
          <button class="rc-btn" id="customGo">Play</button>
        </div>
      </div>
    </details>
  </div>

  <div class="rc-overlay" id="overlay">
    <div class="rc-modal">
      <h2 id="winTitle">Connected! 🎉</h2>
      <div class="rc-big" id="winSteps">0</div>
      <div class="rc-sub" id="winSub"></div>
    <div class="rc-chain" id="winChain"></div>
    <div class="rc-row" style="justify-content:center;margin-top:6px">
      <button class="rc-btn" id="winNext">🎲 Next puzzle</button>
    </div>
  </div>
  </div>
</div>

<script>
const GRAPH = __GRAPH__;
const FILMS = GRAPH.films;
const ACTORS = {};
for (const f in FILMS) for (const a of FILMS[f]) (ACTORS[a] = ACTORS[a] || []).push(f);

const $ = id => document.getElementById(id);
const filmKeys = Object.keys(FILMS);
const rand = arr => arr[Math.floor(Math.random() * arr.length)];

// ---------- BFS solver ----------
function bfs(start, target) {
  if (start === target) return { steps: 0, chain: [{ type: "film", name: start }] };
  const q = [[start, [start], []]];
  const seen = new Set([start]);
  while (q.length) {
    const [cur, pf, pa] = q.shift();
    for (const a of (FILMS[cur] || [])) {
      for (const nxt of (ACTORS[a] || [])) {
        if (seen.has(nxt)) continue;
        const npf = pf.concat(nxt), npa = pa.concat(a);
        if (nxt === target) {
          const chain = [];
          for (let i = 0; i < npf.length; i++) {
            chain.push({ type: "film", name: npf[i] });
            if (i < npa.length) chain.push({ type: "actor", name: npa[i] });
          }
          return { steps: npa.length, chain };
        }
        seen.add(nxt);
        q.push([nxt, npf, npa]);
      }
    }
  }
  return null;
}

// ---------- State ----------
let state = null;
let difficulty = "easy";
let timer = null, startTs = 0, elapsed = 0;

function newPuzzle(a, b) {
  if (!a || !b) {
    const r = pickPair(difficulty);
    a = r[0]; b = r[1];
  }
  const opt = bfs(a, b);
  state = {
    start: a, target: b,
    current: a,
    pathFilms: [a], pathActors: [],
    optimal: opt ? opt.steps : null,
    selectedActor: null,
  };
  $("startName").textContent = a;
  $("targetName").textContent = b;
  $("msg").innerHTML = "";
  hideActorPanel();
  render();
  startTimer();
}

function pickPair(band) {
  let best = null;
  for (let i = 0; i < 4000; i++) {
    const a = rand(filmKeys), b = rand(filmKeys);
    if (a === b) continue;
    const r = bfs(a, b);
    if (!r) continue;
    const s = r.steps;
    let ok = false;
    if (band === "easy") ok = (s === 2);
    else if (band === "medium") ok = (s >= 3 && s <= 4);
    else if (band === "hard") ok = (s >= 5);
    else ok = true;
    if (ok) return [a, b];
    if (!best) best = [a, b];
  }
  return best || [filmKeys[0], filmKeys[1]];
}

// ---------- Rendering ----------
function render() {
  // path chain
  const pc = $("pathChain"); pc.innerHTML = "";
  const total = state.pathFilms.length + state.pathActors.length;
  let idx = 0;
  for (let i = 0; i < state.pathFilms.length; i++) {
    const f = state.pathFilms[i];
    const node = mkNode("film", f);
    if (f === state.current) node.classList.add("rc-current");
    pc.appendChild(node);
    if (i < state.pathActors.length) {
      pc.appendChild(mkNode("actor", state.pathActors[i]));
      pc.appendChild(arrow());
    }
    idx++;
  }
  // cast of current film
  $("curName").textContent = state.current;
  const cast = $("castChips"); cast.innerHTML = "";
  const prevFilm = state.pathFilms[state.pathFilms.length - 2];
  for (const a of (FILMS[state.current] || [])) {
    const c = mkChip("actor", a);
    if (state.selectedActor === a) c.classList.add("rc-picked");
    c.onclick = () => chooseActor(a);
    cast.appendChild(c);
  }
  // meta
  $("stepsTaken").textContent = state.pathActors.length;
  $("optimal").textContent = state.optimal == null ? "—" : state.optimal;
  const rem = bfs(state.current, state.target);
  $("optRemaining").textContent = rem ? rem.steps : "—";
  updateModeBar();
}

function updateModeBar() {
  const bar = $("modeBar");
  if (!bar) return;
  bar.innerHTML = "∞ Endless mode — keep solving for a new puzzle each round.";
}

function mkNode(type, name) {
  const d = document.createElement("span");
  d.className = "rc-node " + type;
  d.textContent = (type === "film" ? "🎬 " : "👤 ") + name;
  return d;
}
function mkChip(kind, name) {
  const b = document.createElement("button");
  b.className = "rc-chip " + kind;
  b.textContent = (kind === "actor" ? "👤 " : "🎬 ") + name;
  return b;
}
function arrow() { const s = document.createElement("span"); s.className = "rc-arrow"; s.textContent = "→"; return s; }

function chooseActor(a) {
  state.selectedActor = a;
  const films = (ACTORS[a] || []).filter(f => f !== state.current);
  const panel = $("actorPanel");
  if (films.length === 0) {
    setMsg("err", a + " only appears in " + state.current + " in this dataset — dead end. Pick another actor.");
    hideActorPanel();
    render();
    return;
  }
  $("filmHint").innerHTML = "<b>" + a + "</b> also stars in — pick where to go next:";
  const fc = $("filmChips"); fc.innerHTML = "";
  const prevFilm = state.pathFilms[state.pathFilms.length - 2];
  for (const f of films) {
    const c = mkChip("film", f);
    if (f === prevFilm) { c.classList.add("rc-dim"); }
    c.onclick = () => chooseFilm(f);
    fc.appendChild(c);
  }
  panel.style.display = "block";
  setMsg("", "");
  render();
}

function chooseFilm(f) {
  if (f === state.target) {
    state.pathActors.push(state.selectedActor);
    state.pathFilms.push(f);
    win();
    return;
  }
  state.pathActors.push(state.selectedActor);
  state.pathFilms.push(f);
  state.current = f;
  state.selectedActor = null;
  hideActorPanel();
  render();
}

function hideActorPanel() { $("actorPanel").style.display = "none"; state && (state.selectedActor = null); }

function undo() {
  if (state.pathActors.length === 0) return;
  state.pathActors.pop();
  state.pathFilms.pop();
  state.current = state.pathFilms[state.pathFilms.length - 1];
  state.selectedActor = null;
  hideActorPanel();
  setMsg("", "");
  render();
}

function reset() { newPuzzle(state.start, state.target); }

function setMsg(kind, txt) {
  const m = $("msg");
  m.className = "rc-msg " + kind;
  m.textContent = txt || "";
}

// ---------- Hint / Reveal ----------
function hint() {
  const r = bfs(state.current, state.target);
  if (!r) { setMsg("err", "No path from here — try Undo."); return; }
  // find first actor on optimal path from current
  const chain = r.chain;
  // chain: film, actor, film, ... starting at current
  let actor = null, film = null;
  for (let i = 0; i < chain.length; i++) {
    if (chain[i].type === "actor") { actor = chain[i].name; film = chain[i + 1].name; break; }
  }
  if (actor && film) {
    setMsg("info", "💡 Try: " + actor + " → " + film);
    // also pre-select that actor to help
    chooseActor(actor);
  }
}

function reveal() {
  const r = bfs(state.start, state.target);
  if (!r) { setMsg("err", "These two films aren't connected in the dataset."); return; }
  const txt = r.chain.map(n => n.name).join("  →  ");
  setMsg("info", "Shortest link (" + r.steps + "): " + txt);
}

// ---------- Win ----------
function win() {
  stopTimer();
  const steps = state.pathActors.length;
  const optimal = state.optimal || steps;
  const perfect = (steps === optimal);
  $("winTitle").textContent = perfect ? "Perfect! 🎯" : "Connected! 🎉";
  $("winSteps").textContent = steps + (steps === 1 ? " link" : " links");
  let sub = perfect ? "Fewest possible — nicely done."
                    : ("Best possible was " + optimal + ". " + (steps - optimal) + " extra.");
  if (elapsed) sub += "  ⏱ " + fmt(elapsed);
  $("winSub").textContent = sub;
  const wc = $("winChain"); wc.innerHTML = "";
  state.pathFilms.forEach((f, i) => {
    wc.appendChild(mkNode("film", f));
    if (i < state.pathActors.length) {
      wc.appendChild(arrow());
      wc.appendChild(mkNode("actor", state.pathActors[i]));
      wc.appendChild(arrow());
    }
  });
  // stats
  let won = +(localStorage.getItem("rc_won") || 0) + 1;
  localStorage.setItem("rc_won", won);
  let best = +(localStorage.getItem("rc_best") || 0);
  if (!best || elapsed < best) { best = elapsed; localStorage.setItem("rc_best", best); }
  refreshStats();
  updateModeBar();
  $("overlay").classList.add("rc-open");
}

function refreshStats() {
  $("statWon").textContent = localStorage.getItem("rc_won") || 0;
  const b = +(localStorage.getItem("rc_best") || 0);
  $("statBest").textContent = b ? fmt(b) : "—";
}

// ---------- Timer ----------
function fmt(ms) {
  const s = Math.floor(ms / 1000);
  return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
}
function startTimer() {
  stopTimer();
  startTs = Date.now(); elapsed = 0;
  $("clock").textContent = "00:00";
  timer = setInterval(() => {
    elapsed = Date.now() - startTs;
    $("clock").textContent = fmt(elapsed);
  }, 250);
}
function stopTimer() { if (timer) { clearInterval(timer); timer = null; } elapsed = Date.now() - startTs; }

// ---------- Custom pair ----------
function fillCustom() {
  const a = $("customA"), b = $("customB");
  a.innerHTML = ""; b.innerHTML = "";
  filmKeys.forEach(f => {
    a.appendChild(new Option(f, f));
    b.appendChild(new Option(f, f));
  });
  if (filmKeys.length > 1) b.selectedIndex = 1;
}

// ---------- Wire up ----------
document.querySelectorAll("#diff button").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll("#diff button").forEach(x => x.classList.remove("rc-active"));
    btn.classList.add("rc-active");
    difficulty = btn.dataset.d;
    newPuzzle();
  };
});
$("newBtn").onclick = () => newPuzzle();
$("hintBtn").onclick = hint;
$("revealBtn").onclick = reveal;
$("shareBtn").onclick = shareCard;
$("flipBtn").onclick = () => { if (state) newPuzzle(state.target, state.start); };
$("undoBtn").onclick = undo;
$("resetBtn").onclick = reset;
$("winNext").onclick = () => { $("overlay").classList.remove("rc-open"); newPuzzle(); };
$("customGo").onclick = () => {
  const a = $("customA").value, b = $("customB").value;
  if (a === b) { setMsg("err", "Pick two different films."); return; }
  $("overlay").classList.remove("rc-open");
  newPuzzle(a, b);
};

// ---------- Share card (client-side canvas, no server) ----------
function buildShareCard() {
  if (!state) return null;
  const steps = state.pathActors.length;
  const optimal = state.optimal || steps;
  const perfect = (steps === optimal);
  const chain = [];
  state.pathFilms.forEach((f, i) => { chain.push({ type: "film", name: f });
    if (i < state.pathActors.length) chain.push({ type: "actor", name: state.pathActors[i] }); });
  const W = 600;
  const nodeH = 40, padTop = 92, gap = 10, padX = 28;
  // wrap rows
  const ctx0 = document.createElement("canvas").getContext("2d");
  ctx0.font = "600 15px -apple-system, Arial, sans-serif";
  let rows = [], x = padX, y = padTop, cur = [];
  chain.forEach(n => {
    const label = (n.type === "film" ? "🎬 " : "👤 ") + n.name;
    const w = ctx0.measureText(label).width + 26;
    if (x + w > W - padX) { rows.push(cur); cur = []; x = padX; y += nodeH + gap; }
    cur.push({ ...n, w, label }); x += w + 10;
  });
  if (cur.length) { rows.push(cur); y += nodeH + gap; }
  const H = y + 64;
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  const x2 = c.getContext("2d");
  x2.fillStyle = "#0d0f17"; x2.fillRect(0, 0, W, H);
  // header
  x2.fillStyle = "#ff4d6d"; x2.font = "800 30px -apple-system, Arial, sans-serif";
  x2.fillText("ReelChain", 24, 44);
  x2.fillStyle = "#8a90a6"; x2.font = "15px -apple-system, Arial, sans-serif";
  const dateLabel = "Puzzle";
  x2.fillText(dateLabel, 24, 68);
  // verdict
  x2.fillStyle = "#ffb84d";
  x2.fillText(perfect ? "PERFECT — matched the optimal link!" : (steps - optimal) + " over optimal", 24, 88);
  // nodes
  let yy = padTop;
  const drawRounded = (rx, ry, rw, rh, r, stroke, fill) => {
    x2.beginPath(); x2.moveTo(rx + r, ry);
    x2.arcTo(rx + rw, ry, rx + rw, ry + rh, r); x2.arcTo(rx + rw, ry + rh, rx, ry + rh, r);
    x2.arcTo(rx, ry + rh, rx, ry, r); x2.arcTo(rx, ry, rx + rw, ry, r); x2.closePath();
    x2.fillStyle = fill; x2.fill(); x2.strokeStyle = stroke; x2.lineWidth = 2; x2.stroke();
  };
  rows.forEach(row => {
    let xx = padX;
    row.forEach(n => {
      const col = n.type === "film" ? "#5b8cff" : "#ffb84d";
      drawRounded(xx, yy, n.w, nodeH, 14, col, "#1b2333");
      x2.fillStyle = col; x2.font = "600 15px -apple-system, Arial, sans-serif";
      x2.fillText(n.label, xx + 13, yy + 25);
      xx += n.w + 10;
    });
    yy += nodeH + gap;
  });
  // footer
  x2.fillStyle = "#8a90a6"; x2.font = "13px -apple-system, Arial, sans-serif";
  x2.fillText("Connect two films through the actors they share", 24, H - 30);
  x2.fillText("reelchain.app", 24, H - 14);
  return c.toDataURL("image/png");
}

async function shareCard() {
  const dataUrl = buildShareCard();
  if (!dataUrl) { alert("Solve a puzzle first, then share!"); return; }
  const blob = await (await fetch(dataUrl)).blob();
  const file = new File([blob], "reelchain_card.png", { type: "image/png" });
  try {
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({ files: [file], title: "ReelChain", text: "I solved a ReelChain puzzle!" });
      return;
    }
  } catch (e) { /* user cancelled */ }
  const a = document.createElement("a");
  a.href = dataUrl; a.download = "reelchain_card.png"; a.click();
}

// ---------- Boot ----------
fillCustom();
refreshStats();
newPuzzle();
</script>
</body>
</html>
"""

import os
import re as _re

PHP_TEMPLATE = r'''<?php
/**
 * Plugin Name: ReelChain
 * Description: Embed the ReelChain film-to-film actor-bridge puzzle game via the [reelchain] shortcode (or the reelchain_game() template tag).
 * Version: 1.0.0
 * Author: ReelChain
 */

if ( ! defined( 'ABSPATH' ) ) exit;

// Enqueue the game's CSS + JS (external files -> never touched by WP filters).
function reelchain_enqueue_assets() {
    $css = plugins_url( 'assets/reelchain.css', __FILE__ );
    $js  = plugins_url( 'assets/reelchain.js',  __FILE__ );
    wp_enqueue_style(  'reelchain', $css, array(), '1.0.0' );
    wp_enqueue_script( 'reelchain', $js,  array(), '1.0.0', true );
}

// Only load the assets on pages that actually use the shortcode.
function reelchain_maybe_enqueue() {
    if ( is_singular() && has_shortcode( get_post()->post_content, 'reelchain' ) ) {
        reelchain_enqueue_assets();
    }
}
add_action( 'wp_enqueue_scripts', 'reelchain_maybe_enqueue' );

// Shortcode: [reelchain]  -> paste into a page in the block editor.
function reelchain_shortcode() {
    $file = __DIR__ . '/assets/reelchain-markup.html';
    if ( ! file_exists( $file ) ) {
        return '<!-- ReelChain: game markup not found. Re-run build_game.py. -->';
    }
    return file_get_contents( $file );
}
add_shortcode( 'reelchain', 'reelchain_shortcode' );

// Template tag: call reelchain_game() directly in a theme template
// (e.g. inside page-reelchain.php).
function reelchain_game() {
    reelchain_enqueue_assets();
    $file = __DIR__ . '/assets/reelchain-markup.html';
    if ( file_exists( $file ) ) {
        echo file_get_contents( $file );
    }
}
'''

def main():
    with open("data.json", encoding="utf-8") as fh:
        data = json.load(fh)
    graph_js = json.dumps({"films": data["films"], "actors": data.get("actors", {})},
                          ensure_ascii=False)
    # Safe for embedding inside <script>: break any </script> sequence.
    graph_js = graph_js.replace("</", "<\\/")
    html = TEMPLATE.replace("__GRAPH__", graph_js)

    # --- Standalone file: open directly / local server / iframe / Cloudflare Pages ---
    out = "reelchain_game.html"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("Wrote %s (%d films, %d actors)" %
          (out, len(data["films"]), len(data.get("actors", {}))))

    # --- Copy into deploy/ so the static host (Cloudflare Pages) serves the latest ---
    import shutil
    deploy_dir = "deploy"
    os.makedirs(deploy_dir, exist_ok=True)
    shutil.copyfile(out, os.path.join(deploy_dir, "index.html"))
    print("Copied to %s/index.html for deployment" % deploy_dir)

    # --- Split into scoped pieces for the WordPress plugin ---
    m_style = _re.search(r"<style>(.*?)</style>", html, _re.S)
    m_body = _re.search(r"<body>(.*?)</body>", html, _re.S)
    if not (m_style and m_body):
        print("WARN: could not split template for plugin build")
        return

    style_full = m_style.group(1)
    body_full = m_body.group(1)
    m_script = _re.search(r"<script>(.*?)</script>", body_full, _re.S)
    if not m_script:
        print("WARN: no <script> found for plugin build")
        return
    js = m_script.group(1)
    markup = (body_full[:m_script.start()] + body_full[m_script.end()]).strip()

    # The game CSS/classes are already namespaced to `.rc-app` / `.rc-*`,
    # so it can't collide with (or be clobbered by) the host theme.
    # No further scoping needed.
    css = style_full

    plugin_dir = "reelchain"
    assets_dir = os.path.join(plugin_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    with open(os.path.join(assets_dir, "reelchain.css"), "w", encoding="utf-8") as fh:
        fh.write(css)
    with open(os.path.join(assets_dir, "reelchain.js"), "w", encoding="utf-8") as fh:
        fh.write(js)
    with open(os.path.join(assets_dir, "reelchain-markup.html"), "w", encoding="utf-8") as fh:
        fh.write(markup + "\n")
    with open(os.path.join(plugin_dir, "reelchain.php"), "w", encoding="utf-8") as fh:
        fh.write(PHP_TEMPLATE)
    print("Wrote plugin/  (reelchain/reelchain.php + assets/)")

    # --- WordPress fragment: paste into a "Custom HTML" block (alt method) ---
    embed = ("<style>" + css + "</style>\n" + markup + "\n")
    with open("reelchain_embed.html", "w", encoding="utf-8") as fh:
        fh.write(embed)
    print("Wrote reelchain_embed.html (Custom-HTML-block alt method)")


if __name__ == "__main__":
    main()
