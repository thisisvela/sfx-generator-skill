"""Build the static demo site from the presets: `sfx site -o site`.

Pages: index (hero), library (every sound: play, in-video level, over narration, waveform, spectrogram, numbers,
recipe and parameters, the CLI command that recreates it, WAV/OGG/MP3 downloads), use (install, CLI, Python, the
skill, placing sounds in video, adding a recipe), how-it-works (building blocks, four recipes explained with
spectrograms, verification), licence, 404. Every page carries a canonical URL, Open Graph and Twitter
card tags; the home and library pages carry JSON-LD (SoftwareApplication, ItemList of AudioObject); the
build also writes sitemap.xml, robots.txt, og.png and llms.txt. Set SFX_SITE_VERIFICATION to a Search
Console token to add its meta tag; set SFX_GA_ID (G-XXXXXXXXXX) to add the Google Analytics tag.
Self-contained: no external fonts, scripts or assets unless SFX_GA_ID is set. Works without a server once hosted (fetch needs http, not file://), at phone
width, and audio starts only on a click.
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path

import numpy as np

from .. import REPO, REPO_URL, SITE_URL, __version__
from .. import inspect as insp
from .. import levels, presets, render, schema
from ..blocks import SR

HERE = Path(__file__).resolve().parent
FAMILY_ORDER = ["cinematic", "interface", "foley", "game", "nature", "ambience"]
FAMILY_BLURB = {
    "cinematic": "Whooshes, risers, impacts, a shimmer, the title hit and the end chime. Transitions and reveals.",
    "interface": "Pops, ticks, clicks, pings, chimes, questions, errors, signals and rewards. Things on screen.",
    "foley": "Keys, paper, stamps, locks, water, a heartbeat, a clock. Small physical events.",
    "game": "Explosions, guns, blades, magic, doors, tools, footsteps, horns and drums. The sounds a game needs.",
    "nature": "Rain, waves, thunder and wind: events to cue and seamless beds to sit under a scene.",
    "ambience": "Seamless loops that sit far under everything: a hum and a bed of air.",
}
CATEGORY_ORDER = ["transition", "anticipation", "reveal", "appear", "emphasis", "ui", "positive", "question",
                  "negative", "camera", "title", "end", "ambience"]

PLAY_SVG = '<svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true"><path d="M2.5 1.5v9l8-4.5z"/></svg>'
COPY_SVG = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" '
            'aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M3.5 10.5h-1a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v1"/></svg>')
DL_SVG = ('<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.4" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2.5v8M4.8 7.6 8 10.8l3.2-3.2M3 13.5h10"/></svg>')
GH_SVG = ('<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')
ICONS = {
    "all": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="2" width="5" height="5" rx="1"/><rect x="9" y="2" width="5" height="5" rx="1"/><rect x="2" y="9" width="5" height="5" rx="1"/><rect x="9" y="9" width="5" height="5" rx="1"/></svg>',
    "cinematic": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1.5 12.5c3-1 5-6 7-6s3 5 6 4"/></svg>',
    "interface": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="3" width="12" height="9" rx="1.5"/><path d="M6 14h4"/></svg>',
    "foley": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="8" r="2.5"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2"/></svg>',
    "ambience": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1.5 8c2-3 4-3 6 0s4 3 6 0"/><path d="M1.5 11c2-3 4-3 6 0s4 3 6 0" opacity=".5"/></svg>',
    "game": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M8 2.5l1.6 3.3 3.6.5-2.6 2.5.6 3.6L8 10.7l-3.2 1.7.6-3.6L2.8 6.3l3.6-.5z"/></svg>',
    "nature": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 12.5h10M4 9.5c2-2 3-5 4-7 1 2 2 5 4 7"/><path d="M6 12.5c0-2 1-3 2-3s2 1 2 3"/></svg>',
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


DEFAULT_DESCRIPTION = ("Sound effects made in code: deterministic numpy recipes. Apache 2.0: free to use anywhere, "
                       "and you own what you generate.")


def head_meta(title: str, description: str, page: str, jsonld: str = "") -> str:
    """Canonical URL, Open Graph and Twitter card, the Search Console tag if asked, and optional JSON-LD."""
    url = SITE_URL if page == "index" else f"{SITE_URL}{page}.html"
    out = [f'<link rel="canonical" href="{esc(url)}">',
           '<meta property="og:type" content="website">',
           '<meta property="og:site_name" content="sfx-generator">',
           f'<meta property="og:title" content="{esc(title)}">',
           f'<meta property="og:description" content="{esc(description)}">',
           f'<meta property="og:url" content="{esc(url)}">',
           f'<meta property="og:image" content="{esc(SITE_URL)}og.png">',
           '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
           '<meta property="og:image:alt" content="The spectrogram of the thunder preset: ink is loud.">',
           '<meta name="twitter:card" content="summary_large_image">',
           f'<meta name="twitter:title" content="{esc(title)}">',
           f'<meta name="twitter:description" content="{esc(description)}">',
           f'<meta name="twitter:image" content="{esc(SITE_URL)}og.png">']
    token = os.environ.get("SFX_SITE_VERIFICATION", "").strip()
    if token:
        out.append(f'<meta name="google-site-verification" content="{esc(token)}">')
    ga = os.environ.get("SFX_GA_ID", "").strip()
    if ga:                              # opt-in: the only external script the site ever loads, and only when asked
        if not re.fullmatch(r"G-[A-Z0-9]{6,14}", ga):
            raise ValueError(f"SFX_GA_ID must look like G-XXXXXXXXXX, got {ga!r}")
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>'
                   "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
                   f"gtag('js',new Date());gtag('config','{ga}');</script>")
    if jsonld:
        out.append(f'<script type="application/ld+json">{jsonld.replace("</", "<\\/")}</script>')
    return "\n".join(out)


def layout(title: str, body: str, page: str, base: str, description: str = "", quiet: bool = False,
           sections: list | None = None, jsonld: str = "") -> str:
    nav = [("index", "Home"), ("library", "Library"), ("use", "Use"), ("how-it-works", "How it works"),
           ("how-thunder-sounds", "Thunder"), ("faq", "FAQ"), ("licence", "Licence")]
    links = "".join(f'<a href="{base}{k}.html"{" aria-current=\"page\"" if k == page else ""}>{v}</a>' for k, v in nav)
    secs = ""
    if sections:
        secs = '<div class="sections"><div class="label">On this page</div>' + "".join(
            f'<a href="#{k}">{esc(v)}</a>' for k, v in sections) + "</div>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description or DEFAULT_DESCRIPTION)}">
{head_meta(title, description or DEFAULT_DESCRIPTION, page, jsonld)}
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}style.css">
<script>try{{var t=localStorage.getItem("sfx-theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script>try{{var n=localStorage.getItem("sfx-nav");var wide=window.innerWidth>=1024;if(n==="open"||(n===null&&wide))document.documentElement.classList.add("nav-open")}}catch(e){{}}</script>
</head>
<body{' class="quiet-bg"' if quiet else ''}>
<canvas id="bg" class="bg" aria-hidden="true"></canvas>
<div class="bg-fade" aria-hidden="true"></div>
<header class="top">
  <button class="menu" id="menu" aria-label="menu" aria-controls="side" aria-expanded="false"><span></span><span></span><span></span></button>
  <a class="brand" href="{base}index.html">sfx <small>v{__version__}</small></a>
  <span class="sp"></span>
  <button class="theme" id="theme" type="button" aria-label="switch between light and dark" title="Light or dark"><svg class="sun" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.6M8 12.9v1.6M1.5 8h1.6M12.9 8h1.6M3.4 3.4l1.1 1.1M11.5 11.5l1.1 1.1M3.4 12.6l1.1-1.1M11.5 4.5l1.1-1.1"/></svg><svg class="moon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" aria-hidden="true"><path d="M13.2 10.1A5.6 5.6 0 0 1 5.9 2.8a5.6 5.6 0 1 0 7.3 7.3z"/></svg></button>
  <a class="gh" href="{REPO_URL}" aria-label="GitHub">{GH_SVG}</a>
</header>
<aside class="side" id="side" aria-label="site navigation">
  <nav class="pages">{links}<a href="{REPO_URL}">GitHub</a></nav>
  {secs}
</aside>
<div class="scrim" id="scrim" aria-hidden="true"></div>
<div class="page">
{body}
<footer>
  <div>Apache 2.0 licensed. Every sound is synthesised by the code in the repository. Free to use anywhere; you own what you generate.</div>
  <div class="links"><a href="{REPO_URL}">GitHub</a><a href="{base}library.html">Library</a><a href="{base}use.html">Docs</a><a href="{base}llms.txt">llms.txt</a></div>
</footer>
</div>
<script src="{base}library.js"></script>
<script src="{base}app.js"></script>
<script src="{base}bg.js"></script>
</body>
</html>
"""


def code_block(text: str, label: str = "", lang_ps: bool = False) -> str:
    lines = text.strip("\n").split("\n")
    body = "\n".join((f'<span class="ps">$ </span>{esc(l)}' if lang_ps and l and not l.startswith(" ") else esc(l)) for l in lines)
    return (f'<div class="code"><div class="bar"><span>{esc(label)}</span>'
            f'<button class="copy" data-copy="{esc(text.strip())}" aria-label="copy">{COPY_SVG}</button></div>'
            f'<pre>{body}</pre></div>')


