"""Impacts: a falling sub sine (the boom), a low-passed noise knock (the hit), a band of body and a reverb tail."""
import numpy as np

from ..blocks import SR, _rng, fade, lowpass, norm, pan, pink, reverb, svf_bandpass, trim_tail, white
from ..schema import P, SEED, recipe


def impact_core(d, f0, f1, tau, knock, tail, wet, seed, bright):
    rng = _rng(seed)
    n = int(SR * d)
    t = np.arange(n) / SR
    fsub = f1 + (f0 - f1) * np.exp(-t / 0.07)
    sub = np.sin(2 * np.pi * np.cumsum(fsub) / SR) * np.exp(-t / tau)
    sub[: int(SR * 0.004)] *= np.linspace(0, 1, int(SR * 0.004))
    k = lowpass(white(n, rng), bright, 2) * np.exp(-t / 0.022) * knock
    body = svf_bandpass(pink(n, rng), 190, 1.1) * np.exp(-t / 0.12) * 0.5
    mono = sub + k + body
    st = reverb(pan(mono, 0.0), seconds=tail, wet=wet, seed=seed + 10, damp=4500)
    return norm(trim_tail(fade(st[: int(SR * (d + tail * 0.6))], 0.0, 0.05)))


@recipe("impact", family="impact",
        doc="A cinematic hit: a falling sub sine, a short low-passed knock, a band of body and a reverb tail.",
        tips="f0 -> f1 is the boom's pitch fall (lower = deeper); tau its decay; knock the hit's amount; bright its "
             "low-pass (lower = duller); tail and wet the room. d is the dry length; the tail adds 0.6 x tail.",
        params=[
            P("d", 1.4, 0.3, 4.0, 0.05, "s", "dry length"),
            P("f0", 110, 30, 400, 1, "Hz", "boom start pitch"),
            P("f1", 42, 20, 200, 1, "Hz", "boom end pitch"),
            P("tau", 0.28, 0.05, 1.5, 0.01, "s", "boom decay"),
            P("knock", 0.35, 0, 1, 0.01, "", "knock amount"),
            P("bright", 2600, 300, 10000, 10, "Hz", "knock low-pass"),
            P("tail", 1.0, 0.2, 4.0, 0.05, "s", "reverb length"),
            P("wet", 0.22, 0, 0.8, 0.01, "", "reverb amount"),
            SEED(21),
        ])
def impact(*, d, f0, f1, tau, knock, bright, tail, wet, seed):
    return impact_core(d, f0, f1, tau, knock, tail, wet, seed, bright)
