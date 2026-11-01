# How thunder and rain really sound: measurements to synthesise against

Written 2026-11-01 from measurements of free recordings (used for analysis only, in a scratch folder, never copied
into this repository; only their numbers are here) and from what is generally known about the acoustics of
thunder and rain. Every figure below was measured with the same script on the recordings and on our own renders,
so the comparison is fair: band shares are dB of the total 20 Hz to 20 kHz energy, the slope is a straight-line
fit of the spectrum in dB per octave from 100 Hz to 8 kHz, the crest factor is peak over RMS, and "texture
modulation" is where the energy of the envelope of everything above 2 kHz sits. The recordings are named in
the tables by what they contain.

## Thunder

### What is known
- A thunder event is a sequence, not a boom: close lightning is heard first as a click or cloth-tearing noise,
  then a cannon shot or sharp crack, then continuous rumbling. Claps are loud sounds lasting 0.2 to 2 s with
  higher pitch; peals change in loudness and pitch; rolls are irregular mixtures; rumbles are quieter, lower and
  last up to more than 30 s. Later return strokes carry more acoustic energy than the first. Sound travels about
  3 s per kilometre, so the flash leads the sound.
- Spectra: claps and peals peak around 100 Hz, rumbles around 50 Hz; a 90-flash study found the most common
  peak band 175-200 Hz with a mean of 227 Hz; broadband measurements peak between 20 and 130 Hz with no sharp
  line. Infrasound below 10 Hz exists but is inaudible. The audible fundamental is below 250 Hz.
- Sound designers' consensus: a short, even peal is the most common reason synthetic thunder sounds fake; real
  thunder varies as it rolls and takes several seconds to die; the crack is the distance cue (none at all on a
  distant strike); the crack competes with speech, the rumble sits under it.

### What the recordings measure (five recordings, close to distant)
| recording | centroid | slope | sub <80 | 80-250 | 250-1k | 1k-4k | >4k | crest |
|---|---|---|---|---|---|---|---|---|
| close dry crack, 15 s | 192 Hz | −9.1 dB/oct | −6.2 | **−2.2** | −8.4 | −17.6 | −31.6 | 24.5 dB |
| close strike ~1.6 km, 13 s | 273 Hz | −12.4 | −10.7 | **−2.4** | −5.1 | −14.8 | −38.5 | 31.2 dB |
| two big claps, urban, 95 s | 156 Hz | −12.5 | −6.5 | **−1.9** | −8.9 | −23.2 | −44.5 | 29.6 dB |
| various big/medium/distant, 150 s | 112 Hz | −7.5 | −3.4 | **−3.4** | −10.9 | −24.7 | −32.5 | 28.0 dB |
| distant thunder under rain, 17 s | 273 Hz | −7.2 | −17.2 | **−1.8** | −5.2 | −19.1 | −25.4 | 24.9 dB |
| **ours (thunder preset)** | 92 Hz | −6.5 | **−0.7** | −10.2 | −12.8 | −22.7 | −29.2 | **17.2 dB** |

- **The weight of thunder is 80-250 Hz, not the sub.** In every recording the 80-250 Hz band carries most of the
  energy (−2 dB of the total) and the sub under 80 Hz is 4 to 15 dB below it. Ours is the other way round: the
  sub dominates and 80-250 is 10 dB down. That is also why ours is "felt" on good speakers and vanishes on small
  ones, while real thunder is heard everywhere.
- **Real thunder is far more dynamic.** Crest factors 24-31 dB; ours 17 dB after the mood master.
- **The spectrum falls faster.** −9 to −12.5 dB per octave on close strikes (−7 on distant ones); ours −6.5.
  Above 4 kHz a real strike is 30-45 dB down; the hiss we add for "canvas ripping" must stay short.
- **The roll modulates slowly.** The texture of a real strike moves at 0.5-4 Hz (dominant by 6 dB over 4-16 and
  16-64 Hz). Ours is flat across all three: our 4-14 Hz tearing and 9 Hz grind are too fast. Only the very
  close strike with its hiss is flat like ours.