def _nums(e: dict) -> str:
    items = [(f"{e['seconds']} s", "length"), (f"{e['loudness_lufs']} LUFS", "loudest 100 ms"),
             (f"{e['peak_dbfs']} dBFS", "peak"), (f"{e['level_lu']:+d} LU", "level vs narration"),
             (f"{e['gain_db']} dB", "gain in a mix" + (" (capped)" if e["capped"] else "")),
             (f"{e['lead']} s", "lead before the cue")]
    return "".join(f'<div class="num"><b>{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in items)


def card(pr: presets.Preset, e: dict, wave: str, base: str) -> str:
    rec = schema.get(pr.recipe)
    defaults = rec.defaults()
    rows = "".join(
        f"<tr><td>{esc(p.name)}</td><td class=\"m\">{esc(e['params'][p.name])}{esc(' ' + p.unit if p.unit else '')}"
        f"{'' if defaults[p.name] == e['params'][p.name] else ' <span class=mute>(default ' + esc(defaults[p.name]) + ')</span>'}</td>"
        f"<td>{esc(p.doc)}</td></tr>" for p in rec.params)
    search = " ".join([pr.id, pr.id.replace("_", " "), pr.family, pr.category, pr.recipe, pr.use, pr.what, *pr.tags, pr.mood])
    mood = f'<span title="mood: the body is mastered to {levels.MOODS[pr.mood]} LUFS">{esc(pr.mood)}</span>' if pr.mood != "normal" else ""
    loop = '<span class="loop">loop</span>' if pr.loop else ""
    return f"""
<article class="card" id="{esc(pr.id)}" data-id="{esc(pr.id)}" data-search="{esc(search)}">
  <div class="head">
    <button class="pl" data-play="{esc(pr.id)}" aria-label="play {esc(pr.id)}">{PLAY_SVG}</button>
    <div><h3>{esc(pr.id)}</h3><p class="use">{esc(pr.use)}</p></div>
  </div>
  {wave}
  <div class="meta"><span>{e['seconds']:.2f} s</span><span>{esc(pr.category)}</span><span>{e['level_lu']:+d} LU</span>{mood}{loop}<span class="sp"></span><details class="dl-menu"><summary aria-label="download {esc(pr.id)}">{DL_SVG}</summary><div><a href="{base}sounds/wav/{esc(pr.id)}.wav" download>WAV 24-bit</a><a href="{base}sounds/ogg/{esc(pr.id)}.ogg" download>OGG q6</a><a href="{base}sounds/mp3/{esc(pr.id)}.mp3" download>MP3 160k</a><a href="{base}presets/{esc(pr.id)}.json" download>preset.json</a></div></details><a class="more" href="#{esc(pr.id)}" data-more>Details</a></div>
  <div class="detail">
    <div>
      <h4>What it is</h4><p>{esc(pr.what)}</p>
      <img data-src="{base}spec/{esc(pr.id)}.png" alt="spectrogram of {esc(pr.id)}" width="480" height="160">
      <div class="spec-cap">Spectrogram, 0 to 12 kHz, ink is loud. Vertical lines would be clicks; a line along the bottom would be DC.</div>
      <h4>Numbers</h4><div class="nums">{_nums(e)}</div>
      <h4>Downloads</h4>
      <div class="dl"><a href="{base}sounds/wav/{esc(pr.id)}.wav" download>WAV 24-bit</a><a href="{base}sounds/ogg/{esc(pr.id)}.ogg" download>OGG q6</a><a href="{base}sounds/mp3/{esc(pr.id)}.mp3" download>MP3 160k</a><a href="{base}presets/{esc(pr.id)}.json" download>preset.json</a></div>
    </div>
    <div>
      <h4>Recipe <span class="mute">{esc(pr.recipe)}</span></h4>
      <p>{esc(rec.doc)}</p>
      <div class="cmd"><span>{esc(e['cli'])}</span><button class="copy" data-copy="{esc(e['cli'])}" aria-label="copy command">{COPY_SVG}</button></div>
      <h4>Parameters</h4>
      <table>{rows}</table>
    </div>
  </div>
</article>"""


def jsonld_software(lib: dict) -> str:
    d = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "sfx-generator",
         "applicationCategory": "MultimediaApplication", "operatingSystem": "Windows, macOS, Linux",
         "softwareVersion": __version__, "url": SITE_URL, "codeRepository": REPO_URL, "license": "https://www.apache.org/licenses/LICENSE-2.0",
         "description": DEFAULT_DESCRIPTION, "author": {"@type": "Person", "name": "Vela", "url": f"https://github.com/{REPO.split('/')[0]}"},
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "featureList": [f"{len(lib)} ready-made sound effects", "deterministic numpy recipes with a parameter schema",
                         "a skill for Claude Code and Codex", "a local tuning page", "WAV, OGG and MP3 export"]}
    return json.dumps(d, ensure_ascii=False)


def jsonld_library(lib: dict, cat: dict) -> str:
    items = []
    for n, (sid, pr) in enumerate(lib.items(), 1):
        e = cat["sounds"][sid]
        secs = float(e["seconds"])
        items.append({"@type": "ListItem", "position": n, "item": {
            "@type": "AudioObject", "name": sid.replace("_", " "), "identifier": sid, "url": f"{SITE_URL}library.html#{sid}",
            "description": pr.what, "contentUrl": f"{SITE_URL}sounds/mp3/{sid}.mp3", "encodingFormat": "audio/mpeg",
            "duration": f"PT{secs:.2f}S", "genre": pr.family, "keywords": ", ".join(pr.tags),
            "license": "https://www.apache.org/licenses/LICENSE-2.0", "isAccessibleForFree": True,
            "creator": {"@type": "SoftwareApplication", "name": "sfx-generator", "url": SITE_URL}}})
    d = {"@context": "https://schema.org", "@type": "ItemList", "name": "sfx-generator library",
         "description": f"{len(lib)} sound effects synthesised by code, free to use anywhere.", "numberOfItems": len(lib),
         "itemListElement": items}
    return json.dumps(d, ensure_ascii=False)


def page_404(lib: dict) -> str:
    body = f"""
<main class="doc">
  <h1>Not here</h1>
  <p class="lede">That address has no page. The library has {len(lib)} sounds; the pages are below.</p>
  <section><ul>
    <li><a href="{SITE_URL}">Home</a></li>
    <li><a href="{SITE_URL}library.html">Library: every sound, play, download, numbers</a></li>
    <li><a href="{SITE_URL}use.html">Use: install, the skill, the CLI, levels in a video</a></li>
    <li><a href="{SITE_URL}how-it-works.html">How it works</a></li>
    <li><a href="{SITE_URL}licence.html">Licence</a></li>
  </ul></section>
</main>"""
    return layout("Not found · sfx-generator", body, "404", SITE_URL, "This page does not exist.", quiet=True)


def sitemap_xml() -> str:
    pages = [SITE_URL] + [f"{SITE_URL}{p}.html" for p in ("library", "use", "how-it-works", "how-thunder-sounds", "faq", "licence")]
    urls = "".join(f"  <url><loc>{esc(u)}</loc></url>\n" for u in pages)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"


def robots_txt() -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n"


def page_index(lib: dict, cat: dict, base: str) -> str:
    featured = ["whoosh", "pop", "success", "ping", "impact_soft", "explosion", "thunder", "sword_clash", "door_knock", "wave", "coin", "shimmer"]
    chips = "".join(f'<button class="chip" data-play="{sid}" aria-label="play {sid}"><span class="pl">{PLAY_SVG}</span>{sid}</button>'
                    for sid in featured if sid in lib)
    n = len(lib)
    words = {59: "Fifty-nine", 97: "Ninety-seven", 98: "Ninety-eight", 99: "Ninety-nine", 100: "A hundred"}.get(n, str(n))
    body = f"""
<main>
  <section class="hero">
    <h1>Sound effects that <em class="serif">come from code</em>.</h1>
    <p class="lede">A skill for Claude Code and Codex that turns a sentence into a finished sound, with {words.lower()} ready-made ones to start from. Deterministic numpy recipes, a tuning page. Apache 2.0: free to use anywhere, and you own what you generate.</p>
    <div class="install"><span class="ps">&gt;</span><span>Install the sound effects skill from {REPO_URL}</span><button class="copy" data-copy="Install the sound effects skill from {REPO_URL}: fetch and follow its INSTALL.md" aria-label="copy">{COPY_SVG}</button></div>
    <p class="mute" style="font-size:13px;margin:10px 0 0">Paste that into Claude Code or Codex. It installs the <code>sfx</code> command and the skills, and asks whether they are for this project or for you.</p>
    <div class="cta"><a class="btn primary" href="{base}use.html">Get started</a><a class="btn ghost" href="{base}library.html"><span class="dot"></span>Or browse the {n} sounds</a></div>
    <div class="chips">{chips}</div>
  </section>
  <section class="facts">
    <div class="fact"><h3>Yours to keep</h3><p>Every file is synthesised by a recipe in the repository. Nothing is recorded or downloaded, so what you generate is yours: free to use anywhere, in anything, with no credit to give.</p></div>
    <div class="fact"><h3>Deterministic</h3><p>A fixed seed per sound: a rebuild gives identical files, and the tests keep a hash of every one. Change a number on purpose, or not at all.</p></div>
    <div class="fact"><h3>Made for a voice</h3><p>Each sound carries its level against narration and its lead before the cue. Play the library at in-video level, or over a real narration line, before you place anything.</p></div>
  </section>
  <section class="audiences"><p>Free game sound effects with no attribution for <a href="{base}faq.html#game">game developers</a>; a one-line install that makes sounds on request for <a href="{base}faq.html#ai">AI-assisted development</a> in Claude Code and Codex; readable synthesis recipes, measurements and <a href="{base}how-thunder-sounds.html">the research behind them</a> for <a href="{base}faq.html#design">sound designers</a>.</p></section>
</main>"""
    return layout("sfx-generator", body, "index", base, jsonld=jsonld_software(lib))


