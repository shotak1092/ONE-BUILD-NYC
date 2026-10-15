#!/usr/bin/env python3
"""Generates the One Build NYC static site. Run: python3 _build/build.py
Edit content in this file, rerun, commit. Output goes to the repo root."""
import os, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_seo import FAQS, AREAS_LIST
from content_blog import POSTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://onebuildnyc.com"
PHONE_DISPLAY = "(888) 781-7547"
PHONE_TEL = "8887817547"
EMAIL = "info@onebuildnyc.com"
AREAS = "Manhattan · Brooklyn · Queens · Long Island · Westchester · New Jersey"

def img(name): return f"/images/{name}.jpg"

# ---------------------------------------------------------------- services
SERVICES = [
 dict(slug="renovations", name="Renovations", kicker="Construction & Remodeling",
  title="Home Renovations in NYC & New Jersey",
  hero="vaulted-feature-wall",
  short="Room-by-room or whole-house, with plumbing, electrical and technology on the same schedule.",
  intro="Most renovations stall in the gaps between trades. We run every trade from one office, so framing, rough-in, inspections and finishes happen in the right order and nobody waits on anybody.",
  includes=["Design walkthrough and single written scope","Demolition and debris removal","Framing, drywall and taping","Flooring, tile and millwork","Paint and finish carpentry","Additions, decks and paver patios","Licensed plumbing and electrical","Lighting, shades, audio and network planned in"],
  gallery=["vaulted-framing","vaulted-scaffolding","vaulted-finishes","vaulted-feature-wall","brick-loft-before","brick-loft-kitchen","addition-exterior","addition-interior","composite-deck","deck-paver-patio","paver-patio","protected-job-site"]),
 dict(slug="kitchens", name="Kitchens", kicker="Kitchen Remodeling",
  title="Kitchen Remodeling in NYC & New Jersey",
  hero="glass-house-kitchen",
  short="Layout, cabinetry, plumbing, appliance circuits and lighting, built as one job.",
  intro="A kitchen touches every trade at once: gas and water lines, dedicated appliance circuits, venting, under-cabinet and scene lighting, and often built-in audio. We plan all of it on day one so the walls only get closed once.",
  includes=["Layout and cabinetry installation","Countertops, backsplash and tile","Sink, dishwasher, gas and water lines","Dedicated appliance circuits and panel work","Recessed, under-cabinet and pendant lighting","Lighting control scenes and keypads","Built-in ceiling speakers","Laundry and pantry build-outs"],
  gallery=["glass-house-kitchen","brick-loft-kitchen","beamed-kitchen","kitchen-demo","kitchen-laundry-after","brick-loft-before"]),
 dict(slug="bathrooms", name="Bathrooms", kicker="Bathroom Remodeling",
  title="Bathroom Remodeling in NYC & New Jersey",
  hero="double-vanity-marble-shower",
  short="Full gut to finish: tile, fixtures, glass, lighting and ventilation.",
  intro="From compact co-op baths to marble primary suites, we take bathrooms down to the studs and rebuild them with licensed plumbing, proper waterproofing and lighting that actually works at the mirror.",
  includes=["Full demolition and waterproofing","Walk-in showers, tubs and glass enclosures","Wall and floor tile, niches and benches","Vanities, medicine cabinets and mirrors","Licensed plumbing and fixture installation","Vanity, shower and recessed lighting","Exhaust fans and GFCI circuits","Smart toilets, heated floors and in-ceiling speakers"],
  gallery=["double-vanity-marble-shower","marble-shower","brass-zellige-bathroom","onyx-shower-sauna","black-white-smart-bath","greek-key-shower","walk-in-glass-shower","black-fixture-tub","hex-niche-bath","hex-niche-bath-2","hex-floor-tile","double-vanity-sconces","blue-subway-bath","soaking-tub","vanity-wainscot","subway-tub-surround","round-mirror-bath","octagon-floor-bath","subway-shelves-shower","subway-window-shower","patterned-floor-tile"]),
 dict(slug="gut-renovations", name="Gut Renovations", kicker="Full Gut Renovations",
  title="Gut Renovations in NYC & New Jersey",
  hero="vaulted-framing",
  short="Apartments, brownstones, lofts and houses, rebuilt from the studs out.",
  intro="A gut renovation is where coordination matters most. With the walls open, plumbing, electrical and low-voltage go in together, get inspected together, and are documented before anything is closed up.",
  includes=["Demolition down to the structure","New framing and layout changes","Plumbing supply, drain and venting rough-in","New panel, circuits and lighting rough-in","Low-voltage, network and speaker pre-wire","Insulation, drywall and finishes","Permits, filings and inspections","Final commissioning and walkthrough"],
  gallery=["vaulted-framing","framing-rough-in","ceiling-rough-in","vaulted-scaffolding","vaulted-finishes","vaulted-feature-wall","kitchen-demo","kitchen-laundry-after","protected-job-site"]),
 dict(slug="plumbing", name="Plumbing", kicker="Licensed Plumbers",
  title="Licensed Plumbing in NYC & New Jersey",
  hero="marble-shower",
  short="Licensed in New York. Kitchen and bath rough-in, fixtures, gas and water heaters.",
  intro="Our plumbing is done by licensed New York plumbers, permitted and inspected. Because they work on the same schedule as the rest of the crew, rough-in is finished before tile and drywall, not squeezed in after.",
  includes=["Kitchen and bathroom rough-in","Supply and drain line replacement","Shower valves, tubs and fixtures","Gas lines for ranges and appliances","Water heaters","Washer and laundry hookups","Permits and DOB filings","Leak repairs and upgrades"],
  gallery=["framing-rough-in","marble-shower","onyx-shower-sauna","walk-in-glass-shower","black-fixture-tub","greek-key-shower","soaking-tub","subway-window-shower","kitchen-laundry-after"]),
 dict(slug="electrical", name="Electrical", kicker="Licensed Electricians",
  title="Licensed Electricians in NYC & New Jersey",
  hero="dimming-panel",
  short="Licensed in New York. Panels, circuits, lighting, dedicated lines and permits.",
  intro="Licensed New York electricians handle panels, new circuits and every line that feeds the lighting, shades and AV, so power and control are designed as one system instead of patched together.",
  includes=["Panel upgrades and new circuits","Dedicated lines for appliances and equipment","Recessed, track and cove lighting","Lighting control and dimming panels","Shade power and motor circuits","Outdoor and landscape lighting power","EV charger circuits","Permits, filings and inspections"],
  gallery=["dimming-panel","electrical-panel-drivers","shade-power-panels","ceiling-rough-in","gallery-lighting","framing-rough-in"]),
 dict(slug="smart-home", name="Smart Home", kicker="Licensed Automation & Low Voltage",
  title="Smart Home Automation in NYC & New Jersey",
  hero="walnut-media-wall",
  short="Lighting, shades, audio, video, network and cameras, on one control system.",
  intro="We design and install the systems that make a home run itself: whole-home Wi-Fi and network, multi-room audio, video distribution, cameras, lighting and shades, all on one app and a few clean keypads. Wiring goes in during rough-in, so nothing is surface-mounted later.",
  includes=["Whole-home Wi-Fi and network","Equipment racks and structured wiring","Multi-room audio and video","Lighting and shade integration","Security cameras","Keypads, remotes and app control","Pre-wire during construction","Programming and owner training"],
  gallery=["walnut-media-wall","equipment-rack","fireplace-tv-after","media-wall-before","primary-suite-shades","shade-power-panels","dining-room"]),
 dict(slug="window-treatments", name="Window Treatments", kicker="Motorized Shades",
  title="Motorized Shades & Window Treatments in NYC & New Jersey",
  hero="primary-suite-shades",
  short="Motorized roller, Roman and blackout shades, recessed and wired during construction.",
  intro="The cleanest shades are planned before the ceiling closes: recessed pockets, power where it belongs, and fabrics chosen in the room. We handle selections, measuring, wiring, installation and programming.",
  includes=["Motorized roller and Roman shades","Blackout and solar fabrics","Drapery and track systems","Recessed shade pockets","Shade power panels and wiring","Keypad, app and schedule control","Fabric selection on site","Programming and scenes"],
  gallery=["primary-suite-shades","shade-selections","addition-interior","shade-power-panels","glass-house-kitchen"]),
 dict(slug="lighting-control", name="Lighting Control", kicker="Lighting & Control",
  title="Lighting Control & Design in NYC & New Jersey",
  hero="gallery-lighting",
  short="Dimming, scenes and keypads, with track, cove and landscape lighting.",
  intro="Good lighting is designed with the room, not added after. We lay out fixtures, run the circuits, install the dimming panels and program scenes, so one button sets the whole space.",
  includes=["Lighting layout and fixture selection","Recessed, track and cove lighting","Dimming panels and keypads","Scenes, schedules and app control","Landscape and step lighting","Art and gallery lighting","Integration with shades and AV","Programming and fine-tuning"],
  gallery=["gallery-lighting","dimming-panel","electrical-panel-drivers","led-wall-lounge","patio-lighting-rendering","beamed-kitchen"]),
 dict(slug="home-theater", name="Home Theater", kicker="Home Theater & Media Rooms",
  title="Home Theater Installation in NYC & New Jersey",
  hero="private-theater",
  short="Dedicated theaters, media walls, LED walls and lounges, built around the system.",
  intro="We build the room and the system together: framing for the screen and speakers, dedicated circuits, acoustic treatment, lighting scenes, then calibrated audio and video. From a clean media wall to a full LED-wall lounge.",
  includes=["Dedicated theaters and media rooms","Projection screens and large-format displays","LED video walls","In-wall and in-ceiling surround audio","Acoustic treatment and seating layout","Lighting scenes and blackout shades","Concealed wiring and equipment racks","Calibration and one-remote control"],
  gallery=["private-theater","led-wall-lounge","led-theater-lounge","walnut-media-wall","fireplace-tv-after","media-wall-after","lounge-bar","glass-cantilever-stair"]),
]
SVC = {s["slug"]: s for s in SERVICES}

