"""Notifications, alarms, countdowns and the fail motif: short tonal signals."""
import numpy as np

from ..blocks import _tr, env, finish, lowpass, osc, pan, place, release, room, tone
from ..schema import I, P, SEED, recipe
from .chime import BELL, note
from .question import SOFT


@recipe("notify", family="notify",
        doc="A two-tone notification: bell partials, the second note a third up.",
        tips="f1/f2 are the two notes (a major third by default; a fifth is brighter, a minor third softer); gap "
             "the time between; decay the ring; wet the room.",
        params=[
            P("f1", 1046.5, 200, 5000, 0.1, "Hz", "first note (C6)"),
            P("f2", 1318.5, 200, 6000, 0.1, "Hz", "second note (E6)"),
            P("gap", 0.09, 0.0, 0.5, 0.005, "s", "time between the notes"),
            P("note_d", 0.5, 0.15, 1.5, 0.01, "s", "each note's length"),
            P("decay", 0.9, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            SEED(201),
        ])
def notify(*, f1, f2, gap, note_d, decay, wet, seed):
    st = place([(0.0, pan(note(f1, note_d, BELL, decay=decay) * 0.8, -0.12)),
                (gap, pan(note(f2, note_d, BELL, decay=decay), 0.12))], gap + note_d + 0.02)
    return finish(room(st, wet=wet, seconds=0.45))


@recipe("alarm", family="notify",
        doc="An alternating two-tone square, low-passed: a warning that wants attention.",
        tips="f1/f2 are the alternating tones; period the time per tone; cycles how many pairs; lowpass_hz the "
             "harshness (lower = softer); decay fades the whole thing out.",
        params=[
            P("f1", 880, 100, 4000, 1, "Hz", "high tone"),
            P("f2", 660, 100, 4000, 1, "Hz", "low tone"),
            P("period", 0.12, 0.04, 0.5, 0.005, "s", "time per tone"),
            I("cycles", 3, 1, 12, "", "number of high-low pairs"),
            P("lowpass_hz", 2400, 400, 10000, 50, "Hz", "square low-pass"),
            P("decay", 0.6, 0.1, 5.0, 0.05, "s", "overall decay"),
            SEED(202),
        ])
def alarm(*, f1, f2, period, cycles, lowpass_hz, decay, seed):
    t = _tr(period)
    parts = []
    for k in range(cycles):
        for j, f in enumerate((f1, f2)):
            start = (2 * k + j) * period
            ph = 2 * np.pi * f * t
            sq = np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5
            x = lowpass(sq, lowpass_hz, 2) * env(t, 0.004, period * 0.6) * np.exp(-start / decay)
            parts.append((start, release(x, 0.015)))
    st = place(parts, 2 * cycles * period + 0.05)
    return finish(st)


@recipe("countdown", family="notify",
        doc="Three short beeps and a higher, longer fourth: three, two, one, go. Ends on the cue.",
        tips="f is the beep pitch and f_go the last one's; interval the time between beeps; beep_d their length; "
             "the last beep rings longer. Lead = the whole length, so 'go' lands on the cue.",
        params=[
            P("f", 880, 200, 4000, 1, "Hz", "beep pitch"),
            P("f_go", 1760, 200, 6000, 1, "Hz", "final beep pitch"),
            P("interval", 0.25, 0.1, 1.0, 0.01, "s", "time between beeps"),
            P("beep_d", 0.07, 0.03, 0.3, 0.005, "s", "short beep length"),
            P("go_d", 0.3, 0.1, 1.0, 0.01, "s", "final beep length"),
            SEED(203),
        ])
def countdown(*, f, f_go, interval, beep_d, go_d, seed):
    def beep(freq, d, tau):
        t = _tr(d)
        return release((osc(freq, t) + 0.15 * osc(2 * freq, t)) * env(t, 0.003, tau), 0.02)
    parts = [(i * interval, beep(f, beep_d, beep_d) * 0.8) for i in range(3)]
    parts.append((3 * interval, beep(f_go, go_d, go_d * 0.5)))
    st = place(parts, 3 * interval + go_d + 0.02)
    return finish(room(st, wet=0.06))


@recipe("fail", family="notify",
        doc="Three soft descending notes: a gentle 'no', softer than error.",
        tips="f1..f3 are the notes (E5, C5, A4 by default); step the time between; decay the ring. A smaller "
             "fall is sadder, a bigger one more comic.",
        params=[
            P("f1", 659.25, 100, 3000, 0.01, "Hz", "first note"),
            P("f2", 523.25, 100, 3000, 0.01, "Hz", "second note"),
            P("f3", 415.3, 80, 3000, 0.01, "Hz", "third note"),
            P("step", 0.14, 0.05, 0.5, 0.005, "s", "time between notes"),
            P("note_d", 0.32, 0.1, 1.0, 0.01, "s", "each note's length"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("wet", 0.1, 0, 0.5, 0.01, "", "room amount"),
            SEED(204),
        ])
def fail(*, f1, f2, f3, step, note_d, decay, wet, seed):
    spec = [(r, a, tau * decay) for r, a, tau in SOFT]
    parts = [(i * step, pan(tone(f, _tr(note_d), spec, attack=0.005) * (0.8 + 0.1 * i), p))
             for i, (f, p) in enumerate(((f1, -0.1), (f2, 0.0), (f3, 0.1)))]
    return finish(room(place(parts, 2 * step + note_d + 0.02), wet=wet))
