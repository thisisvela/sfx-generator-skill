"""Building blocks for code-made sound effects (numpy + scipy only).

Every recipe in `sfx_generator.recipes` is built from these. They are a verbatim port of the reference generator that
made the first 37 sounds, so the shipped presets regenerate bit for bit. Two things to keep when editing:

- `_t(d)` uses int(SR * d) and `_tr(d)` uses int(round(SR * d)). They differ for some lengths (48000 * 2.4 is
  115199.99...). Each recipe was approved with one of them; keep the variant it uses.
- Always integrate frequency into phase (`osc`), never write sin(2*pi*f(t)*t) for a moving f.

Masters are 48 kHz stereo float arrays shaped (n, 2), peak-normalised to -1.5 dBFS by `norm`.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter, sosfilt

SR = 48000


def _t(d):
    """Sample times for d seconds (truncating)."""
    return np.arange(int(SR * d)) / SR


def _tr(d):
    """Sample times for d seconds (rounded, so 0.06 s is exactly 2880 samples)."""
    return np.arange(int(round(SR * d))) / SR


def _rng(seed):
    return np.random.default_rng(int(seed))


# ---- noise ---------------------------------------------------------------------------------------------------
def pink(n, rng):
    """Pink noise, peak-normalised (4-pole IIR approximation, 2000 warm-up samples dropped)."""
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1, -2.494956002, 2.017265875, -0.522189400]
    x = lfilter(b, a, rng.standard_normal(n + 2000))[2000:]
    return x / (np.abs(x).max() + 1e-9)


def white(n, rng):
    """White noise, peak-normalised."""
    x = rng.standard_normal(n)
    return x / (np.abs(x).max() + 1e-9)


# ---- filters -------------------------------------------------------------------------------------------------
def svf_bandpass(x, fc, q):
    """Time-varying band-pass (TPT state-variable filter), unity gain at fc. fc and q: arrays (Hz, Q) or scalars."""
    n = len(x)
    fc = np.broadcast_to(np.asarray(fc, float), (n,))
    q = np.broadcast_to(np.asarray(q, float), (n,))
    g = np.tan(np.pi * np.clip(fc, 20, SR * 0.45) / SR)
    k = 1.0 / q
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    out = np.empty(n)
    ic1 = ic2 = 0.0
    for i in range(n):
        v3 = x[i] - ic2
        v1 = a1[i] * ic1 + a2[i] * v3
        v2 = ic2 + a2[i] * ic1 + a3[i] * v3
        ic1 = 2 * v1 - ic1
        ic2 = 2 * v2 - ic2
        out[i] = v1 * k[i]   # unity gain at fc
    return out


def lowpass(x, fc, order=2):
    """Butterworth low-pass (SOS). Works on mono or (n, 2) arrays."""
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x, axis=0)


def highpass(x, fc, order=2):
    """Butterworth high-pass (SOS). HP at 120 Hz kills DC."""
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x, axis=0)


def logsweep(points, n):
    """Piecewise log-frequency curve through (position 0-1, Hz) points."""
    pos = np.linspace(0, 1, n)
    xs, ys = zip(*points)
    return np.exp(np.interp(pos, xs, np.log(ys)))


# ---- space ---------------------------------------------------------------------------------------------------
def pan(mono, p):
    """Equal-power pan; p from -1 (left) to 1 (right), scalar or array."""
    p = np.broadcast_to(np.asarray(p, float), mono.shape)
    a = (p + 1) * np.pi / 4
    return np.stack([mono * np.cos(a), mono * np.sin(a)], axis=1)


def reverb(stereo, seconds=1.2, wet=0.18, seed=7, damp=6000):
    """Convolution with a synthetic impulse: two channels of white noise, -60 dB at `seconds`, low-passed at `damp`,
    a 12 ms fade-in for a pre-delay feel, energy-normalised. No room recordings needed."""
    rng = _rng(seed)
    n = int(SR * seconds)
    t = np.arange(n) / SR
    env = np.exp(-6.9 * t / seconds)          # -60 dB at `seconds`
    ir = np.stack([white(n, rng) * env, white(n, rng) * env], axis=1)
    ir = lowpass(ir, damp, 1)
    ir[: int(SR * 0.012)] *= np.linspace(0, 1, int(SR * 0.012))[:, None]   # short pre-delay feel
    ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True)) + 1e-9
    wet_sig = np.stack([fftconvolve(stereo[:, c], ir[:, c]) for c in range(2)], axis=1)
    dry = np.zeros_like(wet_sig)
    dry[: len(stereo)] = stereo
    return dry + wet * wet_sig


def room(st, wet=0.1, seconds=0.35, seed=31):
    """A small synthetic room that glues interface sounds."""
    return reverb(st, seconds=seconds, wet=wet, seed=seed, damp=7000)


# ---- edges and levels ------------------------------------------------------------------------------------------
def fade(x, a=0.004, r=0.03):
    """Linear fade-in over a seconds and fade-out over r seconds."""
    x = x.copy()
    na, nr = int(SR * a), int(SR * r)
    if na:
        x[:na] *= np.linspace(0, 1, na)[:, None] if x.ndim == 2 else np.linspace(0, 1, na)
    if nr:
        x[-nr:] *= np.linspace(1, 0, nr)[:, None] if x.ndim == 2 else np.linspace(1, 0, nr)
    return x


def norm(x, peak_db=-1.5):
    """Peak-normalise to peak_db dBFS."""
    return x * (10 ** (peak_db / 20) / (np.abs(x).max() + 1e-9))


def trim_tail(x, floor_db=-62):
    """Cut the silent tail (below floor_db of the peak), keeping 20 ms and fading it."""
    a = np.abs(x).max(axis=1) if x.ndim == 2 else np.abs(x)
    keep = np.nonzero(a > a.max() * 10 ** (floor_db / 20))[0]
    end = min(len(x), (keep[-1] if len(keep) else len(x)) + int(SR * 0.02))
    return fade(x[:end], 0, 0.02)


def release(x, r=0.04):
    """Cosine fade over the last r seconds, so nothing stops while it is still ringing (a cut is a click)."""
    x = np.array(x, dtype=float, copy=True)
    n = min(len(x), int(SR * r))
    if n > 1:
        w = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, n)))
        x[-n:] *= w[:, None] if x.ndim == 2 else w
    return x


def finish(st, tail=True, fade_out=0.015):
    """The standard last step for interface sounds: LP 15 kHz, trim or fade, normalise."""
    st = lowpass(st, 15000, 2)
    st = trim_tail(st) if tail else fade(st, 0.0, fade_out)
    return norm(fade(st, 0.0005, fade_out))


# ---- tones ---------------------------------------------------------------------------------------------------
def env(t, attack=0.002, tau=0.05):
    """Linear attack, exponential decay (tau = time to fall to 37 %; about 2.3 tau to -20 dB)."""
    return np.clip(t / max(attack, 1e-6), 0, 1) * np.exp(-np.maximum(t - attack, 0) / tau)


def glide(f0, f1, t, tc):
    """Frequency moving exponentially from f0 towards f1 with time constant tc."""
    return f1 + (f0 - f1) * np.exp(-t / tc)


def osc(freq, t, phase=0.0):
    """Sine at a constant or time-varying frequency (Hz, scalar or array): frequency is integrated into phase."""
    f = np.broadcast_to(np.asarray(freq, float), t.shape)
    return np.sin(2 * np.pi * np.cumsum(f) / SR + phase)


def tone(f0, t, spec, attack=0.002):
    """Sum of partials: spec = [(ratio, amp, tau), ...], released over the last quarter (max 80 ms).
    Inharmonic ratios give bells and glass: bell (1, 2.0, 2.76, 5.4), glass (1, 2.32, 4.25), marimba (1, 3.93, 9.2)."""
    out = np.zeros_like(t)
    for ratio, amp, tau in spec:
        out += amp * osc(np.asarray(f0) * ratio, t) * env(t, attack, tau)
    return release(out, min(0.08, 0.25 * len(t) / SR))


def place(parts, d):
    """Mix (start_seconds, mono or stereo array) parts into one stereo buffer of d seconds (12 ms safety release)."""
    out = np.zeros((int(round(SR * d)), 2))
    for start, x in parts:
        x = pan(x, 0.0) * np.sqrt(2) if x.ndim == 1 else x
        x = release(x, 0.012)
        a = int(round(start * SR))
        b = min(len(out), a + len(x))
        if b > a:
            out[a:b] += x[: b - a]
    return out


def burst(d, rng, lo=None, hi=None, tau=0.003, attack=0.0004):
    """A short noise transient, optionally band-limited (clicks, knocks, strikes)."""
    t = _tr(d)
    x = white(len(t), rng)
    if hi:
        x = lowpass(x, hi, 2)
    if lo:
        x = highpass(x, lo, 2)
    return x * env(t, attack, tau)


def ks_pluck(f0, d, seed, damp=0.996, bright=0.6):
    """Karplus-Strong plucked string with fractional delay. The excitation's mean is removed and the output
    high-passed, or DC circulates in the loop as a rumble."""
    rng = _rng(seed)
    n = int(SR * d)
    period = SR / f0
    N = int(period)
    frac = period - N
    exc = white(N + 2, rng)
    exc = bright * exc + (1 - bright) * np.convolve(exc, [0.5, 0.5], "same")
    exc -= exc.mean()                     # no DC: it would circulate in the loop as a low rumble
    y = np.zeros(n + N + 2)
    y[: N + 2] = exc
    for i in range(N + 2, n + N + 2):
        a = y[i - N]
        b = y[i - N - 1]
        y[i] = damp * ((1 - frac) * (0.5 * (a + b)) + frac * b)
    return highpass(y[N + 2:], 120, 2)


# ---- helpers used by the newer recipes -------------------------------------------------------------------------
def mix(parts, n=None):
    """Sum stereo arrays of different lengths into one (n, 2) buffer."""
    parts = [pan(p, 0.0) * np.sqrt(2) if p.ndim == 1 else p for p in parts]
    n = n or max(len(p) for p in parts)
    out = np.zeros((n, 2))
    for p in parts:
        m = min(n, len(p))
        out[:m] += p[:m]
    return out


def saw(freq, t, harmonics=12):
    """A band-limited saw: the first `harmonics` partials at 1/k (frequency integrated into phase)."""
    f = np.broadcast_to(np.asarray(freq, float), t.shape)
    ph = 2 * np.pi * np.cumsum(f) / SR
    out = np.zeros_like(t)
    for k in range(1, harmonics + 1):
        out += np.sin(k * ph) / k
    return out * (2 / np.pi)


def square(freq, t, harmonics=7):
    """A band-limited square: odd partials at 1/k."""
    f = np.broadcast_to(np.asarray(freq, float), t.shape)
    ph = 2 * np.pi * np.cumsum(f) / SR
    out = np.zeros_like(t)
    for k in range(1, 2 * harmonics, 2):
        out += np.sin(k * ph) / k
    return out * (4 / np.pi)


def loop_seam(x, cross=0.05):
    """Make a buffer loop seamlessly: crossfade the tail into the head and drop the tail. Returns a shorter array
    whose end flows into its start (test the seam by playing it twice)."""
    n = int(SR * cross)
    if n <= 1 or len(x) <= 2 * n:
        return x
    w = np.linspace(0, 1, n)
    w = w[:, None] if x.ndim == 2 else w
    head = x[:n] * w + x[-n:] * (1 - w)
    return np.concatenate([head, x[n:-n]], axis=0)
