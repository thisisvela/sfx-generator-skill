"""Presets: one JSON file per shipped sound in src/sfx_generator/library/presets/ (shipped inside the wheel).

    {"id": "whoosh", "recipe": "whoosh", "params": {...}, "family": "cinematic", "category": "transition",
     "use": "a slide or pan to the next beat", "lead": 0.265, "level_lu": -4, "what": "Band-passed noise ...",
     "tags": ["swish", "slide"]}

`family` groups sounds on the site (cinematic, interface, foley, ambience); `category` picks the level in a video
mix (see levels.CATEGORY_LU); `lead` is how many seconds the sound starts before its cue; `presence` (0-1) adds
small-speaker harmonics of the low band (levels.presence) for sub-heavy sounds; `mood` (huge, big,
normal; see levels.MOODS) is how big the sound is meant to feel, from the situation it belongs to: it masters the
body, not the peak. Ids are stable: never rename a shipped id, downstream plans reference it.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import levels, schema

PRESET_DIR = Path(__file__).resolve().parent / "library" / "presets"

FAMILIES = ("cinematic", "interface", "foley", "ambience", "nature", "game")


@dataclass
class Preset:
    id: str
    recipe: str
    params: dict
    family: str = "interface"
    category: str = "emphasis"
    use: str = ""
    what: str = ""
    lead: float = 0.0
    level_lu: int | None = None
    tags: list = field(default_factory=list)
    loop: bool = False
    mood: str = "normal"
    presence: float = 0.0

    def __post_init__(self):
        if self.category not in levels.CATEGORY_LU:
            raise ValueError(f"{self.id}: category {self.category!r} is not one of {sorted(levels.CATEGORY_LU)}")
        if self.level_lu is None:
            self.level_lu = levels.CATEGORY_LU[self.category]

    def render(self):
        return levels.master(schema.get(self.recipe).render(self.params), self.mood, presence_amount=self.presence)

    def validate(self):
        if self.family not in FAMILIES:
            raise ValueError(f"{self.id}: family {self.family!r} is not one of {FAMILIES}")
        if self.category not in levels.CATEGORY_LU:
            raise ValueError(f"{self.id}: category {self.category!r} is not one of {sorted(levels.CATEGORY_LU)}")
        if self.mood not in levels.MOODS:
            raise ValueError(f"{self.id}: mood {self.mood!r} is not one of {sorted(levels.MOODS)}")
        schema.get(self.recipe).validate(self.params)
        return self

    def to_dict(self):
        return asdict(self)

    def save(self, path: Path | None = None) -> Path:
        path = path or PRESET_DIR / f"{self.id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=1) + "\n", encoding="utf-8")
        return path

    @classmethod
    def from_dict(cls, d: dict) -> "Preset":
        known = {k: d[k] for k in cls.__dataclass_fields__ if k in d}
        return cls(**known)

    @classmethod
    def load(cls, path: Path | str) -> "Preset":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def load_all(directory: Path | None = None) -> dict[str, Preset]:
    directory = Path(directory) if directory else PRESET_DIR
    out = {}
    for p in sorted(directory.glob("*.json")):
        pr = Preset.load(p)
        out[pr.id] = pr
    return out


def find(name: str, directory: Path | None = None) -> Preset:
    """A preset by id, or a path to a preset JSON file."""
    p = Path(name)
    if p.suffix == ".json" and p.exists():
        return Preset.load(p)
    presets = load_all(directory)
    if name in presets:
        return presets[name]
    raise KeyError(f"no preset {name!r}; presets: {', '.join(sorted(presets))}")


def cli_command(preset: Preset) -> str:
    """The `sfx render` command that recreates a preset from its recipe and parameters."""
    rec = schema.get(preset.recipe)
    defaults = rec.defaults()
    changed = [f"{k}={v}" for k, v in preset.params.items() if defaults.get(k) != v]
    args = (" " + " ".join(changed)) if changed else ""
    return f"sfx render {preset.recipe}{args} -o {preset.id}"
