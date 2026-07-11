# ReelChain — Scoring System Rewrite Brief

**Goal:** Replace the current broken scoring with a correct, transparent, *standalone* scoring module, validated by unit tests, then plug it back into the app. Build the logic OUTSIDE the app first; do not edit the 1700-line HTML app directly.

---

## 1. What the game is
ReelChain is a movie-link puzzle: connect two films by hopping through actors they share (film → actor → film → …). Each solved round earns **Fame**. Players climb **Hall of Fame** tiers based on cumulative Fame. The app is a single static `index.html` (Cloudflare Pages). Scoring is currently embedded in that file and is wrong.

## 2. What's broken (the bug)
"Perfect" is defined **only** as *"you finished in the minimum number of film-links (par)"*. It ignores time, reveals, and undo/backtracks.

Concrete failure (real playtest): a round took 7–8 link attempts, many undos, ages to complete, and 3–4 **Reveal** clicks — yet still scored **PERFECT CHAIN 🎯** with a multiplier bonus (~+31 to +34 Fame).

Root causes confirmed in code:
- `perfect = (steps === optimal)` where `steps` = final path length only. Backtracks/undos don't change it.
- **Time-to-complete is measured but never scored** (the value is computed, then discarded).
- **Reveals:** no counter exists; using Reveal has zero effect on score.
- **Undos/backtracks:** not tracked in scoring at all (only a cosmetic "steps taken" counter in the HUD, not used by scoring).
- The "steps" that's scored is final path length only — total link attempts (including undone ones) isn't a factor.

## 3. The dials (every input that should move the score)
| Dial | Better direction | Status in current code |
|---|---|---|
| Difficulty (easy / medium / hard / surprise) | sets base reward | ✅ wired (base earn) |
| Par vs moves to solve (final optimal link count) | fewer = better | ✅ wired (over-par penalty + perfect flag) |
| **Total link attempts / backtracks (undos)** | fewer = better | ❌ NOT wired |
| **Time to complete** | faster = better | ❌ captured, then ignored |
| **Reveals used** | fewer = better | ❌ NOT wired (no counter) |
| Hints used | fewer = better | ✅ wired (penalty) |
| Second Take assist (full reveal/solve) | fewer = better | ✅ wired (penalty) |
| Streak (consecutive clean/perfect rounds) | more = better | ✅ wired (bonus) |

Hall-of-Fame tiers gate on cumulative Fame (keep as-is).

## 4. What to build
A **standalone, framework-free, pure-JS module** (no DOM, no game state, no `Date.now()` inside) that:

- Exposes one pure function:
  ```js
  scoreRound({
    difficulty,        // 'easy'|'medium'|'hard'|'surprise'
    optimalMoves,      // par (shortest link count) for this puzzle
    movesTaken,        // FINAL path length (== optimalMoves when solved at par)
    backtracks,        // number of undo/backtrack actions taken
    seconds,           // time to complete (real, from the existing timer)
    reveals,           // number of Reveal-button uses
    hints,             // number of Hint uses
    secondTake,        // boolean: used Second Take assist
    streakBefore       // streak count entering this round
  }) -> { fame, perfect, breakdown }
  ```
  - `fame`: integer Fame earned this round.
  - `perfect`: **boolean, correctly defined** (see rule below).
  - `breakdown`: array of `{ label, value }` (signed ints) summing to `fame`, so the UI can render "How you earned it".

- **Define "Perfect" correctly and make it tunable**, e.g.:
  `perfect = (movesTaken === optimalMoves) AND (backtracks === 0) AND (reveals === 0) AND (seconds <= timeBudget[difficulty])`
  (timeBudget per difficulty is a config constant — propose values, e.g. easy 30s / medium 60s / hard 120s, tunable).

- **Time scaling:** fast solves get a bonus, slow solves a penalty, with per-difficulty windows (not a flat cap). Make the window/budget a config object.

- **Penalize reveals and backtracks** (each reveal/backtrack subtracts a tunable amount, floor at a minimum positive Fame).

- **Keep** difficulty base reward + streak bonus (streak should probably require a *clean* round — define clean = perfect-or-near, no reveals/backtracks — and state the exact rule).

- **Deterministic & unit-testable.** Ship a small Node test harness asserting known cases, including:
  1. The messy playtest above (8 attempts, many undos, 3–4 reveals, slow) → **low Fame, perfect = false**.
  2. A clean fast par solve (par, 0 undos, 0 reveals, fast) → **high Fame, perfect = true**.
  3. A par solve that was slow or reveal-spammed → **not perfect**, even though moves == optimal.
  4. Edge: second Take used → heavy penalty but Fame still ≥ 1.

- **Scale:** keep the Fame ballpark similar to today (a clean perfect easy ≈ 28–34) so Hall-of-Fame thresholds don't need immediate rebalancing — but propose the actual numbers and expose them as config.

- **Packaging:** requirable as both an ES module (`export`) and a plain script (attach to `globalThis` / `module.exports` fallback) so it drops into the HTML app AND a Node test with no build step. No external dependencies.

## 5. Plug-back (done by the other agent, not you)
Once the module passes its tests, it gets dropped into the app: replace the inline `scoreRound`/`applyRoundToRun`, capture `reveals` + `backtracks` + real `seconds` at solve time, and feed `breakdown` to the win screen. Then verified live on the deployed site.

## 6. Handoff checklist for review
- [ ] `scoreRound` is pure (no DOM/Date/global state).
- [ ] "Perfect" cannot be earned with reveals > 0 or backtracks > 0 or time over budget.
- [ ] Time, reveals, backtracks all measurably change the score.
- [ ] Node test file included and all cases pass.
- [ ] Breakdown entries sum exactly to `fame`.
- [ ] Module works as ESM and plain script.
