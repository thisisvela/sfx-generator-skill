# Recipes and parameters

Generated from the schemas by `python tools/gen_recipe_reference.py`; do not edit by hand.
Every parameter has a default, a range, a step, a unit and a meaning. `sfx schema <recipe>` prints the same.

## Presets by use

| id | family | category | lead | LU | use |
|---|---|---|---|---|---|
| `air_loop` | ambience | ambience | 0.0 | -16 | room tone, air, a quiet bed under a whole beat (loop) |
| `alarm` | interface | negative | 0.0 | -4 | a warning that needs attention |
| `arrow` | game | emphasis | 0.47 | -4 | an arrow is loosed and lands; lead so the thunk lands on the cue |
| `blacksmith` | game | emphasis | 0.0 | -4 | a smith at the anvil; forging, crafting |
| `bong` | interface | emphasis | 0.0 | -4 | a low, firm accent |
| `bubble` | foley | appear | 0.0 | -4 | something floats up; a playful appear |
| `burning_wood` | game | ambience | 0.0 | -16 | a campfire or hearth under a scene (loop) |
| `camera_shutter` | foley | emphasis | 0.0 | -4 | a snapshot or screenshot is taken |
| `cannon` | game | reveal | 0.0 | -2 | a cannon fires |
| `chest_open` | game | positive | 0.0 | -4 | a chest opens; treasure found |
| `click` | interface | ui | 0.0 | -6 | a pointer clicks or a choice is selected |
| `click_soft` | interface | ui | 0.0 | -6 | a very light click |
| `coin` | interface | positive | 0.0 | -4 | a point scored; a reward collected |
| `countdown` | interface | anticipation | 1.05 | -4 | three, two, one, go: the last beep lands on the cue |
| `data_blips` | interface | ui | 0.0 | -6 | data transferring; packets flowing |
| `ding` | interface | positive | 0.0 | -4 | a check passes, an answer is right |
| `door_knock` | game | emphasis | 0.0 | -4 | someone knocks at the door |
| `door_open` | game | emphasis | 0.0 | -4 | a door opens |
| `door_slam` | game | reveal | 0.0 | -2 | a door slams shut |
| `door_squeak` | game | emphasis | 0.0 | -4 | a squeaky hinge; something old opens slowly |
| `drop` | foley | appear | 0.0 | -4 | a single value drops in; a water drop |
| `drum_march` | game | emphasis | 0.0 | -4 | troops march; a military cadence, a command given |
| `end_chime` | cinematic | end | 0.0 | -1 | the end card |
| `error` | interface | negative | 0.0 | -4 | something fails, a contradiction is shown |
| `explosion` | game | reveal | 0.0 | -2 | a close explosion; a blast |
| `explosion_distant` | game | emphasis | 0.0 | -4 | an explosion far away; artillery over the hill |
| `fail` | interface | negative | 0.0 | -4 | a gentle no, softer than error |
| `fireball` | game | reveal | 0.9 | -2 | a fireball flies and lands; lead so the boom lands on the cue |
| `footstep` | game | ui | 0.0 | -6 | one footstep on a hard floor |
| `footsteps` | game | ui | 0.0 | -6 | walking; someone approaches |
| `game_over` | game | negative | 0.0 | -4 | the run ends; game over |
| `glitch` | interface | negative | 0.0 | -4 | a short 75 ms digital glitch; glitch_burst is the longer, stronger one |
| `glitch_burst` | cinematic | negative | 0.0 | -4 | a broken or inconsistent state (0.4 s stutter) |
| `gunshot` | game | emphasis | 0.0 | -4 | a pistol or rifle shot |
| `hammer` | game | emphasis | 0.0 | -4 | a hammer on a nail; building |
| `heal` | game | positive | 0.0 | -4 | healing; a buff applied |
| `heartbeat` | foley | emphasis | 0.0 | -4 | tension, a pulse, something alive |
| `heartbeat_loop` | foley | emphasis | 0.0 | -4 | a pulse under a scene: tension, fear, waiting (loop) |
| `hum_loop` | ambience | ambience | 0.0 | -16 | a machine room, a server, a bed under a whole beat (loop) |
| `hurt` | game | negative | 0.0 | -4 | the player takes damage |
| `impact_deep` | cinematic | reveal | 0.0 | -2 | the one big reveal of the video |
| `impact_soft` | cinematic | reveal | 0.0 | -2 | the key idea or result lands |
| `jump` | game | emphasis | 0.0 | -4 | the player jumps |
| `keystroke` | foley | ui | 0.0 | -6 | one key is pressed; a character is typed |
| `land` | game | emphasis | 0.0 | -4 | the player lands |
| `level_up` | interface | positive | 0.0 | -4 | a milestone reached; a bigger win than success |
| `machine_gun` | game | emphasis | 0.0 | -4 | a burst of automatic fire |
| `notify` | interface | emphasis | 0.0 | -4 | a message or alert arrives |
| `page_turn` | foley | transition | 0.06 | -4 | a page or card flips |
| `ping` | interface | emphasis | 0.0 | -4 | highlight a key value or word |
| `ping_long` | interface | emphasis | 0.0 | -4 | a highlight that rings while the eye moves |
| `ping_soft` | interface | emphasis | 0.0 | -4 | a lighter highlight |
| `pluck` | interface | appear | 0.0 | -4 | a label or value snaps in |
| `pop` | interface | appear | 0.0 | -4 | an important element lands (not every pop-in) |
| `pop_low` | interface | appear | 0.0 | -4 | a heavier element lands |
| `pop_up` | interface | appear | 0.0 | -4 | something grows or rises into place |
| `power_up` | game | positive | 0.0 | -4 | a power-up collected; a boost |
| `punch` | game | emphasis | 0.0 | -4 | a punch lands; a body hit |
| `question` | interface | question | 0.0 | -2 | the narration asks the viewer a question |
| `question_alt` | interface | question | 0.0 | -2 | a second question, later in the video |
| `rain_drops` | nature | emphasis | 0.0 | -4 | a few drops before the rain; water on a surface |
| `rain_loop` | nature | ambience | 0.0 | -16 | steady rain under a scene (loop) |
| `reload` | game | ui | 0.0 | -6 | a weapon reloads |
| `ricochet` | game | emphasis | 0.0 | -4 | a bullet glances off metal or rock |
| `riser` | cinematic | anticipation | 2.0 | -4 | two seconds of build-up that ends ON the cue; rare |
| `scan` | interface | emphasis | 0.0 | -4 | scanning, searching, a progress sweep |
| `shimmer` | cinematic | emphasis | 0.0 | -4 | an insight, a 'that's it' moment |
| `shotgun` | game | emphasis | 0.0 | -4 | a shotgun blast and the pump |
| `sonar` | interface | question | 0.0 | -2 | a probe, a search, waiting for a reply |
| `spell_cast` | game | emphasis | 0.0 | -4 | a spell is cast; magic |
| `stamp` | foley | appear | 0.0 | -4 | a label is stamped on; approved |
| `success` | interface | positive | 0.0 | -4 | a fix works; a problem is solved |
| `success_short` | interface | positive | 0.0 | -4 | a smaller win |
| `swell` | cinematic | anticipation | 1.2 | -4 | a reverse swell that ends ON the cue |
| `swell_down` | interface | camera | 0.0 | -7 | with a pull-back to the whole picture |
| `swell_up` | interface | camera | 0.0 | -7 | a soft tonal lift with a push-in |
| `switch` | interface | ui | 0.0 | -6 | a mode or view switches |
| `swoosh_up` | cinematic | anticipation | 0.75 | -4 | rises and lands ON the cue (a reveal) |
| `sword_clash` | game | emphasis | 0.0 | -4 | two blades meet; a parry |
| `sword_swing` | game | emphasis | 0.0 | -4 | a blade swung through the air |
| `tank_fire` | game | reveal | 0.0 | +2 | a tank's main gun fires |
| `thunder` | nature | reveal | 2.5 | +5 | a thunder strike; put the flash 2.5 s in (or set approach to 0 to start on the hit); fear, the dark, a dramatic turn |
| `tick` | interface | emphasis | 0.0 | -4 | a counter step or one item of a list |
| `tick_double` | interface | emphasis | 0.0 | -4 | a pair of items, a check mark drawn |
| `tick_tock` | foley | emphasis | 0.0 | -4 | a clock; time passing |
| `title_hit` | cinematic | title | 0.0 | +2 | the intro title landing |
| `toggle` | interface | ui | 0.0 | -6 | a switch flips, a state changes |
| `typing` | foley | ui | 0.0 | -6 | text being typed; a terminal filling |
| `unlock` | foley | positive | 0.0 | -4 | access granted; something opens |
| `war_horn` | game | reveal | 0.0 | -2 | a battle begins; a rally, a command to charge |
| `wave` | nature | emphasis | 1.5 | -4 | one wave breaks and washes out; lead so the break lands on the cue |
| `waves_loop` | nature | ambience | 0.0 | -16 | a beach under a scene (loop) |
| `whoosh` | cinematic | transition | 0.265 | -4 | a slide or pan to the next beat |
| `whoosh_long` | cinematic | transition | 0.54 | -4 | a zoom transition, a big camera move |
| `whoosh_short` | cinematic | transition | 0.105 | -4 | a quick slide transition |
| `whoosh_soft` | cinematic | transition | 0.2 | -4 | a gentle fade or calm change |
| `whoosh_up` | cinematic | transition | 0.24 | -4 | a rise transition (new topic) |
| `wind_loop` | nature | ambience | 0.0 | -16 | wind under a scene (loop) |
| `zap` | interface | emphasis | 0.0 | -4 | a laser, an electric hit, something zapped away |

## Families

### whoosh

#### `whoosh` (presets: `whoosh`, `whoosh_long`, `whoosh_short`, `whoosh_soft`, `whoosh_up`)

Band-passed noise swept up and back down, panned across the stereo field: the transition sound.

