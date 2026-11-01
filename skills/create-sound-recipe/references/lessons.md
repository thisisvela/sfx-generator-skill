# Lessons ledger: create-sound-recipe

Read before adding a recipe. Append one entry per recipe added (what it is physically, the blocks it took, what
went wrong first, what mattered, the approved numbers). Newest last.

## Standing lessons

- Describe the physics first; the block list follows from it. Every family in the library is one of: moving
  band-passed noise, partial stacks with inharmonic ratios, a sine with a gliding pitch, a plucked string, a click
  core with a body, or a seeded cloud of short events.
- Every literal a recipe uses becomes a parameter with that literal as its default. Deriving one value from
  another (`root * ratio`) is not float-exact and breaks determinism against approved files.
- Verify by numbers: length, decay to −20 dB, centroid, pitch track, DC, end level, peak, loudness, mono sum.
  Then the spectrogram. Then a person.

## Entries

### 2026-10-31 · notify, alarm, countdown, fail (tonal signals)
- bell `note()` with a `decay` multiplier covers notify; squares via summed odd harmonics + low-pass cover alarm;
  `place()` sequences beeps. countdown is category anticipation with lead = its length so "go" lands on the cue.
- fail reused the question family's SOFT partials; three notes at 140 ms steps measured 0.74 s with decay 0.25 s.

### 2026-10-31 · keystroke, typing, camera_shutter, unlock (mechanisms)
- a key is `click_core` + a 1.1 kHz "thock" (0.8 amp, tau 6 ms). Without the thock keystrokes measured −21 LUFS
  and were capped 12 LU under the voice; with it −18 LUFS, 8 LU under.
- summing many click cores leaves DC above 0.002: high-pass at 90 Hz before `finish`.
- typing's rhythm comes from `rng.uniform(gap_lo, gap_hi)`; a narrower range reads as a machine.

### 2026-10-31 · page_turn, stamp, heartbeat, tick_tock (foley)
- page_turn: two band-pass stages (fc and 1.6 fc) on pink with a 20 ms attack and a 120 ms decay; the pan from
  −0.3 to 0.3 is the "turn". Category transition with a 0.06 s lead.
- heartbeat: a 90→45 Hz glide with a low-passed knock; the dub is 0.7 × the lub, 0.28 s later. Centroid 72 Hz;
  it reads on small speakers only through the knock.
- tick_tock: a wood is a 3-partial tone (1, 2.4, 4.1) with tau 18 ms plus a 600-5000 Hz burst; alternating pans
  ±0.15 make the two pitches read as two sides of a clock.

### 2026-10-31 · coin, level_up, zap (game)
- coin: summed odd harmonics with a 0.3 second harmonic, low-passed at 6 kHz, two notes B5→E6; the second rings
  3 × its decay. level_up = five bell notes at 50 ms steps + `shimmer_core` × 0.25.
- zap: a band-limited saw (10 harmonics) swept 2.4 kHz→180 Hz in log space through an SVF at 1.5 fc; without
  the +0.35 dry signal it was all whistle and no bite.

### 2026-10-31 · data_blips, scan, sonar (signals)
- data_blips: sorted seeded starts, 12-25 ms sines at log-uniform pitches, 4 ms releases, ±0.5 pan. It measured
  −12 LUFS at −6 LU (ui) without capping because each blip has 8 ms of tau body.
- scan: tremolo as `1 − depth·0.5·(1 − cos 2π·18·t)`; the sin²/cos² envelope keeps both ends clean (end −119 dB).
- sonar: a 1.2 kHz sine (tau 0.12) in a 1.6 s reverb damped at 2.5 kHz, wet 0.5; `trim_tail` cut it to 1.66 s.

### 2026-10-31 · bubble, drop (water)
- a bubble is a sine gliding up 3× with tc 35 ms and tau 45 ms; three of them seeded within 0.3 s. A drop is the
  reverse: a glide down 0.6× with a 4 ms high-passed tick in a 0.5 s room.

### 2026-10-31 · hum_loop, air_loop (ambience)
- seamless by construction: `_cycles(f, d) = round(f·d)/d` makes every partial and LFO complete whole cycles in the
  loop; no fades at the edges; `norm` only. The quality test checks the wrap jump against the largest step inside.
- noise cannot be periodic: `loop_seam(x, 0.15)` crossfades the tail into the head and drops the tail (the loop
  is 0.15 s shorter than `d`).
- a new category `ambience` at −16 LU: loops run under a whole beat, so they must sit far under everything.

### 2026-10-31 · nature: rain_drops, rain_loop, wave, waves_loop, thunder, wind_loop
- a wave is a slow sin²/cos envelope over a band of pink whose centre rises to the crest and falls back, with
  white "foam" entering just before the crest; `waves_loop` wraps the last wave's tail into the start of the loop
  before `loop_seam`, so the loop never has a gap.
- thunder: the roll is white noise through two 140 Hz low-passes, modulated by two slow sines, plus a sub glide
  55→30 Hz and a 90 ms high-passed crack; the reverb is damped at 1.8 kHz. The crack is a parameter so distant
  thunder is `crack=0`.
