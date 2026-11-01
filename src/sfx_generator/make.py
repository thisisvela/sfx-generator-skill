"""Turn a short description into sound effects: map the words to a family and a starting preset, improvise
variants around it, inspect each one, and keep a journal so the next run starts smarter.

    from sfx_generator.make import make
    run = make("soft two-note success chime, about half a second", out=Path("out/chime"))

Every run:
1. reads the description and the lessons ledger (skills/make-sound-effect/references/lessons.md, if present);
2. picks the nearest preset with a synonyms table and the words that describe length, softness, pitch;
3. renders 3-6 variants: the preset itself, seed siblings, and seeded parameter improvisations within the schema;
4. inspects each (numbers, warnings, in-mix level);
5. writes an audition page and a journal entry (what was asked, what was tried, what the numbers say).

The journal (journal.jsonl in the output folder) is what the skill distils into lessons.
"""
from __future__ import annotations

import json
import re
import time
import zlib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import inspect as insp
from . import levels, presets, render, schema
from .audition import write_audition_page

# words -> preset ids, most specific first. The first match wins; several hits are ranked by score.
SYNONYMS: list[tuple[tuple[str, ...], str]] = [
    (("rain drop", "raindrop", "raindrops", "drips", "dripping"), "rain_drops"),
    (("rain", "rainy", "raining", "drizzle", "downpour"), "rain_loop"),
    (("waves", "sea", "ocean", "beach", "surf", "shore"), "waves_loop"),
    (("wave", "breaker"), "wave"),
    (("thunder", "lightning", "thunderclap", "rolling thunder", "thunder rumble", "distant storm"), "thunder"),
    (("wind", "breeze", "gale", "howling"), "wind_loop"),
    (("distant explosion", "far explosion", "artillery", "mortar"), "explosion_distant"),
    (("explosion", "explode", "blast", "bomb", "grenade", "detonat"), "explosion"),
    (("tank",), "tank_fire"),
    (("cannon", "cannonball"), "cannon"),
    (("machine gun", "machinegun", "automatic", "rapid fire", "repeated bullets", "bullets", "burst fire"), "machine_gun"),
    (("shotgun", "pump"), "shotgun"),
    (("gunshot", "gun shot", "gun", "pistol", "rifle", "bang", "shoot", "shot"), "gunshot"),
    (("ricochet", "bullet bounce"), "ricochet"),
    (("arrow", "bow", "archer", "crossbow"), "arrow"),
    (("sword clash", "clang", "parry", "blades meet", "blade clash", "metal clash"), "sword_clash"),
    (("sword", "blade", "slash", "swing"), "sword_swing"),
    (("punch", "fist", "melee hit", "body hit", "kick"), "punch"),
    (("hurt", "damage", "pain", "oof", "take damage"), "hurt"),
    (("fireball", "fire ball"), "fireball"),
    (("spell", "magic", "cast", "wizard", "enchant", "sorcery"), "spell_cast"),
    (("heal", "healing", "cure", "buff", "holy"), "heal"),
    (("power up", "power-up", "powerup", "boost", "upgrade"), "power_up"),
    (("burning", "fire", "campfire", "flames", "crackling", "hearth", "bonfire"), "burning_wood"),
    (("knock", "knocking"), "door_knock"),
    (("squeak", "squeaky", "squeal", "rusty hinge"), "door_squeak"),
    (("slam", "door shut", "door close"), "door_slam"),
    (("door", "creak", "hinge", "open the door", "door open"), "door_open"),
    (("blacksmith", "anvil", "forge", "smith"), "blacksmith"),
    (("hammer", "nail", "hammering", "carpenter"), "hammer"),
    (("footsteps", "walking", "walk", "steps", "running"), "footsteps"),
    (("footstep", "step on", "one step"), "footstep"),
    (("jump", "hop", "leap", "boing"), "jump"),
    (("land", "landing", "lands"), "land"),
    (("chest", "treasure", "loot"), "chest_open"),
    (("reload", "magazine", "ammo"), "reload"),
    (("game over", "gameover", "defeat", "you died", "death"), "game_over"),
    (("horn", "war horn", "charge", "rally", "battle cry", "army command", "command"), "war_horn"),
    (("drum", "snare", "march", "cadence", "military"), "drum_march"),
    (("title", "intro", "logo", "sting"), "title_hit"),
    (("end card", "outro", "end chime", "finish", "closing"), "end_chime"),
    (("level up", "levelup", "milestone", "fanfare", "achievement"), "level_up"),
    (("coin", "reward", "point", "pickup", "score"), "coin"),
    (("countdown", "three two one", "timer start"), "countdown"),
    (("alarm", "siren", "warning", "danger"), "alarm"),
    (("notification", "notify", "alert", "message", "incoming"), "notify"),
    (("success", "solved", "complete", "win", "achieve", "celebrat"), "success"),
    (("small win", "minor win", "ok", "done"), "success_short"),
    (("ding", "correct", "right answer", "check pass", "bell"), "ding"),
    (("chime",), "ding"),
    (("fail", "sad", "lose", "wrong", "descending"), "fail"),
    (("error", "uh-oh", "uh oh", "buzz", "denied", "contradiction", "invalid"), "error"),
    (("glitch", "stutter", "corrupt", "broken", "static", "digital noise"), "glitch_burst"),
    (("question", "hmm", "ask", "curious", "wonder"), "question"),
    (("riser", "build-up", "build up", "buildup", "tension", "anticipation"), "riser"),
    (("reverse cymbal", "swell", "suck"), "swell"),
    (("reveal", "land on", "lands on"), "swoosh_up"),
    (("big impact", "deep impact", "trailer", "huge boom", "massive"), "impact_deep"),
    (("impact", "boom", "hit", "thud", "slam", "drop in", "land"), "impact_soft"),
    (("shimmer", "sparkle", "magic", "glitter", "twinkle", "insight", "aha"), "shimmer"),
    (("zoom", "long whoosh", "big camera", "slow whoosh", "camera move"), "whoosh_long"),
    (("fade", "gentle whoosh", "soft whoosh", "calm", "subtle transition", "iris"), "whoosh_soft"),
    (("rise transition", "whoosh up", "new topic", "lift"), "whoosh_up"),
    (("quick whoosh", "short whoosh", "fast whoosh", "whip", "flick"), "whoosh_short"),
    (("whoosh", "swish", "swoosh", "woosh", "slide", "pan", "wipe", "transition", "fly past", "flyby"), "whoosh"),
    (("push in", "push-in", "zoom in", "camera lift"), "swell_up"),
    (("pull back", "pull-back", "zoom out", "settle"), "swell_down"),
    (("heavy pop", "low pop", "heavier"), "pop_low"),
    (("rising pop", "bloop up", "grow", "expand", "pop up", "pop-up"), "pop_up"),
    (("pop", "bubble pop", "appear", "pop in", "pop-in"), "pop"),
    (("bubble", "bubbles", "float up", "underwater"), "bubble"),
    (("drop", "drip", "droplet", "plink"), "drop"),
    (("pluck", "string", "snap in", "harp", "label"), "pluck"),
    (("tick tock", "tick-tock", "clock", "time passing", "waiting"), "tick_tock"),
    (("double tick", "two ticks", "check mark", "checkmark", "tick tick"), "tick_double"),
    (("tick", "counter", "list item", "step", "tok"), "tick"),
    (("soft click", "light click", "subtle click", "tap"), "click_soft"),
    (("keystroke", "key press", "keypress", "one key", "single key"), "keystroke"),
    (("typing", "keyboard", "terminal", "keys"), "typing"),
    (("click", "mouse", "button", "select", "press"), "click"),
    (("camera", "shutter", "snapshot", "screenshot", "photo", "capture"), "camera_shutter"),
    (("page", "flip", "card turn", "paper", "next page"), "page_turn"),
    (("stamp", "approved", "seal", "stamped"), "stamp"),
    (("unlock", "lock", "latch", "access", "open up"), "unlock"),
    (("heartbeat loop", "heart loop", "pulse loop", "heart beating", "beating heart", "heart rate"), "heartbeat_loop"),
    (("heartbeat", "heart", "pulse", "lub dub"), "heartbeat"),
    (("toggle", "flip on", "switch on", "state change", "blip"), "toggle"),
    (("switch", "lever", "mode", "click-clack", "mechanical"), "switch"),
    (("long ping", "ringing ping", "sustain"), "ping_long"),
    (("soft ping", "light ping", "gentle highlight"), "ping_soft"),
    (("sonar", "submarine", "probe", "echo"), "sonar"),
    (("ping", "glass", "highlight", "ting", "accent high"), "ping"),
    (("bong", "marimba", "wood", "low accent", "accent low"), "bong"),
    (("zap", "laser", "electric", "pew", "shoot", "delete"), "zap"),
    (("data", "packets", "transfer", "network", "loading", "computer", "blips"), "data_blips"),
    (("scan", "search", "radar", "progress", "analyse", "analyze"), "scan"),
    (("hum", "drone", "machine", "server", "engine"), "hum_loop"),
    (("air", "room tone", "wind", "ambience", "ambient", "bed", "noise bed"), "air_loop"),
]

