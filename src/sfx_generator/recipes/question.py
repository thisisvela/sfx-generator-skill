"""Question motifs: a tone that bends or slides upward, like a spoken 'hmm?'."""
import numpy as np

from ..blocks import _tr, env, finish, osc, pan, place, release, room, tone
from ..schema import P, SEED, recipe

SOFT = [(1, 1.0, 0.12), (2, 0.18, 0.06), (3, 0.08, 0.04)]


@recipe("question", family="question",
        doc="'Hmm?': a soft note, then a higher one that bends upwards at the end.",
        tips="f1 is the first note, f2 the second; bend how far the second bends up (0.06 = 6 %); gap the time "
             "between them.",
        params=[
            P("f1", 659.25, 100, 3000, 0.01, "Hz", "first note (E5)"),
            P("f2", 880, 100, 4000, 0.01, "Hz", "second note (A5)"),
            P("bend", 0.06, 0, 0.3, 0.005, "", "upward bend at the end"),
            P("gap", 0.14, 0.03, 0.6, 0.005, "s", "time between the notes"),
            P("wet", 0.1, 0, 0.5, 0.01, "", "room amount"),
            SEED(118),
        ])
def question(*, f1, f2, bend, gap, wet, seed):
    t1, t2 = _tr(0.22), _tr(0.32)
    a = tone(f1, t1, SOFT, attack=0.006)
    ff = f2 * (1 + bend * np.clip((t2 - 0.08) / 0.18, 0, 1) ** 2)
    b = release((osc(ff, t2) + 0.18 * osc(2 * ff, t2)) * env(t2, 0.006, 0.14), 0.1)
    st = place([(0.0, pan(a * 0.8, -0.1)), (gap, pan(b, 0.1))], gap + 0.36)
    return finish(room(st, wet=wet))


@recipe("question_alt", family="question",
        doc="A single tone sliding up (a fifth by default): a lighter question.",
        tips="f0 the start pitch; interval the ratio it slides to (1.5 = a fifth, 2 = an octave); slide the time "
             "the slide takes.",
        params=[
            P("f0", 988, 100, 4000, 0.1, "Hz", "start pitch (B5)"),
            P("interval", 1.5, 1.0, 3.0, 0.01, "", "ratio it slides to"),
            P("slide", 0.2, 0.05, 0.6, 0.005, "s", "slide time"),
            P("d", 0.36, 0.15, 1.5, 0.005, "s", "length"),
            P("wet", 0.1, 0, 0.5, 0.01, "", "room amount"),
            SEED(119),
        ])
def question_alt(*, f0, interval, slide, d, wet, seed):
    t = _tr(d)
    f = f0 * np.exp(np.log(interval) * np.clip(t / slide, 0, 1) ** 1.5)
    x = release((osc(f, t) + 0.2 * osc(2 * f, t)) * np.clip(t / 0.01, 0, 1) * np.exp(-np.maximum(t - 0.12, 0) / 0.08), 0.1)
    return finish(room(pan(x, 0.0), wet=wet))