*Tips:* d sets the length; peak is where (0-1) the loudest, highest moment falls; f_start/f_peak/f_end are the band's centre at the start, the peak and the end; q_* its narrowness there (higher = whistlier); body adds a low band at 0.18 x fc; air adds white noise fizz; pan_from/pan_to move it across the field. A lead of about 0.4 x d puts the peak just after the cue.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.7 | 0.15..3.0 step 0.01 | s | length |
| `peak` | 0.55 | 0.1..0.9 step 0.01 |  | position of the loudest moment (0-1) |
| `f_start` | 350 | 60..6000 step 1 | Hz | band centre at the start |
| `f_peak` | 2200 | 100..12000 step 1 | Hz | band centre at the peak |
| `f_end` | 650 | 60..6000 step 1 | Hz | band centre at the end |
| `q_start` | 0.9 | 0.3..6 step 0.05 |  | band narrowness at the start |
| `q_peak` | 1.5 | 0.3..6 step 0.05 |  | band narrowness at the peak |
| `q_end` | 1.0 | 0.3..6 step 0.05 |  | band narrowness at the end |
| `pan_from` | 0.45 | -1..1 step 0.05 |  | pan at the start (-1 left, 1 right) |
| `pan_to` | -0.45 | -1..1 step 0.05 |  | pan at the end |
| `body` | 0.25 | 0..1 step 0.01 |  | low body band amount |
| `air` | 0.15 | 0..0.6 step 0.01 |  | white-noise air on top of the pink source |
| `lowpass_hz` | 9500 | 2000..20000 step 50 | Hz | final low-pass (takes the fizz off) |
| `seed` | 1 | seed |  | the noise seed: change it for a sibling of the same sound |

### anticipation

#### `swoosh_up` (presets: `swoosh_up`)

A short rising swoosh whose loudest moment is its last: put its end on the cue (a reveal).

*Tips:* f_start -> f_end is the noise band's sweep; tone_* a quiet sine that rises with it; curve shapes the rise (higher = later, steeper); q narrows the band.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.75 | 0.2..3.0 step 0.01 | s | length (ends on the cue) |
| `f_start` | 260 | 60..4000 step 1 | Hz | band centre at the start |
| `f_end` | 4200 | 300..12000 step 1 | Hz | band centre at the end |
| `q` | 1.4 | 0.3..6 step 0.05 |  | band narrowness |
| `tone_start` | 220 | 40..2000 step 1 | Hz | the sine's start pitch |
| `tone_end` | 660 | 40..4000 step 1 | Hz | the sine's end pitch |
| `tone_amp` | 0.12 | 0..0.6 step 0.01 |  | sine amount |
| `curve` | 2.2 | 0.5..6 step 0.1 |  | envelope exponent (s^curve) |
| `width` | 0.25 | 0..1 step 0.05 |  | pan travel, left to right |
| `seed` | 2 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `riser` (presets: `riser`)

Noise and a detuned tone rise together over the length and end on the cue: build-up before a reveal.

*Tips:* d is the whole build; f_* the noise band's sweep (the right ear's band is slightly higher, for width); tone_* the chord's root glide; det_hi/det_lo the two side oscillators' ratios (beating); curve makes the rise later and steeper.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 2.0 | 0.5..8.0 step 0.05 | s | length (ends on the cue) |
| `f_start` | 180 | 40..2000 step 1 | Hz | left noise band at the start |
| `f_end` | 5200 | 500..14000 step 1 | Hz | left noise band at the end |
| `f_start_r` | 200 | 40..2000 step 1 | Hz | right noise band at the start |
| `f_end_r` | 5600 | 500..14000 step 1 | Hz | right noise band at the end |
| `tone_start` | 110 | 30..1000 step 1 | Hz | tone root at the start |
| `tone_end` | 440 | 60..4000 step 1 | Hz | tone root at the end |
| `det_hi` | 1.007 | 1.0..1.05 step 0.001 |  | upper detune ratio |
| `det_lo` | 0.994 | 0.95..1.0 step 0.001 |  | lower detune ratio |
| `tone_amp` | 0.32 | 0..1 step 0.01 |  | tone amount against the noise |
| `curve` | 2.6 | 0.5..6 step 0.1 |  | envelope exponent (s^curve) |
| `seed` | 3 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `swell` (presets: `swell`)

A reverse-cymbal swell: a reverberated noise burst played backwards, so it grows into the cue.

*Tips:* d is the length; hp_hz brightens the burst (higher = thinner, airier); wet is the reverb amount before reversal; lowpass_hz tames the top.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.2 | 0.3..5.0 step 0.05 | s | length (ends on the cue) |
| `hp_hz` | 1800 | 200..8000 step 10 | Hz | high-pass on the burst |
| `wet` | 0.9 | 0.2..1.0 step 0.01 |  | reverb amount |
| `damp_hz` | 7000 | 1500..16000 step 50 | Hz | reverb damping |
| `lowpass_hz` | 8500 | 2000..20000 step 50 | Hz | final low-pass |
| `seed` | 4 | seed |  | the noise seed: change it for a sibling of the same sound |

### impact

#### `impact` (presets: `impact_deep`, `impact_soft`)

A cinematic hit: a falling sub sine, a short low-passed knock, a band of body and a reverb tail.

*Tips:* f0 -> f1 is the boom's pitch fall (lower = deeper); tau its decay; knock the hit's amount; bright its low-pass (lower = duller); tail and wet the room. d is the dry length; the tail adds 0.6 x tail.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.4 | 0.3..4.0 step 0.05 | s | dry length |
| `f0` | 110 | 30..400 step 1 | Hz | boom start pitch |
| `f1` | 42 | 20..200 step 1 | Hz | boom end pitch |
| `tau` | 0.28 | 0.05..1.5 step 0.01 | s | boom decay |
| `knock` | 0.35 | 0..1 step 0.01 |  | knock amount |
| `bright` | 2600 | 300..10000 step 10 | Hz | knock low-pass |
| `tail` | 1.0 | 0.2..4.0 step 0.05 | s | reverb length |
| `wet` | 0.22 | 0..0.8 step 0.01 |  | reverb amount |
| `seed` | 21 | seed |  | the noise seed: change it for a sibling of the same sound |

### shimmer

#### `shimmer` (presets: `shimmer`)

A soft sparkle: short sine pings at seeded pitches and times, spread across the stereo field, in reverb.

*Tips:* count is how many pings; lo/hi their pitch range; spread the seconds over which they start (small = a burst, large = a trickle); the seed picks the pitches and timing.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.8 | 0.5..5.0 step 0.05 | s | length before the tail is trimmed |
| `count` | 14 | 2..60 step 1 |  | number of pings |
| `lo` | 1900 | 300..8000 step 10 | Hz | lowest ping pitch |
| `hi` | 6800 | 500..16000 step 10 | Hz | highest ping pitch |
| `spread` | 0.75 | 0.02..3.0 step 0.01 | s | pings start within this window |
| `seed` | 6 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `title_hit` (presets: `title_hit`)

A deep impact with a quiet shimmer on top: the intro title landing.

*Tips:* sparkle sets the shimmer amount over the hit; f0/f1 the boom; tail the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 90 | 30..300 step 1 | Hz | boom start pitch |
| `f1` | 36 | 20..150 step 1 | Hz | boom end pitch |
| `tau` | 0.42 | 0.1..1.5 step 0.01 | s | boom decay |
| `tail` | 1.6 | 0.3..4.0 step 0.05 | s | reverb length |
| `wet` | 0.26 | 0..0.8 step 0.01 |  | reverb amount |
| `sparkle` | 0.32 | 0..1 step 0.01 |  | shimmer amount |
| `count` | 12 | 2..60 step 1 |  | shimmer pings |
| `seed` | 8 | seed |  | the noise seed: change it for a sibling of the same sound |

### glitch

#### `glitch_burst` (presets: `glitch_burst`)

A digital stutter: five short band-limited square bursts at seeded pitches with gaps, a little crushed. Long enough (about 0.4 s) to be heard under a voice, unlike a 30 ms click.

*Tips:* count is the number of bursts; f_lo/f_hi their pitch range; crush the number of levels (fewer = harsher); band_hz where the band-pass sits; the seed picks pitches, lengths and gaps.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.38 | 0.1..2.0 step 0.01 | s | length |
| `count` | 5 | 1..20 step 1 |  | number of bursts |
| `f_lo` | 320 | 60..4000 step 1 | Hz | lowest burst pitch |
| `f_hi` | 1400 | 100..8000 step 1 | Hz | highest burst pitch |
| `crush` | 6 | 2..32 step 1 |  | quantisation levels |
| `band_hz` | 1800 | 300..8000 step 10 | Hz | band-pass centre |
| `seed` | 10 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `glitch` (presets: `glitch`)

A tiny digital glitch: three crushed square bursts in 75 ms (glitch_burst is the longer one).

*Tips:* count and d set how many bursts fit; f_lo/f_hi their pitch; band_hz the band-pass. Under speech prefer glitch_burst: 75 ms vanishes.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.075 | 0.03..0.5 step 0.005 | s | length |
| `count` | 3 | 1..12 step 1 |  | number of bursts |
| `f_lo` | 900 | 100..6000 step 1 | Hz | lowest burst pitch |
| `f_hi` | 2600 | 200..10000 step 1 | Hz | highest burst pitch |
| `band_hz` | 3000 | 300..10000 step 10 | Hz | band-pass centre |
| `seed` | 121 | seed |  | the noise seed: change it for a sibling of the same sound |

### chime

#### `ding` (presets: `ding`)

A bright two-note chime, f1 then f2 (C5 then G5): something is right.

*Tips:* f1/f2 are the two notes (a fifth apart by default); gap the time between them; decay scales the bell's ring (keep tails under about 0.5 s where speech follows); wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 523.25 | 100..4000 step 0.01 | Hz | first note |
| `f2` | 783.99 | 100..4000 step 0.01 | Hz | second note |
| `gap` | 0.07 | 0.0..0.5 step 0.005 | s | time between the notes |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.14 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.7 | 0.2..3.0 step 0.01 | s | buffer length |
| `seed` | 115 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `success` (presets: `success`)

