# priscillapetty-website

Static site for [Priscilla Petty](https://www.priscillapetty.com). See [PAGES.md](PAGES.md) for structure and video hosting.

## Local preview

```bash
./run.sh
```

## Deploy (GitHub → Cloudflare Pages)

This project is a **Cloudflare Pages** site connected to GitHub. Pushes trigger automatic deploys.

### Cloudflare dashboard settings

**Workers & Pages** → **priscillapetty-website** → **Settings** → **Builds**:

| Setting | Value |
|---------|--------|
| Build command | `npm install` |
| Deploy command | `npx wrangler pages deploy` |

Project name in `wrangler.jsonc` must match the Pages project name: `priscillapetty-website`.

Custom domain is configured in the Pages dashboard. R2 binding for videos is in `wrangler.jsonc`. Legacy URLs use `_redirects`.

### Manual deploy

```bash
npm install
npx wrangler login
npx wrangler pages deploy
```

### Videos (R2)

```bash
npx wrangler r2 bucket create priscillapetty-videos   # first time only
./scripts/upload_videos_r2.sh
```
