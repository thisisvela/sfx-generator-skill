/* The sound matrix: a field of hairline ticks behind every page.
   Three depth layers drift with the pointer (parallax), a slow breathing noise field moves through them, a playhead
   sweeps across like a scrubbing cursor, and when a sound plays the field becomes a live spectrum analyser: each
   column rises with its frequency band. Cheap (one canvas, ~2k line segments), faint (ink at a few percent), and
   still under prefers-reduced-motion. */
(() => {
  const canvas = document.getElementById('bg');
  if (!canvas) return;
  const ctx = canvas.getContext('2d', { alpha: true });
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const quiet = document.body.classList.contains('quiet-bg');       // docs pages: fainter
  const LAYERS = [
    { gap: 16, row: 44, alpha: 0.11, depth: 1.0, scale: 1.0 },
    { gap: 22, row: 60, alpha: 0.07, depth: 0.55, scale: 1.6 },
    { gap: 30, row: 84, alpha: 0.045, depth: 0.25, scale: 2.4 },
  ];
  let W = 0, H = 0, dpr = 1, ink = '10,10,10', accent = '10,10,10';
  let px = 0, py = 0, tx = 0, ty = 0;           // pointer parallax, smoothed
  let spectrum = null, level = 0;
  const t0 = performance.now();

  function readInk() {
    const v = getComputedStyle(document.documentElement).getPropertyValue('--ink').trim();
    const m = v.match(/^#([0-9a-f]{6})$/i);
    if (m) ink = [1, 3, 5].map(i => parseInt(m[1].slice(i - 1, i + 1), 16)).join(',');
    const av = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
    const am = av.match(/^#([0-9a-f]{6})$/i);
    accent = am ? [1, 3, 5].map(i => parseInt(am[1].slice(i - 1, i + 1), 16)).join(',') : ink;
  }
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    readInk();
  }
  // a smooth, cheap value field: sums of sines, no allocations
  function field(x, y, t, s) {
    return 0.5 + 0.5 * Math.sin(x * 0.009 / s + t * 0.45 + Math.sin(y * 0.011 / s + t * 0.21) * 1.7)
                     * Math.cos(y * 0.007 / s - t * 0.17 + Math.sin(x * 0.005 / s + t * 0.13) * 1.1);
  }
  function readAudio() {
    const an = window.sfxAnalyser;
    if (!an) { level *= 0.92; return; }
    if (!spectrum || spectrum.length !== an.frequencyBinCount) spectrum = new Uint8Array(an.frequencyBinCount);
    an.getByteFrequencyData(spectrum);
    let sum = 0;
    for (let i = 0; i < spectrum.length; i++) sum += spectrum[i];
    const now = sum / spectrum.length / 255;
    level = Math.max(now, level * 0.9);           // fast attack, slow release
  }
  function bandAt(u) {                           // u in 0..1 across the screen -> log-spaced bin energy
    if (!spectrum || level < 0.004) return 0;
    const n = spectrum.length;
    const i = Math.min(n - 1, Math.floor(Math.pow(u, 2.2) * n * 0.6));
    const a = spectrum[i] / 255, b = spectrum[Math.min(n - 1, i + 1)] / 255;
    return Math.max(a, b);
  }
  function draw(now) {
    const t = reduce ? 0 : (now - t0) / 1000;
    px += (tx - px) * 0.06; py += (ty - py) * 0.06;
    ctx.clearRect(0, 0, W, H);
    readAudio();
    const head = reduce ? -1 : ((t / 16) % 1) * (W + 160) - 80;         // the playhead's x
    const dim = quiet ? 0.55 : 1;
    for (const L of LAYERS) {
      ctx.strokeStyle = `rgba(${ink},${(L.alpha * dim).toFixed(3)})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      const ox = px * 28 * L.depth, oy = py * 18 * L.depth;
      const phase = (t * 6 * L.depth) % L.gap;                              // a slow drift to the left
      for (let x = -L.gap + phase - ox % L.gap; x < W + L.gap; x += L.gap) {
        const u = x / W;
        const band = bandAt(u) * level * 46 * L.depth;
        const near = head < 0 ? 0 : Math.exp(-((x - head) * (x - head)) / (2 * 90 * 90)) * 7;
        for (let y = (L.row - oy % L.row) * 0.5; y < H + L.row; y += L.row) {
          const f = field(x + ox, y + oy, t, L.scale);
          const h = 1.5 + f * f * 9 * L.depth + near + band * (0.4 + 0.6 * f);
          ctx.moveTo(x + 0.5, y - h);
          ctx.lineTo(x + 0.5, y + h);
        }
      }
      ctx.stroke();
    }
    if (head >= 0) {                                                        // the playhead itself
      ctx.strokeStyle = `rgba(${accent},${(0.16 * dim).toFixed(3)})`;
      ctx.beginPath(); ctx.moveTo(head + 0.5, 0); ctx.lineTo(head + 0.5, H); ctx.stroke();
    }
    if (level > 0.004) {                                                    // a soft bloom while sound plays
      const g = ctx.createRadialGradient(W * 0.5, H * 0.35, 0, W * 0.5, H * 0.35, Math.max(W, H) * 0.5);
      g.addColorStop(0, `rgba(${accent},${(0.07 * level * dim).toFixed(3)})`);
      g.addColorStop(1, `rgba(${accent},0)`);
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
  }
  let raf = 0, running = false;
  function loop(now) { draw(now); raf = requestAnimationFrame(loop); }
  function start() { if (reduce || running) return; running = true; raf = requestAnimationFrame(loop); }
  function stop() { running = false; cancelAnimationFrame(raf); }
  window.addEventListener('resize', () => { resize(); if (reduce) draw(performance.now()); });
  window.addEventListener('pointermove', e => { tx = (e.clientX / W - 0.5) * 2; ty = (e.clientY / H - 0.5) * 2; }, { passive: true });
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', readInk);
  resize();
  if (reduce) draw(performance.now()); else start();
})();
