#!/usr/bin/env python3
"""Apply in-repo technical SEO updates to live RapidWeaver pages.

Preserves visual design by keeping existing IDs/classes and using
visually-hidden topical headings where converting spans would risk layout drift.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "https://www.priscillapetty.com"
DEFAULT_OG_IMAGE = f"{HOST}/assets/images/home/stacks_image_4_1.png"

# path -> SEO fields
PAGES: dict[str, dict] = {
    "/": {
        "file": "index.html",
        "title": "Priscilla Petty | The Deming of America &amp; Quality Leadership",
        "description": (
            "Priscilla Petty is producer and on-camera interviewer for The Deming of America, "
            "sharing W. Edwards Deming’s management philosophy through video, writing, and consulting."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Priscilla Petty — The Deming of America",
        "schema": "home",
        "breadcrumbs": [("Home", "/")],
    },
    "/about/": {
        "file": "about/index.html",
        "title": "About Priscilla Petty | Writer, Interviewer & Deming Consultant",
        "description": (
            "Learn about Priscilla Petty’s career advising leaders, interviewing executives, "
            "and producing The Deming of America with W. Edwards Deming."
        ),
        "og_type": "profile",
        "og_image": f"{HOST}/assets/images/about/stacks_image_48_1.png",
        "h1": "About Priscilla Petty",
        "schema": "article",
        "breadcrumbs": [("Home", "/"), ("About Priscilla Petty", "/about/")],
    },
    "/buy-dvd/": {
        "file": "buy-dvd/index.html",
        "title": "Buy The Deming of America DVD | Petty Consulting Productions",
        "description": (
            "Order The Deming of America DVD—Priscilla Petty’s Public Television program and "
            "business training video featuring W. Edwards Deming and corporate leaders."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Buy The Deming of America DVD",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Buy Deming of America DVD", "/buy-dvd/")],
    },
    "/contact/": {
        "file": "contact/index.html",
        "title": "Contact Priscilla Petty | Petty Consulting Productions",
        "description": (
            "Contact Priscilla Petty and Petty Consulting Productions in Nashville, Tennessee "
            "for Deming-related consulting, media, and The Deming of America inquiries."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Contact Priscilla Petty",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Contact Priscilla Petty", "/contact/")],
    },
    "/deming/": {
        "file": "deming/index.html",
        "title": "W. Edwards Deming | Philosophy, Quality & Leadership",
        "description": (
            "Explore W. Edwards Deming’s principles of management and philosophy of quality, "
            "presented by Priscilla Petty through video clips and commentary."
        ),
        "og_type": "article",
        "og_image": f"{HOST}/assets/images/deming/stacks_image_62_1.png",
        "h1": "W. Edwards Deming",
        "schema": "article",
        "breadcrumbs": [("Home", "/"), ("W. Edwards Deming", "/deming/")],
    },
    "/deming-of-america/": {
        "file": "deming-of-america/index.html",
        "title": "The Deming of America | Public Television & Business Training Video",
        "description": (
            "About The Deming of America—Priscilla Petty’s Public Television program and "
            "business training video featuring Dr. Deming and major corporate CEOs."
        ),
        "og_type": "article",
        "og_image": f"{HOST}/assets/images/deming-of-america/stacks_image_107_1.png",
        "h1": "The Deming of America",
        "schema": "article",
        "breadcrumbs": [("Home", "/"), ("The Deming of America", "/deming-of-america/")],
    },
    "/have-your-say/": {
        "file": "have-your-say/index.html",
        "title": "Have Your Say | Priscilla Petty Reader Responses",
        "description": (
            "Share thoughts and responses with Priscilla Petty on Deming, quality management, "
            "leadership, and The Deming of America."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Have Your Say",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Have Your Say", "/have-your-say/")],
    },
    "/links/": {
        "file": "links/index.html",
        "title": "Links | Deming, Quality & Leadership Resources",
        "description": (
            "Curated links related to W. Edwards Deming, quality management, and resources "
            "recommended by Priscilla Petty."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Links",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Links", "/links/")],
    },
    "/quotes/": {
        "file": "quotes/index.html",
        "title": "Quotes: P&G Leaders | Edwin L. Artzt & Oliver M. Gale",
        "description": (
            "Read quotes from Procter & Gamble leaders Edwin L. Artzt and Oliver M. Gale, "
            "interviewed and presented by Priscilla Petty."
        ),
        "og_type": "article",
        "og_image": f"{HOST}/assets/images/quotes/stacks_image_152_1.png",
        "h1": "Quotes: P&G Leaders",
        "schema": "article",
        "breadcrumbs": [("Home", "/"), ("Quotes: P&G Leaders", "/quotes/")],
    },
    "/quotes/artzt/": {
        "file": "quotes/artzt/index.html",
        "title": "Edwin L. Artzt Quotes | Procter & Gamble Leadership",
        "description": (
            "Quotes and insights from Edwin L. Artzt, former Procter & Gamble CEO, "
            "presented by Priscilla Petty."
        ),
        "og_type": "article",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Edwin L. Artzt",
        "schema": "article",
        "breadcrumbs": [
            ("Home", "/"),
            ("Quotes: P&G Leaders", "/quotes/"),
            ("Edwin L. Artzt", "/quotes/artzt/"),
        ],
    },
    "/quotes/gale/": {
        "file": "quotes/gale/index.html",
        "title": "Oliver M. Gale Quotes | Procter & Gamble Leadership",
        "description": (
            "Quotes and insights from Oliver M. “Muff” Gale of Procter & Gamble, "
            "presented by Priscilla Petty."
        ),
        "og_type": "article",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Oliver M. Gale",
        "schema": "article",
        "breadcrumbs": [
            ("Home", "/"),
            ("Quotes: P&G Leaders", "/quotes/"),
            ("Oliver M. Gale", "/quotes/gale/"),
        ],
    },
    "/sitemap/": {
        "file": "sitemap/index.html",
        "title": "Site Map | Priscilla Petty Website",
        "description": (
            "Browse the full site map for PriscillaPetty.com—pages on Deming, The Deming of America, "
            "videos, quotes, thoughts, and contact information."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Site Map",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Site Map", "/sitemap/")],
    },
    "/special-reports/": {
        "file": "special-reports/index.html",
        "title": "Special Reports | Priscilla Petty",
        "description": (
            "Special reports and featured writing from Priscilla Petty on leadership, "
            "quality, and Deming-related topics."
        ),
        "og_type": "website",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Special Reports",
        "schema": "webpage",
        "breadcrumbs": [("Home", "/"), ("Special Reports", "/special-reports/")],
    },
    "/thoughts/": {
        "file": "thoughts/index.html",
        "title": "Priscilla's Thoughts | Deming & Leadership Reflections",
        "description": (
            "Essays and reflections from Priscilla Petty on W. Edwards Deming, quality management, "
            "and what “doing Deming” means for leaders."
        ),
        "og_type": "article",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Priscilla's Thoughts",
        "schema": "article",
        "breadcrumbs": [("Home", "/"), ("Priscilla's Thoughts", "/thoughts/")],
    },
    "/thoughts/part-2/": {
        "file": "thoughts/part-2/index.html",
        "title": "What \"Doing Deming\" Means | Priscilla Petty",
        "description": (
            "Priscilla Petty explains what “doing Deming” means for organizations—systems thinking, "
            "quality, and leadership beyond slogans."
        ),
        "og_type": "article",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "What \"Doing Deming\" Means",
        "schema": "article",
        "breadcrumbs": [
            ("Home", "/"),
            ("Priscilla's Thoughts", "/thoughts/"),
            ("What \"Doing Deming\" Means", "/thoughts/part-2/"),
        ],
    },
}

DEMING_CLIPS = {
    "01": ("Adversarial competition is not the answer", "1_Deming_adv-comp"),
    "02": ("Defend your rights, you lose", "2_Deming_defend_rights"),
    "03": ("Banks do not fail because of mistakes at the teller's window", "3_Deming_why_banks_fail"),
    "04": ("Everybody doing their best is not the answer", "4_Deming_everybdy_doing_their_best"),
    "05": ("How could they know?", "5_Deming_how_could_they_know"),
    "06": ("Management's job", "6_Deming_managements_job"),
    "07": ("Deming's second theorem", "7_Demings_second_theorem"),
    "08": ("Example without theory", "8_Deming_example_without_theory"),
    "09": ("Managing by results", "9_Deming_managing_by_results"),
    "10": ("Orchestra as an example of optimization", "10_Deming_orchestra_ex_of_optimization"),
    "11": ("The customer does not foresee his wants", "11_Deming_customer_does_not_foresee_his_wants 4"),
}

PETERSEN_CLIPS = {
    "01": ("People are the center", "Petersen1_people_are_the_center"),
    "02": ("Difficult times provide opportunity", "Petersen2_difficult_times_provide_opportunity"),
    "03": ("The golden rule", "Petersen3_golden_rule"),
    "04": ("Continual improvement", "Petersen4_continual_improvement"),
}


def add_video_pages() -> None:
    for num, (clip, stem) in DEMING_CLIPS.items():
        path = f"/videos/deming/{num}/"
        poster = f"{HOST}/assets/images/video-posters/deming/{stem.replace(' ', '%20')}.jpg"
        # fix poster 11 encoding
        if num == "11":
            poster = f"{HOST}/assets/images/video-posters/deming/11_Deming_customer_does_not_foresee_his_wants%204.jpg"
            media = "https://media.priscillapetty.com/videos/deming/11_Deming_customer_does_not_foresee_his_wants%204.mp4"
        else:
            media = f"https://media.priscillapetty.com/videos/deming/{stem}.mp4"
        PAGES[path] = {
            "file": f"videos/deming/{num}/index.html",
            "title": f"Deming Video {int(num)}: {clip} | Priscilla Petty",
            "description": (
                f"Watch Deming video clip {int(num)} from The Deming of America: “{clip}.” "
                "Produced and presented by Priscilla Petty."
            ),
            "og_type": "video.other",
            "og_image": poster,
            "h1": f"Deming Video {int(num)}: {clip}",
            "schema": "video",
            "video_name": f"Deming Video {int(num)}: {clip}",
            "video_url": media,
            "video_poster": poster,
            "breadcrumbs": [
                ("Home", "/"),
                ("W. Edwards Deming", "/deming/"),
                (f"Deming Video {int(num)}", path),
            ],
        }

    for num, (clip, stem) in PETERSEN_CLIPS.items():
        path = f"/videos/petersen/{num}/"
        # discover actual poster/media from file if needed
        PAGES[path] = {
            "file": f"videos/petersen/{num}/index.html",
            "title": f"Don Petersen Video {int(num)}: {clip} | Priscilla Petty",
            "description": (
                f"Watch Don Petersen video clip {int(num)}: “{clip},” from Priscilla Petty’s "
                "Deming of America interview series."
            ),
            "og_type": "video.other",
            "og_image": DEFAULT_OG_IMAGE,
            "h1": f"Don Petersen Video {int(num)}: {clip}",
            "schema": "video",
            "video_name": f"Don Petersen Video {int(num)}: {clip}",
            "video_url": "",
            "video_poster": "",
            "breadcrumbs": [
                ("Home", "/"),
                (f"Don Petersen Video {int(num)}", path),
            ],
        }

    PAGES["/videos/kearns/"] = {
        "file": "videos/kearns/index.html",
        "title": "David Kearns Video | The Deming of America Interviews",
        "description": (
            "Watch David Kearns discuss quality and leadership in Priscilla Petty’s "
            "Deming of America interview series."
        ),
        "og_type": "video.other",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "David Kearns Video",
        "schema": "video",
        "video_name": "David Kearns Video",
        "video_url": "",
        "video_poster": "",
        "breadcrumbs": [("Home", "/"), ("David Kearns Video", "/videos/kearns/")],
    }
    PAGES["/videos/stempel/"] = {
        "file": "videos/stempel/index.html",
        "title": "Bob Stempel Video | The Deming of America Interviews",
        "description": (
            "Watch Bob Stempel discuss quality and leadership in Priscilla Petty’s "
            "Deming of America interview series."
        ),
        "og_type": "video.other",
        "og_image": DEFAULT_OG_IMAGE,
        "h1": "Bob Stempel Video",
        "schema": "video",
        "video_name": "Bob Stempel Video",
        "video_url": "",
        "video_poster": "",
        "breadcrumbs": [("Home", "/"), ("Bob Stempel Video", "/videos/stempel/")],
    }


def fill_video_media_from_html(meta: dict, html: str) -> None:
    if meta.get("schema") != "video":
        return
    src = re.search(r'<source[^>]+src="([^"]+\.mp4)"', html)
    poster = re.search(r'poster="([^"]+)"', html)
    if src:
        meta["video_url"] = src.group(1)
    if poster:
        p = poster.group(1)
        meta["video_poster"] = p if p.startswith("http") else f"{HOST}{p}"
        meta["og_image"] = meta["video_poster"]


ORG = {
    "@type": "Organization",
    "@id": f"{HOST}/#organization",
    "name": "Petty Consulting Productions",
    "url": HOST,
    "email": "Priscilla@PriscillaPetty.com",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Nashville",
        "addressRegion": "TN",
        "addressCountry": "US",
    },
}

PERSON = {
    "@type": "Person",
    "@id": f"{HOST}/#person",
    "name": "Priscilla Petty",
    "url": f"{HOST}/about/",
    "email": "Priscilla@PriscillaPetty.com",
    "jobTitle": "Writer, interviewer, and consultant",
    "worksFor": {"@id": f"{HOST}/#organization"},
    "homeLocation": {
        "@type": "Place",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Nashville",
            "addressRegion": "TN",
            "addressCountry": "US",
        },
    },
}


def build_jsonld(url: str, meta: dict) -> list:
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": f"{HOST}{path}" if path != "/" else HOST + "/",
            }
            for i, (name, path) in enumerate(meta["breadcrumbs"])
        ],
    }
    graph: list = [ORG, PERSON, crumbs]

    if meta["schema"] == "home":
        graph.append(
            {
                "@type": "WebSite",
                "@id": f"{HOST}/#website",
                "url": HOST + "/",
                "name": "Priscilla Petty",
                "publisher": {"@id": f"{HOST}/#organization"},
                "author": {"@id": f"{HOST}/#person"},
            }
        )
    elif meta["schema"] == "article":
        graph.append(
            {
                "@type": "Article",
                "headline": meta["h1"],
                "description": meta["description"],
                "author": {"@id": f"{HOST}/#person"},
                "publisher": {"@id": f"{HOST}/#organization"},
                "mainEntityOfPage": f"{HOST}{url}",
                "image": meta.get("og_image", DEFAULT_OG_IMAGE),
            }
        )
    elif meta["schema"] == "video":
        vo = {
            "@type": "VideoObject",
            "name": meta.get("video_name", meta["h1"]),
            "description": meta["description"],
            "thumbnailUrl": meta.get("video_poster") or meta.get("og_image"),
            "uploadDate": "2009-01-01",
            "author": {"@id": f"{HOST}/#person"},
            "publisher": {"@id": f"{HOST}/#organization"},
        }
        if meta.get("video_url"):
            vo["contentUrl"] = meta["video_url"]
            vo["embedUrl"] = f"{HOST}{url}"
        graph.append(vo)
    else:
        graph.append(
            {
                "@type": "WebPage",
                "name": meta["h1"],
                "description": meta["description"],
                "url": f"{HOST}{url}",
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            }
        )
    return graph


def build_head_block(url: str, meta: dict) -> str:
    canonical = HOST + (url if url != "/" else "/")
    og_image = meta.get("og_image", DEFAULT_OG_IMAGE)
    title = meta["title"]
    desc = meta["description"]
    lines = [
        f'  <title>{title}</title>',
        f'  <meta name="description" content="{xml_escape(desc)}" />',
        f'  <link rel="canonical" href="{canonical}" />',
        f'  <meta property="og:site_name" content="Priscilla Petty" />',
        f'  <meta property="og:type" content="{meta.get("og_type", "website")}" />',
        f'  <meta property="og:title" content="{xml_escape(title)}" />',
        f'  <meta property="og:description" content="{xml_escape(desc)}" />',
        f'  <meta property="og:url" content="{canonical}" />',
        f'  <meta property="og:image" content="{og_image}" />',
        f'  <meta name="twitter:card" content="summary_large_image" />',
        f'  <meta name="twitter:title" content="{xml_escape(title)}" />',
        f'  <meta name="twitter:description" content="{xml_escape(desc)}" />',
        f'  <meta name="twitter:image" content="{og_image}" />',
    ]
    return "\n".join(lines)


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def replace_title_and_inject_meta(html: str, url: str, meta: dict) -> str:
    # Remove prior SEO injections if re-run
    html = re.sub(
        r'\n?  <!-- SEO:meta -->.*?<!-- /SEO:meta -->\n?',
        "\n",
        html,
        flags=re.S,
    )
    html = re.sub(
        r'\n?  <!-- SEO:jsonld -->.*?<!-- /SEO:jsonld -->\n?',
        "\n",
        html,
        flags=re.S,
    )
    # Replace title tag
    html = re.sub(
        r"<title>.*?</title>",
        build_head_block(url, meta),
        html,
        count=1,
        flags=re.S,
    )
    # Remove duplicate description if any leftover from partial runs
    # (title replacement already embeds description once)

    graph = build_jsonld(url, meta)
    payload = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    jsonld = json.dumps(payload, ensure_ascii=False, indent=2)
    script = (
        '  <!-- SEO:jsonld -->\n'
        '  <script type="application/ld+json">\n'
        f"{jsonld}\n"
        "  </script>\n"
        "  <!-- /SEO:jsonld -->\n"
    )
    if "</head>" not in html:
        raise RuntimeError(f"No </head> in {url}")
    html = html.replace("</head>", script + "</head>", 1)
    return html


def apply_landmarks(html: str, meta: dict) -> str:
    # Skip link once
    if 'class="skip-link"' not in html:
        html = html.replace(
            "<body>",
            '<body>\n  <a class="skip-link" href="#content">Skip to main content</a>',
            1,
        )

    html = html.replace(
        '<div id="navcontainer">',
        '<nav id="navcontainer" aria-label="Primary">',
        1,
    )
    html = html.replace("</div><!-- End navigation -->", "</nav><!-- End navigation -->", 1)

    html = html.replace(
        '<div id="pageHeader">',
        '<header id="pageHeader">',
        1,
    )
    html = html.replace("</div><!-- End page header -->", "</header><!-- End page header -->", 1)

    html = html.replace(
        '<div id="contentContainer">',
        '<main id="contentContainer">',
        1,
    )
    html = re.sub(
        r"</div>\s*<!-- End main content wrapper -->",
        "</main><!-- End main content wrapper -->",
        html,
        count=1,
    )

    html = html.replace(
        '<div id="breadcrumbcontainer">',
        '<nav id="breadcrumbcontainer" aria-label="Breadcrumb">',
        1,
    )
    html = html.replace("</div><!-- End breadcrumb -->", "</nav><!-- End breadcrumb -->", 1)

    html = html.replace('<div id="footer">', '<footer id="footer">', 1)
    html = html.replace("</div><!-- End Footer -->", "</footer><!-- End Footer -->", 1)

    # Empty sidebar h1
    html = re.sub(
        r'<h1 class="sideHeader"></h1>',
        '<div class="sideHeader"></div>',
        html,
    )

    # Brand h1 -> p.site-brand
    html = re.sub(
        r"<h1>PriscillaPetty\.com</h1>",
        '<p class="site-brand">PriscillaPetty.com</p>',
        html,
    )

    # Topical visually-hidden h1 inside #content
    if 'class="visually-hidden"' not in html:
        hidden = f'<h1 class="visually-hidden">{xml_escape(meta["h1"])}</h1>\n        '
        html = re.sub(
            r'(<div id="content">\s*<!-- Start content -->\s*)',
            r"\1" + hidden,
            html,
            count=1,
        )

    return html


def add_buy_dvd_nav(html: str) -> str:
    if 'href="/buy-dvd/"' in html and "Buy Deming of America DVD" in html:
        return html
    needle = """        <li><a href="/deming-of-america/"
           rel="self">The Deming of America</a></li>

        <li><a href="/contact/"
           rel="self">Contact Priscilla Petty</a></li>"""
    insert = """        <li><a href="/deming-of-america/"
           rel="self">The Deming of America</a></li>

        <li><a href="/buy-dvd/"
           rel="self">Buy Deming of America DVD</a></li>

        <li><a href="/contact/"
           rel="self">Contact Priscilla Petty</a></li>"""
    if needle in html:
        return html.replace(needle, insert, 1)
    # looser fallback
    if 'href="/buy-dvd/"' not in html:
        html = html.replace(
            '<li><a href="/contact/"\n           rel="self">Contact Priscilla Petty</a></li>',
            '<li><a href="/buy-dvd/"\n           rel="self">Buy Deming of America DVD</a></li>\n\n'
            '        <li><a href="/contact/"\n           rel="self">Contact Priscilla Petty</a></li>',
            1,
        )
    return html


def mark_buy_dvd_current(html: str, url: str) -> str:
    if url != "/buy-dvd/":
        return html
    html = re.sub(
        r'(<a href="/buy-dvd/"\s+rel="self")(>)',
        r'\1 id="current" name="current"\2',
        html,
        count=1,
    )
    return html


IMG_ALTS = {
    "/assets/images/home/stacks_image_4_1.png": "Portrait of Priscilla Petty",
    "/assets/images/about/stacks_image_48_1.png": "Portrait of Priscilla Petty",
    "/assets/images/quotes/stacks_image_152_1.png": "Portrait related to P&G leadership quotes",
}


def optimize_images_in_html(html: str, is_home: bool) -> str:
    def repl_img(match: re.Match) -> str:
        tag = match.group(0)
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        alt = IMG_ALTS.get(src)
        if not alt:
            # deming images
            if "/deming/" in src:
                alt = "Image from W. Edwards Deming and The Deming of America"
            elif "/deming-of-america/" in src:
                alt = "Image from The Deming of America program"
            elif "stacks_image" in (re.search(r'alt="([^"]*)"', tag) or [""])[0]:
                alt = "Illustration from Priscilla Petty website"
            else:
                alt_m = re.search(r'alt="([^"]*)"', tag)
                alt = alt_m.group(1) if alt_m else "Priscilla Petty website image"

        # update alt (may be multiline)
        tag = re.sub(
            r'alt=\s*"[^"]*"',
            f'alt="{alt}"',
            tag,
            count=1,
        )

        eager = is_home and "home/stacks_image_4_1.png" in src
        if "loading=" not in tag:
            if eager:
                tag = tag.replace("<img ", '<img loading="eager" decoding="async" ', 1)
            else:
                tag = tag.replace("<img ", '<img loading="lazy" decoding="async" ', 1)

        # picture/webp wrap if webp exists
        if src.startswith("/") and not src.endswith(".webp"):
            webp_rel = src[1:]
            webp_path = ROOT / Path(webp_rel).with_suffix(".webp")
            # also try replacing extension
            if not webp_path.exists():
                webp_path = ROOT / (webp_rel.rsplit(".", 1)[0] + ".webp")
            if webp_path.exists():
                webp_src = "/" + str(webp_path.relative_to(ROOT)).replace("\\", "/")
                # Avoid double-wrapping
                return (
                    f'<picture><source srcset="{webp_src}" type="image/webp" />'
                    f"{tag}</picture>"
                )
        return tag

    # Only replace raw img not already inside picture
    parts = []
    last = 0
    for m in re.finditer(r"<img\b[^>]*>", html, flags=re.I | re.S):
        # check if already in picture by looking back
        start = m.start()
        preceding = html[max(0, start - 80) : start]
        parts.append(html[last:start])
        if "<picture" in preceding and "</picture>" not in preceding:
            parts.append(m.group(0))
        else:
            parts.append(repl_img(m))
        last = m.end()
    parts.append(html[last:])
    return "".join(parts)


def add_home_internal_links(html: str, url: str) -> str:
    if url != "/":
        return html
    if "<!-- SEO:related -->" in html:
        return html
    block = """
              <!-- SEO:related -->
              <p style="text-align:center;"><span style="font:15px Georgia, serif;">
              Learn more: <a href="/about/" rel="self">About Priscilla Petty</a> ·
              <a href="/deming/" rel="self">W. Edwards Deming</a> ·
              <a href="/deming-of-america/" rel="self">The Deming of America</a> ·
              <a href="/buy-dvd/" rel="self">Buy the DVD</a> ·
              <a href="/videos/deming/01/" rel="self">Watch Deming videos</a>
              </span></p>
              <!-- /SEO:related -->