def page_library(lib: dict, cat: dict, waves: dict, base: str, zips: dict) -> str:
    pills = "".join(f'<button class="pill{" on" if f == "all" else ""}" data-filter="{f}">{ICONS[f]}{f.capitalize() if f != "all" else "All"}</button>'
                    for f in ["all", *FAMILY_ORDER])
    cats = "".join(f'<button class="pill" data-filter="{c}">{c}</button>' for c in CATEGORY_ORDER
                   if any(p.category == c for p in lib.values()))
    sections = []
    for fam in FAMILY_ORDER:
        members = [p for p in lib.values() if p.family == fam]
        members.sort(key=lambda p: (CATEGORY_ORDER.index(p.category), p.id))
        cards = "".join(card(p, cat["sounds"][p.id], waves[p.id], base) for p in members)
        sections.append(f"""
<section class="section" id="fam-{fam}" data-family="{fam}" data-total="{len(members)}">
  <h2>{fam.capitalize()} <small>{len(members)} of {len(members)}</small><span class="sp"></span><a class="all" href="{base}downloads/sfx-{fam}.zip" download>{DL_SVG} Download {fam} ({zips[fam]})</a><button class="all" data-play-all>Play all</button></h2>
  <p class="mute" style="margin:4px 0 0;font-size:13.5px">{esc(FAMILY_BLURB[fam])}</p>
  <div class="grid">{cards}</div>
</section>""")
    body = f"""
<main class="wrap">
  <div class="filters">{pills}<span class="sp"></span>
    <label class="sw"><input type="checkbox" id="invideo" checked> in-video level</label>
    <label class="sw"><input type="checkbox" id="overvoice"> over narration</label>
    <input type="search" id="search" placeholder="Search: whoosh, chime, click, loop…" aria-label="search">
    <a class="pill dl-all" href="{base}downloads/sfx-all.zip" download>{DL_SVG} Download all ({zips['all']})</a>
  </div>
  <div class="filters" style="position:static;padding-top:0;font-size:12px"><span class="mute" style="font-size:12px;margin-right:4px">by category</span>{cats}</div>
  {''.join(sections)}
  <p class="empty" id="empty" style="display:none">Nothing matches. Try a family name, a use, or a word like soft, long, low.</p>
  <p class="note mute" style="padding:28px 0 40px;font-size:13px">In-video level places each sound against a −14 LUFS narration with the −6 dBFS peak cap, so quiet sounds sound quiet. Over narration plays a real line and lands the sound on its cue, respecting its lead. A limiter sits on the output. Audio starts only after a click.</p>
</main>"""
    return layout("Library · sfx-generator", body, "library", base, "Every sound in the library: play it at in-video level, over narration, see its spectrogram, recipe and parameters, and download WAV, OGG or MP3.",
                  sections=[(f"fam-{f}", f.capitalize()) for f in FAMILY_ORDER], jsonld=jsonld_library(lib, cat))


