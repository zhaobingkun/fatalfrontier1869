#!/usr/bin/env python3
"""Idempotently fill social meta tags from each page's existing SEO metadata."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FALLBACK_IMAGE = "https://fatalfrontier1869.wiki/assets/og-card.svg"
OLD_DOWNLOAD = "https://pdg-prod-cdn-gngbazgkbqcza6fg.z01.azurefd.net/"
OFFICIAL_DOWNLOAD = "https://www.fatalfrontier.com/lpdownload"
ASSET_VERSION = "20260827b"
TEXT_REPLACEMENTS = {
    "How to Extract in Fatal Frontier 1869 — Steamer &amp; Signal Fire":
        "Fatal Frontier 1869 Extraction — Steamer &amp; Signal Fire",
    "Track Fatal Frontier 1869 Early Access updates, new Pioneers, economy changes, points of interest and gameplay fixes.":
        "Track Fatal Frontier 1869 Early Access updates, new Pioneers, economy changes, points of interest, gameplay fixes and guide revisions.",
}


def capture(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def insert_after(text: str, pattern: str, tags: list[str]) -> str:
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return text
    following_newline = text[match.end() :].startswith("\n")
    line_start = text.rfind("\n", 0, match.start()) + 1
    indent = re.match(r"[ \t]*", text[line_start : match.start()]).group(0)
    separator = "\n" + indent if following_newline else ""
    addition = separator + separator.join(tags)
    return text[: match.end()] + addition + text[match.end() :]


changed = 0
for path in sorted(ROOT.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    before = text
    text = text.replace(OLD_DOWNLOAD, OFFICIAL_DOWNLOAD)
    text = re.sub(r'href="/styles\.css(?:\?v=[^"]+)?"', f'href="/styles.css?v={ASSET_VERSION}"', text)
    text = re.sub(r'src="/script\.js(?:\?v=[^"]+)?"', f'src="/script.js?v={ASSET_VERSION}"', text)
    if path.name == "404.html":
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed += 1
        continue
    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)

    title = capture(r"<title>(.*?)</title>", text)
    description = capture(r'<meta\s+name="description"\s+content="([^"]*)"', text)
    og_image = capture(r'<meta\s+property="og:image"\s+content="([^"]*)"', text)

    if not og_image:
        text = insert_after(
            text,
            r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>',
            [f'<meta property="og:image" content="{FALLBACK_IMAGE}">'],
        )
        og_image = FALLBACK_IMAGE

    twitter_tags: list[str] = []
    if 'name="twitter:title"' not in text:
        twitter_tags.append(f'<meta name="twitter:title" content="{title}">')
    if 'name="twitter:description"' not in text:
        twitter_tags.append(f'<meta name="twitter:description" content="{description}">')
    if 'name="twitter:image"' not in text:
        twitter_tags.append(f'<meta name="twitter:image" content="{og_image}">')
    if twitter_tags:
        text = insert_after(
            text,
            r'<meta\s+name="twitter:card"\s+content="[^"]*"\s*/?>',
            twitter_tags,
        )

    if text != before:
        path.write_text(text, encoding="utf-8")
        changed += 1

print(f"Normalized {changed} HTML files")
