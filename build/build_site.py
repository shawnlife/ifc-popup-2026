#!/usr/bin/env python3
"""
Generate index.html for the IFC Cape Town Pop-Up 2026 site.

All copy lives in site_data.py — edit there, then run:

    python3 build_site.py

The output is one self-contained index.html (embedded CSS and JS, no
frameworks, no build step needed to view it). Before writing, this script
checks that every internal "#anchor" link actually resolves, so a tapped
session or speaker name can never lead nowhere.
"""

import html
import re
import sys
from pathlib import Path

import site_data as D

ROOT = Path(__file__).parent.parent      # project root, not build/
OUT = ROOT / "index.html"
SITE_URL = "https://ifc.shawnlife.com/"

# Graphik is self-hosted from fonts/ (see build_fonts.py). Weight -> woff2 file.
# Self-hosting means the site makes zero third-party requests: no Google Fonts,
# so no visitor IP leaves for anyone else, and nothing to fail on event wifi.
GRAPHIK = {400: "graphik-400.woff2", 500: "graphik-500.woff2",
           600: "graphik-600.woff2", 700: "graphik-700.woff2"}

BY_SLUG = {s["slug"]: s for s in D.SPEAKERS}
BY_ANCHOR = {s["anchor"]: s for s in D.SESSIONS}

# Which session(s) each speaker appears in.
SESSIONS_FOR = {sp["slug"]: [] for sp in D.SPEAKERS}
for _s in D.SESSIONS:
    for _slug, _note in _s["speakers"]:
        SESSIONS_FOR.setdefault(_slug, []).append(_s)


def e(text):
    return html.escape(str(text), quote=True)


def topics_of(anchor):
    return D.TOPICS.get(anchor, [])


ALL_TOPICS = sorted({t for a in BY_ANCHOR for t in topics_of(a)})


def start_minutes(slot):
    """Sort key for a "9:15 – 10:00" label. The day runs 08:00–17:00, so the
    bare hour needs no am/pm handling."""
    h, m = slot.split("–")[0].strip().split(":")
    return int(h) * 60 + int(m)


