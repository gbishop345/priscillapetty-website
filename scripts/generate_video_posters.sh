#!/usr/bin/env bash
# Extract poster frames from .mp4 files for <video poster="...">.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/assets/images/video-posters"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg is required." >&2
  exit 1
fi

count=0
for mp4 in \
  "$ROOT"/videos/deming/*.mp4 \
  "$ROOT"/videos/petersen/*.mp4 \
  "$ROOT"/videos/kearns/*.mp4 \
  "$ROOT"/videos/stempel/*.mp4 \
  "$ROOT"/videos/deming-of-america/*.mp4; do
  [[ -f "$mp4" ]] || continue
  subdir=$(basename "$(dirname "$mp4")")
  base=$(basename "$mp4" .mp4)
  dest_dir="$OUT/$subdir"
  dest="$dest_dir/$base.jpg"
  mkdir -p "$dest_dir"

  if [[ -f "$dest" && "$dest" -nt "$mp4" ]]; then
    echo "Skip (up to date): ${subdir}/${base}.jpg"
    continue
  fi

  echo "Poster: ${subdir}/${base}.jpg"
  ffmpeg -y -ss 1 -i "$mp4" \
    -vframes 1 -vf "scale=425:-2" -q:v 3 \
    "$dest" -hide_banner -loglevel error
  count=$((count + 1))
done

echo "Generated $count poster(s) in $OUT/"
