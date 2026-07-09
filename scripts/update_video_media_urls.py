#!/usr/bin/env python3
"""Point video embeds at media.priscillapetty.com and use HTML5 <video>."""

from __future__ import annotations

import re
from pathlib import Path

MEDIA_ORIGIN = "https://media.priscillapetty.com"

QUICKTIME_BLOCK = re.compile(
    r'<div align="center">\s*<object classid=.*?</object>\s*</div><!-- End of Quicktime Stack -->',
    re.DOTALL,
)

SRC_PATTERN = re.compile(
    r'(?:param name="src"|embed src=)\s*\n?\s*"(/videos/[^"]+\.mp4)"',
)


def video_block(url: str) -> str:
    return f"""              <div align="center">
                <video width="425" height="344" controls autoplay playsinline>
                  <source src="{url}" type="video/mp4" />
                </video>
              </div><!-- End of Quicktime Stack -->"""


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    updated = 0

    for html in sorted((root / "videos").rglob("index.html")):
        text = html.read_text(encoding="utf-8")
        if ".mp4" not in text:
            continue

        match = SRC_PATTERN.search(text)
        if not match:
            print(f"Skip (no mp4 src): {html.relative_to(root)}")
            continue

        media_url = MEDIA_ORIGIN + match.group(1)
        new_text, count = QUICKTIME_BLOCK.subn(video_block(media_url), text, count=1)
        if count != 1:
            print(f"Skip (quicktime block not found): {html.relative_to(root)}")
            continue

        html.write_text(new_text, encoding="utf-8")
        print(f"Updated: {html.relative_to(root)} -> {media_url}")
        updated += 1

    print(f"\nDone. Updated {updated} page(s).")


if __name__ == "__main__":
    main()
