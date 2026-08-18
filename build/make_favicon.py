#!/usr/bin/env python3
"""
Build the favicon for the usage dashboard, from the IFC logo itself.

    python3 build/make_favicon.py

The full logo is "IFC / POP-UP / CAPE TOWN" stacked, unreadable at 16px. This
crops to just the "IFC" glyphs (found automatically from the logo's own alpha
channel, so a redrawn logo re-crops correctly without hand-tuned coordinates),
pads it onto a navy square, and writes the sizes browsers ask for.

Only the dashboard needs this. The public site's favicon is the full logo
(wired directly in build_site.py) since a browser tab has room for "IFC" being
small within a bigger square; 16x16 does not.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.parent
LOGO = ROOT / "assets" / "images" / "logo.png"
OUT = ROOT / "analytics"
NAVY = (48, 50, 73, 255)
PAD = 18


def find_band(alpha, axis):
    """Row or column indices spanning the first contiguous run of ink,
    reading top-to-bottom or left-to-right. axis=1 scans rows, axis=0 columns."""
    has_ink = alpha.max(axis=axis) > 20
    start = None
    for i, v in enumerate(has_ink):
        if v and start is None:
            start = i
        elif not v and start is not None:
            return start, i
    return (start, len(has_ink)) if start is not None else (0, len(has_ink))


def main():
    if not LOGO.exists():
        raise SystemExit(f"Logo not found: {LOGO}. Run build_images.py first.")

    import numpy as np
    img = Image.open(LOGO).convert("RGBA")
    a = np.array(img)

    top, bottom = find_band(a[..., 3], axis=1)          # first row-band = "IFC"
    left, right = find_band(a[top:bottom, :, 3], axis=0)

    mark = img.crop((max(0, left - PAD), max(0, top - PAD),
                     right + PAD, bottom + PAD))
    side = max(mark.width, mark.height) + 40
    canvas = Image.new("RGBA", (side, side), NAVY)
    canvas.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2), mark)

    for size in (16, 32, 512):
        canvas.resize((size, size), Image.LANCZOS).save(OUT / f"favicon-{size}.png")
    canvas.resize((256, 256), Image.LANCZOS).save(
        OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    print(f"Wrote favicon-16/32/512.png + favicon.ico to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
