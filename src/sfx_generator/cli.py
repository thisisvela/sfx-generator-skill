"""The `sfx` command line.

  sfx list [--family F] [--category C] [--json]        the library
  sfx schema <recipe> [--json]                           a recipe's parameters
  sfx render <recipe|preset> [k=v ...] -o <stem>         render one sound to WAV, OGG and MP3
  sfx render-all [-o out] [--formats wav,ogg,mp3]        render the whole library and its catalog
  sfx make "<description>" [-o out] [-n 4] [--base id]   description -> variants + audition page + journal
  sfx inspect <file|preset> [--category C] [--png P]     numbers, warnings, spectrogram
  sfx tune <preset|recipe> [--port 8765]                 the local tuning page
  sfx site [-o site]                                     build the static demo site
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import webbrowser
from pathlib import Path

from . import __version__


def _kv(pairs: list[str]) -> dict:
    out = {}
    for p in pairs:
        if "=" not in p:
            raise SystemExit(f"expected name=value, got {p!r}")
        k, v = p.split("=", 1)
        try:
            out[k] = json.loads(v)
        except json.JSONDecodeError:
            out[k] = v
    return out


def cmd_list(a):
    from . import presets
    lib = presets.load_all()
    rows = [p for p in lib.values() if (not a.family or p.family == a.family) and (not a.category or p.category == a.category)]
    if a.json:
        print(json.dumps([p.to_dict() for p in rows], indent=1))
        return
    for p in rows:
        print(f"{p.id:16} {p.family:9} {p.category:12} lead {p.lead:<5} {p.level_lu:>3} LU  {p.use}")
    print(f"{len(rows)} sounds")


def cmd_schema(a):
    from . import schema
    rec = schema.get(a.recipe)
    if a.json:
        print(json.dumps(rec.schema(), indent=1))
        return
    print(f"{rec.id} ({rec.family}): {rec.doc}\n")
    for p in rec.params:
        rng = f"{p.min}..{p.max} step {p.step}" if p.kind in ("float", "int") else p.kind
        print(f"  {p.name:12} {str(p.default):>10} {p.unit:3} {rng:28} {p.doc}")
    if rec.tips:
        print(f"\n{rec.tips}")


def cmd_render(a):
    from . import inspect as insp
    from . import presets, render, schema
    over = _kv(a.params)
    try:
        pr = presets.find(a.what)
        rec = schema.get(pr.recipe)
        params = dict(pr.params, **over)
        category = a.category or pr.category
        stem = a.out or pr.id
    except KeyError:
        rec = schema.get(a.what)
        params = rec.validate(over)
        category = a.category
        stem = a.out or rec.id
    x = rec.render(params)
    formats = tuple(a.formats.split(","))
    files = render.export(x, Path(stem), formats)
    rep = insp.report(x, category)
    print(insp.format_report(rep))
    print("wrote " + ", ".join(str(p) for p in files.values()))
    if a.preset:
        presets.Preset(id=Path(stem).name, recipe=rec.id, params=rec.validate(params), category=category or "emphasis",
                       use=a.use or "", what=rec.doc).save(Path(stem).with_suffix(".json"))
        print(f"preset: {Path(stem).with_suffix('.json')}")


def cmd_render_all(a):
    from . import presets, render
    lib = presets.load_all()
    if a.ids:
        lib = {k: v for k, v in lib.items() if k in set(a.ids)}
    out = Path(a.out)
    render.render_presets(lib, out, tuple(a.formats.split(",")))
    print(f"{len(lib)} sounds -> {out}")


def cmd_make(a):
    from .make import make
    out = Path(a.out) if a.out else Path("out") / "_".join(w for w in "".join(c if c.isalnum() else " " for c in a.description.lower()).split()[:4])
    run = make(a.description, out, n=a.n, base_id=a.base, category=a.category, seed=a.seed,
               formats=tuple(a.formats.split(",")))
    print(f"nearest presets: {', '.join(f'{k} ({s:.1f})' for k, s in run.candidates)}")
    if a.open:
        webbrowser.open(run.audition.resolve().as_uri())


def cmd_inspect(a):
    from . import inspect as insp
    from . import presets, render
    p = Path(a.what)
    if p.exists():
        x = render.decode(p) if p.suffix != ".json" else presets.Preset.load(p).render()
        category = a.category
    else:
        pr = presets.find(a.what)
        x, category = pr.render(), a.category or pr.category
    rep = insp.report(x, category)
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        print(insp.format_report(rep))
    if a.png:
        insp.spectrogram_png(x, a.png)
        print("spectrogram ->", a.png)
    if a.svg:
        Path(a.svg).write_text(insp.waveform_svg(x), encoding="utf-8")
        print("waveform ->", a.svg)


def cmd_tune(a):
    from .tune.server import serve
    serve(a.what, port=a.port, open_browser=not a.no_open)


def cmd_site(a):
    from .site.build import build_site
    out = build_site(Path(a.out), base_url=a.base_url)
    print(f"site -> {out}")
    if a.open:
        webbrowser.open((out / "index.html").resolve().as_uri())


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sfx", description="Sound effects made in code.")
    ap.add_argument("--version", action="version", version=f"sfx-generator {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="list the library")
    s.add_argument("--family"); s.add_argument("--category"); s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("schema", help="a recipe's parameters")
    s.add_argument("recipe"); s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_schema)

    s = sub.add_parser("render", help="render one sound")
    s.add_argument("what", help="a preset id, a preset .json, or a recipe id")
    s.add_argument("params", nargs="*", help="name=value overrides")
    s.add_argument("-o", "--out", help="output stem (no extension)")
    s.add_argument("--formats", default="wav,ogg,mp3")
    s.add_argument("--category", help="level category for the in-mix report")
    s.add_argument("--preset", action="store_true", help="also write <stem>.json as a preset")
    s.add_argument("--use", help="one line: when to use it (with --preset)")
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("render-all", help="render the whole library and its catalog")
    s.add_argument("ids", nargs="*"); s.add_argument("-o", "--out", default="out/library")
    s.add_argument("--formats", default="wav,ogg,mp3")
    s.set_defaults(fn=cmd_render_all)

    s = sub.add_parser("make", help="description -> variants, audition page, journal")
    s.add_argument("description"); s.add_argument("-o", "--out")
    s.add_argument("-n", type=int, default=4, help="variants (3-6)")
    s.add_argument("--base", help="start from this preset instead of the best match")
    s.add_argument("--category"); s.add_argument("--seed", type=int, default=0)
    s.add_argument("--formats", default="wav,ogg,mp3")
    s.add_argument("--open", action="store_true", help="open the audition page")
    s.set_defaults(fn=cmd_make)

    s = sub.add_parser("inspect", help="numbers, warnings, pictures")
    s.add_argument("what", help="a sound file, a preset .json, or a preset id")
    s.add_argument("--category"); s.add_argument("--png"); s.add_argument("--svg")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_inspect)

    s = sub.add_parser("tune", help="the local tuning page")
    s.add_argument("what", help="a preset id, a preset .json, or a recipe id")
    s.add_argument("--port", type=int, default=8765); s.add_argument("--no-open", action="store_true")
    s.set_defaults(fn=cmd_tune)

    s = sub.add_parser("site", help="build the static demo site")
    s.add_argument("-o", "--out", default="site"); s.add_argument("--base-url", default="./")
    s.add_argument("--open", action="store_true")
    s.set_defaults(fn=cmd_site)

    a = ap.parse_args(argv)
    try:
        a.fn(a)
    except subprocess.CalledProcessError as e:
        print(f"error: {Path(str(e.cmd[0])).name} failed with exit code {e.returncode}", file=sys.stderr)
        return 1
    except (KeyError, ValueError, RuntimeError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
