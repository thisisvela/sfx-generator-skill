"""Keys and locks: keystrokes, typing, a camera shutter, an unlock."""
import numpy as np

from ..blocks import _rng, _tr, burst, env, finish, highpass, osc, pan, place, release, room, svf_bandpass, tone, white
from ..schema import I, P, SEED, recipe
from .clicks import click_core


def key_core(rng, bright=2400, thock=1100, d=0.045):
    """One key: a plastic click with a short low 'thock' under it."""
    t = _tr(d)
    x = click_core(rng, bright=bright, thump=190, d=d, t_body=0.006)
    x += 0.8 * osc(thock, t) * env(t, 0.0004, 0.006)
    return x


@recipe("keystroke", family="keys",
        doc="One key press: a plastic click with a short low thock under it.",
        tips="bright is the click's band (higher = thinner keycap); thock the body pitch (lower = heavier key).",
        params=[
            P("bright", 2400, 500, 8000, 10, "Hz", "click band centre"),
            P("thock", 1100, 200, 4000, 1, "Hz", "body pitch"),
            P("d", 0.045, 0.02, 0.2, 0.001, "s", "length"),
            SEED(211),
        ])
def keystroke(*, bright, thock, d, seed):
    rng = _rng(seed)
    return finish(pan(key_core(rng, bright, thock, d), 0.0), tail=False, fade_out=0.006)


@recipe("typing", family="keys",
        doc="A seeded burst of keystrokes with varied pitch, loudness and gaps: someone typing.",
        tips="count is the number of keys; gap_lo/gap_hi the range between them (narrower = a machine, wider = a "
             "person); the seed picks the rhythm and the pitches; width spreads the keys across the field.",
        params=[
            I("count", 10, 2, 40, "", "number of keystrokes"),
            P("gap_lo", 0.06, 0.02, 0.5, 0.005, "s", "shortest gap"),
            P("gap_hi", 0.13, 0.03, 1.0, 0.005, "s", "longest gap"),
            P("width", 0.3, 0, 1, 0.05, "", "stereo spread"),
            SEED(212),
        ])
def typing(*, count, gap_lo, gap_hi, width, seed):
    rng = _rng(seed)
    parts, t0 = [], 0.0
    for _ in range(count):
        k = key_core(rng, rng.uniform(2000, 3200), rng.uniform(900, 1400)) * rng.uniform(0.55, 1.0)
        parts.append((t0, pan(k, rng.uniform(-width, width))))
        t0 += rng.uniform(gap_lo, max(gap_lo, gap_hi))
    st = place(parts, t0 + 0.06)
    return finish(highpass(st, 90, 2), tail=False, fade_out=0.01)


@recipe("camera_shutter", family="keys",
        doc="Two clicks a few tens of ms apart with a short noise swish between: a snapshot.",
        tips="gap is the time between the two clicks; swish the noise amount between them; bright the clicks' band.",
        params=[
            P("gap", 0.06, 0.02, 0.3, 0.005, "s", "time between the clicks"),
            P("swish", 0.5, 0, 1.5, 0.01, "", "swish amount"),
            P("bright", 3200, 500, 8000, 10, "Hz", "click band centre"),
            SEED(213),
        ])
def camera_shutter(*, gap, swish, bright, seed):
    rng = _rng(seed)
    t = _tr(gap)
    n = len(t)
    sw = svf_bandpass(white(n, rng), np.linspace(2500, 1200, n), 1.0) * np.sin(np.pi * np.linspace(0, 1, n)) * swish
    st = place([(0.0, click_core(rng, bright, 170, d=0.03)), (0.004, sw),
                (gap, click_core(rng, bright * 0.8, 150, d=0.035) * 0.9)], gap + 0.06)
    return finish(highpass(room(st, wet=0.05), 90, 2), tail=False, fade_out=0.008)


@recipe("unlock", family="keys",
        doc="Mechanical lock clicks: a click, a lower clack and a short spring ring; something opens.",
        tips="gap is the time between click and clack; ring the spring's amount and ring_hz its pitch.",
        params=[
            P("gap", 0.09, 0.03, 0.4, 0.005, "s", "time between click and clack"),
            P("ring", 0.35, 0, 1.5, 0.01, "", "spring ring amount"),
            P("ring_hz", 2900, 500, 8000, 10, "Hz", "spring pitch"),
            SEED(214),
        ])
def unlock(*, gap, ring, ring_hz, seed):
    rng = _rng(seed)
    t = _tr(0.14)
    spring = tone(ring_hz, t, [(1, 1.0, 0.03), (1.9, 0.4, 0.015), (3.3, 0.15, 0.008)], attack=0.0005) * ring
    st = place([(0.0, click_core(rng, 2800, 200, d=0.03)),
                (gap, click_core(rng, 1900, 150, d=0.04) * 1.1),
                (gap + 0.01, spring)], gap + 0.18)
    return finish(highpass(room(st, wet=0.06), 90, 2))