A rising four-note arpeggio (C6 E6 G6 C7), the last note ringing: a problem solved.

*Tips:* f1..f4 are the notes (a major arpeggio by default); step is the time between notes; decay scales the ring; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1046.5 | 200..5000 step 0.1 | Hz | first note (C6) |
| `f2` | 1318.5 | 200..5000 step 0.1 | Hz | second note (E6) |
| `f3` | 1568.0 | 200..6000 step 0.1 | Hz | third note (G6) |
| `f4` | 2093.0 | 200..8000 step 0.1 | Hz | last note (C7) |
| `step` | 0.065 | 0.02..0.3 step 0.005 | s | time between notes |
| `note_d` | 0.55 | 0.15..1.5 step 0.01 | s | each note's length |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.14 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.85 | 0.3..3.0 step 0.01 | s | buffer length |
| `seed` | 116 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `success_short` (presets: `success_short`)

Two notes up a fourth, G6 then C7: a smaller win.

*Tips:* f1/f2 are the notes; gap the time between; decay the ring; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1568.0 | 200..5000 step 0.1 | Hz | first note |
| `f2` | 2093.0 | 200..6000 step 0.1 | Hz | second note |
| `gap` | 0.06 | 0.0..0.4 step 0.005 | s | time between the notes |
| `note_d` | 0.45 | 0.15..1.5 step 0.01 | s | each note's length |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.55 | 0.2..3.0 step 0.01 | s | buffer length |
| `seed` | 117 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `end_chime` (presets: `end_chime`)

Three soft bell tones a fifth and an octave apart (C5, G5, C6) in a long room: the end card.

*Tips:* f1..f3 are the notes; spacing the time between them; decay the ring (0.9 s on the fundamental by default); tail and wet the room. Longer and softer than the interface chimes.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 523.25 | 100..2000 step 0.01 | Hz | first note (C5) |
| `f2` | 783.99 | 100..3000 step 0.01 | Hz | second note (G5) |
| `f3` | 1046.5 | 100..4000 step 0.01 | Hz | third note (C6) |
| `spacing` | 0.12 | 0.0..0.6 step 0.005 | s | time between the notes |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `tail` | 1.6 | 0.3..4.0 step 0.05 | s | reverb length |
| `wet` | 0.3 | 0..0.8 step 0.01 |  | reverb amount |
| `d` | 2.4 | 0.5..6.0 step 0.05 | s | buffer length |
| `seed` | 9 | seed |  | the noise seed: change it for a sibling of the same sound |

### pops

#### `pop` (presets: `pop`)

A round bubble pop: a sine that jumps up in pitch as it dies away, with a soft click on top.

*Tips:* f0 -> f1 is the pitch jump (up = a bubble, down = a thud); tc how fast it moves; tau the decay; click the noise transient's amount; second the 2nd harmonic (rounder when low).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.16 | 0.05..0.6 step 0.005 | s | length |
| `f0` | 600 | 80..3000 step 1 | Hz | pitch at the start |
| `f1` | 900 | 80..4000 step 1 | Hz | pitch it glides to |
| `tc` | 0.03 | 0.005..0.2 step 0.001 | s | glide time constant |
| `tau` | 0.028 | 0.005..0.3 step 0.001 | s | decay |
| `second` | 0.18 | 0..1 step 0.01 |  | 2nd harmonic amount |
| `click` | 0.25 | 0..1 step 0.01 |  | click amount |
| `seed` | 101 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `pop_low` (presets: `pop_low`)

A heavier pop: lower and rounder, with a little sub thump.

*Tips:* f0 -> f1 the body glide; thump the sub amount (140 -> 90 Hz); tau the decay.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.2 | 0.05..0.8 step 0.005 | s | length |
| `f0` | 330 | 60..2000 step 1 | Hz | pitch at the start |
| `f1` | 520 | 60..3000 step 1 | Hz | pitch it glides to |
| `tc` | 0.035 | 0.005..0.2 step 0.001 | s | glide time constant |
| `tau` | 0.04 | 0.005..0.4 step 0.001 | s | decay |
| `thump` | 0.45 | 0..1.5 step 0.01 |  | sub thump amount |
| `click` | 0.18 | 0..1 step 0.01 |  | click amount |
| `seed` | 102 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `pop_up` (presets: `pop_up`)

A rising bloop: the pitch climbs well over an octave while it fades.

*Tips:* f0 -> f1 is the climb; tc how fast; tau the decay; wet the small room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.3 | 0.08..1.0 step 0.005 | s | length |
| `f0` | 480 | 60..3000 step 1 | Hz | pitch at the start |
| `f1` | 1550 | 100..6000 step 1 | Hz | pitch it climbs to |
| `tc` | 0.07 | 0.01..0.5 step 0.001 | s | glide time constant |
| `tau` | 0.06 | 0.01..0.5 step 0.001 | s | decay |
| `wet` | 0.06 | 0..0.4 step 0.01 |  | room amount |
| `seed` | 103 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `pluck` (presets: `pluck`)

A bright plucked string (Karplus-Strong) with a short attack click: a label or value snaps in.

*Tips:* f0 is the pitch; damp how long the string rings (0.999 = long); bright the excitation's brightness; tau an outer decay; the seed changes the string's noise.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1245 | 80..5000 step 1 | Hz | string pitch |
| `d` | 0.22 | 0.05..2.0 step 0.005 | s | length |
| `damp` | 0.993 | 0.9..0.9995 step 0.0005 |  | string damping per sample |
| `bright` | 0.75 | 0..1 step 0.01 |  | excitation brightness |
| `tau` | 0.06 | 0.01..1.0 step 0.001 | s | outer decay |
| `click` | 0.2 | 0..1 step 0.01 |  | attack click amount |
| `seed` | 104 | seed |  | the noise seed: change it for a sibling of the same sound |

### ticks

#### `tick` (presets: `tick`)

A crisp wooden tick: a 2 ms noise snap with a short ring and a little body under it.

*Tips:* f is the ring pitch (woodier lower, glassier higher); body the tonal body at f/3 (it is what keeps a tick audible under speech without hitting the peak cap); noise the snap amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 3400 | 500..10000 step 10 | Hz | ring pitch |
| `d` | 0.04 | 0.02..0.2 step 0.001 | s | length |
| `body` | 0.5 | 0..2 step 0.01 |  | tonal body amount |
| `noise` | 0.6 | 0..2 step 0.01 |  | snap amount |
| `seed` | 105 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `tick_double` (presets: `tick_double`)

Two ticks a few tens of ms apart, the second a step higher (a check mark being drawn).

*Tips:* f1/f2 are the two ring pitches; gap the time between; body and noise as for tick.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 3300 | 500..10000 step 10 | Hz | first ring pitch |
| `f2` | 3700 | 500..10000 step 10 | Hz | second ring pitch |
| `gap` | 0.055 | 0.02..0.4 step 0.001 | s | time between the ticks |
| `body` | 0.5 | 0..2 step 0.01 |  | tonal body amount |
| `noise` | 0.6 | 0..2 step 0.01 |  | snap amount |
| `seed` | 106 | seed |  | the noise seed: change it for a sibling of the same sound |

### clicks

#### `click` (presets: `click`)

A mouse click: a sharp press with a low thump, and a quieter release a few tens of ms later.

*Tips:* bright is the press's band (lower = duller); thump the low body's pitch; release_gap the time to the release click, bright2/thump2 its band and body, release_amp its loudness (0 removes it).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `bright` | 3000 | 500..10000 step 10 | Hz | press band centre |
| `thump` | 140 | 40..600 step 1 | Hz | thump pitch |
| `release_gap` | 0.03 | 0.0..0.3 step 0.001 | s | time to the release click |
| `bright2` | 3600 | 500..10000 step 10 | Hz | release band centre |
| `thump2` | 160 | 40..600 step 1 | Hz | release thump pitch |
| `release_amp` | 0.35 | 0..1 step 0.01 |  | release click amount |
| `d` | 0.07 | 0.03..0.5 step 0.001 | s | length |
| `seed` | 111 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `click_soft` (presets: `click_soft`)

A very light, muffled click.

*Tips:* bright and thump as for click; lowpass_hz muffles it (lower = softer).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `bright` | 1800 | 300..8000 step 10 | Hz | press band centre |
| `thump` | 110 | 40..600 step 1 | Hz | thump pitch |
| `lowpass_hz` | 3500 | 500..15000 step 50 | Hz | muffling low-pass |
| `d` | 0.05 | 0.02..0.3 step 0.001 | s | length |
| `seed` | 112 | seed |  | the noise seed: change it for a sibling of the same sound |

### pings

#### `ping` (presets: `ping`)

A small glass ping: inharmonic partials (1 : 2.32 : 4.25) that die quickly, in a small room.

*Tips:* f0 is the pitch; decay scales how long it rings; strike the noise transient's amount; wet the room. The partial ratios are glass; change them in the code for a different material.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 2015 | 300..8000 step 1 | Hz | pitch |
| `decay` | 1.0 | 0.3..4.0 step 0.05 |  | ring length multiplier |
| `strike` | 0.12 | 0..1 step 0.01 |  | strike noise amount |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.25 | 0.1..1.5 step 0.005 | s | length |
| `seed` | 107 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `ping_soft` (presets: `ping_soft`)

A lighter ping, lower, with a softer strike.

*Tips:* f0 the pitch; attack softens the onset (longer = gentler); decay the ring; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1453 | 300..8000 step 1 | Hz | pitch |
| `attack` | 0.003 | 0.0005..0.05 step 0.0005 | s | attack time |
| `decay` | 1.0 | 0.3..4.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.25 | 0.1..1.5 step 0.005 | s | length |
| `seed` | 108 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `ping_long` (presets: `ping_long`)

