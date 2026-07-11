# ReelChain: Strategy and Prioritised Build Brief — Version 2

**Product stage:** strong next-step prototype; not finished, but ready for focused optimisation  
**Primary success metric:** **Gameplay** — rounds completed per active player  
**Secondary success metric:** **Organic growth** — new players who begin playing after arriving through an organic share

> **Product rule:** Do not design, build or prioritise a feature unless it has a credible route to increasing either completed rounds or organically referred new players.

---

## 1. Strategic direction

ReelChain is a repeatable movie-connection game built around one satisfying action:

> **Find the shortest chain between two films by moving through the actors who connect them.**

The core game already works. The next version should make it stronger in two ways:

1. Turn each completed round into a compelling decision to play another round.
2. Turn each completed chain into a challenge that another person wants to play.

ReelChain should favour **continuous play now**, not time-gated reasons to return later. A player who is enjoying the game should be able to keep playing immediately for as many rounds as they choose. Features that limit meaningful play to one round per day work against the primary metric and should not be introduced.

The optimised product loop is:

> **Complete a chain → earn status → see the next attainable promotion → choose a more valuable and risky round → complete again → share a visual challenge → friend plays the same chain → compare → rematch or challenge onward.**

The game does **not** need DNA or a genome as its central organising idea. Those terms came from an early concept for a shareable DNA card, but they currently make the progression system harder to understand.

DNA/genome can remain available later as an optional visual treatment for a share card. It should be removed from the central gameplay vocabulary.

---

# 2. The two success metrics

## Metric 1: Gameplay

### North-star measure

**Completed rounds per active player.**

This is more useful than page time, taps or rounds started. The product succeeds when people repeatedly finish chains.

### Leading indicators

- Round-one completion rate
- Completed round → next round started
- Completed rounds per session
- Percentage of sessions reaching rounds 3, 5 and 10
- Completion rate by difficulty
- Give-up rate by difficulty
- Seven-day returning-player rate
- Percentage of players who level up during a session

### Guardrails

- Do not increase completed rounds merely by making every chain easy.
- Do not make players afraid to attempt harder chains because the punishment is excessive.
- Do not confuse longer sessions caused by scrolling or poor navigation with stronger gameplay.
- Do not use daily limits or once-a-day puzzles to manufacture retention; the core loop should earn another round immediately.

## Metric 2: Organic growth

### North-star measure

**New players who make their first move after arriving through an organic share.**

Share-button taps are not the success measure. A share only matters when it creates another player.

### Leading indicators

- Share initiation per completed round
- Share completion rate
- Shared-link click-through rate
- Referred landing → first move
- Referred first move → completed round
- Referred player → reshare or rematch
- New referred players per active sharer

### Guardrails

- Do not reveal the answer in the social asset before the recipient plays.
- Do not interrupt every result with an aggressive share demand.
- Do not build share formats that look attractive but cannot be traced to new gameplay.

---

# 3. Simplified product language

The next build should use a small, intuitive vocabulary.

| Product idea | Recommended language | Purpose |
|---|---|---|
| Points | **Fame** or **Fame Points** | Simple reward for completing chains well |
| Long-term progression | **Hall of Fame status** | The player’s persistent movie-game standing |
| Consecutive play | **Run** or **streak** | Creates momentum across rounds |
| Shortest possible solution | **Perfect Chain** | The most important achievement state |
| More moves than necessary | **Chain Complete — over par** | Still a success, but creates a challenge to improve |
| Optional share-card aesthetic | Movie DNA | Visual flavour only; not the game economy |

“Fame” is a working name and can be tested. Whatever term is chosen, it should be understandable without explanation.

---

# 4. Feature gate for every build decision

Before a feature enters development, the team must be able to answer four questions:

1. **Which success metric does this serve?**
2. **What specific player behaviour should it change?**
3. **Which event or conversion rate will measure that change?**
4. **What result would tell us to remove or revise it?**

