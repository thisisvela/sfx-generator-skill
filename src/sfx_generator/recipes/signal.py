"""Signals: data blips, a scan sweep, a sonar ping."""
import numpy as np

from ..blocks import _rng, _tr, env, finish, lowpass, norm, osc, pan, place, release, reverb, trim_tail
from ..schema import I, P, SEED, recipe


@recipe("data_blips", family="signal",
        doc="A seeded stream of very short high blips: data transferring, packets flowing.",
        tips="count is how many blips; d the window they fall in; f_lo/f_hi their pitch range; width the stereo "
             "spread; the seed picks the rhythm and pitches.",
        params=[
            I("count", 12, 2, 60, "", "number of blips"),
            P("d", 0.6, 0.1, 3.0, 0.01, "s", "window length"),
            P("f_lo", 2000, 300, 10000, 10, "Hz", "lowest blip"),
            P("f_hi", 5200, 500, 14000, 10, "Hz", "highest blip"),
            P("width", 0.5, 0, 1, 0.05, "", "stereo spread"),
            SEED(241),
        ])
def data_blips(*, count, d, f_lo, f_hi, width, seed):
    rng = _rng(seed)
    starts = np.sort(rng.uniform(0, d - 0.03, count))
    parts = []
    for s in starts:
        f = np.exp(rng.uniform(np.log(f_lo), np.log(f_hi)))
        t = _tr(rng.uniform(0.012, 0.025))
        x = (osc(f, t) + 0.2 * osc(2 * f, t)) * env(t, 0.001, 0.008) * rng.uniform(0.5, 1.0)
        parts.append((float(s), pan(release(x, 0.004), rng.uniform(-width, width))))
    return finish(place(parts, d + 0.03), tail=False, fade_out=0.01)


@recipe("scan", family="signal",
        doc="A rising sine sweep with tremolo: scanning, searching, a progress sweep.",
        tips="f_start -> f_end is the sweep; d its length; tremolo_hz the flutter rate and depth its amount.",
        params=[
            P("d", 0.6, 0.15, 3.0, 0.01, "s", "length"),
            P("f_start", 400, 60, 4000, 1, "Hz", "sweep start"),
            P("f_end", 2400, 200, 10000, 1, "Hz", "sweep end"),
            P("tremolo_hz", 18, 2, 60, 0.5, "Hz", "tremolo rate"),
            P("depth", 0.5, 0, 1, 0.01, "", "tremolo depth"),
            SEED(242),
        ])
def scan(*, d, f_start, f_end, tremolo_hz, depth, seed):
    t = _tr(d)
    n = len(t)
    f = np.exp(np.linspace(np.log(f_start), np.log(f_end), n))
    x = osc(f, t) + 0.2 * osc(2 * f, t)
    trem = 1 - depth * 0.5 * (1 - np.cos(2 * np.pi * tremolo_hz * t))
    e = np.sin(np.pi * np.clip(t / (0.15 * d), 0, 1) / 2) ** 2 * np.cos(np.pi / 2 * np.clip((t - 0.6 * d) / (0.4 * d), 0, 1)) ** 2
    return finish(pan(lowpass(x * trem * e, 9000, 2), 0.0), tail=False, fade_out=0.02)


@recipe("sonar", family="signal",
        doc="A sine ping in a long, dark reverb: a probe, a search, waiting for a reply.",
        tips="f is the ping's pitch; tau its own decay; tail and wet the dark room (damp_hz sets how dark).",
        params=[
            P("f", 1200, 200, 5000, 1, "Hz", "ping pitch"),
            P("tau", 0.12, 0.02, 0.6, 0.005, "s", "ping decay"),
            P("tail", 1.6, 0.3, 5.0, 0.05, "s", "reverb length"),
            P("wet", 0.5, 0, 1, 0.01, "", "reverb amount"),
            P("damp_hz", 2500, 500, 12000, 50, "Hz", "reverb damping"),
            SEED(243),
        ])
def sonar(*, f, tau, tail, wet, damp_hz, seed):
    t = _tr(0.5)
    x = (osc(f, t) + 0.2 * osc(2 * f, t)) * env(t, 0.002, tau)
    st = reverb(pan(release(x, 0.05), 0.0), seconds=tail, wet=wet, seed=seed, damp=damp_hz)
    return norm(trim_tail(st))
