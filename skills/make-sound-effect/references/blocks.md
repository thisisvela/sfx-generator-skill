# Building blocks and how the families use them

Code: `src/sfx_generator/blocks.py`. Masters are 48 kHz, stereo, float arrays shaped (n, 2), in about −1..1,
peak-normalised to −1.5 dBFS at the end of every recipe (`norm`). Loudness in a mix is set later from
measurements; never bake a mix level into a file.

## Blocks

| block | what it does | notes |
|---|---|---|
| `white(n, rng)`, `pink(n, rng)` | noise, peak-normalised; pink is a 4-pole IIR with 2,000 warm-up samples dropped | pink sounds smoother; whooshes mix 0.7 pink with some white "air" |
| `svf_bandpass(x, fc, q)` | TPT state-variable band-pass, unity gain at fc; **fc and q can be arrays** | the heart of every whoosh; run twice in series for a clearer moving band |
| `lowpass`, `highpass(x, fc, order)` | Butterworth SOS filters | LP 9-11 kHz takes the fizz off noise; HP 120 Hz kills DC |
| `logsweep(points, n)` | a frequency curve through (position 0-1, Hz) points, log-interpolated | any glide |
| `pan(mono, p)` | equal-power pan, −1..1, scalar or array | a right-to-left pan sells "something flew past" |
| `reverb(st, seconds, wet, seed, damp)` | convolution with a synthetic impulse (two channels of white noise, −60 dB at `seconds`, low-passed at `damp`, 12 ms fade-in, energy-normalised) | no room recordings; `room()` (0.35 s, wet 0.06-0.15) glues interface sounds |
| `fade`, `norm`, `trim_tail` | edge fades, peak normalise, cut the silent tail (−62 dB) and fade the last 20 ms | |
| `env(t, attack, tau)` | linear attack then exponential decay (tau = time to 37 %) | decay ≈ 2.3·tau to −20 dB |
| `glide(f0, f1, t, tc)` | exponential approach from f0 to f1 | pops are a sine whose pitch glides |
| `osc(freq, t)` | a sine at constant or time-varying frequency via a cumulative-sum phase | **always integrate frequency into phase**; never sin(2πf(t)t) for a moving f |
| `tone(f0, t, spec)` | a sum of partials `[(ratio, amp, tau), ...]` with a release over the last quarter (max 80 ms) | inharmonic ratios make bells and glass: bell (1, 2.0, 2.76, 5.4), glass (1, 2.32, 4.25), marimba (1, 3.93, 9.2) |
| `place(parts, d)` | mixes (start, signal) parts into one stereo buffer with a 12 ms safety release each | two-note chimes, click-clacks, stutters |
| `release(x, r)` | a cosine fade over the last r seconds | **a cut while still ringing is a click**; every note needs one |
| `burst(d, rng, lo, hi, tau)` | a short, optionally band-limited noise transient | clicks, knocks, strikes |
| `ks_pluck(f0, d, seed, damp, bright)` | Karplus-Strong plucked string with fractional delay | **remove the excitation's mean and high-pass the output**, or DC circulates as a rumble and the pitch reads 0 Hz |
| `finish(st)` | LP 15 kHz, then trim or fade, then normalise | the standard last step for interface sounds |
| `mix`, `saw`, `square`, `loop_seam` | sum stereo parts; band-limited saw and square; crossfade a tail into a head for loops | newer helpers |

Two time helpers: `_t(d)` = `int(SR*d)` samples, `_tr(d)` = `int(round(SR*d))`. They differ for some lengths;
keep the one each recipe uses.

## How the families are built

- **Whoosh**: 0.7 pink + air white → two band-pass stages whose centre follows `logsweep((0,f0),(peak,f1),(1,f2))`
  and whose Q follows `q` → a low body band at 0.18×fc → envelope sin² rising to `peak`, cos^1.6 falling → pan →
  LP 9.5 kHz. The five whooshes differ only in parameters; lead 0.1-0.54 s puts the loudest moment just after the
  cue.
- **Swoosh up, riser** (end on the cue): a 260→4,200 Hz sweep at Q 1.4 plus a quiet 220→660 Hz sine, envelope
  s^2.2; the riser adds three detuned tones (×1.0, ×1.007, ×0.994) gliding 110→440 Hz with 2nd and 3rd harmonics,
  envelope s^2.6, a different noise in each ear.
- **Swell** (reverse cymbal): a 0.35 s high-passed white burst through reverb (wet 0.9), cut to the length and
  played backwards, LP 8.5 kHz.
- **Impact**: a sine falling f0→f1 (exponential, tc 70 ms) decaying with `tau` (the boom) + a low-passed 22 ms
  noise knock (the hit) + a band of pink at 190 Hz (the body) + a reverb tail. `impact_deep` is 80→34 Hz, longer.
- **Shimmer**: `count` short sine pings at seeded log-uniform pitches, seeded starts within `spread`, decays
  0.18-0.55 s, pans −0.8..0.8, through a 1.4 s reverb at 35 %. `title_hit` = deep impact + 0.32 shimmer.
- **Glitch**: short bursts of square + a sine at 2.01×, quantised (bit-crush), gaps, falling amplitude,
  band-passed with some dry signal. `glitch_burst` 0.38 s is audible under speech; `glitch` 75 ms is not.
- **Chimes**: bell partials (1, 2.0, 2.76, 5.4) at 65-120 ms steps in a 0.4-0.5 s room; `end_chime` uses
  (1, 2.01, 3.02, 4.17) with longer decays in a 1.6 s reverb. Mismatched partials are what make a bell, not an
  organ.
- **Pops**: a sine whose pitch glides as it decays (600→900 Hz, tc 30 ms, tau 28 ms) plus a soft noise click;
  `pop_low` adds a 140→90 Hz thump; `pop_up` glides 480→1,550 Hz.
- **Ticks**: a 2 ms high-passed noise snap, a 3.4 kHz ring (6 ms) and a little body at f/3 (the body is what keeps
  a tick audible without hitting the cap). **Clicks**: a band-passed noise press at 3 kHz with a 140 Hz thump, then
  a quieter release 30 ms later.
- **Pings**: glass partials; **bong**: a 233 Hz marimba bar plus a mallet knock. **Toggle**: two odd-harmonic blips
  a fourth apart. **Switch**: click-clack with metallic rings.
- **Question**: E5 then A5 bending up 6 %; `question_alt` slides up a fifth. **Error**: two square-ish tones
  stepping down a tritone, LP 2.6 kHz. **Camera swells**: a tone + fifth + octave gliding 1,078↔1,640 Hz with a
  breath of band-passed pink.
- **Newer families**: notify/alarm/countdown/fail (tonal signals), keystroke/typing/camera_shutter/unlock (click
  cores with bodies and rings), page_turn/stamp/heartbeat/tick_tock (noise bands, thumps, woods), coin/level_up/zap
  (square notes, arpeggio + shimmer, filtered saw sweep), data_blips/scan/sonar (blips, tremolo sweep, ping in a
  dark reverb), bubble/drop (fast glides, a plink), hum_loop/air_loop (partials with whole cycles per loop; a
  crossfaded noise seam).
