# sfx-generator

A skill for Claude Code and Codex that turns a sentence into a finished sound effect, with 99 ready-made sounds
to start from. Every sound is synthesised by code in this repository: deterministic numpy recipes with a
parameter schema each, a tuning page, and the measurements that place a sound under narration. Apache 2.0: free to use anywhere, and you own what you generate.

Site: <https://thisisvela.github.io/sfx-generator-skill/>

## Install the skill

Paste this into Claude Code or Codex, in the project where you want the sounds:

```text
Install the sound effects skill from https://github.com/thisisvela/sfx-generator-skill: fetch and follow its INSTALL.md
```

The agent follows [INSTALL.md](INSTALL.md): it checks Python 3.10+, installs the `sfx` command as an isolated
tool (uv or pipx, private venv as the fallback), asks whether the skills are **for this project** or **for you**,
installs them at that scope, runs a smoke test and tells you what to say next.

By hand, in Claude Code (2.1.292 or later; pick the scope in the dialog):

```text
/plugin install sfx-generator --marketplace thisisvela/sfx-generator-skill
```

By hand, in Codex: copy `skills/make-sound-effect` and `skills/create-sound-recipe` into your project's
`.agents/skills/` (or link the whole `skills/` folder as `~/.agents/skills/sfx-generator`). Then install the
command, below.

## What to say

```text
make a quick whoosh for a slide transition
a soft two-note success chime, about half a second
a notification a fifth up, bright and dry
a low hum to sit under the whole scene, as a loop
open the tuning page for variant b
```

The `make-sound-effect` skill maps the words to a family and the nearest preset, improvises three to six
variants (seed siblings and seeded nudges within the schema), checks each one by numbers and spectrogram, shows
an audition page with in-video level and over-narration playback, and saves the chosen preset with WAV, OGG and
MP3 in `assets/sfx/<name>/`. "Open the tuning page" starts `sfx tune`, a local page with a slider for every
parameter, rendered live by the same Python code. `create-sound-recipe` adds a new family when none fits.

Both skills read a lessons ledger before every generation and append to it after
(`skills/*/references/lessons.md`), so each run improvises around what the last one learned. They are written
host-neutral; `.agents/skills/` is a mirror of `skills/` for Codex.

## For developers: the command and the Python API

The package is not on PyPI; it installs from GitHub. The `ffmpeg` extra brings a static ffmpeg for OGG and MP3.

```bash
uv tool install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

```bash
pipx install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

```bash
pip install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

```bash
sfx list                                  # the library: id, family, category, lead, level, use
sfx schema whoosh                         # every parameter: default, range, step, unit, meaning
sfx render whoosh -o whoosh               # whoosh.wav, .ogg, .mp3 and the numbers
sfx render whoosh d=0.5 f_peak=3200 -o w2 --preset
sfx render-all -o out/library             # the whole library + catalog.json
sfx make "soft two-note success chime, about half a second"    # variants, audition page, journal
sfx inspect out/library/ogg/ping.ogg --category emphasis --png ping.png
sfx tune ping                             # localhost tuning page, sliders from the schema
sfx site -o site                          # build the demo site
```

```python
from pathlib import Path
from sfx_generator import presets, render, schema, levels, inspect as insp

x = presets.find("whoosh").render()                 # (n, 2) float64, 48 kHz, peak -1.5 dBFS
render.export(x, Path("whoosh"))                     # .wav .ogg .mp3
rec = schema.get("whoosh")
y = rec.render({**rec.defaults(), "d": 0.5})
insp.report(y, category="transition")                # numbers, warnings, in-mix placement
```

To work on the recipes: clone, `pip install -e ".[dev]"`, `pytest -q`.

## Layout

```
INSTALL.md           what an agent does when a user pastes the repo URL and says "install"
skills/              make-sound-effect, create-sound-recipe (+ references and lessons ledgers)
.agents/skills/      the same two skills, mirrored for Codex (tools/sync_skills.py keeps them identical)
.claude-plugin/      plugin.json and marketplace.json for Claude Code
src/sfx_generator/   blocks, levels, schema, recipes/ (21 families), library/presets (98 JSON), render,
                     inspect, make, audition, tune/ (server + page), site/ (builder, css, js, narration), cli
tests/               determinism (hashes + the 37 reference OGGs), quality, schema, make, site, skills mirror
docs/design.md       decisions taken, shape, the learning loop, what is not done
tools/               sync_skills, gen_recipe_reference, and the analysis scripts (recordings, rumble texture,
                     drops, laptop check) behind the natural-sound lessons
```

## Levels in a video, briefly

Narration at about −14 LUFS. A sound's loudness is its loudest 100 ms (K-weighted). Level by category in LU:
transition −4, appear −4, emphasis −4, ui −6, positive −4, question −2, negative −4, reveal −2, anticipation −4,
camera −7, title +2, end −1, ambience −16. Gain = `min(ref + level − loudness, −6 dBFS − peak)`. A sound starts
`lead` seconds before its cue; risers end on it. At most about 8 sounds a minute. See the site's Use page.

A preset's `mood` (huge, big, normal) decides how big it is meant to feel from the situation it belongs to:
thunder is fear and the open sky, so it is `huge` and its rumble is mastered to carry the weight (the loudest
second lifted to −12 LUFS, the crack held by the limiter) instead of hiding under a peak-normalised crack. In a mix a huge sound may peak at −3 dBFS, a big one at −4.5,
an ordinary effect at −6.
A `presence` field adds small-speaker harmonics of the low band so a sub-heavy sound is still heard on a laptop.

## Tests

```bash
pytest -q
```

Determinism: every preset renders identically twice and the 37 originals match their stored hashes (and, with
ffmpeg, their reference OGGs within encoder tolerance). Quality: peak −1.5 dBFS, silent ends, no DC, no NaN,
loop seams. Schema: every parameter has a range, a step and a meaning; defaults reproduce the presets. Levels:
every category lands where the table says. Make: the acceptance descriptions produce variants, an audition page
and presets. Site: builds and every link resolves. Skills: the Codex mirror matches `skills/`.

## Licence

Apache 2.0, for the code, the presets and every sound they produce. See `LICENSE`.
