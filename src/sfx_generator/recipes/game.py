"""Game-like rewards and zaps: coin, level_up, zap."""
import numpy as np

from ..blocks import _tr, env, finish, lowpass, norm, osc, pan, place, release, room, saw, svf_bandpass, trim_tail
from ..schema import I, P, SEED, recipe
from .chime import note
from .shimmer import shimmer_core


@recipe("coin", family="game",
        doc="Two quick high square-ish notes, the second ringing: a point scored, a reward collected.",
        tips="f1/f2 are the notes (B5 -> E6 by default, a fourth up); gap the time between; lowpass_hz the "
             "brightness of the square; decay the second note's ring.",
        params=[
            P("f1", 987.77, 200, 5000, 0.01, "Hz", "first note (B5)"),
            P("f2", 1318.5, 200, 6000, 0.01, "Hz", "second note (E6)"),
            P("gap", 0.07, 0.02, 0.3, 0.005, "s", "time between the notes"),
            P("lowpass_hz", 6000, 1000, 15000, 50, "Hz", "square low-pass"),
            P("decay", 0.18, 0.05, 1.0, 0.005, "s", "second note decay"),
            SEED(231),
        ])
def coin(*, f1, f2, gap, lowpass_hz, decay, seed):
    def sq(f, d, tau):
        t = _tr(d)
        ph = 2 * np.pi * f * t
        x = np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5 + 0.3 * np.sin(2 * ph)
        return release(lowpass(x, lowpass_hz, 2) * env(t, 0.002, tau), 0.03)
    st = place([(0.0, pan(sq(f1, gap + 0.02, 0.06) * 0.85, 0.0)), (gap, pan(sq(f2, decay * 3, decay), 0.0))],
               gap + decay * 3 + 0.02)
    return finish(room(st, wet=0.08))


@recipe("level_up", family="game",
        doc="A fast rising five-note arpeggio with a shimmer on top: a milestone, bigger than success.",
        tips="root sets the key; step the time between notes; sparkle the shimmer amount; decay the ring.",
        params=[
            P("root", 1046.5, 200, 4000, 0.1, "Hz", "first note (C6)"),
            P("step", 0.05, 0.02, 0.2, 0.005, "s", "time between notes"),
            P("note_d", 0.5, 0.15, 1.5, 0.01, "s", "each note's length"),
            P("decay", 1.1, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("sparkle", 0.25, 0, 1, 0.01, "", "shimmer amount"),
            P("wet", 0.16, 0, 0.5, 0.01, "", "room amount"),
            SEED(232),
        ])
def level_up(*, root, step, note_d, decay, sparkle, wet, seed):
    ratios = [1.0, 1.25, 1.5, 2.0, 2.5]
    pans = [-0.3, -0.15, 0.0, 0.15, 0.3]
    parts = [(step * i, pan(note(root * r, note_d, decay=decay) * (0.65 + 0.08 * i), p))
             for i, (r, p) in enumerate(zip(ratios, pans))]
    st = room(place(parts, 4 * step + note_d + 0.05), wet=wet, seconds=0.6)
    sp = shimmer_core(1.2, seed, 8, 3000, 8000, 0.35) * sparkle
    n = max(len(st), len(sp))
    out = np.zeros((n, 2))
    out[: len(st)] += st
    out[: len(sp)] += sp
    return finish(out)


@recipe("zap", family="game",
        doc="A fast downward sweep of a filtered saw: a laser, an electric hit.",
        tips="f_start -> f_end is the sweep; d its length; q the filter's bite; tau the decay.",
        params=[
            P("d", 0.2, 0.05, 1.0, 0.005, "s", "length"),
            P("f_start", 2400, 300, 10000, 10, "Hz", "sweep start"),
            P("f_end", 180, 40, 3000, 1, "Hz", "sweep end"),
            P("q", 1.4, 0.4, 6, 0.05, "", "filter narrowness"),
            P("tau", 0.08, 0.02, 0.5, 0.005, "s", "decay"),
            SEED(233),
        ])
def zap(*, d, f_start, f_end, q, tau, seed):
    t = _tr(d)
    n = len(t)
    f = np.exp(np.linspace(np.log(f_start), np.log(f_end), n))
    x = saw(f, t, 10)
    x = svf_bandpass(x, f * 1.5, q) + 0.35 * x
    x = x * env(t, 0.001, tau)
    return finish(pan(release(x, 0.02), 0.0))