A ping that rings, with a slow beat between two close partials: a highlight while the eye moves.

*Tips:* f0 the pitch; beat the ratio of the second partial (1.003 = a slow beat, 1.01 = faster); decay the ring; keep it under about 0.6 s where speech follows.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1921 | 300..8000 step 1 | Hz | pitch |
| `beat` | 1.003 | 1.0..1.03 step 0.0005 |  | second partial ratio |
| `decay` | 1.0 | 0.3..4.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.15 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.55 | 0.1..3.0 step 0.005 | s | length |
| `seed` | 109 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `bong` (presets: `bong`)

A low, firm wooden bong: a marimba-like bar (partials near 1 : 3.9 : 9.2) and a mallet knock.

*Tips:* f0 the pitch (233 Hz = a low accent); decay the ring; knock the mallet's amount; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 233 | 60..1500 step 1 | Hz | pitch |
| `decay` | 1.0 | 0.3..4.0 step 0.05 |  | ring length multiplier |
| `knock` | 0.3 | 0..1 step 0.01 |  | mallet knock amount |
| `wet` | 0.06 | 0..0.5 step 0.01 |  | room amount |
| `d` | 0.3 | 0.1..2.0 step 0.005 | s | length |
| `seed` | 110 | seed |  | the noise seed: change it for a sibling of the same sound |

### ui

#### `toggle` (presets: `toggle`)

Two quick bright blips a fourth apart: a state flips on.

*Tips:* f1/f2 are the blips (f2 below f1 reads as 'off'); gap the time between; tau each blip's decay.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1406 | 200..6000 step 1 | Hz | first blip |
| `f2` | 1875 | 200..8000 step 1 | Hz | second blip |
| `gap` | 0.055 | 0.0..0.3 step 0.001 | s | time between the blips |
| `tau` | 0.018 | 0.005..0.1 step 0.001 | s | each blip's decay |
| `d` | 0.15 | 0.05..0.6 step 0.005 | s | length |
| `seed` | 113 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `switch` (presets: `switch`)

A mechanical switch: click-clack with a short metallic ring after each.

*Tips:* f1/f2 are the two rings' pitches; gap the time between click and clack; ring the ring amount; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1031 | 200..5000 step 1 | Hz | first ring pitch |
| `f2` | 890 | 200..5000 step 1 | Hz | second ring pitch |
| `gap` | 0.11 | 0.03..0.5 step 0.005 | s | time between click and clack |
| `ring` | 0.45 | 0..1.5 step 0.01 |  | metallic ring amount |
| `wet` | 0.07 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 114 | seed |  | the noise seed: change it for a sibling of the same sound |

### question

#### `question` (presets: `question`)

'Hmm?': a soft note, then a higher one that bends upwards at the end.

*Tips:* f1 is the first note, f2 the second; bend how far the second bends up (0.06 = 6 %); gap the time between them.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 659.25 | 100..3000 step 0.01 | Hz | first note (E5) |
| `f2` | 880 | 100..4000 step 0.01 | Hz | second note (A5) |
| `bend` | 0.06 | 0..0.3 step 0.005 |  | upward bend at the end |
| `gap` | 0.14 | 0.03..0.6 step 0.005 | s | time between the notes |
| `wet` | 0.1 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 118 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `question_alt` (presets: `question_alt`)

A single tone sliding up (a fifth by default): a lighter question.

*Tips:* f0 the start pitch; interval the ratio it slides to (1.5 = a fifth, 2 = an octave); slide the time the slide takes.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 988 | 100..4000 step 0.1 | Hz | start pitch (B5) |
| `interval` | 1.5 | 1.0..3.0 step 0.01 |  | ratio it slides to |
| `slide` | 0.2 | 0.05..0.6 step 0.005 | s | slide time |
| `d` | 0.36 | 0.15..1.5 step 0.005 | s | length |
| `wet` | 0.1 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 119 | seed |  | the noise seed: change it for a sibling of the same sound |

### error

#### `error` (presets: `error`)

A short, buzzy 'uh-oh': two square-ish tones stepping down a tritone, low-passed.

*Tips:* f1/f2 are the two tones (466 -> 330 Hz is a tritone; a bigger fall sounds worse); gap the time between; lowpass_hz the buzz's brightness; d2 the second tone's length.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 466 | 80..2000 step 1 | Hz | first tone |
| `f2` | 330 | 60..2000 step 1 | Hz | second tone |
| `gap` | 0.085 | 0.03..0.4 step 0.005 | s | time between the tones |
| `d2` | 0.16 | 0.05..0.6 step 0.005 | s | second tone length |
| `lowpass_hz` | 2600 | 500..10000 step 50 | Hz | buzz low-pass |
| `seed` | 120 | seed |  | the noise seed: change it for a sibling of the same sound |

### camera

#### `swell_up` (presets: `swell_up`)

A soft tonal lift for a push-in: a tone and its fifth gliding up, with a breath of air.

*Tips:* f0 -> f1 is the glide; d the length; air the pink breath's amount; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1078 | 100..5000 step 1 | Hz | start pitch |
| `f1` | 1640 | 100..6000 step 1 | Hz | end pitch |
| `d` | 0.28 | 0.1..1.5 step 0.005 | s | length |
| `air` | 0.25 | 0..1 step 0.01 |  | breath amount |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 122 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `swell_down` (presets: `swell_down`)

The mirror for a pull-back: gliding down, swelling into the end.

*Tips:* f0 -> f1 is the glide (down by default); the envelope is reversed, so it swells into its end.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1640 | 100..6000 step 1 | Hz | start pitch |
| `f1` | 1078 | 100..5000 step 1 | Hz | end pitch |
| `d` | 0.28 | 0.1..1.5 step 0.005 | s | length |
| `air` | 0.25 | 0..1 step 0.01 |  | breath amount |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 123 | seed |  | the noise seed: change it for a sibling of the same sound |

### notify

#### `notify` (presets: `notify`)

A two-tone notification: bell partials, the second note a third up.

*Tips:* f1/f2 are the two notes (a major third by default; a fifth is brighter, a minor third softer); gap the time between; decay the ring; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1046.5 | 200..5000 step 0.1 | Hz | first note (C6) |
| `f2` | 1318.5 | 200..6000 step 0.1 | Hz | second note (E6) |
| `gap` | 0.09 | 0.0..0.5 step 0.005 | s | time between the notes |
| `note_d` | 0.5 | 0.15..1.5 step 0.01 | s | each note's length |
| `decay` | 0.9 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 201 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `alarm` (presets: `alarm`)

An alternating two-tone square, low-passed: a warning that wants attention.

*Tips:* f1/f2 are the alternating tones; period the time per tone; cycles how many pairs; lowpass_hz the harshness (lower = softer); decay fades the whole thing out.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 880 | 100..4000 step 1 | Hz | high tone |
| `f2` | 660 | 100..4000 step 1 | Hz | low tone |
| `period` | 0.12 | 0.04..0.5 step 0.005 | s | time per tone |
| `cycles` | 3 | 1..12 step 1 |  | number of high-low pairs |
| `lowpass_hz` | 2400 | 400..10000 step 50 | Hz | square low-pass |
| `decay` | 0.6 | 0.1..5.0 step 0.05 | s | overall decay |
| `seed` | 202 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `countdown` (presets: `countdown`)

Three short beeps and a higher, longer fourth: three, two, one, go. Ends on the cue.

*Tips:* f is the beep pitch and f_go the last one's; interval the time between beeps; beep_d their length; the last beep rings longer. Lead = the whole length, so 'go' lands on the cue.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 880 | 200..4000 step 1 | Hz | beep pitch |
| `f_go` | 1760 | 200..6000 step 1 | Hz | final beep pitch |
| `interval` | 0.25 | 0.1..1.0 step 0.01 | s | time between beeps |
| `beep_d` | 0.07 | 0.03..0.3 step 0.005 | s | short beep length |
| `go_d` | 0.3 | 0.1..1.0 step 0.01 | s | final beep length |
| `seed` | 203 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `fail` (presets: `fail`)

Three soft descending notes: a gentle 'no', softer than error.

*Tips:* f1..f3 are the notes (E5, C5, A4 by default); step the time between; decay the ring. A smaller fall is sadder, a bigger one more comic.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 659.25 | 100..3000 step 0.01 | Hz | first note |
| `f2` | 523.25 | 100..3000 step 0.01 | Hz | second note |
| `f3` | 415.3 | 80..3000 step 0.01 | Hz | third note |
| `step` | 0.14 | 0.05..0.5 step 0.005 | s | time between notes |
| `note_d` | 0.32 | 0.1..1.0 step 0.01 | s | each note's length |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `wet` | 0.1 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 204 | seed |  | the noise seed: change it for a sibling of the same sound |

### keys

#### `keystroke` (presets: `keystroke`)

One key press: a plastic click with a short low thock under it.

*Tips:* bright is the click's band (higher = thinner keycap); thock the body pitch (lower = heavier key).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `bright` | 2400 | 500..8000 step 10 | Hz | click band centre |
| `thock` | 1100 | 200..4000 step 1 | Hz | body pitch |
| `d` | 0.045 | 0.02..0.2 step 0.001 | s | length |
| `seed` | 211 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `typing` (presets: `typing`)

A seeded burst of keystrokes with varied pitch, loudness and gaps: someone typing.

*Tips:* count is the number of keys; gap_lo/gap_hi the range between them (narrower = a machine, wider = a person); the seed picks the rhythm and the pitches; width spreads the keys across the field.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 10 | 2..40 step 1 |  | number of keystrokes |
| `gap_lo` | 0.06 | 0.02..0.5 step 0.005 | s | shortest gap |
| `gap_hi` | 0.13 | 0.03..1.0 step 0.005 | s | longest gap |
| `width` | 0.3 | 0..1 step 0.05 |  | stereo spread |
| `seed` | 212 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `camera_shutter` (presets: `camera_shutter`)

