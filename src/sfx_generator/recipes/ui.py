"""Toggles and switches: state changes."""
import numpy as np

from ..blocks import _rng, _tr, env, finish, osc, place, release, room, tone
from ..schema import P, SEED, recipe
from .clicks import click_core


@recipe("toggle", family="ui",
        doc="Two quick bright blips a fourth apart: a state flips on.",
        tips="f1/f2 are the blips (f2 below f1 reads as 'off'); gap the time between; tau each blip's decay.",
        params=[
            P("f1", 1406, 200, 6000, 1, "Hz", "first blip"),
            P("f2", 1875, 200, 8000, 1, "Hz", "second blip"),
            P("gap", 0.055, 0.0, 0.3, 0.001, "s", "time between the blips"),
            P("tau", 0.018, 0.005, 0.1, 0.001, "s", "each blip's decay"),
            P("d", 0.15, 0.05, 0.6, 0.005, "s", "length"),
            SEED(113),
        ])
def toggle(*, f1, f2, gap, tau, d, seed):
    t = _tr(0.06)

    def blip(f):
        return (osc(f, t) + 0.3 * osc(3 * f, t) + 0.1 * osc(5 * f, t)) * env(t, 0.001, tau)
    st = place([(0.0, blip(f1) * 0.8), (gap, blip(f2))], d)
    return finish(st, tail=False, fade_out=0.01)


@recipe("switch", family="ui",
        doc="A mechanical switch: click-clack with a short metallic ring after each.",
        tips="f1/f2 are the two rings' pitches; gap the time between click and clack; ring the ring amount; "
             "wet the room.",
        params=[
            P("f1", 1031, 200, 5000, 1, "Hz", "first ring pitch"),
            P("f2", 890, 200, 5000, 1, "Hz", "second ring pitch"),
            P("gap", 0.11, 0.03, 0.5, 0.005, "s", "time between click and clack"),
            P("ring", 0.45, 0, 1.5, 0.01, "", "metallic ring amount"),
            P("wet", 0.07, 0, 0.5, 0.01, "", "room amount"),
            SEED(114),
        ])
def switch(*, f1, f2, gap, ring, wet, seed):
    rng = _rng(seed)

    def part(f, amp):
        t = _tr(0.18)
        r = tone(f, t, [(1, 1.0, 0.035), (2.73, 0.4, 0.015), (4.4, 0.15, 0.008)], attack=0.0005)
        c = np.zeros_like(t)
        b = click_core(rng, bright=2600, thump=180, d=0.03)
        c[: len(b)] = b
        return release((ring * r + c) * amp, 0.05)
    st = place([(0.0, part(f1, 1.0)), (gap, part(f2, 0.75))], gap + 0.22)
    return finish(room(st, wet=wet))