def page_use(lib: dict, base: str) -> str:
    tr = "".join(f"<tr><td class=\"m\">{esc(k)}</td><td class=\"m\">{esc(v or '—')}</td></tr>" for k, v in levels.TRANSITION_SFX.items())
    lv = "".join(f"<tr><td class=\"m\">{esc(k)}</td><td class=\"m\">{v:+d}</td></tr>" for k, v in levels.CATEGORY_LU.items())
    sections = [("claude", "Claude Code"), ("codex", "Codex"), ("ask", "What to say"), ("tune", "Tuning page"), ("video", "In video"), ("developers", "Developers"), ("recipe", "Adding a recipe")]
    paste = f"Install the sound effects skill from {REPO_URL}: fetch and follow its INSTALL.md"
    body = f"""
<main class="doc">
  <h1>Use</h1>
  <p class="lede">The primary way to use this is as a skill inside your coding agent. Paste one line, answer one question, then ask for sounds in plain words.</p>

  <section id="claude"><h2>Install in Claude Code</h2>
  <p>Paste this into a Claude Code session, in the project where you want the sounds:</p>
  {code_block(paste, "paste into Claude Code")}
  <p>Claude reads <code>INSTALL.md</code> from the repository and follows it: it checks Python, installs the <code>sfx</code> command as an isolated tool (uv or pipx, with a private venv as the fallback), asks whether the skills are <b>for this project</b> or <b>for you</b>, installs the plugin at that scope, runs a smoke test and tells you what to say next.</p>
  <p>Prefer to do it by hand? The plugin installs from the repository in one command (Claude Code 2.1.292 or later; pick the scope in the dialog):</p>
  {code_block("/plugin install sfx-generator --marketplace " + REPO, "in a Claude Code session")}
  {code_block("claude plugin install sfx-generator --marketplace " + REPO + " --scope project", "or from your shell")}
  <p>Then install the command once per machine (see <a href="#developers">developers</a> for the exact line) and start a new session. The skills show up as <code>/sfx-generator:make-sound-effect</code> and <code>/sfx-generator:create-sound-recipe</code>, and Claude uses them on its own when a request matches.</p>
  </section>

  <section id="codex"><h2>Install in Codex</h2>
  <p>Paste the same line into Codex (CLI, IDE extension or app):</p>
  {code_block(paste, "paste into Codex")}
  <p>Codex finds skills in <code>.agents/skills</code> of a repository and in <code>~/.agents/skills</code> for you. The install guide copies the two skills into your project, or clones the repository once and links it for every project, and installs the <code>sfx</code> command the same way. Invoke them as <code>$make-sound-effect</code> and <code>$create-sound-recipe</code>, or just ask; Codex picks them up when a request matches.</p>
  <p class="note">By hand: clone the repository and copy <code>skills/make-sound-effect</code> and <code>skills/create-sound-recipe</code> into <code>.agents/skills/</code>, then install <code>sfx</code> as under developers.</p>
  </section>

  <section id="ask"><h2>What to say</h2>
  <p>Describe the moment and the character; the skill maps the words to a family and the nearest of the 98 presets, improvises three to six variants, checks each one by numbers and spectrogram, and shows you an audition page.</p>
  {code_block('''make a quick whoosh for a slide transition
a soft two-note success chime, about half a second
a notification a fifth up, bright and dry
a low hum to sit under the whole scene, as a loop
something for a value dropping into a table, playful
redo b with less room and a longer tail''', "things to ask")}
  <p>Sounds land in <code>assets/sfx/&lt;name&gt;/</code> in your project as WAV, OGG and MP3, with a preset JSON that recreates them and the level they will sit at under narration. Every run reads the skill's lessons ledger first and appends what it learned, so the next request starts smarter.</p>
  </section>

  <section id="tune"><h2>The tuning page</h2>
  <p>Ask for it: <em class="serif">open the tuning page for variant b</em>, or <em class="serif">let me tune the ping</em>. The skill runs <code>sfx tune &lt;preset&gt;</code>, which starts a local page at <code>http://127.0.0.1:8765</code> and opens it in your browser (it prints the address if it cannot). The sliders come from the recipe's schema; every change is rendered by the same Python code and comes back with the numbers, a waveform and a spectrogram, usually well under 300 ms for short sounds.</p>
  <figure class="figure shot"><img src="{base}tune.png" alt="The tuning page for the ping preset: sliders for every parameter on the left; play, A/B and level controls, the waveform, the spectrogram and the measured numbers on the right" width="1280" height="900" loading="lazy"><figcaption>The tuning page for <code>ping</code>: every parameter of the recipe on the left, the rendered waveform, spectrogram and numbers on the right. Save preset writes the JSON; Export writes WAV, OGG and MP3.</figcaption></figure>
  <p>On the page: A/B against the original, loop, in-video level and over-narration playback, stereo width and a left/right offset with a mono-sum check, gain, and the preset's category, lead and use. Nothing is written until you press <b>Save preset</b> or <b>Export</b>; tell the agent when you are done and it stops the server and picks up the saved preset.</p>
  {code_block("sfx tune ping                       # a library sound\nsfx tune assets/sfx/chime/success_b.json   # one of your variants", "by hand", True)}
  </section>

  <section id="video"><h2>Placing sounds in video</h2>
  <p>These rules were measured on real narrated videos. Narration sits at about −14 LUFS integrated. Each sound's loudness is its loudest 100 ms, K-weighted; its level is set in LU relative to the narration, by category:</p>
  <table class="tbl"><tr><th>Category</th><th>LU vs narration</th></tr>{lv}</table>
  <p>The gain that places a sound is <code>min(ref + level − loudness_max, −6 dBFS − peak)</code>: no single effect peaks above −6 dBFS in the mix. When the cap wins the sound is "capped" and quieter than its level asks; fix that in the recipe with a little tonal body under a click, never with gain.</p>
  <h3>Mood: how big a sound is meant to feel</h3>
  <p>Decide the weight of a sound from the situation it belongs to, not from its peak. Every master is peak-normalised, so a dense loop (rain, wind) sits loud all the way through while a peaky event (thunder: one crack, a long quiet rumble) is loud for 100 ms and then hides under the bed. A preset's <code>mood</code> fixes that at the master: <b>huge</b> (fear, violence, the sky: thunder, an explosion, a cannon) lifts the loudest second of the sound to −12 LUFS and lets the limiter hold the crack above it; <b>big</b> (a gunshot, a heavy impact, a slam) to −14 LUFS; <b>normal</b> leaves the recipe's own master alone. The body carries the weight, the way a film mix does; the level table then places that body in the mix, and the mood also sets the peak cap there: a huge sound may peak at −3 dBFS, a big one at −4.5, an ordinary effect at −6. That is where thunder's extra weight against a voice comes from, not from crushing its shape.</p>
  <ul>
    <li><b>Lead.</b> A sound starts <code>lead</code> seconds before its cue. Whooshes peak just after the cue; risers, swells and the countdown end on it; event sounds start when their picture is visible.</li>
    <li><b>Density.</b> At most about 8 sounds a minute, at least 1 s apart. Real videos used 4.4 a minute. Every cue has a written reason.</li>
    <li><b>Too quiet is the common failure.</b> A first level table 5 dB lower than this one was inaudible under speech.</li>
    <li><b>Very short sounds vanish under speech.</b> Under a voice use 0.1 s or more of real energy: <code>glitch_burst</code>, not <code>glitch</code>.</li>
    <li><b>Tails.</b> Keep chime tails under about 0.5 s where speech follows.</li>
    <li><b>The master.</b> narration + effects bed → one gain to −14 LUFS → a look-ahead limiter at −1.5 dBFS (<code>levels.limit</code>).</li>
  </ul>
  <h3>Default transition sounds</h3>
  <table class="tbl"><tr><th>Transition</th><th>Sound</th></tr>{tr}</table>
  <p>Title cards use <code>swoosh_up</code> then <code>title_hit</code>; the end card uses <code>end_chime</code>.</p>
  </section>

  <section id="tune"><h2>Tuning</h2>
  <p><code>sfx tune ping</code> starts a localhost page whose sliders come from the recipe's schema. Every change is rendered by the same Python code and comes back with the numbers, a waveform and a spectrogram, usually well under 300 ms for short sounds. It has A/B against the original preset, loop playback, in-video level and over-narration playback, stereo width and a left/right offset with a mono-sum check, and gain. Nothing is written until you press Save preset or Export.</p>
  </section>

  <section id="developers"><h2>For developers: the command and the Python API</h2>
  <p>The package is not on PyPI; it installs from GitHub. Python 3.10 or newer. The <code>ffmpeg</code> extra brings a static ffmpeg for OGG and MP3 (WAV never needs it).</p>
  {code_block('uv tool install "sfx-generator[ffmpeg] @ git+' + REPO_URL + '"', "uv (isolated)", True)}
  {code_block('pipx install "sfx-generator[ffmpeg] @ git+' + REPO_URL + '"', "pipx (isolated)", True)}
  {code_block('pip install "sfx-generator[ffmpeg] @ git+' + REPO_URL + '"', "pip, into the current environment", True)}
  <p class="note">To work on the recipes: clone, then <code>pip install -e ".[dev]"</code> and <code>pytest -q</code>.</p>
  <h3>The CLI</h3>
  {code_block('''sfx list                         # the library, with use, lead and level
sfx list --family foley --json
sfx schema whoosh                # every parameter: default, range, step, unit, meaning
sfx render whoosh -o whoosh      # whoosh.wav, .ogg, .mp3
sfx render whoosh d=0.5 f_peak=3200 pan_from=0 pan_to=0 -o whoosh_centred --preset
sfx render success.json -o success   # a saved preset
sfx render-all -o out/library    # the whole library plus catalog.json
sfx make "soft two-note success chime, about half a second"   # 4 variants + audition page + journal
sfx make "quick whoosh for a slide" -n 6 --open
sfx inspect out/library/ogg/ping.ogg --category emphasis --png ping.png
sfx tune ping                    # the local tuning page
sfx site -o site                 # this site''', "sfx", True)}
  <p>Parameter overrides are <code>name=value</code>; values are JSON, so <code>seed=7</code>, <code>d=0.5</code>, and strings as-is. Unknown names and values outside a parameter's range are refused.</p>
  <h3>Python</h3>
  {code_block('''from pathlib import Path
from sfx_generator import presets, render, schema, levels, inspect as insp

x = presets.find("whoosh").render()            # (n, 2) float64 at 48 kHz, peak -1.5 dBFS
render.export(x, Path("whoosh"))                # whoosh.wav / .ogg / .mp3

rec = schema.get("whoosh")                     # the recipe and its schema
y = rec.render({**rec.defaults(), "d": 0.5, "f_peak": 3200})
print(insp.report(y, category="transition"))   # numbers, warnings, in-mix placement

g = levels.gain_for(y, levels.CATEGORY_LU["transition"])   # dB to sit -4 LU under a -14 LUFS narration
from sfx_generator.make import make
run = make("a soft error sound", Path("out/error"), n=4)   # variants, audition page, journal''', "python")}
  </section>

  <section id="recipe"><h2>Adding a recipe</h2>
  <p>A recipe is a function of keyword parameters that returns a (n, 2) float array at 48 kHz, registered with its schema:</p>
  {code_block('''from sfx_generator.blocks import _tr, env, finish, osc, pan
from sfx_generator.schema import P, SEED, recipe

@recipe("beep", family="signal", doc="A plain sine beep with a soft edge.",
        tips="f is the pitch; d the length; tau the decay.",
        params=[P("f", 880, 100, 8000, 1, "Hz", "pitch"),
                P("d", 0.12, 0.03, 1.0, 0.005, "s", "length"),
                P("tau", 0.06, 0.01, 0.5, 0.001, "s", "decay"),
                SEED(301)])
def beep(*, f, d, tau, seed):
    t = _tr(d)
    return finish(pan(osc(f, t) * env(t, 0.003, tau), 0.0))''', "src/sfx_generator/recipes/signal.py")}
  <p>Then add a preset JSON in <code>src/sfx_generator/library/presets/</code> (id, recipe, params, family, category, use, what, lead, tags), run <code>sfx inspect beep</code> and the tests, and let the <code>create-sound-recipe</code> skill walk the rest. Rules that bite: integrate frequency into phase (<code>osc</code>), give every note a release fade, remove DC from Karplus-Strong excitations, keep the seed fixed, and never rename a shipped id.</p>
  </section>
</main>"""
    return layout("Use · sfx-generator", body, "use", base, "Install the skill in Claude Code or Codex, what to say, the tuning page, placing sounds in a narrated video, the CLI and Python API, adding a recipe.", quiet=True, sections=sections)


