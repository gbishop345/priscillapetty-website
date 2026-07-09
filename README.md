# priscillapetty-website

Static site for [Priscilla Petty](https://www.priscillapetty.com). See [PAGES.md](PAGES.md) for structure and video hosting.

## Local preview

```bash
./run.sh
```

## Deploy (GitHub → Cloudflare Pages)

### Cloudflare Builds settings

**Workers & Pages** → **priscillapetty-website** → **Settings** → **Builds**:

| Setting | Value |
|---------|--------|
| Root directory | `/` |
| Build command | *(empty)* |
| **Deploy command** | `npm run deploy` |

Node **22** is required (`.node-version`). Cloudflare auto-runs `bun install` before the deploy command.

### Fix `Authentication error [code: 10000]`

The deploy command needs a token with **Cloudflare Pages → Edit** permission. The default CI token often lacks this.

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. **Create Token** → use **Edit Cloudflare Workers** template, or create custom with:
   - Account → **Cloudflare Pages** → **Edit**
   - Account → **Workers R2 Storage** → **Edit** *(for video bindings)*
   - Account → **Account Settings** → **Read**
3. In **Workers & Pages** → **priscillapetty-website** → **Settings** → **Environment variables**, add for **Production** (and Preview):

| Variable | Value |
|----------|--------|
| `CLOUDFLARE_API_TOKEN` | the token you just created |
| `CLOUDFLARE_ACCOUNT_ID` | `5a377a291d032ba4017ebb2b132967b5` |

4. Save and **retry deployment**.

### R2 binding (videos)

**Settings** → **Functions** → **R2 bucket bindings**: `VIDEOS` → `priscillapetty-videos`

Upload videos once: `./scripts/upload_videos_r2.sh`

### Manual deploy (from your machine)

```bash
npm install
npx wrangler login
npm run deploy
```