ALT = {
 "brass-zellige-bathroom":"Bathroom with brass shower enclosure, blue zellige tile and marble double vanity",
 "electrical-panel-drivers":"Electrical panel with labeled circuits next to lighting drivers",
 "glass-cantilever-stair":"Cantilevered glass stair over a backlit agate floor",
 "onyx-shower-sauna":"Onyx-tiled shower beside an infrared sauna",
 "shade-power-panels":"Four labeled shade power panels mounted over a wireway",
 "brick-loft-before":"Brick loft mid-build with millwork going in under the arches",
 "gallery-lighting":"Gallery room with track lighting, cove lighting and a skylight",
 "led-wall-lounge":"Lounge with LED wall forest scenes in gold frames over a backlit agate floor",
 "led-theater-lounge":"Theater lounge facing the main LED wall",
 "glass-house-kitchen":"Modern kitchen with waterfall island and floor-to-ceiling glass",
 "addition-interior":"Bright addition interior with tall black-framed windows",
 "addition-exterior":"Sheathed addition with new windows on a gambrel-roof house",
 "brick-loft-kitchen":"Finished loft kitchen with skylight, planters and TV on painted brick",
 "walnut-media-wall":"Walnut media wall with recessed TV niche and soundbar",
 "equipment-rack":"Equipment rack wired and labeled inside a wall closet",
 "private-theater":"Dedicated home theater with projection screen and leather seating",
 "vaulted-framing":"Vaulted room in open framing with new windows",
 "framing-rough-in":"Contractor measuring inside new framing with plumbing lines run",
 "ceiling-rough-in":"Open joist ceiling with ductwork and speaker brackets during rough-in",
 "protected-job-site":"Bedroom floor covered in protection during finish work",
 "fireplace-tv-after":"Art-mode TV and soundbar over a restored marble mantel",
 "fireplace-tv-before":"Open recessed box and mount brackets above a marble mantel",
 "shade-selections":"Shade fabric swatches held up to a window during selections",
 "lounge-bar":"Lounge bar with banquettes, slatted walls and LED-lit displays",
 "dimming-panel":"Lighting control dimming panel wired inside an enclosure",
 "media-wall-before":"In-wall speakers and low-voltage plates set before the display",
 "vaulted-scaffolding":"Scaffolding in a vaulted room for drywall and ceiling work",
 "vaulted-finishes":"Drywalled vaulted room seen from the loft, finishes underway",
 "vaulted-feature-wall":"Vaulted great room with a finished wood slat wall over the fireplace",
 "paver-patio":"New paver patio with stone steps and retaining wall",
 "patio-lighting-rendering":"Design rendering of the patio at night with step and landscape lighting",
 "media-wall-after":"Finished media wall with TV over a low credenza",
 "beamed-kitchen":"Beamed kitchen and living room with a working fireplace",
 "dining-room":"Formal dining room with flush-mounted TV and ceiling speakers",
 "primary-suite-shades":"Corner bedroom with Roman shades and a pop-up TV cabinet",
 "marble-shower":"Carrara marble shower with linear drain and lit niche",
 "hex-niche-bath-2":"Full bath with tub, hex mosaic niche and vanity",
 "deck-paver-patio":"Raised deck and stairs over a new gray paver patio",
 "composite-deck":"New composite deck with white railings over a lawn",
 "kitchen-demo":"Kitchen gutted during demolition",
 "octagon-floor-bath":"Subway tile tub apron with octagon mosaic floor",
 "black-fixture-tub":"Marble-look tile tub surround with matte black fixtures and niche",
 "blue-subway-bath":"Bath with subway tile tub, niche and pale blue walls",
 "walk-in-glass-shower":"Walk-in glass shower beside a white floating vanity",
 "patterned-floor-tile":"Black patterned porcelain floor tile",
 "double-vanity-marble-shower":"Primary bath with double vanity and marble walk-in shower",
 "hex-niche-bath":"Bath with hex mosaic niche and large hex floor tile",
 "subway-shelves-shower":"Subway tile shower with recessed shelves and tiled window return",
 "double-vanity-sconces":"Double vanity with medicine cabinets and vertical sconces",
 "subway-window-shower":"Floor-to-ceiling subway tile around a shower window",
 "round-mirror-bath":"Beveled subway tile bath with round mirror",
 "hex-floor-tile":"Large gray hexagon floor tile",
 "greek-key-shower":"Rain shower with black and gold Greek key tile band",
 "black-white-smart-bath":"Black and white bath with smart toilet and lit mirror",
 "soaking-tub":"Deep soaking tub with subway tile surround and niche",
 "kitchen-laundry-after":"Kitchen and laundry with checkerboard floor and stainless appliances",
 "vanity-wainscot":"Vanity with medicine cabinet and subway tile wainscot",
 "subway-tub-surround":"Subway tile tub surround with brushed nickel fixtures",
}
CAP = {
 "patio-lighting-rendering":"Lighting design rendering",
}

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- chrome
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

