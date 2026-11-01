---
name: make-sound-effect
description: Use when someone asks for a sound effect from a short description ("a soft two-note success chime", "quick whoosh for a slide", "a notification a fifth up, bright, dry") or wants an existing sound adjusted. Maps the words to a recipe family and the nearest preset, improvises three to six measured variants, shows an audition page, and saves the chosen preset with WAV, OGG and MP3. Reads and updates a lessons ledger on every run.
---

# Make a sound effect

Turn a sentence into a finished sound. Every sound here is synthesised by code (numpy recipes in this repository),
so what you make is owned outright by whoever makes it. Apache 2.0: free to use anywhere, and you own what you generate.

**You cannot hear.** Say what the numbers and the spectrogram show, never that something "sounds good". A person
listens on the audition page and decides.

## Before anything: read the ledger

Read `references/lessons.md` in this skill. It holds what earlier runs learned, newest last. Use it: if the ledger
says "chime + 'soft' wanted a longer attack, not more reverb", start there. You will append to it at the end.

## The loop

1. **Understand the words.** Pull out: the *event* (what happens on screen or in the app), the *character*
   (soft, bright, low, quick, long, dry, wide...), the *length* if given, and the *context* (under narration? in
   an app? a loop?). If the request is for a video, the category decides the level; see `references/levels.md`.
   Also decide the *mood* from the situation the sound belongs to: fear, violence, the sky (thunder, an
   explosion, a cannon) are `huge`; a gunshot, a slam, a heavy impact `big`; interface and foley `normal`.
   The mood masters the body of the sound so a peaky event is not quieter than a bed (`levels.MOODS`).
   And decide the *timing* from who made the sound: man-made sounds (gunfire, a machine, a clock, typing)
   repeat on a steady rhythm; natural ones (thunder, rain, waves, fire, a flock) come in clusters with
   irregular gaps and never repeat evenly. Even spacing on a natural sound reads as a machine.

2. **Map to a family and the nearest preset.** `sfx make` does this with a synonyms table (swish/swoosh/woosh ->
   whoosh; ding/chime/notification -> bell chimes; boom/hit/thud -> impact; and so on), and prints its ranked
   candidates. Check its pick against your reading of the words; override with `--base <id>` when you know better.
   `sfx list` shows every preset with its use; `references/recipes.md` explains every family and parameter.

3. **Improvise, don't replay.** Run, with `<out>` = `assets/sfx/<slug>` in the user's project unless they named
   another place (`sfx` is on PATH after the install; if it was installed into `~/.sfx-generator/venv`, use that
   path):

   ```
   sfx make "<the description>" -o <out> -n 4
   ```

   You get: `a` the nearest preset with the description's adjectives and length applied; `b` a seed sibling (or a
   pitch sibling when the recipe has no noise); `c`.. seeded improvisations, parameters nudged within their
   schema. Each variant comes with its numbers, warnings and in-mix level, a preset JSON, WAV/OGG/MP3, an
   `audition.html`, and a line in `journal.jsonl`.

   Then improvise *yourself*: pick the one or two parameters the words point at and render deliberate moves with
   `sfx render <preset.json> name=value -o out/<slug>/<name>`. Change only what the description asks for. At least
   one variant per run should be an idea the preset did not contain (a different interval, a second layer, a
   reversed envelope): that is where the library grows.

4. **Inspect every variant by numbers and picture.** `sfx inspect <file> --category <c> --png <out.png>`.
   Read `references/verification.md` for what each number means and the warnings to act on: DC, an end that is
   still sounding, too short to survive under speech, capped by the peak limit, mono-sum loss. Fix in the recipe
   parameters, not with gain.

5. **Show the person.** Open `<out>/audition.html` (or tell them where it is). It plays each variant at its
   in-video level, over a real narration line on its cue, A then B, play all, with a choose/redo flag and a note
   per row and a copy-notes button.

   **The tuning page.** When they want to adjust by hand ("open the tuning page", "let me tune b"), start it as a
   background process from the folder the preset should be saved in and keep it running until they say they are
   done:

   ```
   cd <out> && sfx tune <variant>.json
   ```

   It serves http://127.0.0.1:8765 and opens the browser itself; if the host cannot open a browser, add
   `--no-open` and give them the address. Sliders come from the schema; every change re-renders in Python and
   shows the numbers, waveform and spectrogram. Save preset writes `<id>.json` into that folder and Export writes
   WAV, OGG and MP3 next to it; nothing is written without a click. When they are done, stop the server, read the
   saved JSON, and continue from it. Another port: `--port 8766`.

