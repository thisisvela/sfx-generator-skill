"""Glitches: short crushed square bursts with gaps (digital stutters)."""
import numpy as np

from ..blocks import SR, _rng, fade, finish, lowpass, norm, pan, svf_bandpass
from ..schema import I, P, SEED, recipe


@recipe("glitch_burst", family="glitch",
        doc="A digital stutter: five short band-limited square bursts at seeded pitches with gaps, a little crushed. "
            "Long enough (about 0.4 s) to be heard under a voice, unlike a 30 ms click.",
        tips="count is the number of bursts; f_lo/f_hi their pitch range; crush the number of levels (fewer = "
             "harsher); band_hz where the band-pass sits; the seed picks pitches, lengths and gaps.",
        params=[
            P("d", 0.38, 0.1, 2.0, 0.01, "s", "length"),
            I("count", 5, 1, 20, "", "number of bursts"),
            P("f_lo", 320, 60, 4000, 1, "Hz", "lowest burst pitch"),
            P("f_hi", 1400, 100, 8000, 1, "Hz", "highest burst pitch"),
            I("crush", 6, 2, 32, "", "quantisation levels"),
            P("band_hz", 1800, 300, 8000, 10, "Hz", "band-pass centre"),
            SEED(10),
        ])
def glitch_burst(*, d, count, f_lo, f_hi, crush, band_hz, seed):
    rng = _rng(seed)
    n = int(SR * d)
    out = np.zeros(n)
    t0 = 0.0
    for k in range(count):
        ln = rng.uniform(0.035, 0.06)
        f0 = rng.uniform(f_lo, f_hi)
        a, b = int(t0 * SR), min(n, int((t0 + ln) * SR))
        if b <= a:
            break
        tt = np.arange(b - a) / SR
        sq = np.sign(np.sin(2 * np.pi * f0 * tt)) * 0.6 + 0.4 * np.sin(2 * np.pi * f0 * 2.01 * tt)
        sq = np.round(sq * crush) / crush                                   # crushed to a few levels
        env = np.minimum(1, tt / 0.003) * np.minimum(1, (tt[-1] - tt + 1e-4) / 0.004)
        out[a:b] += sq * env * (1.0 - 0.12 * k)
        t0 += ln + rng.uniform(0.015, 0.035)
    out = svf_bandpass(out, band_hz, 0.7) + 0.25 * out
    st = pan(out, np.interp(np.linspace(0, 1, n), [0, 1], [-0.3, 0.3]))
    return norm(fade(lowpass(st, 9000, 2), 0.001, 0.02))


@recipe("glitch", family="glitch",
        doc="A tiny digital glitch: three crushed square bursts in 75 ms (glitch_burst is the longer one).",
        tips="count and d set how many bursts fit; f_lo/f_hi their pitch; band_hz the band-pass. Under speech "
             "prefer glitch_burst: 75 ms vanishes.",
        params=[
            P("d", 0.075, 0.03, 0.5, 0.005, "s", "length"),
            I("count", 3, 1, 12, "", "number of bursts"),
            P("f_lo", 900, 100, 6000, 1, "Hz", "lowest burst pitch"),
            P("f_hi", 2600, 200, 10000, 1, "Hz", "highest burst pitch"),
            P("band_hz", 3000, 300, 10000, 10, "Hz", "band-pass centre"),
            SEED(121),
        ])
def glitch(*, d, count, f_lo, f_hi, band_hz, seed):
    rng = _rng(seed)
    out = np.zeros(int(SR * d))
    t0 = 0.0
    for k in range(count):
        ln = rng.uniform(0.012, 0.02)
        f0 = rng.uniform(f_lo, f_hi)
        a, b = int(t0 * SR), min(len(out), int((t0 + ln) * SR))
        if b <= a:
            break
        tt = np.arange(b - a) / SR
        sq = np.round(np.sign(np.sin(2 * np.pi * f0 * tt)) * 4) / 4
        out[a:b] += sq * np.minimum(1, tt / 0.001) * (1 - 0.2 * k)
        t0 += ln + rng.uniform(0.006, 0.012)
    out = svf_bandpass(out, band_hz, 0.8) + 0.3 * out
    return finish(pan(out, 0.0), tail=False, fade_out=0.005)
