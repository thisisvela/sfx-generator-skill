# sfx-generator: design

Date: 2026-10-31. Built from the handover kit for the code-made sound effects of explainer-studio. The owner's
standing preferences (own code only, deterministic, Apache 2.0, sparse and purposeful in video) are the constraints.

## Decisions taken without the owner (section 9.1 of the handover)

| Question | Decision | Why |
|---|---|---|
| Repo and plugin name | repo `sfx-generator-skill` (the folder the owner named), Python package `sfx-generator` (`sfx_generator`), CLI `sfx`, plugin `sfx-generator` | matches the folder; `sfx` is the shortest command that is not taken by something common |
| GitHub account | `thisisvela` (author `Vela`), held in one place: `REPO` in `src/sfx_generator/__init__.py`; `pyproject.toml`, `plugin.json`, `INSTALL.md`, `README.md` and `CONTRIBUTING.md` spell it out for installers | decided with the owner 2026-11-01; the owner's name appears nowhere in the repository or its history |
| Licence | Apache 2.0 (`LICENSE`, `pyproject.toml`, `plugin.json`, the site's licence page, the catalog's `licence` field) for the code, the presets and every sound they produce | decided with the owner 2026-11-01, replacing MIT |
| Presence | a preset `presence` (0-1) adds harmonics of the band under 250 Hz at 200-1200 Hz and tames that band's peaks, so sub-heavy sounds are heard on a laptop; eight presets ship with 0.6, thunder with 0 | the owner could not hear thunder or the deep impacts on laptop speakers; a 250 Hz high-pass check (`tools/laptop_check.py`) over the library found 30 of 99 at risk |
| Nothing external | the repository names no other site, recording, library of sounds or font; the site loads nothing from outside itself; the natural-sound numbers in `nature-acoustics.md` were measured on free recordings kept in a scratch folder and never copied in | the owner's rule: own code only, nothing to attribute, nothing to clear |
| ChatGPT / Codex package | not built; the skills are written host-neutral so a port is a packaging step | nobody asked for it yet |
| Level table | the explainer's table is the default (`levels.CATEGORY_LU`, profile `video`); a `standalone` profile places every sound at the reference | the library is still mostly for narrated video |
| Mood | a preset `mood` (huge −12, big −14, normal) masters the body (loudest second, K-weighted) rather than the peak, and sets the peak cap in a mix (huge −3 dBFS, big −4.5, normal −6); the originals are `normal` and bit-identical | the owner heard rain and wind louder than thunder: a peaky event measured loud for 100 ms and sat under the beds; the weight of a sound follows the situation it belongs to |
| Narration line | a 4.6 s synthesised voice line ships as `src/sfx_generator/site/narration.mp3`, cue at 3.3 s (how it was made is in the session memory, not the repo) | "over narration" was the most useful feature of the review pages |

## Shape

```
src/sfx_generator/
  blocks.py        building blocks (verbatim port; keeps both _t and _tr)
  levels.py        K-weighting, loudest-100-ms, level table, gain rule, peak cap, limiter, placement
  schema.py        Param + Recipe registry: every parameter has kind, default, min, max, step, unit, meaning
  recipes/         one module per family; 21 families, 54 recipes
  presets.py       src/sfx_generator/library/presets/*.json (inside the wheel): id, recipe, params, family, category, use, what, lead, level, tags, loop
  render.py        WAV/OGG/MP3 export (ffmpeg on PATH, SFX_FFMPEG, or imageio-ffmpeg), measurement, catalog, hashes
  inspect.py       numbers, warnings, greyscale spectrogram PNG, hairline waveform SVG (no matplotlib)
  make.py          description -> nearest preset -> variants (seed sibling, improvisations) -> audition page -> journal
  audition.py      the self-contained audition page (base64 MP3, Web Audio, limiter, over narration, notes)
  tune/            `sfx tune`: localhost server + page; sliders from the schema; one Python source of truth
  site/            `sfx site`: the static GitHub Pages site (hairline-style)
  cli.py           list, schema, render, render-all, make, inspect, tune, site
skills/make-sound-effect, skills/create-sound-recipe   SKILL.md + references (blocks, levels, verification, lessons)
tests/             determinism (hashes + reference OGGs), quality, schema, site
```