A feature without clear answers should not be prioritised.

---

# BUILD TIER 1 — Core strategic optimisation

Tier 1 contains the changes most likely to improve the two success metrics directly. These define the next version of the product.

---

## T1.1 Replace DNA/genome progression with personal Hall of Fame status

**Primary metric:** Gameplay  
**Behaviour to change:** increase completed round → next round conversion and rounds per session

### Build

Create a persistent **ReelChain Hall of Fame status** that grows as the player completes rounds and earns Fame.

The status system should feel like the player is building their own standing in the movie world. Possible level names could follow a movie-career theme, for example:

- Supporting Player
- Breakthrough Star
- Leading Role
- A-Lister
- Screen Legend

These are placeholder names, not a fixed final ladder.

The important interaction is not a large horizontal progression timeline. A timeline implies a finite destination and takes attention away from the present round.

Instead, show only:

- Current status
- Current Fame total
- Progress towards the **next** status
- What the next promotion unlocks or celebrates

Use a compact circular, vertical or fill-based level interaction. The player should always see one attainable next step, not the whole journey.

The system can continue indefinitely through additional levels, prestige ranks or increasingly difficult thresholds. It should never visually suggest that the game is almost over.

### Result-screen example

> **Leading Role**  
> 340 / 400 Fame  
> **One more strong round could make you an A-Lister.**

### Acceptance criteria

- A player can explain what Fame and Hall of Fame status mean without opening help.
- Every completed round visibly advances the player.
- The result screen always shows the next attainable level interaction.
- Progress persists locally without requiring account creation.

---

## T1.2 Introduce understandable risk and reward by difficulty

**Primary metric:** Gameplay  
**Behaviour to change:** make the next-round decision meaningful and encourage more completed rounds at varied difficulty

### Build

Between rounds, let the player choose how ambitious the next chain should be.

Each option should show both its potential reward and its jeopardy:

- **Easy:** lower Fame, low risk
- **Medium:** stronger Fame, moderate risk
- **Hard:** high Fame, meaningful risk
- **Surprise:** uncertain pair, highest potential reward

The exact numbers should be tuned through play data. The interaction should communicate the trade-off immediately, for example:

> **Medium chain**  
> Earn up to **+60 Fame**  
> Give up and lose **10 at-risk Fame**

### Two-score model

To preserve the user’s desired sense of losing points without damaging long-term motivation, separate progression into:

1. **Lifetime Fame:** earned status that is already secured.
2. **At-risk Fame:** a limited stake or bonus attached to the current chain or current run.

Completing a difficult chain adds more Fame. Giving up loses the clearly disclosed at-risk amount and resets or reduces the streak bonus.

The early build should **not** remove large amounts of previously secured lifetime Fame. That could make players avoid difficult rounds or leave the game entirely, directly harming completed rounds.

### Recommended scoring ingredients

`Fame earned = completion reward + difficulty reward + efficiency reward + streak reward − hint cost`

- Completing always earns something.
- A Perfect Chain earns a substantial bonus.
- Extra moves reduce the efficiency bonus but do not erase completion.
- Hints reduce the reward rather than preventing progress.
- Giving up applies the disclosed current-round loss.
- Difficulty changes the size of both the opportunity and the risk.

### Acceptance criteria

- The player understands what they can win and lose before starting.
- Harder chains produce visibly more Fame.
- Give-up penalties feel consequential but do not destroy long-term progress.
- Completion and abandonment are measurable separately for each difficulty.

---

## T1.3 Rebuild the completed-round screen as the “one more round” engine

**Primary metric:** Gameplay  
**Behaviour to change:** increase completed round → next round started

### Build

The result screen should not simply congratulate the player and ask whether they want another round. It should convert the achievement into an immediate next objective.

Recommended hierarchy:

1. **Chain outcome**
   - Perfect Chain
   - Chain Complete — one over par
   - Chain Complete — three over par
