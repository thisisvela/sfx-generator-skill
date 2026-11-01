# Lessons ledger: make-sound-effect

Read this before every generation. Append one entry after every generation (format at the end of SKILL.md).
Newest last. If a run contradicts an earlier lesson, say so in the new entry; do not edit the old one.

## Standing lessons (from building the first 37 sounds)

1. **Too quiet is the common failure.** The first level table put effects 13-19 LU under the voice and nobody could
   hear them. The table was raised about 5 dB. When in doubt, the sound is too quiet, not too loud.
2. **Very short sounds vanish under speech.** A 30 ms glitch measured 17 LU under the voice; the moment it marked was
   silent. Under speech, use 0.1 s or more of real energy (`glitch_burst`, 0.38 s, replaced it).
3. **Transients hit the peak cap first.** Add tonal body under a click (a short sine at f/3), not gain. This raised
   the clicks and ticks 4-5 dB against the voice.
4. **Every note needs a release fade.** Notes stopped while still ringing (8 % amplitude at the end of a 0.55 s note
   with tau 0.22 s) showed as vertical lines in the spectrogram: clicks.
5. **Karplus-Strong needs DC removal.** A noise excitation with a non-zero mean circulated as a low rumble, and the
   pitch analysis read 0 Hz.
6. **Chime tails linger under narration.** Shortening the bell decays (tau 0.22 → 0.16 s) and `ping_long`
   (0.7 → 0.55 s) helped; keep tails under about 0.5 s where speech follows.
7. **"Hmm?" rises.** An earlier question motif fell (1,546 → 750 Hz); a rising E5 → A5 with a 6 % bend at the end read
   as a question to the owner where the falling one did not.
8. **A bell is mismatched partials.** (1, 2.01, 3.02, 4.17) rings like a bell; exact integers ring like an organ.
9. **A pan sells motion.** Whooshes panned right to left read as "something flew past"; centred ones read as a rise.
10. **Measure against the voice directly**, in the same windows; never by subtracting narration from an AAC mix.

## Standing lessons from the listening passes (2026-10-31 to 2026-11-01)

Each of these was learned by fixing one sound and is recorded in full in the entries below; this is the short
form to read before any run.

11. **Energy above about 150 Hz, or the sound does not exist on a laptop.** The level rule is K-weighted and
    cannot see it (heartbeat, thunder, hum_loop, the deep impacts all measured fine and were silent). Check every
    thump, boom, bed and loop through a 250 Hz high-pass (`levels.body_lufs` of the filtered render;
    `tools/laptop_check.py` does the whole library); more than 3 dB lost means `presence` first, a mid-range body
    in the recipe second. Beds are the most at risk because they are placed quietest.
12. **Short, quiet, low events need repetition to be auditioned at all.** When a person cannot hear a sound that
    measures fine, offer the looped or repeated form (heartbeat_loop) before touching the level.
13. **Anything "roaring" or "rolling" is a sequence, not an event.** Several overlapping events whose lengths grow
    and whose levels back off, with movement inside each; a single decaying noise is a boom or a hiss.
14. **Build the sequence the person describes, one stage per act, one parameter per act.** Read the adjectives as
    recipes ("felt not heard" is sub, "grinding" is a 6-12 Hz modulation, "canvas ripping" is a bright band torn
    at 40-70 Hz). When a fix adds parts and they still say no, remove parts and ask for the shape in one sentence.
15. **The weight of a sound follows its situation, and the ear sums over seconds.** Decide the mood first (fear,
    violence, the sky: huge; a slam or a shot: big; interface and foley: normal), master the body to it, then
    place it. "Louder" has two homes: the body of the file (only as far as the limiter goes without flattening
    the shape) and the peak cap in the mix (`PEAK_CAP_BY_MOOD`); never more limiting.
16. **A sequence of events needs a bed of its own under it,** or it sounds like samples played in a row. When a
    person asks for "more" of a layer, double it before judging.
17. **Timing comes from who made the sound.** Man-made: a steady rhythm (gunfire, machines, clocks, typing).
    Natural: clusters with irregular, skewed gaps, never even. A pattern the ear must count needs every member at
    full weight (backoff is for tails, not events); make the counts explicit parameters.
18. **A ring is a bell; a vibration is a beat.** No tuned `tone` with bell ratios on anything that is not a bell
    or a chime (anvils, guns, tanks, doors, rails: a clank or a buzz of beating partials). "Echoes" are discrete
    returns with a gap, darker each time; a reverb tail is a room. A receding object is a falling pitch plus a
    pan away.
19. **Measure the real thing before trusting the words.** "Rumble" reached for the sub and "rain" for hiss; the
    recordings put thunder's weight at 80-250 Hz and rain's at 250 Hz-4 kHz. Run `tools/analyse_recordings.py`
    on a free recording and on the render side by side, set the targets from the numbers, iterate on the numbers,
    and when a band will not move find every helper that feeds it. Recordings are for analysis only, never
    shipped, never named.
