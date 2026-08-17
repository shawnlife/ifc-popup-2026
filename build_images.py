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
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
HEADSHOT_SRC = ROOT / "Headshots"
# Original logos live here, mirroring Headshots/. They used to sit loose in the
# project root, which made it easy to drop copies into images/sponsors/ by
# mistake and ship them. Sources in, generated files out — never mixed.
LOGO_SRC = ROOT / "source-logos"
OUT = ROOT / "images"
OUT_HEADSHOTS = OUT / "headshots"
OUT_SPONSORS = OUT / "sponsors"
OUT_HERO = OUT / "hero"

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
    "Nomsa Muthaphuli.png": "nomsa-muthaphuli",
    "Nondumiso Mabuya.jpg": "nondumiso-mabuya",
    "Olumide Akerewusi Headshot.jpg": "mide-akerewusi",
    "Phano Portrait.jpg": "phano-liphoto",
    "Reanna Rossouw Headshot.JPG": "reana-rossouw",       # brief + LinkedIn both read "Reana"
    "Roland Postma.jpg": "roland-postma",
    "Shona Young Headshot.jpeg": "shona-young",
    "Sophie Olivier Headshot.JPG": "sophie-olivier",
    "Toni Erasmus Headshot.jpg": "toni-erasmus",
}

# Headshot framing is computed per photo by detecting the face (see
# square_crop_on_face). The sources range from tight selfies to full-body shots
# with a guide dog, so a single fixed rule clipped heads on several of them.
#
# How much of the crop height the face should occupy, and where its centre sits
# vertically. Heads belong above the middle, hence 0.42 rather than 0.5.
FACE_FRACTION = 0.38
FACE_CENTRE_Y = 0.42
HEAD_MARGIN = 0.05      # keep at least this much of the crop above the face box

# Only for photos where detection fails or gets it wrong. Fractions of the
# EXIF-corrected original: (left, top, right, bottom).
MANUAL_CROP = {}

SPONSORS = {
    "0924974_0.webp": "resource-alliance",
    "CCA copy.webp": "cca",
    "FBB.webp": "fundraising-beyond-borders",
    "DB.png": "donorbox",
    "DMI.webp": "downes-murray",
    "TPCA.webp": "turning-point",
    "LIFEBrand copy.webp": "lifebrand",
    "Matogen_Digital_Logo.png": "matogen",
    "Weaver logo Dark.png": "weaver-network",
    "HCC Logo Stacked.png": "homecoming-centre",
    # Vector: copied through untouched and used as-is in an <img>, so it stays
    # crisp at any size instead of being rasterised to a fixed width.
    "logo_cooktastic_circle.svg": "cooktastic",
}

# Logos that arrive with dead space around the artwork. Trimming makes them fill
# their cell in the sponsor wall instead of floating tiny in the middle.
#
# Raster: trim fully-transparent margins automatically.
TRIM_TRANSPARENT = {"homecoming-centre"}
# Vector: replace the viewBox to crop. Cooktastic is a circular badge on an
# opaque white circle — invisible on the white sponsor panel — so the visible ink
# filled only 199x285 of its 500x500 canvas (measured). This crops to the ink
# plus a little breathing room, losslessly.
SVG_VIEWBOX = {"cooktastic": "140 97 220 305"}

MAIN_LOGO = "Pop-Up Cape Town logo white no shadow.png"

# Hero background candidates, shot at the 2025 Pop-Up by LIFEbrand. Two widths
# each: phones pull the small one, so nobody downloads 1800px over event wifi.
HEROES = {
    "IFC Pop Up 2025 @LIFEbrand-6.jpg": "theatre-blue",
    "IFC Pop Up 2025 @LIFEbrand-13.jpg": "stage-amber",
    "IFC Pop Up 2025 @LIFEbrand-138.jpg": "audience",
}
HERO_WIDTHS = (900, 1800)
HERO_QUALITY = 72


def fit(img, longest):
    """Downscale so the longest edge is `longest`. Never upscales."""
    if max(img.size) <= longest:
        return img
    ratio = longest / max(img.size)
    size = (max(1, round(img.width * ratio)), max(1, round(img.height * ratio)))
    return img.resize(size, Image.LANCZOS)


