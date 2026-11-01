# Verification without ears

No model can hear. Every sound in the library was verified by numbers and spectrograms against a reference, then a
person listened. `sfx inspect <file|preset> --category <c> --png <out.png> [--svg wave.svg] [--json]`.

## The numbers (`inspect.describe`)

| field | meaning | act when |
|---|---|---|
| `seconds` | length | far from what was asked |
| `attack_s` | time to the peak | a "soft" sound with a 0 ms attack |
| `decay_to_-20dB_s` | time to fall 20 dB below the peak | tails over ~0.5 s where speech follows; under 0.03 s for anything that must be heard under a voice |
| `centroid_hz` | spectral centre of gravity (frames above 5 % of the peak) | the words said dark/bright and it did not move |
| `pitch_track_hz` | the STFT peak at five points (1,024-point frames, 128-sample hop, 0 Hz bin skipped) | a glide goes the wrong way; 0 Hz means DC |
| `dc_offset` | mean of the signal | over 0.002 on sounds longer than 0.15 s: remove the mean / high-pass 80-120 Hz |
| `end_level_db` | level in the last 2 ms relative to the peak | above −40 dB: it ends while still sounding (a cut is a click); add a release fade. Anticipation sounds that end on the cue are exempt |
| `peak_dbfs` | peak | not −1.5 ± 0.1: the recipe forgot `norm` |
| `loudness_max_lufs` | loudest 100 ms, K-weighted | with `--category`: `video_in_mix_lu`, `video_capped`, `video_gain_db` |
| `mono_sum_drop_db` | level lost when L+R is summed | over 3 dB: left/right phase cancellation; reduce the offset |
| `nan` | any NaN | always |

## The spectrogram

Greyscale, 0-12 kHz, the whole sound wide, ink is loud. Look for:

- **vertical lines**: clicks (a note stopped while ringing, a part placed without a release);
- **a smear along 0 Hz**: DC;
- **a tail that runs past the frame**: a reverb or decay too long for speech to follow;
- **the shape the words asked for**: a whoosh is a band that rises and falls; a chime is horizontal lines that fade;
  a glide is a line that slopes.

Compare beside a reference (`--png` of the preset you started from) when matching a character.

## Warnings (`inspect.warnings`)

- NaN samples
- DC offset over 0.002 (sounds over 0.15 s)
- ends while still sounding (end level above −40 dB)
- very short (under 0.1 s with under 30 ms of energy): it may vanish under speech
- peak off −1.5 dBFS
- mono sum loses more than 3 dB

## Small speakers

A laptop or phone speaker plays little under 250 Hz, and the loudness numbers are K-weighted, so a sound whose
weight sits there measures fine and is silent in the room. Before shipping any thump, boom, impact, footstep,
heartbeat, bed or loop: high-pass the render at 250 Hz (4th order) and compare `levels.body_lufs` of the
filtered and the full-band render. More than 3 dB lost is at risk; `sfx inspect` also warns "sub-only" when the
centroid is under 120 Hz. In the repository, `python -I tools/laptop_check.py . [ids]` does this for the whole
library and sorts by loss. The fix is the preset's `presence` first (0.6 brought 15-30 dB losses to about 4 dB
with no recipe change), a mid-range body in the recipe second.

## Natural sounds: measure the real thing

For thunder, rain, wind, waves, fire, crowds and anything else a person has heard outdoors, the words mislead
("rumble" reaches for the sub; the real weight is 80-250 Hz). Measure a free recording and the render with the
same script and iterate on the numbers:

- `tools/analyse_recordings.py`: crest, centroid, slope in dB per octave, band shares, texture modulation
  rate, event envelopes;
- `tools/rumble_texture.py`: kurtosis and envelope crest of the 80-250 Hz band (under 3 is wind, 8-45 is a
  rumble of arrivals);
- `tools/drops_analysis.py`: onset length, attack and pitch direction of individual drops.

The targets found so far are in `nature-acoustics.md`. Recordings used this way stay outside the repository,
are never shipped and are never named in it; only the numbers are kept.

## Measuring a character you want to match

STFT peak track, centroid over frames with energy above 5 % of the peak, and decay as time to fall 20 dB below
the peak. These let you match a sound's character without listening. The 23 interface sounds were matched this
way to the measured character of earlier reference sounds that were never shipped.

## The approval workflow that worked

- An audition page: reference beside new, "A then B", "play all", a choose/redo flag and a note per row, a
  "copy notes" button for the owner to paste back. Twenty-three replacements were approved in one pass.
- Play each sound at its in-video gain, so quiet sounds sound quiet.
- "Over narration": a real 3-5 s voice line with the sound placed on a cue word, respecting `lead`. The most useful
  single feature. (A narration line from a 24 kHz TTS needs resampling to 48 kHz.)
- Decode MP3 with Web Audio; play only after a click (autoplay rules); a DynamicsCompressor limiter on the master,
  because voice plus effect can exceed 0 dBFS.

## Determinism is a test

After any refactor, regenerate and compare with the previous files: they must be identical. `pytest -q` holds a
SHA-256 of every preset's float32 samples (`tests/test_determinism.py`). One real trap: two time helpers,
`int(SR*d)` and `int(round(SR*d))`, give different sample counts (48000 × 2.4 = 115199.99…), so merged code must
keep the variant each recipe was approved with.
