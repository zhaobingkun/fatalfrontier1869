#!/usr/bin/env python3
"""Keep the homepage's inline site CSS synchronized with styles.css."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"
START = '<style id="site-css">'
END = "</style>"


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    css = STYLES.read_text(encoding="utf-8").strip()
    block = f"{START}\n{css}\n{END}"

    if START in html:
        updated, count = re.subn(
            rf"{re.escape(START)}.*?{re.escape(END)}",
            lambda _: block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        updated, count = re.subn(
            r'<link rel="stylesheet" href="/styles\.css(?:\?v=[^"]+)?">',
            lambda _: block,
            html,
            count=1,
        )

    if count != 1:
        raise SystemExit("Could not find a unique homepage CSS insertion point")

    INDEX.write_text(updated, encoding="utf-8")
    print(f"Synchronized {len(css):,} bytes of CSS into index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
