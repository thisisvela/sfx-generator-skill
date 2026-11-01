"""Loudness, levels and mixing rules for code-made sound effects (numpy + scipy).

Tuned on real narrated videos. Everything works on (n, 2) float arrays at 48 kHz.

- loudness_max(x): the loudest 100 ms of a sound, K-weighted (EBU R128), in LUFS. Short clicks need the 100 ms window;
  the standard 400 ms 'momentary' window under-rates them by several dB.
- integrated(x): EBU R128 integrated loudness with gating (for narration and whole mixes).
- gain_for(sound, level_lu, ref_lufs): the gain that places a sound at `level_lu` relative to narration at `ref_lufs`,
  never letting it peak above PEAK_CAP_DB.
- limit(x): a look-ahead peak limiter without a sample loop (for the final mix).
"""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

SR = 48000

# Default level by category: the loudest 100 ms of the sound, in LU relative to the narration's integrated loudness.
# Measured in a real mix (400 ms windows) these put a whoosh or chime about 8-10 LU under the voice's own momentary
# peaks, an impact about 6 under, a pop or tick about 10 under: heard, never competing. (A first table 5 dB lower
# measured 13-19 LU under the voice and was inaudible over speech.) Title and end cards have no voice under them.
# `ambience` is for loops that run under a whole beat; they sit well under everything.
CATEGORY_LU = {"transition": -4, "appear": -4, "emphasis": -4, "ui": -6, "positive": -4, "question": -2,
               "negative": -4, "reveal": -2, "anticipation": -4, "camera": -7, "title": 2, "end": -1,
               "ambience": -16}

# Level profiles: "video" is the table above (effects under narration). "standalone" places every sound at the
# narration reference itself, for games and interfaces where nothing is spoken over it.
PROFILES = {"video": CATEGORY_LU, "standalone": {k: 0 for k in CATEGORY_LU}}

# Transition style -> default sound (an explainer's beat transitions).
TRANSITION_SFX = {"slide": "whoosh", "zoom": "whoosh_long", "rise": "whoosh_up", "fade": "whoosh_soft", "cut": None,
                  "wipe": "whoosh", "iris": "whoosh_soft", "shape": "whoosh_long", "whip": "whoosh_short",
                  "glitch": "glitch_burst"}

# Mood: how big a sound is meant to feel, decided from the situation it belongs to, never from its peak. Every
# master is peak-normalised, so a dense loop (rain, wind) sits loud all the way through while a peaky event
# (thunder: one crack, a long quiet rumble) is loud for 100 ms and then sits under the bed. A mood with a
# `body_lufs` lifts the loudest second (K-weighted) of the master to that target and lets the limiter hold the
# crack above it: the body carries the weight, the way a film mix does. None keeps the peak master as rendered.
MOODS = {
    "huge": -12.0,     # fear, violence, the sky: thunder, an explosion, a cannon, a tank, an avalanche
    "big": -14.0,     # a gunshot, a heavy impact, a door slam, a crash, a stinger
    "normal": None,   # interface and foley sounds at the level the recipe gives them; beds and loops
}

NARRATION_LUFS = -14.0  # a typical narration's integrated loudness
LOUDNESS_WINDOW = 0.1   # 100 ms: close to how loud a short click or pop sounds (400 ms under-rates them)
PEAK_CAP_DB = -6.0      # no single effect peaks above this in a mix (keeps clicks from spiking over the voice)
# ...except by mood: a huge sound (thunder) is meant to dominate the moment and may peak 3 dB higher than a big
# one, 6 dB higher than an ordinary effect; this is where a huge sound's extra weight in a mix comes from.
PEAK_CAP_BY_MOOD = {"huge": -3.0, "big": -4.5, "normal": PEAK_CAP_DB}
MAX_PER_MINUTE = 8      # density: at most about 8 sounds a minute, at least 1 s apart (real videos used 4.4)
MIN_GAP_S = 1.0


def k_weight(x):
    """EBU R128 K-weighting (high shelf + high-pass) at 48 kHz."""
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)


def momentary(x, hop=0.01, window=0.4):
    """Loudness over sliding windows (LUFS, EBU R128 K-weighting; 400 ms = 'momentary') of a (n, 2) 48 kHz signal."""
    p = (k_weight(x) ** 2).sum(axis=1)
    w, h = int(window * SR), max(1, int(hop * SR))
    if len(p) < w:
        p = np.concatenate([p, np.zeros(w - len(p))])
    c = np.concatenate([[0.0], np.cumsum(p)])
    starts = np.arange(0, len(p) - w + 1, h)
    ms = (c[starts + w] - c[starts]) / w
    return -0.691 + 10 * np.log10(np.maximum(ms, 1e-12))


def loudness_max(x, window=LOUDNESS_WINDOW) -> float:
    """The loudest `window` seconds, K-weighted, in LUFS."""
    return float(momentary(x, window=window).max())


def integrated(x: np.ndarray) -> float:
    """Integrated loudness (EBU R128 with gating) of a 48 kHz stereo signal."""
    m = momentary(x, hop=0.1)                     # 400 ms blocks, 75% overlap as in BS.1770
    m = m[m > -70]
    if not len(m):
        return -70.0
    rel = 10 * np.log10(np.mean(10 ** (m / 10))) - 10
    g = m[m > rel]
    return float(10 * np.log10(np.mean(10 ** (g / 10)))) if len(g) else -70.0


def peak_dbfs(x) -> float:
    return float(20 * np.log10(np.abs(x).max() + 1e-12))