## Determinism

The 37 reference presets render sample-for-sample identical to the original generator (checked at float level).
Their OGG masters differ from a fresh encode by up to 0.05 because libvorbis builds differ, so the OGG test is
tolerant (same length, max difference under 0.1) and the exact test is a SHA-256 of the float32 samples.

## The learning loop (the owner's addition: "the skill improvises and learns during every audio generation")

- `sfx make` always renders a seed sibling and seeded improvisations (parameters nudged within their schema, log
  space for Hz), so a run never just replays a preset. Purely tonal recipes, where the seed changes nothing, get a
  pitch sibling instead.
- Every run appends to `journal.jsonl` in its output folder: the words, the candidates and scores, every variant's
  parameters and numbers.
- The skill reads `skills/make-sound-effect/references/lessons.md` before generating and appends one entry after
  every generation (what the words mapped to, what moved, what the numbers said, what was chosen). The
  `create-sound-recipe` skill does the same in its own ledger.

## Not done

- Per-partial start phases in the tuning page (the recipes do not expose partial phases).
- A pure-browser JavaScript tuner on the public site.
- The GitHub repository itself and the Pages deployment: the owner publishes (the steps are in the session's final report).

## Distribution (decided with the owner, 2026-10-31)

- **Not on PyPI.** The package installs from GitHub (`uv tool install "sfx-generator[ffmpeg] @ git+<repo>"`,
  pipx, or pip). The presets ship inside the wheel (`src/sfx_generator/library/presets`).
- **Primary route is the skill.** A user pastes one line into Claude Code or Codex ("Install the sound effects
  skill from <repo>: fetch and follow its INSTALL.md"). `INSTALL.md` is written for the agent: ask project or user
  scope (the owner chose "ask each time"), install `sfx` as an isolated tool (uv, pipx, private venv fallback),
  install the skills (Claude: `claude plugin install sfx-generator --marketplace <owner/repo>`; Codex: copy into
  `.agents/skills` or link `~/.agents/skills/sfx-generator`), smoke test, say what to ask.
- **Codex package.** `.agents/skills/` mirrors `skills/` (checked by a test; `tools/sync_skills.py` syncs), each
  skill carries `agents/openai.yaml`. No Codex marketplace manifest: the official docs describe plugin install
  only from a configured marketplace, so native skill discovery is the reliable path.
- **Docs order.** Home page and Use page: Claude Code, Codex, what to say, the tuning page, in video, then
  developers (git install, CLI, Python), then adding a recipe.
- **The tuning page through the skill.** The skill starts `sfx tune <preset>` in the background from the output
  folder, gives the address when a browser cannot be opened, and stops the server when the user says done.
- Generated sounds default to `assets/sfx/<name>/` in the user's project.

## Site themes and downloads (2026-10-31)

- Theme selector in the top bar, remembered in localStorage and applied before paint: Hairline (follows the
  system), Hairline light, Hairline dark, and Sumi (washi paper, sumi ink, a vermilion seal; the serif accents and
  play buttons go red, a faint enso sits behind the hero, the playhead and bloom of the background use the accent).
- Downloads: a menu on every card (WAV, OGG, MP3, preset), a zip per family in each section header, and a zip of
  everything in the library bar. `build_zips` makes them during `sfx site` with a README and the catalog.

## Game and nature families (2026-10-31)

39 more sounds in two site sections. `nature` (6): rain_drops, rain_loop, wave, waves_loop, thunder, wind_loop.
`game` (33): explosion, explosion_distant, cannon, gunshot, machine_gun, shotgun, tank_fire, ricochet, arrow,
sword_swing, sword_clash, punch, hurt (combat.py); spell_cast, fireball, heal, power_up, burning_wood, door_open,
door_knock, door_squeak, door_slam, hammer, blacksmith, footstep, footsteps, jump, land, chest_open, reload,
game_over, war_horn, drum_march (world.py). "Army commands" became war_horn and drum_march: a convincing voice
cannot be synthesised from these blocks, and a horn and a cadence are what games use for the same beat. The
library is 99 sounds (heartbeat_loop was added later); the level categories are unchanged (loops are `ambience`, blasts `reveal`, steps `ui`).
