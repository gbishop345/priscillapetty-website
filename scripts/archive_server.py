#!/usr/bin/env python3
"""Local server for browsing archived RapidWeaver pages with theme path rewriting."""

from __future__ import annotations

import argparse
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent

RW_COMMON_RE = re.compile(r"\.\./rw_common/")


def rewrite_archive_html(text: str) -> str:
    return RW_COMMON_RE.sub("/assets/theme/", text)


class ArchiveHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path in ("", "/"):
            self.path = "/archive-viewer/index.html"
            return super().do_GET()

        if path.startswith("/_archive/") and path.endswith(".html"):
            return self._serve_archive_html(path)

        return super().do_GET()

    def _serve_archive_html(self, path: str) -> None:
        file_path = (ROOT / path.lstrip("/")).resolve()
        try:
            file_path.relative_to(ROOT)
        except ValueError:
            self.send_error(403)
            return

        if not file_path.is_file():
            self.send_error(404)
            return

        body = rewrite_archive_html(
            file_path.read_text(encoding="utf-8", errors="replace")
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        if args and isinstance(args[0], str) and args[0].startswith("GET /assets/"):
            return
        super().log_message(format, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive page preview server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()

    handler = partial(ArchiveHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)

    print(f"Archive viewer: http://{args.host}:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
