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

  /* ---- Run HUD (the "one more round" driver) ---- */
  .rc-app .rc-hud{display:flex;gap:10px;flex-wrap:wrap;align-items:stretch;margin:-4px 0 14px}
  .rc-app .rc-stat{flex:1;min-width:78px;background:linear-gradient(160deg,#1a2032,#12151f);border:1px solid #2b3142;border-radius:12px;padding:9px 11px}
  .rc-app .rc-stat .rc-k{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--muted)}
  .rc-app .rc-stat .rc-v{font-size:22px;font-weight:800;line-height:1.1;color:var(--text)}
  .rc-app .rc-stat.rc-combo{border-color:rgba(255,184,77,.4)}
  .rc-app .rc-stat.rc-combo .rc-v{color:var(--accent2)}
  .rc-app .rc-stat.rc-hot{border-color:var(--accent);box-shadow:0 0 0 2px rgba(255,77,109,.25);animation:rcpulse 1.2s ease-in-out infinite}
  @keyframes rcpulse{0%,100%{box-shadow:0 0 0 2px rgba(255,77,109,.15)}50%{box-shadow:0 0 0 4px rgba(255,77,109,.45)}}
  .rc-app .rc-stat .rc-pb{font-size:10px;color:var(--muted);margin-top:1px}
  .rc-app .rc-stat .rc-pb b{color:var(--good)}

  /* ---- Live genome ---- */
  .rc-app .rc-genome{background:linear-gradient(160deg,#141826,#0e111b);border:1px solid #232838;border-radius:14px;padding:12px 14px;margin-bottom:14px;overflow:hidden}
  .rc-app .rc-genome .rc-gh{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
  .rc-app .rc-genome .rc-gh h3{margin:0;font-size:12px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted)}
  .rc-app .rc-genome .rc-gh .rc-rarity{font-size:12px;font-weight:700;color:var(--accent2)}
  .rc-app .rc-genome .rc-svgwrap{overflow-x:auto;overflow-y:hidden}
  .rc-app .rc-genome svg{display:block;height:92px}
  .rc-app .rc-genome .rc-empty{color:var(--muted);font-size:13px;padding:26px 0;text-align:center}

  /* ---- Preview-before-share modal ---- */
  .rc-preview{position:fixed;inset:0;background:rgba(8,10,16,.9);display:none;align-items:center;justify-content:center;z-index:2147483647;padding:20px;
        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  .rc-preview.rc-open{display:flex}
  .rc-preview .rc-pv-box{background:var(--panel);border:1px solid #2b3142;border-radius:18px;padding:18px;max-width:520px;width:100%;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.6)}
  .rc-preview .rc-pv-box h2{margin:0 0 4px;font-size:20px;font-weight:800;color:var(--text)}
  .rc-preview .rc-pv-box .rc-pv-sub{color:var(--muted);font-size:13px;margin-bottom:12px}
  .rc-preview .rc-pv-box img{width:100%;border-radius:12px;border:1px solid #2b3142;margin-bottom:14px}
  .rc-preview .rc-pv-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
</style>
</head>
<body>
<div class="rc-app">
  <h1>Reel<span class="rc-c">Chain</span></h1>
  <div class="rc-tag">Just one more round. Connect two films, grow your genome.</div>

  <div class="rc-hud" id="hud">
    <div class="rc-stat rc-round"><div class="rc-k">Round</div><div class="rc-v" id="hudRound">0</div><div class="rc-pb">best run <b id="hudPBRun">0</b></div></div>
    <div class="rc-stat rc-combo" id="hudComboBox"><div class="rc-k">Combo</div><div class="rc-v" id="hudCombo">1.0×</div><div class="rc-pb" id="hudStreakLbl">warm up</div></div>
    <div class="rc-stat rc-dna"><div class="rc-k">DNA</div><div class="rc-v" id="hudDNA">0</div><div class="rc-pb">best <b id="hudPBDNA">0</b></div></div>
  </div>

  <div class="rc-toolbar">
    <div class="rc-seg" id="diff">
      <button data-d="easy" class="rc-active">Easy</button>
      <button data-d="medium">Medium</button>
      <button data-d="hard">Hard</button>
      <button data-d="any">Surprise</button>
    </div>
    <button class="rc-btn ghost" id="hintBtn">💡 Hint</button>
    <button class="rc-btn ghost" id="shareBtn">🧬 Share genome</button>
    <button class="rc-btn ghost" id="endBtn">■ End run</button>
    <span class="rc-spacer"></span>
    <span class="rc-clock" id="clock">00:00</span>
  </div>

  <div class="rc-genome" id="genome">
    <div class="rc-gh"><h3>Run genome</h3><span class="rc-rarity" id="rarity"></span></div>
    <div class="rc-svgwrap"><div class="rc-empty" id="genomeEmpty">Solve a round to grow your first strand.</div><svg id="genomeSvg" xmlns="http://www.w3.org/2000/svg"></svg></div>
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
    <button class="rc-btn ghost" id="revealBtn">👁 Reveal</button>
    <button class="rc-btn ghost" id="flipBtn">🔄 Flip</button>
    <span class="rc-spacer"></span>
    <div class="rc-stats">
      <span>Runs: <b id="statWon">0</b></span>
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
      <h2 id="winTitle">Round solved! 🎉</h2>
      <div class="rc-big" id="winSteps">0</div>
      <div class="rc-sub" id="winSub"></div>
    <div class="rc-chain" id="winChain"></div>
    <div class="rc-row" style="justify-content:center;margin-top:10px">
      <button class="rc-btn" id="winNext">▶ One more round</button>
      <button class="rc-btn ghost" id="winShare">🧬 Share genome</button>
    </div>
    <div class="rc-sub" id="winEndHint" style="margin-top:12px;margin-bottom:0">Stop now and you lock in your genome — but the combo resets.</div>
  </div>
  </div>

  <div class="rc-overlay" id="endOverlay">
    <div class="rc-modal">
      <h2 id="endTitle">Run ended 🧬</h2>
      <div class="rc-big" id="endBig">0</div>
      <div class="rc-sub" id="endSub"></div>
      <div class="rc-chain" id="endGenome" style="justify-content:center;margin:10px 0"></div>
      <div class="rc-row" style="justify-content:center;margin-top:8px">
        <button class="rc-btn" id="endNewRun">▶ Start a new run</button>
        <button class="rc-btn ghost" id="endShare">🧬 Share genome</button>
      </div>
    </div>
  </div>

  <div class="rc-preview" id="preview">
    <div class="rc-pv-box">
      <h2>Your run genome</h2>
      <div class="rc-pv-sub">Preview before you share — nothing leaves your device until you tap Share.</div>
      <img id="pvImg" alt="ReelChain genome card">
      <div class="rc-pv-row">
        <button class="rc-btn" id="pvShare">📤 Share</button>
        <button class="rc-btn ghost" id="pvDownload">⬇ Download</button>
        <button class="rc-btn ghost" id="pvClose">Close</button>
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

// ---------- Run (the "one more round" spine) ----------
// A run is a session of back-to-back rounds. Each solved round adds a "strand"
// to a live genome and feeds a combo multiplier. Ending the run locks the genome
// in and resets the combo — that felt loss is what drives "just one more round".
let run = null;

function newRun() {
  run = { rounds: 0, dna: 0, combo: 1, streak: 0, best: 0, strands: [] };
  renderGenome();
  updateHUD();
}

// deterministic per-strand signature so the genome is legible ("that's how I played")
function makeStrand(steps, optimal, secs) {
  const over = Math.max(0, steps - optimal);
  const perfect = over === 0;
  const fast = secs > 0 && secs < 20;
  // hue derived from the round shape; perfect rounds skew warm/gold, sloppy skew cool
  const hue = perfect ? 42 : (over === 1 ? 12 : 205 + Math.min(over, 4) * 12);
  return {
    steps, optimal, over, perfect, fast, secs,
    hue,
    sat: perfect ? 85 : 60,
    amp: 10 + Math.min(steps, 8) * 3,       // taller wave = longer chain
    speed: fast ? 1.6 : 1,
  };
}

// combo grows with consecutive perfect rounds, decays a touch on sloppy ones
function applyRoundToRun(strand) {
  run.rounds += 1;
  if (strand.perfect) { run.streak += 1; run.combo = Math.min(5, +(run.combo + 0.5).toFixed(1)); }
  else { run.streak = 0; run.combo = Math.max(1, +(run.combo - 0.5).toFixed(1)); }
  // DNA points: base for solving + efficiency + speed, all times combo
  let base = 10 + Math.max(0, 6 - strand.over) * 3 + (strand.fast ? 6 : 0);
  const gain = Math.round(base * run.combo);
  run.dna += gain;
  strand.gain = gain;
  run.strands.push(strand);
  // personal bests
  const pbRun = +(localStorage.getItem("rc_pb_run") || 0);
  const pbDNA = +(localStorage.getItem("rc_pb_dna") || 0);
  if (run.rounds > pbRun) localStorage.setItem("rc_pb_run", run.rounds);
  if (run.dna > pbDNA) localStorage.setItem("rc_pb_dna", run.dna);
  return gain;
}

function rarityLabel() {
  const n = run.rounds;
  if (n >= 20) return "🧬 LEGENDARY GENOME";
  if (n >= 12) return "🧬 Rare genome";
  if (n >= 7) return "🧬 Uncommon genome";
  if (n >= 3) return "🧬 Common genome";
  return n > 0 ? "🧬 Nascent" : "";
}

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
  if (run && run.rounds > 0) {
    bar.innerHTML = "∞ Endless run — round <b>" + (run.rounds + 1) + "</b>. Keep the combo alive.";
  } else {
    bar.innerHTML = "∞ Endless run — solve rounds back to back to grow your genome.";
  }
}

function updateHUD() {
  if (!run) return;
  $("hudRound").textContent = run.rounds;
  $("hudCombo").textContent = run.combo.toFixed(1) + "×";
  $("hudDNA").textContent = run.dna;
  $("hudPBRun").textContent = localStorage.getItem("rc_pb_run") || 0;
  $("hudPBDNA").textContent = localStorage.getItem("rc_pb_dna") || 0;
  const box = $("hudComboBox");
  if (run.streak >= 3) { box.classList.add("rc-hot"); $("hudStreakLbl").innerHTML = "🔥 " + run.streak + " perfect"; }
  else { box.classList.remove("rc-hot"); $("hudStreakLbl").textContent = run.streak > 0 ? run.streak + " streak" : "warm up"; }
}

// Draws the live genome as a double-helix of strands; grows each round.
function renderGenome() {
  const svg = $("genomeSvg"), empty = $("genomeEmpty"), rar = $("rarity");
  if (!run || run.strands.length === 0) {
    svg.innerHTML = ""; svg.removeAttribute("width");
    empty.style.display = "block"; rar.textContent = "";
    return;
  }
  empty.style.display = "none";
  rar.textContent = rarityLabel();
  const step = 30, padX = 16, H = 92, midY = H / 2;
  const W = padX * 2 + run.strands.length * step;
  svg.setAttribute("width", W);
  svg.setAttribute("viewBox", "0 0 " + W + " " + H);
  const NS = "http://www.w3.org/2000/svg";
  let parts = "";
  // backbone (two sine strands)
  const pts = (phase) => {
    let d = "";
    for (let i = 0; i <= run.strands.length; i++) {
      const s = run.strands[Math.min(i, run.strands.length - 1)];
      const x = padX + i * step;
      const y = midY + Math.sin(i * 0.9 + phase) * (s ? s.amp : 12);
      d += (i === 0 ? "M" : "L") + x.toFixed(1) + "," + y.toFixed(1) + " ";
    }
    return d;
  };
  parts += '<path d="' + pts(0) + '" fill="none" stroke="#3a4160" stroke-width="2" opacity="0.5"/>';
  parts += '<path d="' + pts(Math.PI) + '" fill="none" stroke="#3a4160" stroke-width="2" opacity="0.5"/>';
  // rungs + nodes per strand
  run.strands.forEach((s, i) => {
    const x = padX + i * step;
    const y1 = midY + Math.sin(i * 0.9) * s.amp;
    const y2 = midY + Math.sin(i * 0.9 + Math.PI) * s.amp;
    const col = "hsl(" + s.hue + "," + s.sat + "%,60%)";
    parts += '<line x1="' + x + '" y1="' + y1.toFixed(1) + '" x2="' + x + '" y2="' + y2.toFixed(1) + '" stroke="' + col + '" stroke-width="2" opacity="0.7"/>';
    const r = s.perfect ? 6 : 4;
    parts += '<circle cx="' + x + '" cy="' + y1.toFixed(1) + '" r="' + r + '" fill="' + col + '"/>';
    parts += '<circle cx="' + x + '" cy="' + y2.toFixed(1) + '" r="' + (r - 1) + '" fill="' + col + '" opacity="0.85"/>';
    if (s.fast) parts += '<circle cx="' + x + '" cy="' + y1.toFixed(1) + '" r="' + (r + 3) + '" fill="none" stroke="' + col + '" stroke-width="1" opacity="0.6"/>';
  });
  svg.innerHTML = parts;
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

// ---------- Win (a solved round feeds the run) ----------
function win() {
  stopTimer();
  const steps = state.pathActors.length;
  const optimal = state.optimal || steps;
  const perfect = (steps === optimal);
  const secs = Math.round(elapsed / 1000);

  const strand = makeStrand(steps, optimal, secs);
  const gain = applyRoundToRun(strand);
  renderGenome();
  updateHUD();

  $("winTitle").textContent = perfect ? "Perfect round! 🎯" : "Round solved! 🎉";
  $("winSteps").textContent = "+" + gain + " DNA";
  let sub = perfect ? "Fewest possible" : ("Best was " + optimal + " (" + (steps - optimal) + " over)");
  sub += "  ·  combo " + run.combo.toFixed(1) + "×";
  if (run.streak >= 2) sub += "  ·  🔥 " + run.streak + " perfect in a row";
  sub += "  ·  round " + run.rounds + " of this run";
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

  $("winEndHint").textContent = run.rounds >= 3
    ? "Stop now and you lock in a " + rarityLabel().replace("🧬 ", "").toLowerCase() + " — but the combo resets."
    : "Stop now and you lock in your genome — but the combo resets.";

  // best time (per round) is still fun to track
  let best = +(localStorage.getItem("rc_best") || 0);
  if (!best || elapsed < best) { best = elapsed; localStorage.setItem("rc_best", best); }
  refreshStats();
  updateModeBar();
  $("overlay").classList.add("rc-open");
}

// ---------- End run (the felt loss) ----------
function endRun() {
  if (!run || run.rounds === 0) { setMsg("info", "Solve at least one round to build a genome."); return; }
  $("overlay").classList.remove("rc-open");
  // count completed runs
  let runs = +(localStorage.getItem("rc_won") || 0) + 1;
  localStorage.setItem("rc_won", runs);
  refreshStats();
  const pbRun = +(localStorage.getItem("rc_pb_run") || 0);
  const pbDNA = +(localStorage.getItem("rc_pb_dna") || 0);
  $("endTitle").textContent = rarityLabel() + " locked in";
  $("endBig").textContent = run.dna + " DNA";
  let sub = run.rounds + (run.rounds === 1 ? " round" : " rounds") + " · peak combo hit along the way";
  const beatRun = run.rounds >= pbRun, beatDNA = run.dna >= pbDNA;
  if (beatRun || beatDNA) sub += "  ·  🏆 new personal best!";
  else sub += "  ·  best run " + pbRun + " rounds / " + pbDNA + " DNA";
  $("endSub").textContent = sub;
  // render final genome inline
  const eg = $("endGenome"); eg.innerHTML = "";
  eg.appendChild($("genomeSvg").cloneNode(true));
  $("endOverlay").classList.add("rc-open");
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
$("hintBtn").onclick = hint;
$("revealBtn").onclick = reveal;
$("shareBtn").onclick = shareCard;
$("endBtn").onclick = endRun;
$("flipBtn").onclick = () => { if (state) newPuzzle(state.target, state.start); };
$("undoBtn").onclick = undo;
$("winNext").onclick = () => { $("overlay").classList.remove("rc-open"); newPuzzle(); };
$("winShare").onclick = shareCard;
$("endNewRun").onclick = () => { $("endOverlay").classList.remove("rc-open"); newRun(); newPuzzle(); };
$("endShare").onclick = shareCard;
$("pvShare").onclick = doShare;
$("pvDownload").onclick = doDownload;
$("pvClose").onclick = closePreview;
$("customGo").onclick = () => {
  const a = $("customA").value, b = $("customB").value;
  if (a === b) { setMsg("err", "Pick two different films."); return; }
  $("overlay").classList.remove("rc-open");
  newPuzzle(a, b);
};

// ---------- Genome share card (client-side canvas, no server) ----------
function buildShareCard() {
  if (!run || run.strands.length === 0) return null;
  const W = 600, H = 560;
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  const g = c.getContext("2d");
  // background
  g.fillStyle = "#0d0f17"; g.fillRect(0, 0, W, H);
  const grad = g.createRadialGradient(W/2, 40, 40, W/2, 40, 500);
  grad.addColorStop(0, "rgba(40,50,80,0.5)"); grad.addColorStop(1, "rgba(13,15,23,0)");
  g.fillStyle = grad; g.fillRect(0, 0, W, H);
  // header
  g.fillStyle = "#ff4d6d"; g.font = "800 34px -apple-system, Arial, sans-serif";
  g.fillText("ReelChain", 30, 52);
  g.fillStyle = "#8a90a6"; g.font = "15px -apple-system, Arial, sans-serif";
  g.fillText("My run genome", 30, 76);
  g.fillStyle = "#ffb84d"; g.font = "700 15px -apple-system, Arial, sans-serif";
  g.fillText(rarityLabel().replace("🧬 ", ""), 30, 100);

  // big stats row
  const stats = [["ROUNDS", run.rounds], ["DNA", run.dna], ["PEAK COMBO", maxCombo() + "×"]];
  const colW = (W - 60) / 3;
  stats.forEach((s, i) => {
    const x = 30 + i * colW;
    g.fillStyle = "#8a90a6"; g.font = "600 11px -apple-system, Arial, sans-serif";
    g.fillText(s[0], x, 138);
    g.fillStyle = "#e8eaf2"; g.font = "800 34px -apple-system, Arial, sans-serif";
    g.fillText(String(s[1]), x, 174);
  });

  // genome helix
  const gy = 300, amp0 = 70, padX = 40;
  const n = run.strands.length;
  const step = Math.min(46, (W - padX * 2) / Math.max(1, n));
  const xAt = i => padX + i * step + (W - padX * 2 - (n - 1) * step) / 2;
  const yAt = (i, phase) => gy + Math.sin(i * 0.9 + phase) * Math.min(amp0, run.strands[Math.min(i, n-1)].amp * 3.2);
  // backbones
  g.strokeStyle = "#3a4160"; g.lineWidth = 2.5;
  [0, Math.PI].forEach(phase => {
    g.beginPath();
    for (let i = 0; i < n; i++) { const x = xAt(i), y = yAt(i, phase); i ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke();
  });
  // rungs + nodes
  run.strands.forEach((s, i) => {
    const x = xAt(i), y1 = yAt(i, 0), y2 = yAt(i, Math.PI);
    const col = "hsl(" + s.hue + "," + s.sat + "%,62%)";
    g.strokeStyle = col; g.lineWidth = 2; g.globalAlpha = 0.8;
    g.beginPath(); g.moveTo(x, y1); g.lineTo(x, y2); g.stroke();
    g.globalAlpha = 1; g.fillStyle = col;
    const r = s.perfect ? 8 : 5;
    g.beginPath(); g.arc(x, y1, r, 0, 7); g.fill();
    g.beginPath(); g.arc(x, y2, r - 1, 0, 7); g.fill();
    if (s.fast) { g.strokeStyle = col; g.lineWidth = 1.5; g.beginPath(); g.arc(x, y1, r + 4, 0, 7); g.stroke(); }
  });
  // legend
  g.fillStyle = "#8a90a6"; g.font = "13px -apple-system, Arial, sans-serif";
  g.fillText("● gold = perfect round   ○ ring = fast   height = chain length", 30, 470);
  // footer
  g.fillStyle = "#8a90a6"; g.font = "13px -apple-system, Arial, sans-serif";
  g.fillText("Just one more round — connect two films through shared cast", 30, H - 34);
  g.fillStyle = "#ff4d6d"; g.font = "700 15px -apple-system, Arial, sans-serif";
  g.fillText("reelchain.app", 30, H - 14);
  return c.toDataURL("image/png");
}

function maxCombo() {
  // reconstruct peak combo from perfect streaks (combo caps at 5)
  let combo = 1, peak = 1;
  run.strands.forEach(s => {
    combo = s.perfect ? Math.min(5, combo + 0.5) : Math.max(1, combo - 0.5);
    if (combo > peak) peak = combo;
  });
  return peak.toFixed(1);
}

// ---------- Preview-before-share flow ----------
let pvDataUrl = null;
function shareCard() {
  const dataUrl = buildShareCard();
  if (!dataUrl) { setMsg("info", "Solve a round first — your genome needs at least one strand."); return; }
  pvDataUrl = dataUrl;
  $("pvImg").src = dataUrl;
  $("overlay").classList.remove("rc-open");
  $("endOverlay").classList.remove("rc-open");
  $("preview").classList.add("rc-open");
}

function closePreview() { $("preview").classList.remove("rc-open"); }

async function doShare() {
  if (!pvDataUrl) return;
  const blob = await (await fetch(pvDataUrl)).blob();
  const file = new File([blob], "reelchain_genome.png", { type: "image/png" });
  try {
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({ files: [file], title: "ReelChain", text: "My ReelChain run genome — just one more round." });
      return;
    }
  } catch (e) { /* user cancelled */ return; }
  doDownload(); // fallback when Web Share unavailable
}

function doDownload() {
  if (!pvDataUrl) return;
  const a = document.createElement("a");
  a.href = pvDataUrl; a.download = "reelchain_genome.png"; a.click();
}

// ---------- Boot ----------
fillCustom();
refreshStats();
newRun();
newPuzzle();
</script>
</body>
</html>
"""

import os


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


if __name__ == "__main__":
    main()
