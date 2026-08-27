#!/usr/bin/env python3
"""Read-only launch audit for the static Fatal Frontier 1869 Wiki."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://fatalfrontier1869.wiki"
GOOGLE_TAG_ID = "G-KMLT9384LR"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[list[str]] = []
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.json_ld: list[str] = []
        self.text_parts: list[str] = []
        self.lang = ""
        self._in_title = False
        self._in_h1 = False
        self._in_json_ld = False
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.lang = data.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
            self.h1_parts.append([])
        elif tag == "meta":
            self.meta.append(data)
        elif tag == "link" and "canonical" in data.get("rel", "").lower().split():
            self.canonicals.append(data.get("href", ""))
        elif tag == "a":
            self.links.append(data)
        elif tag == "img":
            self.images.append(data)
        elif tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_parts).strip())
            self._in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1 and self.h1_parts:
            self.h1_parts[-1].append(data)
        if self._in_json_ld:
            self._json_parts.append(data)
        if data.strip() and not self._in_json_ld:
            self.text_parts.append(data)


def meta_value(parser: PageParser, key: str, value: str) -> str:
    for item in parser.meta:
        if item.get(key, "").lower() == value.lower():
            return item.get("content", "").strip()
    return ""


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def local_target(source: Path, raw_url: str) -> Path | None:
    parsed = urlparse(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
    if path.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    pages: dict[Path, PageParser] = {}
    titles: dict[str, list[str]] = {}
    canonicals: dict[str, list[str]] = {}

    html_files = sorted(ROOT.rglob("*.html"))
    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(raw)
        pages[path] = parser

        robots = meta_value(parser, "name", "robots").lower()
        is_404 = rel == "404.html"
        indexable = "noindex" not in robots and not is_404
        title = " ".join("".join(parser.title_parts).split())
        description = meta_value(parser, "name", "description")

        if parser.lang.lower() != "en":
            errors.append(f"{rel}: html lang must be en")
        if not title:
            errors.append(f"{rel}: missing title")
        if not description:
            errors.append(f"{rel}: missing meta description")
        if len(parser.h1_parts) != 1:
            errors.append(f"{rel}: expected 1 H1, found {len(parser.h1_parts)}")
        if "1898" in raw or "localhost" in raw or "127.0.0.1" in raw:
            errors.append(f"{rel}: stale project name or local URL found")
        if raw.count(f"googletagmanager.com/gtag/js?id={GOOGLE_TAG_ID}") != 1:
            errors.append(f"{rel}: expected exactly 1 Google tag loader")
        if raw.count(f"gtag('config', '{GOOGLE_TAG_ID}')") != 1:
            errors.append(f"{rel}: expected exactly 1 Google tag config")

        if indexable:
            required_meta = [
                ("property", "og:title"),
                ("property", "og:description"),
                ("property", "og:url"),
                ("property", "og:image"),
                ("name", "twitter:card"),
                ("name", "twitter:title"),
                ("name", "twitter:description"),
                ("name", "twitter:image"),
                ("name", "viewport"),
            ]
            for key, value in required_meta:
                if not meta_value(parser, key, value):
                    errors.append(f"{rel}: missing {value}")
            if len(parser.canonicals) != 1:
                errors.append(f"{rel}: expected 1 canonical, found {len(parser.canonicals)}")
            else:
                canonical = parser.canonicals[0]
                expected = ORIGIN + route_for(path)
                if canonical != expected:
                    errors.append(f"{rel}: canonical {canonical!r} != {expected!r}")
                canonicals.setdefault(canonical, []).append(rel)
            if not parser.json_ld:
                errors.append(f"{rel}: missing JSON-LD")
            titles.setdefault(title, []).append(rel)
        elif not is_404:
            warnings.append(f"{rel}: non-indexable page")

        for index, block in enumerate(parser.json_ld, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD block {index}: {exc.msg}")

        for image in parser.images:
            if not image.get("src"):
                errors.append(f"{rel}: image missing src")
            if not image.get("alt", "").strip():
                errors.append(f"{rel}: image {image.get('src', '(unknown)')} missing alt")

        for item in [*parser.links, *parser.images]:
            url = item.get("href") or item.get("src") or ""
            target = local_target(path, url)
            if target is not None and (ROOT not in target.parents or not target.exists()):
                errors.append(f"{rel}: missing local target {url}")

        if title and not 30 <= len(title) <= 60:
            warnings.append(f"{rel}: title length {len(title)}")
        if description and not 120 <= len(description) <= 160:
            warnings.append(f"{rel}: description length {len(description)}")
        if indexable and rel not in {"about.html", "privacy.html"}:
            words = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", " ".join(parser.text_parts)))
            if words < 180:
                warnings.append(f"{rel}: thin text estimate {words} words")

    for title, rels in titles.items():
        if len(rels) > 1:
            errors.append(f"duplicate title {title!r}: {', '.join(rels)}")
    for canonical, rels in canonicals.items():
        if len(rels) > 1:
            errors.append(f"duplicate canonical {canonical!r}: {', '.join(rels)}")

    sitemap_path = ROOT / "sitemap.xml"
    try:
        sitemap_root = ET.parse(sitemap_path).getroot()
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_urls = {node.text.strip() for node in sitemap_root.findall("sm:url/sm:loc", namespace) if node.text}
        canonical_urls = set(canonicals)
        for missing in sorted(canonical_urls - sitemap_urls):
            errors.append(f"sitemap missing {missing}")
        for extra in sorted(sitemap_urls - canonical_urls):
            errors.append(f"sitemap extra {extra}")
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    expected_sitemap = f"Sitemap: {ORIGIN}/sitemap.xml"
    if expected_sitemap not in robots:
        errors.append("robots.txt: production sitemap URL missing")

    print(f"HTML files: {len(html_files)}")
    print(f"Indexable pages: {len(canonicals)}")
    print(f"Unique titles: {len(titles)}")
    print(f"Sitemap URLs: {len(sitemap_urls) if 'sitemap_urls' in locals() else 0}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Warnings: {len(warnings)}")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
