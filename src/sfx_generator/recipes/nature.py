"""Nature: rain, waves, thunder, wind. Events (a wave, a thunderclap, a few drops) and seamless loops."""
import numpy as np

from ..blocks import (SR, _rng, _tr, burst, env, fade, finish, glide, highpass, loop_seam, lowpass, norm, osc, pan,
                      pink, place, release, reverb, room, svf_bandpass, trim_tail, white)
from ..schema import I, P, SEED, recipe


def _raindrop(rng, water, f, chirp, body):
    """One drop, as the recordings measure it: an instant 2-3 ms broadband impact (500 Hz to 11 kHz), for a big
    drop a 3 ms thump at 600-1800 Hz, and, when it lands in water, a ring that is loud for 10 ms and then runs on quietly for 30-60 ms while its pitch rises, up to doubling, as
    the bubble it trapped shrinks (the plink). Nothing falls in pitch."""
    t = _tr(0.07)
    n = len(t)
    x = np.zeros(n)
    click = burst(0.0025, rng, lo=600, hi=8000, tau=0.0008)
    x[: len(click)] += click
    x += svf_bandpass(white(n, rng), rng.uniform(600, 1800), 1.0) * env(t, 0.0005, 0.003) * body
    if rng.random() < water:
        L = rng.uniform(0.03, 0.06)                                   # the ring: loud for 10 ms, then quietly on
        tt = _tr(L)
        ring = osc(f * (1 + chirp * np.linspace(0, 1, len(tt)) ** 0.8), tt) * (env(tt, 0.0004, 0.004) + 0.06 * env(tt, 0.0004, L * 0.5)) * rng.uniform(0.6, 1.0)
        x[: len(ring)] += ring[:n]
    return release(x, 0.004)


@recipe("rain_drops", family="nature",
        doc="A few rain drops, built to measured drops: each an instant tick of 6-15 ms, broadband; drops that "
            "land in water add a short ring rising in pitch (the plink); on leaves or ground only the tick and a "
            "small thump. Spread across the field at irregular times.",
        tips="count is how many drops; d the window; water the share of drops that land in water (0 = leaves or "
             "ground, 1 = a puddle); f_lo/f_hi the plink pitch (2-5 kHz on real drops); chirp how far it rises; "
             "body the thump of a big drop; wet the surface's room.",
        params=[
            I("count", 8, 1, 40, "", "number of drops"),
            P("d", 1.2, 0.3, 4.0, 0.05, "s", "window the drops fall in"),
            P("water", 0.6, 0, 1, 0.05, "", "share of drops landing in water (plink)"),
            P("f_lo", 1800, 800, 6000, 10, "Hz", "lowest plink pitch"),
            P("f_hi", 4000, 1000, 9000, 10, "Hz", "highest plink pitch"),
            P("chirp", 0.5, 0, 1.5, 0.05, "", "how far the plink rises (1 = an octave)"),
            P("body", 1.0, 0, 2, 0.05, "", "big-drop thump amount (500 Hz to 2 kHz)"),
            P("wet", 0.12, 0, 0.6, 0.01, "", "room amount"),
            SEED(301),
        ])
def rain_drops(*, count, d, water, f_lo, f_hi, chirp, body, wet, seed):
    rng = _rng(seed)
    times = np.sort(rng.uniform(0.02, max(0.05, d - 0.08), count))
    parts = []
    for t0 in times:
        f = np.exp(rng.uniform(np.log(f_lo), np.log(f_hi)))
        amp = rng.lognormal(0, 0.5) * 0.7
        parts.append((float(t0), pan(_raindrop(rng, water, f, chirp, body) * amp, rng.uniform(-0.8, 0.8))))
    return finish(room(place(parts, d + 0.1), wet=wet, seconds=0.5))


