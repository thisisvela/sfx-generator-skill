"""The make loop and the site builder."""
import json
from pathlib import Path

import numpy as np
import pytest

from sfx_generator import render
from sfx_generator.make import apply_description, match_presets, make, parse_duration
from sfx_generator.schema import get


def test_match_presets_maps_words():
    assert match_presets("make a quick whoosh for a slide")[0][0] in ("whoosh", "whoosh_short")
    assert match_presets("a soft error sound")[0][0] == "error"
    assert match_presets("two-note success chime")[0][0] in ("success", "ding", "notify")
    assert match_presets("a low hum under the whole scene")[0][0] == "hum_loop"
    assert match_presets("camera shutter click")[0][0] == "camera_shutter"


def test_parse_duration():
    assert parse_duration("about half a second") == 0.5
    assert parse_duration("300 ms long") == 0.3
    assert parse_duration("two seconds") == 2
    assert parse_duration("no length here") is None


def test_adjectives_move_parameters_within_range():
    rec = get("whoosh")
    params, notes = apply_description(rec, rec.defaults(), "a quick, dark, wide whoosh")
    assert params["d"] < rec.defaults()["d"]
    assert params["f_peak"] < rec.defaults()["f_peak"]
    rec.validate(params)
    assert notes


@pytest.mark.skipif(render.ffmpeg_exe() is None, reason="ffmpeg not available")
def test_make_is_deterministic_and_complete(tmp_path):
    a = make("a soft error sound", tmp_path / "a", n=3, verbose=False)
    b = make("a soft error sound", tmp_path / "b", n=3, verbose=False)
    assert [v.params for v in a.variants] == [v.params for v in b.variants]
    assert len(a.variants) == 3
    assert (tmp_path / "a" / "audition.html").exists()
    entries = [json.loads(l) for l in (tmp_path / "a" / "journal.jsonl").read_text().splitlines()]
    assert entries[0]["base"] == "error" and len(entries[0]["variants"]) == 3
    for v in a.variants:
        assert (tmp_path / "a" / f"error_{v.name}.json").exists()
        assert (tmp_path / "a" / f"error_{v.name}.ogg").exists()
        assert v.report["peak_dbfs"] == pytest.approx(-1.5, abs=0.1)
    # variants differ from each other
    assert not np.array_equal(a.variants[0].x, a.variants[2].x)


def test_make_without_ffmpeg_writes_wav(tmp_path):
    run = make("a tick", tmp_path, n=3, formats=("wav",), verbose=False)
    assert run.base.id == "tick"
    assert (tmp_path / "tick_a.wav").exists()


@pytest.mark.skipif(render.ffmpeg_exe() is None, reason="ffmpeg not available")
def test_site_builds_and_links_resolve(tmp_path):
    from sfx_generator.site.build import build_site, check_links
    out = build_site(tmp_path / "site", verbose=False)
    assert check_links(out) == []
    for page in ("index", "library", "use", "how-it-works", "how-thunder-sounds", "faq", "licence"):
        assert (out / f"{page}.html").exists()
    lib = json.loads((out / "library.json").read_text())
    for sid, s in lib["sounds"].items():
        assert (out / s["mp3"]).exists(), sid
        assert (out / "spec" / f"{sid}.png").exists()
    assert (out / "llms.txt").exists()
    for f in ("sitemap.xml", "robots.txt", "404.html", "og.png", "tune.png"):
        assert (out / f).exists(), f
    index = (out / "index.html").read_text(encoding="utf-8")
    assert '<link rel="canonical"' in index and 'property="og:image"' in index
    assert '"@type": "SoftwareApplication"' in index
    library = (out / "library.html").read_text(encoding="utf-8")
    assert library.count('"@type": "AudioObject"') == len(lib["sounds"])
    sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
    assert sitemap.count("<loc>") == 7
    faq = (out / "faq.html").read_text(encoding="utf-8")
    assert '"@type": "FAQPage"' in faq and faq.count('"@type": "Question"') >= 15
    article = (out / "how-thunder-sounds.html").read_text(encoding="utf-8")
    assert '"@type": "Article"' in article and 'data-play="thunder"' in article
    assert "## FAQ" in (out / "llms.txt").read_text(encoding="utf-8")