def ld_json():
    data = {"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"One Build NYC",
            "url":DOMAIN,"telephone":"+1-888-781-7547","email":EMAIL,
            "areaServed":["Manhattan","Brooklyn","Queens","Long Island","Westchester","New Jersey"],
            "description":"Design-build renovation company with licensed contractors, plumbers, electricians and automation specialists under one contract.",
            "image":DOMAIN+img("glass-house-kitchen")}
    return '<script type="application/ld+json">'+json.dumps(data)+'</script>'

def header(active):
    svc_links = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)
    mob_svc = "".join(f'<a class="sub" href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)
    area_links = "".join(f'<a href="/areas/{a["slug"]}/">{a["name"]}</a>' for a in AREAS_LIST)
    mob_area = "".join(f'<a class="sub" href="/areas/{a["slug"]}/">{a["name"]}</a>' for a in AREAS_LIST)
    def cur(k): return ' aria-current="page"' if active == k else ''
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="One Build NYC home"><span class="brand-mark">1</span><span class="brand-text"><b>One Build</b><small>New York</small></span></a>
<nav class="nav" aria-label="Main">
<details class="dd"><summary>Services</summary><div class="dd-menu"><a href="/services/"><b>All services</b></a>{svc_links}</div></details>
<details class="dd"><summary>Areas</summary><div class="dd-menu">{area_links}</div></details>
<a href="/work/"{cur("work")}>Our Work</a>
<a href="/process/"{cur("process")}>Process</a>
<a href="/faq/"{cur("faq")}>FAQ</a>
<a href="/blog/"{cur("blog")}>Blog</a>
<a href="/contact/"{cur("contact")}>Contact</a>
</nav>
<div class="header-cta">
<a class="btn btn-line btn-sm" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
<a class="btn btn-accent btn-sm" href="/contact/">Book a Walkthrough</a>
<details class="menu-toggle"><summary aria-label="Open menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></summary>
<div class="mobile-menu"><a href="/">Home</a><a href="/services/">Services</a>{mob_svc}<a href="/work/">Our Work</a><a href="/process/">Process</a><a href="/faq/">FAQ</a><a href="/blog/">Blog</a><a href="/blog/">Blog</a><span style="padding:12px 0 4px;font-weight:700">Areas</span>{mob_area}<a href="/contact/">Contact</a><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></details>
</div>
</div></header>'''

def footer():
    svc = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)
    areas_f = "".join(f'<a href="/areas/{a["slug"]}/">{a["name"]}</a>' for a in AREAS_LIST)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="cols">
<div class="foot-brand"><a class="brand" href="/"><span class="brand-mark">1</span><span class="brand-text"><b>One Build</b><small>New York</small></span></a>
<p style="margin:18px 0 0;max-width:300px">Licensed contractors, plumbers, electricians and automation specialists. One contract, one crew, one schedule.</p></div>
<div><h4>Services</h4>{svc}</div>
<div><h4>Areas</h4>{areas_f}</div>
<div><h4>Company</h4><a href="/work/">Our Work</a><a href="/process/">Process</a><a href="/faq/">FAQ</a><a href="/blog/">Blog</a><a href="/services/">All Services</a><a href="/contact/">Contact</a></div>
<div><h4>Contact</h4><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{EMAIL}</a><p style="margin:10px 0 0">{AREAS}</p></div>
</div>
<div class="legal"><span>© 2026 One Build NYC. Licensed &amp; insured. NYC Home Improvement Contractor License #621290</span><span>Design-Build · NYC · New Jersey</span></div>
</div></footer>'''

def page(path, title, desc, body, active="", og=None, extra_ld=None):
    canon = DOMAIN + path
    ogimg = DOMAIN + img(og or "glass-house-kitchen")
    lds = list(extra_ld or [])
    lds.append(breadcrumb_ld(path, title))
    extra = "".join('<script type="application/ld+json">' + json.dumps(x) + '</script>' for x in lds)
    doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{ogimg}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#2E2B27">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{ld_json()}{extra}
</head><body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body></html>'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = add_img_dims(doc)
    with open(out, "w") as f: f.write(doc)
    PAGES.append(path)

PAGES = []
import hashlib
CSS_V = hashlib.md5(open(os.path.join(ROOT,'assets','site.css'),'rb').read()).hexdigest()[:8]
import datetime
BUILD_DATE = datetime.date.today().isoformat()

import re
from PIL import Image as _PIL
_DIMS = {}
def _dims(name):
    if name not in _DIMS:
        with _PIL.open(os.path.join(ROOT, "images", name)) as im: _DIMS[name] = im.size
    return _DIMS[name]
def add_img_dims(doc):
    def rep(m):
        tag = m.group(0)
        if " width=" in tag: return tag
        w, h = _dims(m.group(1))
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
    return re.sub(r'<img src="/images/([^"]+)"[^>]*>', rep, doc)

SEG_NAMES = {"services":"Services","areas":"Areas","work":"Our Work","process":"Process","faq":"FAQ","contact":"Contact","blog":"Blog"}
def breadcrumb_ld(path, title):
    parts = [p for p in path.strip("/").split("/") if p]
    items = [{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN + "/"}]
    acc = ""
    for i, seg in enumerate(parts):
        acc += "/" + seg
        name = SEG_NAMES.get(seg) or title.split(" | ")[0]
        items.append({"@type":"ListItem","position":i + 2,"name":name,"item":DOMAIN + acc + "/"})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def service_ld(s):
    return {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["kicker"],
            "description":s["intro"],"url":f'{DOMAIN}/services/{s["slug"]}/',
            "provider":{"@type":"HomeAndConstructionBusiness","name":"One Build NYC","url":DOMAIN,"telephone":"+1-888-781-7547"},
            "areaServed":["Manhattan","Brooklyn","Queens","Long Island","Westchester","New Jersey"]}

# ---------------------------------------------------------------- pieces
def fig(name, cls="", cap=None, eager=False):
    c = cap if cap is not None else CAP.get(name)
    capm = f'<figcaption>{esc(c)}</figcaption>' if c else ""
    return f'<figure class="{cls}"><img src="{img(name)}" alt="{esc(ALT[name])}" loading="{"eager" if eager else "lazy"}">{capm}</figure>'

def gallery(names, wide=()):
    return '<div class="gallery">' + "".join(fig(n, "w2" if n in wide else "") for n in names) + '</div>'

def pair(title, before, after, lb="Before", la="After"):
    return f'''<div><h3 style="font-family:var(--serif);font-weight:400;font-size:26px;margin-bottom:12px">{esc(title)}</h3>
<div class="pair"><figure><div class="ph"><img src="{img(before)}" alt="{esc(ALT[before])}" loading="lazy"></div><figcaption>{lb}</figcaption></figure>
<figure><div class="ph"><img src="{img(after)}" alt="{esc(ALT[after])}" loading="lazy"></div><figcaption>{la}</figcaption></figure></div></div>'''

def cta(bg="brick-loft-kitchen", heading="One call starts the whole project."):
    return f'''<section class="cta"><img src="{img(bg)}" alt="" loading="lazy">
<div class="wrap"><div class="cta-copy"><div class="eyebrow">Start a Project</div>
<h2 class="h2">{esc(heading)}</h2>
<p class="lead" style="margin:0">Tell us what you're building. We'll bring every trade to the walkthrough.</p>
<div class="btn-row"><a class="btn btn-accent" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn btn-line" href="/contact/">Request a Walkthrough</a></div></div>
<div class="cta-side"><b>One Build NYC</b><span>Licensed contractors, plumbers, electricians and automation specialists</span><span>{AREAS}</span><a href="mailto:{EMAIL}" style="color:var(--accent);font-weight:700">{EMAIL}</a></div>
</div></section>'''

def svc_cards(items=SERVICES):
    out = []
    for s in items:
        out.append(f'''<a class="card" href="/services/{s["slug"]}/"><div class="ph"><img src="{img(s["hero"])}" alt="{esc(ALT[s["hero"]])}" loading="lazy"></div>
<div class="body"><span class="kicker">{esc(s["kicker"])}</span><h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p><span class="more">View {esc(s["name"].lower())} →</span></div></a>''')
    return '<div class="grid g3">' + "".join(out) + '</div>'

WHY = '''<div class="points">
<div class="point"><b>One walkthrough</b><span>Every trade walks the space together on day one. One scope, one price.</span></div>
<div class="point"><b>Built in the right order</b><span>Plumbing, electrical and low-voltage rough-in happen together, before anything gets closed up.</span></div>
<div class="point"><b>One point of contact</b><span>One project lead, one schedule, one phone number from demo to handoff.</span></div>
<div class="point"><b>Licensed where it counts</b><span>Plumbing and electrical by licensed New York professionals, permitted and inspected.</span></div>
</div>'''

STEPS = '''<ol class="steps">
<li><span class="n">I</span><b>Walkthrough</b><span>Every trade on site with you and your designer.</span></li>
<li><span class="n">II</span><b>One Proposal</b><span>A single scope, schedule and price.</span></li>
<li><span class="n">III</span><b>Demo &amp; Rough-In</b><span>Plumbing, electrical and low-voltage go in together.</span></li>
<li><span class="n">IV</span><b>Close-Up &amp; Finishes</b><span>Drywall, tile, millwork and paint after inspections.</span></li>
<li><span class="n">V</span><b>Commission &amp; Handoff</b><span>Systems tested, programmed and explained to you.</span></li>
</ol>'''

# ---------------------------------------------------------------- home
cats = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
home = f'''<section class="hero">
<div class="hero-collage" aria-hidden="true">
<img src="{img("glass-house-kitchen")}" alt="" fetchpriority="high"><img src="{img("led-wall-lounge")}" alt=""><img src="{img("brass-zellige-bathroom")}" alt=""><img src="{img("vaulted-framing")}" alt=""><img src="{img("walnut-media-wall")}" alt="">
</div><div class="hero-veil" aria-hidden="true"></div>
<div class="wrap"><div class="hero-inner">
<div class="eyebrow">Design-Build · NYC · New Jersey</div>
<h1>Four licensed trades.<span>One crew. One schedule. One contract. One number to call. No finger-pointing.</span></h1>
<ul class="cats">{cats}</ul>
<div class="btn-row"><a class="btn btn-accent" href="/contact/">Book a Walkthrough</a><a class="btn btn-dark" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
<div class="trust"><span><b>✓</b> Licensed Contractors</span><span><b>✓</b> Licensed Plumbers</span><span><b>✓</b> Licensed Electricians</span><span><b>✓</b> Licensed Automation &amp; Low Voltage</span><span>Fully Insured</span></div>
</div></div></section>

<section class="section alt"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><div class="eyebrow">Why One Build</div>
<h2 class="h2">Renovations don't fail in the trades. They fail between them.</h2>
<p class="lead" style="margin:0">The wall gets closed before the speaker wire is in. The plumber waits on the GC, the GC waits on the electrician, and you end up managing all of it. One Build exists so that never lands on you.</p></div>
{WHY}
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div class="eyebrow">Services</div><h2 class="h2">Every trade your project needs. All licensed. All in-house.</h2></div>
{svc_cards()}
</div></section>

<section class="section alt"><div class="wrap">
<div class="section-head"><div class="eyebrow">Recent Work</div><h2 class="h2">From open walls to finished rooms.</h2></div>
<div class="seq" style="margin-bottom:40px">
<figure><div class="ph"><img src="{img("vaulted-framing")}" alt="{esc(ALT["vaulted-framing"])}" loading="lazy"></div><figcaption><b>01</b> · Framing</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-scaffolding")}" alt="{esc(ALT["vaulted-scaffolding"])}" loading="lazy"></div><figcaption><b>02</b> · Close-up</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-finishes")}" alt="{esc(ALT["vaulted-finishes"])}" loading="lazy"></div><figcaption><b>03</b> · Finishes</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-feature-wall")}" alt="{esc(ALT["vaulted-feature-wall"])}" loading="lazy"></div><figcaption><b>04</b> · Feature wall</figcaption></figure>
</div>
{gallery(["led-wall-lounge","double-vanity-marble-shower","private-theater","brick-loft-kitchen","black-white-smart-bath","kitchen-laundry-after"], wide=["led-wall-lounge"])}
<div style="margin-top:32px"><a class="btn btn-accent" href="/work/">See all projects</a></div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div class="eyebrow">Process</div><h2 class="h2">Built in the right order, the first time.</h2></div>
{STEPS}
<div style="margin-top:36px"><a class="btn btn-line" href="/process/">How we work</a></div>
</div></section>
{cta()}'''
page("/", "One Build NYC | Design-Build Renovations, Kitchens, Bathrooms & Home Theater",
     "Design-build renovation in NYC and New Jersey. Licensed contractors, plumbers, electricians and automation under one contract. Call (888) 781-7547.", home, og="glass-house-kitchen")

# ---------------------------------------------------------------- services index
idx = f'''<section class="page-hero"><img src="{img("vaulted-feature-wall")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Services</div><div class="eyebrow">Services</div>
<h1>Every trade, one contract.</h1><p>Renovation, plumbing, electrical and technology, planned together and built by one crew.</p></div></section>
<section class="section"><div class="wrap">{svc_cards()}</div></section>
{cta()}'''
page("/services/", "Services | One Build NYC", "Renovations, kitchens, bathrooms, gut renovations, plumbing, electrical, smart home, window treatments, lighting control and home theater in NYC and New Jersey.", idx)

# ---------------------------------------------------------------- service pages
for s in SERVICES:
    others = [o for o in SERVICES if o["slug"] != s["slug"]][:3] if s["slug"] in ("renovations",) else [o for o in SERVICES if o["slug"] != s["slug"]]
    # pick 3 related services
    order = [o["slug"] for o in SERVICES]
    i = order.index(s["slug"])
    related = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
    inc = "".join(f"<li>{esc(x)}</li>" for x in s["includes"])
    body = f'''<section class="page-hero"><img src="{img(s["hero"])}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / <a href="/services/">Services</a> / {esc(s["name"])}</div>
<div class="eyebrow">{esc(s["kicker"])}</div><h1>{esc(s["title"])}</h1><p>{esc(s["short"])}</p>
<div class="btn-row" style="margin-top:26px"><a class="btn btn-accent" href="/contact/">Book a Walkthrough</a><a class="btn btn-line" style="color:#fff;border-color:rgba(255,255,255,.6)" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
</div></section>

<section class="section"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><div class="eyebrow">{esc(s["name"])}</div>
<h2 class="h2">One crew. One schedule.</h2><p class="lead" style="margin:0">{esc(s["intro"])}</p></div>
<div><h3 style="font-size:13px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin-bottom:18px">What's included</h3><ul class="checklist">{inc}</ul></div>
</div></section>

<section class="section alt"><div class="wrap">
<div class="section-head"><div class="eyebrow">Our Work</div><h2 class="h2">{esc(s["name"])} projects</h2></div>
{gallery(s["gallery"], wide=[s["gallery"][0]])}
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div class="eyebrow">Why One Build</div><h2 class="h2">Every trade on the same schedule.</h2></div>
{WHY}
</div></section>

<section class="section" style="padding:56px 0"><div class="wrap"><div class="eyebrow" style="margin-bottom:16px">{esc(s["name"])} across NYC &amp; New Jersey</div><div class="btn-row">{"".join(f'<a class="btn btn-line btn-sm" href="/areas/{a["slug"]}/">{a["name"]}</a>' for a in AREAS_LIST)}</div></div></section>

<section class="section alt"><div class="wrap">
<div class="section-head"><div class="eyebrow">Related Services</div><h2 class="h2">Usually part of the same project.</h2></div>
{svc_cards(related)}
</div></section>
{cta(bg=s["hero"])}'''
    page(f'/services/{s["slug"]}/', f'{s["title"]} | One Build NYC',
         f'{s["short"]} {s["name"]} by One Build NYC: licensed trades, one contract. Call (888) 781-7547.', body, og=s["hero"], extra_ld=[service_ld(s)])

# ---------------------------------------------------------------- work
baths = SVC["bathrooms"]["gallery"]
work = f'''<section class="page-hero"><img src="{img("led-wall-lounge")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Our Work</div><div class="eyebrow">Our Work</div>
<h1>From open walls to finished rooms.</h1><p>Real projects, photographed on site, from rough-in to handoff.</p></div></section>

<section class="section"><div class="wrap">
<div class="block"><div class="block-head"><h3>Vaulted great room, studs to finish</h3><span>One crew · four stages</span></div>
<div class="seq">
<figure><div class="ph"><img src="{img("vaulted-framing")}" alt="{esc(ALT["vaulted-framing"])}" loading="lazy"></div><figcaption><b>01</b> · Framing</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-scaffolding")}" alt="{esc(ALT["vaulted-scaffolding"])}" loading="lazy"></div><figcaption><b>02</b> · Close-up</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-finishes")}" alt="{esc(ALT["vaulted-finishes"])}" loading="lazy"></div><figcaption><b>03</b> · Finishes</figcaption></figure>
<figure><div class="ph"><img src="{img("vaulted-feature-wall")}" alt="{esc(ALT["vaulted-feature-wall"])}" loading="lazy"></div><figcaption><b>04</b> · Feature wall</figcaption></figure>
</div></div>

<div class="block grid g2" style="gap:44px 28px">
{pair("Kitchen & laundry, gutted and rebuilt","kitchen-demo","kitchen-laundry-after")}
{pair("Brick loft kitchen","brick-loft-before","brick-loft-kitchen")}
{pair("Brownstone fireplace wall","fireplace-tv-before","fireplace-tv-after")}
{pair("Living room media wall","media-wall-before","media-wall-after")}
{pair("Country house addition","addition-exterior","addition-interior","Shell","Interior")}
{pair("Decks & pavers","composite-deck","deck-paver-patio","Composite deck","Deck with paver patio")}
</div>

<div class="block"><div class="block-head"><h3>Bathrooms</h3><span>Tile · plumbing · lighting · fixtures</span></div>
{gallery(baths, wide=["double-vanity-marble-shower","black-white-smart-bath"])}</div>

<div class="block"><div class="block-head"><h3>Theaters, lounges &amp; media</h3><span>Low voltage · lighting · AV</span></div>
{gallery(["led-wall-lounge","led-theater-lounge","private-theater","glass-cantilever-stair","lounge-bar","walnut-media-wall","dining-room"], wide=["led-wall-lounge"])}</div>

<div class="block" style="margin-bottom:0"><div class="block-head"><h3>Homes &amp; outdoor</h3><span>Renovation · lighting · exterior</span></div>
{gallery(["glass-house-kitchen","beamed-kitchen","primary-suite-shades","gallery-lighting","paver-patio","patio-lighting-rendering"], wide=["glass-house-kitchen","patio-lighting-rendering"])}</div>
</div></section>
{cta()}'''
page("/work/", "Our Work | Renovation, Bathroom & Home Theater Projects | One Build NYC",
     "Before and after renovation, kitchen, bathroom, home theater and outdoor projects by One Build NYC in NYC and New Jersey.", work, active="work", og="led-wall-lounge")

# ---------------------------------------------------------------- process
proc = f'''<section class="page-hero"><img src="{img("ceiling-rough-in")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Process</div><div class="eyebrow">Process</div>
<h1>Built in the right order, the first time.</h1><p>Every trade on the same schedule, so nothing gets ripped back open later.</p></div></section>
<section class="section"><div class="wrap">{STEPS}</div></section>
<section class="section alt"><div class="wrap">
<div class="section-head"><div class="eyebrow">On the Job</div><h2 class="h2">What each stage looks like.</h2></div>
<div class="gallery">
{fig("kitchen-demo", cap="Demo")}{fig("shade-selections", cap="Selections")}{fig("framing-rough-in", cap="Framing & plumbing")}{fig("ceiling-rough-in", cap="Rough-in")}
{fig("equipment-rack", cap="Low-voltage head end")}{fig("protected-job-site", cap="Protected job site")}{fig("electrical-panel-drivers", cap="Panel & drivers")}{fig("shade-power-panels", cap="Commissioned")}
</div></div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div class="eyebrow">Why One Build</div><h2 class="h2">One contract. One number to call.</h2></div>{WHY}</div></section>
{cta()}'''
page("/process/", "Our Process | One Build NYC", "How One Build NYC runs a renovation: one walkthrough, one proposal, coordinated rough-in, finishes and commissioning.", proc, active="process", og="ceiling-rough-in")

# ---------------------------------------------------------------- contact
checks = "".join(f'<label><input type="checkbox" name="services" value="{s["name"]}"> {s["name"]}</label>' for s in SERVICES)
contact = f'''<section class="page-hero" style="min-height:380px"><img src="{img("brick-loft-kitchen")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Contact</div><div class="eyebrow">Contact</div>
<h1>Book a walkthrough.</h1><p>Tell us about the project. We'll bring every trade to the walkthrough.</p></div></section>
<section class="section"><div class="wrap split" style="align-items:flex-start">
<div style="display:flex;flex-direction:column;gap:22px;flex:0 1 380px">
<div><div class="eyebrow" style="margin-bottom:10px">Call</div><a href="tel:{PHONE_TEL}" style="font-family:var(--serif);font-size:34px">{PHONE_DISPLAY}</a></div>
<div><div class="eyebrow" style="margin-bottom:10px">Email</div><a href="mailto:{EMAIL}" style="font-size:20px;font-weight:600">{EMAIL}</a></div>
<div><div class="eyebrow" style="margin-bottom:10px">Service Area</div><p style="margin:0;color:var(--ink2)">{AREAS}</p></div>
</div>
<form class="form" name="walkthrough" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="company_url">
<input type="hidden" name="form-name" value="walkthrough">
<p class="hidden"><label>Leave blank <input name="company_url"></label></p>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Email<input name="email" type="email" autocomplete="email"></label>
<label>Project location<input name="location" placeholder="Neighborhood or town"></label>
<fieldset class="full"><legend>What do you need?</legend><div class="checks">{checks}</div></fieldset>
<label class="full">Tell us about the project<textarea name="message"></textarea></label>
<div class="full"><button class="btn btn-accent" type="submit" style="border:0;cursor:pointer;font-family:inherit">Request a Walkthrough</button></div>
</form>
</div></section>'''
page("/contact/", "Contact | Book a Walkthrough | One Build NYC", "Book a walkthrough with One Build NYC. Call (888) 781-7547 or email info@onebuildnyc.com.", contact, active="contact")


# ---------------------------------------------------------------- FAQ + areas
def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items) + '</div>'
def faq_ld(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in items]}

