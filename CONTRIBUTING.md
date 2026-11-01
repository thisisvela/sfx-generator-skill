# Contributing

Thank you. Three rules first, because they are the reason this library exists:

1. **Own code only.** Nothing recorded or downloaded, ever. A sound is a recipe, so whoever runs it owns the result.
2. **Deterministic.** A fixed seed per sound; no unseeded randomness; a rebuild gives identical files.
3. **Never rename a shipped id.** Downstream plans reference ids. Add a new one instead.

## Setup

```bash
git clone https://github.com/thisisvela/sfx-generator-skill
cd sfx-generator-skill
python -m venv .venv && . .venv/bin/activate      # .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest -q
```

## Adding a sound

The `create-sound-recipe` skill (`skills/create-sound-recipe/SKILL.md`) is the full procedure. In short:

- a recipe in `src/sfx_generator/recipes/<family>.py`, registered with `@recipe(...)` and a schema in which every
  parameter has a kind, default, min, max, step, unit and one-line meaning; every literal the recipe uses is a
  parameter with that literal as its default;
- a preset in `src/sfx_generator/library/presets/<id>.json` (id, recipe, params, family, category, use, what, lead, tags, loop);
- `sfx inspect <id> --png out/<id>.png`: no warnings; the numbers match what you meant;
- synonyms in `SYNONYMS` in `src/sfx_generator/make.py`;
- `python tools/gen_recipe_reference.py` and `pytest -q`;
- an entry in the skill's lessons ledger: what it is, what went wrong first, what mattered.

## Changing a shipped sound

The determinism test will fail with the new hash. That is the point: a changed sound must be a decision. If a
person has listened and approved the change, update the hash in `tests/test_determinism.py` and say so in the
commit message. If the sound is one of the 37 originals, the reference OGG test will fail too; replace
`tests/reference/<id>.ogg` with the new master in the same commit.

## Style

Short functions, docstrings that say what a block does and what its trap is, numpy and scipy only in the audio
path. No model can hear: in reviews, say what the numbers and the spectrogram show, and ask a person to listen.
