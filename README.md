# priscillapetty-website

Static site for [Priscilla Petty](https://www.priscillapetty.com). See [PAGES.md](PAGES.md) for structure and video hosting.

## Local preview

```bash
./run.sh
```

Serves the site from disk (including local `.mov` files under `videos/`).

## Deploy (GitHub → Cloudflare)

This repo deploys as a **Cloudflare Worker** with static assets. Pushes to GitHub trigger an automatic build when the repo is connected in the Cloudflare dashboard.

### Cloudflare dashboard settings

In **Workers & Pages** → **priscillapetty-website** → **Settings** → **Builds**:

| Setting | Value |
|---------|--------|
| Git repository | `gbishop345/priscillapetty-website` (or your fork) |
| Production branch | `main` |
| Root directory | `/` (repo root) |
| Build command | *(leave empty — static site, no build step)* |
| Deploy command | `npx wrangler deploy` |

The Worker name in the dashboard **must match** `"name"` in [`wrangler.jsonc`](wrangler.jsonc): `priscillapetty-website`.

Custom domains (`priscillapetty.com`, `www.priscillapetty.com`) are declared in `wrangler.jsonc` and applied on each deploy. `_redirects` at the repo root handles legacy URL redirects.

### Manual deploy

```bash
npm install
npx wrangler login
npx wrangler deploy
```

### Videos (R2)

Video files are not in git. Upload once to R2:

```bash
npx wrangler r2 bucket create priscillapetty-videos   # first time only
./scripts/upload_videos_r2.sh
```

The R2 binding is configured in `wrangler.jsonc` (`VIDEOS` → `priscillapetty-videos`).
