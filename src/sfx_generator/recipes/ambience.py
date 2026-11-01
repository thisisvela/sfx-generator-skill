"""Ambience loops: beds that play under a whole beat. Every oscillator and LFO completes a whole number of cycles
in the loop length, so the hum wraps with no seam; the noise bed is crossfaded with `loop_seam`."""
import numpy as np

from ..blocks import SR, _rng, loop_seam, lowpass, norm, pan, pink, svf_bandpass
from ..schema import P, SEED, recipe


def _cycles(f, d):
    """The nearest frequency to f that completes a whole number of cycles in d seconds."""
    return max(1, round(f * d)) / d


@recipe("hum_loop", family="ambience",
        doc="A machine hum that exists on small speakers: a mains-like fundamental with a rich harmonic series "
            "peaking in a formant around 300-700 Hz (the transformer's rasp), a breathing fan bed of filtered noise "
            "above it, and a slow wobble; a seamless loop (every partial completes whole cycles).",
        tips="f0 is the hum's pitch (50 or 60 Hz = mains; 55 = A1); formant where the harmonics peak (what a laptop "
             "hears); buzz the rasp of the upper harmonics; fan the noise bed's amount; breathe how much it all "
             "swells; d the loop length.",
        params=[
            P("f0", 55, 30, 220, 0.5, "Hz", "hum pitch"),
            P("d", 4.0, 1.0, 16.0, 0.5, "s", "loop length"),
            P("formant", 450, 150, 1500, 10, "Hz", "where the harmonics peak"),
            P("buzz", 0.6, 0, 1.5, 0.05, "", "rasp of the upper harmonics"),
            P("fan", 0.5, 0, 1.5, 0.05, "", "fan noise bed amount"),
            P("breathe", 0.4, 0, 1, 0.05, "", "swell depth"),
            SEED(261),
        ])
def hum_loop(*, f0, d, formant, buzz, fan, breathe, seed):
    rng = _rng(seed)
    n = int(round(SR * d))
    t = np.arange(n) / SR
    out = np.zeros(n)
    # the harmonic series: 24 partials, weighted by a formant (a resonance around `formant`) so the energy a
    # small speaker can play sits at 300-700 Hz, not at the fundamental; odd partials a little stronger (mains)
    for k in range(1, 25):
        f = _cycles(f0 * k, d)
        w = np.exp(-0.5 * ((np.log(f / formant)) / 0.55) ** 2)            # the formant, about an octave wide
        a = (1.0 if k == 1 else 0.6) * (1.3 if k % 2 == 1 else 1.0) * (0.35 + w * (0.5 + buzz)) / k ** 0.35
        cyc, ph = (k % 3) + 1, 0.7 * k
        lfo = 1 - breathe * 0.5 * (1 - np.cos(2 * np.pi * cyc * t / d + ph))
        out += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi)) * lfo
    out = np.tanh(out / (np.abs(out).max() + 1e-9) * (1.0 + 1.5 * buzz))   # the transformer's rasp
    out -= out.mean()                                                   # the rasp is asymmetric: no DC in a loop
    # the fan: filtered noise with a soft peak around 2 x the formant, breathing with the hum
    m = n + int(SR * 0.15)                                             # loop_seam drops the crossfade's length
    tm = np.arange(m) / SR
    bed = svf_bandpass(pink(m, rng), formant * 2.2, 0.4) + 0.5 * svf_bandpass(pink(m, rng), formant * 0.8, 0.6)
    bed *= 1 - breathe * 0.3 * (1 - np.cos(2 * np.pi * tm / (m / SR) + 2.0))
    bed = loop_seam(np.stack([bed, bed * 0.9 + 0.3 * svf_bandpass(pink(m, rng), formant * 2.2, 0.4)], axis=1), 0.15)[:n]
    hum = pan(out, 0.0)
    st = hum / (np.abs(hum).max() + 1e-9) + bed / (np.abs(bed).max() + 1e-9) * 0.55 * fan
    return norm(st)                                                     # no causal filter after the seam: it clicks


@recipe("air_loop", family="ambience",
        doc="Filtered pink noise with a slowly moving band: room tone, air, a quiet bed; a seamless loop.",
        tips="f_lo/f_hi are the band's travel; d the loop length; lowpass_hz the overall darkness; the loop is "
             "crossfaded over 0.15 s so the seam is silent.",
        params=[
            P("d", 4.0, 1.0, 16.0, 0.5, "s", "loop length (before the seam crossfade)"),
            P("f_lo", 300, 60, 3000, 10, "Hz", "band low point"),
            P("f_hi", 600, 100, 6000, 10, "Hz", "band high point"),
            P("lowpass_hz", 4000, 500, 16000, 50, "Hz", "final low-pass"),
            SEED(262),
        ])
def air_loop(*, d, f_lo, f_hi, lowpass_hz, seed):
    rng = _rng(seed)
    n = int(round(SR * d))
    t = np.arange(n) / SR
    fc = np.exp(np.log(f_lo) + (np.log(f_hi) - np.log(f_lo)) * 0.5 * (1 - np.cos(2 * np.pi * t / d)))
    left = svf_bandpass(pink(n, rng), fc, 0.7)
    right = svf_bandpass(pink(n, rng), fc * 1.05, 0.7)
    st = lowpass(np.stack([left, right], axis=1), lowpass_hz, 2)
    return norm(loop_seam(st, 0.15))
