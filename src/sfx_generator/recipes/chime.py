"""Chimes: bell partial stacks in a small room (ding, success, the end chime)."""
import numpy as np

from ..blocks import _t, _tr, finish, norm, pan, place, reverb, room, tone, trim_tail
from ..schema import P, SEED, recipe

# Bell partials for the interface chimes: (ratio, amp, tau). Slightly inharmonic ratios are what make it a bell.
BELL = [(1, 1.0, 0.16), (2.0, 0.3, 0.09), (2.76, 0.22, 0.05), (5.4, 0.06, 0.025)]


def note(f, d=0.6, spec=BELL, attack=0.0015, decay=1.0):
    t = _tr(d)
    spec = [(r, a, tau * decay) for r, a, tau in spec]
    return tone(f, t, spec, attack=attack)


@recipe("ding", family="chime",
        doc="A bright two-note chime, f1 then f2 (C5 then G5): something is right.",
        tips="f1/f2 are the two notes (a fifth apart by default); gap the time between them; decay scales the "
             "bell's ring (keep tails under about 0.5 s where speech follows); wet the room.",
        params=[
            P("f1", 523.25, 100, 4000, 0.01, "Hz", "first note"),
            P("f2", 783.99, 100, 4000, 0.01, "Hz", "second note"),
            P("gap", 0.07, 0.0, 0.5, 0.005, "s", "time between the notes"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.14, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.7, 0.2, 3.0, 0.01, "s", "buffer length"),
            SEED(115),
        ])
def ding(*, f1, f2, gap, decay, wet, d, seed):
    st = place([(0.0, pan(note(f1, decay=decay) * 0.75, -0.15)), (gap, pan(note(f2, decay=decay), 0.15))], d)
    return finish(room(st, wet=wet, seconds=0.5))


@recipe("success", family="chime",
        doc="A rising four-note arpeggio (C6 E6 G6 C7), the last note ringing: a problem solved.",
        tips="f1..f4 are the notes (a major arpeggio by default); step is the time between notes; decay scales "
             "the ring; wet the room.",
        params=[
            P("f1", 1046.5, 200, 5000, 0.1, "Hz", "first note (C6)"),
            P("f2", 1318.5, 200, 5000, 0.1, "Hz", "second note (E6)"),
            P("f3", 1568.0, 200, 6000, 0.1, "Hz", "third note (G6)"),
            P("f4", 2093.0, 200, 8000, 0.1, "Hz", "last note (C7)"),
            P("step", 0.065, 0.02, 0.3, 0.005, "s", "time between notes"),
            P("note_d", 0.55, 0.15, 1.5, 0.01, "s", "each note's length"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.14, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.85, 0.3, 3.0, 0.01, "s", "buffer length"),
            SEED(116),
        ])
def success(*, f1, f2, f3, f4, step, note_d, decay, wet, d, seed):
    notes = [(f1, -0.3), (f2, -0.1), (f3, 0.1), (f4, 0.3)]
    parts = [(step * i, pan(note(f, note_d, decay=decay) * (0.7 + 0.1 * i), p)) for i, (f, p) in enumerate(notes)]
    return finish(room(place(parts, d), wet=wet, seconds=0.5))


@recipe("success_short", family="chime",
        doc="Two notes up a fourth, G6 then C7: a smaller win.",
        tips="f1/f2 are the notes; gap the time between; decay the ring; wet the room.",
        params=[
            P("f1", 1568.0, 200, 5000, 0.1, "Hz", "first note"),
            P("f2", 2093.0, 200, 6000, 0.1, "Hz", "second note"),
            P("gap", 0.06, 0.0, 0.4, 0.005, "s", "time between the notes"),
            P("note_d", 0.45, 0.15, 1.5, 0.01, "s", "each note's length"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            P("d", 0.55, 0.2, 3.0, 0.01, "s", "buffer length"),
            SEED(117),
        ])
def success_short(*, f1, f2, gap, note_d, decay, wet, d, seed):
    st = place([(0.0, pan(note(f1, note_d, decay=decay) * 0.75, -0.1)), (gap, pan(note(f2, note_d, decay=decay), 0.1))], d)
    return finish(room(st, wet=wet, seconds=0.4))


@recipe("end_chime", family="chime",
        doc="Three soft bell tones a fifth and an octave apart (C5, G5, C6) in a long room: the end card.",
        tips="f1..f3 are the notes; spacing the time between them; decay the ring (0.9 s on the fundamental by "
             "default); tail and wet the room. Longer and softer than the interface chimes.",
        params=[
            P("f1", 523.25, 100, 2000, 0.01, "Hz", "first note (C5)"),
            P("f2", 783.99, 100, 3000, 0.01, "Hz", "second note (G5)"),
            P("f3", 1046.5, 100, 4000, 0.01, "Hz", "third note (C6)"),
            P("spacing", 0.12, 0.0, 0.6, 0.005, "s", "time between the notes"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("tail", 1.6, 0.3, 4.0, 0.05, "s", "reverb length"),
            P("wet", 0.3, 0, 0.8, 0.01, "", "reverb amount"),
            P("d", 2.4, 0.5, 6.0, 0.05, "s", "buffer length"),
            SEED(9),
        ])
def end_chime(*, f1, f2, f3, spacing, decay, tail, wet, d, seed):
    t = _t(d)
    st = np.zeros((len(t), 2))
    notes = ((f1, 0.0, -0.3), (f2, spacing, 0.3), (f3, 2 * spacing, 0.0))
    for k, (f0, start, p) in enumerate(notes):
        tt = t - start
        on = tt >= 0
        x = np.zeros_like(t)
        for ratio, amp, dec in ((1, 1.0, 0.9 * decay), (2.01, 0.35, 0.5 * decay), (3.02, 0.15, 0.3 * decay),
                                (4.17, 0.08, 0.2 * decay)):
            x += amp * np.sin(2 * np.pi * f0 * ratio * tt) * np.exp(-np.maximum(tt, 0) / dec)
        x = np.where(on, x, 0.0) * np.clip(tt / 0.006, 0, 1)
        st += pan(x * (0.9 - 0.15 * k), p)
    st = reverb(st, seconds=tail, wet=wet, seed=seed, damp=8000)
    return norm(trim_tail(st))
