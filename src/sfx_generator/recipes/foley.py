"""Foley: a page turn, a stamp, a heartbeat, a clock."""
import numpy as np

from ..blocks import _rng, _tr, burst, env, finish, glide, lowpass, norm, osc, pan, pink, place, release, room, svf_bandpass, tone
from ..schema import I, P, SEED, recipe


@recipe("page_turn", family="foley",
        doc="A band-passed noise swish, low-mid, quick attack and slow fall: a page or card flips.",
        tips="f_start -> f_end is the band's slide; attack and tau the shape (longer tau = a bigger sheet); "
             "pan_from/pan_to the direction it moves.",
        params=[
            P("d", 0.35, 0.1, 1.5, 0.01, "s", "length"),
            P("f_start", 900, 200, 5000, 10, "Hz", "band at the start"),
            P("f_end", 400, 100, 4000, 10, "Hz", "band at the end"),
            P("attack", 0.02, 0.002, 0.2, 0.001, "s", "attack"),
            P("tau", 0.12, 0.02, 0.6, 0.005, "s", "decay"),
            P("pan_from", -0.3, -1, 1, 0.05, "", "pan at the start"),
            P("pan_to", 0.3, -1, 1, 0.05, "", "pan at the end"),
            SEED(221),
        ])
def page_turn(*, d, f_start, f_end, attack, tau, pan_from, pan_to, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    fc = np.exp(np.linspace(np.log(f_start), np.log(f_end), n))
    x = svf_bandpass(svf_bandpass(pink(n, rng), fc, 0.9), fc * 1.6, 1.2) * env(t, attack, tau)
    st = pan(x, np.linspace(pan_from, pan_to, n))
    return finish(st)


@recipe("stamp", family="foley",
        doc="A low thump with a paper slap: a label stamped on, approved.",
        tips="thump_hz is the thump's pitch (lower = heavier); slap the paper's amount; wet the room.",
        params=[
            P("thump_hz", 160, 50, 500, 1, "Hz", "thump start pitch"),
            P("slap", 0.6, 0, 1.5, 0.01, "", "paper slap amount"),
            P("tau", 0.05, 0.01, 0.3, 0.001, "s", "thump decay"),
            P("wet", 0.08, 0, 0.5, 0.01, "", "room amount"),
            SEED(222),
        ])
def stamp(*, thump_hz, slap, tau, wet, seed):
    rng = _rng(seed)
    t = _tr(0.22)
    th = osc(glide(thump_hz, thump_hz * 0.45, t, 0.03), t) * env(t, 0.002, tau)
    s = np.zeros_like(t)
    b = burst(0.03, rng, lo=700, hi=4500, tau=0.006) * slap
    s[: len(b)] = b
    body = svf_bandpass(pink(len(t), rng), 420, 1.2) * env(t, 0.001, 0.025) * 0.5
    return finish(room(pan(th + s + body, 0.0), wet=wet))


def _heart_thump(rng, pitch, knock, body, decay, amp):
    t = _tr(0.35)
    n = len(t)
    x = (osc(glide(pitch * 1.6, pitch * 0.6, t, 0.045), t) + 0.4 * osc(glide(pitch * 3.2, pitch * 1.2, t, 0.045), t)) * env(t, 0.003, decay)
    k = np.zeros(n)
    kb = svf_bandpass(burst(0.03, rng, tau=0.012), 420, 0.9) * env(_tr(0.03), 0.0005, 0.012) * knock * 2.2
    k[: len(kb)] = kb
    b = svf_bandpass(pink(n, rng), 170, 1.2) * env(t, 0.002, 0.06) * body * 1.3
    return release(lowpass(x + k + b, 2500, 2) * amp, 0.05)


@recipe("heartbeat", family="foley",
        doc="Two thumps, lub-dub: a pulse, tension, something alive. Built to be heard on small speakers.",
        tips="f is the thump pitch; knock the valve snap in the mids (what makes it audible on a laptop); body the "
             "chest resonance around 170 Hz; gap the time from lub to dub; tau the decay. Repeat every 0.8-1 s for "
             "a resting pulse, faster for fear.",
        params=[
            P("f", 110, 40, 250, 1, "Hz", "thump pitch"),
            P("knock", 0.9, 0, 2, 0.05, "", "mid-range valve knock amount"),
            P("body", 0.8, 0, 2, 0.05, "", "chest body amount (170 Hz band)"),
            P("gap", 0.28, 0.1, 0.8, 0.005, "s", "time from lub to dub"),
            P("tau", 0.1, 0.02, 0.4, 0.005, "s", "thump decay"),
            P("d", 0.8, 0.4, 2.0, 0.01, "s", "length"),
            SEED(223),
        ])
def heartbeat(*, f, knock, body, gap, tau, d, seed):
    rng = _rng(seed)
    st = place([(0.0, _heart_thump(rng, f, knock, body, tau, 1.0)), (gap, _heart_thump(rng, f * 1.15, knock, body, tau * 0.65, 0.75))], d)
    return finish(st)


@recipe("heartbeat_loop", family="foley",
        doc="A beating heart at a steady pulse, lub-dub after lub-dub; a seamless loop (each beat ends before the next).",
        tips="bpm is the pulse (60-70 resting, 110-140 fear); beats how many fit in the loop; knock and body as for "
             "heartbeat; gap the time from lub to dub; f the pitch. The loop length is beats x 60 / bpm.",
        params=[
            P("bpm", 72, 40, 180, 1, "/min", "beats per minute"),
            I("beats", 4, 1, 16, "", "beats in the loop"),
            P("f", 110, 40, 250, 1, "Hz", "thump pitch"),
            P("knock", 0.9, 0, 2, 0.05, "", "mid-range valve knock amount"),
            P("body", 0.8, 0, 2, 0.05, "", "chest body amount (170 Hz band)"),
            P("gap", 0.28, 0.1, 0.6, 0.005, "s", "time from lub to dub"),
            P("tau", 0.1, 0.02, 0.4, 0.005, "s", "thump decay"),
            SEED(224),
        ])
def heartbeat_loop(*, bpm, beats, f, knock, body, gap, tau, seed):
    rng = _rng(seed)
    period = 60.0 / bpm
    parts = []
    for i in range(beats):
        t0 = i * period
        parts.append((t0, _heart_thump(rng, f, knock, body, tau, 1.0 * rng.uniform(0.96, 1.0))))
        parts.append((t0 + gap, _heart_thump(rng, f * 1.15, knock, body, tau * 0.65, 0.75 * rng.uniform(0.96, 1.0))))
    st = place(parts, beats * period)
    return norm(lowpass(st, 15000, 2))


@recipe("tick_tock", family="foley",
        doc="Alternating woodblock ticks at two pitches: a clock, time passing.",
        tips="f1/f2 are the two woods; interval the time between ticks; count how many. Half-second intervals "
             "read as a clock; faster reads as a timer.",
        params=[
            P("f1", 1400, 300, 5000, 10, "Hz", "first wood pitch"),
            P("f2", 1100, 300, 5000, 10, "Hz", "second wood pitch"),
            P("interval", 0.4, 0.1, 1.5, 0.01, "s", "time between ticks"),
            I("count", 4, 1, 16, "", "number of ticks"),
            SEED(224),
        ])
def tick_tock(*, f1, f2, interval, count, seed):
    rng = _rng(seed)

    def wood(f):
        t = _tr(0.09)
        x = tone(f, t, [(1, 1.0, 0.018), (2.4, 0.3, 0.01), (4.1, 0.1, 0.006)], attack=0.0008)
        c = np.zeros_like(t)
        b = burst(0.008, rng, lo=600, hi=5000, tau=0.002) * 0.4
        c[: len(b)] = b
        return x + c
    parts = [(i * interval, pan(wood(f1 if i % 2 == 0 else f2), -0.15 if i % 2 == 0 else 0.15)) for i in range(count)]
    return finish(room(place(parts, (count - 1) * interval + 0.12), wet=0.08))