@recipe("rain_loop", family="nature",
        doc="Steady rain, measured against real recordings: a falling roar with its weight between 250 Hz and "
            "4 kHz, a surface band at 80-250 Hz (roof, window, ground), a granular 16-64 Hz drop texture, and "
            "individual drops as ticks 15-20 dB above the bed; the hiss above 4 kHz sits 15-20 dB under the mids. "
            "A seamless loop.",
        tips="intensity moves light to pouring (more above 5 kHz, more roar, denser ticks); surface is the "
             "80-250 Hz band's amount (ground 0.3, leaves 0.2, roof or skylight 1.0, window 0.8) and surface_hz "
             "where it sits; drops is ticks per second; hiss the air above 4 kHz; d the loop length.",
        params=[
            P("d", 6.0, 2.0, 16.0, 0.5, "s", "loop length (before the seam crossfade)"),
            P("intensity", 0.5, 0, 1, 0.05, "", "light (0) to pouring (1)"),
            P("surface", 0.7, 0, 2, 0.05, "", "surface band amount (80-250 Hz)"),
            P("surface_hz", 160, 80, 250, 5, "Hz", "surface band centre"),
            I("drops", 25, 0, 300, "/s", "individual drop ticks per second"),
            P("hiss", 0.5, 0, 2, 0.05, "", "air above 4 kHz"),
            SEED(302),
        ])
def rain_loop(*, d, intensity, surface, surface_hz, drops, hiss, seed):
    rng = _rng(seed)
    n = int(round(SR * d))

    def bed():
        core = svf_bandpass(pink(n, rng), 900, 0.35) * (1.0 + 0.4 * intensity)      # the roar, 250 Hz to 4 kHz
        low = svf_bandpass(pink(n, rng), 420, 0.5) * 0.9
        surf = svf_bandpass(pink(n, rng), surface_hz, 0.8) * surface * (0.8 + 0.5 * intensity)
        top = highpass(white(n, rng), 4000, 2) * (0.006 + 0.03 * intensity) * hiss  # 15-20 dB under the mids
        return lowpass(core + low + surf, 3600, 2) + top
    shared = bed()
    st = np.stack([shared * 0.8 + bed() * 0.45, shared * 0.8 + bed() * 0.45], axis=1)
    gran = lowpass(white(n, rng), 40, 2)                                             # the 16-64 Hz drop texture
    gran = 0.65 + 0.35 * gran / (np.abs(gran).max() + 1e-9)
    st *= gran[:, None]
    bed_rms = np.sqrt((st ** 2).mean())
    ticks = np.zeros((n, 2))
    k = int(drops * d * (0.5 + intensity))
    for a in (rng.uniform(0, d, k) * SR).astype(int):
        x = burst(rng.uniform(0.003, 0.009), rng, lo=rng.uniform(600, 1800), hi=3000, tau=rng.uniform(0.001, 0.002))
        x = x / (np.abs(x).max() + 1e-9) * bed_rms * 10 ** (rng.uniform(16, 24) / 20)   # 16-24 dB above the bed
        b = min(n, a + len(x))
        ticks[a:b] += pan(x[: b - a], rng.uniform(-0.8, 0.8))
    st = lowpass(st + ticks, 12000, 2)
    return norm(loop_seam(st, 0.25))


def _wave(rng, d, f_lo, f_hi, crest, hiss, pan_from, pan_to):
    n = int(round(SR * d))
    s = np.linspace(0, 1, n)
    e = np.sin(np.pi * np.clip(s / crest, 0, 1) / 2) ** 2 * np.cos(np.pi / 2 * np.clip((s - crest) / (1 - crest), 0, 1)) ** 1.3
    fc = np.exp(np.log(f_lo) + (np.log(f_hi) - np.log(f_lo)) * np.sin(np.pi * np.clip(s, 0, 1)) ** 1.5)
    body = svf_bandpass(pink(n, rng), fc, 0.6)
    foam = svf_bandpass(white(n, rng), fc * 4, 0.8) * hiss * np.clip((s - crest * 0.6) / 0.25, 0, 1) * (1 - s) ** 0.6
    mono = (body + foam) * e
    return pan(mono, np.interp(s, [0, 1], [pan_from, pan_to]))


