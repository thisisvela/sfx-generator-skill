"""World and character: doors, tools, footsteps, jumps, magic, fire, horns and drums."""
import numpy as np

from ..blocks import (SR, _rng, _tr, burst, env, fade, finish, glide, highpass, loop_seam, lowpass, norm, osc, pan,
                      pink, place, release, reverb, saw, square, svf_bandpass, tone, trim_tail, white)
from ..schema import I, P, SEED, recipe
from .chime import BELL, note
from .shimmer import shimmer_core


# ---- magic ---------------------------------------------------------------------------------------------------
@recipe("spell_cast", family="world",
        doc="A spell: a rising tone with vibrato under a cloud of sparkle, in a bright reverb.",
        tips="f_start -> f_end is the rise; d its length; sparkle the shimmer amount; vibrato_hz the wobble.",
        params=[
            P("d", 1.1, 0.4, 3.0, 0.05, "s", "length"),
            P("f_start", 320, 80, 2000, 1, "Hz", "rise start"),
            P("f_end", 2200, 300, 8000, 1, "Hz", "rise end"),
            P("vibrato_hz", 7, 2, 20, 0.5, "Hz", "vibrato rate"),
            P("sparkle", 0.5, 0, 1.5, 0.05, "", "shimmer amount"),
            P("wet", 0.35, 0, 0.8, 0.01, "", "reverb amount"),
            SEED(341),
        ])
def spell_cast(*, d, f_start, f_end, vibrato_hz, sparkle, wet, seed):
    t = _tr(d)
    s = t / d
    f = np.exp(np.log(f_start) + (np.log(f_end) - np.log(f_start)) * s ** 1.4) * (1 + 0.012 * np.sin(2 * np.pi * vibrato_hz * t))
    x = (osc(f, t) + 0.3 * osc(2 * f, t) + 0.12 * osc(3 * f, t)) * np.sin(np.pi * s) ** 0.8
    st = pan(release(x, 0.08), 0.0)
    sp = shimmer_core(d + 0.6, seed, 16, 2000, 7000, d * 0.8) * sparkle
    n = max(len(st), len(sp))
    out = np.zeros((n, 2))
    out[: len(st)] += st
    out[: len(sp)] += sp
    return norm(trim_tail(reverb(out, seconds=1.2, wet=wet, seed=seed + 1, damp=9000)))


@recipe("fireball", family="world",
        doc="A fireball: a low whoosh with crackle that builds and lands in a soft boom. Ends on the cue.",
        tips="d is the flight (lead = d so the boom lands on the cue); crackle the fire's amount; boom the impact.",
        params=[
            P("d", 0.9, 0.3, 3.0, 0.05, "s", "flight length"),
            P("crackle", 0.6, 0, 1.5, 0.05, "", "crackle amount"),
            P("boom", 0.8, 0, 2, 0.05, "", "impact amount"),
            SEED(342),
        ])
