# ReelChain

Film-to-film actor-bridge puzzle game. Connect two movies by clicking a shared
actor, then a film they're both in, building the shortest possible chain.

## Run locally
- Open `reelchain_game.html` directly in a browser, or
- `python app.py` → http://127.0.0.1:5055

## Rebuild
`python build_game.py` regenerates the standalone game (`reelchain_game.html`)
and the Cloudflare Pages source (`deploy/index.html`) from `data.json`.

## Deploy (live)
Canonical site: **https://reelchain.app**
(Cloudflare Pages project `reelchain`, production branch `main`.)

Manual redeploy:
```bash
CLOUDFLARE_API_TOKEN=<token> \
CLOUDFLARE_ACCOUNT_ID=447e2ba0b811301ef01d471963851baf \
npx wrangler pages deploy deploy --project-name reelchain --branch main
```
(`--branch main` is required or only a preview hash is published.)

## Layout
- `build_game.py` — generator (the single source of truth)
- `data.json` — 118 films / 340 actors cast graph
- `app.py` — local Flask server
- `deploy/` — static output pushed to Cloudflare Pages
- `solver.py`, `fetch_data.py` — graph helpers