@recipe("wave", family="nature",
        doc="One wave: a slow swell of band-passed noise that rises, breaks into foam and washes out.",
        tips="d is the whole wave; crest where (0-1) it breaks; f_lo/f_hi the band's travel; hiss the foam; the "
             "pans move it along the shore.",
        params=[
            P("d", 3.5, 1.0, 10.0, 0.1, "s", "length"),
            P("crest", 0.42, 0.15, 0.8, 0.01, "", "position of the break (0-1)"),
            P("f_lo", 220, 60, 1000, 10, "Hz", "band at the start and end"),
            P("f_hi", 1400, 300, 5000, 10, "Hz", "band at the crest"),
            P("hiss", 0.5, 0, 1.5, 0.05, "", "foam amount"),
            P("pan_from", -0.4, -1, 1, 0.05, "", "pan at the start"),
            P("pan_to", 0.4, -1, 1, 0.05, "", "pan at the end"),
            SEED(303),
        ])
def wave(*, d, crest, f_lo, f_hi, hiss, pan_from, pan_to, seed):
    rng = _rng(seed)
    st = _wave(rng, d, f_lo, f_hi, crest, hiss, pan_from, pan_to)
    return norm(fade(lowpass(st, 9000, 2), 0.02, 0.08))


@recipe("waves_loop", family="nature",
        doc="A beach: waves arriving one after another over a bed of surf; a seamless loop.",
        tips="d is the loop length; waves how many arrive in it; hiss the foam; the bed is the distant surf.",
        params=[
            P("d", 10.0, 4.0, 30.0, 0.5, "s", "loop length (before the seam crossfade)"),
            I("waves", 2, 1, 6, "", "waves per loop"),
            P("hiss", 0.5, 0, 1.5, 0.05, "", "foam amount"),
            P("bed", 0.25, 0, 1, 0.05, "", "distant surf amount"),
            SEED(304),
        ])
def waves_loop(*, d, waves, hiss, bed, seed):
    rng = _rng(seed)
    n = int(round(SR * d))
    out = np.zeros((n, 2))
    per = d / waves
    for i in range(waves):
        w = _wave(rng, per * 1.3, 220, 1400, 0.42, hiss, -0.4 if i % 2 == 0 else 0.4, 0.4 if i % 2 == 0 else -0.4)
        a = int(i * per * SR)
        m = min(len(w), n - a)
        out[a:a + m] += w[:m]
        if len(w) > m:                                 # the last wave wraps into the start of the loop
            out[: len(w) - m] += w[m:]
    surf = np.stack([svf_bandpass(pink(n, rng), 500, 0.5), svf_bandpass(pink(n, rng), 560, 0.5)], axis=1) * bed
    st = lowpass(out + surf, 8000, 2)
    return norm(loop_seam(st, 0.4))


def _peal(rng, length, crack, roar, rumble, top_hz, amp):
    """One peal of thunder: a crack, a roar (mid-band noise torn by a fast random modulation, its band sliding
    down from top_hz as it rolls), and a sub rumble under it. Fast rise, slow fall."""
    t = _tr(length)
    n = len(t)
    s = t / length
    shape = (1 - np.exp(-t / 0.035)) * np.exp(-s * 2.4)
    tear = lowpass(white(n, rng), 11, 2)                       # 4-14 Hz random tearing: a roar, not a hiss
    tear = 0.5 + 0.5 * tear / (np.abs(tear).max() + 1e-9)
    fc = np.exp(np.linspace(np.log(top_hz), np.log(max(90.0, top_hz * 0.18)), n))
    r = svf_bandpass(pink(n, rng), fc, 0.6) * shape * tear * roar * 2.2
    low = lowpass(lowpass(white(n, rng), 110, 2), 110, 2) * shape * (0.7 + 0.3 * tear) * rumble * 4.5
    sub = osc(glide(58, 30, t, 0.25), t) * np.exp(-t / (0.22 * length)) * 0.45 * rumble
    c = np.zeros(n)
    b = highpass(burst(0.14, rng, lo=220, hi=5000, tau=0.045), 220, 2) * crack * 1.3
    c[: len(b)] = b
    return release((r + low + sub + c) * amp, 0.05)