faq_body = f"""<section class="page-hero" style="min-height:380px"><img src="{img("ceiling-rough-in")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / FAQ</div><div class="eyebrow">FAQ</div>
<h1>Questions we get before every project.</h1><p>Permits, timelines, buildings, pricing and how one contract works.</p></div></section>
<section class="section"><div class="wrap" style="max-width:900px">{faq_html(FAQS)}</div></section>
{cta()}"""
page("/faq/", "Renovation FAQ: Permits, Timelines & Costs in NYC | One Build NYC",
     "Answers about NYC renovation permits, co-op alterations, bathroom and gut renovation timelines, pricing, and adding smart home or theater during a remodel.",
     faq_body, active="faq", og="ceiling-rough-in", extra_ld=[faq_ld(FAQS)])

for a in AREAS_LIST:
    pts = "".join(f'<div class="point"><b>{esc(t)}</b><span>{esc(d)}</span></div>' for t, d in a["points"])
    items = [FAQS[i] for i in a["faq"]]
    others = "".join(f'<a class="btn btn-line btn-sm" href="/areas/{o["slug"]}/">{o["name"]}</a>' for o in AREAS_LIST if o["slug"] != a["slug"])
    body = f"""<section class="page-hero"><img src="{img(a["hero"])}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Areas / {esc(a["name"])}</div><div class="eyebrow">{esc(a["name"])}</div>
<h1>{esc(a["title"])}</h1><p>{esc(a["lead"])}</p>
<div class="btn-row" style="margin-top:26px"><a class="btn btn-accent" href="/contact/">Book a Walkthrough</a><a class="btn btn-line" style="color:#fff;border-color:rgba(255,255,255,.6)" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
</div></section>
<section class="section"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><div class="eyebrow">One Build in {esc(a["name"])}</div>
<h2 class="h2">Four licensed trades. One crew.</h2><p class="lead" style="margin:0">{esc(a["intro"])}</p></div>
<div class="points">{pts}</div>
</div></section>
<section class="section alt"><div class="wrap">
<div class="section-head"><div class="eyebrow">Services in {esc(a["name"])}</div><h2 class="h2">What we build here.</h2></div>
{svc_cards([SVC[x] for x in a["services"]])}
</div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div class="eyebrow">Our Work</div><h2 class="h2">Recent projects.</h2></div>
{gallery(a["gallery"], wide=[a["gallery"][0]])}
</div></section>
<section class="section alt"><div class="wrap" style="max-width:900px">
<div class="section-head"><div class="eyebrow">Questions</div><h2 class="h2">Common questions from {esc(a["name"])} clients.</h2></div>
{faq_html(items)}
<p style="margin-top:22px"><a href="/faq/" style="color:var(--accent);font-weight:700">See all questions →</a></p>
</div></section>
<section class="section" style="padding:56px 0"><div class="wrap"><div class="eyebrow" style="margin-bottom:16px">Other areas we serve</div><div class="btn-row">{others}</div></div></section>
{cta(bg=a["hero"])}"""
    page(f'/areas/{a["slug"]}/', f'{a["title"]} | One Build NYC',
         f'{a["lead"]} Licensed contractors, plumbers, electricians and automation under one contract. Call (888) 781-7547.',
         body, og=a["hero"], extra_ld=[faq_ld(items)])


