# ReelChain v3 — User Testing Fixes Implementation Plan

> **For Hermes:** Implement task-by-task using agency-agent specialist personas (slugs below) via `delegate_task` / `agency_agents_delegate`, with two-stage review (spec compliance, then code quality). Implementer context: this is a single static `deploy/index.html` (Cloudflare Pages, git-connected from `main`). The root `reelchain_game.html` is a synced dev copy — after editing `deploy/index.html`, run `cp deploy/index.html reelchain_game.html`.

**Goal:** Resolve all 8 issues in `docs/v3/User Testing v3.md` (screenshots + `reelchain-better-gif-design.gif` + `Logo.png`) to lift clarity, scoring fairness, and visual punch — staying inside the v3 phase.

**Architecture:** One self-contained `deploy/index.html` (HTML + CSS + vanilla JS, no build step). All state is client-side (`localStorage`) + optional KV analytics (`RC_ANALYTICS`, already bound). The "ReelPlay" share GIF is generated client-side via `gif.js` from a baked `MEDIA` map (TMDB posters/headshots, keyless). Changes are DOM/CSS/JS edits + one OG/favicon addition. No new dependencies.

**Tech Stack:** HTML/CSS/JS (vanilla), `gif.js` (vendored), Cloudflare Pages (git → `main` → `deploy/`). Review only via **reelchain.app** (live). TMDB key already baked to `MEDIA`; keep runtime keyless.

---

## Housekeeping / constraints (do not violate)
- **Review via reelchain.app only** — never inspect localhost files for sign-off. After each push, poll the live URL for a NEW marker (e.g. a unique HTML comment `<!-- v3-ut:WS2 -->`) because CF cache lag is ~30–90s; HTTP 200 + old bytes = stale.
- **Git:** branch from live `main`; never force-push/merge. Commit per workstream; push to `main`.
- **Keyless:** do not reintroduce the TMDB key into client code.
- **Sync:** every edit to `deploy/index.html` must be mirrored to `reelchain_game.html`.
- **KV:** analytics already live; new scoring must still emit `track(...)` events (reuse existing `track()`).

## Source of truth
- `docs/v3/User Testing v3.md` (8 bullet issues)
- `docs/v3/Screen 1..6.png` (current UI states)
- `docs/v3/Logo.png` (brand mark: film-reel chain + "REEL CHAIN" wordmark, CHAIN in teal)

## Agency-agent roster (lazy-loaded; assign per workstream)
| Slug | Role | Use for |
|---|---|---|
| `game-designer` | mechanics/economy/player-psych | WS2 scoring, WS4 HoF infinity, WS7 steps model |
| `ui-designer` | visual systems, clarity, brand | WS1 logo, WS3 HUD clarity, WS5 win transparency, WS8 gif style |
| `frontend-developer` | vanilla JS/CSS implementation | WS1, WS2, WS3, WS4, WS6, WS7, WS8 |
| `whimsy-injector` | delight/motion moments | WS6 countdown takeover, clock punch |
| `product-manager` | sequencing + success metrics | rollout order, acceptance |

---

## WS1 — Restore the brand logo  (agents: `ui-designer` + `frontend-developer`)
**Objective:** Show a real ReelChain mark (not just text) and add favicon + OG image so shared cards carry the brand.
**Files:** `deploy/index.html` — `<head>` (lines 3–6, add favicon/OG), `<h1>` (line 144), h1 CSS (lines 15–16).
**Key changes:**
- Add an inline SVG logo (film-reel → actor → film-reel chain + "REEL CHAIN" wordmark, CHAIN in `--accent2`/teal) replacing the plain `<h1>`. Keep it tiny (~1.2 KB) so it stays in the single file.
- Add `<link rel="icon" href="data:image/svg+xml,...">` (reuse the SVG) and OG/Twitter tags: `og:title`, `og:description`, `og:image` (point to a committed `deploy/og-reelchain.png` generated from `Logo.png`), `twitter:card=summary_large_image`.
- Verify the logo file from `docs/v3/Logo.png` is referenced (commit a web-safe `deploy/og-reelchain.png`).
**Tasks (bite-sized):**
1. Build inline SVG mark; replace `<h1>` (line 144). Add CSS `.rc-logo{...}`.
2. Add favicon data-URI + OG/Twitter meta to `<head>`.
3. Export `deploy/og-reelchain.png` from `Logo.png` (transparent bg, 1200×630).
4. Commit `WS1`, push, poll live for `<!-- v3-ut:WS1 -->` marker, confirm logo + favicon render on reelchain.app.

