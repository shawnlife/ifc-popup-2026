#!/usr/bin/env python3
"""
Build web-ready images for the IFC Cape Town Pop-Up 2026 site.

Reads the original photos/logos (which are large, inconsistently named, and in
mixed formats) and writes small, slug-named copies into ./images/.
Originals are never modified.

Re-run this any time a photo or logo is replaced:
    python3 build_images.py
"""

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
HEADSHOT_SRC = ROOT / "Headshots"
OUT = ROOT / "images"
OUT_HEADSHOTS = OUT / "headshots"
OUT_SPONSORS = OUT / "sponsors"

HEADSHOT_MAX = 600   # displayed at 120px, so this covers retina with room to spare
LOGO_MAX = 600
MAIN_LOGO_MAX = 800
JPEG_QUALITY = 80

# Original filename -> slug. Explicit rather than derived, because several
# sources are misnamed, duplicated, or extensionless.
HEADSHOTS = {
    "Alison Young Headshot.jpeg": "alison-young",
    "Angela Blackwell.jpeg": "angela-blackwell",          # ignore the "(1)" duplicate
    "Casey Prince Headshot.jpg": "casey-prince",
    "Chantel Cooper Headshot.jpg": "chantel-cooper",
    "Cheryl Manikam Headshot.jpg": "cheryl-manikam",
    "Colleen Francis.jpg": "colleen-francis",
    "Damian Chapman.JPG": "damian-chapman",
    "Delphino Machikicho Headshot.jpg": "delphino-machikicho",
    "Farida Lavangee.jpg": "farida-lavangee",
    "Ian Parsons Headshot.jpg": "ian-parsons",
    "Jenni McLeod.JPG": "jenni-mcleod",
    "Leana de Beer Headshot.png": "leana-de-beer",
    "Malusi Ntoyapi.jpg": "malusi-ntoyapi",
    "Miche Nicholas Headshot.png": "miche-nicholas",
    "Nick Rockey.png": "nick-rockey",                     # 600x600, best of 3 variants
    "Nomsa Muthaphuli": "nomsa-muthaphuli",               # supplied with no file extension
    "Nondumiso Mabuya.jpg": "nondumiso-mabuya",
    "Olumide Akerewusi Headshot.jpg": "mide-akerewusi",
    "Phano Portrait.jpg": "phano-liphoto",
    "Reanna Rossouw Headshot.JPG": "reana-rossouw",       # brief + LinkedIn both read "Reana"
    "Roland Postma.jpg": "roland-postma",
    "Shona Young Headshot.jpeg": "shona-young",
    "Sophie Olivier Headshot.JPG": "sophie-olivier",
    "Toni Erasmus Headshot.jpg": "toni-erasmus",
}

# A few sources are full-body or environmental shots where the face ends up tiny
# (or clipped) in a 120px circle. These re-frame to head-and-shoulders before
# resizing. Values are (left, top, right, bottom) as fractions of the
# EXIF-corrected original, and each box is deliberately square.
CROP = {
    "angela-blackwell": (0.22, 0.03, 0.84, 0.38),    # seated full-body with guide dog
    "ian-parsons": (0.275, 0.267, 0.725, 0.567),     # wide outdoor shot, seated
    "roland-postma": (0.267, 0.155, 0.747, 0.515),   # standing three-quarter
    "malusi-ntoyapi": (0.14, 0.02, 0.79, 0.52),      # arms-folded torso shot
    "phano-liphoto": (0.0, 0.105, 1.0, 0.728),       # tight selfie, centre on the face
}

SPONSORS = {
    "0924974_0.webp": "resource-alliance",
    "CCA.webp": "cca",
    "FBB.webp": "fundraising-beyond-borders",
    "DB.png": "donorbox",
    "DMI.webp": "downes-murray",
    "TPCA.webp": "turning-point",
    "LIFEBrand.webp": "lifebrand",
    "Matogen_Digital_Logo.png": "matogen",
    "Weaver logo Dark.png": "weaver-network",
}

