# ReelChain — Concept & Product Brief
### Connect any two films through the actors they share.

*Working prototype built & tested: solver + playable web UI (Flask + real Wikidata cast graph).*
*Run locally: `python app.py` → http://127.0.0.1:5055*

---

## 1. The idea in one line
A casual puzzle game where the player connects **Film A → Film B** by chaining shared cast members: *The Godfather → Al Pacino → Once Upon a Time in Hollywood → Samuel L. Jackson → Pulp Fiction* (2 steps). It's "Six Degrees of Kevin Bacon" **inverted** — movie-to-movie instead of actor-to-actor — which is more intuitive and far more shareable for a general audience.

## 2. Why it works (the mechanic is sound)
- The film↔actor relationship is a **bipartite graph**. Finding a link is a **shortest-path BFS** — solvable in milliseconds even across hundreds of thousands of titles.
- **Difficulty is automatically quantifiable**: path length = steps. Shared cast = 1 step (trivial); 5+ steps = brutal. The engine *generates* difficulty for free.
- **Every puzzle is verifiable** and **provably solvable** — you precompute connectivity, so you never serve an impossible daily.

## 3. Core loop (MVP)
1. Two films are presented (daily challenge, or picked/Random).
2. Player either (a) asks for the shortest link, or (b) **builds their own chain** film→actor→film… which the app validates instantly.
3. Result: number of steps + the chain visualised, plus a **verdict** (PERFECT / N over optimal) when played as Daily.
4. **Shareable result card** (PNG, Wordle-style) — generated server-side via Pillow, downloadable + Web Share on mobile. The word-of-mouth engine.

## 3b. Daily Challenge (built & tested)
- **Deterministic & fair**: a `sha256(date)` seed picks the same two films for everyone, every day — verified identical across calls.
- **Guaranteed solvable & interesting**: generator only emits pairs with an optimal path ≥ 2 steps; falls back gracefully if none found.
- **Example (2026-07-08):** `GoodFellas → Robert De Niro → Heat → Al Pacino → Once Upon a Time in Hollywood → Brad Pitt → Ocean's Eleven` (3 steps).
- Result card auto-shows "PERFECT — matched the optimal link!" or how many steps over optimal.

## 4. Game modes (roadmap)
| Mode | Hook |
|---|---|
| **Daily Challenge** | Same two films for everyone; compare step counts. Retention + social. |
| **Versus / Race** | Two players; shortest valid chain wins. |
| **Impossible Link** | Deliberately distant films; bragging rights for longest *legit* chain. |
| **Time Attack** | Solve as many as possible in 60s. |
| **Marathon** | Connect a sequence of N films with minimal total steps. |

## 5. The assist layer (what makes it *fun not frustrating*)
- Auto-suggest actors/films as you type (autocomplete against the DB).
- "You're N links away" distance indicator.
- Hint button: reveals one actor on the optimal path.
- Without this layer, free-form chaining is tedious — *this is the difference between a toy and a game.*

## 6. Data & licensing (critical decision)
| Source | Pros | Cons |
|---|---|---|
| **Wikidata** | Fully open (CC0), queryable, no key, no commercial restriction | Smaller/messier cast coverage; needs cleaning |
| **TMDB** | Huge, clean, great API | Free tier for dev; **commercial use needs approval/licensing** |
| **IMDb** | Definitive | Not licensed for redistribution |

**Recommendation:** prototype on **Wikidata** (done — live query works), graduate to **TMDB** for production with a commercial agreement. Precompute & cache the graph nightly; never query live in the hot path.

## 7. Monetisation (light, optional)
- **Free** daily challenge + versus (core loop).
- **Premium**: unlimited custom pairs, hint packs, stats/history, ad-free. Subscription or one-off "Unlock All Modes."
- **Brand/Studio partnerships**: "Connect two Marvel films" sponsored puzzles (native fit for a film-trivia game).

## 8. Name options
**ReelChain** (current working name), ReelLink, StarBridge, The Cast Chain, CrossCameo, TwoReels, Pass The Reel. *ReelChain* is available-feeling, descriptive, and trademark-friendly — recommend holding unless a search flags it.

## 9. What's proven vs. what's next
**Proven by the prototype:** real data fetch (118 films / 336 actors from Wikidata), correct BFS solver (Godfather→Pulp Fiction = 2 steps, Star Wars→Dark Knight = 5), chain validation, playable UI.
**Next:** scale dataset (TMDB), daily-challenge generator, result-card sharing, persistence/accounts, mobile wrap (Capacitor/React Native).

---
*Prototype files: `fetch_data.py` (data), `solver.py` (BFS), `app.py` (Flask API), `index.html` (UI). All run locally with `pip install flask && python app.py`.*