2. **Animated route recap**
3. **Fame earned and simple breakdown**
4. **Hall of Fame progress towards the next status**
5. **Next-round choices showing reward and risk**
6. Secondary actions such as share, change avatar or end session

### Example: Perfect Chain

> **PERFECT CHAIN**  
> 3 moves — par 3  
> **+75 Fame**  
> 28 Fame until your next Hall of Fame promotion
>
> **Play a Hard chain**  
> Up to +100 Fame · 20 Fame at risk

### Example: completed over par

> **CHAIN COMPLETE**  
> 5 moves — perfect is 3  
> **+38 Fame**  
> One more Medium round could level you up

The result should create a sense that the next round is part of the progress already underway, not a completely new session.

### Acceptance criteria

- The main action includes a specific next reward or promotion opportunity.
- The player can start the next round in one tap.
- The screen never presents an end-of-road horizontal ladder.
- Result → next-round-start conversion is captured for every outcome type.

---

## T1.4 Let the player choose an actor avatar that also helps them play

**Primary metric:** Gameplay  
**Secondary metric:** Organic growth  
**Behaviour to change:** increase attachment to personal progression and reduce abandonment when stuck

### Build

Allow the player to choose a favourite actor as their **Star Avatar**.

The avatar has two jobs:

1. Give the player a visible movie identity on their Hall of Fame profile and challenge cards.
2. Provide one simple, clearly understood assist during a run.

For the first implementation, every actor avatar should provide the same help mechanic so the system remains balanced. A good starting ability is:

> **Second Take:** once per run, rewind one move without losing the Perfect Chain bonus.

Alternative universal assists to test later include:

- Surface three high-potential actors from the current film
- Remove obvious dataset dead ends from one selection
- Reveal whether the current route can still reach par

Avoid launching with dozens of actor-specific powers. The avatar should create identity and a helpful moment, not a complicated character class system.

Use actor names and simple graphic tokens initially. Photographs or likeness-based artwork should only be used where the relevant rights and licensing position is clear.

### Acceptance criteria

- Avatar choice takes seconds, not a long onboarding flow.
- The avatar remains visible but does not crowd the game board.
- The assist is usable in one tap and its effect is obvious.
- Track whether using the assist increases chain completion and subsequent rounds.

---

## T1.5 Bring back Instant ReelPlay as the visual result and share asset

**Primary metric:** Organic growth  
**Secondary metric:** Gameplay  
**Behaviour to change:** increase challenge shares, referred first moves and referred completions

### Build

After every completed round, generate an animated **Instant ReelPlay** that builds the chain node by node.

The animation should celebrate the fact that a route was created while making the difference between a perfect and imperfect result unmistakable.

### Perfect Chain treatment

- Strong **PERFECT CHAIN** title
- Start and target films anchor the animation
- The exact number of moves is prominent
- The chain builds cleanly with no wasted nodes
- Final challenge copy:

> **I found the perfect 3-move chain. Can you match it without hints?**

Time can operate as a secondary comparison when both players find a perfect route. Another future option is rewarding a different valid perfect route.

### Over-par treatment

- Begin with **CHAIN COMPLETE** rather than framing completion as failure
- Animate every move the player made
- Visually distinguish excess moves from the perfect number
- For example, three optimal-position nodes can remain solid while two excess nodes pulse, stack or retract
- Final challenge copy:

> **I connected these films in 5 moves. Perfect is 3. Can you find the Perfect Chain?**

This creates a more compelling social invitation than simply sharing a score.

### Important spoiler rule

The in-game replay can show the full route to the player. The exported challenge asset should communicate the shape and length of the chain without revealing every middle film and actor before the recipient plays.

Recommended share version:

- Show start and target films
- Animate the correct number of intermediary nodes
- Conceal intermediary labels with silhouettes, question marks or blurred tokens
- Reveal the sender’s full route only after the recipient completes or gives up