## WS2 — Scoring: one action = one result, with speed + accuracy multipliers  (agents: `game-designer` + `frontend-developer`)
**Objective:** Replace opaque `applyRoundToRun` (lines 370–395) with a transparent model the player can read: base points by difficulty (easy 1, medium 2, hard 3) × speed multiplier × accuracy multiplier.
**Files:** `deploy/index.html` — `DIFF` (343–348), `applyRoundToRun` (370–395), `win()` sub text (644–653).
**New model (proposed, confirm numbers in review):**
```
base = {easy:1, medium:2, hard:3}[difficulty]   // points per completed round
speedMult = clamp(2 - secs/parTime, 1.0, 2.0)    // faster = up to 2x
accuracyMult = steps===optimal ? 1.5 : max(0.5, 1 - 0.15*(steps-optimal))  // perfect chain bonus
earn = round(base * speedMult * accuracyMult)
```
- Keep `run.streak`/perfect streak (it's separate from "Fame"); surface it as 🔥 only.
- Keep HoF status driven by lifetime Fame (unchanged feed).
**Tasks:**
1. Write failing node test for `scoreRound(diff, steps, optimal, secs)` (extract the formula into a pure fn first).
2. Refactor `applyRoundToRun` to call `scoreRound`; keep side-effects (streak, saveFame, lastRound).
3. Run node harness → expected values (e.g. easy/perfect/fast = 1×1.5×2 = 3; hard/slow/over = 3×1×0.5 = 1.5→2).
4. Update `win()` sub text to show the breakdown in plain words (e.g. "Easy round · 1 pt ×1.5 perfect ×2.0 fast = +3 Fame").
5. Commit `WS2`, push, live-verify a round shows the new breakdown and KV `round_completed` logs new `fameEarned`.

## WS3 — HUD clarity: unify Round / Streak / Fame / Status  (agents: `ui-designer`)
**Objective:** Stop four look-alike tiles from reading as one number. Differentiate by icon + color + label weight; keep "one action = one result" mental model.
**Files:** HUD HTML (147–152), `updateHUD` (489–501), HUD CSS (108–119).
**Key changes:** give each tile a distinct accent (Round=blue, Streak=orange, Fame=pink, Status=teal); add a tiny icon glyph; make the sub-label ("this run", "lifetime", "to next") larger/clearer; merge "Status" into the HoF tile (WS4) so it's not a 4th mystery number.
**Tasks:** 1. Restyle 4 tiles with distinct accents+icons. 2. Fold Status into HoF tile. 3. Commit `WS3`, push, live-confirm tiles are distinguishable.

## WS4 — Hall of Fame: infinite, not a finite bar  (agents: `game-designer` + `ui-designer`)
**Objective:** HoF has no endpoint — show unlocked tiers growing forever, not a bar to "Breakthrough Star".
**Files:** `HOF` array (335–342), `renderHof` (503–520), HoF HTML (170–173), HoF CSS (120–130).
**Key changes:** render HoF as a **vertical list of tiers** (already-unlocked dimmed, current highlighted, next shown with "X Fame to <tier>"). After the top hardcoded tier, generate procedural tiers (+400 Fame each) so it never ends. Drop the `%` finite bar (or keep a subtle "progress within current tier" only).
**Tasks:** 1. Add `nextTier(fame)` that procedurally extends past `Hollywood Royalty`. 2. Rewrite `renderHof` to emit the vertical tier list into `#hof` (replace bar). 3. Update HoF CSS for list style. 4. Commit `WS4`, push, live-confirm list grows and never shows "100%/finish".

## WS5 — Win screen transparency (speed/accuracy shown)  (agents: `ui-designer` + `game-designer`)
**Objective:** The "+31 Fame" line must explain itself in plain language (ties to WS2 multipliers).
**Files:** `win()` title/sub (644–653); the `optimal` meta (line 197) hidden per WS7.
**Key changes:** sub-line = "Easy · 1 pt ×1.5 perfect ×2.0 fast = **+3 Fame** · 2 to Breakthrough Star". Remove implied randomness.
**Tasks:** 1. Wire `scoreRound` components into `winSub`. 2. Commit `WS5`, push, live-confirm a round's sub-line reads as a clear equation.

## WS6 — Run-streak movie countdown takeover  (agents: `whimsy-injector` + `frontend-developer`)
**Objective:** On each new round, a full-screen "3 · 2 · 1 · ROUND x" cinematic takeover, then drop into the game; make the top-right clock more striking.
**Files:** `newPuzzle` (397–423) call site, `modeBar` (479–487), clock (167, 738–747), add overlay markup + CSS.
**Key changes:** add `#countdown` overlay (fixed, z above HUD, below modals); on round start show 3→2→1→"ROUND x" with scale/blur animation (~1.6s), then reveal board; clock gets a brighter gradient + pulse when <10s.
**Tasks:** 1. Add `#countdown` HTML + keyframes. 2. Call `playCountdown(run.rounds+1)` at top of `newPuzzle`. 3. Punch up `#clock` style. 4. Commit `WS6`, push, live-confirm takeover plays each round and clock pops.

## WS7 — Steps vs optimal: hide optimal, persist step count, rename undo  (agents: `game-designer` + `frontend-developer`)
**Objective:** Show "Steps taken" as a count that only goes up; hide Best possible / Optimal from here; rename Undo → "Go back a step".
**Files:** meta HTML (195–199), `render` (472–475), `undo` (577–586), `undoBtn` (213).
**Key changes:**
- Add `run.movesTaken` (or `state.movesTaken`) that increments on every link and is **never decremented** by undo.
- `stepsTaken` shows `movesTaken`; remove `optimal` + `optRemaining` spans from UI (keep `state.optimal` internally for scoring/perfect detection).
- `undoBtn` label → "↩ Go back a step"; `undo()` pops path but does NOT touch `movesTaken`.
**Tasks:** 1. Add `movesTaken` counter; increment in `chooseFilm`. 2. Remove optimal/optRemaining DOM + render lines. 3. Rename undo button + keep undo logic. 4. Node-test: simulate link, undo, link → `movesTaken` = 3 not 2. 5. Commit `WS7`, push, live-confirm steps only increase and optimal is hidden.

## WS9 — Game-area visual boost  (agent: `ui-designer`) — DEFERRED (user: "I'll come back to this")
Light polish only if time allows: card depth, hover states, cast-chip density. Not blocking.

> **WS8 removed by user decision (2026-07-10):** the ReelPlay GIF was already improved with TMDB headshots/posters (live), so the `reelchain-better-gif-design.gif` redesign is out of scope.

---

## Rollout order (per `product-manager`)
WS1 (logo, cheap, high trust) → WS7 (steps, pure logic, low risk) → WS2+WS5 (scoring, paired) → WS3+WS4 (HUD+HoF, paired) → WS6 (countdown). Each = own commit + live check.

## Verification (per workstream, all live via reelchain.app)
- Logic (WS2/WS7): node ad-hoc harness in `C:\Users\andyg\AppData\Local\Temp\hermes-verify-*.js`, then delete. Must show expected scores / monotonic step count.
- Live: push to `main`; poll `https://reelchain.app/` for the workstream marker comment; confirm in browser. Re-run `GET /api/stats` sanity (KV still `kv:true`).
- GIF (WS8): confirm a generated/embedded GIF appears in the win modal and downloads.

## Open Questions
1. Scoring numbers in WS2 are a proposal — confirm easy=1/med=2/hard=3 base + 2x speed / 1.5x perfect multipliers feel right, or adjust.
2. WS9 deferred unless you flag otherwise.
3. **USER FLAG (post-WS7, 2026-07-11):** Andy misses the "optimal"/par number that WS7 removed from the live panel. Likely to revisit — prefer re-showing optimal at the **win screen** (post-solve, non-spoiling) and/or a subtle "par N" on completion, NOT live during play. Tie into WS2/WS5 breakdown. Do NOT treat WS7's hide-optimal as permanently final.

## Files likely to change
- `deploy/index.html` (primary), `reelchain_game.html` (mirror)
- `deploy/og-reelchain.png` (new, from Logo.png)