20. **A sine sweep is a drum, wherever you put it.** Booms get their weight from the length of their pulses and
    their resonances, not from an oscillator gliding down. A natural crack is a 100-300 ms build-up of crackle,
    not an onset; measure onsets at 5 ms with a pitch-strength check before calling anything a crack.
21. **Rumble is arrivals, wind is noise; kurtosis tells them apart.** Any natural rumble, roar or roll is a pile
    of impulsive events with heavy-tailed sizes (`_arrivals`), a few hundred a second at most, reverb kept under
    them, and never a resonator on an impulse. `tools/rumble_texture.py`: kurtosis under 3 in the weight band
    means wind.
22. **Structure and content on separate random streams.** Timing from one seed, what sounds at each time from
    another, so a variant changes only what it is meant to change. When the owner designs a fix in numbers
    ("100 % louder, 60 % shorter, peak on the same time"), build exactly that beside the original for A/B, then
    ship only the version they choose and retire the other.
23. **"Louder on a laptop" is not gain, it is where the energy sits.** `presence` adds harmonics of the band
    under 250 Hz at 200-1200 Hz and tames that band's peaks (which set the ceiling yet the speaker cannot play);
    a sound whose weight is under 250 Hz can only ever be a few dB louder on a laptop, the rest is physics.
24. **A drop is a tick, and a plink rises.** A drip, drop or plink is an instant broadband impact of a few
    milliseconds; its tonal part, if any, is short and rises in pitch. A falling glide is a cartoon.
    `tools/drops_analysis.py` measures onset length and pitch direction.
25. **A hum is a formant, not a fundamental.** A bed that sits 16 LU under the voice must put its energy where
    every speaker plays it: partials weighted around a few hundred Hz, a little saturation (mean removed, or the
    loop thumps at its seam), a breathing noise bed.
26. **Every fix writes a lesson, and every batch of low sounds triggers the whole-library laptop check.**

## Lessons from building this package (2026-10-31)

### 2026-10-31 · port of the 37 reference sounds
- the port is sample-exact against the original generator; the OGG masters differ by up to 0.05 from a fresh
  encode only because libvorbis builds differ. Compare floats (hashes), tolerate encoders.
- float-exactness traps: derive nothing. `1046.5 * (1318.5 / 1046.5)` is not `1318.5`; `3000 * 1.2` may not be
  `3600`. Every value a recipe used must be a parameter with that literal as its default.

### 2026-10-31 · 22 new sounds
- click cores summed many times (typing, unlock, camera_shutter) accumulate DC past 0.002: high-pass at 90 Hz
  before `finish`.
- keystrokes needed more body (0.8 × a 1.1 kHz thock, tau 6 ms) to sit above −20 LUFS; the first version was
  capped 12 LU under the voice.
- a seamless loop: give every partial and LFO a whole number of cycles in the loop length (`round(f*d)/d`); noise
  beds need `loop_seam` (a 0.15 s crossfade). Test the seam: the wrap jump must be no bigger than any step inside.
- anticipation sounds (riser, swell, swoosh_up, countdown) end on the cue by design: their end level is above −40
  dB and that is correct; exempt them from the end-level check.

### 2026-10-31 · "soft two-note success chime, about half a second" (acceptance run)
- mapped: success (12.6), ding (6.3); base success; category positive
- moved: "soft" -> wet 0.14→0.16 (the only soft-able parameter success has); "half a second" -> d=0.5, but the
  room tail made the file 0.82 s
- numbers: all four −4.0 LU, none capped, decay 0.33 s; no warnings
- lesson: on chimes "about half a second" means the audible decay, so set `decay` (and `note_d`), not `d`; and
  "soft" on a bell wants a longer `attack`, which the chime recipes do not expose yet (candidate for a recipe
  change: add `attack` to `note`)
- the seed changes nothing on tonal recipes: `sfx make` now offers a pitch sibling instead and says so

### 2026-10-31 · "quick whoosh for a slide" (acceptance run)
- mapped: whoosh (16.7), whoosh_short (9.8); base whoosh; "quick" -> d 0.7→0.455; the result is a whoosh_short
  by another route. When a preset already exists for the adjective (whoosh_short), prefer it as the base: it was
  approved by ear.

## Lessons from the owner's listening pass (2026-10-31)

### heartbeat · "I cannot even hear the heart beat"
- numbers before: centroid 72 Hz, pitch track 93→46 Hz, −8.2 LUFS, placed at −4 LU: by the level rule it was
  fine. By ear it was silent, because every bit of energy sat below 100 Hz, which laptop and phone speakers
  cannot reproduce, and K-weighting discounts those frequencies so the loudness number never complained.
- fix: a mid-range "valve knock" (band-passed burst at 420 Hz), a chest body band at 170 Hz, a second harmonic
  on the thump, and the thump pitched higher (glide 176→66 Hz). The dub is shorter and 15 % higher than the lub.
