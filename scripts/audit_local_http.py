#!/usr/bin/env python3
"""Check every production sitemap path against a running local preview server."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_ORIGIN = "https://fatalfrontier1869.wiki"
LOCAL_ORIGIN = "http://localhost:4173"
NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


urls = [
    node.text.strip().replace(PRODUCTION_ORIGIN, LOCAL_ORIGIN, 1)
    for node in ET.parse(ROOT / "sitemap.xml").findall("sm:url/sm:loc", NAMESPACE)
    if node.text
]
results: list[tuple[str, int | str]] = []
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
for url in urls:
    try:
        request = urllib.request.Request(url, method="HEAD")
        with opener.open(request, timeout=3) as response:
            results.append((url, response.status))
    except urllib.error.HTTPError as error:
        results.append((url, error.code))
    except urllib.error.URLError as error:
        results.append((url, str(error.reason)))
    except TimeoutError:
        results.append((url, "timeout"))

bad = [(url, status) for url, status in results if status != 200]
print(f"Checked {len(results)} sitemap URLs; non-200: {len(bad)}")
for url, status in bad:
    print(f"{status}: {url}")
sys.exit(1 if bad else 0)
