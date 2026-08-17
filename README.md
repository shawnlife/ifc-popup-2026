# IFC Cape Town Pop-Up 2026 — event website

Mobile-first schedule site for the IFC Cape Town Pop-Up, **2 September 2026**,
Homecoming Centre, District Six, Cape Town. Attendees scan a QR code on the day
and read the programme on their phones.

**Live:** https://shawnlife.github.io/ifc-popup-2026/

---

## How to change something

All the words live in **`site_data.py`** — speaker names, titles, bios, session
descriptions, times, sponsor links. Open it, edit the text, then run:

```bash
python3 build_site.py
```

That rewrites `index.html`. It also checks that every internal link still points
at something real, so a tapped session or speaker name can never lead nowhere.
If a link breaks, it tells you and refuses to write the file.

To publish the change:

```bash
git add -A && git commit -m "Update speaker bio" && git push
```

GitHub Pages picks it up within a minute or so.

## If a photo changes

Drop the new photo in `Headshots/`, add or update its entry in the map at the top
of `build_images.py`, then:

```bash
python3 build_images.py && python3 build_site.py
```

`build_images.py` resizes the originals (72MB) down to web copies (~1.1MB),
corrects EXIF rotation, and re-frames the handful of full-body shots so the face
fills the circle. Originals are never modified.

---

## Files

| File | What it is |
|---|---|
| `index.html` | The whole site. Generated — edit `site_data.py` instead. |
| `site_data.py` | All copy: schedule, sessions, speakers, sponsors. |
| `build_site.py` | Builds `index.html`. Holds the CSS and JS. |
| `build_images.py` | Resizes and re-frames photos into `images/`. |
| `images/` | Web-ready logo, headshots, sponsor logos. |
| `make_qr.py` | Builds the QR code + printable A5 card in `qr/`. |
| `qr/` | QR code (PNG + SVG) and a print-ready A5 card for the info desk. |
| `Headshots/`, `*.webp` | Originals. Not committed — local only. |

## Notes

- One self-contained HTML file: embedded CSS and JS, no frameworks, no build
  step needed to view it. Just open `index.html`.
- Three tabs (Schedule / Sessions / Speakers). Only one shows at a time. Links
  between them switch tabs and jump to the right card, with a "back" pill to
  return. Without JavaScript it degrades to one long readable page.
- Tapping a speaker's name anywhere opens their profile in a pop-up: big
  headshot, bio, which session they're in, LinkedIn. Without JavaScript the same
  content simply shows inline on the card instead.
- The Sessions tab filters by theatre, time and topic. Topic tags live in
  `TOPICS` in `site_data.py` — the filter chips are generated from whatever is
  in there, so renaming or re-tagging needs no other change.
- Sponsor logos sit on one pale band rather than individual white tiles.
  Something light is needed behind them: Weaver, Downes Murray, CCA and Matogen
  are all dark-on-transparent and vanish on the navy background.
- Headshot framing is computed by face detection (`build_images.py`), not a
  fixed crop rule, because the sources range from tight selfies to full-body
  shots. Photos framed too tightly for a square get their edge pixels extended
  rather than the head clipped.
- Font is Inter (Graphik is commercial and unavailable); the CSS asks for
  Graphik first, so licensed webfont files would drop straight in.

## The QR code for the day

`qr/ifc-popup-2026-qr-print-A5.png` is print-ready at A5, 300dpi. Both files were
decoded back to the live URL to confirm they scan.

**If the site moves to a custom domain, regenerate and reprint:**

```bash
python3 make_qr.py https://ifc.shawnlife.com/
```

## Hero background

`EVENT["hero"]` in `site_data.py` picks the photo behind the logo. Options are
the slugs in `HEROES` in `build_images.py` — `theatre-blue`, `stage-amber`,
`audience` — or `None` for plain navy. All three are already built at two widths
(phones load the 900px file), so switching is a one-word change plus a rebuild.

### Still outstanding

- A higher-resolution Fundraising Beyond Borders logo (current is 200×50px)
- Cooktastic and Homecoming Centre logos to add to the sponsor band
- "On the day" info (parking etc.) — likely a fourth tab
- Custom domain (`ifc.shawnlife.com`) — needs a DNS record plus a `CNAME` file,
  and a reprinted QR code
