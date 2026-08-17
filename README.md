# IFC Cape Town Pop-Up 2026 — event website

Mobile-first schedule site for the IFC Cape Town Pop-Up, **2 September 2026**,
Homecoming Centre, District Six, Cape Town. Attendees scan a QR code on the day
and read the programme on their phones.

**Live:** https://ifc.shawnlife.com/

---

## Where everything lives

```
index.html          The site. GENERATED — never edit this by hand.
build.py            Rebuilds everything. Start here.

build/              The scripts that make the site
  site_data.py        ← ALL THE WORDS. This is the file you edit.
  build_site.py       Turns site_data.py into index.html (holds the CSS + JS)
  build_images.py     source/ photos + logos  ->  assets/images/
  build_fonts.py      source/ Graphik .otf    ->  assets/fonts/ .woff2
  make_qr.py          Makes the QR code and printable card

assets/             What the live site actually loads (small, committed)
  images/             logo, headshots/, sponsors/, hero/
  fonts/              graphik-400/500/600/700.woff2

source/             ORIGINALS. Big, and never published. Not in git.
  headshots/          The photos speakers sent
  logos/              Sponsor logo artwork as supplied
  hero-photos/        2025 event photos by LIFEbrand
  fonts-graphik/      The Graphik family

analytics/          Usage tracking — see analytics/SETUP.md
docs/               The original project brief
qr/                 QR code + print-ready A5 card
```

The rule that matters: **sources go in `source/`, generated files come out in
`assets/`, and the two never share a folder.** They used to, and nine original
logo files got shipped to the live site by accident.

---

## Changing something

**Words** — speaker titles, bios, session descriptions, times, sponsor links,
the Info tab, topic tags — all live in **`build/site_data.py`**. Edit it, then:

```bash
python3 build.py --site
```

That rewrites `index.html`. It also checks every internal link still points at
something real, and refuses to write the file if one is broken.

**A photo or logo changed?** Drop it in the matching `source/` folder, update
the filename map at the top of `build/build_images.py`, then:

```bash
python3 build.py
```

**Publishing** — from this folder:

```bash
git add -A && git commit -m "Update speaker bio" && git push
```

GitHub Pages picks it up within a minute or two.

---

## Notes

- One self-contained HTML file: embedded CSS and JS, no frameworks, no build
  step needed to *view* it. Just open `index.html`.
- Four tabs (Schedule / Sessions / Speakers / Info). Only one shows at a time.
  Links between them switch tabs and jump to the right card, with a "back" pill
  to return. Without JavaScript it degrades to one long readable page.
- Tapping a speaker card anywhere opens their profile pop-up: big headshot, bio,
  which session they're in, LinkedIn. Tapping a schedule box opens that session.
- The Sessions tab filters by theatre, time and topic. Topic tags are the
  `TOPICS` dict in `site_data.py`; the dropdown is generated from whatever is in
  there, so renaming or re-tagging needs no other change.
- Sponsor logos sit on one white panel. White specifically: Donorbox and Downes
  Murray have opaque white backgrounds baked in, and Turning Point's is opaque
  dark navy, so no other single colour works for all three.
- Headshot framing is computed by face detection, not a fixed crop rule, because
  the sources range from tight selfies to full-body shots. Photos framed too
  tightly for a square get their edge pixels extended rather than the head
  clipped.
- **Graphik is self-hosted** from `assets/fonts/`. No Google Fonts, so the page
  makes no third-party requests except the analytics beacon — nothing to leak,
  and nothing to fail on conference wifi.
- `.nojekyll` stops GitHub running its Jekyll pipeline over the repo. A Pages
  build failed on it once; nothing here is a Jekyll site.

## Usage tracking

Live. Full walkthrough in `analytics/SETUP.md`.

Records which sessions and speaker profiles get opened, which tabs and filters
get used, and every outbound link click (sponsors, train schedule, maps,
LinkedIn by whose profile). No cookies, nothing stored on the visitor's device,
no IP or demographic data — so **no consent banner is needed**. Turn it off by
setting `ANALYTICS_URL = None` in `site_data.py`; the tracking code then isn't
written into the page at all.

`analytics/dashboard.html` is the local dashboard — open it, click **Change
URL**, paste the Apps Script `/exec` URL. Refreshes every 60 seconds.

**Browsing the live site yourself?** Use
`https://ifc.shawnlife.com/?shawn` — that suppresses tracking entirely for
that browser tab (and any tab it navigates to next), so your own clicks never
land in the Sheet. Nothing is sent, not even a marked "ignore this" event.

## The QR code for the day

`qr/ifc-popup-2026-qr-print-A5.png` is print-ready at A5, 300dpi. Both files were
decoded back to the live URL to confirm they scan.

It points at **https://ifc.shawnlife.com/**. If the domain ever changes, the QR
must be regenerated and reprinted — the URL is baked into the code:

```bash
python3 build/make_qr.py https://new-domain/
```

## Custom domain

Live at **ifc.shawnlife.com**, with HTTPS enforced.

- Squarespace DNS: `CNAME` on host `ifc` -> `shawnlife.github.io`
- `CNAME` file in this repo holds the domain. **Do not delete it** — Pages
  reads it, and removing it drops the domain
- `shawnlife.github.io/ifc-popup-2026/` now 301-redirects here

### Still outstanding

- A higher-resolution Fundraising Beyond Borders logo (current is 200×50px)
