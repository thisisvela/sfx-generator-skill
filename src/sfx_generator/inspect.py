"""Check a sound without listening to it: numbers, defect warnings, a spectrogram and a waveform.

No model can hear. Every sound in the library was verified by comparing these numbers and pictures against a
reference, then a person listened. What to look for:

- vertical lines in the spectrogram: clicks (a note cut while still ringing; add a release fade);
- a smear at 0 Hz: DC (remove the mean or high-pass at 80-120 Hz);
- a tail that runs on past the picture: a reverb or decay too long for speech to follow;
- `end_level_db` above -40: it ends while still sounding;
- a very short sound (under 0.1 s of energy): it will vanish under a voice.
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

import numpy as np
from scipy.signal import spectrogram as _spectrogram
from scipy.signal import stft

from . import levels
from .blocks import SR


def describe(x: np.ndarray) -> dict:
    """Length, attack, decay to -20 dB, centroid, pitch track, DC, end level, peak and loudness."""
    mono = x.mean(axis=1) if x.ndim == 2 else x
    if len(mono) < 1024:
        mono = np.concatenate([mono, np.zeros(1024 - len(mono))])
    f, _, Z = stft(mono, SR, nperseg=1024, noverlap=896)
    A = np.abs(Z)
    e = A.sum(axis=0)
    keep = e > e.max() * 0.05
    peaks = [int(f[1 + np.argmax(A[1:, i])]) for i in range(A.shape[1]) if keep[i]]   # skip the 0 Hz bin
    track = [peaks[int(k)] for k in np.linspace(0, len(peaks) - 1, min(5, len(peaks)))] if peaks else []
    spec = A[:, keep].mean(axis=1) if keep.any() else A.mean(axis=1)
    env = np.abs(x).max(axis=1) if x.ndim == 2 else np.abs(x)
    i = int(np.argmax(env))
    after = np.nonzero(env[i:] > env[i] * 0.1)[0]
    tail = np.abs(x[-int(SR * 0.002):]).max() if len(x) > SR * 0.002 else 0.0
    return {
        "seconds": round(len(x) / SR, 3),
        "attack_s": round(i / SR, 3),
        "decay_to_-20dB_s": round(float(after[-1]) / SR, 3) if len(after) else 0.0,
        "centroid_hz": int((f * spec).sum() / (spec.sum() + 1e-12)),
        "pitch_track_hz": track,
        "dc_offset": round(float(mono.mean()), 5),
        "end_level_db": round(20 * np.log10(tail / (np.abs(x).max() + 1e-12) + 1e-12), 1),
        "peak_dbfs": round(levels.peak_dbfs(x), 2),
        "loudness_max_lufs": round(levels.loudness_max(x), 2),
        "mono_sum_drop_db": levels.mono_sum_drop_db(x) if x.ndim == 2 else 0.0,
        "nan": bool(np.isnan(x).any()),
    }


def warnings(d: dict, loop: bool = False) -> list[str]:
    w = []
    if d["nan"]:
        w.append("NaN samples: a division by zero or an empty buffer somewhere")
    if abs(d["dc_offset"]) > 0.002 and d["seconds"] > 0.15:   # short thumps have a harmless net mean
        w.append("DC offset: remove the mean / high-pass at 80-120 Hz")
    if d["end_level_db"] > -40 and not loop:
        w.append("ends while still sounding: add a release fade (a cut is a click)")
    if d["decay_to_-20dB_s"] < 0.03 and d["seconds"] < 0.1:
        w.append("very short: it may vanish under speech; give it 0.1 s or more of energy or some tonal body")
    if abs(d["peak_dbfs"] + 1.5) > 0.1:
        w.append(f"peak {d['peak_dbfs']} dBFS: masters are normalised to -1.5 dBFS")
    if d["mono_sum_drop_db"] > 3:
        w.append("mono sum loses more than 3 dB: left/right phase cancellation; reduce the stereo offset")
    if d["centroid_hz"] < 120 and not loop:
        w.append("sub-only (centroid under 120 Hz): inaudible on laptop and phone speakers, and K-weighting hides it "
                 "from the level rule; add a mid-range knock or body (200-700 Hz)")
    return w


def report(x: np.ndarray, category: str | None = None, loop: bool = False) -> dict:
    d = describe(x)
    if category:
        d.update({f"video_{k}": v for k, v in levels.placement(x, category).items()})
    d["warnings"] = warnings(d, loop)
    return d


# ---- pictures (dependency-free: an 8-bit greyscale PNG and a hairline SVG) ------------------------------------
def _png_grey(img: np.ndarray) -> bytes:
    """Encode a (h, w) uint8 array as a greyscale PNG."""
    h, w = img.shape
    raw = b"".join(b"\x00" + img[r].tobytes() for r in range(h))

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def spectrogram_png(x: np.ndarray, path: Path | str, width=480, height=160, fmax=12000, floor_db=-90,
                    ceil_db=-20) -> Path:
    """A greyscale spectrogram, ink on white (dark = loud), 0 to fmax Hz, the whole sound wide."""
    mono = x.mean(axis=1) if x.ndim == 2 else x
    if len(mono) < 1024:
        mono = np.concatenate([mono, np.zeros(1024 - len(mono))])
    f, t, S = _spectrogram(mono, SR, nperseg=512, noverlap=448)
    S = 10 * np.log10(S + 1e-12)
    S = S[f <= fmax]
    # resample to the picture size (nearest), low frequencies at the bottom
    rows = np.linspace(0, S.shape[0] - 1, height).astype(int)[::-1]
    cols = np.linspace(0, S.shape[1] - 1, width).astype(int)
    img = S[rows][:, cols]
    v = np.clip((img - floor_db) / (ceil_db - floor_db), 0, 1)
    grey = (255 - v * 235).astype(np.uint8)       # white background, dark ink
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_png_grey(grey))
    return path


def waveform_svg(x: np.ndarray, width=480, height=64, columns=240, stroke="currentColor") -> str:
    """A hairline waveform (min/max per column) as an SVG string that inherits the page's text colour."""
    mono = x.mean(axis=1) if x.ndim == 2 else x
    n = len(mono)
    edges = np.linspace(0, n, columns + 1).astype(int)
    mid = height / 2
    amp = (height / 2 - 1) / (np.abs(mono).max() + 1e-9)
    parts = []
    for i in range(columns):
        seg = mono[edges[i]:edges[i + 1]]
        if not len(seg):
            continue
        lo, hi = float(seg.min()), float(seg.max())
        xx = (i + 0.5) * width / columns
        parts.append(f"M{xx:.1f} {mid - hi * amp:.1f}V{mid - lo * amp:.1f}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'preserveAspectRatio="none" aria-hidden="true"><path d="{"".join(parts)}" stroke="{stroke}" '
            f'stroke-width="1" fill="none" stroke-linecap="round"/></svg>')


def format_report(d: dict) -> str:
    lines = [f"{k:22} {v}" for k, v in d.items() if k != "warnings"]
    lines += [f"WARN {w}" for w in d.get("warnings", [])]
    return "\n".join(lines)