def page_how(lib: dict, cat: dict, waves: dict, base: str) -> str:
    blocks = [
        ("white, pink", "Seeded noise, peak-normalised. Pink (a 4-pole IIR) is smoother; whooshes mix 0.7 pink with some white air."),
        ("svf_bandpass", "A state-variable band-pass whose centre and Q can be arrays, so the band moves sample by sample. The heart of every whoosh; run twice for a clearer band."),
        ("lowpass, highpass", "Butterworth filters. LP 9-11 kHz takes the fizz off noise; HP 120 Hz kills DC."),
        ("logsweep", "A frequency curve through (position, Hz) points, interpolated in log frequency. Every glide."),
        ("pan", "Equal-power pan, scalar or array. A right-to-left pan sells 'something flew past'."),
        ("reverb, room", "Convolution with a synthetic impulse: two channels of decaying white noise, low-passed, with a 12 ms pre-delay feel. No room recordings."),
        ("env, glide, osc", "Attack-then-exponential-decay envelopes; exponential pitch glides; a sine whose frequency is integrated into phase (never sin(2πf(t)t))."),
        ("tone", "A sum of partials (ratio, amp, tau) with an automatic release. Inharmonic ratios make bells and glass: bell 1 : 2 : 2.76 : 5.4, glass 1 : 2.32 : 4.25, marimba 1 : 3.93 : 9.2."),
        ("burst, ks_pluck", "A short band-limited noise transient; a Karplus-Strong string with DC removed from the excitation."),
        ("place, release, finish", "Mix parts at start times with a safety release; cosine fades (a cut while ringing is a click); LP 15 kHz, trim the tail, normalise to -1.5 dBFS."),
    ]
    rows = "".join(f"<tr><td class=\"m\">{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in blocks)
    figs = [
        ("whoosh", "Band-passed noise. The dark band rises to 2.6 kHz at the peak position and falls back; the pan moves it right to left. Its lead (0.265 s) puts the loudest moment just after the cue."),
        ("impact_soft", "A sub sine falling from 110 to 42 Hz (the line at the bottom), a 22 ms low-passed knock (the vertical smudge at the start), a band of body at 190 Hz, and a reverb tail that trims itself."),
        ("ding", "Two bell stacks, C5 then G5, 70 ms apart. The partials are slightly off whole-number ratios, which is what makes a bell and not an organ. The tails stop under 0.5 s so speech can follow."),
        ("tick", "A 2 ms noise snap, a 3.4 kHz ring and a little body at a third of that. The body is why a 40 ms tick is still heard under a voice without hitting the -6 dBFS peak cap."),
    ]
    figures = "".join(f"""
<div class="figure">
  <div class="row"><button class="pl" data-play="{sid}" aria-label="play {sid}">{PLAY_SVG}</button><b>{sid}</b><span class="mute">{cat['sounds'][sid]['seconds']} s · {cat['sounds'][sid]['loudness_lufs']} LUFS</span></div>
  {waves[sid]}
  <img src="{base}spec/{sid}.png" alt="spectrogram of {sid}" width="480" height="160" loading="lazy">
  <div class="cap">{esc(text)}</div>
</div>""" for sid, text in figs)
    sections = [("why", "Why code"), ("blocks", "Blocks"), ("recipes", "Four recipes"), ("levels", "Levels"), ("verify", "Verification"), ("determinism", "Determinism")]
    article = f'<p>For a natural sound built from measurements rather than from the word, read <a href="{base}how-thunder-sounds.html">how thunder really sounds, and how to synthesise it</a>.</p>'
    body = f"""
<main class="doc">
  <h1>How it works</h1>
  <p class="lede">Every sound is a short numpy program: noise, filters, sines, envelopes, a synthetic room. Nothing is recorded.</p>

  <section id="why"><h2>Why code</h2>
  <p>A sound made by code has one owner: whoever runs the code. There is nothing to clear, credit or check, and nothing that changes under you later. It also means every sound can be remade, resized and retuned from its numbers, which a recording never can. The interface sounds here were designed to measured targets (length, decay, centroid, pitch track), so their character is deliberate rather than found.</p>
  </section>

  <section id="blocks"><h2>Building blocks</h2>
  <table class="tbl"><tr><th>Block</th><th>What it does</th></tr>{rows}</table>
  </section>

  <section id="recipes"><h2>Four recipes, explained</h2>
  <p>Spectrograms run 0 to 12 kHz, the whole sound wide; ink is loud. Press play to hear each one.</p>
  {figures}
  {article}
  </section>

  <section id="levels"><h2>Levels</h2>
  <p>A sound's loudness is its loudest 100 ms, K-weighted (EBU R128). The standard 400 ms window under-rates clicks and pops by several dB. Each category has a level in LU relative to the narration; the gain that places a sound is capped so it never peaks above −6 dBFS. In the last real video, 28 cues sat a median 8.8 LU under the voice's momentary loudness, which is the target band (8 to 14 LU under).</p>
  </section>

  <section id="verify"><h2>Verification without ears</h2>
  <p>No model can hear. Every sound is checked by numbers and pictures, then a person listens:</p>
  <ul>
    <li><b>Numbers.</b> Length, attack, time to fall 20 dB, spectral centroid, a five-point pitch track (STFT peak, 1,024-point frames, 128-sample hop, the 0 Hz bin skipped), DC offset, the level in the last 2 ms, peak, loudest 100 ms, mono-sum loss.</li>
    <li><b>Pictures.</b> A spectrogram beside a reference: vertical lines are clicks, a smear at 0 Hz is DC, a tail past the frame is a decay too long for speech.</li>
    <li><b>Warnings.</b> DC over 0.002 on sounds longer than 0.15 s; an end above −40 dB of the peak; less than 30 ms of energy under 0.1 s; a peak off −1.5 dBFS; more than 3 dB lost in mono.</li>
    <li><b>Tests.</b> Every preset passes those checks in CI, and its category lands where the level table says.</li>
    <li><b>A person.</b> An audition page with A then B, play all, a redo flag and a note per row. Twenty-three replacements were approved in one pass this way.</li>
  </ul>
  </section>

  <section id="determinism"><h2>Determinism</h2>
  <p>A fixed seed per sound and no unseeded randomness anywhere. The tests hold a hash of every preset's float32 samples; the 37 original sounds also match the files shipped before this package existed, decoded from their OGG masters. One trap worth knowing: two time helpers, <code>int(SR·d)</code> and <code>int(round(SR·d))</code>, give different sample counts for some lengths (48000 × 2.4 is 115199.99…), so each recipe keeps the variant it was approved with.</p>
  </section>
</main>"""
    return layout("How it works · sfx-generator", body, "how-it-works", base, "The building blocks, four recipes explained with spectrograms, the level rules, and how every sound is verified without ears.", quiet=True, sections=sections)


INSTALL_BLOCKS = (
    code_block("Install the sound effects skill from " + REPO_URL + ": fetch and follow its INSTALL.md", "paste into Claude Code or Codex: the agent does the rest")
    + code_block("/plugin install sfx-generator --marketplace " + REPO, "Claude Code, by hand, in a session (pick the scope in the dialog)")
    + code_block("claude plugin install sfx-generator --marketplace " + REPO + " --scope project", "Claude Code, by hand, from your shell (--scope user for every project)", True)
    + code_block("git clone --depth 1 " + REPO_URL + " /tmp/sfx-generator-skill\nmkdir -p .agents/skills\ncp -r /tmp/sfx-generator-skill/skills/make-sound-effect /tmp/sfx-generator-skill/skills/create-sound-recipe .agents/skills/", "Codex, by hand: copy the two skills into the project", True)
    + code_block('uv tool install "sfx-generator[ffmpeg] @ git+' + REPO_URL + '"', "the sfx command itself (pipx or pip work too); the agent route installs it for you", True)
    + code_block("make a quick whoosh for a slide transition\na soft two-note success chime, about half a second\na short low hit for landing, for a platformer\na coin pickup, brighter than the library one\na loop of light rain to sit under the whole scene", "then say, in your own words")
)
TUNER_BLOCKS = (
    code_block("open the tuning page for variant b\nlet me tune the ping\ntune the thunder: fewer strikes, longer rumble", "what to say to the agent; it starts the server and gives you the address")
    + code_block("sfx tune ping                                   # a library sound\nsfx tune assets/sfx/chime/success_b.json        # one of your own presets, saved next to it\nsfx tune thunder --port 8766 --no-open          # another port; prints the address instead of opening a browser", "by hand, from your shell; Ctrl-C stops it", True)
)


FAQ = [
    ("For game developers", "game", [
        ("Can I use these sounds in a commercial game, app or video?",
         "Yes. Apache 2.0 covers the code, the presets and every sound they produce. There is no fee, no licence key and no limit on copies, players or revenue."),
        ("Do I need to credit anyone?",
         "No. Nothing in a game, video, app or product needs attribution for these sounds. A credit is welcome, never required."),
        ("What formats do I get?",
         "WAV (24-bit, 48 kHz, stereo), OGG Vorbis (quality 6) and MP3 (160 kb/s), plus the preset JSON that recreates the sound. The library page has a zip per family and one for everything."),
        ("Can I get a sound shorter, longer, lower or brighter?",
         "Yes. Every sound is a recipe with named parameters, so `sfx render explosion d=0.6` or a slider on the tuning page gives a new version with the same character. The same parameters and seed give the same file every time."),
        ("Which sounds are for games?",
         "The game family: explosions, cannon and tank fire, gunshot, machine gun and shotgun, ricochet, arrow, sword swing and clash, punch and hurt, spells, fireball, heal and power-up, burning wood, doors, hammer and anvil, footsteps, jump and land, chest, reload, game over, war horn and marching drums. The interface family adds coin, level up, zap and the pops, clicks and chimes a menu needs.",
         '<p><a href="{base}library.html?f=game">Open the library with the game family selected</a>: play each one at its in-mix level, download WAV, OGG or MP3, or take the whole family as one zip. The <a href="{base}library.html?f=interface">interface family</a> has the menu and reward sounds.</p>'),
        ("Are the sounds the same for everyone who downloads them?",
         "Yes. A fixed seed per sound and no unseeded randomness anywhere: a rebuild on any machine gives identical samples. Change the seed and you get a sibling of the same sound for free."),
    ]),
    ("For AI-assisted game development", "ai", [
        ("How do I use this from Claude Code or Codex?",
         "Paste one line into the agent and it installs the sfx command and the two skills by following INSTALL.md; or install by hand with the commands below. Then ask in your own words: \"a short low hit for landing\", \"a coin pickup, brighter\", \"a loop of rain to sit under the scene\".",
         INSTALL_BLOCKS),
        ("What happens when I ask for a sound?",
         "The skill maps the words to a sound family and the nearest preset, renders three to six variants (a seed sibling and seeded nudges within each parameter's range), measures every one, and opens an audition page where you play them at their in-video level, over a narration line if you like, and mark the one to keep. The chosen sound lands in your project as WAV, OGG, MP3 and a preset JSON."),
        ("Are the sounds AI-generated?",
         "No. Every sound is synthesised by deterministic numpy recipes written as code; no model generates audio and nothing is recorded or downloaded. The assistant chooses and adjusts parameters, reads the numbers, and writes what it learned into a lessons ledger for the next run."),
        ("Can I adjust a sound by hand?",
         "Yes. Say \"open the tuning page\" and a local page appears with a slider for every parameter; each change is re-rendered by the same Python code and comes back with the numbers, a waveform and a spectrogram. Save preset writes the JSON; Export writes the files. From a shell, sfx tune does the same for a library sound or one of your own presets.",
         TUNER_BLOCKS),
        ("What if no sound in the library fits?",
         "The second skill, create-sound-recipe, adds a new kind of sound the way the library was built: the physics in words first, then a building block, the recipe with its parameter schema, a preset, the measurements, the tests and the docs."),
        ("Does anything leave my machine?",
         "No. Rendering, the audition page and the tuning page all run locally; the tuning server listens on 127.0.0.1 only and answers its own page alone. There is no account, no key and no telemetry."),
    ]),
    ("For sound designers and editors", "design", [
        ("How are the sounds made?",
         "From a small set of numpy and scipy blocks: seeded white and pink noise, a state-variable band-pass whose centre can move every sample, stacks of inharmonic partials for bells and glass, pitch glides integrated into phase, a Karplus-Strong string, short band-limited bursts, and a synthetic reverb. Each recipe is one Python function with a schema that names every parameter, its range and its meaning."),
        ("How is a sound verified when nobody can listen?",
         "By numbers and pictures first: loudness of the loudest 100 ms (K-weighted), peak, spectral centroid, decay to -20 dB, a pitch track, DC offset, end level, mono-sum loss, and a spectrogram where clicks show as vertical lines and DC as a smear along the bottom. Then a person listens and decides."),
        ("How loud should an effect sit under narration?",
         "With narration at about -14 LUFS, an effect's loudness is its loudest 100 ms and its level depends on its job: transitions, appearances and emphasis at -4 LU, interface at -6, titles at +2, ambience beds at -16. The gain is the smaller of that and whatever keeps the peak under -6 dBFS; a sound starts its lead before the cue; at most about eight sounds a minute."),
        ("Why does the thunder here sound like thunder?",
         "Because it was built to measurements of real strikes rather than to the word: the weight sits at 80 to 250 Hz, not in the sub; the rumble is a train of thousands of small impulsive arrivals (kurtosis 7 to 30 in that band, where filtered noise scores about 1 and reads as wind); the crack builds for 100 to 300 ms as a crackle instead of hitting at once; strikes come in clusters with irregular gaps. The article on this site walks through it."),
        ("Can I read or change a recipe?",
         "Yes. The recipes are plain Python in the repository, one module per family, each with its parameter schema and a note on what every value does; the references explain every block. Change what you like and ship the result under any licence you choose; the sounds you generate are yours."),
        ("What is the sample rate and headroom?",
         "48 kHz stereo, every master peak-normalised to -1.5 dBFS. Big sounds carry a mood (huge, big) that masters the loudest second rather than the peak so a crack does not hide the rumble, and a presence setting adds low-band harmonics so sub-heavy sounds are still heard on a laptop."),
    ]),
]


def jsonld_faq() -> str:
    items = [{"@type": "Question", "name": qa[0], "acceptedAnswer": {"@type": "Answer", "text": qa[1].replace("`", "")}}
             for _, _, qas in FAQ for qa in qas]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}, ensure_ascii=False)


