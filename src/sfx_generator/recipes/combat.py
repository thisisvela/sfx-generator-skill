"""Combat: explosions, guns, cannon, arrows, blades, blows. Game sounds built from the same blocks."""
import numpy as np

from ..blocks import (SR, _rng, _tr, burst, env, fade, finish, glide, highpass, ks_pluck, lowpass, norm, osc, pan,
                      pink, place, release, reverb, saw, square, svf_bandpass, tone, trim_tail, white)
from ..schema import I, P, SEED, recipe


def _boom(rng, d, f0, f1, tau, knock_hz, knock, body_hz, body_tau):
    t = _tr(d)
    sub = osc(glide(f0, f1, t, 0.06), t) * env(t, 0.003, tau)
    k = lowpass(white(len(t), rng), knock_hz, 2) * env(t, 0.0005, 0.03) * knock
    body = svf_bandpass(pink(len(t), rng), body_hz, 0.8) * env(t, 0.002, body_tau) * 0.8
    return sub + k + body


@recipe("explosion", family="combat",
        doc="A close explosion: a crack, a sub boom, a noise body that decays, debris ticks and a long tail.",
        tips="crack is the snap at the front; f0/f1 the boom's fall; body_tau how long the roar lasts; debris "
             "the seeded ticks after it; tail the reverb.",
        params=[
            P("d", 1.6, 0.5, 4.0, 0.05, "s", "dry length"),
            P("crack", 1.0, 0, 2, 0.05, "", "initial crack amount"),
            P("f0", 70, 30, 200, 1, "Hz", "boom start pitch"),
            P("f1", 28, 15, 100, 1, "Hz", "boom end pitch"),
            P("body_tau", 0.45, 0.1, 1.5, 0.01, "s", "roar decay"),
            P("debris", 0.5, 0, 1.5, 0.05, "", "debris ticks amount"),
            P("tail", 1.8, 0.3, 5.0, 0.1, "s", "reverb length"),
            P("wet", 0.3, 0, 0.8, 0.01, "", "reverb amount"),
            SEED(321),
        ])
