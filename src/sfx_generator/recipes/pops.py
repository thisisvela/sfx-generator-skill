"""Pops and plucks: a sine whose pitch glides as it decays, with a soft click on top (things appearing)."""
import numpy as np

from ..blocks import _rng, _tr, burst, env, finish, glide, ks_pluck, osc, pan, release, room
from ..schema import P, SEED, recipe


@recipe("pop", family="pops",
        doc="A round bubble pop: a sine that jumps up in pitch as it dies away, with a soft click on top.",
        tips="f0 -> f1 is the pitch jump (up = a bubble, down = a thud); tc how fast it moves; tau the decay; "
             "click the noise transient's amount; second the 2nd harmonic (rounder when low).",
        params=[
            P("d", 0.16, 0.05, 0.6, 0.005, "s", "length"),
            P("f0", 600, 80, 3000, 1, "Hz", "pitch at the start"),
            P("f1", 900, 80, 4000, 1, "Hz", "pitch it glides to"),
            P("tc", 0.03, 0.005, 0.2, 0.001, "s", "glide time constant"),
            P("tau", 0.028, 0.005, 0.3, 0.001, "s", "decay"),
            P("second", 0.18, 0, 1, 0.01, "", "2nd harmonic amount"),
            P("click", 0.25, 0, 1, 0.01, "", "click amount"),
            SEED(101),
        ])
def pop(*, d, f0, f1, tc, tau, second, click, seed):
    rng = _rng(seed)
    t = _tr(d)
    f = glide(f0, f1, t, tc)
    body = (osc(f, t) + second * osc(2 * f, t)) * env(t, 0.0015, tau)
    c = np.zeros_like(t)
    b = burst(0.01, rng, lo=1500, hi=7000, tau=0.0015) * click
    c[: len(b)] = b
    return finish(pan(body + c, 0.0))


@recipe("pop_low", family="pops",
        doc="A heavier pop: lower and rounder, with a little sub thump.",
        tips="f0 -> f1 the body glide; thump the sub amount (140 -> 90 Hz); tau the decay.",
        params=[
            P("d", 0.2, 0.05, 0.8, 0.005, "s", "length"),
            P("f0", 330, 60, 2000, 1, "Hz", "pitch at the start"),
            P("f1", 520, 60, 3000, 1, "Hz", "pitch it glides to"),
            P("tc", 0.035, 0.005, 0.2, 0.001, "s", "glide time constant"),
            P("tau", 0.04, 0.005, 0.4, 0.001, "s", "decay"),
            P("thump", 0.45, 0, 1.5, 0.01, "", "sub thump amount"),
            P("click", 0.18, 0, 1, 0.01, "", "click amount"),
            SEED(102),
        ])
def pop_low(*, d, f0, f1, tc, tau, thump, click, seed):
    rng = _rng(seed)
    t = _tr(d)
    f = glide(f0, f1, t, tc)
    body = (osc(f, t) + 0.22 * osc(2 * f, t)) * env(t, 0.002, tau)
    th = osc(glide(140, 90, t, 0.03), t) * env(t, 0.002, 0.03) * thump
    c = np.zeros_like(t)
    b = burst(0.01, rng, lo=800, hi=4000, tau=0.002) * click
    c[: len(b)] = b
    return finish(pan(body + th + c, 0.0))


@recipe("pop_up", family="pops",
        doc="A rising bloop: the pitch climbs well over an octave while it fades.",
        tips="f0 -> f1 is the climb; tc how fast; tau the decay; wet the small room.",
        params=[
            P("d", 0.3, 0.08, 1.0, 0.005, "s", "length"),
            P("f0", 480, 60, 3000, 1, "Hz", "pitch at the start"),
            P("f1", 1550, 100, 6000, 1, "Hz", "pitch it climbs to"),
            P("tc", 0.07, 0.01, 0.5, 0.001, "s", "glide time constant"),
            P("tau", 0.06, 0.01, 0.5, 0.001, "s", "decay"),
            P("wet", 0.06, 0, 0.4, 0.01, "", "room amount"),
            SEED(103),
        ])
def pop_up(*, d, f0, f1, tc, tau, wet, seed):
    t = _tr(d)
    f = glide(f0, f1, t, tc)
    x = release((osc(f, t) + 0.15 * osc(2 * f, t)) * env(t, 0.003, tau), 0.08)
    return finish(room(pan(x, 0.0), wet=wet))


@recipe("pluck", family="pops",
        doc="A bright plucked string (Karplus-Strong) with a short attack click: a label or value snaps in.",
        tips="f0 is the pitch; damp how long the string rings (0.999 = long); bright the excitation's brightness; "
             "tau an outer decay; the seed changes the string's noise.",
        params=[
            P("f0", 1245, 80, 5000, 1, "Hz", "string pitch"),
            P("d", 0.22, 0.05, 2.0, 0.005, "s", "length"),
            P("damp", 0.993, 0.9, 0.9995, 0.0005, "", "string damping per sample"),
            P("bright", 0.75, 0, 1, 0.01, "", "excitation brightness"),
            P("tau", 0.06, 0.01, 1.0, 0.001, "s", "outer decay"),
            P("click", 0.2, 0, 1, 0.01, "", "attack click amount"),
            SEED(104),
        ])
def pluck(*, f0, d, damp, bright, tau, click, seed):
    rng = _rng(seed)
    s = ks_pluck(f0, d, seed, damp=damp, bright=bright)
    t = _tr(d)
    s = s[: len(t)] * env(t, 0.0005, tau)
    s = s / (np.abs(s).max() + 1e-9)
    c = np.zeros_like(t)
    b = burst(0.006, rng, lo=3000, tau=0.001) * click
    c[: len(b)] = b
    return finish(pan(s + c, 0.0))
