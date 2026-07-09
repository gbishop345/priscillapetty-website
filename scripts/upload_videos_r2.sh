#!/usr/bin/env bash
# Upload all .mov files from videos/ to Cloudflare R2.
# Prerequisites:
#   npm install -g wrangler   (or npx wrangler)
#   wrangler login
#   wrangler r2 bucket create priscillapetty-videos   (first time only)
#
# Usage:
#   ./scripts/upload_videos_r2.sh
#   BUCKET=my-other-bucket ./scripts/upload_videos_r2.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUCKET="${BUCKET:-priscillapetty-videos}"
CONTENT_TYPE="video/quicktime"

if ! command -v wrangler >/dev/null 2>&1; then
  echo "Error: wrangler CLI not found. Install with: npm install -g wrangler" >&2
  exit 1
fi

shopt -s nullglob
mapfile -t FILES < <(find "$ROOT/videos" -name '*.mov' -type f | sort)

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No .mov files found under $ROOT/videos/" >&2
  exit 1
fi

echo "Uploading ${#FILES[@]} videos to R2 bucket: $BUCKET"
echo ""

for file in "${FILES[@]}"; do
  key="${file#$ROOT/videos/}"
  echo "→ $key"
  wrangler r2 object put "$BUCKET/$key" \
    --file="$file" \
    --content-type="$CONTENT_TYPE" \
    --remote
done

echo ""
echo "Done. Verify a file:"
echo "  wrangler r2 object get $BUCKET/deming/1_Deming_adv-comp.mov --file=/tmp/test.mov --remote"
echo ""
echo "After deploy (npx wrangler deploy), test in browser:"
echo "  https://<your-domain>/videos/deming/1_Deming_adv-comp.mov"
