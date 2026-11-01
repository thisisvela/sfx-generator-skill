---
name: create-sound-recipe
description: Use when a requested sound fits no existing recipe family (make-sound-effect found no good base, or the person asks for a new kind of sound such as a rain loop, a bell tree, an engine, a footstep). Adds a recipe the way the library was built: building block first, then the recipe with a parameter schema, a preset, an inspection, the tests, the docs. Keeps its own lessons ledger and records what each new recipe taught.
---

# Create a sound recipe

A recipe is a Python function of keyword parameters that returns a (n, 2) float array at 48 kHz, registered with
a schema that declares every parameter (kind, default, min, max, step, unit, meaning). Everything else (the CLI,
the tuning page, the site, the make skill, the tests) reads that declaration. Code lives in
`src/sfx_generator/recipes/<family>.py`; blocks in `src/sfx_generator/blocks.py`.

**You cannot hear.** Verify by numbers and spectrogram, then a person listens.

## Before anything: read the ledger

`references/lessons.md` in this skill: what earlier recipes taught, newest last. Append at the end.

## The order that worked

1. **Describe the sound in physical terms before any code.** What makes the noise? A struck bar (partials with
   inharmonic ratios, a knock), air moving (band-passed noise with a moving centre), a string (Karplus-Strong), a
   mechanism (clicks with bodies and rings), a signal (sines, squares, blips). Which family is nearest? Read the
   `make-sound-effect` skill's `references/blocks.md` for every block and how the families use them.

2. **Measure a reference if you have one.** `sfx inspect <file> --png ref.png`: length, decay to −20 dB, centroid,
   pitch track. For natural sounds add the comparison scripts in `tools/` (`analyse_recordings.py`,
   `rumble_texture.py`, `drops_analysis.py`; what they found so far is in the make skill's
   `references/nature-acoustics.md`). These numbers are the target. Never ship the reference audio, and never
   name it or where it came from in the repository: only its numbers are kept.

3. **Building block first, if a new one is needed.** A new block goes in `blocks.py` with a docstring that says
   what it does and its trap (DC, clicks, aliasing). Keep it pure numpy/scipy, seeded, shaped (n,) or (n, 2).

4. **The recipe.** Start from the nearest module. Template:

   ```python
   @recipe("rain_loop", family="ambience",
           doc="Filtered noise with seeded drop ticks; a seamless loop.",
           tips="density is drops per second; f_hi the brightness; d the loop length.",
           params=[P("d", 4.0, 1.0, 16.0, 0.5, "s", "loop length"),
                   P("density", 12, 1, 60, 1, "/s", "drops per second"),
                   P("f_hi", 6000, 1000, 16000, 50, "Hz", "brightness"),
                   SEED(271)])
   def rain_loop(*, d, density, f_hi, seed): ...
   ```

   Rules: every value the recipe uses is a parameter with that literal as its default (derived values are not
   float-exact); `seed` always exists; integrate frequency into phase (`osc`); release every note; `finish` or
   `norm` at the end so the peak is −1.5 dBFS; loops get whole cycles per loop or `loop_seam`, and no edge fades.

5. **The preset.** `src/sfx_generator/library/presets/<id>.json` with id, recipe, params (all of them, from `rec.defaults()` or
   `rec.validate({...})`), family (cinematic, interface, foley, ambience), category (decides the level; see the
   make skill's `references/levels.md`), use (one line: when), what (one line: what it is), lead, tags, loop.
   Never rename a shipped id.

6. **Inspect.** `sfx inspect <id> --png out/<id>.png`. Act on every warning. Compare the numbers with the target.
   Read the make skill's `references/verification.md`.

7. **Improvise.** Render three to six variants (`sfx make "<words>" --base <id>` once the preset exists, or
   `sfx render <id> name=value`) and look at what each parameter does to the numbers. If a parameter does nothing
   measurable, it should not be a parameter.

8. **Tests.** `pytest -q`. Determinism (renders identically twice), quality (peak, end, DC, NaN, loop seam),
   schema (every param has a range, step, meaning; the function's signature matches), levels (the category lands).
   If the hash test complains about a *shipped* sound you did not mean to change, you changed shared code: revert.

9. **Docs.** Regenerate `skills/make-sound-effect/references/recipes.md` (`python tools/gen_recipe_reference.py`),
   add the synonyms for the new sound to `SYNONYMS` in `src/sfx_generator/make.py`, rebuild the site
   (`sfx site`) and look at the card.

10. **A person listens.** `sfx make "<words>" --base <id> --open` gives an audition page. Say what the numbers
    show; ask them to flag redo.

11. **Write the lesson.** Append to `references/lessons.md`: what the sound is physically, which blocks it took,
    what went wrong first and how it was fixed, which parameters mattered, what the numbers of the approved
    version are. The next recipe is cheaper only if this one wrote that down.

## Pitfalls that cost time before

- DC: Karplus-Strong excitations, summed click cores, long low sines with short envelopes. High-pass 80-120 Hz
  before `finish`, or remove the mean.
- Clicks at the end: a part placed without a release; `trim_tail` on a loop; a buffer shorter than its parts.
- Too short to survive under speech: under 0.1 s of energy. Give it body or make it longer.
- Capped by the peak rule: a bare transient. Add a short sine under it.
- Aliasing: a raw `np.sign(sin)` square at high pitch. Use `square()`/`saw()` (band-limited) unless the harshness
  is the point (glitches), and low-pass after.
- Non-determinism: `hash()` of a string is salted per process; `np.random.seed` globals; dict ordering of sets.
  Use `np.random.default_rng(seed)` and `zlib.crc32` for stable hashes.
- `_t` vs `_tr`: different sample counts for the same length. Pick one per recipe and keep it.
- Silent on a laptop: all the weight under 250 Hz (a heartbeat at 72 Hz, a 55 Hz hum, a sub-only impact). Put
  energy where small speakers play it (a knock, a formant, a mid body) and check with a 250 Hz high-pass; the
  preset's `presence` is the generic fix when the recipe must not change.
- A drum where a boom was wanted: a sine sweeping down, or a resonant filter on an impulse. Booms and cracks are
  pulses (their length is the weight) and crackle (100-300 ms of growing impulses), without an oscillator.
- Wind where a rumble was wanted: filtered noise with an LFO. A rumble is a Poisson train of short N-wave
  pulses with lognormal sizes (`_arrivals` in `recipes/nature.py`); kurtosis of the 80-250 Hz band over 3.
- A bell where a tool was wanted: `tone` with bell ratios. Metal that vibrates is close partial pairs that
  beat, saturated a little, gone fast; a tuned ping stays above 3 kHz and under 0.1 s.
- A cartoon drop: a glide falling in pitch. A drop is a 2-3 ms broadband tick; its ring, if any, rises.
- Even gaps on a natural sound read as a machine: clusters with skewed random gaps, and a separate random
  stream for the timing so content variants keep it.
- DC at a loop seam: an asymmetric waveform through `tanh` has a mean; subtract it. A causal low-pass after
  `loop_seam` moves the seam: filter before the seam, or not at all.

## References

Everything in `skills/make-sound-effect/references/` applies here too (blocks, levels, verification, recipes).
This skill's own ledger is `references/lessons.md`.