MAIN_LOGO = "Pop-Up Cape Town logo white no shadow.png"


def fit(img, longest):
    """Downscale so the longest edge is `longest`. Never upscales."""
    if max(img.size) <= longest:
        return img
    ratio = longest / max(img.size)
    size = (max(1, round(img.width * ratio)), max(1, round(img.height * ratio)))
    return img.resize(size, Image.LANCZOS)


def build_headshots():
    missing = [n for n in HEADSHOTS if not (HEADSHOT_SRC / n).exists()]
    if missing:
        sys.exit("Missing headshot source files:\n  " + "\n  ".join(missing))

    manifest = {}
    for name, slug in sorted(HEADSHOTS.items(), key=lambda kv: kv[1]):
        src = HEADSHOT_SRC / name
        with Image.open(src) as img:
            # Phone photos carry EXIF rotation; without this some faces ship sideways.
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")
            if slug in CROP:
                l, t, r, b = CROP[slug]
                img = img.crop((round(l * img.width), round(t * img.height),
                                round(r * img.width), round(b * img.height)))
            img = fit(img, HEADSHOT_MAX)
            dest = OUT_HEADSHOTS / f"{slug}.jpg"
            img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True,
                     progressive=True)
            manifest[slug] = list(img.size)
        kb = dest.stat().st_size / 1024
        print(f"  {slug:<22} {img.width:>4}x{img.height:<4}  {kb:6.0f} KB   <- {name}")
    return manifest


def build_sponsors():
    missing = [n for n in SPONSORS if not (ROOT / n).exists()]
    if missing:
        sys.exit("Missing sponsor logo source files:\n  " + "\n  ".join(missing))

    manifest = {}
    for name, slug in sorted(SPONSORS.items(), key=lambda kv: kv[1]):
        src = ROOT / name
        ext = src.suffix.lower()
        dest = OUT_SPONSORS / f"{slug}{ext}"
        with Image.open(src) as img:
            img = ImageOps.exif_transpose(img)
            if max(img.size) > LOGO_MAX:
                img = fit(img, LOGO_MAX)
                img.save(dest, lossless=True) if ext == ".webp" else img.save(dest)
            else:
                # Already small enough; copy byte-for-byte rather than re-encode.
                shutil.copy2(src, dest)
            manifest[slug] = {"file": dest.name, "w": img.width, "h": img.height}
        kb = dest.stat().st_size / 1024
        print(f"  {slug:<26} {img.width:>4}x{img.height:<4} {kb:6.0f} KB   <- {name}")
    return manifest


def build_main_logo():
    src = ROOT / MAIN_LOGO
    if not src.exists():
        sys.exit(f"Missing main logo: {MAIN_LOGO}")
    with Image.open(src) as img:
        img = fit(img, MAIN_LOGO_MAX)
        # Keep the alpha channel: this is a white logo for a dark background.
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        dest = OUT / "logo.png"
        img.save(dest, "PNG", optimize=True)
        size = list(img.size)
    print(f"  logo.png               {size[0]}x{size[1]}  "
          f"{dest.stat().st_size / 1024:.0f} KB")
    return size


def main():
    for d in (OUT, OUT_HEADSHOTS, OUT_SPONSORS):
        d.mkdir(parents=True, exist_ok=True)

    print("Main logo:")
    logo = build_main_logo()
    print("\nHeadshots:")
    headshots = build_headshots()
    print("\nSponsor logos:")
    sponsors = build_sponsors()

    assert len(headshots) == 24, f"expected 24 headshots, wrote {len(headshots)}"
    assert len(sponsors) == 9, f"expected 9 sponsor logos, wrote {len(sponsors)}"

    (OUT / "manifest.json").write_text(
        json.dumps({"logo": logo, "headshots": headshots, "sponsors": sponsors},
                   indent=2, sort_keys=True)
    )

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"\nOK — 24 headshots, 9 sponsor logos, 1 main logo.")
    print(f"Total images/ size: {total / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
