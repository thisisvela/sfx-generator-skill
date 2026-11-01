"""Pings and bongs: inharmonic partial stacks (glass, marimba) that die quickly, in a small room."""
import numpy as np

from ..blocks import _rng, _tr, burst, finish, pan, room, tone
from ..schema import P, SEED, recipe


@recipe("ping", family="pings",
        doc="A small glass ping: inharmonic partials (1 : 2.32 : 4.25) that die quickly, in a small room.",
        tips="f0 is the pitch; decay scales how long it rings; strike the noise transient's amount; wet the room. "
             "The partial ratios are glass; change them in the code for a different material.",
        params=[
            P("f0", 2015, 300, 8000, 1, "Hz", "pitch"),
            P("decay", 1.0, 0.3, 4.0, 0.05, "", "ring length multiplier"),
            P("strike", 0.12, 0, 1, 0.01, "", "strike noise amount"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.25, 0.1, 1.5, 0.005, "s", "length"),
            SEED(107),
        ])
def ping(*, f0, decay, strike, wet, d, seed):
    rng = _rng(seed)
    t = _tr(d)
    x = tone(f0, t, [(1, 1.0, 0.04 * decay), (2.32, 0.28, 0.02 * decay), (4.25, 0.08, 0.01 * decay)], attack=0.0008)
    c = np.zeros_like(t)
    b = burst(0.005, rng, lo=4000, tau=0.0008) * strike
    c[: len(b)] = b
    return finish(room(pan(x + c, 0.0), wet=wet))


@recipe("ping_soft", family="pings",
        doc="A lighter ping, lower, with a softer strike.",
        tips="f0 the pitch; attack softens the onset (longer = gentler); decay the ring; wet the room.",
        params=[
            P("f0", 1453, 300, 8000, 1, "Hz", "pitch"),
            P("attack", 0.003, 0.0005, 0.05, 0.0005, "s", "attack time"),
            P("decay", 1.0, 0.3, 4.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.25, 0.1, 1.5, 0.005, "s", "length"),
            SEED(108),
        ])
def ping_soft(*, f0, attack, decay, wet, d, seed):
    t = _tr(d)
    x = tone(f0, t, [(1, 1.0, 0.035 * decay), (1.68, 0.3, 0.02 * decay), (3.1, 0.06, 0.01 * decay)], attack=attack)
    return finish(room(pan(x, 0.0), wet=wet))


@recipe("ping_long", family="pings",
        doc="A ping that rings, with a slow beat between two close partials: a highlight while the eye moves.",
        tips="f0 the pitch; beat the ratio of the second partial (1.003 = a slow beat, 1.01 = faster); decay the "
             "ring; keep it under about 0.6 s where speech follows.",
        params=[
            P("f0", 1921, 300, 8000, 1, "Hz", "pitch"),
            P("beat", 1.003, 1.0, 1.03, 0.0005, "", "second partial ratio"),
            P("decay", 1.0, 0.3, 4.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.15, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.55, 0.1, 3.0, 0.005, "s", "length"),
            SEED(109),
        ])
def ping_long(*, f0, beat, decay, wet, d, seed):
    t = _tr(d)
    x = tone(f0, t, [(1, 1.0, 0.12 * decay), (beat, 0.5, 0.12 * decay), (2.41, 0.2, 0.05 * decay), (4.6, 0.05, 0.02 * decay)],
             attack=0.0008)
    return finish(room(pan(x, 0.0), wet=wet, seconds=0.6))


@recipe("bong", family="pings",
        doc="A low, firm wooden bong: a marimba-like bar (partials near 1 : 3.9 : 9.2) and a mallet knock.",
        tips="f0 the pitch (233 Hz = a low accent); decay the ring; knock the mallet's amount; wet the room.",
        params=[
            P("f0", 233, 60, 1500, 1, "Hz", "pitch"),
            P("decay", 1.0, 0.3, 4.0, 0.05, "", "ring length multiplier"),
            P("knock", 0.3, 0, 1, 0.01, "", "mallet knock amount"),
            P("wet", 0.06, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.3, 0.1, 2.0, 0.005, "s", "length"),
            SEED(110),
        ])
def bong(*, f0, decay, knock, wet, d, seed):
    rng = _rng(seed)
    t = _tr(d)
    x = tone(f0, t, [(1, 1.0, 0.07 * decay), (3.93, 0.35, 0.025 * decay), (9.2, 0.08, 0.008 * decay)], attack=0.0015)
    c = np.zeros_like(t)
    b = burst(0.012, rng, lo=300, hi=2500, tau=0.003) * knock
    c[: len(b)] = b
    return finish(room(pan(x + c, 0.0), wet=wet))