def detect_face(img):
    """Largest face as (x, y, w, h) in image pixels, or None.

    OpenCV's frontal-face cascade. Photos here are all posed portraits, which is
    exactly what it is good at.
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None

    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        return None

    # Detect on a downscaled copy: faster, and less sensitive to sensor noise.
    work = fit(img, 900)
    scale = img.width / work.width
    grey = cv2.cvtColor(np.array(work), cv2.COLOR_RGB2GRAY)
    grey = cv2.equalizeHist(grey)

    faces = cascade.detectMultiScale(
        grey, scaleFactor=1.08, minNeighbors=6,
        minSize=(int(work.width * 0.06), int(work.width * 0.06)))
    if len(faces) == 0:
        return None

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    return (x * scale, y * scale, w * scale, h * scale)


def extend_edges(img, pad, horizontal):
    """Grow the image by `pad` on both sides, replicating the edge pixels.

    Used when a photo is framed too tightly to yield a square containing the
    whole head. Stretching the outermost row/column blends into a plain studio
    or wall background; a flat average colour leaves a visible seam.
    """
    if horizontal:
        canvas = Image.new("RGB", (img.width + pad * 2, img.height))
        canvas.paste(img.crop((0, 0, 1, img.height)).resize((pad, img.height)), (0, 0))
        canvas.paste(img.crop((img.width - 1, 0, img.width, img.height))
                     .resize((pad, img.height)), (pad + img.width, 0))
        canvas.paste(img, (pad, 0))
    else:
        canvas = Image.new("RGB", (img.width, img.height + pad * 2))
        canvas.paste(img.crop((0, 0, img.width, 1)).resize((img.width, pad)), (0, 0))
        canvas.paste(img.crop((0, img.height - 1, img.width, img.height))
                     .resize((img.width, pad)), (0, pad + img.height))
        canvas.paste(img, (0, pad))
    return canvas


def square_crop_on_face(img, face):
    """Square crop framing the detected face as a headshot.

    Sizes the square so the face fills FACE_FRACTION of it, centres it
    horizontally on the face and places the face centre at FACE_CENTRE_Y.
    If the photo is framed too tightly for a square that holds the whole head,
    pads the narrow sides with the background colour rather than clipping.
    """
    fx, fy, fw, fh = face
    fcx, fcy = fx + fw / 2, fy + fh / 2

    side = fh / FACE_FRACTION

    # Never let the top of the head fall outside the crop.
    needed = (fcy - (fy - HEAD_MARGIN * side)) / FACE_CENTRE_Y
    side = max(side, min(needed, img.height))
    side = min(side, max(img.width, img.height))

    if side > img.width:
        pad = int(side - img.width) // 2 + 1
        img, fcx = extend_edges(img, pad, True), fcx + pad
    if side > img.height:
        pad = int(side - img.height) // 2 + 1
        img, fcy, fy = extend_edges(img, pad, False), fcy + pad, fy + pad

    side = min(side, img.width, img.height)
    left = fcx - side / 2
    top = fcy - side * FACE_CENTRE_Y
    top = min(top, fy - HEAD_MARGIN * side)          # guarantee headroom
    left = max(0, min(left, img.width - side))
    top = max(0, min(top, img.height - side))
    return img.crop((round(left), round(top), round(left + side), round(top + side)))


def build_headshots():
    already = {f'{slug}.jpg' for slug in HEADSHOTS.values()
               if (OUT_HEADSHOTS / f"{slug}.jpg").exists()}
    if not HEADSHOT_SRC.exists() and len(already) == len(HEADSHOTS):
        # Source photos are large and live outside git, so they go walkabout.
        # If every web copy is already built, carry on rather than blocking a
        # logo or hero rebuild for want of originals nothing currently needs.
        print(f"  ! {HEADSHOT_SRC.name}/ not found — keeping the "
              f"{len(already)} existing web copies.")
        print("    Restore the folder to re-crop or add a photo.")
        return {slug: None for slug in HEADSHOTS.values()}

    missing = [n for n in HEADSHOTS if not (HEADSHOT_SRC / n).exists()]
    if missing:
        sys.exit(f"Missing headshot source files in {HEADSHOT_SRC.name}/:\n  "
                 + "\n  ".join(missing))

    manifest = {}
    undetected = []
    for name, slug in sorted(HEADSHOTS.items(), key=lambda kv: kv[1]):
        src = HEADSHOT_SRC / name
        with Image.open(src) as img:
            # Phone photos carry EXIF rotation; without this some faces ship sideways.
            # Phone photos carry EXIF rotation; without this some faces ship sideways.
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")

            if slug in MANUAL_CROP:
                l, t, r, b = MANUAL_CROP[slug]
                img = img.crop((round(l * img.width), round(t * img.height),
                                round(r * img.width), round(b * img.height)))
                how = "manual"
            else:
                face = detect_face(img)
                if face:
                    img = square_crop_on_face(img, face)
                    how = "face"
                else:
                    how = "NO FACE FOUND"
                    undetected.append(slug)

            img = fit(img, HEADSHOT_MAX)
            dest = OUT_HEADSHOTS / f"{slug}.jpg"
            img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True,
                     progressive=True)
            manifest[slug] = list(img.size)
        kb = dest.stat().st_size / 1024
        print(f"  {slug:<22} {img.width:>4}x{img.height:<4} {kb:6.0f} KB  {how:<14} <- {name}")

    if undetected:
        print("\n  !! no face detected, framing may be wrong: "
              + ", ".join(undetected)
              + "\n     add a MANUAL_CROP entry for these.")
    return manifest


def build_sponsors():
    missing = [n for n in SPONSORS if not (LOGO_SRC / n).exists()]
    if missing:
        sys.exit("Missing sponsor logo source files:\n  " + "\n  ".join(missing))

    manifest = {}
    for name, slug in sorted(SPONSORS.items(), key=lambda kv: kv[1]):
        src = LOGO_SRC / name
        ext = src.suffix.lower()
        dest = OUT_SPONSORS / f"{slug}{ext}"

        if ext == ".svg":
            # Vector: nothing to resize, and PIL cannot read it anyway.
            svg = src.read_text(encoding="utf-8")
            box = SVG_VIEWBOX.get(slug)
            if box:
                svg, n = re.subn(r'viewBox="[^"]*"', f'viewBox="{box}"', svg, count=1)
                if n != 1:
                    sys.exit(f"{name}: expected one viewBox to rewrite, found {n}")
            dest.write_text(svg, encoding="utf-8")
            manifest[slug] = {"file": dest.name, "w": None, "h": None}
            print(f"  {slug:<26} {'vector':>9}  "
                  f"{dest.stat().st_size / 1024:6.0f} KB   <- {name}"
                  + ("  (viewBox cropped)" if box else ""))
            continue

        with Image.open(src) as img:
            img = ImageOps.exif_transpose(img)
            if slug in TRIM_TRANSPARENT:
                bbox = img.convert("RGBA").getchannel("A").getbbox()
                if bbox:
                    img = img.crop(bbox)
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


def build_heroes():
    missing = [n for n in HEROES if not (ROOT / n).exists()]
    if missing:
        print("  (skipping heroes, sources not present: "
              + ", ".join(missing) + ")")
        return {}

    OUT_HERO.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, slug in sorted(HEROES.items(), key=lambda kv: kv[1]):
        with Image.open(ROOT / name) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")
            sizes = {}
            for width in HERO_WIDTHS:
                v = img if img.width <= width else fit(img, width)
                dest = OUT_HERO / f"{slug}-{width}.jpg"
                v.save(dest, "JPEG", quality=HERO_QUALITY, optimize=True,
                       progressive=True)
                sizes[width] = [v.width, v.height]
                print(f"  {dest.name:<28} {v.width:>4}x{v.height:<4} "
                      f"{dest.stat().st_size / 1024:6.0f} KB")
            manifest[slug] = sizes
    return manifest


def build_main_logo():
    src = LOGO_SRC / MAIN_LOGO
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
    print("\nHero backgrounds:")
    heroes = build_heroes()
    print("\nHeadshots:")
    headshots = build_headshots()
    print("\nSponsor logos:")
    sponsors = build_sponsors()

    assert len(headshots) == 24, f"expected 24 headshots, wrote {len(headshots)}"
    assert len(sponsors) == 11, f"expected 11 sponsor logos, wrote {len(sponsors)}"

    (OUT / "manifest.json").write_text(
        json.dumps({"logo": logo, "heroes": heroes, "headshots": headshots,
                    "sponsors": sponsors}, indent=2, sort_keys=True)
    )

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"\nOK — 24 headshots, 11 sponsor logos, 1 main logo.")
    print(f"Total images/ size: {total / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
