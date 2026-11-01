"""What a laptop speaker is left with: the loudness of a render after a 4th-order 250 Hz high-pass (a small
speaker plays little under that), K-weighted, loudest second and integrated, next to the full-band numbers.

  python -I tools/laptop_check.py <repo-root> [preset_id ...]

With no ids the whole library is checked and sorted by loss. More than 3 dB lost means the sound needs
`presence` (see the make skill's references/levels.md) or a mid-range body in its recipe.
"""
import sys
from pathlib import Path

from scipy.signal import butter, sosfilt

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "src"))
from sfx_generator import levels, presets  # noqa: E402

SR = 48000
lib = presets.load_all()
ids = sys.argv[2:] or list(lib)
sos = butter(4, 250, "hp", fs=SR, output="sos")
rows = []
for sid in ids:
    x = lib[sid].render()
    lap = sosfilt(sos, x, axis=0)
    bf, ifull = levels.body_lufs(x), levels.integrated(x)
    bl, ilap = levels.body_lufs(lap), levels.integrated(lap)
    rows.append((bl - bf, sid, bf, ifull, bl, ilap))
rows.sort()
print(f"{'preset':18} {'body full':>10} {'integ full':>11} {'body laptop':>12} {'integ laptop':>13} {'loss':>6}")
for loss, sid, bf, ifull, bl, ilap in rows:
    flag = "  <- at risk" if loss < -3 else ""
    print(f"{sid:18} {bf:10.1f} {ifull:11.1f} {bl:12.1f} {ilap:13.1f} {loss:6.1f}{flag}")
at_risk = sum(1 for r in rows if r[0] < -3)
print(f"\n{at_risk} of {len(rows)} lose more than 3 dB on a small speaker")
