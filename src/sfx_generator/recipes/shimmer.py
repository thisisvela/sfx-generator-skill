"""Shimmer: seeded high sine pings across the field in reverb; title_hit layers it over a deep impact."""
import numpy as np

from ..blocks import SR, _rng, norm, pan, reverb, trim_tail
from ..schema import I, P, SEED, recipe
from .impact import impact_core


def shimmer_core(d, seed, count, lo, hi, spread):
    rng = _rng(seed)
    n = int(SR * d)
    st = np.zeros((n, 2))
    t = np.arange(n) / SR
    for i in range(count):
        f0 = np.exp(rng.uniform(np.log(lo), np.log(hi)))
        start = rng.uniform(0, spread)
        dec = rng.uniform(0.18, 0.55)
        amp = rng.uniform(0.35, 1.0)
        tt = t - start
        ping = np.where(tt >= 0, np.sin(2 * np.pi * f0 * tt) * np.exp(-np.maximum(tt, 0) / dec), 0.0)
        ping *= np.clip(tt / 0.004, 0, 1)
        st += pan(ping * amp, rng.uniform(-0.8, 0.8))
    st = reverb(st, seconds=1.4, wet=0.35, seed=seed + 20, damp=9000)
    return norm(trim_tail(st))


@recipe("shimmer", family="shimmer",
        doc="A soft sparkle: short sine pings at seeded pitches and times, spread across the stereo field, in reverb.",
        tips="count is how many pings; lo/hi their pitch range; spread the seconds over which they start (small = a "
             "burst, large = a trickle); the seed picks the pitches and timing.",
        params=[
            P("d", 1.8, 0.5, 5.0, 0.05, "s", "length before the tail is trimmed"),
            I("count", 14, 2, 60, "", "number of pings"),
            P("lo", 1900, 300, 8000, 10, "Hz", "lowest ping pitch"),
            P("hi", 6800, 500, 16000, 10, "Hz", "highest ping pitch"),
            P("spread", 0.75, 0.02, 3.0, 0.01, "s", "pings start within this window"),
            SEED(6),
        ])
def shimmer(*, d, count, lo, hi, spread, seed):
    return shimmer_core(d, seed, count, lo, hi, spread)


@recipe("title_hit", family="shimmer",
        doc="A deep impact with a quiet shimmer on top: the intro title landing.",
        tips="sparkle sets the shimmer amount over the hit; f0/f1 the boom; tail the room.",
        params=[
            P("f0", 90, 30, 300, 1, "Hz", "boom start pitch"),
            P("f1", 36, 20, 150, 1, "Hz", "boom end pitch"),
            P("tau", 0.42, 0.1, 1.5, 0.01, "s", "boom decay"),
            P("tail", 1.6, 0.3, 4.0, 0.05, "s", "reverb length"),
            P("wet", 0.26, 0, 0.8, 0.01, "", "reverb amount"),
            P("sparkle", 0.32, 0, 1, 0.01, "", "shimmer amount"),
            I("count", 12, 2, 60, "", "shimmer pings"),
            SEED(8),
        ])
def title_hit(*, f0, f1, tau, tail, wet, sparkle, count, seed):
    hit = impact_core(1.6, f0, f1, tau, 0.4, tail, wet, seed, 2600)
    sp = shimmer_core(2.0, seed + 1, count, 2200, 7500, 0.35) * sparkle
    n = max(len(hit), len(sp))
    out = np.zeros((n, 2))
    out[: len(hit)] += hit
    out[: len(sp)] += sp
    return norm(trim_tail(out))
