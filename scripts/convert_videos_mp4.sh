#!/usr/bin/env bash
# Convert all .mov files under videos/ to .mp4 (H.264 + AAC).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg is required." >&2
  exit 1
fi

count=0
for mov in \
  "$ROOT"/videos/deming/*.mov \
  "$ROOT"/videos/petersen/*.mov \
  "$ROOT"/videos/kearns/*.mov \
  "$ROOT"/videos/stempel/*.mov \
  "$ROOT"/videos/deming-of-america/*.mov; do
  [[ -f "$mov" ]] || continue
  mp4="${mov%.mov}.mp4"
  if [[ -f "$mp4" && "$mp4" -nt "$mov" ]]; then
    echo "Skip (up to date): ${mp4#$ROOT/}"
    continue
  fi
  echo "Converting: ${mov#$ROOT/}"
  ffmpeg -y -i "$mov" \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    "$mp4" \
    -hide_banner -loglevel error
  count=$((count + 1))
done

echo "Converted $count file(s)."
