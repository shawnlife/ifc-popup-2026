#!/usr/bin/env python3
"""
Build the social share card (the image WhatsApp / LinkedIn show for a link).

    python3 build/make_social.py

Writes assets/images/social-card.jpg at 1200x630.

Why not just use the logo: the logo is a white wordmark on a TRANSPARENT
background. WhatsApp flattens transparency onto white, so it rendered as an
empty white block. A share card has to be a flat image with a solid background
and no alpha channel.

Kept under 300KB deliberately: WhatsApp silently skips preview images larger
than roughly that, which looks identical to having no image at all.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
HERO = ROOT / "assets" / "images" / "hero" / "audience-1800.jpg"
LOGO = ROOT / "assets" / "images" / "logo.png"
FONTS = ROOT / "source" / "fonts-graphik"
OUT = ROOT / "assets" / "images" / "social-card.jpg"

# Set this to a filename in source/social/ to publish that artwork instead of
# the card this script draws. None = use the generated card.
# Shawn's sponsor-credited version is kept at source/social/share-card.png if
# it is ever wanted: set SUPPLIED = "share-card.png".
SUPPLIED = None

SUPPLIED_DIR = ROOT / "source" / "social"
SUPPLIED_WIDTHS = (1600, 1200, 1000)

W, H = 1200, 630          # 1.91:1, the standard Open Graph size
NAVY = (48, 50, 73)
ORANGE = (244, 148, 4)
MAX_KB = 300


def supported(text, path):
    """Characters the font can actually draw.

    PIL does not fall back to another font for a missing glyph, it draws
    nothing, which is how the ampersands and middots silently vanished from
    the first version of this card. These Graphik trial weights carry only 74
    glyphs: no & : / | or dashes beyond a plain hyphen.
    (The website is unaffected: browsers do fall back per character.)
    """
    from fontTools.ttLib import TTFont
    cmap = set()
    for t in TTFont(path)["cmap"].tables:
        cmap |= set(t.cmap.keys())
    return {c for c in text if ord(c) not in cmap and c != " "}


def font(size, weight="Bold"):
    for name in (f"Graphik-{weight}-Trial.otf", f"Graphik-{weight}.otf"):
        p = FONTS / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def save_within_budget(img, widths):
    """Shrink and re-encode until the file fits MAX_KB, largest version first."""
    for w in widths:
        v = img if img.width <= w else img.resize(
            (w, round(img.height * w / img.width)), Image.LANCZOS)
        for quality in (86, 80, 74, 68, 62):
            v.save(OUT, "JPEG", quality=quality, optimize=True, progressive=True)
            kb = OUT.stat().st_size / 1024
            if kb <= MAX_KB:
                return v.size, kb, quality
    return v.size, kb, quality


def use_supplied():
    """Publish the supplied card if one is selected. Returns True if it did."""
    if not SUPPLIED:
        return False
    src = SUPPLIED_DIR / SUPPLIED
    if not src.exists():
        sys.exit(f"SUPPLIED is set to {SUPPLIED!r} but {src} does not exist.")
    # Flatten any alpha onto navy: a transparent share image renders as a white
    # block in WhatsApp, which is what went wrong the first time round.
    img = Image.open(src)
    if img.mode in ("RGBA", "LA", "P"):
        flat = Image.new("RGB", img.size, NAVY)
        img = img.convert("RGBA")
        flat.paste(img, mask=img.split()[-1])
        img = flat
    else:
        img = img.convert("RGB")

    ratio = img.width / img.height
    size, kb, quality = save_within_budget(img, SUPPLIED_WIDTHS)
    print(f"Wrote {OUT.relative_to(ROOT)} from {src.name}")
    print(f"  {size[0]}x{size[1]}  {kb:.0f} KB  quality {quality}  ratio {ratio:.2f}:1")
    if not 1.7 <= ratio <= 2.0:
        print(f"  ! ratio {ratio:.2f}:1 is outside the 1.78-1.91 range platforms like;"
              " it may be cropped.")
    if kb > MAX_KB:
        sys.exit(f"  ! still over {MAX_KB}KB. WhatsApp may skip it.")
    return True


def main():
    if use_supplied():
        return

    card = Image.new("RGB", (W, H), NAVY)

    # Hero photo, cropped to fill, then dimmed so white type stays readable.
    if HERO.exists():
        photo = Image.open(HERO).convert("RGB")
        scale = max(W / photo.width, H / photo.height)
        photo = photo.resize((round(photo.width * scale), round(photo.height * scale)),
                             Image.LANCZOS)
        left = (photo.width - W) // 2
        top = int((photo.height - H) * 0.38)
        card.paste(photo.crop((left, top, left + W, top + H)), (0, 0))

        scrim = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(scrim)
        for y in range(H):
            # a little lighter at the top, heavier lower down where the text sits
            alpha = int(150 + 85 * (y / H))
            d.line([(0, y), (W, y)], fill=NAVY + (alpha,))
        card = Image.alpha_composite(card.convert("RGBA"), scrim).convert("RGB")

    d = ImageDraw.Draw(card)

    # Logo, centred in the upper half.
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lw = 400
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        card.paste(logo, ((W - lw) // 2, 66), logo)

    lines = [
        (458, "2 SEPTEMBER 2026", 52, "Bold", "#FFFFFF"),
        (512, "HOMECOMING CENTRE, DISTRICT SIX, CAPE TOWN", 27, "Medium", "#E4E6F2"),
        (570, "FULL PROGRAMME, SESSIONS, SPEAKERS", 24, "Medium", ORANGE),
    ]

    # Refuse to ship a card with invisible characters.
    src = FONTS / "Graphik-Bold-Trial.otf"
    if src.exists():
        bad = set()
        for _, text, _, _, _ in lines:
            bad |= supported(text, src)
        if bad:
            sys.exit("Characters this font cannot draw: "
                     + " ".join(sorted(bad))
                     + "\nThey would render blank. Reword, or use A-Z 0-9 , . - only.")

    d.line([(W // 2 - 70, 410), (W // 2 + 70, 410)], fill=ORANGE, width=5)
    for y, text, size, weight, colour in lines:
        d.text((W // 2, y), text, font=font(size, weight), fill=colour, anchor="mm")

    for quality in (88, 82, 76, 70, 62):
        card.save(OUT, "JPEG", quality=quality, optimize=True, progressive=True)
        kb = OUT.stat().st_size / 1024
        if kb <= MAX_KB:
            break

    print(f"Wrote {OUT.relative_to(ROOT)}: {W}x{H}, {kb:.0f} KB (quality {quality})")
    if kb > MAX_KB:
        sys.exit(f"Still over {MAX_KB}KB. WhatsApp may skip it.")


if __name__ == "__main__":
    main()
