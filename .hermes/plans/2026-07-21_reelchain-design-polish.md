# ReelChain Design Polish Plan (visual/UX only)

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task. Do NOT touch game logic, data.json, or solver.py. This is a presentation-layer pass only.

**Goal:** Fix the four specific visual weaknesses revealed in the live `reelchain.app` review (empty vertical space, alignment inconsistency, small actor targets, missing interactive states) so the game reads as "finished product" not "prototype" — without changing any game rules.

**Architecture:** `reelchain_game.html` is a single-file artifact (HTML + inline `<style>` + inline `<script>`). It is *generated* by `build_game.py` from `data.json`. Two safe paths: (A) edit `reelchain_game.html` directly for a fast local preview, then port the same CSS/JS edits back into the template section of `build_game.py` so the next `build_game.py` run reproduces them; or (B) edit only `build_game.py`'s template and regenerate. **Recommended: do (A) first for fast iteration + `browser_vision` verification, then (B) to persist.** This plan assumes path (A) with a port-back step.

**Tech Stack:** Vanilla HTML/CSS/JS, Google Fonts (Fraunces display + Oswald brand). No build step. Deployed via Cloudflare Pages (`deploy/`).

**Current design system (from live review + source read):**
- Dark navy `#0b0d12` bg, raised panel `#14171f`, gold accent `#D9A63D`, ink `#F2EFE8`, ink-dim `#8E93A3`
- Fonts: `--font-display:"Fraunces"`, `--font-brand:"Oswald"`
- Layout: centered single column, top bar (logo + Run/Fame), hero (2 posters + VS badge), chain track, instruction text, 5 actor headshots row, reward line, 3 bottom circular buttons
- Already has: consistent palette, clear chain metaphor (dashed line / glow on start poster), recognizable icons

**Observed weaknesses (the scope of this plan):**
1. Excessive empty vertical space between sections → feels unfinished
2. Inconsistent alignment — reward text is left-aligned while everything else is centered
3. Actor headshots + labels too small → tap/readability risk on mobile
4. No visible interactive/hover/selected state on actor options in static view

---

## Task 1: Audit current spacing & alignment tokens

**Objective:** Establish the exact CSS variables/rules driving the empty space and misalignment before changing anything.

**Files:**
- Read: `C:\Projects\reelchain\reelchain_game.html` (CSS block, lines ~21–400)
- Read: `C:\Projects\reelchain\build_game.py` (find the template string that holds the `<style>` block)

**Step 1:** Grep `reelchain_game.html` for `margin-bottom`, `margin-top`, `padding`, `gap`, `justify-content`, `text-align`, `left-aligned` in the actor/reward/instruction section CSS.

**Step 2:** Record current values (e.g. hero `margin-bottom:10px`, chain-track `padding:18px 6px 10px`, reward line alignment rule).

**Step 3:** Confirm the reward text rule is `text-align:left` while siblings are centered — that is the misalignment bug.

**Verification:** You can describe the 3–4 largest vertical gaps and the exact CSS rule causing the left-aligned reward text. No code change yet.

---

## Task 2: Tighten vertical rhythm (kill the empty space)

**Objective:** Reduce dead vertical space so the UI reads as a cohesive screen, not scattered islands.

**Files:**
- Modify: `C:\Projects\reelchain\reelchain_game.html` `<style>` (container + section margins)
- Modify (port-back): `build_game.py` template `<style>`

**Step 1:** Wrap the whole game in a max-width container (e.g. `.rc-app{max-width:440px;margin:0 auto}`) if not present, so on desktop it reads as a phone-like card, not a stretched sparse column.

**Step 2:** Reduce inter-section gaps: change hero `margin-bottom:10px` → `:14px` is fine, but cut the large gaps *between* instruction / actor row / reward. Look for rules like `.rc-instruction{margin:NNpx 0}` and `.rc-actors{margin:NNpx 0}` and halve the top margins.

**Step 3:** Add `padding:18px 16px` to the app shell so edges aren't flush, giving a contained "product" feel.

**Step 4:** Verify in browser (see Task 6) — the screen should feel full, not empty, at 390×844 (iPhone 12 viewport).

**Verification:** Screenshot at mobile viewport shows content filling ~85–95% of vertical space with balanced, not cavernous, gaps.

---

## Task 3: Fix alignment consistency

**Objective:** Make the reward/Fame line align with the rest of the centered content (or intentionally left-align a coherent group).

**Files:**
- Modify: `reelchain_game.html` reward-line CSS
- Modify (port-back): `build_game.py` template

**Step 1:** Find the reward/Fame line rule (likely `.rc-reward` or similar with `text-align:left`). Change to `text-align:center` to match the centered column — OR, if keeping left-align, also left-align the instruction text above it so the lower "info block" is a deliberate left group. **Recommended: center it** for cohesion with the rest.

**Step 2:** Check the bottom 3-button row is centered (it is per review) — leave as-is.

**Step 3:** Verify no orphaned left-aligned elements remain in the static view.

**Verification:** Static screenshot shows all text blocks sharing one alignment axis.

---

## Task 4: Enlarge & elevate actor targets (mobile tap + readability)

**Objective:** Actor headshots are too small; increase size and add a tappable affordance.