# ---------------------------------------------------------------- blog
import datetime as _dt
def _fmt(d): return _dt.date.fromisoformat(d).strftime("%B %-d, %Y")
def _para(x):
    if isinstance(x, tuple) and x[0] == "ul":
        return '<ul class="checklist" style="grid-template-columns:1fr;margin:8px 0 22px">' + "".join(f"<li>{esc(i)}</li>" for i in x[1]) + "</ul>"
    return f"<p>{esc(x)}</p>"
def post_card(pst):
    return f"""<a class="card" href="/blog/{pst["slug"]}/"><div class="ph"><img src="{img(pst["hero"])}" alt="{esc(ALT[pst["hero"]])}" loading="lazy"></div>
<div class="body"><span class="kicker">{_fmt(pst["date"])}</span><h3>{esc(pst["title"])}</h3><p>{esc(pst["desc"])}</p><span class="more">Read article →</span></div></a>"""

for pst in POSTS:
    secs = "".join(f"<h2>{esc(h)}</h2>" + "".join(_para(x) for x in paras) for h, paras in pst["sections"])
    more = [o for o in POSTS if o["slug"] != pst["slug"]]
    body = f"""<section class="page-hero" style="min-height:420px"><img src="{img(pst["hero"])}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a></div><div class="eyebrow">{_fmt(pst["date"])}</div>
<h1>{esc(pst["title"])}</h1><p>{esc(pst["desc"])}</p></div></section>
<section class="section"><div class="wrap"><article class="article"><p class="lead">{esc(pst["intro"])}</p>{secs}
<div class="article-cta"><b>Planning a project?</b><span>One Build NYC brings licensed contractors, plumbers, electricians and automation specialists to one walkthrough.</span><div class="btn-row"><a class="btn btn-accent" href="/contact/">Book a Walkthrough</a><a class="btn btn-line" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></div>
</article></div></section>
<section class="section alt"><div class="wrap"><div class="section-head"><div class="eyebrow">Related Services</div><h2 class="h2">Where this applies.</h2></div>{svc_cards([SVC[x] for x in pst["services"]][:3])}</div></section>
<section class="section"><div class="wrap"><div class="section-head"><div class="eyebrow">More from the blog</div></div><div class="grid g3">{"".join(post_card(o) for o in more)}</div></div></section>"""
    art = {"@context":"https://schema.org","@type":"BlogPosting","headline":pst["title"],"description":pst["desc"],
           "datePublished":pst["date"],"dateModified":pst["date"],"image":DOMAIN + img(pst["hero"]),
           "author":{"@type":"Organization","name":"One Build NYC"},"publisher":{"@type":"Organization","name":"One Build NYC"},
           "mainEntityOfPage":f'{DOMAIN}/blog/{pst["slug"]}/'}
    page(f'/blog/{pst["slug"]}/', f'{pst["title"]} | One Build NYC', pst["desc"], body, active="blog", og=pst["hero"], extra_ld=[art])