def _arrivals(rng, length, rate, amp, lo_ms=3.0, hi_ms=18.0, heavy=0.9, lp=600):
    """A rumble the way a real one is made: a dense train of small shock arrivals (N-wave pulses of random
    length and sign, heavy-tailed amplitudes) rather than filtered noise. Noise is wind (kurtosis ~0); real
    thunder rumble measures kurtosis 8-45 in its 80-250 Hz band because it is a pile of arrivals. `rate` and
    `amp` are arrays over the length (arrivals per second, level); pulse length sets the weight (a 10 ms pulse
    peaks near 100 Hz), so there is no resonant filter to make a tone."""
    n = int(round(SR * length))
    x = np.zeros(n + int(SR * 0.03))
    step = 0.002
    k = int(length / step)
    r = np.interp(np.arange(k) * step, np.linspace(0, length, len(rate)), rate)
    a = np.interp(np.arange(k) * step, np.linspace(0, length, len(amp)), amp)
    counts = rng.poisson(np.maximum(r, 0) * step)
    for idx in np.nonzero(counts)[0]:
        for _ in range(counts[idx]):
            L = int(SR * rng.uniform(lo_ms, hi_ms) / 1000)
            at = int((idx * step + rng.uniform(0, step)) * SR)
            g = a[idx] * rng.lognormal(0.0, heavy) * rng.choice([-1, 1])
            x[at:at + L] += np.linspace(1, -1, L)[: len(x) - at] * g
    return highpass(lowpass(x[:n], lp, 2), 60, 2)        # the weight above 80 Hz, as recorded


def _rolling(rng, n, depth=0.45, grind=0.12):
    """How a roll moves: slow waves at 0.5-3 Hz carry the movement (real strikes modulate there), a 9 Hz grind is
    only a light texture on top."""
    w = lowpass(white(n, rng), 1.5, 2)
    w = (1 - depth) + depth * w / (np.abs(w).max() + 1e-9)
    g = lowpass(white(n, rng), 9, 2)
    g = (1 - grind) + grind * g / (np.abs(g).max() + 1e-9)
    return w * g


def _approach(rng, length, amount):
    """The distant rumble before the first hit: sparse, soft, long arrivals (a far strike's pile of echoes),
    swelling slowly and melting back a little just before the crack."""
    t = _tr(length)
    n = len(t)
    s = t / length
    swell = s ** 1.3 * (1 - 0.35 * np.clip((s - 0.85) / 0.15, 0, 1))
    mov = _rolling(rng, n, depth=0.4)
    x = _arrivals(rng, length, rate=30 + 110 * swell, amp=0.12 * swell * mov, lo_ms=4, hi_ms=14, heavy=1.1, lp=320)
    return x * amount


def _rip(rng, length, amount):
    """Heavy canvas ripping: a bright noise band that grows and sweeps up, torn by a 40-70 Hz granular modulation.
    Only a close strike has it, and only for a fraction of a second: above 4 kHz a real strike is 30-45 dB down."""
    t = _tr(length)
    n = len(t)
    s = t / length
    gran = lowpass(white(n, rng), 55, 2)
    gran = np.clip(0.3 + 0.7 * gran / (np.abs(gran).max() + 1e-9), 0, 1)
    fc = np.exp(np.linspace(np.log(800), np.log(2800), n))
    return svf_bandpass(white(n, rng), fc, 0.8) * s ** 0.8 * gran * amount * 1.7


