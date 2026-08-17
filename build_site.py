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

ROOT = Path(__file__).parent
OUT = ROOT / "index.html"
SITE_URL = "https://shawnlife.github.io/ifc-popup-2026/"

BY_SLUG = {s["slug"]: s for s in D.SPEAKERS}
BY_ANCHOR = {s["anchor"]: s for s in D.SESSIONS}


def e(text):
    return html.escape(str(text), quote=True)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none !important}
:root{
  --orange:#F49404;
  --orange-dim:#c4760a;
  --bg:#303249;
  --surface:#3D3F5A;
  --surface-2:#454764;
  --muted:#A0A3C0;
  --line:rgba(255,255,255,.08);
  --line-strong:rgba(255,255,255,.16);
  --radius:12px;
  --nav-h:56px;
  --wrap:1080px;
}
@media (min-width:760px){:root{--nav-h:66px}}
html{-webkit-text-size-adjust:100%}
html:focus-within{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html:focus-within{scroll-behavior:auto}}
body{
  margin:0;background:var(--bg);color:#fff;
  font-family:'Graphik','Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
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
.skip{position:absolute;left:8px;top:-60px;z-index:60;background:var(--orange);
  color:#241f10;font-weight:700;padding:10px 14px;border-radius:8px;transition:top .15s}
.skip:focus{top:8px}

/* ---------- sticky header ---------- */
header{
  position:sticky;top:0;z-index:50;background:rgba(48,50,73,.96);
  backdrop-filter:saturate(1.4) blur(8px);
  border-bottom:1px solid var(--line);
}
.bar{display:flex;align-items:center;gap:10px;height:var(--nav-h);
  max-width:var(--wrap);margin:0 auto;padding:0 12px}
.bar .mark{flex:0 0 auto;display:flex;align-items:center}
.bar .mark img{height:38px;width:auto;display:block}
@media (min-width:760px){.bar{gap:18px;padding:0 16px}.bar .mark img{height:50px}}
[role=tablist]{display:flex;flex:1 1 auto;gap:4px;justify-content:flex-end;min-width:0}
[role=tab]{
  flex:1 1 0;min-width:0;min-height:44px;
  display:flex;align-items:center;justify-content:center;
  padding:0 6px;border-radius:9px;
  font-size:.83rem;font-weight:600;letter-spacing:.01em;
  color:var(--muted);text-decoration:none;white-space:nowrap;
  border:1px solid transparent;background:none;cursor:pointer;
  font-family:inherit;
}
@media (min-width:760px){[role=tab]{flex:0 0 auto;font-size:.95rem;padding:0 18px}}
[role=tab]:hover{color:#fff;text-decoration:none;background:rgba(255,255,255,.05)}
[role=tab][aria-selected=true]{
  color:#241f10;background:var(--orange);border-color:var(--orange);
}

/* ---------- panels ---------- */
[role=tabpanel]{padding:22px 0 8px;scroll-margin-top:calc(var(--nav-h) + 8px)}
.panel-head{margin:0 0 4px;font-size:1.5rem;line-height:1.2;letter-spacing:-.01em}
.panel-sub{margin:0 0 20px;color:var(--muted);font-size:.92rem}

/* ---------- hero ---------- */
.hero{text-align:center;padding:14px 0 26px}
.hero img{width:min(260px,68vw);height:auto;margin:0 auto 18px;display:block}
.hero h1{margin:0 0 10px;font-size:clamp(1.5rem,6vw,2.5rem);line-height:1.15;
  letter-spacing:-.02em;font-weight:700}
.hero .meta{margin:0 auto 20px;color:var(--muted);font-size:.98rem;max-width:34ch}
.hero .meta b{color:#fff;font-weight:600}
.cta{
  display:inline-flex;align-items:center;gap:8px;min-height:50px;
  padding:0 26px;border-radius:999px;
  background:var(--orange);color:#241f10;font-weight:700;font-size:1.02rem;
}
.cta:hover{background:#ffa61f;text-decoration:none}
.cta svg{width:15px;height:15px;fill:currentColor;flex:0 0 auto}

/* ---------- schedule ---------- */
.slot{
  display:grid;grid-template-columns:70px minmax(0,1fr);gap:10px;
  padding:12px 0;border-top:1px solid var(--line);
}
.slot:nth-child(odd){background:rgba(255,255,255,.018)}
@media (min-width:760px){.slot{grid-template-columns:104px minmax(0,1fr);gap:18px;padding:14px 0}}
.slot-time{
  font-weight:700;font-size:.76rem;color:var(--orange);line-height:1.35;
  padding-top:11px;letter-spacing:.005em;
}
@media (min-width:760px){.slot-time{font-size:.9rem}}
.rooms{display:grid;gap:10px;grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.rooms{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:12px 14px;min-width:0;
}
.card.star{border-left:3px solid var(--orange)}
.card.avalon{border-left:3px solid rgba(255,255,255,.34)}
.card.plenary{
  border:1px solid rgba(244,148,4,.42);border-left:3px solid var(--orange);
  background:linear-gradient(180deg,rgba(244,148,4,.10),rgba(244,148,4,.03)),var(--surface);
}
.card.break,.card.logistics{
  background:transparent;border:1px dashed var(--line-strong);border-left:1px dashed var(--line-strong);
}
.card.remarks{background:rgba(255,255,255,.03);border-left:3px solid rgba(255,255,255,.2)}
.room{
  font-size:.63rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;
  color:var(--muted);display:block;margin-bottom:5px;
}
.card.star .room{color:var(--orange)}
.kicker{
  font-size:.63rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;
  color:var(--orange);display:block;margin-bottom:5px;
}
.card .title{
  display:block;font-weight:600;font-size:.97rem;line-height:1.35;color:#fff;
  margin:0 0 6px;
}
a.title:hover{color:var(--orange);text-decoration:none}
a.title::after{content:' \\203A';color:var(--orange);font-weight:700}
.card.break .title,.card.logistics .title{font-size:.92rem;color:var(--muted)}
.card .who{font-size:.86rem;color:var(--muted);margin:0;line-height:1.5}
.card .who a{color:#cfd2e8;text-decoration:underline;text-decoration-color:rgba(207,210,232,.35);
  text-underline-offset:2px}
.card .who a:hover{color:var(--orange);text-decoration-color:var(--orange)}
.card .detail{font-size:.86rem;color:var(--muted);margin:0}

/* ---------- badges ---------- */
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.badge{
  font-size:.64rem;text-transform:uppercase;letter-spacing:.09em;font-weight:700;
  padding:4px 9px;border-radius:999px;border:1px solid var(--line-strong);
  color:var(--muted);white-space:nowrap;
}
.badge.star{color:var(--orange);border-color:rgba(244,148,4,.45);background:rgba(244,148,4,.08)}
.badge.avalon{color:#d3d6ec;border-color:var(--line-strong)}
.badge.plenary{color:#241f10;background:var(--orange);border-color:var(--orange)}
.badge.intl{color:#9fe3c4;border-color:rgba(159,227,196,.4);background:rgba(159,227,196,.08)}
.badge.time{color:#fff;border-color:var(--line-strong);letter-spacing:.04em}

/* ---------- session cards ---------- */
.sessions{display:grid;gap:14px}
.session{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px;scroll-margin-top:calc(var(--nav-h) + 14px);
}
@media (min-width:760px){.session{padding:22px 24px}}
.session.is-plenary{
  border-color:rgba(244,148,4,.42);
  background:linear-gradient(180deg,rgba(244,148,4,.09),rgba(244,148,4,.02)),var(--surface);
}
.session h3{
  margin:0 0 10px;color:var(--orange);font-size:1.1rem;line-height:1.3;
  letter-spacing:-.005em;
}
@media (min-width:760px){.session h3{font-size:1.28rem}}
.session .who{font-size:.92rem;color:var(--muted);margin:0 0 12px}
.session .who a{color:#fff;font-weight:600;text-decoration:underline;
  text-decoration-color:rgba(255,255,255,.3);text-underline-offset:2px}
.session .who a:hover{color:var(--orange);text-decoration-color:var(--orange)}
.session p.desc{margin:0;color:#e6e8f5;font-size:.95rem}

/* ---------- speakers ---------- */
.speakers{display:grid;gap:14px;grid-template-columns:minmax(0,1fr)}
@media (min-width:560px){.speakers{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:900px){.speakers{grid-template-columns:repeat(3,minmax(0,1fr))}}
.spk{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px 18px;text-align:center;display:flex;flex-direction:column;align-items:center;
  scroll-margin-top:calc(var(--nav-h) + 14px);
}
.spk img{
  width:120px;height:120px;border-radius:50%;object-fit:cover;object-position:50% 25%;
  border:2px solid rgba(255,255,255,.14);background:var(--surface-2);margin-bottom:14px;
}
.spk h3{margin:0 0 4px;font-size:1.04rem;line-height:1.3}
.spk .role{margin:0;color:var(--muted);font-size:.85rem;line-height:1.45}
.spk .org{margin:0;color:var(--muted);font-size:.85rem;font-weight:600;line-height:1.45}
/* Badge sits below the org so name/title/org stay aligned across a row. */
.spk .spk-badges{display:flex;gap:6px;justify-content:center;margin:8px 0 0}
.spk .pending-note{margin:8px 0 0;color:var(--muted);font-size:.8rem;font-style:italic}
.actions{
  margin-top:auto;padding-top:14px;display:flex;gap:8px;
  justify-content:center;flex-wrap:wrap;width:100%;
}
.bio-btn{
  margin:0;background:none;border:1px solid var(--line-strong);color:var(--muted);
  font-family:inherit;font-size:.78rem;font-weight:600;letter-spacing:.04em;
  text-transform:uppercase;padding:9px 14px;border-radius:999px;cursor:pointer;
  min-height:44px;
}
.bio-btn:hover{color:#fff;border-color:var(--muted)}
.bio-btn[aria-expanded=true]{color:var(--orange);border-color:rgba(244,148,4,.45)}
.bio{
  margin:14px 0 0;font-size:.88rem;color:#e6e8f5;text-align:left;
  border-top:1px solid var(--line);padding-top:12px;width:100%;
}
.li{
  display:inline-flex;align-items:center;justify-content:center;gap:7px;
  min-height:44px;padding:0 16px;border-radius:999px;
  border:1px solid var(--line-strong);color:var(--muted);
  font-size:.78rem;font-weight:600;
}
.li:hover{color:#fff;border-color:#0A66C2;background:#0A66C2;text-decoration:none}
.li svg{width:14px;height:14px;fill:currentColor}

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
  position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:55;
  display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 20px;
  border-radius:999px;border:1px solid rgba(0,0,0,.2);
  background:var(--orange);color:#241f10;font-family:inherit;font-weight:700;
  font-size:.9rem;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.4);
}
#backpill:hover{background:#ffa61f}

/* ---------- sponsors + footer ---------- */
.sponsors-wrap{border-top:1px solid var(--line);margin-top:34px;padding:34px 0 0}
.sponsors-wrap h2{margin:0 0 6px;text-align:center;font-size:1.2rem;letter-spacing:-.01em}
.sponsors-wrap p.note{margin:0 0 22px;text-align:center;color:var(--muted);font-size:.88rem}
.sponsors{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;list-style:none;
  margin:0;padding:0}
.sponsors li{flex:1 1 calc(50% - 10px);max-width:230px;display:flex}
@media (min-width:640px){.sponsors li{flex:0 1 200px}}
.sponsors a{
  flex:1;background:#fff;border-radius:10px;padding:14px 16px;min-height:84px;
  display:flex;align-items:center;justify-content:center;
}
.sponsors a:hover{box-shadow:0 0 0 2px var(--orange);text-decoration:none}
.sponsors img{max-width:100%;max-height:48px;width:auto;height:auto;display:block}
footer{
  margin-top:34px;border-top:1px solid var(--line);padding:22px 0 30px;
  text-align:center;color:var(--muted);font-size:.83rem;
}
footer p{margin:0 0 6px}
footer .credit{font-size:.78rem;opacity:.75}
footer .credit a{color:var(--muted);text-decoration:underline}
footer .credit a:hover{color:var(--orange)}
"""

# ---------------------------------------------------------------------------
# JS — tab switching plus cross-tab deep linking
# ---------------------------------------------------------------------------

JS = """
(function(){
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
  function clearHash(){
    if(location.hash) history.replaceState(null, '', location.pathname + location.search);
  }

  // Without JS every panel stays visible, so the page still reads as one long
  // document. Now that JS is running, collapse it into real tabs.
  activate(panels[0].id);

  function syncFromHash(){
    var id = location.hash.replace(/^#/, '');
    if(!id) return false;
    var target = document.getElementById(id);
    if(!target) return false;
    var p = panelOf(target);
    if(!p) return false;
    if(p !== currentPanel()) activate(p.id);
    target.scrollIntoView({ block:'start' });
    pulse(target);
    return true;
  }

  tabs.forEach(function(tab, i){
    tab.addEventListener('click', function(ev){
      ev.preventDefault();
      activate(tab.getAttribute('aria-controls'));
      hidePill();
      clearHash();
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

  // Any in-page link: reveal the owning panel first, then jump to it.
  document.addEventListener('click', function(ev){
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href^="#"]') : null;
    if(!a || a.getAttribute('role') === 'tab') return;
    var id = a.getAttribute('href').slice(1);
    if(!id) return;
    var target = document.getElementById(id);
    if(!target) return;
    var p = panelOf(target);
    if(!p) return;
    ev.preventDefault();
    var cur = currentPanel();
    if(p !== cur) showPill(cur.id);
    activate(p.id);
    history.pushState(null, '', '#' + id);
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block:'start' });
    pulse(target);
  });

  pill.addEventListener('click', function(){
    if(!ret){ hidePill(); return; }
    var back = ret;
    activate(back.id);
    hidePill();
    history.pushState(null, '', location.pathname + location.search);
    window.scrollTo(0, back.y);
  });

  window.addEventListener('popstate', function(){
    if(!syncFromHash()){ hidePill(); }
  });

  // Bios collapse by default; keeps the 3-up grid tidy and the phone scroll short.
  document.addEventListener('click', function(ev){
    var b = ev.target && ev.target.closest ? ev.target.closest('.bio-btn') : null;
    if(!b) return;
    var bio = document.getElementById(b.getAttribute('aria-controls'));
    if(!bio) return;
    var open = b.getAttribute('aria-expanded') === 'true';
    b.setAttribute('aria-expanded', open ? 'false' : 'true');
    b.textContent = open ? 'Read bio' : 'Hide bio';
    bio.hidden = open;
  });

  // Deep link straight from a QR code or a shared link.
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
# Rendering helpers
# ---------------------------------------------------------------------------

def speaker_links(pairs, sep=", "):
    """Render "Name (Moderator), Name, Name" with each name linked to its card."""
    out = []
    for slug, note in pairs:
        if slug not in BY_SLUG:
            sys.exit(f"Unknown speaker slug in a session: {slug!r}")
        sp = BY_SLUG[slug]
        bit = f'<a href="#{sp["slug"]}">{e(sp["name"])}</a>'
        if note:
            bit += f' <span class="note">({e(note)})</span>'
        out.append(bit)
    if len(out) > 1:
        return sep.join(out[:-1]) + " &amp; " + out[-1]
    return out[0] if out else ""


def render_schedule_item(item, room_class=None, room_label=None):
    classes = ["card"]
    if room_class:
        classes.append(room_class)

    if "session" in item:
        s = BY_ANCHOR[item["session"]]
        if item.get("flavour") == "plenary" or s.get("plenary"):
            classes.append("plenary")
        head = ""
        if room_label:
            head = f'<span class="room">{e(room_label)}</span>'
        else:
            head = f'<span class="kicker">{e(s["label"])} &middot; {e(s["room"])}</span>'
        who = ""
        if s["speakers"]:
            who = f'<p class="who">{speaker_links(s["speakers"])}</p>'
        label = e(s["label"]) + ": " if room_label else ""
        return (
            f'<div class="{" ".join(classes)}">{head}'
            f'<a class="title" href="#{s["anchor"]}">{label}{e(s["title"])}</a>{who}</div>'
        )

    classes.append(item["flavour"])
    return (
        f'<div class="{" ".join(classes)}">'
        f'<span class="title">{e(item["name"])}</span>'
        f'<p class="detail">{e(item["detail"])}</p></div>'
    )


def render_schedule():
    rows = []
    for slot in D.SCHEDULE:
        if slot["kind"] == "full":
            body = render_schedule_item(slot["item"])
        else:
            star = render_schedule_item(slot["star"], "star", D.STAR)
            avalon = render_schedule_item(slot["avalon"], "avalon", D.AVALON)
            body = f'<div class="rooms">{star}{avalon}</div>'
        rows.append(
            f'<div class="slot"><div class="slot-time">{e(slot["time"])}</div>'
            f'<div class="slot-body">{body}</div></div>'
        )

    ev = D.EVENT
    logo = ev["logo"]
    hero = f"""
    <div class="hero">
      <img src="images/{e(logo['file'])}" width="{logo['w']}" height="{logo['h']}"
           alt="IFC Cape Town Pop-Up 2026">
      <h1>{e(ev['headline'])}</h1>
      <p class="meta"><b>{e(ev['date'])}</b><br>{e(ev['venue'])}</p>
      <a class="cta" href="{e(ev['tickets_url'])}" target="_blank" rel="noopener">
        Get Your Tickets {EXT_SVG}</a>
    </div>"""

    return (hero
            + '<h2 class="panel-head">Programme</h2>'
            + '<p class="panel-sub">Tap any session title or speaker name for the full '
              'details.</p>'
            + '<div class="schedule">' + "".join(rows) + '</div>')


def render_sessions():
    cards = []
    for s in D.SESSIONS:
        badges = [f'<span class="badge time">{e(s["time"])}</span>']
        room_cls = "star" if s["room"] == D.STAR else "avalon"
        badges.append(f'<span class="badge {room_cls}">{e(s["room"])}</span>')
        if s.get("plenary"):
            badges.append('<span class="badge plenary">Plenary</span>')
        if any(BY_SLUG[slug].get("international") for slug, _ in s["speakers"]):
            badges.append('<span class="badge intl">International Speaker</span>')

        who = ""
        if s["speakers"]:
            word = "Speakers" if len(s["speakers"]) > 1 else "Speaker"
            who = f'<p class="who">{word}: {speaker_links(s["speakers"])}</p>'

        cards.append(
            f'<article class="session{" is-plenary" if s.get("plenary") else ""}" '
            f'id="{s["anchor"]}" tabindex="-1">'
            f'<div class="badges">{"".join(badges)}</div>'
            f'<h3>{e(s["label"])}: {e(s["title"])}</h3>'
            f'{who}<p class="desc">{e(s["description"])}</p></article>'
        )

    return ('<h2 class="panel-head">Sessions</h2>'
            f'<p class="panel-sub">{len(D.SESSIONS)} sessions across the Star and Avalon '
            'theatres. Speaker names link through to their profiles.</p>'
            '<div class="sessions">' + "".join(cards) + '</div>')


def render_speakers():
    cards = []
    for sp in D.SPEAKERS:
        pending = sp["bio"] == D.BIO_PENDING
        bio_id = f'bio-{sp["slug"]}'
        badge = ('<div class="spk-badges"><span class="badge intl">International</span></div>'
                 if sp.get("international") else "")

        if pending:
            note = f'<p class="pending-note">{e(sp["bio"])}</p>'
            toggle = ""
            bio_block = ""
        else:
            note = ""
            toggle = (f'<button class="bio-btn" type="button" aria-expanded="false" '
                      f'aria-controls="{bio_id}">Read bio</button>')
            bio_block = f'<p class="bio" id="{bio_id}" hidden>{e(sp["bio"])}</p>'

        linkedin = (f'<a class="li" href="{e(sp["linkedin"])}" target="_blank" rel="noopener">'
                    f'{LINKEDIN_SVG}<span>LinkedIn</span>'
                    f'<span class="sr"> profile for {e(sp["name"])} (opens in a new tab)</span>'
                    f'</a>')

        cards.append(
            f'<article class="spk" id="{sp["slug"]}" tabindex="-1">'
            f'<img src="images/headshots/{sp["slug"]}.jpg" width="120" height="120" '
            f'loading="lazy" decoding="async" alt="{e(sp["name"])}">'
            f'<h3>{e(sp["name"])}</h3>'
            f'<p class="role">{e(sp["title"])}</p>'
            f'<p class="org">{e(sp["org"])}</p>'
            f'{badge}{note}'
            f'<div class="actions">{toggle}{linkedin}</div>'
            f'{bio_block}</article>'
        )

    return ('<h2 class="panel-head">Speakers</h2>'
            f'<p class="panel-sub">{len(D.SPEAKERS)} speakers, listed alphabetically. '
            'Tap “Read bio” for more.</p>'
            '<div class="speakers">' + "".join(cards) + '</div>')


def render_sponsors():
    items = []
    for s in D.SPONSORS:
        items.append(
            f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener" '
            f'title="{e(s["name"])} (opens in a new tab)">'
            f'<img src="images/sponsors/{e(s["file"])}" width="{s["w"]}" height="{s["h"]}" '
            f'loading="lazy" decoding="async" alt="{e(s["name"])}"></a></li>'
        )
    return ('<div class="sponsors-wrap"><h2>Thank You to Our Sponsors</h2>'
            '<p class="note">This event would not be possible without them.</p>'
            '<ul class="sponsors">' + "".join(items) + '</ul></div>')


TABS = [("panel-schedule", "Schedule"), ("panel-sessions", "Sessions"),
        ("panel-speakers", "Speakers")]


def render_page():
    ev = D.EVENT
    tabs = "".join(
        f'<a role="tab" id="tab-{pid}" href="#{pid}" aria-controls="{pid}" '
        f'data-label="{label}" aria-selected="{"true" if i == 0 else "false"}" '
        f'tabindex="{0 if i == 0 else -1}">{label}</a>'
        for i, (pid, label) in enumerate(TABS)
    )

    panels = [
        ("panel-schedule", render_schedule()),
        ("panel-sessions", render_sessions()),
        ("panel-speakers", render_speakers()),
    ]
    panels_html = "".join(
        f'<section role="tabpanel" id="{pid}" aria-labelledby="tab-{pid}" tabindex="0">'
        f'{body}</section>'
        for pid, body in panels
    )

    desc = (f"{ev['name']} — {ev['date']}, {ev['venue']}. "
            "Full programme, sessions and speakers.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(ev['name'])}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="{D.__dict__.get('THEME_COLOR', '#303249')}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(ev['name'])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}images/{e(ev['logo']['file'])}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="images/logo.png">
<link rel="apple-touch-icon" href="images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#panel-schedule">Skip to content</a>
<header>
  <div class="bar">
    <span class="mark">
      <img src="images/{e(ev['logo']['file'])}" width="{ev['logo']['w']}"
           height="{ev['logo']['h']}" alt="{e(ev['name'])}">
    </span>
    <nav role="tablist" aria-label="Sections">{tabs}</nav>
  </div>
</header>
<main class="wrap">
{panels_html}
{render_sponsors()}
</main>
<footer class="wrap">
  <p><b>{e(ev['name'])}</b> &middot; {e(ev['date'])} &middot; {e(ev['venue'])}</p>
  <p class="credit">Tool made using AI vibe-coding by
    <a href="https://shawnlife.com" target="_blank" rel="noopener">ShawnLife</a></p>
</footer>
<button id="backpill" type="button" hidden>&larr; <span id="backpill-text">Back</span></button>
<script>{JS}</script>
</body>
</html>
"""


def validate(page):
    """Every internal #anchor must point at an element that exists."""
    ids = set(re.findall(r'\sid="([^"]+)"', page))
    refs = set(re.findall(r'href="#([^"]+)"', page))
    dead = sorted(r for r in refs if r not in ids)
    if dead:
        sys.exit("Dead internal links (no element with that id):\n  " + "\n  ".join(dead))

    # Every speaker needs a built headshot, and every session a real room.
    missing = [sp["slug"] for sp in D.SPEAKERS
               if not (ROOT / "images" / "headshots" / f'{sp["slug"]}.jpg').exists()]
    if missing:
        sys.exit("Missing headshot images (run build_images.py first):\n  "
                 + "\n  ".join(missing))
    for s in D.SPONSORS:
        if not (ROOT / "images" / "sponsors" / s["file"]).exists():
            sys.exit(f'Missing sponsor logo: images/sponsors/{s["file"]}')

    # Every speaker should appear in at least one session, and vice versa.
    used = {slug for s in D.SESSIONS for slug, _ in s["speakers"]}
    orphan_speakers = sorted(set(BY_SLUG) - used)
    if orphan_speakers:
        print("  note: speakers not in any session: " + ", ".join(orphan_speakers))

    # Every session must be reachable from the schedule.
    scheduled = set()
    for slot in D.SCHEDULE:
        for key in ("item", "star", "avalon"):
            if key in slot and "session" in slot[key]:
                scheduled.add(slot[key]["session"])
    unscheduled = sorted(set(BY_ANCHOR) - scheduled)
    if unscheduled:
        sys.exit("Sessions missing from the schedule:\n  " + "\n  ".join(unscheduled))

    return len(ids), len(refs)


def main():
    page = render_page()
    n_ids, n_refs = validate(page)
    OUT.write_text(page, encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"Wrote index.html — {kb:.0f} KB")
    print(f"  {len(D.SCHEDULE)} schedule slots, {len(D.SESSIONS)} sessions, "
          f"{len(D.SPEAKERS)} speakers, {len(D.SPONSORS)} sponsors")
    print(f"  {n_refs} internal links checked against {n_ids} anchors — all resolve")


if __name__ == "__main__":
    main()
