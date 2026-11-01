"""Compare recordings with our renders by the same numbers (the standard comparison for natural sounds).

  python -I tools/analyse_recordings.py <repo-root> <file-or-preset-id> ...

A preset id (no dot) is rendered from the library; anything else is read as a file. Prints, per sound:
  seconds, crest factor (peak over RMS), spectral centroid, slope dB/octave 100 Hz-8 kHz, band energy shares,
  modulation (where the envelope's energy sits, 0.5-4 / 4-16 / 16-64 Hz), and for event sounds the event list
  (peaks of a 50 ms RMS envelope above the floor: time, level, and the -20 dB decay of each).
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt, welch

SR = 48000
BANDS = [("sub<80", 20, 80), ("low80-250", 80, 250), ("mid250-1k", 250, 1000), ("hi1k-4k", 1000, 4000), ("air>4k", 4000, 20000)]


def load(path):
    x, sr = sf.read(str(path), always_2d=True)
    m = x.mean(axis=1)
    if sr != SR:
        from math import gcd
        g = gcd(SR, sr)
        m = resample_poly(m, SR // g, sr // g)
    return m.astype(float)


def band_shares(m):
    f, p = welch(m, SR, nperseg=8192)
    tot = p[(f >= 20) & (f < 20000)].sum() + 1e-18
    out = {}
    for name, lo, hi in BANDS:
        out[name] = round(10 * np.log10(p[(f >= lo) & (f < hi)].sum() / tot + 1e-12), 1)
    sel = (f >= 100) & (f <= 8000)
    slope = np.polyfit(np.log2(f[sel]), 10 * np.log10(p[sel] + 1e-18), 1)[0]
    cen = int((f * p).sum() / (p.sum() + 1e-18))
    return out, round(slope, 1), cen


def modulation(m):
    env = np.abs(sosfilt(butter(2, 2000, "hp", fs=SR, output="sos"), m))        # the hiss/texture envelope
    hop = 240                                                                     # 200 Hz envelope rate
    e = np.array([env[i:i + hop].mean() for i in range(0, len(env) - hop, hop)])
    e = e - e.mean()
    f, p = welch(e, 200, nperseg=min(1024, len(e)))
    tot = p[(f >= 0.5)].sum() + 1e-18
    return {k: round(10 * np.log10(p[(f >= lo) & (f < hi)].sum() / tot + 1e-12), 1)
            for k, lo, hi in [("0.5-4Hz", 0.5, 4), ("4-16Hz", 4, 16), ("16-64Hz", 16, 64)]}


def events(m, floor_db=-45):
    hop = int(SR * 0.05)
    rms = np.array([np.sqrt((m[i:i + hop] ** 2).mean()) for i in range(0, len(m) - hop, hop)])
    db = 20 * np.log10(rms / (rms.max() + 1e-12) + 1e-12)
    floor = np.percentile(db, 30)
    out = []
    i = 2
    while i < len(db) - 2:
        if db[i] == db[i - 2:i + 3].max() and db[i] > max(floor + 10, floor_db):
            j = i
            while j < len(db) and db[j] > db[i] - 20:
                j += 1
            out.append((round(i * 0.05, 2), round(float(db[i]), 1), round((j - i) * 0.05, 2)))
            i = j
        else:
            i += 1
    return out, round(float(floor), 1)


def describe(name, m):
    rms = np.sqrt((m ** 2).mean()) + 1e-12
    crest = 20 * np.log10(np.abs(m).max() / rms)
    shares, slope, cen = band_shares(m)
    print(f"\n== {name}: {len(m) / SR:.1f} s, crest {crest:.1f} dB, centroid {cen} Hz, slope {slope} dB/oct")
    print("   bands dB of total:", shares)
    print("   texture modulation:", modulation(m))
    ev, floor = events(m)
    if ev:
        print(f"   events (t, dB re max, -20 dB decay s), floor {floor} dB:")
        for e in ev[:14]:
            print("     ", e)
        if len(ev) > 1:
            gaps = np.diff([e[0] for e in ev])
            print(f"   gaps between events: min {gaps.min():.2f} median {np.median(gaps):.2f} max {gaps.max():.2f} s")


def main():
    root = Path(sys.argv[1])
    sys.path.insert(0, str(root / "src"))
    from sfx_generator import presets
    lib = presets.load_all()
    for arg in sys.argv[2:]:
        if "." in Path(arg).name and Path(arg).exists():
            describe(Path(arg).name, load(arg))
        else:
            x = lib[arg].render()
            describe(f"OURS {arg}", x.mean(axis=1))


main()