def _crack(rng, amount, build=None):
    """The crack, as the recordings show it: not a hit. A ragged crackle of many short impulses that builds over
    100-300 ms (rate and level both rising), culminates in a dense burst of arrivals (the channel's segments
    arriving together: a burst, not three thuds), and falls away raggedly over the next 150 ms. Broadband and
    flat to 4 kHz for its first 60 ms, the weight at 80-250 Hz from the pulses' length; no oscillator and no
    resonant filter, so it never reads as a drum. Returns (signal, seconds from start to the peak)."""
    build = rng.uniform(0.12, 0.3) if build is None else build
    length = build + 0.45
    n = int(round(SR * length))
    t = np.arange(n) / SR
    s = np.clip(t / build, 0, None)
    rising = s < 1
    rate = np.where(rising, 60 + 500 * s ** 2, 560 * np.exp(-(t - build) / 0.05) + 20)
    amp = np.where(rising, s ** 1.6, np.exp(-(t - build) / 0.07))
    crackle = _arrivals(rng, length, rate=rate, amp=amp * 0.6, lo_ms=1.0, hi_ms=5.0, heavy=0.7, lp=5000)
    # the shock: a dense burst of 40-80 arrivals inside 25 ms at the peak, long pulses for the weight
    at = int(build * SR)
    burst_len = int(SR * 0.025)
    shock = np.zeros(n)
    for _ in range(int(rng.integers(40, 80))):
        L = int(SR * rng.uniform(0.004, 0.014))
        a0 = at + int(rng.uniform(0, burst_len))
        shock[a0:a0 + L] += np.linspace(1, -1, L)[: n - a0] * rng.lognormal(0, 0.6) * rng.choice([-1, 1]) * 0.9
    shock = lowpass(shock, 900, 2)
    snap = np.zeros(n)
    sn = highpass(burst(0.02, rng, lo=600, hi=8000, tau=0.006), 600, 2) * 1.8   # the shock's own air
    snap[at:at + len(sn)] += sn[: n - at]
    y = crackle + shock + snap
    y = y / (np.abs(y).max() + 1e-9) * 1.3 * amount
    return release(y, 0.05), build


def _rumble_clap(rng, length, roar, rumble, top_hz, amp):
    """The clap as a short, loud rumble instead of a crack: the same arrivals as a roll, 40 % of its length and
    twice its level, with a fast rise. Returns (signal, seconds from its start to its peak) so the peak can be
    placed on the hit time."""
    rise = 0.04
    x = _roll(rng, length, roar, rumble, top_hz, amp, rise=rise)
    t = np.arange(len(x)) / SR
    shape = (1 - np.exp(-t / rise)) * np.exp(-(t / length) * 1.7)
    return x, float(np.argmax(shape)) / SR


def _roll(rng, length, roar, rumble, top_hz, amp, rise=0.12):
    """The rumble that rolls out of a hit: a pile of arrivals, dense at first and thinning as it falls, with the
    weight at 80-250 Hz from their length, a shorter-pulse presence layer sliding down from top_hz, and the
    whole thing bumping in slow waves."""
    n = int(round(SR * length))
    t = np.arange(n) / SR
    s = t / length
    shape = (1 - np.exp(-t / rise)) * np.exp(-s * 1.7)
    mov = _rolling(rng, n)
    low = _arrivals(rng, length, rate=50 + 200 * shape, amp=0.16 * shape * mov, lo_ms=3, hi_ms=11, heavy=1.1, lp=600) * rumble
    hi_ms = np.interp(s, [0, 1], [2.5, 6.0])
    pres = _arrivals(rng, length, rate=30 + 150 * shape, amp=0.1 * shape * mov, lo_ms=1.0, hi_ms=float(hi_ms[0]),
                     heavy=0.9, lp=min(top_hz * 2.2, 3000)) * roar
    return release((low + pres) * amp, 0.08)


def _surge(rng, length, peak_at, amount):
    """The bed under the clusters: a steady pile of arrivals that swells under the first strike and fades across
    the rest, rolling slowly. It is what the gaps are made of, and it is not wind."""
    n = int(round(SR * length))
    t = np.arange(n) / SR
    up = np.clip(t / max(peak_at, 0.05), 0, 1) ** 1.4
    down = np.exp(-np.clip(t - peak_at, 0, None) / max(0.55 * (length - peak_at), 0.2))
    env_ = up * down * _rolling(rng, n, depth=0.4)
    low = _arrivals(rng, length, rate=40 + 110 * env_, amp=0.16 * env_, lo_ms=3, hi_ms=12, heavy=1.1, lp=600)
    pres = _arrivals(rng, length, rate=20 + 60 * env_, amp=0.06 * env_, lo_ms=1.5, hi_ms=5.0, heavy=0.9, lp=1200)
    return release((low + pres) * amount * 0.8, 0.15)