- lesson: **a sound must carry energy above ~150 Hz to exist on small speakers.** The level rule cannot see this.
  `sfx inspect` now warns "sub-only" when the centroid is under 120 Hz. Applies to any thump, boom, impact,
  footstep or drop: the sub is the weight, the mids are the audibility.

### heartbeat_loop · "still can't hear it, probably too quick"
- a single 0.64 s lub-dub is over before the ear settles on it; the character of a pulse is in its repetition.
- fix: `heartbeat_loop`, beats at a steady bpm from the same thump, seamless because every beat ends in silence
  before the next (no crossfade needed). 72 bpm resting, 110-140 for fear.
- lesson: **short, quiet, low events need repetition or a longer form to be auditioned at all.** When a person
  says they cannot hear a sound that measures fine, offer the looped or repeated form before touching the level.

### thunder · "does not sound like thunder; it needs to be one strike with two or three thunders of different lengths and backoff"
- before: one crack and one low rumble (noise low-passed at 140 Hz) under a long reverb: a single soft boom with
  a hiss on the front, nothing that rolled.
- fix: a `_peal` helper (a crack, a tearing roar, a sub) placed two to four times inside one strike. The roar is
  pink noise band-passed with the band sliding from 700 Hz down to ~125 Hz and torn by a 4-14 Hz random
  modulation, so it rips rather than hisses. Peal i is `grow`^i times longer, `backoff`^i times quieter, its
  crack weaker and its band darker (farther), and it starts once the previous peal has fallen about 16 dB, so
  the envelope shows separate claps (0 s, 1 s, 2.6 s at the defaults) bridged by the reverb.
- numbers: centroid 1438 Hz (the cracks), most energy still under 150 Hz (the weight), three rises in the
  100 ms envelope with 10-17 dB valleys between them; no warnings.
- lesson: **a thunderclap is a sequence, not an event.** Anything a person describes as "roaring" or "rolling"
  (thunder, an avalanche, a crowd, a distant battle) wants several overlapping events whose lengths grow and
  whose levels back off, plus modulation inside each one; a single decaying noise reads as a boom or a hiss.
  Expose the count, the backoff and the growth as parameters so the tuner can make it one clap or a long roll.

### thunder, second pass · the owner wrote a three-paragraph description of thunder
- the peal version was still "not yet perfect". The owner's description had three acts: (1) a low, guttural
  rumble, felt in the chest, grinding like boulders or a distant train, a drumroll that melts back into the rain;
  (2) a deafening crack, heavy canvas ripped in half, then a sharp percussive explosion that rattles the panes;
  (3) the shockwave collapsing into a heavy boom that rolls in overlapping waves and fades into a hollow growl.
- fix: one stage per act, each with its own parameter so the tuner can remove it. `_approach` (low noise and a
  44 Hz sub, swelling as s^1.5, a 6-12 Hz grind modulation, a 55 % dip in the last fifth: "melts back"), `_rip`
  (a 0.26 s bright band sweeping 800 to 2800 Hz, torn at 40-70 Hz, growing into the crack), `_crack` (snap, sub
  95 to 28 Hz, a 900 Hz knock, a 220 Hz body), the peals from the first pass as the rolling waves, `_growl`
  (a 120 Hz band and 80 Hz noise breathing at 2-5 Hz under the last half). The flash belongs at `approach`
  seconds in, so the preset's `lead` is 1.6.
- numbers: the 100 ms envelope rises from -65 to -32 dB over the approach, hits -10 at the crack, then
  -20, -24 for the rolls, and fades to -75 over 8.7 s; no warnings; placed at -2 LU uncapped.
- lesson: **when a person writes a description with a sequence in it, build the sequence, one stage per act,
  and give every act a parameter.** Read the adjectives as recipes: "felt not heard" is sub plus a hint of
  160 Hz; "grinding / drumroll" is a 6-12 Hz modulation; "canvas ripping" is a bright band torn at 40-70 Hz
  growing into the hit; "rattles the panes" is a 220 Hz body on the crack; "overlapping waves" is the peals;
  "hollow growl" is a narrow 120 Hz band breathing slowly. A single envelope cannot hold a story.

### thunder, third pass · "a slow distant rumble, a sudden hit, higher rumbles, and the next thunder starts while the first rumble fades"
- the three-act build was "still not right": it had too many parts (a rip, a crack, three short peals, a growl)
  and the ear could not find the shape in it. The owner then said the shape in one sentence.
- fix: strikes instead of peals. One slow distant rumble (`approach`), then `strikes` hits; each hit is a crack
  with a long rumble rolling out of it (`_roll`: a quick rise, a slow fall rolling in 1-3 Hz waves with a 6-12 Hz
  grind, the mid band sliding down from 520 Hz, so it is louder and higher than the distant rumble); the next
  hit lands at `overlap` of the previous roll (0.6: while it is still fading), `backoff` quieter and `grow`
  longer. The growl stage and the separate peals are gone; the rip is a short tear in front of each hit.
- numbers: envelope -67 to -34 dB over the approach, -10 at the first hit, down to -33, -13 at the second hit
  at 4.4 s, then a 5 s fade to -74; no warnings; -2 LU uncapped.