### Inside one strike (50 ms RMS from the crack, close dry crack recording)
```
crack  -15 -13   dip -27   roll -20 -18   -25 -33 -28 -31 -33 -32 -29 -35 -37   peal -26 -33 -31 -26 -17 -21   -38 ...
```
- The crack lasts about 0.3 s, then the level drops 12-14 dB for a quarter second, then a roll comes back
  within 5 dB of the crack for half a second, then the rumble settles 12-18 dB under the crack and keeps
  bumping irregularly by ±5-8 dB for 8 s or more, with a secondary peal 4-5 s later on the close strike. The
  1.6 km strike has the same shape without the peal and decays about 3 dB per second after the roll.
- Band shares barely change from crack to rumble: 80-250 Hz carries the weight throughout; only the air above
  4 kHz leaves (−29 → −43 dB). Thunder does not get "darker" by losing mids; it loses the hiss.
- Ours: crack −10, then a flat −16 to −20 for ten seconds (the rumble only 6-10 dB under the crack, sub
  dominant, no dip after the crack, no secondary peal), and the cluster gaps came out 3.45, 3.48, 3.50 s:
  nearly even by bad luck of the seed. Cluster gaps need a wider and skewed distribution.

### What was changed in the thunder recipe (applied 2026-11-01)
1. Move the weight up: the rumble and rolls band-passed 80-250 Hz (peak ~120-180 Hz) with the sub 6-10 dB
   under it, not a 110 Hz low-pass with the sub on top.
2. The rumble 12-18 dB under the crack, not 6-10; keep the mood master's lift but let the body it lifts be the
   80-250 Hz roll, not the sub.
3. Slow the modulation: the rolling waves at 0.5-3 Hz carry the movement; the 9 Hz grind only as a light texture.
4. After the crack, a 0.25 s dip of 12 dB, then the roll back up, then the rumble: the "shockwave collapsing".
5. Cluster gaps from a skewed distribution (e.g. 0.3-3.5 s, most short) so no two gaps match; a secondary peal
   4-5 s after a close strike at −15 dB.
6. The rip (hiss) only on the close strike and under 0.3 s; nothing above 4 kHz after that.

## Rain

### What is known
- Rain is not pink noise: its spectrum depends on how hard it falls and what it lands on. Heavier rain adds
  more high frequencies (a rooftop study: no rain, nothing above 2.5 kHz; 5 mm/h added 2.5-5 kHz; 58 mm/h added
  a lot above 5 kHz). Published airborne band findings: 600-1200 Hz as the most prominent rain band in one
  study, 4.4-5.6 kHz in another, 6-8 kHz most prominent in a third: the surface decides.
- Each drop is an impact plus, on water, a bubble ring (small drops 13-25 kHz underwater; large drops down to
  1 kHz); in air the impact on the surface is what we hear, and the surface's resonance (roof, leaves, window,
  concrete) colours it. Spectrograms of rain show vertical lines: individual drops are audible as ticks across
  the whole spectrum, over the hiss.
- Synthesis practice: a filtered-noise bed shaped like the recording plus a separate layer of individual drops
  with their own attack and decay, one intensity parameter moving light to pouring, resonant filters for the
  surface. Rain on leaves is softer and muted; on concrete or metal sharper.

### What the recordings measure (three recordings)
| recording | centroid | slope | sub <80 | 80-250 | 250-1k | 1k-4k | >4k | crest | texture 0.5-4 / 4-16 / 16-64 Hz |
|---|---|---|---|---|---|---|---|---|---|
| rain on open ground, 10 s | 1236 Hz | −18.6 dB/oct | −15.9 | −10.6 | **−3.8** | **−3.6** | −15.0 | 23.8 dB | −10.2 / −7.7 / **−3.6** |
| rain against a window with wind, 82 s | 344 Hz | −6.9 | −2.7 | −7.1 | −8.0 | −9.8 | −21.7 | 21.1 dB | −3.0 / −8.8 / −5.8 |
| heavy rain on a skylight, 151 s | 672 Hz | −7.7 | −14.0 | **−4.1** | **−4.8** | −6.4 | −20.7 | 24.2 dB | −4.5 / −6.4 / −4.8 |
| **ours rain_loop** | **4374 Hz** | **+1.7** | −40.4 | −30.9 | −18.9 | −3.9 | **−2.4** | 23.2 dB | −13.0 / −7.4 / −2.9 |
| **ours rain_drops** | 1957 Hz | −0.3 | −63.0 | −57.6 | −7.3 | −1.0 | −17.5 | 16.7 dB | −5.0 / −3.7 / −6.3 |