6. **Save and export the choice.** The chosen variant's `<id>.json` is the preset; rename its `id` to a clean
   snake_case name and `sfx render <preset.json> -o <final>` exports WAV, OGG and MP3. If it belongs in the
   library, copy the JSON to `src/sfx_generator/library/presets/` with `family`, `category`, `use`, `what`, `lead`, `tags`, and run
   `pytest -q` (determinism, quality, schema, levels).

7. **Report the level.** For video, say where it sits: "in a −14 LUFS narration mix this plays at −4 LU (not
   capped); start it 0.27 s before the cue". The numbers are in the inspect report (`video_in_mix_lu`,
   `video_capped`) and the preset's `lead`.

8. **Write the lesson.** Append one entry to `references/lessons.md` (format below). This is not optional: the
   next run is only cheaper if this one wrote down what it learned.

## Rules that bite

- Deterministic: a fixed seed per sound; never unseeded randomness. A rebuild gives the same file.
- Own code only: never download, record or borrow audio. A free recording may be measured for its numbers, in a
  folder outside the repository; it is never shipped and never named in the repository.
- Never rename a shipped id: plans downstream reference it.
- Too quiet is the common failure under narration; very short sounds vanish under speech (use 0.1 s or more of
  real energy); transients hit the peak cap first (add tonal body, not gain); every note needs a release fade;
  Karplus-Strong needs DC removal; keep chime tails under about 0.5 s where speech follows.
- Small speakers: a sound with no energy above about 150 Hz does not exist on a laptop, whatever the level rule
  says. Check thumps, booms, beds and loops through a 250 Hz high-pass (`levels.body_lufs` of the filtered
  render); more than 3 dB lost means `presence` first, a mid-range body second.
- The mood sets the weight, the cap sets "louder" in the mix; never reach a body target by crushing the shape.
- Natural sounds: a roar or roll is a sequence with a bed under it; a rumble is a pile of impulsive arrivals
  (kurtosis over 3), not filtered noise; a crack builds for 100-300 ms; a sine sweep is a drum; a drop is a tick
  whose plink rises; timing is clusters with irregular gaps. Measure the real thing first
  (`references/nature-acoustics.md`).
- Nothing rings in tune unless it is a bell or a chime; echoes are discrete returns, a reverb is a room.
- Ship only the version the person chose; retire the A/B variant and move its synonyms.
- Do not claim to hear. Numbers and pictures, then a person.

## When no family fits

Use the `create-sound-recipe` skill: a new building block, recipe, schema, preset, inspection and catalog entry,
with its own ledger.

## The lesson entry

Append to `references/lessons.md`:

```
### 2026-10-31 · "soft two-note success chime, about half a second"
- mapped: success (12.6), ding (6.3); base success; category positive
- moved: "soft" -> wet 0.14->0.16; length 0.5 -> d=0.5 (buffer only; the room makes it 0.82 s)
- numbers: all four -4.0 LU, none capped; decay 0.34 s; no warnings
- chosen: c (f4 1798 Hz: the top note a step lower reads calmer); redo: none
- lesson: "half a second" for a chime means the audible decay, not the buffer: set decay, not d
- next time: offer a minor-third variant for "soft"; try attack 0.004 before adding room
```

Keep entries short and factual. If a run contradicts an earlier lesson, say so under the new entry rather than
editing the old one.

## References

- `references/recipes.md`: every family, recipe and parameter with its meaning and tips (generated from the schema).
- `references/levels.md`: levels, leads, density, transitions, the gain rule.
- `references/verification.md`: the numbers, the warnings, the spectrogram, the approval workflow.
- `references/blocks.md`: the building blocks and how the families are built from them.
- `references/nature-acoustics.md`: what thunder, rain, rumbles and drops measure, the targets to synthesise
  against, and the comparison scripts in `tools/`.
- `references/lessons.md`: the ledger. Read first, append last. Its two standing-lessons sections are the
  short form of everything the listening passes taught.