- lesson: **when a fix adds parts and the owner still says no, remove parts and ask for the shape in one
  sentence.** A sound a person can describe as "A, then B, then C again while B fades" wants exactly those
  three units and nothing else; every extra stage blurs the outline they listen for. Build the simplest
  structure that has every unit they named, then let the tuner add colour.

### thunder, fourth pass · "rain and wind seem louder; thunder is very low in volume"
- the owner's rule: decide the volume of a sound from the situation and the emotion it belongs to. Thunder is
  fear, the dark, a quiet night it interrupts: it must be louder than the rain and echo through the sky.
- why it was quiet: every master is peak-normalised, so a dense loop (rain, wind) is loud all the way through
  while thunder was one crack at the peak and a rumble 20 dB under it; the level rule reads the loudest 100 ms
  (the crack), places it, and the −6 dBFS peak cap then holds the whole sound down ("capped"). The rumble, which
  is most of the sound, sat under the rain bed. The numbers said thunder was louder (−9 vs −16 LUFS); the ear
  said the opposite, because the ear sums over seconds, not 100 ms.
- fix: a preset `mood` (huge −12, big −14, normal) that masters the *body* (the loudest second, K-weighted):
  lift it to the target, let the limiter hold the crack above it, peak at −1.5 dBFS (`levels.master`, applied in
  `Preset.render`, the tuner and `sfx make`). Thunder is `huge`, carries its own `level_lu` 0 (placement now
  honours a preset's level), and its tail grew to 3.6 s at 0.4 wet. Its rumble now sits about 14 dB above the
  rain bed in a mix; the originals are `normal` and bit-identical.
- tried and rejected: a −9 LUFS body. Reaching it flattened the strike by 17 dB and the slow distant rumble
  stopped being distant; the master must lift the weight without erasing the shape the owner asked for.
- lesson: **the weight of a sound follows its situation, and the ear sums over seconds.** Decide the mood first
  (fear, violence, the sky: huge; a slam or shot: big; interface and foley: normal), master the body to it, then
  place it. Peak normalisation plus a 100 ms loudness rule will always make a bed louder than an event.
  Candidates for `huge`/`big` on the next listening passes: explosion, cannon, tank_fire, explosion_distant,
  impact_deep, shotgun, door_slam.

### thunder, fifth pass · "a little more loudness, and a louder rumble starting and fading, overlapping the thunders"
- fix: a `surge` stage, a long rumble (low noise, a 320 to 140 Hz band, a sub, rolling in 1-3 Hz waves) that
  starts halfway through the approach, swells to its peak about 0.9 s after the first hit and fades across the
  second, so the two strikes sit on one slow wave of weight instead of on silence; and `level_lu` 2 (the peak
  cap now decides the placement, about 1.7 dB louder in a mix). The first surge amount (1.0) only raised the
  floor between the hits by 8 dB and read as nothing; 1.6 makes it a wave of its own.
- lesson: **a sequence of events needs a bed of its own under it.** Separate hits on silence sound like samples
  played in a row; one slow swell that overlaps them turns them into one weather. When a person asks for
  "more" of a layer, double it before judging: a layer that only measures as a few dB is not heard as a layer.

### thunder, sixth pass · "two or three more thunders overlapping at random seeds, and 40 % more loudness"
- strikes: default 4 (max 6), overlap 0.45, grow 1.15; every strike is its own seeded variation (level ±20 %,
  length ±20 %, colour ±15 %, a place in the field), so no two hits are the same. The surge eased to 1.2 so the
  hits still stand above the bed.
- loudness, tried and rejected: a huge body of −9 LUFS (+3 dB = 40 % in amplitude). The limiter had to crush the
  strike to reach it: the whole 2-7 s region peaked at −2 to −4 dBFS continuously and the distant opening came up
  to the level of the body. The shape the owner liked was gone.
- loudness, kept: the peak cap by mood in the mix (`levels.PEAK_CAP_BY_MOOD`: huge −3 dBFS, big −4.5, normal −6).
  Thunder in a mix is now held by the −3 dBFS cap, about 3 dB (40 %) louder than before, and its file keeps the
  −12 LUFS body and its dynamics.
- lesson: **"louder" has two homes: the body of the file and the cap in the mix. Lift the body only as far as
  the limiter can go without flattening the shape; after that, the extra weight is a placement decision (how
  high a sound of this mood may peak against the voice), never more limiting.** A huge sound earns a higher cap
  because it is meant to dominate its moment.

### thunder, seventh pass · "strikes very close together, irregular gaps, two or three thunders again"
- the owner's rule: man-made sounds (gunfire) are a continuous rhythm; natural ones (thunder) are random and
  unpredictable. Four evenly overlapping strikes were "real good" but still read as a sequence.
- fix: clusters. Hits come in groups of two or three cracks 0.12-0.45 s apart (each follower rides the first
  roll with a shorter rumble of its own), then an irregular gap (0.6-1.4 x the rumble x `overlap`) before the
  next cluster. `strikes` is the total (7), `cluster` the group size at most (3; 1 gives single, evenly
  spaced hits for the man-made case). The default seed lands clusters at 2.5-3.1 s, 4.9-5.2 s and later.
- lesson: **decide timing from who made the sound.** Man-made: a steady rhythm (gunfire, machines, clocks,
  typing). Natural: clusters with irregular gaps, never even (thunder, rain, waves, fire, birds). Even spacing on
  a natural sound reads as a machine; a cluster parameter plus a seeded irregular gap is the general fix.
  Now in the skill's loop (step 1) next to the mood rule.

### thunder, eighth pass · "it still sounds like two thunders at a regular interval; each thunder needs its own rumble fading out, and a full rumble in the background"
- why the clusters did not read: the followers in a cluster had shortened rumbles and a 0.75 backoff per
  cluster, so the third and fourth clusters were 5-8 dB down and the ear counted two events; the bed faded
  early (decay 0.3 of its length) so the gaps were nearly empty.
- fix: explicit `clusters` (3) and `per_cluster` (up to 3) instead of a total count; every crack carries its
  own full rumble (0.7-1.3 x `roll`), backoff 0.9 so every cluster is loud, cluster gaps 0.4-1.8 x the rumble
  (really irregular), the bed holds (decay 0.55 of its length). Default seed: clusters at 2.5-3.4 s, 6.0-6.2 s
  and 9.5-10.2 s, each −10 to −13 dB RMS, the bed −20 to −30 dB between them.
- lesson: **a pattern the ear must count needs every member at full weight.** Backoff and shortening are
  for a tail, not for the events themselves; if later events are quieter and shorter, the listener hears one
  event with echoes. Make the count explicit in the parameters (clusters, per_cluster) so the words map
  straight onto the sliders.

### blacksmith · "sounds like a bell ringing; I want steel, with a vibration that comes out of iron and fades"
- before: each blow was `tone(1650 Hz)` with four partials decaying over 0.3 s: a tuned bell by construction
  (inharmonic ratios 1, 1.41, 2.2, 3.5 are exactly the bell family in `tone`'s docstring).
- fix: three parts and nothing in tune. The clank (a 4 ms burst 1.5-12 kHz and a 700 Hz knock for the mass of
  the blow); the anvil's ping (a tight cluster above 3 kHz, 1.00/1.02/1.37/1.71, gone in 0.09 s); the iron's
  vibration (close partial pairs at 620 Hz and its 2.01x and 3.2x, each pair `beat` Hz apart so they throb at
  24 Hz, through a tanh for buzz, fading over 0.35 s). The pitch track reads 3.5 kHz then 609 Hz: ping, then
  vibration. Blows drift ±4 % in time: a smith is steady, with a little life.
- lesson: **a ring is a bell; a vibration is a beat.** Metal that is "struck and rings in tune" is a bell or a
  chime. Metal that "vibrates" (steel, iron, a rail, a sheet) is partials beating against near neighbours,
  saturated a little, and gone fast. Keep the tuned ring above 3 kHz and under 0.1 s on tools; put the weight in
  a buzz at a few hundred Hz. Applies to hammer, rail, sword, armour, chains.

### tank_fire · "sounds like a bell; it needs to start with an explosion that echoes, with a shell piercing the air"
- before: a cannon boom plus `tone(1850 Hz)` with bell-family partials for a "breech ring": the same bell
  mistake as blacksmith, and the ring was the brightest thing in the sound, so the ear named it a bell.
- fix: three things the words named. The muzzle blast (the `_boom` helper plus a roar: pink noise band sliding
  900 to 140 Hz, torn at 14 Hz, gone in 0.4 s); discrete echoes (the blast's low half returned 3 times at
  `echo_gap`, each 7 dB quieter and darker, scattered across the field: the landscape answering, which a reverb
  alone never says); the shell (a narrow Q-14 whistle whose pitch falls from 2600 Hz to a ninth of that over
  1.3 s as it recedes, panning away, with a zip at the start). Mood huge, level +2, like thunder.
- lesson: **no tuned ring on anything that is not a bell or a chime.** Guns, cannon, tanks, anvils, doors: the
  metal they contain is a clank or a buzz, never a `tone` with bell ratios. And "echoes" means discrete
  returns with a gap, darker each time; a reverb tail is "a room", not "an echo". A receding object is a
  falling pitch plus a pan away.

### 2026-11-01 · research pass: how real thunder and rain sound (see `nature-acoustics.md`)
- method: five free thunder recordings and three free rain recordings, every one measured with
  the same script as our own renders (band shares, slope, crest, texture modulation, event envelopes).
- thunder: the weight is 80-250 Hz in every recording (−2 dB of the total) with the sub 4-15 dB under it; ours
  is sub-dominant with 80-250 ten dB down. Real crest 24-31 dB, ours 17. Real roll modulates at 0.5-4 Hz, ours
  at 4-14. Inside a strike: crack, a 12 dB dip for a quarter second, a roll back up, then a rumble 12-18 dB
  under the crack bumping irregularly for 8 s, sometimes a secondary peal 4-5 s later. Our cluster gaps came
  out 3.45/3.48/3.50 s: even by bad luck; the gap distribution must be wider and skewed.
- rain: every recording falls −7 to −19 dB per octave with its weight 250 Hz-4 kHz and a solid 80-250 Hz
  surface band; ours rises (+1.7 dB/oct), centres at 4.4 kHz, and has nothing under 1 kHz. Ours is hiss, not
  rain. The granular 16-64 Hz drop texture is right; individual ticks 15-20 dB above the bed are missing.
- lesson: **measure the real thing before trusting the words.** "Rumble" made us reach for the sub and "rain"
  for hiss; the recordings put thunder's weight at 80-250 Hz and rain's at 250 Hz-4 kHz. One analysis script
  run on free recordings and on our render, side by side, settles in minutes what listening passes take hours
  to find. Keep the script's numbers (band shares, slope, crest, texture rate, event envelope) as the standard
  comparison for any natural sound.

### 2026-11-01 · thunder and rain rebuilt to the recordings' numbers (see `nature-acoustics.md`, "after")
- thunder: a `_weight` band (pink noise centred 150 Hz, Q 0.55) replaced the 110 Hz low-passed noise as the
  body in the approach, the rolls and the surge; the sub cut to a third; the crack's body moved from 220 Hz to
  150 Hz; the roll starts 0.28 s after the crack at 0.35 of the hit and falls at exp(-1.7 s); a secondary peal
  (no crack, −15 dB) 3.8-5.2 s after each cluster; cluster gaps 0.15 + 1.6·u^2.2 of the rumble (skewed short);
  the rip only on the first, close strike; a 40 Hz high-pass at the end. Result: 80-250 Hz leads the sub by
  1 dB (was 10 dB behind), rumble 13.5 dB under the crack (was 6-10), centroid 92 → 230 Hz.
- rain_loop: rebuilt from scratch. A roar band (pink, 900 Hz, Q 0.35) plus a 420 Hz band, a `surface` band at
  `surface_hz` (160 Hz roof by default), the bed low-passed at 3.6 kHz, the air above 4 kHz 15-20 dB under, a
  16-64 Hz granular texture, and `drops` ticks per second (band-limited bursts 600-3000 Hz) placed 16-24 dB
  above the bed's RMS; `intensity` moves light to pouring. Result: centroid 4374 → 1355 Hz, slope +1.7 → −5.3
  dB/oct, >4 kHz −2.4 → −12.5 dB.
- iteration record: three passes each. The sub kept winning the thunder's band shares until it was cut in
  every helper and the crack (the mood master lifts whatever is there); the rain's air kept winning until the
  bed itself was low-passed and the ticks band-limited (broadband ticks are air).
- lesson: **set the targets from the measurements, then iterate on the numbers, not on adjectives.** Each pass
  took one run of the comparison script; three passes landed both sounds inside the recordings' ranges. When a
  band will not move, look for every helper that feeds it (the sub came from four places).

### thunder crack · "the loud clap sounds artificial, like a drum beat"
- why: `_crack` was a kick drum by construction: a sine sweeping 95 to 28 Hz with a knock and a burst on top.
  Measured at 5 ms resolution, no real crack has a tone at all (pitch strength 0.2-0.5, no downward glide),
  and none is an instant hit: all three close strikes build over 100-300 ms as a ragged, growing crackle of many
  impulses (33 in 0.4 s on the urban claps) that culminates in the peak; the first 60 ms are broadband and flat
  up to 4 kHz; the weight is 80-250 Hz throughout.
- fix: the crack is a thinned impulse train (tiny N-waves with a click, rate ramping 40 to 400 a second, level
  rising as s^1.6) into a stack of three 8-14 ms N-waves a few ms apart (the channel's segments arriving), a
  20 ms broadband snap on the peak, resonances at 170 and 450 Hz for the body, nothing above 6 kHz, no
  oscillator anywhere. The crack buffer is placed so its peak lands on the hit time; the rip rides the build.
- numbers after: 17 impulses in the 0.4 s before the peak (was 3), pitch track weak and not falling, whole-file
  slope −8.4 dB/oct (real −9 to −12.5), 80-250 Hz leads the sub by 5 dB, texture modulation now 0.5-4 Hz
  dominant like the recordings.
- lesson: **a sine sweep is a drum, wherever you put it.** Explosions, thunder, cannon and any "boom" in nature
  get their low weight from the length of their pulses and their resonances, not from an oscillator gliding
  down. And a natural crack is a build-up, not an onset: give it 100-300 ms of growing crackle before the peak.
  Measure onsets at 5 ms, with a pitch-strength check, before calling anything a "crack".

### thunder, rumble and crack again · "a group of drums; the noise behind has no rumble, only wind"
- measured what separates a rumble from wind, in the 80-250 Hz band of the rumble sections: real strikes have
  kurtosis 8-45 (scipy's excess kurtosis; Gaussian noise is 0) and envelope crests of 10-21, because a rumble
  is a pile of small shock arrivals. Ours scored 0.9 with a crest of 4: the same as our wind loop (0.7, 4.2)
  and a windy rain recording (1.2, 5.3). Filtered noise with slow swells is wind by definition, whatever band
  it sits in. The "group of drums" was three big stacked N-waves plus resonant band-passes at 170 and 450 Hz on
  the pulses: a resonator on an impulse is a drum.
- fix: `_arrivals`, a dense train of random N-wave pulses (3-14 ms, random sign, lognormal amplitudes, Poisson
  timing with a time-varying rate) replaces the noise in the approach, every roll and the bed; the pulse
  length sets the weight (no resonant filter), high-passed at 60 Hz. The crack's peak is a burst of 40-80
  arrivals inside 25 ms instead of three thuds, with a broadband snap. Reverb dried (wet 0.4 → 0.25, 3 s):
  a reverb tail is Gaussian and turns arrivals back into wind.
- the first arrivals pass measured kurtosis 3.3: too dense (500 a second overlap into a Gaussian pile) and
  the pulses too long (sub came back). Halving the rate, heavier tails (lognormal sigma 1.1), 3-11 ms pulses
  and the 60 Hz high-pass gave kurtosis 7-32 and crests 7-19, inside the recordings' range.
- lesson: **rumble is arrivals, wind is noise; measure kurtosis to tell them apart.** Any natural "rumble",
  "roar" or "roll" (thunder, avalanche, stampede, surf breaking, a distant battle) is a pile of impulsive
  events and must be synthesised as events with heavy-tailed sizes, not as filtered noise with an LFO. Keep
  the rate low enough that they do not merge (a few hundred a second at most), keep reverb under them, and
  never put a resonator on an impulse unless you want a drum.

### thunder_rolling · "the rumble is perfect, the crack is not: replace each crack with a 100 % louder, 60 % shorter rumble peaking where the crack was"
- done as a `clap` parameter on the thunder recipe (0 = crack, 1 = rumble only, blends between) and a second
  preset `thunder_rolling` (clap 1, rip 0) so the owner can A/B against `thunder`. The clap is `_roll` at 40 %
  of the roll's length and twice its level with a 40 ms rise; its peak offset is computed from the roll's shape
  and the part is placed so the peak lands on the hit time. Each hit's content now comes from its own seeded
  stream (`seed*1000 + i`), so both presets share the exact same timing and bed; only the hits differ.
- lesson: **when the owner designs the fix in numbers ("100 % louder, 60 % shorter, peak on the same time"),
  build exactly that and ship it beside the original.** Keep structure (timing) and content (what sounds at
  each time) on separate random streams, so a variant changes only what it is meant to change.

### thunder_rolling · "perfect, but I can only hear it with my ear at the laptop speaker or on headphones"
- measured what a laptop speaker gets (the render through a 4th-order 250 Hz high-pass, K-weighted loudest
  second): thunder_rolling lost 6.6 dB and sat 5 dB under the wind loop, while a whoosh or a ping lost nothing.
  The file was already at full scale: its weight is at 80-250 Hz and a laptop plays little of that.
- fix: `levels.presence(x, amount)`, a preset field `presence` (0-1) applied in the master before the mood
  lift: soft saturation of the band under 250 Hz driven from the band's RMS (driving from its peak did nothing:
  with a 20 dB crest the band sits far below its peak most of the time), 200-1200 Hz kept, mixed at the band's
  own RMS, never peakier than the band; and the low band's peaks tamed by up to 8 dB with the look-ahead
  limiter, because they set the file's ceiling yet the speaker cannot play them, so the normaliser can lift
  everything it does play. Thunder and thunder_rolling ship with presence 0.6; the tuner has a presence slider
  under the post controls and saves it with the preset.
- numbers: laptop body −18.8 → about −16 LUFS (within 2 dB of the wind loop); full-band body unchanged at −12;
  the 80-250 Hz band loses impulsiveness (kurtosis 11 → 2-3) but the 200-1200 Hz harmonics carry the arrivals'
  shape (kurtosis 17) for headphones. The honest limit: a sound whose weight is under 250 Hz can only ever be
  a few dB louder on a laptop; the rest is physics.
- lesson: **"louder on a laptop" is not gain, it is where the energy sits.** Check every sub-heavy sound through
  a 250 Hz high-pass before shipping; if it loses more than 3 dB, add presence. And when a master is
  peak-normalised, peaks the target speaker cannot reproduce are pure waste: tame them per band.

### thunder, final · "the one we had previously was better, make that thunder"
- `thunder` is now the rolling version (clap 1, clap_gain 6, surge 0.5, rip 0) without presence; the separate
  `thunder_rolling` preset is retired and its synonyms point at `thunder`. The presence stage stays in the
  tuner for anyone who needs laptop playback.
- lesson: **ship the version the owner chose, and only that one.** A variant kept "for A/B" becomes a duplicate
  the moment the owner decides; retire it and move its synonyms.

### rain_drops · "the rain loop's foreground water is good, but the rain drops are not right"
- measured five free drop recordings (drops into water, big drops, drops on wet leaves, from a roof, on ground
  and leaves): every drop is a 6-12 ms tick with an instant attack, centred 1.5-2.8 kHz; drops into water add
  a ring whose pitch rises (21 of 25 drops, e.g. 3200 → 3400 → 6900 → 8000 Hz over 50 ms: the plink, the
  trapped bubble shrinking); drops on leaves or ground are broadband clicks with almost no tone and more
  500 Hz-2 kHz. Ours was an 82 ms tonal blob with a 50 ms attack whose pitch fell: the opposite on every count.
- fix: `_raindrop`: a 2.5 ms broadband impact (600 Hz-8 kHz), a 3 ms thump at 600-1800 Hz for a big drop, and
  for a `water` share of the drops a ring loud for 10 ms then quietly on for 30-60 ms while its pitch rises
  (`chirp`, 0.5 = half an octave). Drops at irregular times, lognormal sizes, spread across the field, a small
  room. Result: 11 ms to −20 dB, instant attack, 2-5 kHz dominant with 500 Hz-2 kHz 25 dB under, like the
  water-drop recording; `water` 0 gives the leaves/ground kind.
- tried and backed off: a doubling chirp with a louder tail (centroid 4.5 kHz, too bright); half an octave and
  a tail at 6 % landed near the recordings.
- lesson: **a drop is a tick, and a plink rises.** Any "drip", "drop" or "plink" is an instant broadband impact
  of a few milliseconds; the tonal part, when there is one, is short and rises in pitch, never falls. A falling
  glide is a cartoon. Measure onset length and pitch direction on real drops before building any of them.
- approved by ear (owner, 2026-11-01): rain_drops as rebuilt; thunder as the rolling version; rain_loop, blacksmith
  and tank_fire from the earlier passes. The listening pass continues sound by sound.

### hum_loop · "I can't hear anything"
- numbers: a 55 Hz sine with six harmonics up to 440 Hz, centroid 69 Hz, nothing above 1 kHz. Through a 250 Hz
  high-pass (a laptop speaker) it lost 16.6 dB, against 0.4 dB for the air loop; and as an ambience bed it is
  placed 16 LU under the voice, so on a laptop there was nothing left at all. The same failure as the first
  heartbeat and the first thunder: the weight under 150 Hz, invisible to the level rule.
- fix: a machine hum built the way a real one is heard: 24 partials of f0 weighted by a formant around 450 Hz
  (where a transformer's rasp sits and what a small speaker plays), odd partials a little stronger (mains),
  soft saturation for the rasp (mean removed: an asymmetric waveform through tanh leaves DC, and DC in a loop
  is a thump at the seam), and a breathing fan bed of filtered noise around 1 kHz, loop-seamed from a buffer
  0.15 s longer than the loop (loop_seam drops the crossfade's length). Result: centroid 69 → 496 Hz, laptop
  loss 16.6 → 0.5 dB, no warnings; still a seamless loop (every partial completes whole cycles).
- lesson: **a bed that sits 16 LU under the voice must put its energy where every speaker plays it.** Beds are
  the sounds most at risk from the small-speaker trap because they are placed quietest; run every loop through
  the 250 Hz high-pass check (`levels.body_lufs` of the filtered render) and keep the loss under 3 dB. For a
  hum that means a formant in the mids, not a sine at the fundamental.
- approved by ear (owner, 2026-11-01): hum_loop as rebuilt.

### the worst eight on a laptop · impact_deep, impact_soft, explosion_distant, punch, land, cannon, stamp, shotgun
- the 250 Hz high-pass check over the whole library: 30 of 99 sounds lose more than 3 dB on a small speaker,
  these eight 14-29 dB (the two impacts are silent on a laptop). All are low thuds whose whole weight sits
  under 250 Hz.
- fix: `presence` 0.6 on the eight presets, no recipe change (the owner's rule: the details stay the same).
  Measured: impact_deep −29.3 → −4.8 dB, impact_soft −27.6 → −4.0, explosion_distant −20.6 → −5.7, punch
  −20.5 → −3.9, land −18.7 → −3.7, cannon −18.1 → −4.1, stamp −16.5 → −4.3, shotgun −13.9 → −3.6. Presence
  0.9 gained nothing more (the low-band taming is capped), so 0.6 is the setting. The two impacts are reference
  sounds: their determinism hashes and reference OGGs were regenerated, with the change named in the commit.
- lesson: **presence is the first tool for a sub-heavy sound, the recipe the second.** It is generic, keeps the
  character, and brings a 15-30 dB laptop loss to about 4 dB in one step; only a sound that must be louder
  still on small speakers earns a mid-range body in its recipe. Run the whole-library check after any new batch
  of low sounds, not one sound at a time.
