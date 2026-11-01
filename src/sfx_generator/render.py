"""Render a preset or a recipe with parameters to WAV, OGG and MP3, measure it, and write a catalog.

Masters are 48 kHz stereo float32 WAV. Ogg Vorbis q6 is the package format; MP3 160 kb/s is for browsers. ffmpeg
(with libvorbis and libmp3lame) is found on PATH, through the SFX_FFMPEG environment variable, or from the
optional `imageio-ffmpeg` package.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from . import levels, schema
from .blocks import SR
from .presets import Preset, cli_command


def ffmpeg_exe() -> str | None:
    exe = os.environ.get("SFX_FFMPEG") or shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def ffmpeg(*args):
    exe = ffmpeg_exe()
    if not exe:
        raise RuntimeError("ffmpeg not found: put it on PATH, set SFX_FFMPEG, or `pip install imageio-ffmpeg`")
    subprocess.run([exe, "-v", "error", "-y", *args], check=True)


def decode(path: Path | str) -> np.ndarray:
    """Decode any audio file to a (n, 2) float64 array at 48 kHz."""
    exe = ffmpeg_exe()
    if not exe:
        raise RuntimeError("ffmpeg not found: put it on PATH, set SFX_FFMPEG, or `pip install imageio-ffmpeg`")
    raw = subprocess.run([exe, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def write_wav(x: np.ndarray, path: Path, subtype="FLOAT"):
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), x.astype(np.float32), SR, subtype=subtype)
    return path


def export(x: np.ndarray, stem: Path, formats=("wav", "ogg", "mp3"), wav_subtype="FLOAT") -> dict[str, Path]:
    """Write <stem>.wav / .ogg / .mp3 and return the paths. The WAV is written first and the others are encoded
    from it, so all three carry the same samples."""
    out = {}
    wav = stem.with_suffix(".wav")
    write_wav(x, wav, wav_subtype)
    if "wav" in formats:
        out["wav"] = wav
    if "ogg" in formats:
        ogg = stem.with_suffix(".ogg")
        ffmpeg("-i", str(wav), "-ac", "2", "-ar", str(SR), "-c:a", "libvorbis", "-q:a", "6", str(ogg))
        out["ogg"] = ogg
    if "mp3" in formats:
        mp3 = stem.with_suffix(".mp3")
        ffmpeg("-i", str(wav), "-c:a", "libmp3lame", "-b:a", "160k", str(mp3))
        out["mp3"] = mp3
    if "wav" not in formats:
        wav.unlink(missing_ok=True)
    return out


def measure(x: np.ndarray) -> dict:
    return {"seconds": round(len(x) / SR, 3), "loudness_lufs": round(levels.loudness_max(x), 2),
            "peak_dbfs": round(levels.peak_dbfs(x), 2)}


def catalog_entry(preset: Preset, x: np.ndarray, file: str | None = None) -> dict:
    m = measure(x)
    pl = levels.placement(x, preset.category, level_lu=preset.level_lu, mood=preset.mood)
    return {"file": file or f"ogg/{preset.id}.ogg", "recipe": preset.recipe, "family": preset.family,
            "category": preset.category, "use": preset.use, "what": preset.what, "lead": preset.lead,
            "level_lu": preset.level_lu, "loop": preset.loop, "mood": preset.mood, "presence": preset.presence,
            "body_lufs": round(levels.body_lufs(x), 2), "tags": preset.tags, **m,
            "gain_db": pl["gain_db"], "capped": pl["capped"], "in_mix_lu": pl["in_mix_lu"],
            "params": preset.params, "cli": cli_command(preset),
            "licence": "Apache-2.0 (original, sfx-generator)", "source": f"synthesised by recipe {preset.recipe}"}


def render_presets(presets: dict[str, Preset], out: Path, formats=("wav", "ogg", "mp3"), verbose=True,
                   arrays: dict[str, np.ndarray] | None = None) -> dict:
    """Render every preset into out/{wav,ogg,mp3}/<id>.* and write out/catalog.json. Returns the catalog.
    `arrays` holds presets already rendered by the caller (the site build), so nothing renders twice."""
    cat = {"version": 3, "sample_rate": SR,
           "levels": "level_lu is relative to the narration's integrated loudness; loudness_lufs is the loudest "
                     "100 ms (K-weighted); gain_db places the sound in a -14 LUFS narration mix; a placed sound "
                     "never peaks above -6 dBFS (capped says when that cap won)",
           "lead": "seconds the sound starts before its cue (whooshes peak just after it; risers end on it)",
           "transition_sfx": levels.TRANSITION_SFX, "category_lu": levels.CATEGORY_LU, "sounds": {}}
    for sid, pr in presets.items():
        x = arrays[sid] if arrays and sid in arrays else pr.render()
        stem = out / "wav" / sid
        files = export(x, stem, formats)
        for fmt, p in files.items():
            if fmt != "wav":
                dest = out / fmt / p.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                p.replace(dest)
        cat["sounds"][sid] = catalog_entry(pr, x)
        if verbose:
            e = cat["sounds"][sid]
            print(f"{sid:16} {e['seconds']:6.3f} s  {e['loudness_lufs']:7.2f} LUFS  {e['peak_dbfs']:6.2f} dBFS"
                  f"{'  capped' if e['capped'] else ''}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "catalog.json").write_text(json.dumps(cat, indent=1) + "\n", encoding="utf-8")
    return cat


def array_hash(x: np.ndarray) -> str:
    """SHA-256 of the float32 samples: the determinism fingerprint stored in tests."""
    import hashlib
    return hashlib.sha256(np.ascontiguousarray(x.astype(np.float32)).tobytes()).hexdigest()[:16]


def render_params(recipe_id: str, params: dict | None = None) -> np.ndarray:
    return schema.get(recipe_id).render(params)