"""
    # Insert before breadcrumb / end of content
    html = re.sub(
        r'(</div>\s*<!-- End content -->)',
        block + r"\1",
        html,
        count=1,
    )
    return html


def add_thoughts_link(html: str, url: str) -> str:
    if url != "/thoughts/":
        return html
    if 'href="/thoughts/part-2/"' in html and "What" in html:
        return html
    # ensure a clear text link exists; many pages already link — skip if present
    return html


def add_deming_cross_links(html: str, url: str) -> str:
    if url != "/deming/":
        return html
    if "<!-- SEO:related -->" in html:
        return html
    block = """
              <!-- SEO:related -->
              <p><span style="font:15px Georgia, serif;">
              Related: <a href="/deming-of-america/" rel="self">The Deming of America</a> ·
              <a href="/videos/deming/01/" rel="self">Deming video clips</a> ·
              <a href="/buy-dvd/" rel="self">Buy the DVD</a>
              </span></p>
              <!-- /SEO:related -->
"""
    html = re.sub(
        r"(</div>\s*<!-- End content -->)",
        block + r"\1",
        html,
        count=1,
    )
    return html


def add_doa_cross_links(html: str, url: str) -> str:
    if url != "/deming-of-america/":
        return html
    if "<!-- SEO:related -->" in html:
        return html
    block = """
              <!-- SEO:related -->
              <p><span style="font:15px Georgia, serif;">
              Related: <a href="/deming/" rel="self">W. Edwards Deming</a> ·
              <a href="/videos/deming/01/" rel="self">Deming video clips</a> ·
              <a href="/buy-dvd/" rel="self">Buy the DVD</a>
              </span></p>
              <!-- /SEO:related -->
