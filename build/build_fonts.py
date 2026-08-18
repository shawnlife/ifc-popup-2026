#!/usr/bin/env python3
"""
Convert the Graphik weights the site uses into web-ready woff2 files.

    python3 build_fonts.py

Reads from graphik-font-family/ (the full vendor dump, not committed) and writes
just the four weights the CSS asks for into fonts/ (committed, ~35KB each).

woff2 rather than the source .otf: roughly half the bytes for identical
rendering, and it is the only webfont format any current browser needs.

Licence: Graphik is a commercial typeface from Commercial Type. Shawn confirmed
2026-08-17 that the licence sits with The Resource Alliance, whom this site is
built for. If Resource Alliance supplies their own licensed webfont files, drop
them into fonts/ with these filenames and skip this script entirely.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent      # project root, not build/
SRC = ROOT / "source" / "fonts-graphik"
OUT = ROOT / "assets" / "fonts"

# CSS weight -> (source file, output file). Only what the stylesheet uses; there
# is no point shipping 145 weights to render four.
WEIGHTS = {
    400: ("Graphik-Regular-Trial.otf", "graphik-400.woff2"),
    500: ("Graphik-Medium-Trial.otf", "graphik-500.woff2"),
    600: ("Graphik-Semibold-Trial.otf", "graphik-600.woff2"),
    700: ("Graphik-Bold-Trial.otf", "graphik-700.woff2"),
}


def main():
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        sys.exit("Needs fonttools:  python3 -m pip install --user fonttools brotli")

    missing = [src for src, _ in WEIGHTS.values() if not (SRC / src).exists()]
    if missing:
        sys.exit(f"Missing source weights in {SRC.name}/:\n  " + "\n  ".join(missing))

    OUT.mkdir(exist_ok=True)
    total = 0
    for weight in sorted(WEIGHTS):
        src, dest = WEIGHTS[weight]
        font = TTFont(SRC / src)
        font.flavor = "woff2"
        font.save(OUT / dest)
        before = (SRC / src).stat().st_size
        after = (OUT / dest).stat().st_size
        total += after
        print(f"  {dest:<20} weight {weight}   "
              f"{before / 1024:5.0f} KB -> {after / 1024:5.0f} KB   <- {src}")

    print(f"\nOK: {len(WEIGHTS)} weights, {total / 1024:.0f} KB total in fonts/")


if __name__ == "__main__":
    main()
