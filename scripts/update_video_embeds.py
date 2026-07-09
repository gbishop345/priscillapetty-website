#!/usr/bin/env python3
"""Update video pages with poster images and standard preload behavior."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

MEDIA_ORIGIN = "https://media.priscillapetty.com"

VIDEO_BLOCK = re.compile(
    r'<div align="center">\s*<video[^>]*>.*?</video>\s*</div><!-- End of Quicktime Stack -->',
    re.DOTALL,
)

SRC_PATTERN = re.compile(
    r'<source src="(https://media\.priscillapetty\.com)(/videos/[^"]+\.mp4)"',
)


def poster_path(media_path: str) -> str:
    """/videos/deming/foo.mp4 -> /assets/images/video-posters/deming/foo.jpg"""
    rel = media_path.removeprefix("/videos/")
    stem = rel.rsplit(".", 1)[0]
    # URL-encode only the filename segment for paths with spaces
    parts = stem.split("/")
    parts[-1] = quote(parts[-1])
    return "/assets/images/video-posters/" + "/".join(parts) + ".jpg"


def video_block(media_url: str, poster: str) -> str:
    return f"""              <div align="center">
                <video
                  width="425"
                  height="344"
                  controls
                  playsinline
                  preload="metadata"
                  poster="{poster}">
                  <source src="{media_url}" type="video/mp4" />
                </video>
              </div><!-- End of Quicktime Stack -->"""


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    updated = 0

    for html in sorted((root / "videos").rglob("index.html")):
        text = html.read_text(encoding="utf-8")
        match = SRC_PATTERN.search(text)
        if not match:
            print(f"Skip (no media src): {html.relative_to(root)}")
            continue

        media_url = match.group(1) + match.group(2)
        poster = poster_path(match.group(2))
        new_text, count = VIDEO_BLOCK.subn(
            video_block(media_url, poster), text, count=1
        )
        if count != 1:
            print(f"Skip (video block not found): {html.relative_to(root)}")
            continue

        html.write_text(new_text, encoding="utf-8")
        print(f"Updated: {html.relative_to(root)}")
        updated += 1

    print(f"\nDone. Updated {updated} page(s).")


if __name__ == "__main__":
    main()