"""
    html = re.sub(
        r"(</div>\s*<!-- End content -->)",
        block + r"\1",
        html,
        count=1,
    )
    return html


def process_page(url: str, meta: dict) -> None:
    path = ROOT / meta["file"]
    html = path.read_text(encoding="utf-8", errors="replace")
    fill_video_media_from_html(meta, html)
    html = replace_title_and_inject_meta(html, url, meta)
    html = apply_landmarks(html, meta)
    html = add_buy_dvd_nav(html)
    html = mark_buy_dvd_current(html, url)
    html = optimize_images_in_html(html, is_home=(url == "/"))
    html = add_home_internal_links(html, url)
    html = add_deming_cross_links(html, url)
    html = add_doa_cross_links(html, url)
    path.write_text(html, encoding="utf-8")
    print(f"updated {meta['file']}")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        """User-agent: *
Allow: /

Disallow: /_archive/
Disallow: /archive-viewer/
Disallow: /scripts/
Disallow: /r2-upload/
Disallow: /assets/pages/sitemap/sitemap.xml

Sitemap: https://www.priscillapetty.com/sitemap.xml
""",
        encoding="utf-8",
    )
    print("wrote robots.txt")


def write_sitemap() -> None:
    urls = sorted(PAGES.keys(), key=lambda u: (u != "/", u))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        loc = HOST + (url if url != "/" else "/")
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    # neutralize duplicate stale sitemap
    dup = ROOT / "assets/pages/sitemap/sitemap.xml"
    if dup.exists():
        dup.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<!-- Deprecated duplicate. See /sitemap.xml -->\n"
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n',
            encoding="utf-8",
        )
    print("wrote sitemap.xml")


def write_headers() -> None:
    (ROOT / "_headers").write_text(
        """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""",
        encoding="utf-8",
    )
    print("wrote _headers")


def generate_webp() -> None:
    # Content images referenced by live pages + posters
    patterns = [
        "assets/images/home/*.{png,jpg,jpeg}",
        "assets/images/about/*.{png,jpg,jpeg}",
        "assets/images/deming/*.{png,jpg,jpeg}",
        "assets/images/deming-of-america/*.{png,jpg,jpeg}",
        "assets/images/quotes/*.{png,jpg,jpeg}",
        "assets/images/video-posters/**/*.{png,jpg,jpeg}",
    ]
    files: list[Path] = []
    for folder in [
        ROOT / "assets/images/home",
        ROOT / "assets/images/about",
        ROOT / "assets/images/deming",
        ROOT / "assets/images/deming-of-america",
        ROOT / "assets/images/quotes",
        ROOT / "assets/images/video-posters",
    ]:
        if not folder.exists():
            continue
        for p in folder.rglob("*"):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                files.append(p)

    for src in files:
        dest = src.with_suffix(".webp")
        if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
            continue
        cmd = ["cwebp", "-quiet", "-q", "82", str(src), "-o", str(dest)]
        try:
            subprocess.run(cmd, check=True)
            print(f"webp {dest.relative_to(ROOT)}")
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            print(f"skip webp {src}: {exc}")


def patch_theme_css() -> None:
    css_path = ROOT / "assets/theme/themes/simplebusiness/styles.css"
    css = css_path.read_text(encoding="utf-8")
    if ".site-brand" not in css:
        css = css.replace(
            "#pageHeader h1 {",
            "#pageHeader h1,\n#pageHeader .site-brand {",
            1,
        )
        # site-brand paragraph reset
        if "margin: 10px 0 0px;" in css:
            pass
        css += """

