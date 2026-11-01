"""Water: bubbles and a single drop."""
import numpy as np

from ..blocks import _rng, _tr, burst, env, finish, glide, lowpass, osc, pan, place, release, room
from ..schema import I, P, SEED, recipe


@recipe("bubble", family="water",
        doc="Fast upward sine glides, seeded: water bubbles, a playful appear.",
        tips="count is how many bubbles; spread the window they rise in; f_lo/f_hi their start pitch range; "
             "rise how far each glides up (ratio).",
        params=[
            I("count", 3, 1, 12, "", "number of bubbles"),
            P("spread", 0.3, 0.0, 2.0, 0.01, "s", "window they start in"),
            P("f_lo", 300, 80, 2000, 1, "Hz", "lowest start pitch"),
            P("f_hi", 700, 100, 4000, 1, "Hz", "highest start pitch"),
            P("rise", 3.0, 1.2, 8.0, 0.1, "", "glide ratio (end / start)"),
            P("wet", 0.08, 0, 0.5, 0.01, "", "room amount"),
            SEED(251),
        ])
def bubble(*, count, spread, f_lo, f_hi, rise, wet, seed):
    rng = _rng(seed)
    parts = []
    for i in range(count):
        f0 = np.exp(rng.uniform(np.log(f_lo), np.log(f_hi)))
        t = _tr(0.13)
        f = glide(f0, f0 * rise, t, 0.035)
        x = (osc(f, t) + 0.1 * osc(2 * f, t)) * env(t, 0.002, 0.045) * rng.uniform(0.6, 1.0)
        parts.append((float(rng.uniform(0, spread)) if count > 1 else 0.0, pan(release(x, 0.03), rng.uniform(-0.4, 0.4))))
    return finish(room(place(parts, spread + 0.15), wet=wet))


@recipe("drop", family="water",
        doc="A single water drop: a tiny tick and a short plink that glides down, in a small room.",
        tips="f is the plink's pitch; tau its decay; wet the room (more = a bigger basin).",
        params=[
            P("f", 1500, 300, 6000, 1, "Hz", "plink start pitch"),
            P("tau", 0.05, 0.01, 0.3, 0.001, "s", "plink decay"),
            P("wet", 0.18, 0, 0.6, 0.01, "", "room amount"),
            SEED(252),
        ])
def drop(*, f, tau, wet, seed):
    rng = _rng(seed)
    t = _tr(0.2)
    x = (osc(glide(f, f * 0.6, t, 0.02), t) + 0.15 * osc(glide(2 * f, 1.2 * f, t, 0.02), t)) * env(t, 0.001, tau)
    c = np.zeros_like(t)
    b = burst(0.004, rng, lo=3000, tau=0.0006) * 0.2
    c[: len(b)] = b
    return finish(room(pan(x + c, 0.0), wet=wet, seconds=0.5))