Two clicks a few tens of ms apart with a short noise swish between: a snapshot.

*Tips:* gap is the time between the two clicks; swish the noise amount between them; bright the clicks' band.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `gap` | 0.06 | 0.02..0.3 step 0.005 | s | time between the clicks |
| `swish` | 0.5 | 0..1.5 step 0.01 |  | swish amount |
| `bright` | 3200 | 500..8000 step 10 | Hz | click band centre |
| `seed` | 213 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `unlock` (presets: `unlock`)

Mechanical lock clicks: a click, a lower clack and a short spring ring; something opens.

*Tips:* gap is the time between click and clack; ring the spring's amount and ring_hz its pitch.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `gap` | 0.09 | 0.03..0.4 step 0.005 | s | time between click and clack |
| `ring` | 0.35 | 0..1.5 step 0.01 |  | spring ring amount |
| `ring_hz` | 2900 | 500..8000 step 10 | Hz | spring pitch |
| `seed` | 214 | seed |  | the noise seed: change it for a sibling of the same sound |

### foley

#### `page_turn` (presets: `page_turn`)

A band-passed noise swish, low-mid, quick attack and slow fall: a page or card flips.

*Tips:* f_start -> f_end is the band's slide; attack and tau the shape (longer tau = a bigger sheet); pan_from/pan_to the direction it moves.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.35 | 0.1..1.5 step 0.01 | s | length |
| `f_start` | 900 | 200..5000 step 10 | Hz | band at the start |
| `f_end` | 400 | 100..4000 step 10 | Hz | band at the end |
| `attack` | 0.02 | 0.002..0.2 step 0.001 | s | attack |
| `tau` | 0.12 | 0.02..0.6 step 0.005 | s | decay |
| `pan_from` | -0.3 | -1..1 step 0.05 |  | pan at the start |
| `pan_to` | 0.3 | -1..1 step 0.05 |  | pan at the end |
| `seed` | 221 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `stamp` (presets: `stamp`)

A low thump with a paper slap: a label stamped on, approved.

*Tips:* thump_hz is the thump's pitch (lower = heavier); slap the paper's amount; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `thump_hz` | 160 | 50..500 step 1 | Hz | thump start pitch |
| `slap` | 0.6 | 0..1.5 step 0.01 |  | paper slap amount |
| `tau` | 0.05 | 0.01..0.3 step 0.001 | s | thump decay |
| `wet` | 0.08 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 222 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `heartbeat` (presets: `heartbeat`)

Two thumps, lub-dub: a pulse, tension, something alive. Built to be heard on small speakers.

*Tips:* f is the thump pitch; knock the valve snap in the mids (what makes it audible on a laptop); body the chest resonance around 170 Hz; gap the time from lub to dub; tau the decay. Repeat every 0.8-1 s for a resting pulse, faster for fear.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 110 | 40..250 step 1 | Hz | thump pitch |
| `knock` | 0.9 | 0..2 step 0.05 |  | mid-range valve knock amount |
| `body` | 0.8 | 0..2 step 0.05 |  | chest body amount (170 Hz band) |
| `gap` | 0.28 | 0.1..0.8 step 0.005 | s | time from lub to dub |
| `tau` | 0.1 | 0.02..0.4 step 0.005 | s | thump decay |
| `d` | 0.8 | 0.4..2.0 step 0.01 | s | length |
| `seed` | 223 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `heartbeat_loop` (presets: `heartbeat_loop`)

A beating heart at a steady pulse, lub-dub after lub-dub; a seamless loop (each beat ends before the next).

*Tips:* bpm is the pulse (60-70 resting, 110-140 fear); beats how many fit in the loop; knock and body as for heartbeat; gap the time from lub to dub; f the pitch. The loop length is beats x 60 / bpm.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `bpm` | 72 | 40..180 step 1 | /min | beats per minute |
| `beats` | 4 | 1..16 step 1 |  | beats in the loop |
| `f` | 110 | 40..250 step 1 | Hz | thump pitch |
| `knock` | 0.9 | 0..2 step 0.05 |  | mid-range valve knock amount |
| `body` | 0.8 | 0..2 step 0.05 |  | chest body amount (170 Hz band) |
| `gap` | 0.28 | 0.1..0.6 step 0.005 | s | time from lub to dub |
| `tau` | 0.1 | 0.02..0.4 step 0.005 | s | thump decay |
| `seed` | 224 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `tick_tock` (presets: `tick_tock`)

Alternating woodblock ticks at two pitches: a clock, time passing.

*Tips:* f1/f2 are the two woods; interval the time between ticks; count how many. Half-second intervals read as a clock; faster reads as a timer.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 1400 | 300..5000 step 10 | Hz | first wood pitch |
| `f2` | 1100 | 300..5000 step 10 | Hz | second wood pitch |
| `interval` | 0.4 | 0.1..1.5 step 0.01 | s | time between ticks |
| `count` | 4 | 1..16 step 1 |  | number of ticks |
| `seed` | 224 | seed |  | the noise seed: change it for a sibling of the same sound |

### game

#### `coin` (presets: `coin`)

Two quick high square-ish notes, the second ringing: a point scored, a reward collected.

*Tips:* f1/f2 are the notes (B5 -> E6 by default, a fourth up); gap the time between; lowpass_hz the brightness of the square; decay the second note's ring.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f1` | 987.77 | 200..5000 step 0.01 | Hz | first note (B5) |
| `f2` | 1318.5 | 200..6000 step 0.01 | Hz | second note (E6) |
| `gap` | 0.07 | 0.02..0.3 step 0.005 | s | time between the notes |
| `lowpass_hz` | 6000 | 1000..15000 step 50 | Hz | square low-pass |
| `decay` | 0.18 | 0.05..1.0 step 0.005 | s | second note decay |
| `seed` | 231 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `level_up` (presets: `level_up`)

A fast rising five-note arpeggio with a shimmer on top: a milestone, bigger than success.

*Tips:* root sets the key; step the time between notes; sparkle the shimmer amount; decay the ring.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `root` | 1046.5 | 200..4000 step 0.1 | Hz | first note (C6) |
| `step` | 0.05 | 0.02..0.2 step 0.005 | s | time between notes |
| `note_d` | 0.5 | 0.15..1.5 step 0.01 | s | each note's length |
| `decay` | 1.1 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `sparkle` | 0.25 | 0..1 step 0.01 |  | shimmer amount |
| `wet` | 0.16 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 232 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `zap` (presets: `zap`)

A fast downward sweep of a filtered saw: a laser, an electric hit.

*Tips:* f_start -> f_end is the sweep; d its length; q the filter's bite; tau the decay.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.2 | 0.05..1.0 step 0.005 | s | length |
| `f_start` | 2400 | 300..10000 step 10 | Hz | sweep start |
| `f_end` | 180 | 40..3000 step 1 | Hz | sweep end |
| `q` | 1.4 | 0.4..6 step 0.05 |  | filter narrowness |
| `tau` | 0.08 | 0.02..0.5 step 0.005 | s | decay |
| `seed` | 233 | seed |  | the noise seed: change it for a sibling of the same sound |

### signal

#### `data_blips` (presets: `data_blips`)

A seeded stream of very short high blips: data transferring, packets flowing.

*Tips:* count is how many blips; d the window they fall in; f_lo/f_hi their pitch range; width the stereo spread; the seed picks the rhythm and pitches.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 12 | 2..60 step 1 |  | number of blips |
| `d` | 0.6 | 0.1..3.0 step 0.01 | s | window length |
| `f_lo` | 2000 | 300..10000 step 10 | Hz | lowest blip |
| `f_hi` | 5200 | 500..14000 step 10 | Hz | highest blip |
| `width` | 0.5 | 0..1 step 0.05 |  | stereo spread |
| `seed` | 241 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `scan` (presets: `scan`)

A rising sine sweep with tremolo: scanning, searching, a progress sweep.

*Tips:* f_start -> f_end is the sweep; d its length; tremolo_hz the flutter rate and depth its amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.6 | 0.15..3.0 step 0.01 | s | length |
| `f_start` | 400 | 60..4000 step 1 | Hz | sweep start |
| `f_end` | 2400 | 200..10000 step 1 | Hz | sweep end |
| `tremolo_hz` | 18 | 2..60 step 0.5 | Hz | tremolo rate |
| `depth` | 0.5 | 0..1 step 0.01 |  | tremolo depth |
| `seed` | 242 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `sonar` (presets: `sonar`)

A sine ping in a long, dark reverb: a probe, a search, waiting for a reply.

*Tips:* f is the ping's pitch; tau its own decay; tail and wet the dark room (damp_hz sets how dark).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 1200 | 200..5000 step 1 | Hz | ping pitch |
| `tau` | 0.12 | 0.02..0.6 step 0.005 | s | ping decay |
| `tail` | 1.6 | 0.3..5.0 step 0.05 | s | reverb length |
| `wet` | 0.5 | 0..1 step 0.01 |  | reverb amount |
| `damp_hz` | 2500 | 500..12000 step 50 | Hz | reverb damping |
| `seed` | 243 | seed |  | the noise seed: change it for a sibling of the same sound |

### water

#### `bubble` (presets: `bubble`)

Fast upward sine glides, seeded: water bubbles, a playful appear.

*Tips:* count is how many bubbles; spread the window they rise in; f_lo/f_hi their start pitch range; rise how far each glides up (ratio).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 3 | 1..12 step 1 |  | number of bubbles |
| `spread` | 0.3 | 0.0..2.0 step 0.01 | s | window they start in |
| `f_lo` | 300 | 80..2000 step 1 | Hz | lowest start pitch |
| `f_hi` | 700 | 100..4000 step 1 | Hz | highest start pitch |
| `rise` | 3.0 | 1.2..8.0 step 0.1 |  | glide ratio (end / start) |
| `wet` | 0.08 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 251 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `drop` (presets: `drop`)

A single water drop: a tiny tick and a short plink that glides down, in a small room.