/* SEO / accessibility helpers (no visual change in normal layout) */
#pageHeader .site-brand {
	display: block;
	margin: 10px 0 0px;
	padding: 0;
}

.visually-hidden {
	position: absolute !important;
	width: 1px !important;
	height: 1px !important;
	padding: 0 !important;
	margin: -1px !important;
	overflow: hidden !important;
	clip: rect(0, 0, 0, 0) !important;
	white-space: nowrap !important;
	border: 0 !important;
}

.skip-link {
	position: absolute;
	left: -9999px;
	top: 0;
	z-index: 10000;
	padding: 8px 12px;
	background: #21536a;
	color: #ffffff;
	text-decoration: none;
	font-weight: bold;
}

.skip-link:focus,
.skip-link:focus-visible {
	left: 8px;
	top: 8px;
}

footer#footer,
nav#navcontainer,
nav#breadcrumbcontainer,
header#pageHeader,
main#contentContainer {
	/* landmark tags keep existing IDs; ensure block layout like former divs */
	display: block;
}
"""
        css_path.write_text(css, encoding="utf-8")
        print("patched styles.css")
    else:
        print("styles.css already patched")


def main() -> None:
    add_video_pages()
    assert len(PAGES) == 32, f"expected 32 pages, got {len(PAGES)}"
    generate_webp()
    patch_theme_css()
    write_robots()
    write_sitemap()
    write_headers()
    for url, meta in PAGES.items():
        process_page(url, meta)
    print("done")


if __name__ == "__main__":
    main()