# adjectives -> parameter nudges, applied to whichever of these names the recipe has
ADJECTIVES: dict[str, dict[str, float]] = {
    "soft": {"wet": 1.15, "attack": 1.6, "click": 0.5, "knock": 0.6, "strike": 0.5, "air": 0.5, "lowpass_hz": 0.7,
             "bright": 0.7, "noise": 0.6, "slap": 0.6},
    "gentle": {"wet": 1.15, "attack": 1.6, "click": 0.5, "knock": 0.6, "strike": 0.5, "lowpass_hz": 0.7, "bright": 0.7},
    "quiet": {"lowpass_hz": 0.7, "bright": 0.7},
    "hard": {"click": 1.6, "knock": 1.4, "strike": 1.6, "bright": 1.3, "noise": 1.4, "slap": 1.4},
    "sharp": {"click": 1.6, "strike": 1.6, "bright": 1.4, "noise": 1.4, "attack": 0.5},
    "bright": {"bright": 1.3, "lowpass_hz": 1.3, "f0": 1.25, "f1": 1.25, "f2": 1.25, "f": 1.25, "f_peak": 1.3},
    "dark": {"bright": 0.7, "lowpass_hz": 0.6, "f0": 0.75, "f1": 0.75, "f2": 0.75, "f": 0.75, "f_peak": 0.7,
             "damp_hz": 0.6},
    "low": {"f0": 0.7, "f1": 0.7, "f2": 0.7, "f3": 0.7, "f4": 0.7, "f": 0.7, "f_start": 0.7, "f_peak": 0.7,
            "f_end": 0.7, "root": 0.7, "thump_hz": 0.7, "tone_start": 0.7, "tone_end": 0.7},
    "deep": {"f0": 0.6, "f1": 0.6, "f": 0.6, "f_start": 0.7, "f_peak": 0.7, "f_end": 0.7, "tau": 1.4, "root": 0.6},
    "high": {"f0": 1.4, "f1": 1.4, "f2": 1.4, "f3": 1.4, "f4": 1.4, "f": 1.4, "f_start": 1.3, "f_peak": 1.3,
             "f_end": 1.3, "root": 1.4, "thump_hz": 1.3},
    "quick": {"d": 0.65, "gap": 0.7, "step": 0.7, "interval": 0.7, "tau": 0.7, "decay": 0.7, "note_d": 0.7,
              "tail": 0.6},
    "fast": {"d": 0.65, "gap": 0.7, "step": 0.7, "interval": 0.7, "tau": 0.7, "decay": 0.7, "note_d": 0.7},
    "short": {"d": 0.6, "tau": 0.6, "decay": 0.6, "note_d": 0.6, "tail": 0.5, "go_d": 0.6},
    "long": {"d": 1.6, "tau": 1.5, "decay": 1.6, "note_d": 1.5, "tail": 1.6, "go_d": 1.5},
    "slow": {"d": 1.5, "gap": 1.4, "step": 1.4, "interval": 1.5, "tau": 1.4, "decay": 1.4},
    "big": {"d": 1.3, "tail": 1.5, "wet": 1.4, "body": 1.5, "knock": 1.3, "sparkle": 1.4, "count": 1.5},
    "small": {"d": 0.75, "tail": 0.6, "wet": 0.6, "body": 0.6, "sparkle": 0.6, "count": 0.6},
    "wet": {"wet": 1.8, "tail": 1.4},
    "dry": {"wet": 0.3, "tail": 0.6},
    "wide": {"width": 1.8, "pan_from": 1.6, "pan_to": 1.6},
    "narrow": {"width": 0.4, "pan_from": 0.4, "pan_to": 0.4},
    "airy": {"air": 2.0, "hp_hz": 1.3},
    "metallic": {"ring": 1.6, "bright": 1.3},
    "wooden": {"body": 1.4, "bright": 0.8, "lowpass_hz": 0.7},
}