The share should show the achievement, not give away the answer.

### Acceptance criteria

- The animation appears immediately after completion and does not block the next action.
- Perfect and over-par results are visually distinct without requiring explanatory copy.
- A spoiler-safe challenge version can be shared as an animated asset or linked preview.
- Every asset retains an attributable playable challenge link.

---

## T1.6 Build the playable friend challenge around Perfect Chain

**Primary metric:** Organic growth  
**Behaviour to change:** turn a completed chain into a new player and then another share

### Build

The social action should be framed around the recipient’s task, not the sender’s profile:

- **Perfect result:** `Can you match my Perfect Chain?`
- **Over par:** `Can you solve this in the perfect number of moves?`

The challenge link must preserve:

- Start film
- Target film
- Par or perfect number
- Difficulty and game rules
- Sender’s move count
- Sender’s time and hints for later comparison
- Dataset version

### Recipient journey

1. Friend opens the shared link.
2. They immediately see the same start and target films.
3. The challenge statement is clear in one sentence.
4. They begin in one tap, without registration or homepage detour.
5. The sender’s route remains hidden.
6. After completion or give-up, both results are compared.
7. The recipient can send a rematch or challenge someone else.

### Comparison states

- `You found the Perfect Chain too — 18 seconds faster.`
- `You beat Andy: 3 moves versus 5.`
- `Andy still leads: 3 moves versus 4.`
- `This one beat both of you — try a rematch.`

### Acceptance criteria

- Every completed round can create a stable, playable challenge URL.
- The recipient reaches their first move with no unnecessary intermediate screen.
- The sender’s answer is protected until the recipient finishes or reveals it.
- The full loop from share to recipient completion to reshare is measurable.

---

## T1.7 Instrument the two loops before adding more systems

**Metrics:** Gameplay and Organic growth

The Tier 1 work cannot be judged without event-level measurement.

### Minimum gameplay events

- `round_started`
- `actor_selected`
- `film_selected`
- `undo_used`
- `avatar_assist_used`
- `hint_used`
- `round_completed`
- `round_given_up`
- `fame_earned`
- `fame_lost`
- `hall_of_fame_progress_viewed`
- `hall_of_fame_level_reached`
- `next_round_selected`

### Minimum sharing events

- `instant_reelplay_generated`
- `challenge_created`
- `share_sheet_opened`
- `share_completed` where detectable
- `challenge_landed`
- `challenge_first_move`
- `challenge_completed`
- `comparison_viewed`
- `rematch_created`
- `challenge_reshared`

### Essential properties

- Anonymous player/session ID
- Pair ID
- Difficulty
- Par
- Moves used
- Time
- Hints and undos
- Fame available, earned and lost
- Current Hall of Fame level
- Challenge ID
- Referral source/channel
- Dataset version

---

# BUILD TIER 2 — Other high-value discoveries

Tier 2 contains improvements observed in the recorded gameplay that should strengthen completion, retention or the challenge loop without changing the strategic direction above.

---

## T2.1 Reduce first-screen cognitive load

**Primary metric:** Gameplay

The opening state currently asks the player to process too many systems before making the first meaningful move.

### Build

Keep the first viewport focused on:

- Start film
- Target film
- Current chain
- Actor choices
- Steps versus par
- Small Fame/status indicator

Move or collapse:

- Full progression detail
- Difficulty tabs during active play
- Share before a result exists
- End-session action
- Detailed route calculations

The player should be able to make the first choice without scrolling.

---

## T2.2 Make long filmographies fast to navigate

**Primary metric:** Gameplay

Long actor filmographies can turn movie reasoning into list administration.

### Build

- Show a curated first set of useful or recognisable films
- Add instant search/filter
- Use `More films` rather than rendering everything immediately
- Optionally group very long lists by decade or franchise
- Keep the current chain visible while the player searches