@recipe("thunder", family="nature",
        doc="Thunder, measured against real strikes: a slow distant rumble, then strikes in clusters, two or three "
            "cracks close together, each collapsing into its own rumble that rolls in slow waves; irregular gaps; "
            "a secondary peal seconds later; a rumble bed under it all; a long dark reverb. The weight sits at "
            "80-250 Hz, as it does in every recording.",
        tips="approach is the distant rumble before the first hit (0 to start on the hit); clusters how many "
             "groups of strikes, per_cluster the most cracks in a group (2 to that many, 0.15-0.6 s apart; 1 = "
             "single hits); every crack has its own rumble (roll seconds, each a little different) 12-18 dB under "
             "the crack; overlap scales the irregular gaps between clusters; backoff how much quieter each later "
             "cluster is; peal the secondary peal 4-5 s after a cluster; hit the strike, rip the canvas tear in "
             "front of the first (close) one; roar the sliding mid band, rumble the 80-250 Hz weight and the sub; "
             "surge the bed under it all. Put the flash at `approach` seconds in.",
        params=[
            P("approach", 2.5, 0.0, 6.0, 0.1, "s", "slow distant rumble before the first hit"),
            P("rumble", 1.0, 0, 2, 0.05, "", "80-250 Hz weight and sub amount"),
            I("clusters", 3, 1, 6, "", "groups of strikes at irregular intervals"),
            I("per_cluster", 3, 1, 4, "", "cracks in a group at most (2 to this many, close together; 1 = single hits)"),
            P("hit", 1.0, 0, 2, 0.05, "", "strike amount"),
            P("clap", 0.0, 0, 1, 0.05, "", "replace the crack with a short loud rumble (0 = crack, 1 = rumble only)"),
            P("clap_gain", 2.0, 1, 8, 0.1, "x", "level of the rumble clap relative to the roll it sits on"),
            P("rip", 0.6, 0, 2, 0.05, "", "canvas-rip amount in front of the first (close) hit"),
            P("roll", 3.2, 1.0, 8.0, 0.1, "s", "rumble rolling out of each crack (each a little different)"),
            P("roar", 1.0, 0.2, 2, 0.05, "", "sliding mid band of the rolls"),
            P("overlap", 0.6, 0.2, 1.5, 0.05, "", "gap to the next cluster, as a fraction of the rumble (irregular, skewed short)"),
            P("backoff", 0.9, 0.3, 1.0, 0.05, "", "level of each later cluster relative to the one before"),
            P("grow", 1.1, 1.0, 2.5, 0.05, "", "length of each later cluster's rumbles relative to the one before"),
            P("peal", 0.5, 0, 1.5, 0.05, "", "secondary peal 4-5 s after each cluster"),
            P("surge", 1.2, 0, 3, 0.05, "", "long rumble bed swelling under the first hit, fading across the rest"),
            P("tail", 3.0, 0.5, 6.0, 0.1, "s", "reverb length"),
            P("wet", 0.25, 0, 0.8, 0.01, "", "reverb amount (a reverb tail is noise: keep it under the arrivals)"),
            SEED(305),
        ])