def _md_inline(text: str) -> str:
    """Backticks to <code>; everything else escaped."""
    parts = text.split("`")
    return "".join(esc(p) if i % 2 == 0 else f"<code>{esc(p)}</code>" for i, p in enumerate(parts))


def page_faq(lib: dict, base: str) -> str:
    groups = "".join(f"""
  <section id="{key}"><h2>{esc(title)}</h2>
  {''.join(f'<h3>{esc(qa[0])}</h3><p>{_md_inline(qa[1])}</p>' + (qa[2].replace('{base}', base) if len(qa) > 2 else '') for qa in qas)}
  </section>""" for title, key, qas in FAQ)
    body = f"""
<main class="doc">
  <h1>Questions and answers</h1>
  <p class="lede">Free sound effects made by code, for games, videos, apps and AI-assisted development: what you may do with them, how they are made, and how to get the one you need.</p>
  {groups}
  <section><h2>Where next</h2>
  <ul>
    <li><a href="{base}library.html">The library</a>: {len(lib)} sounds to play, download and recreate.</li>
    <li><a href="{base}use.html">Use</a>: the install line, what to say, the tuning page, levels in a video.</li>
    <li><a href="{base}how-thunder-sounds.html">How thunder really sounds</a>: the measurements behind the nature sounds.</li>
    <li><a href="{base}how-it-works.html">How it works</a>: the blocks, four recipes explained, verification.</li>
  </ul>
  </section>
</main>"""
    sections = [(key, title) for title, key, _ in FAQ]
    return layout("FAQ · sfx-generator", body, "faq", base,
                  "Free sound effects for games, video and apps, made by code: licence, credit, formats, how to get a sound from Claude Code or Codex, how the sounds are made and measured.",
                  quiet=True, sections=sections, jsonld=jsonld_faq())


THUNDER_RECORDINGS = [
    ("a close, dry crack, 15 s", "192 Hz", "-9.1", "-6.2", "-2.2", "-8.4", "-17.6", "-31.6", "24.5 dB"),
    ("a close strike, about 1.6 km, 13 s", "273 Hz", "-12.4", "-10.7", "-2.4", "-5.1", "-14.8", "-38.5", "31.2 dB"),
    ("two big claps over a city, 95 s", "156 Hz", "-12.5", "-6.5", "-1.9", "-8.9", "-23.2", "-44.5", "29.6 dB"),
    ("mixed big, medium and distant, 150 s", "112 Hz", "-7.5", "-3.4", "-3.4", "-10.9", "-24.7", "-32.5", "28.0 dB"),
    ("distant thunder under rain, 17 s", "273 Hz", "-7.2", "-17.2", "-1.8", "-5.2", "-19.1", "-25.4", "24.9 dB"),
    ("ours, first version", "92 Hz", "-6.5", "-0.7", "-10.2", "-12.8", "-22.7", "-29.2", "17.2 dB"),
    ("ours, now", "230 Hz", "-6.5", "-4.7", "-3.6", "-6.9", "-17.7", "-23.5", "18.4 dB"),
]
RUMBLE_TEXTURE = [
    ("close, dry crack", "16.2", "12.7"), ("close strike, about 1.6 km", "23.5", "16.6"), ("two big claps over a city", "8.0", "9.8"),
    ("a big strike in a mixed recording", "45.1", "20.8"), ("rain at a window with wind", "1.2", "5.3"), ("our wind loop", "0.7", "4.2"),
    ("our thunder, first version (filtered noise)", "0.9", "4.1"), ("our thunder, now (arrivals), the roll", "16.7", "11.6"),
    ("our thunder, now, the rumble 5 s later", "7.0", "7.0"),
]


def jsonld_article(title: str, description: str, page: str) -> str:
    d = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": description,
         "url": f"{SITE_URL}{page}.html", "image": f"{SITE_URL}og.png", "datePublished": "2026-11-01", "dateModified": "2026-11-01",
         "inLanguage": "en", "author": {"@type": "Person", "name": "Vela", "url": f"https://github.com/{REPO.split('/')[0]}"},
         "publisher": {"@type": "Organization", "name": "sfx-generator", "url": SITE_URL},
         "about": ["thunder", "sound synthesis", "procedural audio", "sound design"], "license": "https://www.apache.org/licenses/LICENSE-2.0"}
    return json.dumps(d, ensure_ascii=False)


