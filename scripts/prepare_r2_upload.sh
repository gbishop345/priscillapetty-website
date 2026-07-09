#!/usr/bin/env bash
# Build r2-upload/videos/ with copies of all .mp4 files for Cyberduck.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/r2-upload/videos"

rm -rf "$ROOT/r2-upload"
mkdir -p "$OUT"/{deming,petersen,kearns,stempel,deming-of-america}

count=0
for f in "$ROOT"/videos/deming/*.mp4 \
         "$ROOT"/videos/petersen/*.mp4 \
         "$ROOT"/videos/kearns/*.mp4 \
         "$ROOT"/videos/stempel/*.mp4 \
         "$ROOT"/videos/deming-of-america/*.mp4; do
  [[ -f "$f" ]] || continue
  subdir=$(basename "$(dirname "$f")")
  base=$(basename "$f")
  cp "$f" "$OUT/$subdir/$base"
  count=$((count + 1))
done

cat > "$ROOT/r2-upload/README.txt" <<'EOF'
R2 upload folder for Cyberduck
==============================

This folder contains copies of all .mp4 video files (no HTML pages).

Structure matches the live site URLs:
  /videos/deming/1_Deming_adv-comp.mp4  →  videos/deming/1_Deming_adv-comp.mp4

Cyberduck steps
---------------
1. Connect to your Cloudflare R2 bucket (S3-compatible API).
2. Upload the entire "videos" folder from this directory into the bucket.
3. Final object keys should look like:
     videos/deming/1_Deming_adv-comp.mp4
     videos/petersen/Petersen1_people_are_the_center.mp4
     etc.

4. Enable public access on the bucket (or bind it to your site) so those
   URLs are reachable at https://priscillapetty.com/videos/...

To rebuild this folder:
  ./scripts/prepare_r2_upload.sh

To convert .mov sources to .mp4:
  ./scripts/convert_videos_mp4.sh
EOF

echo "Prepared $count videos in $ROOT/r2-upload/videos/"
echo "Upload the videos/ folder to your R2 bucket with Cyberduck."
