#!/usr/bin/env python3
"""
Rebuild the whole site.

    python3 build.py            # images, fonts, then the page
    python3 build.py --site     # just the page (after editing copy)

Editing words? That is build/site_data.py, then `python3 build.py --site`.
"""

import subprocess
import sys
from pathlib import Path

BUILD = Path(__file__).parent / "build"
STEPS = [("build_images.py", "Images"),
         ("build_fonts.py", "Fonts"),
         ("make_social.py", "Social card"),
         ("build_site.py", "Page")]


def run(script, label):
    print(f"\n=== {label} " + "=" * (58 - len(label)))
    r = subprocess.run([sys.executable, str(BUILD / script)])
    if r.returncode != 0:
        sys.exit(f"\n{label} step failed — stopping.")


def main():
    steps = STEPS[-1:] if "--site" in sys.argv else STEPS
    for script, label in steps:
        run(script, label)
    print("\nDone. Open index.html to view it, or:")
    print("  git add -A && git commit -m \"...\" && git push")


if __name__ == "__main__":
    main()
