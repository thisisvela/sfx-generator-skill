"""What a rain drop sounds like: find the individual drops in a recording (or our render) and measure each.

  python -I tools/drops_analysis.py <repo-root> <file-or-preset> ...

Per sound: drops per second, and over the loudest 25 drops the median of: length to -20 dB, attack to peak,
centroid, band shares, the pitch track of the ring (five 10 ms windows after the peak: Hz and tonal strength), and
how the pitch moves (up, down, none).
"""
import sys
from math import gcd
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt, welch

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "src"))
from sfx_generator import presets  # noqa: E402

SR = 48000


def load(arg):
    if "." in Path(arg).name and not Path(arg).exists():
        raise SystemExit(f"no such file: {arg}")
    if "." in Path(arg).name and Path(arg).exists():
        x, sr = sf.read(arg, always_2d=True)
        m = x.mean(axis=1)
        if sr != SR:
            g = gcd(SR, sr)
            m = resample_poly(m, SR // g, sr // g)
        return Path(arg).name[:36], m / (np.abs(m).max() + 1e-9)
    m = presets.load_all()[arg].render().mean(axis=1)
    return "OURS " + arg, m / (np.abs(m).max() + 1e-9)


def onsets(m):
    """Drops: peaks of a 2 ms envelope that rise 12 dB above the 50 ms before them, at least 40 ms apart."""
    hop = int(SR * 0.002)
    e = np.array([np.abs(m[i:i + hop]).max() for i in range(0, len(m) - hop, hop)])
    db = 20 * np.log10(e + 1e-9)
    out = []
    last = -1e9
    for i in range(25, len(db) - 25):
        if db[i] == db[i - 5:i + 6].max() and db[i] > np.median(db[i - 25:i - 2]) + 12 and db[i] > db.max() - 40 and (i - last) * 0.002 > 0.04:
            out.append(i * hop)
            last = i
    return out


def pitch(seg):
    out = []
    w = int(SR * 0.01)
    for a in range(0, min(len(seg), w * 5), w):
        s = seg[a:a + w] - seg[a:a + w].mean()
        if np.abs(s).max() < 1e-4 or len(s) < w:
            out.append((0, 0.0))
            continue
        ac = np.correlate(s, s, "full")[w - 1:]
        ac /= ac[0] + 1e-12
        lo, hi = SR // 8000, SR // 300
        k = lo + int(np.argmax(ac[lo:hi]))
        out.append((int(SR / k), round(float(ac[k]), 2)))
    return out


def shares(seg):
    f, p = welch(seg, SR, nperseg=min(1024, len(seg)))
    tot = p[f >= 100].sum() + 1e-18
    return {k: round(10 * np.log10(p[(f >= lo) & (f < hi)].sum() / tot + 1e-12), 1)
            for k, lo, hi in [("<500", 100, 500), ("500-2k", 500, 2000), ("2k-5k", 2000, 5000), ("5k-10k", 5000, 10000), (">10k", 10000, 24000)]}


for arg in sys.argv[2:]:
    name, m = load(arg)
    ons = onsets(m)
    print(f"\n== {name}: {len(m) / SR:.1f} s, {len(ons)} drops found ({len(ons) / (len(m) / SR):.1f} a second)")
    if not ons:
        continue
    loud = [i for i in sorted(ons, key=lambda i: -np.abs(m[i:i + int(SR * 0.01)]).max()) if i + int(SR * 0.26) < len(m)][:25]
    lens, atks, cents, ups, downs, flats, strengths = [], [], [], 0, 0, 0, []
    bands = []
    for i in loud:
        seg = m[max(0, i - int(SR * 0.005)):i + int(SR * 0.25)]
        pk = int(np.argmax(np.abs(seg)))
        atks.append(pk / SR * 1000)
        env = np.abs(seg[pk:])
        hop = int(SR * 0.002)
        e = np.array([env[j:j + hop].max() for j in range(0, len(env) - hop, hop)])
        if len(e) < 3:
            continue
        below = np.nonzero(e < e[0] * 0.1)[0]
        lens.append((below[0] * 0.002 * 1000) if len(below) else 250)
        f, p = welch(seg[pk:pk + int(SR * 0.06)], SR, nperseg=512)
        cents.append((f * p).sum() / (p.sum() + 1e-18))
        bands.append(shares(seg[pk:pk + int(SR * 0.06)]))
        pt = pitch(seg[pk:])
        hz = [h for h, s_ in pt if s_ > 0.3]
        strengths.append(max(s_ for _, s_ in pt))
        if len(hz) >= 2:
            if hz[-1] > hz[0] * 1.08:
                ups += 1
            elif hz[-1] < hz[0] / 1.08:
                downs += 1
            else:
                flats += 1
    med = lambda v: round(float(np.median(v)), 1)  # noqa: E731
    print(f"   loudest 25 drops: length to -20 dB {med(lens)} ms, attack {med(atks)} ms, centroid {int(np.median(cents))} Hz")
    print(f"   bands (median): {{{', '.join(f'{k}: {np.median([b[k] for b in bands]):.1f}' for k in bands[0])}}}")
    print(f"   tonal ring: strength {med(strengths)} (1 = pure tone); pitch moves up {ups}, down {downs}, flat {flats}, none {25 - ups - downs - flats}")
    i = loud[0]
    print(f"   loudest drop pitch track (10 ms steps, Hz/strength): {pitch(m[i:i + int(SR * 0.06)])}")