def explosion(*, d, crack, f0, f1, body_tau, debris, tail, wet, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    boom = _boom(rng, d, f0, f1, 0.5, 900, 0.9, 160, body_tau)
    roar = lowpass(white(n, rng), 2500, 2) * env(t, 0.004, body_tau) * 0.9
    c = np.zeros(n)
    b = burst(0.02, rng, lo=800, hi=9000, tau=0.004) * crack * 1.6
    c[: len(b)] = b
    deb = np.zeros(n)
    for _ in range(14):
        s0 = rng.uniform(0.25, min(d - 0.05, 1.3))
        bb = burst(rng.uniform(0.004, 0.012), rng, lo=600, hi=5000, tau=0.002) * rng.uniform(0.2, 0.7) * debris
        a = int(s0 * SR)
        deb[a:a + len(bb)] += bb[: n - a]
    mono = boom + roar + c + deb
    st = reverb(pan(mono, 0.0), seconds=tail, wet=wet, seed=seed + 1, damp=3500)
    return norm(trim_tail(fade(st, 0.0005, 0.08)))


@recipe("explosion_distant", family="combat",
        doc="An explosion far away: no crack, a soft low boom and a long rolling tail.",
        tips="lowpass_hz is the distance (lower = farther); tail the air it rolls through.",
        params=[
            P("d", 1.4, 0.5, 4.0, 0.05, "s", "dry length"),
            P("lowpass_hz", 500, 150, 2000, 10, "Hz", "distance low-pass"),
            P("tail", 2.6, 0.5, 6.0, 0.1, "s", "reverb length"),
            P("wet", 0.45, 0, 0.9, 0.01, "", "reverb amount"),
            SEED(322),
        ])
def explosion_distant(*, d, lowpass_hz, tail, wet, seed):
    rng = _rng(seed)
    t = _tr(d)
    boom = _boom(rng, d, 60, 26, 0.6, 400, 0.5, 120, 0.6)
    roar = lowpass(white(len(t), rng), lowpass_hz, 2) * env(t, 0.03, 0.5) * 1.2
    st = reverb(pan(lowpass(boom + roar, lowpass_hz, 2), 0.0), seconds=tail, wet=wet, seed=seed + 1, damp=1200)
    return norm(trim_tail(fade(st, 0.01, 0.1)))


@recipe("cannon", family="combat",
        doc="A cannon: a hard low boom with a mid thump and a long tail; heavier and rounder than a gunshot.",
        tips="f0/f1 the boom; thump the mid body; tail the field it echoes over.",
        params=[
            P("d", 1.2, 0.4, 3.0, 0.05, "s", "dry length"),
            P("f0", 95, 40, 250, 1, "Hz", "boom start pitch"),
            P("f1", 34, 15, 100, 1, "Hz", "boom end pitch"),
            P("thump", 0.8, 0, 2, 0.05, "", "mid thump amount"),
            P("tail", 1.6, 0.3, 5.0, 0.1, "s", "reverb length"),
            P("wet", 0.28, 0, 0.8, 0.01, "", "reverb amount"),
            SEED(323),
        ])
def cannon(*, d, f0, f1, thump, tail, wet, seed):
    rng = _rng(seed)
    t = _tr(d)
    boom = _boom(rng, d, f0, f1, 0.4, 1500, 1.2, 220, 0.25)
    mid = svf_bandpass(white(len(t), rng), 420, 1.0) * env(t, 0.001, 0.09) * thump
    c = np.zeros(len(t))
    b = burst(0.012, rng, lo=500, hi=6000, tau=0.003) * 0.8
    c[: len(b)] = b
    st = reverb(pan(boom + mid + c, 0.0), seconds=tail, wet=wet, seed=seed + 1, damp=2500)
    return norm(trim_tail(fade(st, 0.0005, 0.08)))


def _shot(rng, bright, thump_hz, crack, tail_hz, tail_tau):
    t = _tr(0.35)
    n = len(t)
    c = np.zeros(n)
    b = burst(0.006, rng, lo=1500, tau=0.0012) * crack * 1.8
    c[: len(b)] = b
    body = svf_bandpass(white(n, rng), bright, 1.0) * env(t, 0.0005, 0.02) * 1.2
    th = osc(glide(thump_hz, thump_hz * 0.4, t, 0.03), t) * env(t, 0.001, 0.05) * 0.9
    tl = lowpass(white(n, rng), tail_hz, 2) * env(t, 0.004, tail_tau) * 0.5
    return c + body + th + tl


@recipe("gunshot", family="combat",
        doc="A pistol shot: a snap, a mid crack, a low thump and a short slap-back.",
        tips="bright is the crack's band; thump_hz the low body; crack the snap; room the slap-back amount.",
        params=[
            P("bright", 2600, 800, 8000, 10, "Hz", "crack band centre"),
            P("thump_hz", 150, 50, 400, 1, "Hz", "thump pitch"),
            P("crack", 1.0, 0, 2, 0.05, "", "snap amount"),
            P("tail_tau", 0.12, 0.03, 0.5, 0.005, "s", "noise tail decay"),
            P("room", 0.18, 0, 0.6, 0.01, "", "slap-back amount"),
            SEED(324),
        ])
def gunshot(*, bright, thump_hz, crack, tail_tau, room, seed):
    rng = _rng(seed)
    x = _shot(rng, bright, thump_hz, crack, 1200, tail_tau)
    st = reverb(pan(x, 0.0), seconds=0.45, wet=room, seed=seed + 1, damp=4000)
    return norm(trim_tail(fade(st, 0.0003, 0.04)))


@recipe("machine_gun", family="combat",
        doc="A burst of automatic fire: seeded shots at a steady rate with small variations.",
        tips="count is the number of rounds; rate the time between them; jitter their timing variance.",
        params=[
            I("count", 8, 2, 40, "", "rounds"),
            P("rate", 0.085, 0.04, 0.3, 0.005, "s", "time between rounds"),
            P("jitter", 0.004, 0, 0.03, 0.001, "s", "timing variance"),
            P("bright", 2200, 800, 8000, 10, "Hz", "crack band centre"),
            SEED(325),
        ])
def machine_gun(*, count, rate, jitter, bright, seed):
    rng = _rng(seed)
    parts = []
    for i in range(count):
        x = _shot(rng, bright * rng.uniform(0.9, 1.1), 140, 0.8, 1000, 0.05) * rng.uniform(0.75, 1.0)
        parts.append((i * rate + float(rng.uniform(-jitter, jitter)) + jitter, pan(x, rng.uniform(-0.15, 0.15))))
    st = place(parts, count * rate + 0.4)
    st = reverb(st, seconds=0.4, wet=0.12, seed=seed + 1, damp=4000)
    return norm(trim_tail(fade(highpass(st, 60, 2), 0.0003, 0.04)))


@recipe("shotgun", family="combat",
        doc="A shotgun: a wide low blast with a long noise tail, then the pump: click-clack.",
        tips="blast is the low body; pump_gap the time before the pump action (0 removes it).",
        params=[
            P("blast", 1.0, 0.2, 2, 0.05, "", "low blast amount"),
            P("pump_gap", 0.55, 0, 1.5, 0.01, "s", "time to the pump action"),
            P("tail_tau", 0.25, 0.05, 0.8, 0.005, "s", "noise tail decay"),
            SEED(326),
        ])
def shotgun(*, blast, pump_gap, tail_tau, seed):
    rng = _rng(seed)
    x = _shot(rng, 1400, 90, 1.2, 700, tail_tau)
    t = _tr(0.35)
    x += osc(glide(70, 35, t, 0.05), t) * env(t, 0.002, 0.12) * blast
    parts = [(0.0, x)]
    if pump_gap > 0:
        for k, (f, amp) in enumerate(((2400, 0.5), (1700, 0.6))):
            tt = _tr(0.06)
            click = svf_bandpass(white(len(tt), rng), f, 1.5) * env(tt, 0.0003, 0.004) * amp
            click += 0.3 * osc(900, tt) * env(tt, 0.0005, 0.006) * amp
            parts.append((pump_gap + 0.11 * k, click))
    st = place(parts, pump_gap + 0.4)
    st = reverb(st, seconds=0.5, wet=0.15, seed=seed + 1, damp=3500)
    return norm(trim_tail(fade(st, 0.0003, 0.04)))


@recipe("tank_fire", family="combat",
        doc="A tank's main gun: the muzzle blast, an explosion with a roar; discrete echoes off the landscape, each "
            "darker and quieter; and the shell piercing the air, a whistle that falls in pitch as it recedes.",
        tips="blast is the explosion's amount; echoes how many returns off the hills, echo_gap their spacing, "
             "echo_drop dB lost per return; shell the whistle's amount, shell_hz its starting pitch, shell_d how "
             "long it takes to recede; rumble the low roll; tail the reverb.",
        params=[
            P("blast", 1.0, 0.2, 2, 0.05, "", "muzzle blast amount"),
            P("rumble", 1.2, 0.3, 3.0, 0.05, "s", "low roll decay"),
            I("echoes", 3, 0, 6, "", "returns off the landscape"),
            P("echo_gap", 0.42, 0.15, 1.2, 0.01, "s", "time between returns"),
            P("echo_drop", 7, 2, 15, 0.5, "dB", "level lost per return"),
            P("shell", 1.0, 0, 2, 0.05, "", "shell whistle amount"),
            P("shell_hz", 2600, 800, 6000, 10, "Hz", "whistle start pitch"),
            P("shell_d", 1.3, 0.4, 3.0, 0.05, "s", "time for the shell to recede"),
            P("tail", 2.2, 0.5, 6.0, 0.1, "s", "reverb length"),
            SEED(327),
        ])
def tank_fire(*, blast, rumble, echoes, echo_gap, echo_drop, shell, shell_hz, shell_d, tail, seed):
    rng = _rng(seed)
    d = 1.8
    t = _tr(d)
    n = len(t)
    # the muzzle blast: an explosion (crack, sub boom, knock, body) with a roar that tears as it fades
    boom = _boom(rng, d, 120, 28, 0.5, 1800, 1.4, 240, 0.3)
    s_ = t / d
    tear = lowpass(white(n, rng), 14, 2)
    tear = 0.5 + 0.5 * tear / (np.abs(tear).max() + 1e-9)
    fc = np.exp(np.linspace(np.log(900), np.log(140), n))
    roar = svf_bandpass(pink(n, rng), fc, 0.7) * np.exp(-s_ * 5.0) * tear * 1.6
    roll = lowpass(white(n, rng), 160, 2) * env(t, 0.01, rumble) * 3.0
    c = np.zeros(n)
    b = burst(0.02, rng, lo=500, hi=9000, tau=0.004) * 1.5
    c[: len(b)] = b
    blast_x = (boom + roar + c) * blast + roll
    parts = [(0.0, pan(blast_x, 0.0))]
    # the echoes: the blast's low half returning off the landscape, each later one darker and quieter
    for i in range(1, echoes + 1):
        g = 10 ** (-echo_drop * i / 20)
        e = lowpass(blast_x, 1400 * (0.6 ** i), 2) * g * rng.uniform(0.8, 1.0)
        parts.append((echo_gap * i * rng.uniform(0.9, 1.15), pan(e, rng.uniform(-0.5, 0.5))))
    # the shell piercing the air: a narrow whistle that falls in pitch (doppler) as it recedes, with a zip at the start
    if shell > 0:
        ts = _tr(shell_d)
        m = len(ts)
        ss = ts / shell_d
        fw = shell_hz * np.exp(-2.2 * ss)                        # falls to about a ninth of its start pitch
        whistle = svf_bandpass(white(m, rng), fw, 14) * (np.clip(ss / 0.04, 0, 1) * np.exp(-ss * 2.8)) * 2.4
        zip_ = svf_bandpass(white(m, rng), np.exp(np.linspace(np.log(shell_hz * 2.5), np.log(shell_hz), m)), 6)             * env(ts, 0.002, 0.05) * 1.2
        parts.append((0.02, pan(release((whistle + zip_) * shell, 0.1), np.linspace(0.0, 0.6, m))))
    st = place(parts, max(a + len(x) / SR for a, x in parts) + 0.05)
    st = reverb(st, seconds=tail, wet=0.3, seed=seed + 1, damp=2500)
    return norm(trim_tail(fade(st, 0.0005, 0.1)))


@recipe("ricochet", family="combat",
        doc="A ricochet: a click, then a falling narrow whistle: the classic pee-yow.",
        tips="f_start -> f_end is the whistle's fall; d its length; q its narrowness (higher = purer).",
        params=[
            P("d", 0.45, 0.15, 1.5, 0.01, "s", "length"),
            P("f_start", 5200, 1500, 12000, 10, "Hz", "whistle start"),
            P("f_end", 1400, 300, 6000, 10, "Hz", "whistle end"),
            P("q", 7, 2, 20, 0.5, "", "whistle narrowness"),
            SEED(328),
        ])
def ricochet(*, d, f_start, f_end, q, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    fc = np.exp(np.log(f_start) + (np.log(f_end) - np.log(f_start)) * (t / d) ** 0.7)
    w = svf_bandpass(svf_bandpass(white(n, rng), fc, q), fc, q) * env(t, 0.004, d * 0.35) * 3.0
    c = np.zeros(n)
    b = burst(0.005, rng, lo=2000, tau=0.001) * 1.2
    c[: len(b)] = b
    st = pan(w + c, np.linspace(-0.3, 0.5, n))
    return finish(st)


@recipe("arrow", family="combat",
        doc="An arrow: the bow's twang, a short rising whoosh of flight, and a wooden thunk where it lands.",
        tips="flight is the time in the air (the thunk lands at the end: use it as the lead); twang the string "
             "amount; thunk the impact.",
        params=[
            P("flight", 0.45, 0.15, 1.5, 0.01, "s", "time in the air"),
            P("twang", 0.7, 0, 1.5, 0.05, "", "bow string amount"),
            P("thunk", 1.0, 0, 2, 0.05, "", "impact amount"),
            SEED(329),
        ])
def arrow(*, flight, twang, thunk, seed):
    rng = _rng(seed)
    s = ks_pluck(105, 0.3, seed, damp=0.985, bright=0.5)
    ts = _tr(0.3)
    s = s[: len(ts)] / (np.abs(s[: len(ts)]).max() + 1e-9) * env(ts, 0.0005, 0.08) * twang
    tf = _tr(flight)
    n = len(tf)
    fc = np.exp(np.log(900) + (np.log(2600) - np.log(900)) * np.linspace(0, 1, n))
    wh = svf_bandpass(svf_bandpass(white(n, rng), fc, 1.6), fc, 1.6) * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.2 * 1.2
    tt = _tr(0.25)
    k = np.zeros(len(tt))
    b = lowpass(burst(0.03, rng, hi=2500, tau=0.008), 2500, 2) * 1.5
    k[: len(b)] = b
    th = (k + osc(glide(190, 120, tt, 0.02), tt) * env(tt, 0.001, 0.05) * 0.9
          + tone(410, tt, [(1, 0.4, 0.03), (2.7, 0.15, 0.015)], attack=0.0005))
    th = release(th * thunk, 0.05)
    st = place([(0.0, pan(s, -0.3)), (0.02, pan(wh, np.linspace(-0.3, 0.3, n))), (flight, pan(th, 0.3))], flight + 0.3)
    return finish(reverb(st, seconds=0.5, wet=0.1, seed=seed + 1, damp=5000))


@recipe("sword_swing", family="combat",
        doc="A blade swung through the air: a fast metallic whoosh with a thin high ring.",
        tips="d is the swing's length; f_peak the whoosh's top; ring the blade's edge tone.",
        params=[
            P("d", 0.32, 0.1, 1.0, 0.01, "s", "length"),
            P("f_peak", 3200, 800, 9000, 10, "Hz", "whoosh peak band"),
            P("ring", 0.25, 0, 1, 0.01, "", "edge ring amount"),
            SEED(330),
        ])
def sword_swing(*, d, f_peak, ring, seed):
    rng = _rng(seed)
    t = _tr(d)
    n = len(t)
    s = np.linspace(0, 1, n)
    fc = np.exp(np.interp(s, [0, 0.45, 1], np.log([700, f_peak, 1400])))
    e = np.sin(np.pi * s) ** 1.6
    wh = svf_bandpass(svf_bandpass(white(n, rng) * 0.6 + pink(n, rng) * 0.4, fc, 2.2), fc, 2.2) * e * 2.5
    r = osc(fc * 1.9, t) * e * ring * 0.4
    st = pan(wh + r, np.interp(s, [0, 1], [0.5, -0.5]))
    return finish(st)


@recipe("sword_clash", family="combat",
        doc="Two blades meeting: a sharp strike, an inharmonic metallic ring, a little room.",
        tips="f0 is the ring's pitch; decay its length; strike the hit's amount.",
        params=[
            P("f0", 1180, 300, 4000, 10, "Hz", "ring pitch"),
            P("decay", 1.0, 0.3, 3.0, 0.05, "", "ring length multiplier"),
            P("strike", 1.0, 0, 2, 0.05, "", "strike amount"),
            P("wet", 0.12, 0, 0.5, 0.01, "", "room amount"),
            SEED(331),
        ])
def sword_clash(*, f0, decay, strike, wet, seed):
    rng = _rng(seed)
    t = _tr(0.7)
    r = tone(f0, t, [(1, 1.0, 0.25 * decay), (1.52, 0.6, 0.18 * decay), (2.31, 0.4, 0.12 * decay),
                     (3.17, 0.25, 0.08 * decay), (4.73, 0.12, 0.05 * decay), (6.1, 0.06, 0.03 * decay)], attack=0.0004)
    c = np.zeros_like(t)
    b = burst(0.012, rng, lo=1500, hi=12000, tau=0.002) * strike * 1.6
    c[: len(b)] = b
    return finish(reverb(pan(r + c, 0.0), seconds=0.5, wet=wet, seed=seed + 1, damp=8000))


@recipe("punch", family="combat",
        doc="A body blow: a low thump with a short slap on top.",
        tips="f is the thump pitch; slap the skin's snap; tau the decay.",
        params=[
            P("f", 120, 50, 300, 1, "Hz", "thump pitch"),
            P("slap", 0.6, 0, 1.5, 0.05, "", "slap amount"),
            P("tau", 0.07, 0.02, 0.3, 0.005, "s", "thump decay"),
            SEED(332),
        ])
def punch(*, f, slap, tau, seed):
    rng = _rng(seed)
    t = _tr(0.25)
    th = osc(glide(f, f * 0.45, t, 0.025), t) * env(t, 0.002, tau)
    body = lowpass(white(len(t), rng), 1100, 2) * env(t, 0.001, 0.03) * 0.8
    c = np.zeros_like(t)
    b = burst(0.01, rng, lo=1200, hi=5000, tau=0.002) * slap
    c[: len(b)] = b
    return finish(reverb(pan(th + body + c, 0.0), seconds=0.3, wet=0.06, seed=seed + 1, damp=4000))


@recipe("hurt", family="combat",
        doc="Taking damage: a short buzzy tone that drops, with a little noise: an 'oof' without a voice.",
        tips="f0 -> f1 is the drop; d the length; lowpass_hz the buzz's brightness.",
        params=[
            P("f0", 420, 100, 1500, 1, "Hz", "start pitch"),
            P("f1", 230, 60, 1000, 1, "Hz", "end pitch"),
            P("d", 0.28, 0.1, 0.8, 0.005, "s", "length"),
            P("lowpass_hz", 2200, 500, 8000, 50, "Hz", "buzz low-pass"),
            SEED(333),
        ])
def hurt(*, f0, f1, d, lowpass_hz, seed):
    rng = _rng(seed)
    t = _tr(d)
    f = glide(f0, f1, t, d * 0.35)
    x = lowpass(square(f, t, 5), lowpass_hz, 2) * env(t, 0.004, d * 0.45)
    nz = lowpass(white(len(t), rng), 1800, 2) * env(t, 0.002, 0.04) * 0.35
    return finish(pan(release(x + nz, 0.05), 0.0))
