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
| `videos/` | Video pages (HTML in git) + `.mp4` media on R2 at `media.priscillapetty.com` |

## Video hosting (Cloudflare R2)

Video **pages** deploy with the main site. Video **files** (`.mp4`) are stored in R2 and served from:

`https://media.priscillapetty.com/videos/<subdir>/<filename>.mp4`

Example: `https://media.priscillapetty.com/videos/deming/10_Deming_orchestra_ex_of_optimization.mp4`

### Upload to R2 (Cyberduck)

1. Run `./scripts/convert_videos_mp4.sh` if you need `.mp4` from `.mov` sources.
2. Run `./scripts/prepare_r2_upload.sh` to build `r2-upload/videos/`.
3. Upload the `videos` folder to your R2 bucket so keys match the URLs above.
4. Bind the bucket to custom domain `media.priscillapetty.com` in Cloudflare.

To refresh embed URLs after path changes: `./scripts/update_video_embeds.py`

Video posters (thumbnail shown while loading) live in `assets/images/video-posters/`. Regenerate with `./scripts/generate_video_posters.sh`.


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

Video files (`.mov` / `.mp4`) are gitignored. Production videos are served from `https://media.priscillapetty.com/videos/...` (Cloudflare R2). For local preview, place `.mp4` files under `videos/` on disk, or temporarily point embeds at the media URL.

## Migration

One-time migration script: [`scripts/migrate_structure.py`](scripts/migrate_structure.py)
