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
GOOGLE_TAG_ID = "G-KMLT9384LR"
GOOGLE_TAG = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_TAG_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GOOGLE_TAG_ID}');
</script>
'''
TEXT_REPLACEMENTS = {
    "How to Extract in Fatal Frontier 1869 — Steamer &amp; Signal Fire":
        "Fatal Frontier 1869 Extraction — Steamer &amp; Signal Fire",
    "Track Fatal Frontier 1869 Early Access updates, new Pioneers, economy changes, points of interest and gameplay fixes.":
        "Track Fatal Frontier 1869 Early Access updates, new Pioneers, economy changes, points of interest, gameplay fixes and guide revisions.",
    "Privacy information for Fatal Frontier 1869 Wiki, including the current static-site setup, external links, local server behavior and future analytics changes.":
        "Privacy information for Fatal Frontier 1869 Wiki, including hosting logs, Google Analytics, browser storage and external links.",
    "This page describes the Wiki as prepared on August 27, 2026. It must be updated before adding analytics, advertising, forms or user accounts.":
        "This page explains the Wiki's current Vercel and Cloudflare hosting, Google Analytics measurement, browser storage and external links.",
    "<strong>Current status:</strong> the project contains no analytics script, advertising network, account system, comments, payment form or identity-document upload. It does not ask for game passwords, KYC documents or payment details.":
        "<strong>Current status:</strong> the site uses Google Analytics 4 to understand aggregate visits and page usage. It has no advertising network, account system, comments, payment form or identity-document upload, and it does not ask for game passwords, KYC documents or payment details.",
    "When the site is publicly hosted, the hosting provider may process standard server logs such as IP address, requested URL, browser information, timestamps and security events. Retention and processing depend on the provider selected for launch and must be documented after deployment.":
        "The site is hosted on Vercel and currently uses Cloudflare for DNS and proxy delivery. These providers may process standard technical records such as IP address, requested URL, browser information, timestamps and security events under their own policies.",
    "The current code uses normal browser navigation and interface state. It does not intentionally store a tracking identifier in cookies or local storage. If analytics or consent controls are added later, this section must change before those tools go live.":
        "The site uses Google Analytics 4 with measurement ID G-KMLT9384LR. Google Analytics may use cookies or similar browser storage and may process page URLs, referrers, browser and device details, approximate location and interaction events. See <a href=\"https://policies.google.com/privacy\" rel=\"nofollow noopener\">Google's Privacy Policy</a> and the <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"nofollow noopener\">Google Analytics opt-out tool</a>.",
    "The page will be revised when the production host, analytics, advertising or contact method changes. The modified date should move with the implementation, not merely with wording.":
        "The page will be revised when the hosting, analytics configuration, advertising, consent controls or contact method changes. The modified date moves with material implementation changes.",
    "Last updated August 27, 2026. This policy describes the project files before public hosting. Hosting-provider details must be added during deployment.":
        "Last updated August 27, 2026. This policy reflects the current Vercel deployment, Cloudflare delivery and Google Analytics 4 configuration.",
    "The current static build does not contain analytics, advertising, account creation or payment collection. External download, support and community links leave this Wiki and follow the destination’s policies. See the <a href=\"/privacy.html\">Privacy page</a> for the current implementation.":
        "The site uses Google Analytics 4 for aggregate usage measurement, but it does not contain advertising, account creation or payment collection. External download, support and community links leave this Wiki and follow the destination’s policies. See the <a href=\"/privacy.html\">Privacy page</a> for details.",
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
    if f"gtag/js?id={GOOGLE_TAG_ID}" not in text:
        text = text.replace("</head>", f"{GOOGLE_TAG}</head>", 1)
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