**Files:**
- Modify: `reelchain_game.html` `.rc-actor` / headshot CSS
- Modify (port-back): `build_game.py` template

**Step 1:** Increase actor circle diameter (e.g. from ~56px to ~72px) and name font-size (e.g. 12px → 13–14px) so labels are legible.

**Step 2:** Increase the row's horizontal breathing room but keep 5 across on a 390px screen — if 5×72px overflows, reduce gap or allow horizontal scroll (already has `overflow-x:auto` on chain-track; apply same pattern to actor row if needed).

**Step 3:** Add a subtle border/ring on each actor circle (e.g. `border:2px solid var(--slot-empty)`) so they read as distinct tappable chips, not floating photos.

**Verification:** Mobile screenshot — actor names readable without zoom; circles clearly tappable.

---

## Task 5: Add interactive states (hover / selected / disabled)

**Objective:** Make actor options and buttons show clear state changes so the UI feels alive and trustworthy.

**Files:**
- Modify: `reelchain_game.html` actor + button CSS (+ minimal JS if state classes are toggled in script)
- Modify (port-back): `build_game.py` template

**Step 1:** Add `:hover` + `:active` on `.rc-actor` → `transform:translateY(-2px)` + `border-color:var(--gold)` + slight glow.

**Step 2:** Add a `.rc-actor.is-selected` state (gold ring + scale) — confirm the JS already toggles such a class; if not, add the class toggle in the click handler (search `reelchain_game.html` script for `actor` click listener).

**Step 3:** Add `:hover`/`:active` on the 3 bottom buttons (primary gold button already emphasized; add lift + brightness on hover for all three).

**Step 4:** Add `transition:transform .15s ease, border-color .15s ease` to actor/button base rules so state changes animate.

**Verification:** In browser, hover/click an actor → visible ring/lift; click primary button → brightness change. (Desktop hover testable now; mobile tap-state testable via DevTools device mode.)

---

## Task 6: Visual verification pass (browser_vision)

**Objective:** Confirm all four fixes landed and the result reads as polished, not prototype.

**Files:** None (verification only)

**Step 1:** Serve locally: `cd C:\Projects\reelchain && python -m http.server 8000` (background).

**Step 2:** `browser_navigate` to `http://localhost:8000/reelchain_game.html`, set mobile viewport 390×844.

**Step 3:** `browser_vision` prompt: "Rate vertical space balance, alignment consistency, actor tap-target size, and interactive-state clarity. List any remaining amateur traits."

**Step 4:** Iterate Tasks 2–5 if the review flags regressions.

**Verification:** Vision review reports no "unfinished / sparse / misaligned" traits; explicitly confirms the 4 target issues resolved.

---

## Task 7: Port-back to build_game.py template

**Objective:** Ensure the next `build_game.py` regen keeps the polish (don't let a rebuild wipe it).

**Files:**
- Modify: `C:\Projects\reelchain\build_game.py` (the `<style>` template string + any actor/button HTML template + click-handler JS template)

**Step 1:** In `build_game.py`, locate the template that emits the `<style>` block and the actor/button markup. Apply the same edits from Tasks 2–5.

**Step 2:** Regenerate: `python build_game.py` (confirm it writes `reelchain_game.html` and the file size/structure is intact).

**Step 3:** Re-run Task 6 verification on the regenerated file.

**Verification:** Regenerated `reelchain_game.html` matches the polished version; `git diff` shows only intended CSS/JS changes, no logic drift.

---

## Task 8: Commit & note deploy step

**Objective:** Save the work; deployment to live is a separate, explicit step (do NOT auto-deploy).

**Files:**
- `C:\Projects\reelchain\reelchain_game.html`, `build_game.py`

**Step 1:** `git add reelchain_game.html build_game.py && git commit -m "style: ReelChain visual polish — spacing, alignment, actor targets, interactive states"`

**Step 2:** Tell the user: live `reelchain.app` updates only after a Cloudflare Pages deploy from `deploy/` (per memory: git-connected, ~30–90s lag, verify post-push). **Do not deploy without explicit go-ahead.**

**Verification:** `git log -1` shows the commit; working tree clean of logic changes.

---

## Out of scope (explicitly NOT changing)
- Game rules, chain-solving logic (`solver.py`), data (`data.json`), actor dataset
- New features (score counter, progress bar, profile) — the review noted their *absence* but adding them is a separate product decision, not a polish pass
- Logo/brand mark change
- Color palette overhaul (palette is already coherent; this plan tunes layout/states, not hue)

## Risks / tradeoffs
- **Single-file edit vs template edit:** editing `reelchain_game.html` directly is fastest for preview but a later `build_game.py` run would overwrite it — hence Task 7 port-back is mandatory.
- **5 actors on small screens:** enlarging circles may overflow at 360px width; mitigate with reduced gap or horizontal scroll (already supported pattern).
- **CF Pages deploy:** live change requires a deploy step the user must approve; this plan stops at commit.

## Open questions for the user (answer before/at implementation)
1. Keep reward text **centered** (recommended) or make a deliberate left-aligned "info block"?
2. Is enlarging actors to 72px acceptable, or prefer keeping them smaller but adding stronger ring/border affordance instead?
3. Any desired micro-interaction beyond hover/lift (e.g. poster cross-fade on chain advance)?
