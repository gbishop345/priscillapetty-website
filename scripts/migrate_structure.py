#!/usr/bin/env python3
"""One-time migration: rename pageXX folders and consolidate assets."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# old_html_path -> (new_html_path, section_key for assets)
PAGES: list[tuple[str, str, str]] = [
    ("page16/page16.html", "sitemap/index.html", "sitemap"),
    ("page21/page21.html", "have-your-say/index.html", "have-your-say"),
    ("page22/page22.html", "special-reports/index.html", "special-reports"),
    ("page23/page23.html", "links/index.html", "links"),
    ("page26/page26.html", "about/index.html", "about"),
    ("page26/buy-dvd.html", "buy-dvd/index.html", "buy-dvd"),
    ("page27/page27.html", "deming/index.html", "deming"),
    ("page28/page28.html", "deming-of-america/index.html", "deming-of-america"),
    ("page43/page43.html", "contact/index.html", "contact"),
    ("page50/page50.html", "thoughts/index.html", "thoughts"),
    ("page50/page51/page51.html", "thoughts/part-2/index.html", "thoughts-part-2"),
    ("page42/page42.html", "quotes/index.html", "quotes"),
    ("page42/page24/page24.html", "quotes/artzt/index.html", "quotes-artzt"),
    ("page42/page45/page45.html", "quotes/gale/index.html", "quotes-gale"),
    ("page29/page29.html", "videos/deming/01/index.html", "videos-deming-01"),
    ("page30/page30.html", "videos/deming/02/index.html", "videos-deming-02"),
    ("page31/page31.html", "videos/deming/03/index.html", "videos-deming-03"),
    ("page32/page32.html", "videos/deming/04/index.html", "videos-deming-04"),
    ("page33/page33.html", "videos/deming/05/index.html", "videos-deming-05"),
    ("page34/page34.html", "videos/deming/06/index.html", "videos-deming-06"),
    ("page35/page35.html", "videos/deming/07/index.html", "videos-deming-07"),
    ("page36/page36.html", "videos/deming/08/index.html", "videos-deming-08"),
    ("page38/page38.html", "videos/deming/09/index.html", "videos-deming-09"),
    ("page39/page39.html", "videos/deming/10/index.html", "videos-deming-10"),
    ("page37/page37.html", "videos/deming/11/index.html", "videos-deming-11"),
    ("page40/page40.html", "videos/petersen/01/index.html", "videos-petersen-01"),
    ("page41/page41.html", "videos/petersen/02/index.html", "videos-petersen-02"),
    ("page48/page48.html", "videos/petersen/03/index.html", "videos-petersen-03"),
    ("page49/page49.html", "videos/petersen/04/index.html", "videos-petersen-04"),
    ("page46/page46.html", "videos/kearns/index.html", "videos-kearns"),
    ("page47/page47.html", "videos/stempel/index.html", "videos-stempel"),
]

VIDEO_MOVES: dict[str, str] = {
    "page29": "videos/deming",
    "page30": "videos/deming",
    "page31": "videos/deming",
    "page32": "videos/deming",
    "page33": "videos/deming",
    "page34": "videos/deming",
    "page35": "videos/deming",
    "page36": "videos/deming",
    "page37": "videos/deming",
    "page38": "videos/deming",
    "page39": "videos/deming",
    "page40": "videos/petersen",
    "page41": "videos/petersen",
    "page46": "videos/kearns",
    "page47": "videos/stempel",
    "page48": "videos/petersen",
    "page49": "videos/petersen",
    "page28": "videos/deming-of-america",
}

PHP_DIRS = ["page3", "page26", "page43"]
PHP_FILES = {
    "page3": ["page3.php", "files/mailer.php"],
    "page26": ["page26.php", "files/mailer.php"],
    "page43": ["page43.php", "files/ydss_formloomjr.php"],
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
STACK_EXTS = {".css", ".js"}
SKIP_FILES = {"mailer.php", "ydss_formloomjr.php", "page3.php", "page26.php", "page43.php"}

asset_map: dict[str, str] = {}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def register_asset(old_rel: str, new_abs: str) -> None:
    old_rel = old_rel.replace("\\", "/")
    if not new_abs.startswith("/"):
        new_abs = "/" + new_abs
    asset_map[old_rel] = new_abs
    # Shorthand used in page HTML (e.g. files/stacks_page_page27.css)
    if "/files/" in old_rel or old_rel.startswith("files/"):
        short = "files/" + Path(old_rel).name
        asset_map[short] = new_abs
    if "/assets/" in old_rel or old_rel.startswith("assets/"):
        short = "assets/" + Path(old_rel).name
        asset_map[short] = new_abs


def move_theme() -> None:
    src = ROOT / "rw_common"
    dst = ROOT / "assets" / "theme"
    if src.exists():
        ensure_parent(dst)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
    register_asset("rw_common/", "/assets/theme/")


def move_root_files() -> None:
    src = ROOT / "files"
    if not src.exists():
        return
    pages_dst = ROOT / "assets" / "pages" / "home"
    images_dst = ROOT / "assets" / "images" / "home"
    pages_dst.mkdir(parents=True, exist_ok=True)
    images_dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() in IMAGE_EXTS:
            shutil.copy2(f, images_dst / f.name)
            register_asset(f"files/{f.name}", f"/assets/images/home/{f.name}")
        elif f.suffix.lower() in STACK_EXTS:
            shutil.copy2(f, pages_dst / f.name)
            register_asset(f"files/{f.name}", f"/assets/pages/home/{f.name}")
        elif f.name not in SKIP_FILES:
            shutil.copy2(f, pages_dst / f.name)
            register_asset(f"files/{f.name}", f"/assets/pages/home/{f.name}")


def move_page_dir_assets(page_dir: str, section: str) -> None:
    base = ROOT / page_dir
    if not base.exists():
        return
    pages_dst = ROOT / "assets" / "pages" / section
    images_dst = ROOT / "assets" / "images" / section
    pages_dst.mkdir(parents=True, exist_ok=True)
    images_dst.mkdir(parents=True, exist_ok=True)

    video_dest = VIDEO_MOVES.get(page_dir.split("/")[0])
    if video_dest:
        (ROOT / video_dest).mkdir(parents=True, exist_ok=True)

    for sub in ("files", "assets"):
        subdir = base / sub
        if not subdir.exists():
            continue
        for f in subdir.iterdir():
            if not f.is_file():
                continue
            rel = f"{page_dir}/{sub}/{f.name}"
            if f.suffix.lower() == ".mov":
                dest_dir = ROOT / (video_dest or "videos/misc")
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest_dir / f.name)
                register_asset(rel, f"/{(video_dest or 'videos/misc')}/{f.name}")
                register_asset(f"assets/{f.name}", f"/{(video_dest or 'videos/misc')}/{f.name}")
            elif f.name in SKIP_FILES:
                continue
            elif f.suffix.lower() in IMAGE_EXTS:
                shutil.copy2(f, images_dst / f.name)
                register_asset(rel, f"/assets/images/{section}/{f.name}")
            elif f.suffix.lower() in STACK_EXTS or f.suffix.lower() == ".xml":
                shutil.copy2(f, pages_dst / f.name)
                register_asset(rel, f"/assets/pages/{section}/{f.name}")
            else:
                shutil.copy2(f, pages_dst / f.name)
                register_asset(rel, f"/assets/pages/{section}/{f.name}")


def move_html_pages() -> None:
    for old, new, section in PAGES:
        src = ROOT / old
        if not src.exists():
            print(f"WARN missing {old}")
            continue
        dst = ROOT / new
        ensure_parent(dst)
        shutil.copy2(src, dst)


def move_php() -> None:
    for page_dir in PHP_DIRS:
        dst_base = ROOT / "php" / page_dir
        dst_base.mkdir(parents=True, exist_ok=True)
        src_base = ROOT / page_dir
        for rel in PHP_FILES[page_dir]:
            src = src_base / rel
            if src.exists():
                dst = dst_base / Path(rel).name if "/" in rel else dst_base / rel
                ensure_parent(dst)
                shutil.copy2(src, dst)


def build_url_map() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for old, new, _ in PAGES:
        new_url = "/" + new.replace("index.html", "").rstrip("/") + "/"
        if new == "sitemap/index.html":
            new_url = "/sitemap/"
        pairs.append((old, new_url))
        parts = old.split("/")
        for depth in range(4):
            prefix = "/".join([".."] * depth)
            rel = f"{prefix}/{old}" if prefix else old
            rel = rel.lstrip("/")
            if rel != old:
                pairs.append((rel, new_url))
    # legacy duplicate targets -> new urls
    legacy = [
        ("page1/page1.html", "/videos/deming/01/"),
        ("page2/page2.html", "/videos/deming/02/"),
        ("page4/page4.html", "/videos/deming/03/"),
        ("page6/page6.html", "/videos/deming/04/"),
        ("page10/page10.html", "/videos/deming/05/"),
        ("page11/page11.html", "/videos/deming/06/"),
        ("page12/page12.html", "/videos/deming/07/"),
        ("page5/page5.html", "/videos/petersen/01/"),
        ("page13/page13.html", "/videos/petersen/02/"),
        ("page14/page14.html", "/videos/kearns/"),
        ("page15/page15.html", "/videos/stempel/"),
        ("page3/page3.html", "/contact/"),
        ("page7/page7.html", "/deming-of-america/"),
        ("page8/page8.html", "/deming/"),
        ("page9/page9.html", "/about/"),
        ("page19/page19.html", "/quotes/"),
        ("page19/page24/page24.html", "/quotes/artzt/"),
        ("page19/page20/page20.html", "/quotes/gale/"),
    ]
    pairs.extend(legacy)
    pairs.append(("index.html", "/"))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def rewrite_file(path: Path, url_pairs: list[tuple[str, str]]) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    original = text

    for prefix in ("../../../rw_common/", "../../rw_common/", "../rw_common/", "rw_common/"):
        text = text.replace(prefix, "/assets/theme/")

    for old, new in sorted(asset_map.items(), key=lambda x: len(x[0]), reverse=True):
        if old == new.lstrip("/"):
            continue
        for pattern in (old, f"../{old}", f"../../{old}", f"../../../{old}"):
            if pattern in text:
                text = text.replace(pattern, new)
                text = text.replace(f"url({pattern})", f"url({new})")
                text = text.replace(f"url('{pattern}')", f"url('{new}')")
                text = text.replace(f'url("{pattern}")', f'url("{new}")')

    for old, new in url_pairs:
        text = text.replace(f'href="{old}"', f'href="{new}"')
        text = text.replace(f"href='{old}'", f"href='{new}'")
        text = text.replace(f'src="{old}"', f'src="{new}"')
        text = text.replace(f"src='{old}'", f"src='{new}'")
        text = text.replace(f'value="{old}"', f'value="{new}"')

    text = re.sub(r'href="\.\./index\.html"', 'href="/"', text)
    text = re.sub(r"href='\.\./index\.html'", "href='/'", text)
    text = re.sub(r'href="\.\./\.\./index\.html"', 'href="/"', text)
    text = re.sub(r'href="\.\./\.\./\.\./index\.html"', 'href="/"', text)
    text = re.sub(r'href="index\.html"', 'href="/"', text)

    if text != original:
        path.write_text(text, encoding="utf-8")


def rewrite_all(url_pairs: list[tuple[str, str]]) -> None:
    exts = {".html", ".css", ".js", ".php", ".xml"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("_archive/", ".git/", "scripts/", "php/")):
            continue
        if path.suffix.lower() in exts:
            rewrite_file(path, url_pairs)


def fix_php_paths() -> None:
    for php_file in (ROOT / "php").rglob("*.php"):
        text = php_file.read_text(encoding="utf-8", errors="replace")
        text = text.replace("require_once 'files/ydss_formloomjr.php'", "require_once 'ydss_formloomjr.php'")
        text = text.replace('require_once "files/ydss_formloomjr.php"', 'require_once "ydss_formloomjr.php"')
        text = text.replace("./files/mailer.php", "mailer.php")
        text = text.replace("Location:../page3.php", "Location:/php/page3/page3.php")
        text = text.replace("Location: ../page3.php", "Location: /php/page3/page3.php")
        text = text.replace("Location:../page26.php", "Location:/php/page26/page26.php")
        text = text.replace("Location: ../page26.php", "Location: /php/page26/page26.php")
        php_file.write_text(text, encoding="utf-8")


def write_redirects(url_pairs: list[tuple[str, str]]) -> None:
    existing = (ROOT / "_redirects").read_text(encoding="utf-8") if (ROOT / "_redirects").exists() else ""
    lines = [existing.rstrip(), "", "# Current site restructure (pageXX -> semantic paths)"]
    seen = set()
    for old, new in url_pairs:
        if old in seen or old == "index.html":
            continue
        if not old.endswith((".html", ".php")):
            continue
        seen.add(old)
        lines.append(f"/{old}  {new}  301")
    # update legacy redirect destinations in existing file
    updated = "\n".join(lines) + "\n"
    for old, new in url_pairs:
        if old.endswith(".html") and old.startswith("page1"):
            pass
    # rewrite old _redirects targets to new paths
    replacements = {f"/{old}": new for old, new in url_pairs if "/" not in old[:-5]}
    content = (ROOT / "_redirects").read_text(encoding="utf-8")
    for old_target, new_dest in [
        ("/page29/page29.html", "/videos/deming/01/"),
        ("/page30/page30.html", "/videos/deming/02/"),
        ("/page31/page31.html", "/videos/deming/03/"),
        ("/page32/page32.html", "/videos/deming/04/"),
        ("/page33/page33.html", "/videos/deming/05/"),
        ("/page34/page34.html", "/videos/deming/06/"),
        ("/page35/page35.html", "/videos/deming/07/"),
        ("/page36/page36.html", "/videos/deming/08/"),
        ("/page38/page38.html", "/videos/deming/09/"),
        ("/page39/page39.html", "/videos/deming/10/"),
        ("/page37/page37.html", "/videos/deming/11/"),
        ("/page40/page40.html", "/videos/petersen/01/"),
        ("/page41/page41.html", "/videos/petersen/02/"),
        ("/page48/page48.html", "/videos/petersen/03/"),
        ("/page49/page49.html", "/videos/petersen/04/"),
        ("/page46/page46.html", "/videos/kearns/"),
        ("/page47/page47.html", "/videos/stempel/"),
        ("/page43/page43.html", "/contact/"),
        ("/page28/page28.html", "/deming-of-america/"),
        ("/page27/page27.html", "/deming/"),
        ("/page26/page26.html", "/about/"),
        ("/page42/page42.html", "/quotes/"),
        ("/page42/page24/page24.html", "/quotes/artzt/"),
        ("/page42/page45/page45.html", "/quotes/gale/"),
        ("/page26/buy-dvd.html", "/buy-dvd/"),
        ("/index.html", "/"),
    ]:
        content = content.replace(f"  {old_target}  ", f"  {new_dest}  ")
    new_rules = []
    for old, new in url_pairs:
        if old.endswith(".html") and not old.startswith("../"):
            rule = f"/{old}  {new}  301"
            if rule not in content:
                new_rules.append(rule)
    (ROOT / "_redirects").write_text(content.rstrip() + "\n\n# Semantic path redirects\n" + "\n".join(new_rules) + "\n", encoding="utf-8")


def cleanup_old_dirs() -> None:
    remove_dirs = []
    for p in ROOT.iterdir():
        if p.is_dir() and re.match(r"page\d+", p.name):
            remove_dirs.append(p)
    for d in sorted(remove_dirs, key=lambda x: len(x.as_posix()), reverse=True):
        if d.exists():
            shutil.rmtree(d)
    for name in ("files",):
        p = ROOT / name
        if p.exists() and p.is_dir():
            shutil.rmtree(p)


def main() -> None:
    print("Moving theme...")
    move_theme()
    print("Moving root files...")
    move_root_files()

    seen_sections: set[str] = set()
    for old, new, section in PAGES:
        page_dir = str(Path(old).parent)
        if page_dir == ".":
            continue
        key = page_dir
        if key not in seen_sections:
            move_page_dir_assets(page_dir, section)
            seen_sections.add(key)
        # nested page dirs
        if "/" in page_dir:
            move_page_dir_assets(page_dir, section)

    # per-page top-level dirs
    for page_dir, section in [
        ("page16", "sitemap"),
        ("page21", "have-your-say"),
        ("page22", "special-reports"),
        ("page23", "links"),
        ("page26", "about"),
        ("page27", "deming"),
        ("page28", "deming-of-america"),
        ("page43", "contact"),
        ("page50", "thoughts"),
        ("page50/page51", "thoughts-part-2"),
        ("page42", "quotes"),
        ("page42/page45", "quotes-gale"),
    ]:
        if (ROOT / page_dir).exists():
            move_page_dir_assets(page_dir, section)

    for old, _, section in PAGES:
        pd = str(Path(old).parent)
        if (ROOT / pd / "files").exists() or (ROOT / pd / "assets").exists():
            move_page_dir_assets(pd, section)

    print("Moving HTML pages...")
    move_html_pages()
    print("Moving PHP...")
    move_php()

    url_pairs = build_url_map()
    print("Rewriting links...")
    rewrite_all(url_pairs)
    fix_php_paths()
    print("Writing redirects...")
    write_redirects(url_pairs)
    print("Cleaning up old dirs...")
    cleanup_old_dirs()
    print("Done.")


if __name__ == "__main__":
    main()
