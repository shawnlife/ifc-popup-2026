#!/usr/bin/env python3
"""
Generate the QR code and a printable A5 card for the info desk.

    python3 make_qr.py                        # uses the GitHub Pages URL
    python3 make_qr.py https://ifc.shawnlife.com/    # after the domain moves

IMPORTANT: if the site ever moves to a custom domain, re-run this with the new
URL and reprint. The old QR will keep working only as long as the Pages URL does.

Needs segno (pure Python):  python3 -m pip install --user segno
"""

import sys
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

URL = sys.argv[1] if len(sys.argv) > 1 else "https://shawnlife.github.io/ifc-popup-2026/"
OUT = Path(__file__).parent.parent / "qr"
NAVY, ORANGE, MUTED = "#303249", "#F49404", "#A0A3C0"


def font(size, bold=False):
    path = ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf")
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main():
    OUT.mkdir(exist_ok=True)
    pretty = URL.replace("https://", "").rstrip("/")

    # error='h' = highest correction, so it still scans if the print is scuffed
    # or partly covered on the day.
    qr = segno.make(URL, error="h")
    qr.save(OUT / "ifc-popup-2026-qr.png", scale=24, border=3, dark=NAVY, light="#FFFFFF")
    qr.save(OUT / "ifc-popup-2026-qr.svg", scale=24, border=3, dark=NAVY, light="#FFFFFF")

    W, H = 1748, 2480                     # A5 at 300 dpi
    card = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(card)

    d.rectangle([0, 0, W, 300], fill=NAVY)
    d.text((W // 2, 118), "IFC CAPE TOWN POP-UP 2026", font=font(78, True),
           fill="#FFFFFF", anchor="mm")
    d.text((W // 2, 205), "2 September 2026  ·  Homecoming Centre",
           font=font(46), fill=MUTED, anchor="mm")

    d.text((W // 2, 470), "Scan for the full programme", font=font(74, True),
           fill=NAVY, anchor="mm")
    d.text((W // 2, 566), "Schedule, sessions and speakers on your phone",
           font=font(48), fill="#6b6e8c", anchor="mm")

    side = 1180
    q = Image.open(OUT / "ifc-popup-2026-qr.png").convert("RGB")
    q = q.resize((side, side), Image.LANCZOS)
    qx, qy = (W - side) // 2, 660
    d.rectangle([qx - 16, qy - 16, qx + side + 16, qy + side + 16],
                outline=ORANGE, width=10)
    card.paste(q, (qx, qy))

    d.text((W // 2, 2035), pretty, font=font(52, True), fill=NAVY, anchor="mm")
    d.rectangle([0, H - 130, W, H], fill=ORANGE)
    d.text((W // 2, H - 65), "Free tea & coffee in the lobby  ·  Ask at the info desk",
           font=font(44, True), fill="#241f10", anchor="mm")

    card.save(OUT / "ifc-popup-2026-qr-print-A5.png", dpi=(300, 300))

    print(f"QR points to: {URL}")
    for f in sorted(OUT.iterdir()):
        print(f"  qr/{f.name:36} {f.stat().st_size / 1024:6.0f} KB")


if __name__ == "__main__":
    main()