*Tips:* f is the plink's pitch; tau its decay; wet the room (more = a bigger basin).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 1500 | 300..6000 step 1 | Hz | plink start pitch |
| `tau` | 0.05 | 0.01..0.3 step 0.001 | s | plink decay |
| `wet` | 0.18 | 0..0.6 step 0.01 |  | room amount |
| `seed` | 252 | seed |  | the noise seed: change it for a sibling of the same sound |

### ambience

#### `hum_loop` (presets: `hum_loop`)

A machine hum that exists on small speakers: a mains-like fundamental with a rich harmonic series peaking in a formant around 300-700 Hz (the transformer's rasp), a breathing fan bed of filtered noise above it, and a slow wobble; a seamless loop (every partial completes whole cycles).

*Tips:* f0 is the hum's pitch (50 or 60 Hz = mains; 55 = A1); formant where the harmonics peak (what a laptop hears); buzz the rasp of the upper harmonics; fan the noise bed's amount; breathe how much it all swells; d the loop length.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 55 | 30..220 step 0.5 | Hz | hum pitch |
| `d` | 4.0 | 1.0..16.0 step 0.5 | s | loop length |
| `formant` | 450 | 150..1500 step 10 | Hz | where the harmonics peak |
| `buzz` | 0.6 | 0..1.5 step 0.05 |  | rasp of the upper harmonics |
| `fan` | 0.5 | 0..1.5 step 0.05 |  | fan noise bed amount |
| `breathe` | 0.4 | 0..1 step 0.05 |  | swell depth |
| `seed` | 261 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `air_loop` (presets: `air_loop`)

Filtered pink noise with a slowly moving band: room tone, air, a quiet bed; a seamless loop.

*Tips:* f_lo/f_hi are the band's travel; d the loop length; lowpass_hz the overall darkness; the loop is crossfaded over 0.15 s so the seam is silent.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 4.0 | 1.0..16.0 step 0.5 | s | loop length (before the seam crossfade) |
| `f_lo` | 300 | 60..3000 step 10 | Hz | band low point |
| `f_hi` | 600 | 100..6000 step 10 | Hz | band high point |
| `lowpass_hz` | 4000 | 500..16000 step 50 | Hz | final low-pass |
| `seed` | 262 | seed |  | the noise seed: change it for a sibling of the same sound |

### nature

#### `rain_drops` (presets: `rain_drops`)

A few rain drops, built to measured drops: each an instant tick of 6-15 ms, broadband; drops that land in water add a short ring rising in pitch (the plink); on leaves or ground only the tick and a small thump. Spread across the field at irregular times.

*Tips:* count is how many drops; d the window; water the share of drops that land in water (0 = leaves or ground, 1 = a puddle); f_lo/f_hi the plink pitch (2-5 kHz on real drops); chirp how far it rises; body the thump of a big drop; wet the surface's room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 8 | 1..40 step 1 |  | number of drops |
| `d` | 1.2 | 0.3..4.0 step 0.05 | s | window the drops fall in |
| `water` | 0.6 | 0..1 step 0.05 |  | share of drops landing in water (plink) |
| `f_lo` | 1800 | 800..6000 step 10 | Hz | lowest plink pitch |
| `f_hi` | 4000 | 1000..9000 step 10 | Hz | highest plink pitch |
| `chirp` | 0.5 | 0..1.5 step 0.05 |  | how far the plink rises (1 = an octave) |
| `body` | 1.0 | 0..2 step 0.05 |  | big-drop thump amount (500 Hz to 2 kHz) |
| `wet` | 0.12 | 0..0.6 step 0.01 |  | room amount |
| `seed` | 301 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `rain_loop` (presets: `rain_loop`)

Steady rain, measured against real recordings: a falling roar with its weight between 250 Hz and 4 kHz, a surface band at 80-250 Hz (roof, window, ground), a granular 16-64 Hz drop texture, and individual drops as ticks 15-20 dB above the bed; the hiss above 4 kHz sits 15-20 dB under the mids. A seamless loop.

*Tips:* intensity moves light to pouring (more above 5 kHz, more roar, denser ticks); surface is the 80-250 Hz band's amount (ground 0.3, leaves 0.2, roof or skylight 1.0, window 0.8) and surface_hz where it sits; drops is ticks per second; hiss the air above 4 kHz; d the loop length.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 6.0 | 2.0..16.0 step 0.5 | s | loop length (before the seam crossfade) |
| `intensity` | 0.5 | 0..1 step 0.05 |  | light (0) to pouring (1) |
| `surface` | 0.7 | 0..2 step 0.05 |  | surface band amount (80-250 Hz) |
| `surface_hz` | 160 | 80..250 step 5 | Hz | surface band centre |
| `drops` | 25 | 0..300 step 1 | /s | individual drop ticks per second |
| `hiss` | 0.5 | 0..2 step 0.05 |  | air above 4 kHz |
| `seed` | 302 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `wave` (presets: `wave`)

One wave: a slow swell of band-passed noise that rises, breaks into foam and washes out.

*Tips:* d is the whole wave; crest where (0-1) it breaks; f_lo/f_hi the band's travel; hiss the foam; the pans move it along the shore.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 3.5 | 1.0..10.0 step 0.1 | s | length |
| `crest` | 0.42 | 0.15..0.8 step 0.01 |  | position of the break (0-1) |
| `f_lo` | 220 | 60..1000 step 10 | Hz | band at the start and end |
| `f_hi` | 1400 | 300..5000 step 10 | Hz | band at the crest |
| `hiss` | 0.5 | 0..1.5 step 0.05 |  | foam amount |
| `pan_from` | -0.4 | -1..1 step 0.05 |  | pan at the start |
| `pan_to` | 0.4 | -1..1 step 0.05 |  | pan at the end |
| `seed` | 303 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `waves_loop` (presets: `waves_loop`)

A beach: waves arriving one after another over a bed of surf; a seamless loop.

*Tips:* d is the loop length; waves how many arrive in it; hiss the foam; the bed is the distant surf.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 10.0 | 4.0..30.0 step 0.5 | s | loop length (before the seam crossfade) |
| `waves` | 2 | 1..6 step 1 |  | waves per loop |
| `hiss` | 0.5 | 0..1.5 step 0.05 |  | foam amount |
| `bed` | 0.25 | 0..1 step 0.05 |  | distant surf amount |
| `seed` | 304 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `thunder` (presets: `thunder`)

Thunder, measured against real strikes: a slow distant rumble, then strikes in clusters, two or three cracks close together, each collapsing into its own rumble that rolls in slow waves; irregular gaps; a secondary peal seconds later; a rumble bed under it all; a long dark reverb. The weight sits at 80-250 Hz, as it does in every recording.

*Tips:* approach is the distant rumble before the first hit (0 to start on the hit); clusters how many groups of strikes, per_cluster the most cracks in a group (2 to that many, 0.15-0.6 s apart; 1 = single hits); every crack has its own rumble (roll seconds, each a little different) 12-18 dB under the crack; overlap scales the irregular gaps between clusters; backoff how much quieter each later cluster is; peal the secondary peal 4-5 s after a cluster; hit the strike, rip the canvas tear in front of the first (close) one; roar the sliding mid band, rumble the 80-250 Hz weight and the sub; surge the bed under it all. Put the flash at `approach` seconds in.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `approach` | 2.5 | 0.0..6.0 step 0.1 | s | slow distant rumble before the first hit |
| `rumble` | 1.0 | 0..2 step 0.05 |  | 80-250 Hz weight and sub amount |
| `clusters` | 3 | 1..6 step 1 |  | groups of strikes at irregular intervals |
| `per_cluster` | 3 | 1..4 step 1 |  | cracks in a group at most (2 to this many, close together; 1 = single hits) |
| `hit` | 1.0 | 0..2 step 0.05 |  | strike amount |
| `clap` | 0.0 | 0..1 step 0.05 |  | replace the crack with a short loud rumble (0 = crack, 1 = rumble only) |
| `clap_gain` | 2.0 | 1..8 step 0.1 | x | level of the rumble clap relative to the roll it sits on |
| `rip` | 0.6 | 0..2 step 0.05 |  | canvas-rip amount in front of the first (close) hit |
| `roll` | 3.2 | 1.0..8.0 step 0.1 | s | rumble rolling out of each crack (each a little different) |
| `roar` | 1.0 | 0.2..2 step 0.05 |  | sliding mid band of the rolls |
| `overlap` | 0.6 | 0.2..1.5 step 0.05 |  | gap to the next cluster, as a fraction of the rumble (irregular, skewed short) |
| `backoff` | 0.9 | 0.3..1.0 step 0.05 |  | level of each later cluster relative to the one before |
| `grow` | 1.1 | 1.0..2.5 step 0.05 |  | length of each later cluster's rumbles relative to the one before |
| `peal` | 0.5 | 0..1.5 step 0.05 |  | secondary peal 4-5 s after each cluster |
| `surge` | 1.2 | 0..3 step 0.05 |  | long rumble bed swelling under the first hit, fading across the rest |
| `tail` | 3.0 | 0.5..6.0 step 0.1 | s | reverb length |
| `wet` | 0.25 | 0..0.8 step 0.01 |  | reverb amount (a reverb tail is noise: keep it under the arrivals) |
| `seed` | 305 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `wind_loop` (presets: `wind_loop`)

Wind: broad filtered noise with a slowly wandering whistle; a seamless loop.

*Tips:* f_lo/f_hi are the whistle's travel; whistle its amount (0 for plain air); d the loop length; gust how much the level breathes.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 8.0 | 3.0..30.0 step 0.5 | s | loop length (before the seam crossfade) |
| `f_lo` | 220 | 60..1500 step 10 | Hz | whistle low point |
| `f_hi` | 900 | 200..4000 step 10 | Hz | whistle high point |
| `whistle` | 0.5 | 0..1.5 step 0.05 |  | whistle amount |
| `gust` | 0.5 | 0..1 step 0.05 |  | level breathing depth |
| `seed` | 306 | seed |  | the noise seed: change it for a sibling of the same sound |

### combat

#### `explosion` (presets: `explosion`)

A close explosion: a crack, a sub boom, a noise body that decays, debris ticks and a long tail.

*Tips:* crack is the snap at the front; f0/f1 the boom's fall; body_tau how long the roar lasts; debris the seeded ticks after it; tail the reverb.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.6 | 0.5..4.0 step 0.05 | s | dry length |
| `crack` | 1.0 | 0..2 step 0.05 |  | initial crack amount |
| `f0` | 70 | 30..200 step 1 | Hz | boom start pitch |
| `f1` | 28 | 15..100 step 1 | Hz | boom end pitch |
| `body_tau` | 0.45 | 0.1..1.5 step 0.01 | s | roar decay |
| `debris` | 0.5 | 0..1.5 step 0.05 |  | debris ticks amount |
| `tail` | 1.8 | 0.3..5.0 step 0.1 | s | reverb length |
| `wet` | 0.3 | 0..0.8 step 0.01 |  | reverb amount |
| `seed` | 321 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `explosion_distant` (presets: `explosion_distant`)

An explosion far away: no crack, a soft low boom and a long rolling tail.

*Tips:* lowpass_hz is the distance (lower = farther); tail the air it rolls through.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.4 | 0.5..4.0 step 0.05 | s | dry length |
| `lowpass_hz` | 500 | 150..2000 step 10 | Hz | distance low-pass |
| `tail` | 2.6 | 0.5..6.0 step 0.1 | s | reverb length |
| `wet` | 0.45 | 0..0.9 step 0.01 |  | reverb amount |
| `seed` | 322 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `cannon` (presets: `cannon`)

A cannon: a hard low boom with a mid thump and a long tail; heavier and rounder than a gunshot.

*Tips:* f0/f1 the boom; thump the mid body; tail the field it echoes over.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.2 | 0.4..3.0 step 0.05 | s | dry length |
| `f0` | 95 | 40..250 step 1 | Hz | boom start pitch |
| `f1` | 34 | 15..100 step 1 | Hz | boom end pitch |
| `thump` | 0.8 | 0..2 step 0.05 |  | mid thump amount |
| `tail` | 1.6 | 0.3..5.0 step 0.1 | s | reverb length |
| `wet` | 0.28 | 0..0.8 step 0.01 |  | reverb amount |
| `seed` | 323 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `gunshot` (presets: `gunshot`)

A pistol shot: a snap, a mid crack, a low thump and a short slap-back.

*Tips:* bright is the crack's band; thump_hz the low body; crack the snap; room the slap-back amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `bright` | 2600 | 800..8000 step 10 | Hz | crack band centre |
| `thump_hz` | 150 | 50..400 step 1 | Hz | thump pitch |
| `crack` | 1.0 | 0..2 step 0.05 |  | snap amount |
| `tail_tau` | 0.12 | 0.03..0.5 step 0.005 | s | noise tail decay |
| `room` | 0.18 | 0..0.6 step 0.01 |  | slap-back amount |
| `seed` | 324 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `machine_gun` (presets: `machine_gun`)

A burst of automatic fire: seeded shots at a steady rate with small variations.

*Tips:* count is the number of rounds; rate the time between them; jitter their timing variance.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 8 | 2..40 step 1 |  | rounds |
| `rate` | 0.085 | 0.04..0.3 step 0.005 | s | time between rounds |
| `jitter` | 0.004 | 0..0.03 step 0.001 | s | timing variance |
| `bright` | 2200 | 800..8000 step 10 | Hz | crack band centre |
| `seed` | 325 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `shotgun` (presets: `shotgun`)

A shotgun: a wide low blast with a long noise tail, then the pump: click-clack.

*Tips:* blast is the low body; pump_gap the time before the pump action (0 removes it).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `blast` | 1.0 | 0.2..2 step 0.05 |  | low blast amount |
| `pump_gap` | 0.55 | 0..1.5 step 0.01 | s | time to the pump action |
| `tail_tau` | 0.25 | 0.05..0.8 step 0.005 | s | noise tail decay |
| `seed` | 326 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `tank_fire` (presets: `tank_fire`)

A tank's main gun: the muzzle blast, an explosion with a roar; discrete echoes off the landscape, each darker and quieter; and the shell piercing the air, a whistle that falls in pitch as it recedes.

*Tips:* blast is the explosion's amount; echoes how many returns off the hills, echo_gap their spacing, echo_drop dB lost per return; shell the whistle's amount, shell_hz its starting pitch, shell_d how long it takes to recede; rumble the low roll; tail the reverb.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `blast` | 1.0 | 0.2..2 step 0.05 |  | muzzle blast amount |
| `rumble` | 1.2 | 0.3..3.0 step 0.05 | s | low roll decay |
| `echoes` | 3 | 0..6 step 1 |  | returns off the landscape |
| `echo_gap` | 0.42 | 0.15..1.2 step 0.01 | s | time between returns |
| `echo_drop` | 7 | 2..15 step 0.5 | dB | level lost per return |
| `shell` | 1.0 | 0..2 step 0.05 |  | shell whistle amount |
| `shell_hz` | 2600 | 800..6000 step 10 | Hz | whistle start pitch |
| `shell_d` | 1.3 | 0.4..3.0 step 0.05 | s | time for the shell to recede |
| `tail` | 2.2 | 0.5..6.0 step 0.1 | s | reverb length |
| `seed` | 327 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `ricochet` (presets: `ricochet`)

A ricochet: a click, then a falling narrow whistle: the classic pee-yow.

*Tips:* f_start -> f_end is the whistle's fall; d its length; q its narrowness (higher = purer).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.45 | 0.15..1.5 step 0.01 | s | length |
| `f_start` | 5200 | 1500..12000 step 10 | Hz | whistle start |
| `f_end` | 1400 | 300..6000 step 10 | Hz | whistle end |
| `q` | 7 | 2..20 step 0.5 |  | whistle narrowness |
| `seed` | 328 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `arrow` (presets: `arrow`)

An arrow: the bow's twang, a short rising whoosh of flight, and a wooden thunk where it lands.

*Tips:* flight is the time in the air (the thunk lands at the end: use it as the lead); twang the string amount; thunk the impact.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `flight` | 0.45 | 0.15..1.5 step 0.01 | s | time in the air |
| `twang` | 0.7 | 0..1.5 step 0.05 |  | bow string amount |
| `thunk` | 1.0 | 0..2 step 0.05 |  | impact amount |
| `seed` | 329 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `sword_swing` (presets: `sword_swing`)

A blade swung through the air: a fast metallic whoosh with a thin high ring.

*Tips:* d is the swing's length; f_peak the whoosh's top; ring the blade's edge tone.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.32 | 0.1..1.0 step 0.01 | s | length |
| `f_peak` | 3200 | 800..9000 step 10 | Hz | whoosh peak band |
| `ring` | 0.25 | 0..1 step 0.01 |  | edge ring amount |
| `seed` | 330 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `sword_clash` (presets: `sword_clash`)

Two blades meeting: a sharp strike, an inharmonic metallic ring, a little room.

*Tips:* f0 is the ring's pitch; decay its length; strike the hit's amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 1180 | 300..4000 step 10 | Hz | ring pitch |
| `decay` | 1.0 | 0.3..3.0 step 0.05 |  | ring length multiplier |
| `strike` | 1.0 | 0..2 step 0.05 |  | strike amount |
| `wet` | 0.12 | 0..0.5 step 0.01 |  | room amount |
| `seed` | 331 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `punch` (presets: `punch`)

A body blow: a low thump with a short slap on top.

*Tips:* f is the thump pitch; slap the skin's snap; tau the decay.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 120 | 50..300 step 1 | Hz | thump pitch |
| `slap` | 0.6 | 0..1.5 step 0.05 |  | slap amount |
| `tau` | 0.07 | 0.02..0.3 step 0.005 | s | thump decay |
| `seed` | 332 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `hurt` (presets: `hurt`)

Taking damage: a short buzzy tone that drops, with a little noise: an 'oof' without a voice.

*Tips:* f0 -> f1 is the drop; d the length; lowpass_hz the buzz's brightness.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 420 | 100..1500 step 1 | Hz | start pitch |
| `f1` | 230 | 60..1000 step 1 | Hz | end pitch |
| `d` | 0.28 | 0.1..0.8 step 0.005 | s | length |
| `lowpass_hz` | 2200 | 500..8000 step 50 | Hz | buzz low-pass |
| `seed` | 333 | seed |  | the noise seed: change it for a sibling of the same sound |

### world

#### `spell_cast` (presets: `spell_cast`)

A spell: a rising tone with vibrato under a cloud of sparkle, in a bright reverb.

*Tips:* f_start -> f_end is the rise; d its length; sparkle the shimmer amount; vibrato_hz the wobble.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.1 | 0.4..3.0 step 0.05 | s | length |
| `f_start` | 320 | 80..2000 step 1 | Hz | rise start |
| `f_end` | 2200 | 300..8000 step 1 | Hz | rise end |
| `vibrato_hz` | 7 | 2..20 step 0.5 | Hz | vibrato rate |
| `sparkle` | 0.5 | 0..1.5 step 0.05 |  | shimmer amount |
| `wet` | 0.35 | 0..0.8 step 0.01 |  | reverb amount |
| `seed` | 341 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `fireball` (presets: `fireball`)

A fireball: a low whoosh with crackle that builds and lands in a soft boom. Ends on the cue.

*Tips:* d is the flight (lead = d so the boom lands on the cue); crackle the fire's amount; boom the impact.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.9 | 0.3..3.0 step 0.05 | s | flight length |
| `crackle` | 0.6 | 0..1.5 step 0.05 |  | crackle amount |
| `boom` | 0.8 | 0..2 step 0.05 |  | impact amount |
| `seed` | 342 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `heal` (presets: `heal`)

A heal: three soft ascending bell notes with slow attacks and a gentle sparkle.

*Tips:* root sets the key; step the time between notes; sparkle the shimmer; attack softens the onsets.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `root` | 1046.5 | 200..4000 step 0.1 | Hz | first note (C6) |
| `step` | 0.16 | 0.05..0.5 step 0.005 | s | time between notes |
| `attack` | 0.02 | 0.002..0.1 step 0.001 | s | note attack |
| `sparkle` | 0.3 | 0..1 step 0.05 |  | shimmer amount |
| `wet` | 0.25 | 0..0.6 step 0.01 |  | reverb amount |
| `seed` | 343 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `power_up` (presets: `power_up`)

A power-up: a quick rising run of eight square notes up the scale, the last one ringing.

*Tips:* root sets the key; step the speed; lowpass_hz the square's brightness.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `root` | 523.25 | 100..2000 step 0.01 | Hz | first note (C5) |
| `step` | 0.045 | 0.02..0.15 step 0.005 | s | time between notes |
| `lowpass_hz` | 5000 | 1000..15000 step 50 | Hz | square low-pass |
| `seed` | 344 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `burning_wood` (presets: `burning_wood`)

A wood fire: a low roar that breathes, with seeded crackles and pops; a seamless loop.

*Tips:* crackle is how many pops per second; roar the low bed; d the loop length.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 6.0 | 2.0..16.0 step 0.5 | s | loop length (before the seam crossfade) |
| `crackle` | 10 | 1..60 step 1 | /s | crackles per second |
| `roar` | 1.0 | 0..2 step 0.05 |  | low roar amount |
| `seed` | 345 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `door_open` (presets: `door_open`)

A door opens: a latch click, a slow creak of the hinge, and a soft stop.

*Tips:* d is the creak's length; f0 -> f1 the hinge's pitch travel; wobble its unevenness; latch the click at the start.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 0.9 | 0.3..3.0 step 0.05 | s | creak length |
| `f0` | 160 | 60..800 step 1 | Hz | hinge pitch at the start |
| `f1` | 240 | 60..1200 step 1 | Hz | hinge pitch at the end |
| `wobble` | 0.6 | 0..1.5 step 0.05 |  | hinge unevenness |
| `latch` | 0.8 | 0..1.5 step 0.05 |  | latch click amount |
| `seed` | 346 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `door_knock` (presets: `door_knock`)

Knocking on a wooden door: three knocks, each a knuckle tap with a wooden body.

*Tips:* count is the number of knocks; interval the time between; f the wood's pitch (lower = heavier door).

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 3 | 1..8 step 1 |  | number of knocks |
| `interval` | 0.22 | 0.1..0.6 step 0.005 | s | time between knocks |
| `f` | 180 | 80..500 step 1 | Hz | wood pitch |
| `seed` | 347 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `door_squeak` (presets: `door_squeak`)

A squeaky hinge: a long wavering squeal, high and uneven.

*Tips:* d is the length; f0 -> f1 the squeal's travel; wobble its waver.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `d` | 1.0 | 0.3..3.0 step 0.05 | s | length |
| `f0` | 1300 | 300..4000 step 10 | Hz | squeal start |
| `f1` | 2100 | 300..6000 step 10 | Hz | squeal end |
| `wobble` | 1.0 | 0..2 step 0.05 |  | waver |
| `seed` | 348 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `door_slam` (presets: `door_slam`)

A door slams: a heavy thud, a wooden body, a rattle of the frame and a short room.

*Tips:* f the thud's pitch (lower = heavier); rattle the frame's ticks; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 85 | 40..250 step 1 | Hz | thud pitch |
| `rattle` | 0.6 | 0..1.5 step 0.05 |  | frame rattle amount |
| `wet` | 0.18 | 0..0.6 step 0.01 |  | room amount |
| `seed` | 349 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `hammer` (presets: `hammer`)

A hammer on a nail: a hard tap, a bright ring, a wooden body underneath.

*Tips:* ring_hz is the nail's pitch; wood the body's amount; count the number of blows; interval between them.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 1 | 1..6 step 1 |  | number of blows |
| `interval` | 0.5 | 0.15..1.5 step 0.01 | s | time between blows |
| `ring_hz` | 3300 | 800..8000 step 10 | Hz | nail ring pitch |
| `wood` | 0.7 | 0..1.5 step 0.05 |  | wooden body amount |
| `seed` | 350 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `blacksmith` (presets: `blacksmith`)

A smith at the anvil: hammer blows on steel. Each blow is a hard clank, a very short high ping off the anvil, and the iron's own vibration, a buzzing beat that fades. Not a bell: nothing rings in tune.

*Tips:* count is the number of blows; interval the rhythm (a smith is steady, with a little drift); ting_hz the anvil's ping (high, short), ting its amount; buzz_hz the iron's vibration pitch, buzz its amount, beat how fast it throbs, decay how long it fades; wet the room.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 4 | 1..12 step 1 |  | number of blows |
| `interval` | 0.45 | 0.15..1.5 step 0.01 | s | time between blows |
| `ting_hz` | 3600 | 1500..8000 step 10 | Hz | anvil ping pitch |
| `ting` | 0.6 | 0..1.5 step 0.05 |  | anvil ping amount |
| `buzz_hz` | 620 | 150..2000 step 10 | Hz | iron vibration pitch |
| `buzz` | 1.0 | 0..2 step 0.05 |  | iron vibration amount |
| `beat` | 24 | 4..80 step 1 | Hz | vibration throb rate |
| `decay` | 0.35 | 0.08..1.2 step 0.01 | s | vibration fade |
| `wet` | 0.2 | 0..0.6 step 0.01 |  | room amount |
| `seed` | 351 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `footstep` (presets: `footstep`)

One footstep: a heel, a toe and a little body, on a hard floor.

*Tips:* surface_hz sets the floor (lower = softer ground, higher = tile); heavy the weight of the body.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `surface_hz` | 1800 | 300..6000 step 10 | Hz | surface brightness |
| `heavy` | 1.0 | 0.3..2.5 step 0.05 |  | body weight |
| `seed` | 352 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `footsteps` (presets: `footsteps`)

Walking: seeded steps at a steady pace, alternating left and right.

*Tips:* count is the number of steps; interval the pace; surface_hz the floor; heavy the weight.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `count` | 6 | 2..20 step 1 |  | number of steps |
| `interval` | 0.42 | 0.15..1.2 step 0.01 | s | time between steps |
| `surface_hz` | 1800 | 300..6000 step 10 | Hz | surface brightness |
| `heavy` | 1.0 | 0.3..2.5 step 0.05 |  | body weight |
| `seed` | 353 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `jump` (presets: `jump`)

A jump: a quick rising boing with a soft push of air.

*Tips:* f0 -> f1 is the rise; d its length.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f0` | 280 | 80..1000 step 1 | Hz | start pitch |
| `f1` | 900 | 200..3000 step 1 | Hz | end pitch |
| `d` | 0.28 | 0.1..0.8 step 0.005 | s | length |
| `seed` | 354 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `land` (presets: `land`)

Landing: a thump with a short scuff of dust.

*Tips:* f the thump; scuff the dust's amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 110 | 40..300 step 1 | Hz | thump pitch |
| `scuff` | 0.5 | 0..1.5 step 0.05 |  | dust amount |
| `seed` | 355 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `chest_open` (presets: `chest_open`)

A chest opens: a latch, a short creak of the lid, then a rising sparkle of treasure.

*Tips:* creak is the lid's length; sparkle the treasure's amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `creak` | 0.5 | 0.2..1.5 step 0.05 | s | lid creak length |
| `sparkle` | 0.6 | 0..1.5 step 0.05 |  | treasure sparkle amount |
| `seed` | 356 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `reload` (presets: `reload`)

A reload: the magazine out, a slide of metal, the magazine in and the bolt: click, slide, clack-clack.

*Tips:* gap is the time between the actions; slide the metal slide's amount.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `gap` | 0.22 | 0.08..0.6 step 0.01 | s | time between actions |
| `slide` | 0.6 | 0..1.5 step 0.05 |  | metal slide amount |
| `seed` | 357 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `game_over` (presets: `game_over`)

Game over: three slow falling notes over a low tone, in a long room.

*Tips:* root sets the key; step the time between notes; the fall is a minor third then a fourth.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `root` | 440 | 100..2000 step 0.1 | Hz | first note (A4) |
| `step` | 0.4 | 0.15..1.0 step 0.01 | s | time between notes |
| `tail` | 1.8 | 0.4..5.0 step 0.1 | s | reverb length |
| `seed` | 358 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `war_horn` (presets: `war_horn`)

A war horn: a brass-like call that swells and opens, with a faint octave below.

*Tips:* f is the horn's note (G3 = 196); d its length; open how far the tone brightens; vibrato its shake.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `f` | 196 | 60..600 step 1 | Hz | horn pitch |
| `d` | 1.8 | 0.6..5.0 step 0.05 | s | length |
| `open` | 0.7 | 0..1 step 0.05 |  | brightening |
| `vibrato` | 0.4 | 0..1 step 0.05 |  | vibrato depth |
| `tail` | 1.6 | 0.3..5.0 step 0.1 | s | reverb length |
| `seed` | 359 | seed |  | the noise seed: change it for a sibling of the same sound |

#### `drum_march` (presets: `drum_march`)

A military snare: four strokes and a roll, the pattern of a march.

*Tips:* tempo is the stroke interval; roll_len the roll's length; snare the wires' brightness.

| parameter | default | range | unit | meaning |
|---|---|---|---|---|
| `tempo` | 0.3 | 0.12..0.8 step 0.01 | s | stroke interval |
| `roll_len` | 0.6 | 0.2..2.0 step 0.05 | s | roll length |
| `snare` | 1.0 | 0..2 step 0.05 |  | snare wire amount |
| `seed` | 360 | seed |  | the noise seed: change it for a sibling of the same sound |

