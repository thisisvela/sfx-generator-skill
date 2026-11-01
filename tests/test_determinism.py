"""Determinism: every preset renders to exactly the same samples, run after run, and the 37 reference presets match
the sounds shipped before this package existed.

The float32 hashes below were taken when the port was verified sample for sample against the original generator.
If a hash changes, a recipe's numbers changed: either revert, or (if the change is intended and approved by ear)
update the hash and say so in the commit. The OGG comparison is encoder-tolerant, since libvorbis builds differ.
"""
from pathlib import Path

import numpy as np
import pytest

from sfx_generator import presets, render

HASHES = {
    'bong': 'a00f22c9cada39db', 'click': '41e39333576a731a', 'click_soft': '28f3728c9d6ed5dd',
    'ding': '91cd3c0e1c12e2f3', 'end_chime': '75a84aa145ac8dc8', 'error': '7f1a815bc25e844e',
    'glitch': '839e4a959db29375', 'glitch_burst': '8f58394d50d82c43', 'impact_deep': '033ba19ce6baac35',
    'impact_soft': 'a1704b9469a5d25b', 'ping': 'fea561dcc62467d7', 'ping_long': '598f7e6352aa4814',
    'ping_soft': '2f782703cdb936d3', 'pluck': '1eb1200697b51503', 'pop': 'b050c887d63def8e',
    'pop_low': 'c463e90ec0782c01', 'pop_up': 'ec4ecf11361adc23', 'question': '7b8931d4c7563034',
    'question_alt': '1e7f4190fb84e4c5', 'riser': '55fcc5087bebfdc6', 'shimmer': 'df349c30d1bd52cb',
    'success': 'f6e536e8476aa2fc', 'success_short': 'f99cc05159d5f27c', 'swell': 'c6f587970fa0c669',
    'swell_down': '423a40121f64d5ff', 'swell_up': 'acc5ae8fa62bf6dc', 'switch': '13789edfdd4e873a',
    'swoosh_up': '1ed785ab6bcc4fea', 'tick': 'a0babcfead242966', 'tick_double': '5a3b0dc61a577585',
    'title_hit': 'a68d5cf0da9b193e', 'toggle': '35063d61b7fb485c', 'whoosh': '700e3985e0f974e2',
    'whoosh_long': 'ccc185f421cf7225', 'whoosh_short': 'cdff52b7f7bb3647', 'whoosh_soft': '4382a79beac8c56a',
    'whoosh_up': 'd24c6fdf3f55f25f',
}

ALL = presets.load_all()
REF_DIR = Path(__file__).resolve().parent / "reference"


@pytest.mark.parametrize("sid", sorted(HASHES))
def test_reference_hash(sid):
    assert render.array_hash(ALL[sid].render()) == HASHES[sid]


@pytest.mark.parametrize("sid", sorted(ALL))
def test_renders_identically_twice(sid):
    a, b = ALL[sid].render(), ALL[sid].render()
    assert a.shape == b.shape and np.array_equal(a, b)


@pytest.mark.skipif(render.ffmpeg_exe() is None, reason="ffmpeg not available")
@pytest.mark.parametrize("sid", sorted(HASHES))
def test_matches_reference_ogg(sid, tmp_path):
    """Encoder-tolerant: same length, and within 0.1 of the decoded reference (encoders differ by up to ~0.05)."""
    x = ALL[sid].render()
    files = render.export(x, tmp_path / sid, formats=("wav", "ogg"))
    y = render.decode(files["ogg"])
    r = render.decode(REF_DIR / f"{sid}.ogg")
    assert len(y) == len(r)
    assert float(np.abs(y - r).max()) < 0.1
