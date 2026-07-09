# priscillapetty-website

Static site for [Priscilla Petty](https://www.priscillapetty.com). See [PAGES.md](PAGES.md) for page structure.

## Local preview

```bash
./run.sh
```

## Deploy

This is a plain static HTML site — no build step required.

To deploy on Cloudflare Pages, connect this GitHub repo as a new Pages project:

| Setting | Value |
|---------|--------|
| Framework preset | None |
| Build command | *(empty)* |
| Build output directory | `/` |

Cloudflare will serve the files directly from the repo. Old URLs are handled by [`_redirects`](_redirects).
