"""Whooshes: band-passed noise whose centre frequency sweeps up and back down, panned across the field."""
import numpy as np

from ..blocks import SR, _rng, fade, logsweep, lowpass, norm, pan, pink, svf_bandpass, white
from ..schema import P, SEED, recipe


@recipe("whoosh", family="whoosh",
        doc="Band-passed noise swept up and back down, panned across the stereo field: the transition sound.",
        tips="d sets the length; peak is where (0-1) the loudest, highest moment falls; f_start/f_peak/f_end are "
             "the band's centre at the start, the peak and the end; q_* its narrowness there (higher = whistlier); "
             "body adds a low band at 0.18 x fc; air adds white noise fizz; pan_from/pan_to move it across the "
             "field. A lead of about 0.4 x d puts the peak just after the cue.",
        params=[
            P("d", 0.7, 0.15, 3.0, 0.01, "s", "length"),
            P("peak", 0.55, 0.1, 0.9, 0.01, "", "position of the loudest moment (0-1)"),
            P("f_start", 350, 60, 6000, 1, "Hz", "band centre at the start"),
            P("f_peak", 2200, 100, 12000, 1, "Hz", "band centre at the peak"),
            P("f_end", 650, 60, 6000, 1, "Hz", "band centre at the end"),
            P("q_start", 0.9, 0.3, 6, 0.05, "", "band narrowness at the start"),
            P("q_peak", 1.5, 0.3, 6, 0.05, "", "band narrowness at the peak"),
            P("q_end", 1.0, 0.3, 6, 0.05, "", "band narrowness at the end"),
            P("pan_from", 0.45, -1, 1, 0.05, "", "pan at the start (-1 left, 1 right)"),
            P("pan_to", -0.45, -1, 1, 0.05, "", "pan at the end"),
            P("body", 0.25, 0, 1, 0.01, "", "low body band amount"),
            P("air", 0.15, 0, 0.6, 0.01, "", "white-noise air on top of the pink source"),
            P("lowpass_hz", 9500, 2000, 20000, 50, "Hz", "final low-pass (takes the fizz off)"),
            SEED(1),
        ])
def whoosh(*, d, peak, f_start, f_peak, f_end, q_start, q_peak, q_end, pan_from, pan_to, body, air, lowpass_hz,
           seed):
    rng = _rng(seed)
    n = int(SR * d)
    src = 0.7 * pink(n, rng) + air * white(n, rng)
    fc = logsweep([(0, f_start), (peak, f_peak), (1, f_end)], n)
    qq = np.interp(np.linspace(0, 1, n), [0, peak, 1], (q_start, q_peak, q_end))
    band = svf_bandpass(svf_bandpass(src, fc, qq), fc, qq)      # two stages: a clearer moving band
    low = svf_bandpass(pink(n, rng), fc * 0.18, 0.8) * body
    s = np.linspace(0, 1, n)
    rise = np.sin(np.pi / 2 * np.clip(s / peak, 0, 1)) ** 2
    fall = np.cos(np.pi / 2 * np.clip((s - peak) / (1 - peak), 0, 1)) ** 1.6
    env = np.where(s < peak, rise, fall)
    mono = (band + low) * env
    st = pan(mono, np.interp(s, [0, 1], [pan_from, pan_to]))
    st = lowpass(st, lowpass_hz, 2)
    return norm(fade(st, 0.002, 0.02))