- **Our rain is a rising hiss; real rain is a falling roar with ticks.** Every recording's spectrum falls
  (−7 to −19 dB per octave) with its weight between 250 Hz and 4 kHz and a solid 80-250 Hz band (−4 to −11 dB);
  above 4 kHz is 15-22 dB down. Ours rises, centres at 4.4 kHz, and has nothing under 1 kHz (−19 to −40 dB).
  That is why ours reads as "hiss" or "static" instead of rain.
- **The surface shows in the low band.** Rain on a skylight carries 80-250 Hz at −4 dB (the pane resonating);
  rain at a window with wind carries sub energy from the wind; plain rain on ground has its floor at 250 Hz.
- **The texture is granular at 16-64 Hz** in every recording (the drops), as ours is: keep that.
- **Crest factor 21-24 dB** in real rain: individual drops stick out of the bed by 20 dB. Ours matches on the
  loop; the drops preset is a different thing (a few plinks).

### What was changed in the rain loop (applied 2026-11-01)
1. rain_loop: a falling bed. Pink noise through a 250 Hz to 4 kHz shelf (peak around 600-1200 Hz), a surface
   band at 80-250 Hz with its own amount (roof, window, ground), and the hiss above 4 kHz 15-20 dB under the mids
   instead of on top. Target: centroid 600-1200 Hz, slope −7 to −10 dB per octave.
2. Keep the granular 16-64 Hz drop texture and add audible individual drops as short broadband ticks 15-20 dB
   above the bed, randomly timed (the vertical lines in a real spectrogram), with a `drops` density parameter.
3. One `intensity` parameter from light (little above 2.5 kHz, sparse ticks) to pouring (more above 5 kHz,
   dense ticks, more 80-250 Hz roar), matching the rooftop measurements.
4. A `surface` choice (ground, roof/skylight, window, leaves) that sets the 80-250 Hz amount and the top band.

### After the change (same script)
| sound | centroid | slope | sub <80 | 80-250 | 250-1k | 1k-4k | >4k | crest |
|---|---|---|---|---|---|---|---|---|
| thunder, before | 92 Hz | −6.5 | −0.7 | −10.2 | −12.8 | −22.7 | −29.2 | 17.2 dB |
| thunder, after | 230 Hz | −6.5 | −4.7 | **−3.6** | −6.9 | −17.7 | −23.5 | 18.4 dB |
| rain_loop, before | 4374 Hz | +1.7 | −40.4 | −30.9 | −18.9 | −3.9 | −2.4 | 23.2 dB |
| rain_loop, after | 1355 Hz | −5.3 | −15.6 | −8.2 | **−4.3** | **−4.0** | −12.5 | 20.1 dB |

Thunder's weight moved to 80-250 Hz with the sub under it; inside a strike the rumble now runs 13-16 dB under the
crack and falls about 1.5 dB per second, the roll rises after a quarter-second dip, a secondary peal lands 4-5 s
after each cluster, cluster gaps come from a skewed distribution, the whole thing is high-passed at 40 Hz. The
crest stays near 18 dB because the mood master lifts the body on purpose. Rain's spectrum now falls, its weight
sits between 250 Hz and 4 kHz with a roof band at 160 Hz, the air is 12 dB under the mids, and drop ticks stand
16-24 dB above the bed; it lands between the plain-rain and the skylight recordings, and `intensity`, `surface`
and `hiss` move it either way.

