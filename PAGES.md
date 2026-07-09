# Priscilla Petty Website — Page Map

## Live site (current)

Entry point: [`index.html`](index.html)

| Folder | Page | URL |
|--------|------|-----|
| *(root)* | Home | `/` |
| `about/` | About Priscilla Petty | `/about/` |
| `buy-dvd/` | Buy Deming of America DVD | `/buy-dvd/` |
| `deming/` | W. Edwards Deming | `/deming/` |
| `deming-of-america/` | The Deming of America | `/deming-of-america/` |
| `contact/` | Contact | `/contact/` |
| `thoughts/` | Priscilla's Thoughts | `/thoughts/` |
| `thoughts/part-2/` | What "Doing Deming" Means | `/thoughts/part-2/` |
| `quotes/` | Quotes: P&G Leaders | `/quotes/` |
| `quotes/artzt/` | Edwin L. Artzt | `/quotes/artzt/` |
| `quotes/gale/` | Oliver M. Gale | `/quotes/gale/` |
| `have-your-say/` | Have Your Say | `/have-your-say/` |
| `special-reports/` | Special Reports | `/special-reports/` |
| `links/` | Links | `/links/` |
| `sitemap/` | Site Map | `/sitemap/` |
| `videos/deming/01/`–`11/` | Deming Videos 1–11 | `/videos/deming/01/` … `/videos/deming/11/` |
| `videos/petersen/01/`–`04/` | Don Petersen Videos 1–4 | `/videos/petersen/01/` … `/videos/petersen/04/` |
| `videos/kearns/` | David Kearns Video | `/videos/kearns/` |
| `videos/stempel/` | Bob Stempel Video | `/videos/stempel/` |

### Shared assets

| Path | Contents |
|------|----------|
| `assets/theme/` | RapidWeaver theme (formerly `rw_common/`) |
| `assets/pages/` | Per-page Stacks CSS/JS |
| `assets/images/` | Per-section images |
| `videos/` | Video **pages** (HTML, tracked in git) + `.mov` media (gitignored, served from R2) |

## Video hosting (Cloudflare R2)

Video **pages** deploy with the site. Video **files** (`.mov`) are stored in R2 and served at the same URLs the HTML already uses (e.g. `/videos/deming/1_Deming_adv-comp.mov`).

### How it works

```
Browser → /videos/deming/01/          → static HTML from Pages
Browser → /videos/deming/foo.mov      → Pages Function → R2 bucket
```

- [`functions/videos/[[path]].js`](functions/videos/[[path]].js) — fetches `.mov` files from R2 with range-request support (seeking/scrubbing)
- [`wrangler.toml`](wrangler.toml) — R2 bucket binding (`VIDEOS` → `priscillapetty-videos`)
- [`videos/manifest.json`](videos/manifest.json) — list of all 17 video files and their R2 keys
- [`scripts/upload_videos_r2.sh`](scripts/upload_videos_r2.sh) — one-command upload script

### One-time Cloudflare setup

1. **Create the R2 bucket** (Dashboard → R2 → Create bucket, or CLI):
   ```bash
   wrangler r2 bucket create priscillapetty-videos
   ```

2. **Bind R2 to Pages** (Dashboard → Pages → your project → Settings → Functions → R2 bucket bindings):
   - Variable name: `VIDEOS`
   - R2 bucket: `priscillapetty-videos`

   Or rely on [`wrangler.toml`](wrangler.toml) if your Pages project reads it on deploy.

3. **Upload videos** (from a machine that has the `.mov` files locally):
   ```bash
   wrangler login
   ./scripts/upload_videos_r2.sh
   ```

4. **Deploy** the site (push to GitHub as usual). Video pages and the R2 function deploy together.

5. **Verify** in browser:
   - `https://<your-domain>/videos/deming/01/` — page loads
   - `https://<your-domain>/videos/deming/1_Deming_adv-comp.mov` — video file returns 200

### R2 key layout

Object keys match the URL path after `/videos/`:

| Local file | R2 key |
|------------|--------|
| `videos/deming/1_Deming_adv-comp.mov` | `deming/1_Deming_adv-comp.mov` |
| `videos/petersen/Petersen1_....mov` | `petersen/Petersen1_....mov` |

No HTML changes needed when uploading — paths are already root-absolute.

### Local dev

[`run.sh`](run.sh) serves `.mov` files directly from disk when they exist under `videos/`. R2 is only used in production.


## Archived (`_archive/`)

Unique pages with content not duplicated elsewhere on the live site. Not linked from the live nav. Old public URLs redirect via [`_redirects`](_redirects).

| Archived | Content | Old URL redirects to |
|----------|---------|----------------------|
| `page17/` | Priscilla's Columns | `/` |
| `page18/` | Allain Philosophy & Quotes | `/` |
| `page24/` | Priscilla's Blog | `/` |
| `page20/` | Harvard Business Review Article | `/` |

## Retired PHP (kept, disconnected from site)

These form handlers are not linked from the live site but are preserved in the repo under `php/`:

- `php/page3/page3.php`, `php/page3/mailer.php` — old contact form
- `php/page26/page26.php`, `php/page26/mailer.php` — DVD order form
- `php/page43/page43.php`, `php/page43/ydss_formloomjr.php` — newer contact form

Live replacements: `contact/index.html`, `buy-dvd/index.html`. Old `.php` URLs redirect via `_redirects`.

## Deleted duplicates

These were removed from the repo entirely (live versions remain). Bookmarks are handled by `_redirects`:

- `page1`–`page15` (old videos) → `/videos/...`
- `page3` (old contact) → `/contact/`
- `page7` (old DOA) → `/deming-of-america/`
- `page8` (old Deming) → `/deming/`
- `page9` (old About) → `/about/`
- `page19/` (old P&G quotes) → `/quotes/` and subpages
- `test.html` (hosting placeholder)

## Local dev

```bash
./run.sh
```

Videos (`.mov`) are gitignored. They must exist on disk under `videos/` for playback during local preview. In production, upload them to R2 — see **Video hosting (Cloudflare R2)** above.

## Migration

One-time migration script: [`scripts/migrate_structure.py`](scripts/migrate_structure.py)
