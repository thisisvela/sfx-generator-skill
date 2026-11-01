"""Ticks: a 2 ms noise snap, a short ring and a little tonal body (counters, list items, check marks)."""
from ..blocks import _rng, _tr, env, finish, highpass, osc, pan, place, white
from ..schema import P, SEED, recipe


def tick_core(rng, f=3400, d=0.04, body=0.5, noise=0.6):
    t = _tr(d)
    x = noise * highpass(white(len(t), rng), 2500, 2) * env(t, 0.0003, 0.002)
    x += osc(f, t) * env(t, 0.0005, 0.006)
    x += body * osc(f * 0.33, t) * env(t, 0.0008, 0.005)
    return x


@recipe("tick", family="ticks",
        doc="A crisp wooden tick: a 2 ms noise snap with a short ring and a little body under it.",
        tips="f is the ring pitch (woodier lower, glassier higher); body the tonal body at f/3 (it is what keeps a "
             "tick audible under speech without hitting the peak cap); noise the snap amount.",
        params=[
            P("f", 3400, 500, 10000, 10, "Hz", "ring pitch"),
            P("d", 0.04, 0.02, 0.2, 0.001, "s", "length"),
            P("body", 0.5, 0, 2, 0.01, "", "tonal body amount"),
            P("noise", 0.6, 0, 2, 0.01, "", "snap amount"),
            SEED(105),
        ])
def tick(*, f, d, body, noise, seed):
    rng = _rng(seed)
    return finish(pan(tick_core(rng, f, d, body, noise), 0.0), tail=False, fade_out=0.004)


@recipe("tick_double", family="ticks",
        doc="Two ticks a few tens of ms apart, the second a step higher (a check mark being drawn).",
        tips="f1/f2 are the two ring pitches; gap the time between; body and noise as for tick.",
        params=[
            P("f1", 3300, 500, 10000, 10, "Hz", "first ring pitch"),
            P("f2", 3700, 500, 10000, 10, "Hz", "second ring pitch"),
            P("gap", 0.055, 0.02, 0.4, 0.001, "s", "time between the ticks"),
            P("body", 0.5, 0, 2, 0.01, "", "tonal body amount"),
            P("noise", 0.6, 0, 2, 0.01, "", "snap amount"),
            SEED(106),
        ])
def tick_double(*, f1, f2, gap, body, noise, seed):
    rng = _rng(seed)
    st = place([(0.0, tick_core(rng, f1, body=body, noise=noise) * 0.8), (gap, tick_core(rng, f2, body=body, noise=noise))],
               gap + 0.055)
    return finish(st, tail=False, fade_out=0.004)