def gain_for(x, level_lu: float, ref_lufs: float = NARRATION_LUFS, peak_cap_db: float = PEAK_CAP_DB) -> float:
    """dB of gain that puts sound x at level_lu relative to narration at ref_lufs, capped so it never peaks above
    PEAK_CAP_DB. When the cap wins the sound is quieter than asked ('capped'): give short clicks a little tonal body
    instead of raising them, since a bare 2-4 ms transient carries little loudness for its peak."""
    return min(ref_lufs + level_lu - loudness_max(x), peak_cap_db - peak_dbfs(x))


def placement(x, category: str, ref_lufs: float = NARRATION_LUFS, profile: str = "video",
              level_lu: float | None = None, mood: str = "normal") -> dict:
    """Where a sound sits against narration: the gain to apply, whether the peak cap won, and the level reached.
    level_lu overrides the category's level (a preset's own level); mood picks the peak cap (PEAK_CAP_BY_MOOD)."""
    level = PROFILES[profile][category] if level_lu is None else level_lu
    g = gain_for(x, level, ref_lufs, PEAK_CAP_BY_MOOD[mood])
    asked = ref_lufs + level - loudness_max(x)
    return {"level_lu": level, "gain_db": round(g, 2), "capped": bool(g < asked - 1e-9),
            "in_mix_lu": round(loudness_max(x) + g - ref_lufs, 2)}


def presence(x: np.ndarray, amount: float) -> np.ndarray:
    """Small-speaker presence. A laptop or phone speaker plays little under 250 Hz, so a sound whose weight sits
    there (thunder, an explosion) loses 5-10 dB on it while a whoosh loses nothing. Generate harmonics of the
    low band (soft saturation of everything under 250 Hz, then 200-1200 Hz kept) and mix them in: the ear
    hears the missing fundamental, the dynamics stay (louder lows make louder harmonics), nothing else moves.
    amount 0 = off; 0.5-0.8 brings a sub-heavy sound within about 2 dB of its full-band loudness on a laptop."""
    if amount <= 0:
        return x
    from scipy.signal import butter, sosfilt
    low = sosfilt(butter(2, 250, "lp", fs=SR, output="sos"), x, axis=0)
    rms = np.sqrt((low ** 2).mean()) + 1e-9
    drive = 2.5 / rms                                                   # the band's RMS well into tanh's bend
    h = np.tanh(low * drive) + 0.35 * np.tanh(low * drive) ** 2 * np.sign(low)   # odd harmonics plus a 2nd
    harm = sosfilt(butter(2, [200, 1200], "bp", fs=SR, output="sos"), h, axis=0)
    harm *= rms / (np.sqrt((harm ** 2).mean()) + 1e-9)                 # harmonics at the low band's own RMS...
    peak = np.abs(low).max()
    harm = np.clip(harm * amount * 2.4, -peak, peak)                    # ...never peakier than the band itself
    # the low band's peaks set the file's ceiling yet a small speaker cannot play them: tame them by up to 8 dB
    # (a 40 ms look-ahead limiter on the band alone) so the normaliser can lift everything the speaker does play;
    # (this costs the band some of its impulsiveness, which a small speaker never hears; the 250-1200 Hz
    # harmonics keep the arrivals' shape for headphones)
    tamed, _ = limit(low, 20 * np.log10(peak + 1e-9) - 8 * min(1.0, amount / 0.7))
    return (x - low) + tamed + harm


def master(x: np.ndarray, mood: str = "normal", ceiling_db: float = -1.5, presence_amount: float = 0.0) -> np.ndarray:
    """The mood master: small-speaker presence first (if asked), then lift the loudest second of the sound to
    MOODS[mood] (LUFS), hold the peaks above it with the limiter, and land the peak at ceiling_db. A mood of
    "normal" with no presence returns the sound untouched, so the originals stay bit-identical."""
    target = MOODS[mood]
    if target is None and presence_amount <= 0:
        return x
    y = presence(x, presence_amount)
    if target is None:
        return y * (10 ** (ceiling_db / 20) / (np.abs(y).max() + 1e-9))
    for _ in range(4):                                     # the limiter pulls the body down a little: iterate
        body = float(momentary(y, window=1.0).max())
        if body >= target - 0.3:
            break
        y, _ = limit(y * 10 ** ((target - body) / 20), ceiling_db)
    return y * (10 ** (ceiling_db / 20) / (np.abs(y).max() + 1e-9))


def body_lufs(x: np.ndarray) -> float:
    """The loudest second of a sound, K-weighted: what a mood master targets."""
    return float(momentary(x, window=1.0).max())


def mono_sum_drop_db(x) -> float:
    """How much level is lost when L+R is summed to mono (phase cancellation check). 0 for a centred mono source."""
    st = loudness_max(x)
    m = x.mean(axis=1)
    mono = np.stack([m, m], axis=1)
    return round(st - loudness_max(mono), 2)


def limit(x: np.ndarray, ceiling_db=-1.5, window=0.04) -> tuple[np.ndarray, int]:
    """Peak limiter without a sample loop: the gain is a moving minimum (window) smoothed by a moving average of half
    that width, so it starts falling about 20 ms before a peak, never lets one through and recovers smoothly."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    c = 10 ** (ceiling_db / 20)
    a = np.abs(x).max(axis=1)
    need = np.minimum(1.0, c / np.maximum(a, 1e-9))
    over = int((need < 1.0).sum())
    if not over:
        return x, 0
    w = max(3, int(window * SR))
    g = uniform_filter1d(minimum_filter1d(need, size=w), size=w // 2)
    return x * np.minimum(g, need)[:, None], over