Curation must not silently place the correct answer first every time. The purpose is to reduce scrolling, not solve the puzzle.

---

## T2.3 Treat dataset dead ends differently from player mistakes

**Primary metric:** Gameplay

A branch caused by incomplete coverage should not feel like a strategic failure.

### Build

Distinguish:

- **Coverage dead end:** the actor only has the film just used in the current dataset
- **Strategic dead end:** valid credits exist, but the route has become poor or impossible under the rules

For coverage dead ends:

- Warn or disable before selection where possible
- Do not remove Perfect Chain eligibility
- Offer one-tap return to the previous choice

For strategic dead ends:

- Allow the consequence
- Make rewind immediate
- Explain the game state without apologising for the database

---

## T2.4 Replace exact route judgement with non-spoiling guidance

**Primary metric:** Gameplay

Constant “optimal from here” information risks making the interface feel like it already knows the answer and is judging each move.

### Build

- Show par at the start
- During play, use qualitative guidance:
  - `Still on a perfect route`
  - `A longer route, but still live`
  - `This branch is getting risky`
- Reserve exact shortest-path information for a deliberate hint or the completed result

This keeps orientation without removing discovery.

---

## T2.5 Add lightweight rivalry and rematch history

**Metrics:** Gameplay and Organic growth

Store a simple history of challenge exchanges without requiring a full social network:

- Head-to-head score
- Latest challenge result
- Best shared chain
- `Send rematch`

Account creation should only be introduced later for cross-device history or notifications. Core challenge play remains account-free.

---

## T2.6 Build a personal Hall of Fame profile from real play

**Metrics:** Gameplay and Organic growth

Once a player has enough rounds, their profile can summarise achievements that feel earned:

- Current Hall of Fame status
- Best Perfect Chain
- Number of perfect rounds
- Highest difficulty completed
- Favourite or most-used actor
- Most-played decade or franchise
- Best challenge record

This creates identity and additional share material without making a fictional “genome” the primary product concept.

---

# BUILD TIER 3 — Hygiene, polish and lower-priority work

Tier 3 should improve usability and quality, but it should not displace work that directly proves the two core loops.

## T3.1 Naming and copy consistency

- Remove DNA/genome terminology from active gameplay
- Use one term consistently for moves, links and par
- Make `Give up` consequences explicit before confirmation
- Make Perfect Chain language consistent across gameplay, result and share
- Distinguish `End session` from `Give up current chain`

## T3.2 Mobile interaction hygiene

- Keep Undo or Second Take accessible without scrolling
- Respect mobile safe areas
- Use sufficiently large tap targets
- Preserve selection state when navigating long lists
- Avoid accidental double taps
- Keep the active chain anchored during scrolling

## T3.3 Feedback and accessibility

- Add optional haptics for a successful link, dead end, Perfect Chain and level-up
- Add optional sound, with a clear mute control
- Do not rely on colour alone to distinguish perfect, over-par and dead-end states
- Respect reduced-motion settings for Instant ReelPlay
- Ensure readable contrast and scalable text

## T3.4 Performance and reliability

- Preload likely next-state data where practical
- Avoid visible pauses when opening filmographies
- Generate the result animation without blocking the next-round button
- Preserve an active chain after refresh or temporary connection loss
- Handle missing credits and failed share generation gracefully

## T3.5 Sharing infrastructure hygiene

- Dynamic social metadata for every challenge
- Static fallback image when animated previews are unsupported
- Native share sheet plus reliable `Copy link`
- Referral attribution that survives app/browser handoff where possible
- Clear spoiler-safe preview text

## T3.6 Data quality operations

- Log coverage dead ends
- Prioritise missing credits that cause the most failed or abandoned rounds
- Version the graph so friend challenges remain reproducible
- Prevent a challenge from silently changing because the dataset changed

## T3.7 Deferred features

Do not prioritise these until Tier 1 has improved the two success metrics:

