"""Anticipation: sounds that build and end ON the cue (lead = duration)."""
import numpy as np

from ..blocks import SR, _rng, fade, highpass, logsweep, lowpass, norm, pan, pink, reverb, svf_bandpass, white
from ..schema import P, SEED, recipe


@recipe("swoosh_up", family="anticipation",
        doc="A short rising swoosh whose loudest moment is its last: put its end on the cue (a reveal).",
        tips="f_start -> f_end is the noise band's sweep; tone_* a quiet sine that rises with it; curve shapes the "
             "rise (higher = later, steeper); q narrows the band.",
        params=[
            P("d", 0.75, 0.2, 3.0, 0.01, "s", "length (ends on the cue)"),
            P("f_start", 260, 60, 4000, 1, "Hz", "band centre at the start"),
            P("f_end", 4200, 300, 12000, 1, "Hz", "band centre at the end"),
            P("q", 1.4, 0.3, 6, 0.05, "", "band narrowness"),
            P("tone_start", 220, 40, 2000, 1, "Hz", "the sine's start pitch"),
            P("tone_end", 660, 40, 4000, 1, "Hz", "the sine's end pitch"),
            P("tone_amp", 0.12, 0, 0.6, 0.01, "", "sine amount"),
            P("curve", 2.2, 0.5, 6, 0.1, "", "envelope exponent (s^curve)"),
            P("width", 0.25, 0, 1, 0.05, "", "pan travel, left to right"),
            SEED(2),
        ])
def swoosh_up(*, d, f_start, f_end, q, tone_start, tone_end, tone_amp, curve, width, seed):
    rng = _rng(seed)
    n = int(SR * d)
    s = np.linspace(0, 1, n)
    fc = logsweep([(0, f_start), (1, f_end)], n)
    src = 0.75 * pink(n, rng) + 0.25 * white(n, rng)
    band = svf_bandpass(svf_bandpass(src, fc, q), fc, q)
    tone_f = logsweep([(0, tone_start), (1, tone_end)], n)
    tone = np.sin(2 * np.pi * np.cumsum(tone_f) / SR) * tone_amp
    env = s ** curve
    env[-int(SR * 0.05):] *= np.linspace(1, 0, int(SR * 0.05))
    st = pan((band + tone) * env, np.interp(s, [0, 1], [-width, width]))
    return norm(lowpass(st, 10000, 2))


@recipe("riser", family="anticipation",
        doc="Noise and a detuned tone rise together over the length and end on the cue: build-up before a reveal.",
        tips="d is the whole build; f_* the noise band's sweep (the right ear's band is slightly higher, for "
             "width); tone_* the chord's root glide; det_hi/det_lo the two side oscillators' ratios (beating); "
             "curve makes the rise later and steeper.",
        params=[
            P("d", 2.0, 0.5, 8.0, 0.05, "s", "length (ends on the cue)"),
            P("f_start", 180, 40, 2000, 1, "Hz", "left noise band at the start"),
            P("f_end", 5200, 500, 14000, 1, "Hz", "left noise band at the end"),
            P("f_start_r", 200, 40, 2000, 1, "Hz", "right noise band at the start"),
            P("f_end_r", 5600, 500, 14000, 1, "Hz", "right noise band at the end"),
            P("tone_start", 110, 30, 1000, 1, "Hz", "tone root at the start"),
            P("tone_end", 440, 60, 4000, 1, "Hz", "tone root at the end"),
            P("det_hi", 1.007, 1.0, 1.05, 0.001, "", "upper detune ratio"),
            P("det_lo", 0.994, 0.95, 1.0, 0.001, "", "lower detune ratio"),
            P("tone_amp", 0.32, 0, 1, 0.01, "", "tone amount against the noise"),
            P("curve", 2.6, 0.5, 6, 0.1, "", "envelope exponent (s^curve)"),
            SEED(3),
        ])
def riser(*, d, f_start, f_end, f_start_r, f_end_r, tone_start, tone_end, det_hi, det_lo, tone_amp, curve, seed):
    rng = _rng(seed)
    n = int(SR * d)
    s = np.linspace(0, 1, n)
    band = svf_bandpass(0.6 * pink(n, rng) + 0.4 * white(n, rng), logsweep([(0, f_start), (1, f_end)], n), 1.2)
    f0 = logsweep([(0, tone_start), (1, tone_end)], n)
    tone = np.zeros(n)
    for det, amp in ((1.0, 1.0), (det_hi, 0.7), (det_lo, 0.7)):
        ph = 2 * np.pi * np.cumsum(f0 * det) / SR
        tone += amp * (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph))
    tone /= np.abs(tone).max()
    env = s ** curve
    env[-int(SR * 0.04):] *= np.linspace(1, 0, int(SR * 0.04))
    left = (band * 0.8 + tone * tone_amp) * env
    right = (svf_bandpass(white(n, rng), logsweep([(0, f_start_r), (1, f_end_r)], n), 1.2) * 0.8 + tone * tone_amp) * env
    st = np.stack([left, right], axis=1)
    return norm(lowpass(st, 11000, 2))


@recipe("swell", family="anticipation",
        doc="A reverse-cymbal swell: a reverberated noise burst played backwards, so it grows into the cue.",
        tips="d is the length; hp_hz brightens the burst (higher = thinner, airier); wet is the reverb amount "
             "before reversal; lowpass_hz tames the top.",
        params=[
            P("d", 1.2, 0.3, 5.0, 0.05, "s", "length (ends on the cue)"),
            P("hp_hz", 1800, 200, 8000, 10, "Hz", "high-pass on the burst"),
            P("wet", 0.9, 0.2, 1.0, 0.01, "", "reverb amount"),
            P("damp_hz", 7000, 1500, 16000, 50, "Hz", "reverb damping"),
            P("lowpass_hz", 8500, 2000, 20000, 50, "Hz", "final low-pass"),
            SEED(4),
        ])
def swell(*, d, hp_hz, wet, damp_hz, lowpass_hz, seed):
    rng = _rng(seed)
    n = int(SR * 0.35)
    burst = highpass(white(n, rng), hp_hz, 2) * np.exp(-np.arange(n) / SR / 0.08)
    st = reverb(pan(burst, 0.0), seconds=d, wet=wet, seed=seed, damp=damp_hz)
    st = st[: int(SR * d)][::-1]
    st = lowpass(st, lowpass_hz, 2)
    return norm(fade(st, 0.01, 0.03))
