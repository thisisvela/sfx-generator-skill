# sfx-generator: notes for agents working in this repository

- **Installing for a user?** Follow `INSTALL.md`. Do not improvise an install procedure.
- **Making a sound?** Use the `make-sound-effect` skill (`skills/make-sound-effect/SKILL.md`, mirrored in
  `.agents/skills/` for Codex). It reads and appends a lessons ledger on every run.
- **Adding a recipe?** Use `create-sound-recipe` (`skills/create-sound-recipe/SKILL.md`).
- **Changing code?** `pip install -e ".[dev]"`, then `pytest -q`. The determinism test holds a hash of every
  shipped sound; a changed hash is a changed sound and needs a person's approval by ear.
- **Rules that never bend:** own code only (nothing recorded or downloaded, ever), a fixed seed per sound, never
  rename a shipped id, and never claim to hear: report numbers and spectrograms and ask a person to listen.
- `skills/` is the source of truth; `.agents/skills/` is a copy kept in sync by `python tools/sync_skills.py`
  (the test suite checks they match).