- Public global leaderboards
- Complex actor-specific powers
- Shops, currencies or battle passes
- Synchronous multiplayer
- Mandatory accounts
- Large cosmetic redesigns detached from conversion behaviour
- Aggressive notifications
- Once-a-day or time-gated core puzzles that interrupt continuous play
- Extensive licensed poster or actor-image systems
- Additional scoring categories that players cannot predict

---

# 5. Recommended build sequence

## Release 1A — Prove stronger repeated gameplay

1. Replace DNA/genome with Fame and Hall of Fame status
2. Build the compact next-level interaction
3. Add difficulty-based reward and limited at-risk Fame
4. Rebuild the result screen around the next round
5. Add the universal actor-avatar assist
6. Instrument the gameplay funnel

### Decision gate

Continue when the build improves:

- Completed round → next round started
- Completed rounds per session
- Percentage of sessions reaching rounds 3 and 5

without causing a disproportionate increase in hard-chain give-up or total session abandonment.

## Release 1B — Prove organic challenge growth

1. Restore Instant ReelPlay
2. Create separate Perfect Chain and over-par animations
3. Produce spoiler-safe share exports
4. Build stable challenge links
5. Create direct-to-play recipient landing
6. Add result comparison, rematch and reshare
7. Instrument the complete referral funnel

### Decision gate

Optimise for:

- New referred players making a first move
- Referred players completing the challenge
- Referred players resharing or rematching

Do not use raw share-button taps as the decision metric.

## Release 2 — Remove the biggest flow blockers

1. Simplify the first viewport
2. Improve long filmography navigation
3. Separate coverage dead ends from strategic dead ends
4. Add non-spoiling route guidance
5. Add lightweight rivalry history and Hall of Fame profiles

## Release 3 — Hygiene and polish

Complete the Tier 3 quality work in the order indicated by observed drop-off, bugs and user feedback.

---

# 6. Prioritisation summary

| Recommendation | Tier | Primary metric |
|---|---:|---|
| Fame and Hall of Fame progression | 1 | Gameplay |
| Difficulty-based reward and at-risk Fame | 1 | Gameplay |
| Result screen built around the next round | 1 | Gameplay |
| Actor avatar with one universal assist | 1 | Gameplay |
| Instant ReelPlay result animation | 1 | Organic growth |
| Perfect versus over-par challenge creative | 1 | Organic growth |
| Direct playable challenge and comparison loop | 1 | Organic growth |
| Gameplay and referral instrumentation | 1 | Both |
| Reduced opening complexity | 2 | Gameplay |
| Searchable and condensed filmographies | 2 | Gameplay |
| Fair treatment of dataset dead ends | 2 | Gameplay |
| Non-spoiling route guidance | 2 | Gameplay |
| Rivalry/rematch history | 2 | Both |
| Personal Hall of Fame profile | 2 | Both |
| Naming, mobile, accessibility and performance hygiene | 3 | Supporting |

---

# 7. Definition of success

The next version is working when:

1. Players understand the reward and status system without learning DNA or genome terminology.
2. A player can continue into another round immediately, without a daily limit or waiting period.
3. A completed chain visibly moves the player towards their next Hall of Fame status.
4. Choosing another round feels like an attractive risk-and-reward decision.
5. Harder chains offer more Fame, while giving up has a clear but proportionate consequence.
6. The actor avatar makes the experience feel personal and provides useful help without adding complexity.
7. Instant ReelPlay makes both a Perfect Chain and an over-par completion visually compelling.
8. An over-par result naturally creates the challenge: **Can you find the Perfect Chain?**
9. A friend can open the share, play the same pair immediately, compare results and challenge onward.
10. Every significant build can be tied to either completed rounds or organically referred new players.

The central product principle is:

> **Every completed chain should create either a stronger reason for the player to complete another round or a stronger reason for someone in their network to start one.**