- a stereo bed of two independent pink noises loses 3 dB in mono (the warning fires). Share one bed between the
  ears and let only the whistle differ.

### 2026-10-31 · combat: explosion, explosion_distant, cannon, gunshot, machine_gun, shotgun, tank_fire, ricochet, arrow, sword_swing, sword_clash, punch, hurt
- every blast is `_boom` (sub glide + knock + body band) plus a crack burst and a reverb damped at 2.5-3.5 kHz;
  distance is a low-pass plus more and darker reverb.
- a gunshot's four parts: a 6 ms snap, a 20 ms band-passed crack, a thump gliding to 40 % of its pitch, and a
  low-passed noise tail; `machine_gun` repeats it with ±10 % band and 75-100 % level per round. Many summed
  thumps leave DC: high-pass at 60 Hz.
- a ricochet is two SVF stages at Q 7 following a 5.2 kHz → 1.4 kHz curve (t^0.7), driven by white noise.
- an arrow's thunk is a low-passed burst + a 190→120 Hz glide + a 410 Hz wood tone, placed at `flight`; the
  preset's lead equals the flight so the thunk lands on the cue.
- adding arrays of different lengths is the commonest crash: pad the shorter into a zero buffer first.

### 2026-10-31 · world: spell_cast, fireball, heal, power_up, burning_wood, door_open, door_knock, door_squeak, door_slam, hammer, blacksmith, footstep, footsteps, jump, land, chest_open, reload, game_over, war_horn, drum_march
- a creak is a saw+square at a slowly rising pitch, modulated by a seeded random walk and a 14-20 Hz stick-slip
  grain, through an SVF at 2.2× the pitch; the same `_creak` serves doors and the chest lid.
- a footstep is heel (low-passed noise, 25 ms) + toe (a softer burst 60 ms later) + a short body glide; it sits
  at ui (−6 LU) and needed a 70 Hz high-pass for DC.
- a horn is a band-limited saw with a sub-octave, through an SVF whose centre opens with the envelope; vibrato
  arrives after 30 % of the note.
- a snare stroke is white noise through an SVF at 2.6 kHz (Q 0.6) with a 240→180 Hz body; a roll is strokes
  every 55 ms with rising level and ±4 ms jitter.

### 2026-11-01 · rebuilt by ear and by measurement: thunder, rain_loop, rain_drops, blacksmith, tank_fire, hum_loop
- thunder, four times over, until it measured like the real thing: the weight at 80-250 Hz (not the sub), the
  rumble a Poisson train of 3-14 ms N-wave pulses with lognormal sizes (`_arrivals`; kurtosis 7-32 in the band,
  filtered noise scored 0.9 and was heard as wind), the crack a 100-300 ms crackle build-up with no oscillator
  (a 95→28 Hz sine was heard as a kick drum), hits in clusters with skewed random gaps, every hit with its own
  full rumble, a slow surge under all of it, a secondary peal 4-5 s after each cluster, reverb kept low (a
  reverb tail is Gaussian and turns arrivals back into wind), a 40 Hz high-pass at the end. The crack can be
  replaced by a short loud rumble (`clap`); the shipped preset uses that. Timing and content on separate seeds.
- rain_loop: a falling bed (pink through 900 Hz and 420 Hz bands, a `surface` band at 160 Hz, low-passed at
  3.6 kHz, air 15-20 dB under), a 16-64 Hz granular texture, and band-limited drop ticks 16-24 dB above the bed;
  centroid 4374 → 1355 Hz, slope +1.7 → −5.3 dB/oct. "Rain" built from the word was hiss.
- rain_drops: a 2.5 ms broadband tick, a 3 ms thump for a big drop, and for a `water` share a ring whose pitch
  rises over 30-60 ms; 11 ms to −20 dB. The first version was an 82 ms tonal blob with a falling glide.
- blacksmith: clank (4 ms burst + 700 Hz knock), a tight ping above 3 kHz gone in 0.09 s, and the iron's
  vibration as partial pairs beating at 24 Hz through tanh, fading over 0.35 s. The first version was a tuned
  `tone` and was heard as a bell.
- tank_fire: `_boom` plus a roar band sliding 900 → 140 Hz, three discrete echoes 7 dB apart and darker each
  time, and a Q-14 whistle falling from 2600 Hz over 1.3 s panning away. Mood huge. The breech "ring" was a bell.
- hum_loop: 24 partials weighted by a formant at 450 Hz, odd partials stronger, soft saturation with the mean
  removed (DC thumps at the seam), a fan bed loop-seamed from a buffer 0.15 s longer than the loop; laptop loss
  16.6 → 0.5 dB. A 55 Hz sine with six harmonics was inaudible on a laptop.
- the master grew two stages that any new recipe can use: `mood` (huge −12 / big −14 LUFS body, peak caps −3 /
  −4.5 / −6 in the mix) and `presence` (harmonics of the band under 250 Hz for small speakers). Decide the mood
  from the situation; run `tools/laptop_check.py` on every new low sound.
- lesson: for natural sounds the recipe is written from measurements, not from the word. The checks that
  settled each argument in minutes: band shares and slope, kurtosis of the weight band, onset length at 5 ms
  with pitch strength, and the 250 Hz high-pass loss.
