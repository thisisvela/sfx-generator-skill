"""Camera swells: a tone with its fifth and octave gliding, with a breath of band-passed pink (push-ins, pull-backs)."""
import numpy as np

from ..blocks import _rng, _tr, finish, osc, pan, pink, room, svf_bandpass
from ..schema import B, P, SEED, recipe


def swell_core(f0, f1, rising, d, seed, air, wet):
    rng = _rng(seed)
    t = _tr(d)
    s = t / d
    f = f0 * (f1 / f0) ** s
    x = osc(f, t) + 0.25 * osc(1.5 * f, t) + 0.1 * osc(2 * f, t)
    a = svf_bandpass(pink(len(t), rng), f * 1.8, 1.5) * air
    e = np.sin(np.pi * np.clip(s / 0.35, 0, 1) / 2) ** 2 * np.cos(np.pi / 2 * np.clip((s - 0.35) / 0.65, 0, 1)) ** 1.5
    if not rising:
        e = e[::-1]
    return finish(room(pan((x + a) * e, 0.0), wet=wet), tail=False, fade_out=0.01)


@recipe("swell_up", family="camera",
        doc="A soft tonal lift for a push-in: a tone and its fifth gliding up, with a breath of air.",
        tips="f0 -> f1 is the glide; d the length; air the pink breath's amount; wet the room.",
        params=[
            P("f0", 1078, 100, 5000, 1, "Hz", "start pitch"),
            P("f1", 1640, 100, 6000, 1, "Hz", "end pitch"),
            P("d", 0.28, 0.1, 1.5, 0.005, "s", "length"),
            P("air", 0.25, 0, 1, 0.01, "", "breath amount"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            SEED(122),
        ])
def swell_up(*, f0, f1, d, air, wet, seed):
    return swell_core(f0, f1, True, d, seed, air, wet)


@recipe("swell_down", family="camera",
        doc="The mirror for a pull-back: gliding down, swelling into the end.",
        tips="f0 -> f1 is the glide (down by default); the envelope is reversed, so it swells into its end.",
        params=[
            P("f0", 1640, 100, 6000, 1, "Hz", "start pitch"),
            P("f1", 1078, 100, 5000, 1, "Hz", "end pitch"),
            P("d", 0.28, 0.1, 1.5, 0.005, "s", "length"),
            P("air", 0.25, 0, 1, 0.01, "", "breath amount"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            SEED(123),
        ])
def swell_down(*, f0, f1, d, air, wet, seed):
    return swell_core(f0, f1, False, d, seed, air, wet)
