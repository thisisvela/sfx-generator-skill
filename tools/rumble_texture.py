"""What makes a rumble a rumble and not wind: the texture of the 80-250 Hz band in the rumble section.

  python -I tools/rumble_texture.py <repo-root> <file-or-preset[:t0:t1]> ...

Per sound: kurtosis of the band signal (3 = Gaussian noise/wind; higher = impulsive, made of arrivals), the
band envelope's crest (peak over mean), its modulation spectrum (0.5-4 / 4-16 / 16-64 / 64-200 Hz shares), and
the same for the 250-1000 Hz band.
"""
import sys
from math import gcd
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, hilbert, resample_poly, sosfiltfilt, welch
from scipy.stats import kurtosis

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "src"))
from sfx_generator import presets  # noqa: E402

SR = 48000


def load(arg):
    import re
    mm = re.match(r"^(.*?):([0-9.]+):([0-9.]+)$", arg)
    src = mm.group(1) if mm else arg
    t0, t1 = (float(mm.group(2)), float(mm.group(3))) if mm else (None, None)
    if "." in Path(src).name and not Path(src).exists():
        raise SystemExit(f"no such file: {src}")
    if "." in Path(src).name and Path(src).exists():
        x, sr = sf.read(src, always_2d=True)
        m = x.mean(axis=1)
        if sr != SR:
            g = gcd(SR, sr)
            m = resample_poly(m, SR // g, sr // g)
        name = Path(src).name[:30]
    else:
        m = presets.load_all()[src].render().mean(axis=1)
        name = "OURS " + src
    if t0 is None:                       # default: 3-8 s after the loudest crack (the rumble)
        i = int(np.argmax(np.abs(m)))
        t0, t1 = i / SR + 3, i / SR + 8
    return f"{name} [{t0:.1f}-{t1:.1f} s]", m[int(t0 * SR):int(t1 * SR)]


def texture(seg, lo, hi):
    b = sosfiltfilt(butter(4, [lo, hi], "bp", fs=SR, output="sos"), seg)
    env = np.abs(hilbert(b))
    k = kurtosis(b)
    crest = env.max() / (env.mean() + 1e-12)
    hop = 48                                            # 1 kHz envelope rate
    e = env[: len(env) // hop * hop].reshape(-1, hop).mean(axis=1)
    e = e - e.mean()
    f, p = welch(e, 1000, nperseg=min(2048, len(e)))
    tot = p[f >= 0.5].sum() + 1e-18
    mod = {kk: round(10 * np.log10(p[(f >= a) & (f < bb)].sum() / tot + 1e-12), 1)
           for kk, a, bb in [("0.5-4", 0.5, 4), ("4-16", 4, 16), ("16-64", 16, 64), ("64-200", 64, 200)]}
    return round(float(k), 1), round(float(crest), 1), mod


for arg in sys.argv[2:]:
    name, seg = load(arg)
    print(f"\n== {name}")
    for lo, hi in [(80, 250), (250, 1000)]:
        k, c, mod = texture(seg, lo, hi)
        print(f"   {lo}-{hi} Hz: kurtosis {k} (3 = noise), envelope crest {c}, modulation {mod}")
