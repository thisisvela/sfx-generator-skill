# Levels, leads and density

Measured on real narrated videos. The first attempt put effects 13-19 LU under the voice and nobody could hear
them; the table was raised about 5 dB to these values. Code: `sfx_generator/levels.py`.

## Loudness of a sound

Its loudest 100 ms, K-weighted (EBU R128 filters). Use 100 ms, not the standard 400 ms window: 400 ms under-rates
short clicks and pops by several dB. `levels.loudness_max(x)`.

## Narration

About −14 LUFS integrated. Measure it in stereo the way the mixer sees it: a mono voice duplicated to two channels
reads 3 dB louder than a mono measurement. `levels.integrated(x)`.

## Level by category (LU relative to the narration)

| category | transition | appear | emphasis | ui | positive | question | negative | reveal | anticipation | camera | title | end | ambience |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LU | −4 | −4 | −4 | −6 | −4 | −2 | −4 | −2 | −4 | −7 | +2 | −1 | −16 |

Title and end cards have no voice under them, so they sit higher. Ambience loops sit far under everything.
Profiles: `video` (this table) and `standalone` (every category at 0, for apps and games with no voice).

## The gain rule

`gain = min(ref + level − loudness_max, −6 dBFS − peak)`. No single effect may peak above −6 dBFS in the mix.

- When the cap wins the sound is **capped**: quieter than its level asks. `levels.placement(x, category)` reports
  `gain_db`, `capped` and `in_mix_lu`.
- Bare 2-4 ms transients hit the cap long before they are loud enough. Fix that in the recipe by adding a little
  tonal body (a short sine under the click), not by raising gain. This raised the clicks and ticks 4-5 dB against
  the voice.

## Placement in time

A sound starts `lead` seconds before its cue.

- Whooshes peak just after the cue (lead about 0.4 × length).
- Risers, swells, the swoosh and the countdown end on it (lead = length).
- Event sounds start when their picture is visible, not when the line starts.
- Sounds after a transition land on the beat's content, not on an empty stage.

## Density

At most about 8 sounds a minute, at least 1 s apart. Real videos used 4.4 a minute. Every cue has a written reason.

## Target in the mix

Effects should sit 8-14 LU under the voice's momentary loudness. In the last measured video 28 cues sat a median
8.8 LU under (range −13.5 to −2.9); anything above −4 was flagged too loud and got a −6 to −8 dB `gain_db`.

## Mood: the weight of a sound follows its situation

Every master is peak-normalised, so a dense loop (rain, wind) is loud all the way through while a peaky event
(thunder: one crack, a long quiet rumble) is loud for 100 ms and then sits under the bed; the level rule, which
reads the loudest 100 ms, cannot see it. The preset's `mood` fixes that at the master (`levels.master`):

| mood | body (loudest second, K-weighted) | for |
|---|---|---|
| huge | −12 LUFS | fear, violence, the sky: thunder, an explosion, a cannon, a tank, an avalanche |
| big | −14 LUFS | a gunshot, a heavy impact, a door slam, a crash, a stinger |
| normal | as rendered | interface and foley; beds and loops |

The body is lifted to the target, the limiter holds the crack above it, the peak lands at −1.5 dBFS. Decide the
mood from the situation and the emotion (thunder is fear in the dark; it is meant to be louder than the rain it
interrupts), then let the category place that body in the mix. A `huge` sound may also carry its own
`level_lu` (thunder: +5, so the cap decides). The mood also sets the peak cap in the mix: huge −3 dBFS, big −4.5, normal −6
(`levels.PEAK_CAP_BY_MOOD`). Asked for "40 % louder" thunder, raise the cap, not the body target: a body target
the limiter has to crush to reach flattens the shape (the distant opening becomes as loud as the strike).

## Presence: being heard on a laptop

A laptop or phone speaker plays little under 250 Hz. A sound whose weight sits there (thunder, an explosion, a
deep impact) loses 5-10 dB on it while a whoosh loses nothing, however loud the file is. The preset field
`presence` (0-1, `levels.presence`) adds harmonics of the low band at 200-1200 Hz, driven from the band's RMS,
and tames the low band's peaks (which set the file's ceiling yet the speaker cannot play) so the normaliser can
lift what the speaker does play. Check any sub-heavy sound through a 250 Hz high-pass (`levels.body_lufs` of the
filtered render) before shipping; more than 3 dB lost means it needs presence. The tuner has a presence slider
under the post controls and saves it with the preset. Thunder ships at 0 (the owner preferred it without; raise it in the tuner for laptop playback).

## The master

narration + effects bed → one linear gain to −14 LUFS integrated → a look-ahead limiter at −1.5 dBFS
(`levels.limit`) → AAC. Results: −14.0 LUFS, true peak −2.5 to −2.8 dBFS.

Measure effects against the voice directly: rebuild the effects bed and compare it with the narration in the same
windows. Subtracting narration from an encoded AAC mix is invalid (the encoder delay misaligns them).

## Default transition sounds

| transition | slide | zoom | rise | fade | wipe | iris | shape | whip | glitch | cut |
|---|---|---|---|---|---|---|---|---|---|---|
| sound | whoosh | whoosh_long | whoosh_up | whoosh_soft | whoosh | whoosh_soft | whoosh_long | whoosh_short | glitch_burst | none |

Title cards: `swoosh_up` then `title_hit`. End card: `end_chime`.
