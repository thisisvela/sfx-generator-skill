"""Error: two square-ish tones stepping down (a tritone by default), low-passed: a short buzzy 'uh-oh'."""
import numpy as np

from ..blocks import _tr, env, finish, lowpass, place, release
from ..schema import P, SEED, recipe


@recipe("error", family="error",
        doc="A short, buzzy 'uh-oh': two square-ish tones stepping down a tritone, low-passed.",
        tips="f1/f2 are the two tones (466 -> 330 Hz is a tritone; a bigger fall sounds worse); gap the time "
             "between; lowpass_hz the buzz's brightness; d2 the second tone's length.",
        params=[
            P("f1", 466, 80, 2000, 1, "Hz", "first tone"),
            P("f2", 330, 60, 2000, 1, "Hz", "second tone"),
            P("gap", 0.085, 0.03, 0.4, 0.005, "s", "time between the tones"),
            P("d2", 0.16, 0.05, 0.6, 0.005, "s", "second tone length"),
            P("lowpass_hz", 2600, 500, 10000, 50, "Hz", "buzz low-pass"),
            SEED(120),
        ])
def error(*, f1, f2, gap, d2, lowpass_hz, seed):
    def buzz(f, d, tau):
        t = _tr(d)
        ph = 2 * np.pi * f * t
        sq = np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5 + np.sin(7 * ph) / 7
        return release(lowpass(sq, lowpass_hz, 2) * env(t, 0.003, tau), 0.04)
    st = place([(0.0, buzz(f1, 0.09, 0.05)), (gap, buzz(f2, d2, 0.07))], gap + d2 + 0.015)
    return finish(st)