# "about half a second", "0.3 s", "300 ms", "two seconds"
_DUR = re.compile(r"(?:about |around |roughly |~)?(\d+(?:\.\d+)?|half a|a quarter|one|two|three|four|five)\s*"
                  r"(ms|millisecond|milliseconds|s\b|sec|secs|second|seconds)")
_WORDS = {"half a": 0.5, "a quarter": 0.25, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def parse_duration(text: str) -> float | None:
    m = _DUR.search(text.lower())
    if not m:
        return None
    v = _WORDS.get(m.group(1), None)
    v = float(m.group(1)) if v is None else v
    return v / 1000 if m.group(2).startswith("m") else v


def match_presets(text: str, library: dict[str, presets.Preset] | None = None) -> list[tuple[str, int]]:
    """Rank preset ids by how many synonym phrases (and tags, ids, uses) the description hits."""
    library = library or presets.load_all()
    t = " " + re.sub(r"[^a-z0-9 ]+", " ", text.lower()) + " "
    scores: dict[str, int] = {}
    for i, (words, sid) in enumerate(SYNONYMS):
        for w in words:
            if f" {w}" in t or f"{w} " in t:
                scores[sid] = scores.get(sid, 0) + 3 + (len(SYNONYMS) - i) / len(SYNONYMS) + len(w) / 10
    for sid, pr in library.items():
        if f" {sid.replace('_', ' ')} " in t or f" {sid} " in t:
            scores[sid] = scores.get(sid, 0) + 6
        for tag in pr.tags:
            if f" {tag.lower()} " in t:
                scores[sid] = scores.get(sid, 0) + 2
        for w in re.findall(r"[a-z]{4,}", pr.use.lower()):
            if f" {w} " in t:
                scores[sid] = scores.get(sid, 0) + 0.5
    return sorted(scores.items(), key=lambda kv: -kv[1])


def quantize(p: schema.Param, v: float):
    """Clip to the range and round to the parameter's step, so improvised values read like hand-set ones."""
    v = float(np.clip(v, p.min, p.max))
    if p.step:
        v = round(round(v / p.step) * p.step, 6)
        v = float(np.clip(v, p.min, p.max))
    return p.check(v)


def _nudge(rec: schema.Recipe, params: dict, factors: dict[str, float]) -> dict:
    out = dict(params)
    for name, f in factors.items():
        p = rec.by_name.get(name)
        if not p or p.kind not in ("float", "int"):
            continue
        out[name] = quantize(p, float(out[name]) * f)
    return out


def apply_description(rec: schema.Recipe, params: dict, text: str) -> tuple[dict, list[str]]:
    """Apply adjectives and an explicit duration from the description. Returns params and the notes of what changed."""
    notes = []
    t = text.lower()
    for adj, factors in ADJECTIVES.items():
        if re.search(rf"\b{adj}(er|est|ly)?\b", t):
            before = dict(params)
            params = _nudge(rec, params, factors)
            changed = [k for k in params if params[k] != before[k]]
            if changed:
                notes.append(f"{adj}: {', '.join(f'{k} {before[k]}->{params[k]}' for k in changed)}")
    dur = parse_duration(text)
    if dur and "d" in rec.by_name:
        p = rec.by_name["d"]
        params["d"] = quantize(p, dur)
        notes.append(f"length {dur} s -> d={params['d']}")
    return params, notes


def improvise(rec: schema.Recipe, params: dict, seed: int, amount: float = 0.18) -> tuple[dict, str]:
    """A seeded improvisation: nudge a few parameters within their ranges (log-space for Hz, linear otherwise),
    never the seed. Returns the new params and a one-line note of what moved."""
    rng = np.random.default_rng(seed)
    out = dict(params)
    cands = [p for p in rec.params if p.kind in ("float", "int") and p.name != "seed"]
    k = min(len(cands), int(rng.integers(2, 5)))
    picks = rng.choice(len(cands), size=k, replace=False)
    moved = []
    for i in picks:
        p = cands[i]
        v = float(out[p.name])
        if p.unit == "Hz" or p.name in ("f0", "f1", "f2", "f3", "f4", "f", "root"):
            v = v * float(np.exp(rng.normal(0, amount)))
        else:
            span = (p.max - p.min)
            v = v + float(rng.normal(0, amount)) * span * 0.5
        nv = quantize(p, v)
        if nv != out[p.name]:
            moved.append(f"{p.name} {out[p.name]}->{nv}")
            out[p.name] = nv
    return out, "; ".join(moved) or "no change"


@dataclass
class Variant:
    name: str
    recipe: str
    params: dict
    note: str
    x: np.ndarray = field(repr=False)
    report: dict = field(default_factory=dict)
    files: dict = field(default_factory=dict)


@dataclass
class Run:
    description: str
    base: presets.Preset
    category: str
    variants: list[Variant]
    out: Path
    audition: Path | None = None
    journal: Path | None = None
    candidates: list = field(default_factory=list)


def narration_clip() -> Path | None:
    """The short narration line shipped with the package, for 'over narration' playback (None if absent)."""
    p = Path(__file__).resolve().parent / "site" / "narration.mp3"
    return p if p.exists() else None


def make(description: str, out: Path, n: int = 4, base_id: str | None = None, category: str | None = None,
         formats=("wav", "ogg", "mp3"), seed: int = 0, lessons: str | None = None, verbose=True) -> Run:
    """Render n variants (3-6) for a description into out/, with an audition page and a journal entry."""
    n = int(np.clip(n, 3, 6))
    library = presets.load_all()
    ranked = match_presets(description, library)
    if base_id is None:
        base_id = ranked[0][0] if ranked else "ping"
    base = library[base_id]
    rec = schema.get(base.recipe)
    category = category or base.category

    def _render(p):                       # every variant is mastered for the base preset's mood
        return levels.master(rec.render(p), base.mood, presence_amount=base.presence)
    params, notes = apply_description(rec, dict(base.params), description)
    variants: list[Variant] = []
    # 1: the nearest preset as it ships (or as the description adjusts it)
    variants.append(Variant("a", rec.id, params, "nearest preset" + (f" with {'; '.join(notes)}" if notes else ""), _render(params)))
    # 2: a seed sibling (same recipe, other noise)
    sib = dict(params, seed=int(params["seed"]) + 1000 + seed)
    xs = _render(sib)
    if xs.shape == variants[0].x.shape and np.array_equal(xs, variants[0].x):
        # a purely tonal recipe: the seed changes nothing, so offer a pitch sibling (a whole tone up) instead
        up = {p.name: 2 ** (2 / 12) for p in rec.params if p.unit == "Hz" and p.name != "lowpass_hz"}
        sib = _nudge(rec, params, up)
        variants.append(Variant("b", rec.id, sib, "pitch sibling, a whole tone up (this recipe has no noise, so the "
                                                   "seed changes nothing)", _render(sib)))
    else:
        variants.append(Variant("b", rec.id, sib, f"seed sibling (seed {sib['seed']})", xs))
    # 3..n: seeded improvisations around it, a little bolder each time
    for i in range(n - 2):
        stable = zlib.crc32(f"{description}|{base_id}|{i}|{seed}".encode("utf-8"))   # hash() is salted per process
        imp, note = improvise(rec, params, seed=stable, amount=0.12 + 0.08 * i)
        variants.append(Variant("cdefg"[i], rec.id, imp, f"improvisation {i + 1}: {note}", _render(imp)))
    out.mkdir(parents=True, exist_ok=True)
    for v in variants:
        v.report = insp.report(v.x, category)
        v.files = {k: str(p.relative_to(out)) for k, p in render.export(v.x, out / f"{base_id}_{v.name}", formats).items()}
        pj = presets.Preset(id=f"{base_id}_{v.name}", recipe=v.recipe, params=v.params, family=base.family,
                            category=category, use=description, what=v.note, lead=base.lead, tags=list(base.tags),
                            mood=base.mood, presence=base.presence)
        pj.save(out / f"{base_id}_{v.name}.json")
        if verbose:
            r = v.report
            print(f"{v.name}: {v.note}\n   {r['seconds']} s, {r['loudness_max_lufs']} LUFS, peak {r['peak_dbfs']}, "
                  f"in mix {r['video_in_mix_lu']} LU{' (capped)' if r['video_capped'] else ''}"
                  + (f"\n   WARN " + "; ".join(r["warnings"]) if r["warnings"] else ""))
    run = Run(description, base, category, variants, out, candidates=ranked[:5])
    run.audition = write_audition_page(run, out / "audition.html", narration_clip())
    run.journal = write_journal(run, out / "journal.jsonl", lessons)
    if verbose:
        print(f"audition page: {run.audition}\njournal: {run.journal}")
    return run


def write_journal(run: Run, path: Path, lessons: str | None) -> Path:
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "description": run.description,
        "base": run.base.id, "recipe": run.base.recipe, "category": run.category,
        "candidates": run.candidates,
        "lessons_read": bool(lessons),
        "variants": [{"name": v.name, "note": v.note, "params": v.params,
                      "report": {k: v.report[k] for k in ("seconds", "decay_to_-20dB_s", "centroid_hz",
                                                         "pitch_track_hz", "loudness_max_lufs", "peak_dbfs",
                                                         "end_level_db", "dc_offset", "video_in_mix_lu",
                                                         "video_capped", "warnings")}}
                     for v in run.variants],
        "chosen": None, "lesson": None,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return path
