#!/usr/bin/env python3
"""Regenerate skills/architecture/metrics.json — glyph widths for /architecture's renderer.

render.py measures every text with Excalidraw's real fonts so labels never get cut or
overlap. It can't load fonts at skill time (standard library only), so the advance widths
are extracted here once and shipped as JSON.

Dev-only. Needs fonttools and brotli (woff2), which the skill itself never uses:

    python3 -m venv /tmp/fontenv && /tmp/fontenv/bin/pip install fonttools brotli
    /tmp/fontenv/bin/python scripts/architecture_metrics.py

Rerun it only when bumping EXCALIDRAW_VERSION, i.e. when Excalidraw changes its fonts.
"""

import json
import urllib.request
from io import BytesIO
from pathlib import Path

from fontTools.ttLib import TTFont

EXCALIDRAW_VERSION = "0.18.0"
CDN = f"https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@{EXCALIDRAW_VERSION}"
OUT = Path(__file__).resolve().parent.parent / "skills" / "architecture" / "metrics.json"

# Characters a diagram realistically uses: Latin, punctuation, arrows, maths, box symbols.
RANGES = [(0x20, 0x24F), (0x2000, 0x206F), (0x2190, 0x21FF), (0x2200, 0x22FF), (0x2500, 0x25FF)]


def fetch(path: str) -> bytes:
    with urllib.request.urlopen(f"{CDN}{path}") as r:
        return r.read()


def widths(fonts: list[bytes]) -> dict[str, float]:
    out: dict[str, float] = {}
    for data in fonts:
        font = TTFont(BytesIO(data))
        upm = font["head"].unitsPerEm
        hmtx = font["hmtx"].metrics
        for cp, glyph in font.getBestCmap().items():
            if any(lo <= cp <= hi for lo, hi in RANGES):
                out.setdefault(chr(cp), round(hmtx[glyph][0] / upm, 4))
    return out


def main() -> None:
    listing = json.load(urllib.request.urlopen(
        f"https://data.jsdelivr.com/v1/package/npm/@excalidraw/excalidraw@{EXCALIDRAW_VERSION}/flat"))
    names = [f["name"] for f in listing["files"]]
    hand = [fetch(n) for n in names if n.startswith("/dist/prod/fonts/Excalifont/")]
    mono = [fetch("/dist/prod/fonts/Cascadia/CascadiaCode-Regular.woff2")]
    data = {
        "source": f"@excalidraw/excalidraw@{EXCALIDRAW_VERSION}",
        "fallback": 0.75,
        "fonts": {"5": widths(hand), "3": widths(mono)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(data['fonts']['5'])} hand glyphs, {len(data['fonts']['3'])} mono glyphs)")


if __name__ == "__main__":
    main()
