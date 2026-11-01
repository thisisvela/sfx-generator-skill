"""Quality, for every preset: peak -1.5 dBFS, a silent end, no DC, no NaN, a sane length, and loop seams that
do not click. Levels: every category lands where the level table says, with 'capped' reported."""
import numpy as np
import pytest

from sfx_generator import inspect as insp
from sfx_generator import levels, presets, schema
from sfx_generator.blocks import SR

ALL = presets.load_all()


@pytest.fixture(scope="module")
def rendered():
    return {sid: pr.render() for sid, pr in ALL.items()}


def test_library_size():
    assert 90 <= len(ALL) <= 120


@pytest.mark.parametrize("sid", sorted(ALL))
def test_sound_quality(sid, rendered):
    pr, x = ALL[sid], rendered[sid]
    d = insp.describe(x)
    assert not d["nan"]
    assert x.ndim == 2 and x.shape[1] == 2
    assert abs(d["peak_dbfs"] + 1.5) <= 0.1, d
    if d["seconds"] > 0.15:
        assert abs(d["dc_offset"]) < 0.002, d
    if not pr.loop and pr.category != "anticipation":        # anticipation sounds end ON the cue by design
        assert d["end_level_db"] < -40, d
    if pr.loop:
        step = np.abs(np.diff(x, axis=0)).max()               # the wrap must be no bigger than any step inside
        assert np.abs(x[0] - x[-1]).max() <= step * 1.5, "loop seam clicks"
    rec = schema.get(pr.recipe)
    if "d" in rec.by_name:                                    # length within the schema's idea of the length
        assert d["seconds"] <= rec.by_name["d"].max + 4.0


@pytest.mark.parametrize("sid", sorted(ALL))
def test_level_placement(sid, rendered):
    pr, x = ALL[sid], rendered[sid]
    pl = levels.placement(x, pr.category, level_lu=pr.level_lu, mood=pr.mood)
    level = pr.level_lu
    if pl["capped"]:
        assert pl["in_mix_lu"] < level
        assert pl["in_mix_lu"] > level - 12, "capped so hard it is inaudible: give it tonal body"
    else:
        assert abs(pl["in_mix_lu"] - level) < 0.05
    g = 10 ** (pl["gain_db"] / 20)
    assert levels.peak_dbfs(x * g) <= levels.PEAK_CAP_BY_MOOD[pr.mood] + 1e-6


def test_anticipation_lead_is_length(rendered):
    for sid, pr in ALL.items():
        if pr.category == "anticipation":
            assert abs(pr.lead - len(rendered[sid]) / SR) < 0.25, sid


def test_mood_masters_the_body(rendered):
    for sid, pr in ALL.items():
        assert pr.mood in levels.MOODS, sid
        target = levels.MOODS[pr.mood]
        if target is not None:                                # the loudest second reaches the mood's body
            assert levels.body_lufs(rendered[sid]) >= target - 1.0, sid
    x = ALL["thunder"].render()
    raw = schema.get("thunder").render(ALL["thunder"].params)
    assert levels.body_lufs(x) >= levels.body_lufs(raw) - 1e-6  # the master never lowers the body


def test_transition_defaults_exist():
    for style, sid in levels.TRANSITION_SFX.items():
        assert sid is None or sid in ALL, style