## The comparison scripts
`python -I tools/analyse_recordings.py . <recording.wav> <preset_id> ...` prints the same numbers for any file
and any preset: seconds, crest, centroid, slope, band shares, texture modulation and the event list. Run it on a
free recording and on our render side by side before and after a change to a natural sound. The two companions
are `tools/rumble_texture.py` (kurtosis and envelope crest of the 80-250 Hz band: rumble or wind) and
`tools/drops_analysis.py` (onset length, attack and pitch direction of individual drops), and
`tools/laptop_check.py` reports what a small speaker is left with. Recordings used for such a comparison stay
outside the repository, are never shipped, and are not named in it; only the numbers are kept.

## Rumble is arrivals, not noise (added after the owner heard "wind" behind the strikes)
Measured in the 80-250 Hz band of the rumble sections (3-8 s after the loudest crack), with scipy's excess
kurtosis (Gaussian noise = 0) and the Hilbert envelope's crest (peak over mean):

| sound | kurtosis 80-250 | env. crest | kurtosis 250-1k | env. crest |
|---|---|---|---|---|
| close dry crack | 16.2 | 12.7 | 10.4 | 12.4 |
| close strike ~1.6 km | 23.5 | 16.6 | 12.4 | 13.2 |
| two big claps, urban | 8.0 | 9.8 | 11.5 | 12.0 |
| various, a big one at 28 s | 45.1 | 20.8 | 21.5 | 15.9 |
| our wind loop | 0.7 | 4.2 | 0.8 | 4.2 |
| rain at a window with wind (recording) | 1.2 | 5.3 | 3.9 | 10.2 |
| **ours, before** (filtered noise) | **0.9** | **4.1** | 0.9 | 4.6 |
| ours, after (arrivals), roll 0.5-2.4 s | 16.7 | 11.6 | 32.0 | 18.6 |
| ours, after, rumble 5.5-10.5 s | 7.0 | 7.0 | 9.9 | 10.8 |

A real rumble is impulsive: a pile of small shock arrivals of random size. Filtered noise with slow swells,
whatever its band, measures like wind, and the ear hears wind. The synthesis is therefore a Poisson train of
short N-wave pulses with lognormal amplitudes (`_arrivals` in nature.py), the pulse length setting the weight,
no resonant filter (a resonator on an impulse is a drum) and little reverb (a reverb tail is Gaussian). The
crack's peak is a 25 ms burst of such arrivals, not a stack of thuds. The script `tools/rumble_texture.py` is the check: kurtosis under 3 in the weight band means wind.

## Rain drops (added for the rain_drops pass)
Five free recordings (drops into water, big rain drops, drops on wet forest leaves, drops from a roof, drops
on ground and leaves), loudest 25 drops each, measured with `tools/drops_analysis.py`:

| recording | length to −20 dB | attack | centroid | dominant bands | tonal strength | pitch moves |
|---|---|---|---|---|---|---|
| drops into water | 12 ms | instant | 2789 Hz | 2-5 kHz (−1.8), 500-2k −22 | 0.9 | up 21 of 25 |
| big rain drops | long (wet surface) | instant | 1473 Hz | 500-2k (−2.2), <500 −7 | 0.6 | flat |
| drops on wet leaves | 8 ms | instant | 1508 Hz | flat 500 Hz-10 kHz | 0.8 | up 12, flat 10 |
| drops from a roof | 10 ms | instant | 2247 Hz | flat 500 Hz-10 kHz | 0.8 | up 15, flat 9 |
| drops on ground and leaves | 6 ms | instant | 2580 Hz | 500 Hz-5 kHz | 0.4 | mostly none |
| **ours, before** | **82 ms** | **52 ms** | 2661 Hz | 2-5 kHz only | 0.9 | **down** |
| ours, after | 11 ms | instant | ~4 kHz | 2-5 kHz, 500-2k −26 | 0.9 | rises by design |

A drop is a tick of a few milliseconds. Into water it adds a ring that rises in pitch, up to doubling over
50 ms (the bubble shrinking); on leaves, ground or a roof it is a broadband click with a little 500 Hz-2 kHz
thump and almost no tone. Nothing about a drop falls in pitch.