ALL_TIMES = sorted({s["time"] for s in D.SESSIONS}, key=start_minutes)
ALL_ROOMS = [D.STAR, D.AVALON]


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none !important}
:root{
  --orange:#F49404;
  --bg:#303249;
  --surface:#3D3F5A;
  --surface-2:#474A69;
  --text:#FFFFFF;
  --muted:#CDD0E4;
  --line:rgba(255,255,255,.10);
  --line-strong:rgba(255,255,255,.20);
  --radius:12px;
  --nav-h:58px;
  --wrap:1080px;
}
@media (min-width:760px){:root{--nav-h:64px}}
html{-webkit-text-size-adjust:100%}
html:focus-within{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html:focus-within{scroll-behavior:auto}}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Graphik',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  font-size:16px;line-height:1.55;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
img{max-width:100%;height:auto}
a{color:var(--orange);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px;border-radius:4px}
.wrap{width:100%;max-width:var(--wrap);margin:0 auto;padding:0 16px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}
.skip{position:absolute;left:8px;top:-60px;z-index:80;background:var(--orange);
  color:#241f10;font-weight:700;padding:10px 14px;border-radius:8px;transition:top .15s}
.skip:focus{top:8px}

/* All headings set in caps. */
h1,h2,h3{text-transform:uppercase;letter-spacing:.01em;font-weight:700}

/* ---------- sticky header: centred tabs, no logo ---------- */
header{
  position:sticky;top:0;z-index:60;background:rgba(48,50,73,.97);
  backdrop-filter:saturate(1.4) blur(8px);
  border-bottom:1px solid var(--line);
}
.bar{display:flex;align-items:center;height:var(--nav-h);
  max-width:var(--wrap);margin:0 auto;padding:0 10px}
[role=tablist]{display:flex;flex:1 1 auto;gap:6px;justify-content:center;min-width:0}
[role=tab]{
  flex:1 1 0;min-width:0;max-width:190px;min-height:44px;
  display:flex;align-items:center;justify-content:center;
  padding:0 4px;border-radius:9px;
  font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;
  color:var(--muted);text-decoration:none;white-space:nowrap;
  border:1px solid transparent;background:none;cursor:pointer;font-family:inherit;
}
@media (min-width:400px){[role=tab]{font-size:.82rem;letter-spacing:.05em;padding:0 8px}}
@media (min-width:760px){[role=tab]{font-size:.9rem;padding:0 24px}}
[role=tab]:hover{color:#fff;text-decoration:none;background:rgba(255,255,255,.06)}
[role=tab][aria-selected=true]{color:#241f10;background:var(--orange);border-color:var(--orange)}

/* ---------- panels ---------- */
[role=tabpanel]{padding:22px 0 8px;scroll-margin-top:calc(var(--nav-h) + 8px)}
.panel-head{margin:0 0 4px;font-size:1.4rem;line-height:1.2}
.panel-sub{margin:0 0 20px;color:var(--muted);font-size:.92rem}

/* ---------- hero ---------- */
.hero{
  position:relative;text-align:center;
  padding:34px 18px 38px;margin-bottom:6px;
  border-radius:16px;overflow:hidden;background:var(--bg);
}
/* Full-bleed: cancel the .wrap padding and the centred max-width so the photo
   runs edge to edge. body has overflow-x:hidden, so no sideways scroll. */
.hero.has-photo{
  margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);
  width:100vw;max-width:100vw;border-radius:0;
}
/* The photo sits behind a navy scrim so white text stays legible over it and
   the bottom edge fades into the page. Phones get the 900px file. */
.hero.has-photo::before{
  content:'';position:absolute;inset:0;z-index:0;
  background-image:
    linear-gradient(180deg, rgba(35,37,55,.62) 0%, rgba(38,40,59,.78) 55%,
                    rgba(48,50,73,.96) 100%),
    var(--hero-sm);
  background-size:cover;background-position:center 38%;
}
@media (min-width:900px){
  .hero.has-photo::before{background-image:
    linear-gradient(180deg, rgba(35,37,55,.62) 0%, rgba(38,40,59,.78) 55%,
                    rgba(48,50,73,.96) 100%),
    var(--hero-lg);}
}
.hero > *{position:relative;z-index:1}
.hero.has-photo{padding:44px 18px 46px}
.hero.has-photo h1,.hero.has-photo .meta{text-shadow:0 2px 14px rgba(0,0,0,.5)}
.hero img{width:min(260px,68vw);height:auto;margin:0 auto 18px;display:block}
.hero.has-photo img{filter:drop-shadow(0 3px 18px rgba(0,0,0,.5))}
.hero h1{margin:0 0 12px;font-size:clamp(1.35rem,5.4vw,2.3rem);line-height:1.18}
.hero .meta{margin:0 auto 22px;color:var(--text);font-size:1rem;max-width:34ch}
.hero .meta b{display:block;font-size:1.1rem;letter-spacing:.02em}
.hero .meta span{color:var(--muted)}
.hero.has-photo .meta span{color:#E4E6F2}
.cta{
  display:inline-flex;align-items:center;gap:8px;min-height:50px;padding:0 26px;
  border-radius:999px;background:var(--orange);color:#241f10;
  font-weight:700;font-size:1rem;text-transform:uppercase;letter-spacing:.04em;
}
.cta:hover{background:#ffa61f;text-decoration:none}
.cta svg{width:15px;height:15px;fill:currentColor;flex:0 0 auto}

/* ---------- schedule ---------- */
.slot{
  display:grid;grid-template-columns:84px minmax(0,1fr);gap:8px;
  padding:12px 0;border-top:1px solid var(--line);
}
@media (min-width:760px){.slot{grid-template-columns:112px minmax(0,1fr);gap:18px;padding:14px 0}}
/* nowrap + a column wide enough for the longest label, so every time sits on
   one line — a mix of one- and two-line times looked ragged. */
.slot-time{
  font-weight:700;font-size:.72rem;color:var(--orange);line-height:1.35;
  padding-top:12px;white-space:nowrap;font-variant-numeric:tabular-nums;
}
@media (min-width:760px){.slot-time{font-size:.9rem;padding-top:11px}}
.rooms{display:grid;gap:10px;grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.rooms{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:12px 14px;min-width:0;
}
.card.clickable{cursor:pointer}
.card.star,.card.plenary{border-left:3px solid var(--orange)}
.card.avalon{border-left:3px solid var(--orange)}
.card.break,.card.logistics,.card.remarks{border-left:3px solid var(--line-strong)}
/* Room and section labels are always orange. */
.room,.kicker{
  font-size:.64rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;
  color:var(--orange);display:block;margin-bottom:5px;
}
.card .title{display:block;font-weight:700;font-size:.92rem;line-height:1.35;
  color:var(--text);margin:0 0 6px;text-transform:uppercase;letter-spacing:.02em}
a.title:hover{color:var(--orange);text-decoration:none}
/* Non-breaking space binds the chevron to the last word, so it can never
   wrap onto a line by itself. */
a.title::after{content:'\\00A0\\203A';color:var(--orange);font-weight:700}
.card .who{font-size:.87rem;color:var(--text);margin:0;line-height:1.6}
.card .who a{color:var(--text);text-decoration:underline;
  text-decoration-color:rgba(255,255,255,.4);text-underline-offset:2px}
.card .who a:hover{color:var(--orange);text-decoration-color:var(--orange)}
.card .who .note{color:var(--text)}
.card .detail{font-size:.87rem;color:var(--text);margin:0}
.card .topics{margin-top:8px}

/* Speaker headshot inline with their name — a name alone means nothing to
   someone who has never met them; a face at least makes them a person before
   the reader has tapped through. Shared by the Schedule and Sessions tabs.
   inline-flex so each name+photo wraps together as one unit, never splitting
   the avatar from its name mid-line. */
.who-link{display:inline-flex;align-items:center;gap:6px;vertical-align:-6px}
.who-avatar{
  width:20px;height:20px;border-radius:50%;object-fit:cover;flex:0 0 auto;
  border:1px solid rgba(255,255,255,.28);background:var(--surface-2);
}
.session .who-link{vertical-align:-7px}
.session .who-avatar{width:24px;height:24px}

/* ---------- badges ---------- */
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.badge{
  font-size:.64rem;text-transform:uppercase;letter-spacing:.09em;font-weight:700;
  padding:4px 9px;border-radius:999px;border:1px solid var(--line-strong);
  color:var(--muted);white-space:nowrap;
}
.badge.room-b{color:var(--orange);border-color:rgba(244,148,4,.5);background:rgba(244,148,4,.09)}
.badge.plenary{color:#241f10;background:var(--orange);border-color:var(--orange)}
.badge.panel{color:#ffd9a0;border-color:rgba(244,148,4,.45)}
.badge.intl{color:#9fe3c4;border-color:rgba(159,227,196,.45);background:rgba(159,227,196,.09)}
.badge.time{color:var(--text);border-color:var(--line-strong);letter-spacing:.04em}
.badge.topic{color:#c9d8ff;border-color:rgba(201,216,255,.35);background:rgba(201,216,255,.07)}

/* ---------- filters: native selects, compact on a phone ---------- */
.filters{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px;margin:0 0 16px;display:grid;gap:12px;grid-template-columns:minmax(0,1fr);
}
@media (min-width:700px){.filters{grid-template-columns:repeat(3,minmax(0,1fr))}}
.fgroup{display:flex;flex-direction:column;gap:6px;min-width:0}
.flabel{
  font-size:.64rem;text-transform:uppercase;letter-spacing:.1em;
  font-weight:700;color:var(--orange);
}
.fselect{position:relative}
/* Chevron drawn in CSS so the control matches in every browser. */
.fselect::after{
  content:'';position:absolute;right:14px;top:50%;width:8px;height:8px;
  border-right:2px solid var(--orange);border-bottom:2px solid var(--orange);
  transform:translateY(-70%) rotate(45deg);pointer-events:none;
}
.fselect select{
  appearance:none;-webkit-appearance:none;width:100%;min-height:46px;
  padding:0 38px 0 14px;border-radius:9px;
  border:1px solid var(--line-strong);background:rgba(0,0,0,.18);color:var(--text);
  font-family:inherit;font-size:.9rem;font-weight:600;cursor:pointer;
}
.fselect select:hover{border-color:var(--muted)}
.fselect select:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
/* Native dropdown lists render with the OS palette, so force readable colours. */
.fselect option{background:#3D3F5A;color:#fff}
.fresult{display:flex;align-items:center;gap:12px;margin:0 0 16px;
  font-size:.85rem;color:var(--muted)}
.fclear{
  background:none;border:1px solid var(--line-strong);color:var(--muted);
  font-family:inherit;font-size:.75rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.06em;padding:7px 12px;border-radius:999px;cursor:pointer;min-height:36px;
}
.fclear:hover{color:#fff;border-color:#fff}
.empty{
  background:var(--surface);border:1px dashed var(--line-strong);
  border-radius:var(--radius);padding:28px;text-align:center;color:var(--muted);
}

/* ---------- session cards ---------- */
.sessions{display:grid;gap:14px}
.session{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px;scroll-margin-top:calc(var(--nav-h) + 14px);
}
@media (min-width:760px){.session{padding:22px 24px}}
.session h3{margin:0 0 10px;color:var(--orange);font-size:1.05rem;line-height:1.3}
@media (min-width:760px){.session h3{font-size:1.2rem}}
.session .who{font-size:.92rem;color:var(--text);margin:0 0 12px}
.session .who a{color:var(--text);font-weight:600;text-decoration:underline;
  text-decoration-color:rgba(255,255,255,.4);text-underline-offset:2px}
.session .who a:hover{color:var(--orange);text-decoration-color:var(--orange)}
.session .who .note{color:var(--text);font-weight:400}
.session p.desc{margin:0;color:var(--text);font-size:.95rem}

/* ---------- speakers ---------- */
.speakers{display:grid;gap:14px;grid-template-columns:minmax(0,1fr)}
@media (min-width:560px){.speakers{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:900px){.speakers{grid-template-columns:repeat(3,minmax(0,1fr))}}
.spk{
  background:var(--surface);border:1px solid rgba(244,148,4,.26);
  border-radius:var(--radius);
  padding:20px 18px;text-align:center;display:flex;flex-direction:column;align-items:center;
  scroll-margin-top:calc(var(--nav-h) + 14px);
  transition:border-color .15s, background-color .15s;
}
.spk{cursor:pointer}
.spk:hover{border-color:var(--orange);background:var(--surface-2)}
.spk img{
  width:120px;height:120px;border-radius:50%;object-fit:cover;object-position:50% 50%;
  border:2px solid rgba(244,148,4,.45);background:var(--surface-2);margin-bottom:14px;
}
.spk:hover img{border-color:var(--orange)}
.spk h3{margin:0 0 5px;font-size:1rem;line-height:1.3}
.spk .role{margin:0;color:var(--muted);font-size:.85rem;line-height:1.45}
.spk .org{margin:0;color:var(--text);font-size:.85rem;font-weight:600;line-height:1.45}
.spk .in-session{margin:10px 0 0;font-size:.8rem;line-height:1.4}
.spk .in-session a{color:var(--orange);font-weight:600;text-decoration:none}
.spk .in-session a:hover{color:var(--text);text-decoration:underline;
  text-underline-offset:2px}
.spk .in-session .note{display:block;color:var(--muted);font-size:.76rem}
.spk .pending-note{margin:8px 0 0;color:var(--muted);font-size:.8rem;font-style:italic}
.actions{margin-top:auto;padding-top:16px;display:flex;gap:8px;
  justify-content:center;flex-wrap:wrap;width:100%}
.learn-btn{
  background:none;border:1px solid var(--line-strong);color:var(--muted);
  font-family:inherit;font-size:.75rem;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;padding:9px 15px;border-radius:999px;cursor:pointer;min-height:44px;
}
.learn-btn:hover{color:var(--orange);border-color:rgba(244,148,4,.5)}
.li{
  display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:44px;
  padding:0 16px;border-radius:999px;border:1px solid var(--line-strong);color:var(--muted);
  font-size:.78rem;font-weight:600;
}
.li:hover{color:#fff;border-color:#0A66C2;background:#0A66C2;text-decoration:none}
.li svg{width:14px;height:14px;fill:currentColor}

/* Inline detail is the no-JS fallback; with JS it moves into the modal. */
.spk-detail{margin:14px 0 0;text-align:left;border-top:1px solid var(--line);
  padding-top:12px;width:100%}
html.js .spk-detail{display:none}
html:not(.js) .learn-btn{display:none}
.spk-detail .bio{margin:0;font-size:.88rem;color:var(--text)}

/* ---------- speaker modal ---------- */
.modal{position:fixed;inset:0;z-index:90;display:flex;align-items:flex-end;
  justify-content:center;
  /* Keep the card clear of the phone browser's URL bar, or the close button
     ends up underneath it and is nearly untappable. */
  padding:calc(84px + env(safe-area-inset-top)) 0 0}
@media (min-width:640px){.modal{align-items:center;padding:88px 24px 24px}}
.modal-backdrop{position:absolute;inset:0;background:rgba(16,17,26,.72);
  backdrop-filter:blur(3px)}
.modal-card{
  position:relative;background:var(--surface);border:1px solid var(--line-strong);
  border-radius:16px 16px 0 0;width:100%;max-width:560px;
  max-height:100%;
  overflow-y:auto;padding:26px 20px calc(24px + env(safe-area-inset-bottom));
  text-align:center;-webkit-overflow-scrolling:touch;
}
@media (min-width:640px){.modal-card{border-radius:16px;padding:30px 32px 28px;max-height:86vh}}
.modal-x{
  position:absolute;top:10px;right:10px;width:40px;height:40px;border-radius:50%;
  border:1px solid var(--line-strong);background:rgba(0,0,0,.25);color:#fff;
  font-size:1.35rem;line-height:1;cursor:pointer;font-family:inherit;
}
.modal-x:hover{background:var(--orange);color:#241f10;border-color:var(--orange)}
#modal-img{width:150px;height:150px;border-radius:50%;object-fit:cover;
  border:3px solid rgba(255,255,255,.18);margin:4px auto 16px;display:block}
#modal-name{margin:0 0 6px;font-size:1.2rem;line-height:1.25}
#modal-role{margin:0;color:var(--muted);font-size:.9rem}
#modal-org{margin:0 0 4px;color:var(--text);font-size:.9rem;font-weight:600}
#modal-badges{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:10px 0 0}
#modal-badges:empty{display:none}
#modal-body{text-align:left;margin-top:18px}
#modal-body .bio{margin:0;font-size:.92rem;color:var(--text);line-height:1.6}
#modal-body .bio + .bio{margin-top:12px}
.spk-detail .bio + .bio{margin-top:10px}
#modal-body .in-session{margin:0 0 16px;padding:12px 14px;background:rgba(0,0,0,.16);
  border-left:3px solid var(--orange);border-radius:8px;font-size:.88rem}
#modal-body .in-session a{color:var(--orange);font-weight:700;text-decoration:none}
#modal-body .in-session a:hover{color:var(--text);text-decoration:underline;
  text-underline-offset:2px}
#modal-body .in-session .note{color:var(--muted)}
.modal-foot{margin-top:20px}
html.modal-open,html.modal-open body{overflow:hidden}

/* ---------- pulse on deep-link arrival ---------- */
@keyframes pulse{
  0%,100%{box-shadow:0 0 0 0 rgba(244,148,4,0)}
  18%{box-shadow:0 0 0 4px rgba(244,148,4,.55)}
  70%{box-shadow:0 0 0 4px rgba(244,148,4,.30)}
}
.pulse{animation:pulse 1.6s ease-out}
@media (prefers-reduced-motion:reduce){.pulse{animation:none;outline:3px solid var(--orange)}}

/* ---------- back pill ---------- */
#backpill{
  position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:100;
  display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 20px;
  border-radius:999px;border:1px solid rgba(0,0,0,.2);
  background:var(--orange);color:#241f10;font-family:inherit;font-weight:700;
  font-size:.88rem;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.4);
  text-transform:uppercase;letter-spacing:.04em;
}
#backpill:hover{background:#ffa61f}
/* With a profile open, the pill moves into the empty strip above the card, so
   it stays reachable without covering the card's own content. */
html.modal-open #backpill{
  bottom:auto;top:calc(env(safe-area-inset-top) + 18px);
}

/* ---------- on-the-day info ---------- */
.info-when{
  background:var(--surface);border:1px solid var(--line);
  border-left:3px solid var(--orange);border-radius:var(--radius);
  padding:14px 16px;margin:0 0 16px;
}
.info-when b{display:block;font-size:1.05rem;letter-spacing:.02em}
.info-when span{color:var(--muted);font-size:.9rem}
.info-grid{display:grid;gap:14px;grid-template-columns:minmax(0,1fr)}
@media (min-width:700px){.info-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
.info-card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px;
}
.info-card h3{margin:0 0 10px;color:var(--orange);font-size:.95rem;line-height:1.3}
.info-card p{margin:0 0 10px;font-size:.92rem;color:var(--text)}
.info-card p:last-child{margin-bottom:0}
.info-card a{color:var(--orange);text-decoration:underline;text-underline-offset:2px}
.info-list{margin:0 0 12px;padding:0;list-style:none}
.info-list li{position:relative;padding-left:18px;font-size:.92rem;margin-bottom:6px}
.info-list li::before{content:'';position:absolute;left:0;top:.55em;width:7px;height:7px;
  border-radius:50%;background:var(--orange)}
.info-card .hashtag{color:var(--orange);font-weight:700;letter-spacing:.04em}
.info-link{
  display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:0 16px;
  margin-top:4px;border-radius:999px;border:1px solid rgba(244,148,4,.5);
  color:var(--orange);font-size:.8rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.05em;text-decoration:none;
}
.info-link:hover{background:var(--orange);color:#241f10;text-decoration:none}
.info-link svg{width:13px;height:13px;fill:currentColor}
/* Wraps on a phone, which is fine; sits on one line from tablet up. */
.info-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
@media (min-width:700px){
  .info-links{flex-wrap:nowrap}
  .info-links .info-link{padding:0 12px;font-size:.74rem;letter-spacing:.03em}
}
.info-links .info-link{margin-top:0}
.info-outro{
  margin:20px 0 0;text-align:center;color:var(--text);font-size:.95rem;font-weight:600;
}

/* ---------- sponsors ----------
   One white panel, not nine tiles. White specifically: Donorbox and Downes
   Murray have opaque white backgrounds baked in, so they only sit seamlessly on
   white, while Turning Point's is opaque dark navy and reads as a dark logo.
   Nine logos divide evenly into 3x3, so there is no orphan row. */
.sponsors-wrap{margin-top:46px;padding:30px 0 34px;background:#fff;border-radius:16px}
.sponsors-wrap h2{
  margin:0 0 22px;text-align:center;font-size:.95rem;color:#303249;letter-spacing:.06em;
}
/* Centred flex rather than a fixed grid: the last row centres itself whatever
   the sponsor count is, so adding one does not leave a ragged row. */
.sponsors{
  display:flex;flex-wrap:wrap;justify-content:center;align-items:stretch;
  gap:4px;list-style:none;margin:0;padding:0 12px;
}
.sponsors li{flex:0 0 calc(50% - 4px);display:flex}
@media (min-width:640px){
  .sponsors{gap:10px;padding:0 24px}
  .sponsors li{flex:0 0 calc(33.333% - 10px)}
}
@media (min-width:900px){.sponsors li{flex:0 0 calc(25% - 10px)}}
.sponsors a{
  flex:1;display:flex;align-items:center;justify-content:center;
  min-height:92px;padding:10px 12px;border-radius:8px;
}
@media (min-width:640px){.sponsors a{min-height:110px;padding:14px 16px}}
.sponsors a:hover{background:#F2F3F8;text-decoration:none}
.sponsors a:focus-visible{outline:3px solid var(--orange);outline-offset:-2px}
/* Wide wordmarks hit the width cap; the stacked (Homecoming Centre) and square
   (Cooktastic) logos hit the height cap, so it has to be generous or they end up
   a third the size of everything else. */
.sponsors img{max-height:56px;max-width:100%;width:auto;height:auto;display:block}
@media (min-width:640px){.sponsors img{max-height:66px}}
.sponsors a.tall img{max-height:82px}
@media (min-width:640px){.sponsors a.tall img{max-height:96px}}

footer{
  border-top:1px solid var(--line);padding:38px 0 36px;
  text-align:center;color:var(--muted);font-size:.84rem;
}
/* Needs to out-specify .wrap's "margin:0 auto", which would zero this out. */
footer.wrap{margin-top:44px}
footer p{margin:0 0 10px}
footer .tickets{color:var(--orange);font-weight:700;text-decoration:underline;
  text-underline-offset:2px}
footer .tickets:hover{color:#ffa61f}
footer .credit{font-size:.78rem;opacity:.8}
footer .credit a{color:var(--muted);text-decoration:underline}
footer .credit a:hover{color:var(--orange)}
"""

# ---------------------------------------------------------------------------
# JS
# ---------------------------------------------------------------------------

TRACK_JS = """
  /* ------------- usage tracking: aggregate counts, no identifiers -------------
     Buffers events and flushes on a timer and on page-hide, so a visitor tapping
     round the schedule costs a handful of requests rather than one per tap.
     The session id is random and lives in memory only — never stored, so it
     resets on reload and identifies nobody. */
  var TRACK_URL = '__TRACK_URL__';
  var tq = [], tsid = Math.random().toString(36).slice(2, 10), ttimer = null;

  // ?shawn on the URL (or in a previous history entry this tab visited, since
  // switching tabs rewrites the URL via pushState) suppresses tracking, so
  // Shawn's own browsing — and anyone's manual QA of the live site — never
  // pollutes real usage data. Persisted in sessionStorage so it survives
  // navigating around after landing on the ?shawn link.
  var PREVIEW = /[?&]shawn(?:&|=|$)/.test(location.search);
  try {
    if(PREVIEW) sessionStorage.setItem('ifc_preview', '1');
    else if(sessionStorage.getItem('ifc_preview') === '1') PREVIEW = true;
  } catch(err){ /* private browsing: falls back to the URL check above only */ }

  function flushTrack(){
    if(ttimer){ clearTimeout(ttimer); ttimer = null; }
    if(!tq.length) return;
    var body = JSON.stringify({ sid: tsid, events: tq });
    tq = [];
    if(PREVIEW) return;   // drop the batch — preview mode never sends
    try { if(navigator.sendBeacon && navigator.sendBeacon(TRACK_URL, body)) return; }
    catch(err){}
    try { fetch(TRACK_URL, { method:'POST', mode:'no-cors', keepalive:true, body:body }); }
    catch(err){}
  }
  function track(type, target){
    if(PREVIEW) return;
    tq.push({ t: Date.now(), type: type, target: String(target || '').slice(0, 80) });
    if(tq.length >= 12){ flushTrack(); return; }
    if(!ttimer) ttimer = setTimeout(flushTrack, 5000);
  }
  window.addEventListener('pagehide', flushTrack);
  document.addEventListener('visibilitychange', function(){
    if(document.visibilityState === 'hidden') flushTrack();
  });
  // Every outbound link is recorded, labelled by what the visitor actually saw
  // (link text, or a sponsor logo's alt text), so "did anyone click the train
  // schedule / a sponsor / ShawnLife" is answerable.
  function outLabel(a){
    var t = (a.textContent || '').replace(/\\s+/g, ' ').trim();
    if(!t){ var img = a.querySelector('img'); t = img ? (img.alt || '') : ''; }
    if(!t){ try { t = new URL(a.href).hostname; } catch(err){ t = a.href; } }
    return t;
  }
  document.addEventListener('click', function(ev){
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href^="http"]') : null;
    if(!a) return;
    if(a.href.indexOf('qkt.io') > -1){ track('ticket', ''); return; }
    if(a.classList.contains('li')){
      // Record whose profile, not the word "LinkedIn".
      var card = a.closest('.spk');
      var who = card ? card.getAttribute('data-name')
        : (document.getElementById('modal-name').textContent || '').trim();
      track('linkedin', who);
      return;
    }
    track('outbound', outLabel(a));
  });
  track('visit', '');
"""

JS = """
(function(){
  var root = document.documentElement;
  root.classList.add('js');
__TRACK_BLOCK__

  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role=tab]'));
  if(!tabs.length) return;
  var panels = tabs.map(function(t){ return document.getElementById(t.getAttribute('aria-controls')); });
  var pill = document.getElementById('backpill');
  var pillText = document.getElementById('backpill-text');
  var ret = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function labelFor(id){
    for(var i=0;i<tabs.length;i++){
      if(tabs[i].getAttribute('aria-controls') === id) return tabs[i].getAttribute('data-label');
    }
    return 'Schedule';
  }
  function currentPanel(){
    for(var i=0;i<panels.length;i++){ if(!panels[i].hidden) return panels[i]; }
    return panels[0];
  }
  function panelOf(el){
    while(el && el.getAttribute){
      if(el.getAttribute('role') === 'tabpanel') return el;
      el = el.parentNode;
    }
    return null;
  }
  function activate(id){
    for(var i=0;i<tabs.length;i++){
      var on = tabs[i].getAttribute('aria-controls') === id;
      tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
      tabs[i].tabIndex = on ? 0 : -1;
      panels[i].hidden = !on;
    }
  }
  function showPill(fromId){
    ret = { id: fromId, y: window.pageYOffset || 0 };
    pillText.textContent = 'Back to ' + labelFor(fromId);
    pill.hidden = false;
  }
  function hidePill(){ pill.hidden = true; ret = null; }
  function pulse(el){
    el.classList.remove('pulse');
    void el.offsetWidth;
    el.classList.add('pulse');
    setTimeout(function(){ el.classList.remove('pulse'); }, 1700);
  }

  // Without JS every panel stays visible, so the page reads as one long
  // document. Now that JS is running, collapse it into real tabs.
  activate(panels[0].id);

  /* ---------------- speaker modal ---------------- */
  var modal = document.getElementById('modal');
  var mImg = document.getElementById('modal-img');
  var mName = document.getElementById('modal-name');
  var mRole = document.getElementById('modal-role');
  var mOrg = document.getElementById('modal-org');
  var mBadges = document.getElementById('modal-badges');
  var mBody = document.getElementById('modal-body');
  var mLi = document.getElementById('modal-li');
  var mClose = modal.querySelector('.modal-x');
  var lastFocus = null;

  function openModal(card){
    var detail = card.querySelector('.spk-detail');
    mImg.src = card.getAttribute('data-img');
    mImg.alt = card.getAttribute('data-name');
    mName.textContent = card.getAttribute('data-name');
    mRole.textContent = card.getAttribute('data-role');
    mOrg.textContent = card.getAttribute('data-org');
    mBadges.innerHTML = card.getAttribute('data-intl') === '1'
      ? '<span class="badge intl">International Speaker</span>' : '';
    mBody.innerHTML = detail ? detail.innerHTML : '';
    mLi.href = card.getAttribute('data-linkedin');
    track('speaker', card.id);
    lastFocus = document.activeElement;
    modal.hidden = false;
    root.classList.add('modal-open');
    mClose.focus();
  }
  function closeModal(){
    if(modal.hidden) return;
    modal.hidden = true;
    root.classList.remove('modal-open');
    if(lastFocus && lastFocus.focus) lastFocus.focus();
    lastFocus = null;
  }
  function modalOpen(){ return !modal.hidden; }

  document.addEventListener('click', function(ev){
    var t = ev.target;
    if(!t || !t.closest) return;
    if(t.closest('[data-close]')){ ev.preventDefault(); closeModal(); return; }
    var btn = t.closest('.learn-btn');
    if(btn){ openModal(btn.closest('.spk')); return; }
    // Anywhere on a speaker card opens the profile — except the real links on it
    // (LinkedIn, and the session title), which do their own thing.
    var card = t.closest('.spk');
    if(card && !t.closest('a')){ openModal(card); return; }
    // Same for a schedule box: tapping it anywhere opens that session. Delegates
    // to the title link so the tab-switch, history and back-pill logic is shared.
    var slot = t.closest('.card.clickable');
    if(slot && !t.closest('a')){
      var link = slot.querySelector('a.title');
      if(link) link.click();
    }
  });
  document.addEventListener('keydown', function(ev){
    if(!modalOpen()) return;
    if(ev.key === 'Escape'){ ev.preventDefault(); closeModal(); return; }
    if(ev.key !== 'Tab') return;
    // Keep focus inside the dialog.
    var f = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    f = Array.prototype.filter.call(f, function(el){ return el.offsetParent !== null; });
    if(!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if(ev.shiftKey && document.activeElement === first){ ev.preventDefault(); last.focus(); }
    else if(!ev.shiftKey && document.activeElement === last){ ev.preventDefault(); first.focus(); }
  });

  /* ---------------- navigation ---------------- */
  function goTo(target, withModal){
    var p = panelOf(target);
    if(!p) return;
    if(p !== currentPanel()) activate(p.id);
    if(target.classList.contains('session')) track('session', target.id);
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block:'start' });
    if(withModal && target.classList.contains('spk')){
      setTimeout(function(){ openModal(target); }, reduce ? 0 : 260);
    } else {
      pulse(target);
    }
  }

  tabs.forEach(function(tab, i){
    tab.addEventListener('click', function(ev){
      ev.preventDefault();
      track('tab', tab.getAttribute('data-label'));
      closeModal();
      activate(tab.getAttribute('aria-controls'));
      hidePill();
      if(location.hash) history.replaceState(null, '', location.pathname + location.search);
      window.scrollTo(0, 0);
      tab.focus();
    });
    tab.addEventListener('keydown', function(ev){
      var n = null;
      if(ev.key === 'ArrowRight') n = (i + 1) % tabs.length;
      else if(ev.key === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
      else if(ev.key === 'Home') n = 0;
      else if(ev.key === 'End') n = tabs.length - 1;
      if(n === null) return;
      ev.preventDefault();
      tabs[n].click();
    });
  });

  document.addEventListener('click', function(ev){
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href^="#"]') : null;
    if(!a || a.getAttribute('role') === 'tab') return;
    var id = a.getAttribute('href').slice(1);
    if(!id) return;
    var target = document.getElementById(id);
    if(!target) return;
    if(!panelOf(target)) return;
    ev.preventDefault();
    var cameFromModal = !!a.closest('#modal');
    if(cameFromModal) closeModal();
    var cur = currentPanel();
    var dest = panelOf(target);
    if(dest !== cur) showPill(cur.id);
    history.pushState(null, '', '#' + id);
    // Tapping a speaker's name opens their profile, which is the point of the tap.
    goTo(target, true);
  });

  pill.addEventListener('click', function(){
    if(!ret){ hidePill(); return; }
    var back = ret;
    closeModal();
    activate(back.id);
    hidePill();
    history.pushState(null, '', location.pathname + location.search);
    window.scrollTo(0, back.y);
  });

  function syncFromHash(){
    var id = location.hash.replace(/^#/, '');
    if(!id) return false;
    var target = document.getElementById(id);
    if(!target || !panelOf(target)) return false;
    goTo(target, true);
    return true;
  }
  window.addEventListener('popstate', function(){
    closeModal();
    if(!syncFromHash()) hidePill();
  });

  /* ---------------- session filters ---------------- */
  var state = { room:'all', time:'all', topic:'all' };
  var cards = Array.prototype.slice.call(document.querySelectorAll('.session'));
  var countEl = document.getElementById('fcount');
  var emptyEl = document.getElementById('fempty');
  var clearBtn = document.getElementById('fclear');

  function applyFilters(){
    var shown = 0;
    cards.forEach(function(c){
      var okRoom = state.room === 'all' || c.getAttribute('data-room') === state.room;
      var okTime = state.time === 'all' || c.getAttribute('data-time') === state.time;
      var okTopic = state.topic === 'all' ||
        ('|' + c.getAttribute('data-topics') + '|').indexOf('|' + state.topic + '|') > -1;
      var on = okRoom && okTime && okTopic;
      c.hidden = !on;
      if(on) shown++;
    });
    countEl.textContent = shown === cards.length
      ? cards.length + ' sessions'
      : shown + ' of ' + cards.length + ' sessions';
    emptyEl.hidden = shown > 0;
    var active = state.room !== 'all' || state.time !== 'all' || state.topic !== 'all';
    clearBtn.hidden = !active;
  }

  var selects = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  selects.forEach(function(sel){
    sel.addEventListener('change', function(){
      var key = sel.getAttribute('data-filter');
      state[key] = sel.value;
      track('filter', key + ':' + sel.value);
      applyFilters();
    });
  });
  if(clearBtn) clearBtn.addEventListener('click', function(){
    state = { room:'all', time:'all', topic:'all' };
    selects.forEach(function(sel){ sel.value = 'all'; });
    applyFilters();
  });
  if(cards.length) applyFilters();

  /* ---------------- contact address, assembled at runtime ---------------- */
  var mail = document.getElementById('email-link');
  if(mail){
    var addr = mail.getAttribute('data-u') + String.fromCharCode(64) + mail.getAttribute('data-h');
    mail.href = 'mailto:' + addr + '?subject=' +
      encodeURIComponent('IFC Cape Town Pop-Up 2026');
  }

  /* ---------------- deep link from a QR or shared link ---------------- */
  if(location.hash) syncFromHash();
})();
"""

LINKEDIN_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.45 20.45h'
    '-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.5'
    '6h.05c.47-.9 1.63-1.85 3.36-1.85 3.59 0 4.26 2.37 4.26 5.45v6.29zM5.34 7.43a2.07 2.07'
    ' 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 '
    '0 0 .78 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .78 '
    '23.2 0 22.22 0z"/></svg>'
)

EXT_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14 3v2h'
           '3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7zM5 5h5V3H3v18h18v-7h-2v5H5V5z"/></svg>')


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def speaker_links(pairs):
    """Renders speaker names as links, each with a small circular headshot —
    used on both the Schedule and Sessions tabs, so a name is never just text
    with no face attached to it."""
    out = []
    for slug, note in pairs:
        if slug not in BY_SLUG:
            sys.exit(f"Unknown speaker slug in a session: {slug!r}")
        sp = BY_SLUG[slug]
        avatar = (f'<img class="who-avatar" src="assets/images/headshots/{sp["slug"]}.jpg" '
                 f'width="24" height="24" loading="lazy" decoding="async" alt="">')
        bit = f'<a class="who-link" href="#{sp["slug"]}">{avatar}{e(sp["name"])}</a>'
        if note:
            bit += f' <span class="note">({e(note)})</span>'
        out.append(bit)
    if len(out) > 1:
        return ", ".join(out[:-1]) + " &amp; " + out[-1]
    return out[0] if out else ""


def bio_html(bio):
    """A bio is either one string or a list of paragraphs."""
    paras = [bio] if isinstance(bio, str) else list(bio)
    return "".join(f'<p class="bio">{e(p)}</p>' for p in paras)


def topic_badges(anchor):
    return "".join(f'<span class="badge topic">{e(t)}</span>' for t in topics_of(anchor))


def render_schedule_item(item, room_class=None, room_label=None):
    classes = ["card"]
    if room_class:
        classes.append(room_class)

    if "session" in item:
        s = BY_ANCHOR[item["session"]]
        classes.append("clickable")
        if item.get("flavour") == "plenary" or s.get("plenary"):
            classes.append("plenary")
        # Full-width plenaries keep their "OPENING PLENARY · STAR THEATRE" kicker.
        head = (f'<span class="room">{e(room_label)}</span>' if room_label
                else f'<span class="kicker">{e(s["label"])} &middot; {e(s["room"])}</span>')
        who = (f'<p class="who">{speaker_links(s["speakers"])}</p>'
               if s["speakers"] else "")
        return (
            f'<div class="{" ".join(classes)}">{head}'
            f'<a class="title" href="#{s["anchor"]}">{e(s["title"])}</a>{who}</div>'
        )

    classes.append(item["flavour"])
    detail = (f'<p class="detail">{e(item["detail"])}</p>' if item.get("detail") else "")
    return (f'<div class="{" ".join(classes)}">'
            f'<span class="title">{e(item["name"])}</span>{detail}</div>')


def render_schedule():
    rows = []
    for slot in D.SCHEDULE:
        if slot["kind"] == "full":
            body = render_schedule_item(slot["item"])
        else:
            body = ('<div class="rooms">'
                    + render_schedule_item(slot["star"], "star", D.STAR)
                    + render_schedule_item(slot["avalon"], "avalon", D.AVALON)
                    + '</div>')
        rows.append(
            f'<div class="slot"><div class="slot-time">{e(slot["time"])}</div>'
            f'<div class="slot-body">{body}</div></div>'
        )

    ev, logo = D.EVENT, D.EVENT["logo"]
    photo = ev.get("hero")
    hero_cls = "hero has-photo" if photo else "hero"
    style = ""
    if photo:
        style = (f' style="--hero-sm:url(assets/images/hero/{photo}-900.jpg);'
                 f'--hero-lg:url(assets/images/hero/{photo}-1800.jpg)"')
    hero = f"""
    <div class="{hero_cls}"{style}>
      <img src="assets/images/{e(logo['file'])}" width="{logo['w']}" height="{logo['h']}"
           alt="IFC Cape Town Pop-Up 2026">
      <h1>{e(ev['headline'])}</h1>
      <p class="meta"><b>{e(ev['date'])}</b><span>{e(ev['venue'])}</span></p>
      <a class="cta" href="{e(ev['tickets_url'])}" target="_blank" rel="noopener">
        Get Your Tickets {EXT_SVG}</a>
    </div>"""

    return (hero
            + '<h2 class="panel-head">Programme</h2>'
            + '<p class="panel-sub">Tap any session title or speaker name for the full '
              'details.</p>'
            + '<div class="schedule">' + "".join(rows) + '</div>')


def render_filters():
    def group(label, key, values, all_label):
        opts = [f'<option value="all">{all_label}</option>']
        opts += [f'<option value="{e(v)}">{e(v)}</option>' for v in values]
        return (f'<div class="fgroup">'
                f'<label class="flabel" for="f-{key}">{label}</label>'
                f'<div class="fselect"><select id="f-{key}" data-filter="{key}">'
                f'{"".join(opts)}</select></div></div>')

    return ('<div class="filters">'
            + group("Theatre", "room", ALL_ROOMS, "All theatres")
            + group("Time", "time", ALL_TIMES, "Any time")
            + group("Topic", "topic", ALL_TOPICS, "All topics")
            + '</div>'
            '<div class="fresult"><span id="fcount"></span>'
            '<button class="fclear" id="fclear" type="button" hidden>Clear filters</button>'
            '</div>')


def render_sessions():
    cards = []
    for s in D.SESSIONS:
        badges = [f'<span class="badge time">{e(s["time"])}</span>',
                  f'<span class="badge room-b">{e(s["room"])}</span>']
        if s.get("plenary"):
            badges.append('<span class="badge plenary">Plenary</span>')
        if s["anchor"] in D.PANELS:
            badges.append('<span class="badge panel">Panel</span>')
        badges.append(topic_badges(s["anchor"]))
        if any(BY_SLUG[slug].get("international") for slug, _ in s["speakers"]):
            badges.append('<span class="badge intl">International Speaker</span>')

        who = (f'<p class="who">{speaker_links(s["speakers"])}</p>'
               if s["speakers"] else "")

        cards.append(
            f'<article class="session" id="{s["anchor"]}" tabindex="-1" '
            f'data-room="{e(s["room"])}" data-time="{e(s["time"])}" '
            f'data-topics="{e("|".join(topics_of(s["anchor"])))}">'
            f'<div class="badges">{"".join(badges)}</div>'
            f'<h3>{e(s["title"])}</h3>'
            f'{who}<p class="desc">{e(s["description"])}</p></article>'
        )

    return ('<h2 class="panel-head">Sessions</h2>'
            f'<p class="panel-sub">{len(D.SESSIONS)} sessions across the Star and Avalon '
            'theatres. Filter below, or tap a speaker name for their profile.</p>'
            + render_filters()
            + '<div class="sessions">' + "".join(cards) + '</div>'
            + '<div class="empty" id="fempty" hidden>No sessions match those filters.</div>')


def session_lines(slug):
    """The 'Speaking in' block — same markup on the card and in the modal."""
    out = []
    for s in SESSIONS_FOR.get(slug, []):
        out.append(f'<a href="#{s["anchor"]}">{e(s["title"])}</a>'
                   f'<br><span class="note">{e(s["time"])} &middot; {e(s["room"])}</span>')
    if not out:
        return ""
    return '<p class="in-session">' + "<br>".join(out) + '</p>'   


def render_speakers():
    cards = []
    for sp in D.SPEAKERS:
        pending = sp["bio"] == D.BIO_PENDING
        sessions = session_lines(sp["slug"])

        linkedin = (f'<a class="li" href="{e(sp["linkedin"])}" target="_blank" rel="noopener">'
                    f'{LINKEDIN_SVG}<span>LinkedIn</span>'
                    f'<span class="sr"> profile for {e(sp["name"])} (opens in a new tab)</span>'
                    f'</a>')
        learn = ('<button class="learn-btn" type="button">Learn more</button>'
                 if not pending else "")
        note = f'<p class="pending-note">{e(sp["bio"])}</p>' if pending else ""

        # Detail block: shown inline without JS, moved into the modal with JS.
        detail = ""
        if not pending:
            detail = (f'<div class="spk-detail">{sessions}'
                      f'{bio_html(sp["bio"])}</div>')

        cards.append(
            f'<article class="spk" id="{sp["slug"]}" tabindex="-1" '
            f'data-name="{e(sp["name"])}" data-role="{e(sp["title"])}" '
            f'data-org="{e(sp["org"])}" data-linkedin="{e(sp["linkedin"])}" '
            f'data-img="assets/images/headshots/{sp["slug"]}.jpg" '
            f'data-intl="{"1" if sp.get("international") else "0"}">'
            f'<img src="assets/images/headshots/{sp["slug"]}.jpg" width="120" height="120" '
            f'loading="lazy" decoding="async" alt="{e(sp["name"])}">'
            f'<h3>{e(sp["name"])}</h3>'
            f'<p class="role">{e(sp["title"])}</p>'
            f'<p class="org">{e(sp["org"])}</p>'
            f'{sessions}{note}'
            f'<div class="actions">{learn}{linkedin}</div>'
            f'{detail}</article>'
        )

    return ('<h2 class="panel-head">Speakers</h2>'
            f'<p class="panel-sub">{len(D.SPEAKERS)} speakers, listed alphabetically. '
            'Tap “Learn more” for a full profile.</p>'
            '<div class="speakers">' + "".join(cards) + '</div>')


def render_info():
    blocks = []
    for b in D.INFO_BLOCKS:
        parts = []
        if b.get("items"):
            parts.append('<ul class="info-list">'
                         + "".join(f'<li>{e(i)}</li>' for i in b["items"])
                         + '</ul>')
        for p in b.get("body", []):
            parts.append(f'<p>{e(p)}</p>')
        if b.get("html"):
            # Authored above, not user input, so intentionally not escaped.
            parts.append(f'<p>{b["html"]}</p>')
        if b.get("hashtag"):
            parts.append(f'<p class="hashtag">{e(b["hashtag"])}</p>')
        if b.get("email"):
            # href is filled in by JS from two halves, so the plain address is
            # not sitting in the source for scrapers to harvest.
            parts.append(
                f'<a class="info-link" id="email-link" href="#" '
                f'data-u="{e(D.CONTACT_EMAIL_USER)}" data-h="{e(D.CONTACT_EMAIL_HOST)}">'
                f'Email us</a>'
                f'<noscript><p>{e(D.CONTACT_EMAIL_USER)} at '
                f'{e(D.CONTACT_EMAIL_HOST)}</p></noscript>')
        if b.get("links"):
            parts.append('<div class="info-links">' + "".join(
                f'<a class="info-link" href="{e(l["url"])}" target="_blank" '
                f'rel="noopener">{e(l["label"])} {EXT_SVG}</a>'
                for l in b["links"]) + '</div>')
        blocks.append(f'<section class="info-card"><h3>{e(b["heading"])}</h3>'
                      + "".join(parts) + '</section>')

    ev = D.EVENT
    return ('<h2 class="panel-head">On the Day</h2>'
            f'<p class="panel-sub">{e(D.INFO_INTRO)}</p>'
            f'<div class="info-when"><b>{e(ev["date"])}</b>'
            f'<span>{e(ev["venue"])}</span></div>'
            '<div class="info-grid">' + "".join(blocks) + '</div>'
            f'<p class="info-outro">{e(D.INFO_OUTRO)}</p>')


def render_sponsors():
    items = "".join(
        f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener" '
        f'title="{e(s["name"])} (opens in a new tab)">'
        f'<img src="assets/images/sponsors/{e(s["file"])}" width="{s["w"]}" height="{s["h"]}" '
        f'loading="lazy" decoding="async" alt="{e(s["name"])}"></a></li>'
        for s in D.SPONSORS
    )
    return ('<div class="sponsors-wrap"><h2>Thank You to Our Sponsors</h2>'
            f'<ul class="sponsors">{items}</ul></div>')


def render_modal():
    return f"""
<div class="modal" id="modal" hidden>
  <div class="modal-backdrop" data-close></div>
  <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-name">
    <button class="modal-x" type="button" data-close aria-label="Close profile">&times;</button>
    <img id="modal-img" alt="" width="150" height="150"
         src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
    <h3 id="modal-name"></h3>
    <p id="modal-role"></p>
    <p id="modal-org"></p>
    <div id="modal-badges"></div>
    <div id="modal-body"></div>
    <div class="modal-foot">
      <a class="li" id="modal-li" href="#" target="_blank" rel="noopener">
        {LINKEDIN_SVG}<span>View LinkedIn profile</span></a>
    </div>
  </div>
</div>"""


TABS = [("panel-schedule", "Schedule"), ("panel-sessions", "Sessions"),
        ("panel-speakers", "Speakers"), ("panel-info", "Info")]


def font_block():
    """Self-hosted Graphik. font-display:swap so text paints immediately in the
    system font and swaps when the woff2 lands."""
    faces = "\n".join(
        f"@font-face{{font-family:'Graphik';font-style:normal;font-weight:{w};"
        f"font-display:swap;src:url('assets/fonts/{f}') format('woff2')}}"
        for w, f in sorted(GRAPHIK.items()))
    # Preload only the two weights that appear above the fold.
    pre = "\n".join(
        f'<link rel="preload" href="assets/fonts/{GRAPHIK[w]}" as="font" '
        f'type="font/woff2" crossorigin>' for w in (400, 700))
    return f"{pre}\n<style>\n{faces}\n</style>"


def tracking_js():
    """Tracking code, or an inert no-op when ANALYTICS_URL is not configured."""
    url = getattr(D, "ANALYTICS_URL", None)
    if not url:
        return "  function track(){}   /* usage tracking not configured */"
    return TRACK_JS.replace("__TRACK_URL__", url)


def render_page():
    ev = D.EVENT
    tabs = "".join(
        f'<a role="tab" id="tab-{pid}" href="#{pid}" aria-controls="{pid}" '
        f'data-label="{label}" aria-selected="{"true" if i == 0 else "false"}" '
        f'tabindex="{0 if i == 0 else -1}">{label}</a>'
        for i, (pid, label) in enumerate(TABS)
    )
    panels = [("panel-schedule", render_schedule()),
              ("panel-sessions", render_sessions()),
              ("panel-speakers", render_speakers()),
              ("panel-info", render_info())]
    panels_html = "".join(
        f'<section role="tabpanel" id="{pid}" aria-labelledby="tab-{pid}" tabindex="0">'
        f'{body}</section>'
        for pid, body in panels
    )
    desc = (f"{ev['name']} — {ev['date']}, {ev['venue']}. "
            "Full programme, sessions and speakers.")

    # Read the real dimensions off the card rather than hardcoding them: the
    # supplied artwork may be any ratio, and wrong og:image:width/height makes
    # some scrapers lay the preview out badly.
    try:
        from PIL import Image
        with Image.open(ROOT / "assets" / "images" / "social-card.jpg") as _c:
            card_w, card_h = _c.size
    except Exception:
        card_w, card_h = 1200, 630

    # The hero is a CSS background, so it is discovered late. Preloading the size
    # that will actually be used keeps it as a fast LCP element.
    preload = ""
    if ev.get("hero"):
        h = ev["hero"]
        preload = (
            f'<link rel="preload" as="image" href="assets/images/hero/{h}-900.jpg"'
            f' media="(max-width: 899px)">\n'
            f'<link rel="preload" as="image" href="assets/images/hero/{h}-1800.jpg"'
            f' media="(min-width: 900px)">')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(ev['name'])}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#303249">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(ev['name'])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/images/social-card.jpg">
<meta property="og:image:width" content="{card_w}">
<meta property="og:image:height" content="{card_h}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{e(ev['name'])} — {e(ev['date'])}">
<meta property="og:site_name" content="{e(ev['name'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}assets/images/social-card.jpg">
<link rel="icon" href="assets/images/logo.png">
<link rel="apple-touch-icon" href="assets/images/logo.png">
{preload}
{font_block()}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#panel-schedule">Skip to content</a>
<header>
  <div class="bar">
    <nav role="tablist" aria-label="Sections">{tabs}</nav>
  </div>
</header>
<main class="wrap">
{panels_html}
{render_sponsors()}
</main>
<footer class="wrap">
  <p><b>{e(ev['name'])}</b> &middot; {e(ev['date'])} &middot; {e(ev['venue'])}
    &middot; <a class="tickets" href="{e(ev['tickets_url'])}" target="_blank"
      rel="noopener">Get Your Tickets</a></p>
  <p class="credit">Tool made using AI vibe-coding by
    <a href="https://shawnlife.com" target="_blank" rel="noopener">ShawnLife</a></p>
</footer>
<button id="backpill" type="button" hidden>&larr; <span id="backpill-text">Back</span></button>
{render_modal()}
<script>{JS.replace('__TRACK_BLOCK__', tracking_js())}</script>
</body>
</html>
"""


def validate(page):
    ids = set(re.findall(r'\sid="([^"]+)"', page))
    refs = set(re.findall(r'href="#([^"]+)"', page))
    dead = sorted(r for r in refs if r not in ids)
    if dead:
        sys.exit("Dead internal links (no element with that id):\n  " + "\n  ".join(dead))

    missing = [sp["slug"] for sp in D.SPEAKERS
               if not (ROOT / "assets" / "images" / "headshots" / f'{sp["slug"]}.jpg').exists()]
    if missing:
        sys.exit("Missing headshot images (run build_images.py first):\n  "
                 + "\n  ".join(missing))
    for s in D.SPONSORS:
        if not (ROOT / "assets" / "images" / "sponsors" / s["file"]).exists():
            sys.exit(f'Missing sponsor logo: assets/images/sponsors/{s["file"]}')

    # Every session needs a topic, or the filter silently hides it.
    untagged = sorted(a for a in BY_ANCHOR if not topics_of(a))
    if untagged:
        sys.exit("Sessions with no topic tag in TOPICS:\n  " + "\n  ".join(untagged))
    stray = sorted(set(D.TOPICS) - set(BY_ANCHOR)) + sorted(set(D.PANELS) - set(BY_ANCHOR))
    if stray:
        sys.exit("TOPICS/PANELS refer to unknown sessions:\n  " + "\n  ".join(stray))

    # Every speaker in a session, every session in the schedule.
    orphans = sorted(s for s, v in SESSIONS_FOR.items() if not v)
    if orphans:
        print("  note: speakers not in any session: " + ", ".join(orphans))
    scheduled = set()
    for slot in D.SCHEDULE:
        for key in ("item", "star", "avalon"):
            if key in slot and "session" in slot[key]:
                scheduled.add(slot[key]["session"])
    unscheduled = sorted(set(BY_ANCHOR) - scheduled)
    if unscheduled:
        sys.exit("Sessions missing from the schedule:\n  " + "\n  ".join(unscheduled))
    return len(ids), len(refs)


def write_analytics_names():
    """Id -> readable name, for the usage dashboard. Means the tracking backend
    only ever has to store ids, never names."""
    import json
    names = {s["anchor"]: s["title"] for s in D.SESSIONS}
    names.update({sp["slug"]: sp["name"] for sp in D.SPEAKERS})
    out = ROOT / "analytics" / "names.js"
    if not out.parent.exists():
        return
    out.write_text("/* Generated by build_site.py — do not edit. */\n"
                   "window.IFC_NAMES = "
                   + json.dumps(names, indent=2, ensure_ascii=False) + ";\n",
                   encoding="utf-8")


def main():
    missing = [f for f in GRAPHIK.values() if not (ROOT / "assets" / "fonts" / f).exists()]
    if missing:
        sys.exit("Missing webfonts (run build_fonts.py first):\n  " + "\n  ".join(missing))

    page = render_page()
    n_ids, n_refs = validate(page)
    OUT.write_text(page, encoding="utf-8")
    write_analytics_names()
    print(f"Wrote index.html — {OUT.stat().st_size / 1024:.0f} KB")
    print(f"  {len(D.SCHEDULE)} schedule slots, {len(D.SESSIONS)} sessions, "
          f"{len(D.SPEAKERS)} speakers, {len(D.SPONSORS)} sponsors")
    print(f"  {len(ALL_TOPICS)} topics: " + ", ".join(ALL_TOPICS))
    print(f"  {n_refs} internal links checked against {n_ids} anchors — all resolve")


if __name__ == "__main__":
    main()