def fireball(*, d, crackle, boom, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    s = t / d
    fc = np.exp(np.interp(s, [0, 1], np.log([220, 1100])))
    wh = svf_bandpass(pink(n, rng), fc, 0.9) * s ** 1.3 * 2.0
    cr = np.zeros(n)
    for _ in range(int(40 * d)):
        a = int(rng.uniform(0, d - 0.02) * SR)
        bb = burst(rng.uniform(0.003, 0.01), rng, lo=1500, hi=7000, tau=0.0015) * rng.uniform(0.2, 0.8) * crackle
        cr[a:a + len(bb)] += bb[: n - a]
    cr *= 0.3 + 0.7 * s
    tb = _tr(0.6)
    bm = (osc(glide(90, 38, tb, 0.05), tb) * env(tb, 0.003, 0.3) + lowpass(white(len(tb), rng), 1200, 2) * env(tb, 0.001, 0.08) * 0.8) * boom
    st = place([(0.0, pan(wh + cr, np.linspace(-0.4, 0.2, n))), (d - 0.02, pan(bm, 0.0))], d + 0.6)
    return norm(trim_tail(reverb(st, seconds=0.9, wet=0.2, seed=seed + 1, damp=3500)))


@recipe("heal", family="world",
        doc="A heal: three soft ascending bell notes with slow attacks and a gentle sparkle.",
        tips="root sets the key; step the time between notes; sparkle the shimmer; attack softens the onsets.",
        params=[
            P("root", 1046.5, 200, 4000, 0.1, "Hz", "first note (C6)"),
            P("step", 0.16, 0.05, 0.5, 0.005, "s", "time between notes"),
            P("attack", 0.02, 0.002, 0.1, 0.001, "s", "note attack"),
            P("sparkle", 0.3, 0, 1, 0.05, "", "shimmer amount"),
            P("wet", 0.25, 0, 0.6, 0.01, "", "reverb amount"),
            SEED(343),
        ])
def heal(*, root, step, attack, sparkle, wet, seed):
    ratios = [1.0, 1.25, 1.5]
    parts = [(step * i, pan(note(root * r, 0.8, BELL, attack=attack, decay=1.6) * (0.7 + 0.1 * i), p))
             for i, (r, p) in enumerate(zip(ratios, (-0.2, 0.0, 0.2)))]
    st = place(parts, 2 * step + 0.85)
    sp = shimmer_core(1.3, seed, 8, 3000, 8000, 0.6) * sparkle
    n = max(len(st), len(sp))
    out = np.zeros((n, 2))
    out[: len(st)] += st
    out[: len(sp)] += sp
    return norm(trim_tail(reverb(out, seconds=1.2, wet=wet, seed=seed + 1, damp=9000)))


@recipe("power_up", family="world",
        doc="A power-up: a quick rising run of eight square notes up the scale, the last one ringing.",
        tips="root sets the key; step the speed; lowpass_hz the square's brightness.",
        params=[
            P("root", 523.25, 100, 2000, 0.01, "Hz", "first note (C5)"),
            P("step", 0.045, 0.02, 0.15, 0.005, "s", "time between notes"),
            P("lowpass_hz", 5000, 1000, 15000, 50, "Hz", "square low-pass"),
            SEED(344),
        ])
def power_up(*, root, step, lowpass_hz, seed):
    ratios = [1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3, 15 / 8, 2]
    parts = []
    for i, r in enumerate(ratios):
        last = i == len(ratios) - 1
        t = _tr(0.35 if last else step * 1.4)
        x = lowpass(square(root * r, t, 6), lowpass_hz, 2) * env(t, 0.002, 0.2 if last else step)
        parts.append((i * step, pan(release(x, 0.02), 0.0) * (0.6 + 0.05 * i)))
    return finish(reverb(place(parts, 7 * step + 0.4), seconds=0.4, wet=0.1, seed=seed + 1, damp=7000))


# ---- fire --------------------------------------------------------------------------------------------------------
@recipe("burning_wood", family="world",
        doc="A wood fire: a low roar that breathes, with seeded crackles and pops; a seamless loop.",
        tips="crackle is how many pops per second; roar the low bed; d the loop length.",
        params=[
            P("d", 6.0, 2.0, 16.0, 0.5, "s", "loop length (before the seam crossfade)"),
            I("crackle", 10, 1, 60, "/s", "crackles per second"),
            P("roar", 1.0, 0, 2, 0.05, "", "low roar amount"),
            SEED(345),
        ])
def burning_wood(*, d, crackle, roar, seed):
    rng = _rng(seed)
    n = int(round(SR * d))
    t = np.arange(n) / SR
    breathe = 0.7 + 0.3 * np.sin(2 * np.pi * 2 * t / d) * np.sin(2 * np.pi * 3 * t / d + 1.0)
    bed = np.stack([lowpass(pink(n, rng), 500, 1), lowpass(pink(n, rng), 520, 1)], axis=1) * breathe[:, None] * roar * 0.9
    pops = np.zeros((n, 2))
    for _ in range(int(crackle * d)):
        a = int(rng.uniform(0, d) * SR)
        ln = rng.uniform(0.003, 0.02)
        bb = burst(ln, rng, lo=rng.uniform(800, 2500), hi=rng.uniform(4000, 9000), tau=ln * 0.4) * rng.uniform(0.15, 1.0)
        if rng.uniform() < 0.25:                      # the odd deeper pop
            tt = _tr(ln + 0.02)
            bb = np.concatenate([bb, np.zeros(len(tt) - len(bb))]) + osc(rng.uniform(150, 400), tt) * env(tt, 0.0005, 0.01) * 0.6
        b = min(n, a + len(bb))
        pops[a:b] += pan(bb[: b - a], rng.uniform(-0.6, 0.6))
    st = bed + pops * 0.8
    return norm(loop_seam(st, 0.3))


# ---- doors ---------------------------------------------------------------------------------------------------
def _creak(rng, d, f0, f1, wobble, seed):
    t = _tr(d)
    n = len(t)
    walk = np.cumsum(rng.normal(0, 1, n))
    walk = walk / (np.abs(walk).max() + 1e-9)
    f = np.exp(np.linspace(np.log(f0), np.log(f1), n)) * (1 + wobble * 0.08 * walk + 0.01 * np.sin(2 * np.pi * 9 * t))
    x = saw(f, t, 8) * 0.6 + square(f, t, 4) * 0.2
    x = svf_bandpass(x, f * 2.2, 1.5) + 0.35 * x
    stick = 0.75 + 0.25 * np.clip(np.sin(2 * np.pi * (14 + 6 * walk) * t) * 3, -1, 1)   # stick-slip grain
    return x * stick


@recipe("door_open", family="world",
        doc="A door opens: a latch click, a slow creak of the hinge, and a soft stop.",
        tips="d is the creak's length; f0 -> f1 the hinge's pitch travel; wobble its unevenness; latch the "
             "click at the start.",
        params=[
            P("d", 0.9, 0.3, 3.0, 0.05, "s", "creak length"),
            P("f0", 160, 60, 800, 1, "Hz", "hinge pitch at the start"),
            P("f1", 240, 60, 1200, 1, "Hz", "hinge pitch at the end"),
            P("wobble", 0.6, 0, 1.5, 0.05, "", "hinge unevenness"),
            P("latch", 0.8, 0, 1.5, 0.05, "", "latch click amount"),
            SEED(346),
        ])
def door_open(*, d, f0, f1, wobble, latch, seed):
    rng = _rng(seed)
    cr = _creak(rng, d, f0, f1, wobble, seed)
    t = _tr(d)
    cr = cr * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7 * 0.5
    tl = _tr(0.05)
    lt = (burst(0.012, rng, lo=1500, hi=7000, tau=0.002) * 1.2)
    lt = np.concatenate([lt, np.zeros(len(tl) - len(lt))]) + 0.5 * osc(1300, tl) * env(tl, 0.0005, 0.006)
    ts = _tr(0.2)
    stop = np.zeros(len(ts))
    sb = lowpass(burst(0.03, rng, hi=1500, tau=0.01), 1500, 2) * 0.8
    stop[: len(sb)] = sb
    stop += osc(glide(140, 90, ts, 0.03), ts) * env(ts, 0.002, 0.05) * 0.6
    st = place([(0.0, pan(lt * latch, -0.2)), (0.08, pan(cr, 0.0)), (d + 0.05, pan(release(stop, 0.05), 0.1))], d + 0.3)
    return finish(reverb(st, seconds=0.6, wet=0.12, seed=seed + 1, damp=5000))


@recipe("door_knock", family="world",
        doc="Knocking on a wooden door: three knocks, each a knuckle tap with a wooden body.",
        tips="count is the number of knocks; interval the time between; f the wood's pitch (lower = heavier door).",
        params=[
            I("count", 3, 1, 8, "", "number of knocks"),
            P("interval", 0.22, 0.1, 0.6, 0.005, "s", "time between knocks"),
            P("f", 180, 80, 500, 1, "Hz", "wood pitch"),
            SEED(347),
        ])
def door_knock(*, count, interval, f, seed):
    rng = _rng(seed)
    parts = []
    for i in range(count):
        t = _tr(0.14)
        x = tone(f, t, [(1, 1.0, 0.04), (2.6, 0.35, 0.02), (4.1, 0.15, 0.01)], attack=0.0008)
        c = np.zeros_like(t)
        b = burst(0.01, rng, lo=500, hi=4000, tau=0.003) * 0.7
        c[: len(b)] = b
        parts.append((i * interval, (x + c) * rng.uniform(0.8, 1.0)))
    return finish(reverb(place(parts, (count - 1) * interval + 0.2), seconds=0.5, wet=0.1, seed=seed + 1, damp=5000))


@recipe("door_squeak", family="world",
        doc="A squeaky hinge: a long wavering squeal, high and uneven.",
        tips="d is the length; f0 -> f1 the squeal's travel; wobble its waver.",
        params=[
            P("d", 1.0, 0.3, 3.0, 0.05, "s", "length"),
            P("f0", 1300, 300, 4000, 10, "Hz", "squeal start"),
            P("f1", 2100, 300, 6000, 10, "Hz", "squeal end"),
            P("wobble", 1.0, 0, 2, 0.05, "", "waver"),
            SEED(348),
        ])
def door_squeak(*, d, f0, f1, wobble, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    walk = np.cumsum(rng.normal(0, 1, n))
    walk = walk / (np.abs(walk).max() + 1e-9)
    f = np.exp(np.linspace(np.log(f0), np.log(f1), n)) * (1 + wobble * 0.06 * walk + 0.006 * np.sin(2 * np.pi * 11 * t))
    x = (osc(f, t) + 0.5 * osc(2 * f, t) + 0.2 * osc(3 * f, t)) * np.sin(np.pi * t / d) ** 0.6
    x *= 0.8 + 0.2 * np.sin(2 * np.pi * (18 + 8 * walk) * t)
    return finish(reverb(pan(x, 0.1), seconds=0.5, wet=0.1, seed=seed + 1, damp=6000))


@recipe("door_slam", family="world",
        doc="A door slams: a heavy thud, a wooden body, a rattle of the frame and a short room.",
        tips="f the thud's pitch (lower = heavier); rattle the frame's ticks; wet the room.",
        params=[
            P("f", 85, 40, 250, 1, "Hz", "thud pitch"),
            P("rattle", 0.6, 0, 1.5, 0.05, "", "frame rattle amount"),
            P("wet", 0.18, 0, 0.6, 0.01, "", "room amount"),
            SEED(349),
        ])
def door_slam(*, f, rattle, wet, seed):
    rng = _rng(seed)
    t = _tr(0.5)
    n = len(t)
    th = osc(glide(f, f * 0.45, t, 0.03), t) * env(t, 0.002, 0.12)
    body = lowpass(white(n, rng), 1400, 2) * env(t, 0.001, 0.05) * 1.1
    wood = tone(230, t, [(1, 0.6, 0.05), (2.5, 0.3, 0.025), (4.3, 0.12, 0.012)], attack=0.0005)
    rt = np.zeros(n)
    for _ in range(9):
        a = int(rng.uniform(0.03, 0.3) * SR)
        bb = burst(rng.uniform(0.004, 0.01), rng, lo=700, hi=5000, tau=0.002) * rng.uniform(0.2, 0.7) * rattle
        rt[a:a + len(bb)] += bb[: n - a]
    return finish(reverb(pan(th + body + wood + rt, 0.0), seconds=0.7, wet=wet, seed=seed + 1, damp=4000))


# ---- tools -------------------------------------------------------------------------------------------------------
@recipe("hammer", family="world",
        doc="A hammer on a nail: a hard tap, a bright ring, a wooden body underneath.",
        tips="ring_hz is the nail's pitch; wood the body's amount; count the number of blows; interval between them.",
        params=[
            I("count", 1, 1, 6, "", "number of blows"),
            P("interval", 0.5, 0.15, 1.5, 0.01, "s", "time between blows"),
            P("ring_hz", 3300, 800, 8000, 10, "Hz", "nail ring pitch"),
            P("wood", 0.7, 0, 1.5, 0.05, "", "wooden body amount"),
            SEED(350),
        ])
def hammer(*, count, interval, ring_hz, wood, seed):
    rng = _rng(seed)
    parts = []
    for i in range(count):
        t = _tr(0.22)
        r = tone(ring_hz, t, [(1, 1.0, 0.05), (1.6, 0.4, 0.03), (2.9, 0.2, 0.015)], attack=0.0003)
        w = tone(210, t, [(1, 1.0, 0.03), (2.4, 0.3, 0.015)], attack=0.0005) * wood
        c = np.zeros_like(t)
        b = burst(0.008, rng, lo=1000, hi=9000, tau=0.0015) * 1.3
        c[: len(b)] = b
        parts.append((i * interval, (r + w + c) * rng.uniform(0.85, 1.0)))
    return finish(reverb(place(parts, (count - 1) * interval + 0.3), seconds=0.4, wet=0.08, seed=seed + 1, damp=7000))


@recipe("blacksmith", family="world",
        doc="A smith at the anvil: hammer blows on steel. Each blow is a hard clank, a very short high ping off the "
            "anvil, and the iron's own vibration, a buzzing beat that fades. Not a bell: nothing rings in tune.",
        tips="count is the number of blows; interval the rhythm (a smith is steady, with a little drift); ting_hz "
             "the anvil's ping (high, short), ting its amount; buzz_hz the iron's vibration pitch, buzz its amount, "
             "beat how fast it throbs, decay how long it fades; wet the room.",
        params=[
            I("count", 4, 1, 12, "", "number of blows"),
            P("interval", 0.45, 0.15, 1.5, 0.01, "s", "time between blows"),
            P("ting_hz", 3600, 1500, 8000, 10, "Hz", "anvil ping pitch"),
            P("ting", 0.6, 0, 1.5, 0.05, "", "anvil ping amount"),
            P("buzz_hz", 620, 150, 2000, 10, "Hz", "iron vibration pitch"),
            P("buzz", 1.0, 0, 2, 0.05, "", "iron vibration amount"),
            P("beat", 24, 4, 80, 1, "Hz", "vibration throb rate"),
            P("decay", 0.35, 0.08, 1.2, 0.01, "s", "vibration fade"),
            P("wet", 0.2, 0, 0.6, 0.01, "", "room amount"),
            SEED(351),
        ])
def blacksmith(*, count, interval, ting_hz, ting, buzz_hz, buzz, beat, decay, wet, seed):
    rng = _rng(seed)
    parts = []
    t0 = 0.0
    for i in range(count):
        t = _tr(max(0.3, decay * 2.2))
        n = len(t)
        # the clank: the hammer face on steel, and the mass of the blow behind it
        c = np.zeros(n)
        b = burst(0.004, rng, lo=1500, hi=12000, tau=0.0012) * 1.6
        c[: len(b)] = b
        knock = svf_bandpass(white(n, rng), 700, 1.0) * env(t, 0.0003, 0.012)
        # the anvil's ping: a tight inharmonic cluster above 3 kHz, gone in a tenth of a second
        f = ting_hz * rng.uniform(0.97, 1.03)
        ping = tone(f, t, [(1, 1.0, 0.09), (1.02, 0.6, 0.07), (1.37, 0.4, 0.05), (1.71, 0.25, 0.04)], attack=0.0002) * ting
        # the iron's vibration: close partial pairs beating against each other, a little saturated, fading
        fb = buzz_hz * rng.uniform(0.96, 1.04)
        vib = ((osc(fb, t) + osc(fb + beat, t))
               + 0.5 * (osc(fb * 2.01, t) + osc(fb * 2.01 + beat * 1.3, t))
               + 0.3 * (osc(fb * 3.2, t) + osc(fb * 3.2 + beat * 0.7, t)))
        vib = np.tanh(1.6 * vib) * env(t, 0.001, decay) * 0.45 * buzz
        blow = highpass(c + knock + ping + vib, 100, 2) * rng.uniform(0.85, 1.0)
        parts.append((t0, pan(release(blow, 0.03), rng.uniform(-0.1, 0.1))))
        t0 += interval * rng.uniform(0.96, 1.04)             # a smith is steady, with a little drift
    return finish(reverb(place(parts, t0 - interval + max(0.3, decay * 2.2) + 0.1), seconds=1.1, wet=wet, seed=seed + 1, damp=5000))


# ---- movement ------------------------------------------------------------------------------------------------
def _step(rng, heavy, surface_hz):
    t = _tr(0.16)
    n = len(t)
    heel = lowpass(white(n, rng), surface_hz, 2) * env(t, 0.001, 0.025) * 1.0
    toe = np.zeros(n)
    b = lowpass(burst(0.03, rng, hi=surface_hz * 0.7, tau=0.012), surface_hz, 2) * 0.6
    a = int(0.06 * SR)
    toe[a:a + len(b)] += b[: n - a]
    body = osc(glide(110 * heavy, 60 * heavy, t, 0.02), t) * env(t, 0.001, 0.04) * 0.6 * heavy
    return heel + toe + body


@recipe("footstep", family="world",
        doc="One footstep: a heel, a toe and a little body, on a hard floor.",
        tips="surface_hz sets the floor (lower = softer ground, higher = tile); heavy the weight of the body.",
        params=[
            P("surface_hz", 1800, 300, 6000, 10, "Hz", "surface brightness"),
            P("heavy", 1.0, 0.3, 2.5, 0.05, "", "body weight"),
            SEED(352),
        ])
def footstep(*, surface_hz, heavy, seed):
    rng = _rng(seed)
    return finish(highpass(reverb(pan(_step(rng, heavy, surface_hz), 0.0), seconds=0.35, wet=0.08, seed=seed + 1, damp=5000), 70, 2))


@recipe("footsteps", family="world",
        doc="Walking: seeded steps at a steady pace, alternating left and right.",
        tips="count is the number of steps; interval the pace; surface_hz the floor; heavy the weight.",
        params=[
            I("count", 6, 2, 20, "", "number of steps"),
            P("interval", 0.42, 0.15, 1.2, 0.01, "s", "time between steps"),
            P("surface_hz", 1800, 300, 6000, 10, "Hz", "surface brightness"),
            P("heavy", 1.0, 0.3, 2.5, 0.05, "", "body weight"),
            SEED(353),
        ])
def footsteps(*, count, interval, surface_hz, heavy, seed):
    rng = _rng(seed)
    parts = [(i * interval + float(rng.uniform(0, 0.02)), pan(_step(rng, heavy, surface_hz * rng.uniform(0.9, 1.1)) * rng.uniform(0.75, 1.0),
                                                              -0.2 if i % 2 == 0 else 0.2)) for i in range(count)]
    return finish(highpass(reverb(place(parts, (count - 1) * interval + 0.3), seconds=0.35, wet=0.08, seed=seed + 1, damp=5000), 70, 2))


@recipe("jump", family="world",
        doc="A jump: a quick rising boing with a soft push of air.",
        tips="f0 -> f1 is the rise; d its length.",
        params=[
            P("f0", 280, 80, 1000, 1, "Hz", "start pitch"),
            P("f1", 900, 200, 3000, 1, "Hz", "end pitch"),
            P("d", 0.28, 0.1, 0.8, 0.005, "s", "length"),
            SEED(354),
        ])
def jump(*, f0, f1, d, seed):
    rng = _rng(seed)
    t = _tr(d)
    f = np.exp(np.linspace(np.log(f0), np.log(f1), len(t)))
    x = (osc(f, t) + 0.25 * osc(2 * f, t)) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7
    air = svf_bandpass(white(len(t), rng), f * 3, 1.0) * env(t, 0.01, d * 0.4) * 0.3
    return finish(pan(release(x + air, 0.04), 0.0))


@recipe("land", family="world",
        doc="Landing: a thump with a short scuff of dust.",
        tips="f the thump; scuff the dust's amount.",
        params=[
            P("f", 110, 40, 300, 1, "Hz", "thump pitch"),
            P("scuff", 0.5, 0, 1.5, 0.05, "", "dust amount"),
            SEED(355),
        ])
def land(*, f, scuff, seed):
    rng = _rng(seed)
    t = _tr(0.3)
    th = osc(glide(f, f * 0.5, t, 0.03), t) * env(t, 0.002, 0.07)
    body = lowpass(white(len(t), rng), 900, 2) * env(t, 0.001, 0.035) * 0.9
    sc = svf_bandpass(white(len(t), rng), 2200, 0.8) * env(t, 0.01, 0.08) * scuff * 0.5
    return finish(highpass(reverb(pan(th + body + sc, 0.0), seconds=0.35, wet=0.08, seed=seed + 1, damp=4000), 60, 2))


@recipe("chest_open", family="world",
        doc="A chest opens: a latch, a short creak of the lid, then a rising sparkle of treasure.",
        tips="creak is the lid's length; sparkle the treasure's amount.",
        params=[
            P("creak", 0.5, 0.2, 1.5, 0.05, "s", "lid creak length"),
            P("sparkle", 0.6, 0, 1.5, 0.05, "", "treasure sparkle amount"),
            SEED(356),
        ])
def chest_open(*, creak, sparkle, seed):
    rng = _rng(seed)
    cr = _creak(rng, creak, 120, 200, 0.5, seed)
    t = _tr(creak)
    cr = cr * np.sin(np.pi * np.clip(t / creak, 0, 1)) ** 0.8 * 0.4
    tl = _tr(0.05)
    lt = burst(0.01, rng, lo=1500, hi=7000, tau=0.002) * 1.2
    lt = np.concatenate([lt, np.zeros(len(tl) - len(lt))]) + 0.5 * osc(1500, tl) * env(tl, 0.0005, 0.006)
    notes = [(0.0, 1046.5), (0.07, 1318.5), (0.14, 1568.0), (0.21, 2093.0)]
    sp = [(creak + 0.05 + s, pan(note(f, 0.5, BELL, decay=0.9) * sparkle * 0.9, p)) for (s, f), p in zip(notes, (-0.3, -0.1, 0.1, 0.3))]
    st = place([(0.0, pan(lt, -0.1)), (0.06, pan(cr, 0.0)), *sp], creak + 0.9)
    return finish(reverb(st, seconds=0.8, wet=0.18, seed=seed + 1, damp=7000))


@recipe("reload", family="world",
        doc="A reload: the magazine out, a slide of metal, the magazine in and the bolt: click, slide, clack-clack.",
        tips="gap is the time between the actions; slide the metal slide's amount.",
        params=[
            P("gap", 0.22, 0.08, 0.6, 0.01, "s", "time between actions"),
            P("slide", 0.6, 0, 1.5, 0.05, "", "metal slide amount"),
            SEED(357),
        ])
def reload(*, gap, slide, seed):
    rng = _rng(seed)

    def click(f, amp, d=0.05):
        t = _tr(d)
        x = svf_bandpass(white(len(t), rng), f, 1.4) * env(t, 0.0003, 0.005) * amp * 1.5
        x += 0.4 * osc(f * 0.5, t) * env(t, 0.0005, 0.008) * amp
        return x
    ts = _tr(0.16)
    sl = svf_bandpass(white(len(ts), rng), np.linspace(2600, 1800, len(ts)), 1.2) * np.sin(np.pi * ts / 0.16) * slide * 0.8
    parts = [(0.0, click(2100, 0.9)), (gap, sl), (2 * gap, click(1700, 1.0)), (2 * gap + 0.09, click(2400, 0.8)),
             (3 * gap, click(1400, 1.1, 0.07))]
    return finish(reverb(place(parts, 3 * gap + 0.2), seconds=0.4, wet=0.1, seed=seed + 1, damp=5000))


# ---- stingers ------------------------------------------------------------------------------------------------
@recipe("game_over", family="world",
        doc="Game over: three slow falling notes over a low tone, in a long room.",
        tips="root sets the key; step the time between notes; the fall is a minor third then a fourth.",
        params=[
            P("root", 440, 100, 2000, 0.1, "Hz", "first note (A4)"),
            P("step", 0.4, 0.15, 1.0, 0.01, "s", "time between notes"),
            P("tail", 1.8, 0.4, 5.0, 0.1, "s", "reverb length"),
            SEED(358),
        ])
def game_over(*, root, step, tail, seed):
    ratios = [1.0, 0.8409, 0.6674]
    parts = []
    for i, r in enumerate(ratios):
        t = _tr(0.9 if i < 2 else 1.6)
        x = lowpass(square(root * r, t, 5), 2200, 2) * env(t, 0.01, 0.35 if i < 2 else 0.7)
        parts.append((i * step, pan(release(x, 0.1) * (0.8 + 0.1 * i), (-0.2, 0.0, 0.2)[i])))
    tl = _tr(2 * step + 1.6)
    low = osc(root / 4, tl) * env(tl, 0.05, 1.0) * 0.5
    parts.append((0.0, pan(release(low, 0.2), 0.0)))
    return norm(trim_tail(reverb(place(parts, 2 * step + 1.7), seconds=tail, wet=0.3, seed=seed + 1, damp=3500)))


@recipe("war_horn", family="world",
        doc="A war horn: a brass-like call that swells and opens, with a faint octave below.",
        tips="f is the horn's note (G3 = 196); d its length; open how far the tone brightens; vibrato its shake.",
        params=[
            P("f", 196, 60, 600, 1, "Hz", "horn pitch"),
            P("d", 1.8, 0.6, 5.0, 0.05, "s", "length"),
            P("open", 0.7, 0, 1, 0.05, "", "brightening"),
            P("vibrato", 0.4, 0, 1, 0.05, "", "vibrato depth"),
            P("tail", 1.6, 0.3, 5.0, 0.1, "s", "reverb length"),
            SEED(359),
        ])
def war_horn(*, f, d, open, vibrato, tail, seed):
    t = _tr(d)
    s = t / d
    ff = f * (1 + 0.006 * vibrato * np.sin(2 * np.pi * 5.5 * t) * np.clip((s - 0.3) / 0.4, 0, 1))
    x = saw(ff, t, 14) + 0.4 * saw(ff * 0.5, t, 8)
    fc = 700 + 2200 * open * np.sin(np.pi * s) ** 0.8
    x = svf_bandpass(x, fc, 0.7) * 1.2 + 0.4 * lowpass(x, 900, 2)
    e = np.sin(np.pi * np.clip(s / 0.25, 0, 1) / 2) ** 2 * np.cos(np.pi / 2 * np.clip((s - 0.75) / 0.25, 0, 1)) ** 1.5
    st = pan(release(x * e, 0.1), 0.0)
    return norm(trim_tail(reverb(st, seconds=tail, wet=0.3, seed=seed + 1, damp=4000)))


@recipe("drum_march", family="world",
        doc="A military snare: four strokes and a roll, the pattern of a march.",
        tips="tempo is the stroke interval; roll_len the roll's length; snare the wires' brightness.",
        params=[
            P("tempo", 0.3, 0.12, 0.8, 0.01, "s", "stroke interval"),
            P("roll_len", 0.6, 0.2, 2.0, 0.05, "s", "roll length"),
            P("snare", 1.0, 0, 2, 0.05, "", "snare wire amount"),
            SEED(360),
        ])
def drum_march(*, tempo, roll_len, snare, seed):
    rng = _rng(seed)

    def stroke(amp):
        t = _tr(0.18)
        w = svf_bandpass(white(len(t), rng), 2600, 0.6) * env(t, 0.0005, 0.045) * snare * 1.3
        body = osc(glide(240, 180, t, 0.02), t) * env(t, 0.0008, 0.05) * 0.9
        return (w + body) * amp
    parts = [(i * tempo, stroke(1.0 if i % 2 == 0 else 0.7)) for i in range(4)]
    t0 = 4 * tempo
    k = 0
    while k * 0.055 < roll_len:
        parts.append((t0 + k * 0.055 + float(rng.uniform(0, 0.004)), stroke(0.45 + 0.45 * (k * 0.055 / roll_len))))
        k += 1
    parts.append((t0 + roll_len + 0.05, stroke(1.2)))
    return finish(reverb(place(parts, t0 + roll_len + 0.4), seconds=0.9, wet=0.18, seed=seed + 1, damp=5000))