def page_thunder(lib: dict, cat: dict, waves: dict, base: str) -> str:
    def fig(sid, text):
        e = cat["sounds"][sid]
        return f"""
<div class="figure">
  <div class="row"><button class="pl" data-play="{sid}" aria-label="play {sid}">{PLAY_SVG}</button><b>{sid}</b><span class="mute">{e['seconds']} s · {e['loudness_lufs']} LUFS</span></div>
  {waves[sid]}
  <img src="{base}spec/{sid}.png" alt="spectrogram of {sid}: {esc(text[:90])}" width="480" height="160" loading="lazy">
  <div class="cap">{esc(text)}</div>
</div>"""
    rec_rows = "".join(f"<tr><td>{esc(r[0])}</td><td class=\"m\">{r[1]}</td><td class=\"m\">{r[2]}</td><td class=\"m\">{r[3]}</td><td class=\"m\"><b>{r[4]}</b></td><td class=\"m\">{r[5]}</td><td class=\"m\">{r[6]}</td><td class=\"m\">{r[7]}</td><td class=\"m\">{r[8]}</td></tr>" for r in THUNDER_RECORDINGS)
    tex_rows = "".join(f"<tr><td>{esc(a)}</td><td class=\"m\">{k}</td><td class=\"m\">{c}</td></tr>" for a, k, c in RUMBLE_TEXTURE)
    title = "How thunder really sounds, and how to synthesise it"
    description = ("Measurements of real thunder (where the weight sits, what makes a rumble a rumble, why a crack is a "
                   "build-up) and how the thunder in this library is built from them: arrivals, crackle, clusters, a swell.")
    body = f"""
<main class="doc">
  <h1>How thunder really sounds, and how to synthesise it</h1>
  <p class="lede">Thunder in this library is not a recording and not a boom. It is a cluster of strikes, each a crackle growing into a crack, each with a rumble made of thousands of small shock arrivals, placed on a slow swell of weight between 80 and 250 Hz. Every one of those choices came from measuring real strikes, because the words ("rumble", "boom", "crack") had led the first version somewhere else.</p>

  <section id="measure"><h2>What real thunder measures</h2>
  <p>Five free recordings of thunder, from a close dry crack to a distant roll under rain, were analysed with the same script as our own renders: the spectral centroid, the slope of the spectrum in dB per octave from 100 Hz to 8 kHz, how the energy divides between five bands (dB of the total), and the crest factor, peak over RMS. The recordings stay outside the repository; only the numbers are here.</p>
  <table class="tbl"><thead><tr><th>recording</th><th>centroid</th><th>slope dB/oct</th><th>sub &lt;80 Hz</th><th>80-250 Hz</th><th>250-1k</th><th>1-4 kHz</th><th>&gt;4 kHz</th><th>crest</th></tr></thead><tbody>{rec_rows}</tbody></table>
  <p>Three things are true of every recording and were false of our first attempt. <b>The weight of thunder is 80 to 250 Hz, not the sub.</b> That band carries most of the energy, about 2 dB under the total, and the band below 80 Hz sits 4 to 15 dB under it; our first version had the sub on top and 80 to 250 Hz ten decibels down, which is why it was felt on good speakers and vanished on small ones while real thunder is heard everywhere. <b>Real thunder is far more dynamic</b>, with crest factors of 24 to 31 dB against our 17. <b>The spectrum falls fast</b>, 9 to 12 dB per octave on close strikes; above 4 kHz a real strike is 30 to 45 dB down, so any hiss for "the air ripping" has to be short.</p>
  <p>Inside one close strike, measured in 50 ms steps: the crack lasts about 0.3 s, the level then drops 12 to 14 dB for a quarter of a second, a roll comes back to within 5 dB of the crack for half a second, and the rumble settles 12 to 18 dB under the crack, bumping irregularly by 5 to 8 dB for eight seconds or more, sometimes with a second peal four or five seconds later. The band shares barely change from crack to rumble: thunder does not get darker by losing its mids, it loses the hiss.</p>
  </section>

  <section id="rumble"><h2>Rumble is arrivals, not wind</h2>
  <p>The first rumble was what the word suggests: low-passed noise with slow swells. A listener called it wind, and the measurement agreed. In the 80 to 250 Hz band of a rumble, scipy's excess kurtosis (Gaussian noise scores 0) and the crest of the Hilbert envelope (peak over mean) separate the two cleanly:</p>
  <table class="tbl"><thead><tr><th>sound, 80-250 Hz band</th><th>kurtosis</th><th>envelope crest</th></tr></thead><tbody>{tex_rows}</tbody></table>
  <p>A real rumble is impulsive: a pile of small shock arrivals of random size, the sound channel's segments reaching the ear at slightly different times. Filtered noise with a slow modulation, whatever band it sits in, measures like wind and is heard as wind. So the rumble here is a Poisson train of short N-wave pulses, 3 to 14 ms long, random sign, lognormal amplitudes, at a rate that follows the shape of the roll; the pulse length sets the weight, there is no resonant filter (a resonator on an impulse is a drum), and the reverb is kept small, because a reverb tail is Gaussian and turns arrivals back into wind. The first pass at this scored kurtosis 3: too dense, so the pulses merged into noise again. Halving the rate and giving the sizes heavier tails brought it to 7 to 30, inside the recordings' range.</p>
  </section>

  <section id="crack"><h2>A crack is a build-up, not a hit</h2>
  <p>The first crack was a kick drum by construction: a sine sweeping from 95 to 28 Hz with a knock and a burst on top. Heard beside the recordings it was "a drum beat", and at 5 ms resolution the recordings explain why. No real crack has a tone at all (pitch strength 0.2 to 0.5, no downward glide), and none is instantaneous: every close strike builds over 100 to 300 ms as a ragged, growing crackle of many impulses that culminates in the peak, broadband and flat up to 4 kHz for the first 60 ms, with the weight at 80 to 250 Hz throughout. The crack here is therefore a thinning impulse train whose rate climbs from tens to hundreds a second and whose level rises as a power of time, ending in a 25 ms burst of forty to eighty arrivals and a short broadband snap, with no oscillator anywhere. A sine sweep is a drum wherever you put it; explosions and cannon in this library follow the same rule.</p>
  <p>The shipped preset goes one step further, at a listener's request: the crack is replaced by a rumble twice as loud and 60 % as long whose peak lands exactly where the crack was (the <code>clap</code> parameter blends between the two). The ear reads it as a nearer, heavier strike with nothing artificial on its front.</p>
  </section>

  <section id="clusters"><h2>Clusters, irregular gaps, a swell underneath</h2>
  <p>Man-made sounds repeat on a rhythm: gunfire, machines, a clock. Natural ones come in clusters with gaps that never match: thunder, rain, waves, fire. Four evenly spaced strikes were "good but still a sequence"; the fix was explicit structure. Strikes arrive in two or three clusters, each of two or three cracks 0.15 to 0.6 s apart, and the gaps between clusters are drawn from a skewed distribution so no two are alike. Every crack carries its own full rumble, because a pattern the ear must count needs every member at full weight; backoff and shortening belong to tails, not to the events themselves. Under all of it runs a surge: one slow rumble that starts during the distant approach, peaks just after the first strike and fades across the rest, so the strikes sit on one weather instead of on silence. Timing and content come from separate random streams, so changing the seed of what sounds at each moment does not move the moments.</p>
  </section>

  <section id="weight"><h2>The weight follows the situation</h2>
  <p>With every sound peak-normalised, a dense loop like rain is loud all the way through while thunder, one crack and a long quiet rumble, is loud for 100 ms and then sits under the bed. A listener heard the rain as louder than the storm. The answer is not gain but a master that lifts the loudest second of the sound to a target that depends on what the sound is for: thunder is fear and the open sky, so it is <code>huge</code> and its body is mastered to -12 LUFS with the limiter holding the crack above it; a slam or a shot is <code>big</code> at -14; interface sounds are left as rendered. In a mix a huge sound may also peak higher than an ordinary effect. And because a laptop speaker plays little under 250 Hz, a <code>presence</code> setting can add harmonics of the low band at 200 to 1200 Hz so the weight is heard there too.</p>
  </section>

  <section id="listen"><h2>What it looks like</h2>
  {fig("thunder", "The approach rumbles in from the left, then clusters of strikes, each with its own rumble, over one slow surge; the ink sits between 80 and 250 Hz throughout and the air above 4 kHz leaves after each strike.")}
  {fig("rain_loop", "Rain built the same way: a falling bed with its weight between 250 Hz and 4 kHz, a roof band at 160 Hz, and individual drop ticks standing 16 to 24 dB above it, as the recordings showed, instead of the rising hiss the word suggested.")}
  </section>

  <section id="make"><h2>Make your own</h2>
  <p>Everything above is a parameter. <code>sfx tune thunder</code> opens the tuning page with sliders for the approach length, the number of clusters and strikes per cluster, the rumble length, overlap, backoff and growth, the secondary peal, the surge, the tail and the seed; <code>clap</code> at 0 brings the crackle-crack back. <code>sfx render thunder clusters=1 per_cluster=1</code> is a single distant strike; <code>sfx render thunder seed=42</code> is the same storm on another night. The recipe is <code>recipes/nature.py</code> in the repository, Apache 2.0, and the measurements and scripts behind this page are in the skill's references.</p>
  {code_block("sfx tune thunder\nsfx render thunder clusters=2 per_cluster=3 surge=0.8 -o storm", "try it", True)}
  </section>
</main>"""
    sections = [("measure", "Measurements"), ("rumble", "Rumble"), ("crack", "Crack"), ("clusters", "Clusters"), ("weight", "Weight"), ("listen", "Listen"), ("make", "Make your own")]
    return layout(title + " · sfx-generator", body, "how-thunder-sounds", base, description, quiet=True, sections=sections,
                  jsonld=jsonld_article(title, description, "how-thunder-sounds"))


