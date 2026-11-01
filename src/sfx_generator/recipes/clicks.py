"""Clicks: a band-passed noise press with a low thump, then an optional quieter release (pointer clicks)."""
from ..blocks import _rng, _tr, env, finish, lowpass, osc, pan, place, svf_bandpass, white
from ..schema import P, SEED, recipe


def click_core(rng, bright=3000, thump=140, d=0.03, t_body=0.008):
    t = _tr(d)
    x = svf_bandpass(white(len(t), rng), bright, 1.2) * env(t, 0.0002, 0.0022) * 1.4
    x += 0.75 * osc(thump, t) * env(t, 0.0006, t_body)
    x += 0.35 * osc(bright * 0.62, t) * env(t, 0.0003, 0.004)
    return x


@recipe("click", family="clicks",
        doc="A mouse click: a sharp press with a low thump, and a quieter release a few tens of ms later.",
        tips="bright is the press's band (lower = duller); thump the low body's pitch; release_gap the time to the "
             "release click, bright2/thump2 its band and body, release_amp its loudness (0 removes it).",
        params=[
            P("bright", 3000, 500, 10000, 10, "Hz", "press band centre"),
            P("thump", 140, 40, 600, 1, "Hz", "thump pitch"),
            P("release_gap", 0.03, 0.0, 0.3, 0.001, "s", "time to the release click"),
            P("bright2", 3600, 500, 10000, 10, "Hz", "release band centre"),
            P("thump2", 160, 40, 600, 1, "Hz", "release thump pitch"),
            P("release_amp", 0.35, 0, 1, 0.01, "", "release click amount"),
            P("d", 0.07, 0.03, 0.5, 0.001, "s", "length"),
            SEED(111),
        ])
def click(*, bright, thump, release_gap, bright2, thump2, release_amp, d, seed):
    rng = _rng(seed)
    st = place([(0.0, click_core(rng, bright, thump)), (release_gap, click_core(rng, bright2, thump2) * release_amp)], d)
    return finish(st, tail=False, fade_out=0.006)


@recipe("click_soft", family="clicks",
        doc="A very light, muffled click.",
        tips="bright and thump as for click; lowpass_hz muffles it (lower = softer).",
        params=[
            P("bright", 1800, 300, 8000, 10, "Hz", "press band centre"),
            P("thump", 110, 40, 600, 1, "Hz", "thump pitch"),
            P("lowpass_hz", 3500, 500, 15000, 50, "Hz", "muffling low-pass"),
            P("d", 0.05, 0.02, 0.3, 0.001, "s", "length"),
            SEED(112),
        ])
def click_soft(*, bright, thump, lowpass_hz, d, seed):
    rng = _rng(seed)
    x = lowpass(click_core(rng, bright=bright, thump=thump, d=d, t_body=0.012), lowpass_hz, 2)
    return finish(pan(x, 0.0), tail=False, fade_out=0.008)