def thunder(*, approach, rumble, clusters, per_cluster, hit, clap, clap_gain, rip, roll, roar, overlap, backoff, grow,
            peal, surge, tail, wet, seed):
    rng = _rng(seed)
    parts = []
    if approach > 0:
        parts.append((0.0, pan(_approach(rng, approach, rumble), 0.0)))
    rip_len = 0.18
    t_hit = approach
    # Weather, not a machine: hits come in clusters of two or three cracks a few hundred ms apart, with irregular
    # gaps between clusters (skewed: most short, some long, never two alike). Every hit is its own seeded variation.
    i = 0
    for c in range(clusters):
        size = int(rng.integers(2, per_cluster + 1)) if per_cluster >= 2 else 1
        t_first = t_hit
        for k in range(size):
            amp = backoff ** c * (1.0 if i == 0 else rng.uniform(0.7, 1.0))
            length = roll * grow ** c * rng.uniform(0.7, 1.3)
            top = 520 * (0.85 ** c) * rng.uniform(0.8, 1.2)
            side = 0.0 if i == 0 else rng.uniform(-0.4, 0.4)
            if rip > 0 and i == 0:                                           # the tear rides the crackle's build
                parts.append((max(0.0, t_hit - rip_len), pan(_rip(rng, rip_len, rip * 0.7), 0.0)))
            # the hit's own content comes from its own stream, so the timing above is the same whatever the clap
            rng_h = _rng(seed * 1000 + i)
            if hit > 0 and clap < 1:
                cr, build = _crack(rng_h, hit * amp * (1 - clap))
                parts.append((max(0.0, t_hit - build), pan(cr, side * 0.3)))     # the peak lands on t_hit
            if hit > 0 and clap > 0:                                              # the owner's clap: a short loud rumble
                rc, off = _rumble_clap(rng_h, length * 0.4, roar, rumble, top, amp * 0.35 * clap_gain * hit * clap)
                parts.append((max(0.0, t_hit - off), pan(rc, side * 0.3)))        # its peak lands on t_hit
            # the crack is over in 0.3 s; the roll rises after a quarter-second dip, 12-18 dB under the crack
            parts.append((t_hit + 0.28, pan(_roll(rng, length, roar, rumble, top_hz=top, amp=amp * 0.35), side)))
            i += 1
            if k < size - 1:
                t_hit += rng.uniform(0.15, 0.6)                        # the next crack of the same cluster
            else:
                t_hit += roll * overlap * (0.15 + 1.6 * rng.random() ** 2.2)   # skewed irregular gap
        if peal > 0:                                                   # the secondary peal, no crack, -15 dB
            parts.append((t_first + rng.uniform(3.8, 5.2),
                          pan(_roll(rng, roll * 0.8 * grow ** c, roar, rumble, top_hz=260, amp=0.18 * peal * backoff ** c,
                                    rise=0.25), rng.uniform(-0.5, 0.5))))
    total = max(a + len(x) / SR for a, x in parts) + 0.1
    if surge > 0:
        start = approach * 0.5
        parts.append((start, pan(_surge(rng, total - start - 0.1, approach - start + 0.9, surge * rumble), 0.0)))
    st = place(parts, total)
    st = reverb(st, seconds=tail, wet=wet, seed=seed + 1, damp=1600)
    st = highpass(st, 40, 2)                      # nothing a speaker cannot make; the recordings have little under 40 Hz
    return norm(trim_tail(fade(st, 0.001, 0.1)))


@recipe("wind_loop", family="nature",
        doc="Wind: broad filtered noise with a slowly wandering whistle; a seamless loop.",
        tips="f_lo/f_hi are the whistle's travel; whistle its amount (0 for plain air); d the loop length; "
             "gust how much the level breathes.",
        params=[
            P("d", 8.0, 3.0, 30.0, 0.5, "s", "loop length (before the seam crossfade)"),
            P("f_lo", 220, 60, 1500, 10, "Hz", "whistle low point"),
            P("f_hi", 900, 200, 4000, 10, "Hz", "whistle high point"),
            P("whistle", 0.5, 0, 1.5, 0.05, "", "whistle amount"),
            P("gust", 0.5, 0, 1, 0.05, "", "level breathing depth"),
            SEED(306),
        ])
def wind_loop(*, d, f_lo, f_hi, whistle, gust, seed):
    rng = _rng(seed)
    n = int(round(SR * d))
    t = np.arange(n) / SR
    lfo = 0.5 * (1 - np.cos(2 * np.pi * t / d)) * 0.6 + 0.4 * 0.5 * (1 - np.cos(2 * np.pi * 3 * t / d + 0.8))
    fc = np.exp(np.log(f_lo) + (np.log(f_hi) - np.log(f_lo)) * lfo)
    g = 1 - gust * 0.5 * (1 - np.cos(2 * np.pi * 2 * t / d + 2.0))
    bed = lowpass(pink(n, rng), 1200, 1) * 0.7                      # one bed in both ears: no mono-sum loss
    src = pink(n, rng)
    left = (bed + svf_bandpass(src, fc, 3.0) * whistle * 1.5) * g
    right = (bed + svf_bandpass(src, fc * 1.03, 3.0) * whistle * 1.5) * g
    st = np.stack([left, right], axis=1)
    return norm(loop_seam(st, 0.4))