def page_licence(base: str) -> str:
    body = f"""
<main class="doc">
  <h1>Licence</h1>
  <p class="lede">Apache 2.0. The code, the presets and every sound they produce.</p>
  <section>
  <p>Copyright 2026 Vela.</p>
  <p>Licensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. The full text of the License is in the <code>LICENSE</code> file of the repository.</p>
  <p>Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.</p>
  </section>
  <section><h2>What that means for the sounds</h2>
  <ul>
    <li>Every sound on this site is synthesised by the code in the repository. Nothing is recorded or downloaded.</li>
    <li>You may use the sounds commercially, in videos, apps, games and products, with no credit required.</li>
    <li>You may change the recipes and ship the results under any licence you like; the licence notice travels with the code you redistribute, and the sounds you generate are yours.</li>
    <li>The narration line used by "over narration" is a synthesised voice made for this demo only; it is not part of the library.</li>
  </ul>
  </section>
</main>"""
    return layout("Licence · sfx-generator", body, "licence", base, quiet=True, description="Apache 2.0: the code, the presets and every sound they produce. Free to use anywhere; you own what you generate.")


def llms_txt(lib: dict, cat: dict) -> str:
    lines = [f"# sfx-generator v{__version__}", "",
             "> Sound effects made in code: deterministic numpy recipes with a parameter schema each, a CLI (sfx), a local "
             "tuning page, and a Claude Code skill that turns a short description into a finished sound. Apache 2.0; you own what you generate.",
             "", f"Repository: {REPO_URL}", "Install: paste \"Install the sound effects skill from " + REPO_URL + ": fetch and follow its INSTALL.md\" into Claude Code or Codex; developers: uv tool install \"sfx-generator[ffmpeg] @ git+" + REPO_URL + "\"", "",
             "## Sounds (id: family, category, seconds, level LU vs narration, lead s; use)"]
    for sid, pr in lib.items():
        e = cat["sounds"][sid]
        lines.append(f"- {sid}: {pr.family}, {pr.category}, {e['seconds']} s, {e['level_lu']:+d} LU, lead {pr.lead}; {pr.use}")
    lines += ["", "## Pages", f"- {SITE_URL}library.html: every sound, play, download, numbers, recipe",
              f"- {SITE_URL}use.html: install, what to say, the tuning page, levels in a video",
              f"- {SITE_URL}how-thunder-sounds.html: measurements of real thunder and how the recipe is built from them",
              f"- {SITE_URL}faq.html: licence, credit, formats, how the sounds are made and measured",
              "", "## FAQ", *[f"- Q: {qa[0]}\n  A: {qa[1]}" for _, _, qas in FAQ for qa in qas]]
    lines += ["", "## Recipes", *[f"- {rid}: {rec.doc}" for rid, rec in schema.all_recipes().items()],
              "", "## Rules", "- loudness = loudest 100 ms, K-weighted; narration about -14 LUFS; level by category; "
              "gain = min(ref + level - loudness, -6 dBFS - peak)", "- a sound starts `lead` s before its cue; "
              "anticipation sounds end on it", "- at most ~8 sounds a minute, 1 s apart; every cue has a reason"]
    return "\n".join(lines) + "\n"


README_TXT = """sfx-generator sounds
=====================

Every file here was synthesised by code (https://github.com/{repo}). They are free to use anywhere, in anything,
and whoever generates them owns the result. Apache 2.0.

Folders: wav (24-bit, 48 kHz, stereo), ogg (Vorbis q6), mp3 (160 kb/s), presets (the JSON that recreates each
sound with `sfx render <preset.json>`). catalog.json lists every sound's category, use, lead before its cue, level
against narration, length, loudness and peak.
"""


def build_zips(out: Path, lib: dict, cat: dict) -> dict:
    """downloads/sfx-<family>.zip and sfx-all.zip: wav, ogg, mp3, presets, catalog and a README. Returns sizes."""
    import zipfile
    ddir = out / "downloads"
    ddir.mkdir(exist_ok=True)
    groups = {fam: [sid for sid, p in lib.items() if p.family == fam] for fam in FAMILY_ORDER}
    groups["all"] = list(lib)
    sizes = {}
    for name, ids in groups.items():
        path = ddir / f"sfx-{name}.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("README.txt", README_TXT.format(repo=REPO))
            z.writestr("catalog.json", json.dumps({**cat, "sounds": {k: cat["sounds"][k] for k in ids}}, indent=1))
            for sid in ids:
                for fmt in ("wav", "ogg", "mp3"):
                    z.write(out / "sounds" / fmt / f"{sid}.{fmt}", f"{fmt}/{sid}.{fmt}")
                z.write(out / "presets" / f"{sid}.json", f"presets/{sid}.json")
        mb = path.stat().st_size / 1e6
        sizes[name] = f"{mb:.0f} MB" if mb >= 1 else f"{path.stat().st_size / 1e3:.0f} KB"
    return sizes


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0a0a0a"/>'
           '<path d="M6 17c2-6 4-6 6 0s4 6 6 0 4-6 6 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>')


def build_site(out: Path, base_url: str = "./", verbose=True) -> Path:
    out = Path(out)
    if out.exists():                      # clear the contents, keep the directory (a server may hold it open)
        for child in out.iterdir():
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    out.mkdir(parents=True, exist_ok=True)
    lib = presets.load_all()
    lib = {k: lib[k] for k in sorted(lib)}
    base = base_url if base_url.endswith("/") else base_url + "/"
    # sounds: each preset rendered once, then encoded, measured, drawn
    arrays = {sid: pr.render() for sid, pr in lib.items()}
    cat = render.render_presets(lib, out / "sounds", formats=("wav", "ogg", "mp3"), verbose=False, arrays=arrays)
    waves = {}
    for sid, pr in lib.items():
        x = arrays[sid]
        # 24-bit WAV for downloads (smaller than float masters, what editors expect)
        render.write_wav(x, out / "sounds" / "wav" / f"{sid}.wav", subtype="PCM_24")
        insp.spectrogram_png(x, out / "spec" / f"{sid}.png")
        waves[sid] = insp.waveform_svg(x, 480, 44, 160).replace("<svg ", '<svg class="wave" ')
        (out / "presets").mkdir(exist_ok=True)
        shutil.copy(presets.PRESET_DIR / f"{sid}.json", out / "presets" / f"{sid}.json")
        if verbose:
            print(f"  {sid}")
    (out / "sounds" / "catalog.json").write_text(json.dumps(cat, indent=1) + "\n", encoding="utf-8")
    # narration
    voice = None
    clip = HERE / "narration.mp3"
    if clip.exists():
        shutil.copy(clip, out / "sounds" / "narration.mp3")
        voice = {"file": "sounds/narration.mp3", "cue": 3.3}
    data = {"base": base, "voice": voice,
            "sounds": {sid: {"mp3": f"sounds/mp3/{sid}.mp3", "gain_db": cat["sounds"][sid]["gain_db"],
                             "lead": pr.lead, "loop": pr.loop, "family": pr.family, "category": pr.category,
                             "mood": pr.mood}
                       for sid, pr in lib.items()}}
    (out / "library.js").write_text("window.SFX_LIBRARY=" + json.dumps(data) + ";\n", encoding="utf-8")
    zips = build_zips(out, lib, cat)
    (out / "library.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    # static
    shutil.copy(HERE / "style.css", out / "style.css")
    shutil.copy(HERE / "app.js", out / "app.js")
    shutil.copy(HERE / "bg.js", out / "bg.js")
    shutil.copy(HERE / "tune.png", out / "tune.png")
    (out / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    # pages
    (out / "index.html").write_text(page_index(lib, cat, base), encoding="utf-8")
    (out / "library.html").write_text(page_library(lib, cat, waves, base, zips), encoding="utf-8")
    (out / "use.html").write_text(page_use(lib, base), encoding="utf-8")
    (out / "how-it-works.html").write_text(page_how(lib, cat, waves, base), encoding="utf-8")
    (out / "licence.html").write_text(page_licence(base), encoding="utf-8")
    (out / "faq.html").write_text(page_faq(lib, base), encoding="utf-8")
    (out / "how-thunder-sounds.html").write_text(page_thunder(lib, cat, waves, base), encoding="utf-8")
    (out / "llms.txt").write_text(llms_txt(lib, cat), encoding="utf-8")
    # search and sharing: sitemap, robots, a 404 page, and a social card image (the thunder spectrogram)
    (out / "404.html").write_text(page_404(lib), encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap_xml(), encoding="utf-8")
    (out / "robots.txt").write_text(robots_txt(), encoding="utf-8")
    og = "thunder" if "thunder" in arrays else next(iter(arrays))
    insp.spectrogram_png(arrays[og], out / "og.png", width=1200, height=630)
    return out


def check_links(out: Path) -> list[str]:
    """Every local href/src in the built pages points at a file that exists."""
    import re
    missing = []
    for page in out.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        for m in re.finditer(r'(?:href|src|data-src)="([^"#]+)"', text):
            url = m.group(1)
            if url.startswith(("http:", "https:", "mailto:")):
                continue
            target = (page.parent / url.split("?")[0]).resolve()
            if not target.exists():
                missing.append(f"{page.name}: {url}")
    return missing