blog_idx = f"""<section class="page-hero" style="min-height:380px"><img src="{img("vaulted-scaffolding")}" alt="" fetchpriority="high"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Blog</div><div class="eyebrow">Blog</div>
<h1>Notes from the job site.</h1><p>How renovations actually get built in NYC and New Jersey: permits, sequencing, technology and what to plan before the walls close.</p></div></section>
<section class="section"><div class="wrap"><div class="grid g3">{"".join(post_card(p_) for p_ in POSTS)}</div></div></section>
{cta()}"""
page("/blog/", "Renovation & Smart Home Blog | One Build NYC", "Practical guides on NYC renovations, co-op alterations, bathroom sequencing and pre-wiring for smart home and theater.", blog_idx, active="blog", og="vaulted-scaffolding")

thanks = f'''<section class="section" style="min-height:60vh;display:flex;align-items:center"><div class="wrap" style="display:flex;flex-direction:column;gap:20px;max-width:760px">
<div class="eyebrow">Thank you</div><h1 class="h2">We got your request.</h1>
<p class="lead" style="margin:0">We'll call you shortly to schedule the walkthrough. Need us sooner? Call <a href="tel:{PHONE_TEL}" style="color:var(--accent);font-weight:700">{PHONE_DISPLAY}</a>.</p>
<div><a class="btn btn-line" href="/work/">See our work</a></div></div></section>'''
page("/thank-you/", "Thank You | One Build NYC", "Thanks for contacting One Build NYC.", thanks)

# ---------------------------------------------------------------- 404, sitemap, robots, favicon
nf = '''<section class="section" style="min-height:60vh"><div class="wrap" style="display:flex;flex-direction:column;gap:20px">
<div class="eyebrow">404</div><h1 class="h2">That page isn't here.</h1><div><a class="btn btn-accent" href="/">Go home</a></div></div></section>'''
page("/404/", "Page not found | One Build NYC", "Page not found.", nf)
os.replace(os.path.join(ROOT, "404", "index.html"), os.path.join(ROOT, "404.html")); os.rmdir(os.path.join(ROOT, "404"))
PAGES.remove("/404/"); PAGES.remove("/thank-you/")

with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{BUILD_DATE}</lastmod></url>\n" for p in PAGES) + "</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
with open(os.path.join(ROOT, "assets", "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#F2EFEA"/><rect x="6" y="6" width="52" height="52" fill="none" stroke="#9A5824" stroke-width="5"/><text x="32" y="45" font-family="Georgia,serif" font-size="36" text-anchor="middle" fill="#9A5824">1</text></svg>')
print("built", len(PAGES), "pages")
