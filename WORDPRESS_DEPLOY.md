# ReelChain — WordPress Plugin Install Guide (isitablog.com)

ReelChain ships as a tiny **WordPress plugin**. On self-hosted WordPress it gives
you a `[reelchain]` shortcode (paste into any page) **and** a `reelchain_game()`
template tag (for theme files). No backend, no API, no database — the full
film graph is baked into the JS at build time.

## What was produced

`build_game.py` now emits a ready-to-upload plugin folder:

```
reelchain/
├── reelchain.php                # plugin: registers [reelchain] shortcode + template tag
└── assets/
    ├── reelchain.css            # game styles, scoped to .reelchain-app
    ├── reelchain.js             # game logic + embedded 118-film / 340-actor graph
    └── reelchain-markup.html    # the game's HTML body (injected by the shortcode)
```

(It also still emits `reelchain_game.html` for direct use/iframe, and
`reelchain_embed.html` as a Custom-HTML-block fallback.)

## Install (3 ways)

### A. Zip upload (no FTP / no terminal on the server)
1. On your PC, zip the `reelchain/` folder → `reelchain.zip`.
2. WP admin → **Plugins → Add New → Upload Plugin** → choose `reelchain.zip` → Install → Activate.
3. Done.

### B. FTP / file manager
1. Upload the `reelchain/` folder to `wp-content/plugins/`.
   (Result: `wp-content/plugins/reelchain/reelchain.php`.)
2. WP admin → **Plugins** → activate **ReelChain**.

### C. WP-CLI (if you have shell on the server)
```bash
# from the machine that has the files:
cd /path/to/build
zip -r reelchain.zip reelchain
# then in WP root, or just copy the folder:
cp -r reelchain wp-content/plugins/
wp plugin activate reelchain
```

## Use it

### As a shortcode (the easy way)
1. **Pages → Add New**, title it "ReelChain".
2. Set the **permalink/slug** to `reelchain`, under a `games` parent (or slug
   `games/reelchain`) so the URL is `https://isitablog.com/games/reelchain`.
3. In the block editor, add a **Shortcode** block (or just type in a Paragraph /
   Custom HTML block) containing exactly:
   ```
   [reelchain]
   ```
4. Publish. The game appears, with your theme's header/footer around it.

### As a template tag (for developers)
In a theme template, e.g. `page-reelchain.php`:
```php
<?php get_header(); ?>
<main>
  <?php reelchain_game(); ?>
</main>
<?php get_footer(); ?>
```

## How it stays safe inside WordPress
- CSS/JS are **external files** enqueued via `wp_enqueue_*`. WordPress's
  `wpautop`/`kses` content filters **never touch them**, so the game's
  `<script>` can't be stripped or mangled (this is the failure mode of pasting
  raw `<script>` into a block).
- All CSS is **scoped to `.reelchain-app`**, so it can't leak onto (or be
  overridden by) your theme.
- Assets are only loaded on pages that actually use the shortcode
  (`has_shortcode` check) — zero footprint elsewhere.

## Updating the game later
1. Edit `data.json` / rerun `fetch_data.py`, then `python build_game.py`.
2. Re-zip the `reelchain/` folder (or re-FTP it), overwriting the existing
   plugin files. No need to deactivate. Bump the `Version:` in `reelchain.php`
   if you want WP to show an update — purely cosmetic.

## Notes
- If you ever want to embed the game on a **non-WordPress** page, use the
  standalone `reelchain_game.html` (iframe) or `reelchain_embed.html`.
- The game is fully client-side; there is no PHP runtime logic beyond serving
  the markup. It will run on any WordPress version from ~4.0 onward.
