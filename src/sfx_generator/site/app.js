/* sfx-generator site: Web Audio playback at in-video level, 'over narration', filters, search, card details. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const LIB = window.SFX_LIBRARY || null;      // {base, sounds:{id:{...}}, voice:{file, cue}}
  let ctx = null, limiter = null;
  const buffers = {};
  let voiceBuf = null;
  let playing = [];
  const dB = g => Math.pow(10, g / 20);

  function audio() {
    if (ctx) return ctx;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -3; limiter.knee.value = 0; limiter.ratio.value = 20;
    limiter.attack.value = 0.002; limiter.release.value = 0.08;
    limiter.connect(ctx.destination);
    const analyser = ctx.createAnalyser();              // the background listens here
    analyser.fftSize = 512; analyser.smoothingTimeConstant = 0.7;
    limiter.connect(analyser);
    window.sfxAnalyser = analyser;
    return ctx;
  }
  async function load(url) {
    if (buffers[url]) return buffers[url];
    const res = await fetch(url);
    const data = await res.arrayBuffer();
    buffers[url] = await audio().decodeAudioData(data);
    return buffers[url];
  }
  const inVideo = () => { const e = $('#invideo'); return e ? e.checked : false; };
  const overVoice = () => { const e = $('#overvoice'); return e ? e.checked : false; };

  function stopAll() {
    playing.forEach(s => { try { s.stop(); } catch (e) {} });
    playing = [];
    $$('.playing').forEach(el => el.classList.remove('playing'));
  }

  async function play(id, el, when) {
    const s = LIB.sounds[id];
    await audio().resume();
    const b = await load(LIB.base + s.mp3);
    const src = ctx.createBufferSource();
    src.buffer = b; src.loop = !!s.loop;
    const g = ctx.createGain();
    g.gain.value = (inVideo() || overVoice()) ? dB(s.gain_db) : 1;
    src.connect(g); g.connect(limiter);
    const t0 = when ?? ctx.currentTime + 0.02;
    let end = t0 + b.duration;
    if (overVoice() && LIB.voice && !s.loop) {
      const v = await load(LIB.base + LIB.voice.file);
      const vs = ctx.createBufferSource(); vs.buffer = v; vs.connect(limiter);
      vs.start(t0); playing.push(vs);
      src.start(t0 + Math.max(0, LIB.voice.cue - s.lead));
      end = t0 + v.duration;
    } else {
      src.start(t0);
    }
    playing.push(src);
    if (el) {
      el.classList.add('playing');
      src.onended = () => el.classList.remove('playing');
      if (s.loop) setTimeout(() => { try { src.stop(); } catch (e) {} el.classList.remove('playing'); }, (b.duration * 2) * 1000);
    }
    return end;
  }

  // play buttons
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('[data-play]');
    if (!b) return;
    e.preventDefault(); e.stopPropagation();
    const card = b.closest('.card, .chip, .row');
    if (card && card.classList.contains('playing')) { stopAll(); return; }
    stopAll();
    play(b.dataset.play, card || b).catch(err => toast('could not play: ' + err.message));
  });

  // play all in a section
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('[data-play-all]');
    if (!b) return;
    e.preventDefault();
    stopAll();
    const sec = b.closest('.section');
    const cards = $$('.card', sec).filter(c => c.style.display !== 'none' && !LIB.sounds[c.dataset.id].loop);
    await audio().resume();
    let t = ctx.currentTime + 0.05;
    for (const c of cards) {
      const end = await play(c.dataset.id, c, t);
      t = end + 0.5;
    }
  });

  // card details
  document.addEventListener('click', (e) => {
    const m = e.target.closest('[data-more]');
    if (!m) return;
    e.preventDefault();
    const card = m.closest('.card');
    const open = card.classList.toggle('open');
    m.textContent = open ? 'Less' : 'Details';
    if (open) {
      const img = $('img[data-src]', card);
      if (img) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });

  // copy
  document.addEventListener('click', async (e) => {
    const c = e.target.closest('[data-copy]');
    if (!c) return;
    e.preventDefault();
    const text = c.dataset.copy || c.closest('.code, .cmd, .install')?.querySelector('span, pre')?.textContent || '';
    try { await navigator.clipboard.writeText(text.trim()); toast('Copied'); } catch (err) { toast('Copy failed'); }
  });

  // filters and search
  const pills = $$('.filters .pill[data-filter]');
  const search = $('#search');
  function applyFilters() {
    const f = (pills.find(p => p.classList.contains('on')) || {}).dataset?.filter || 'all';
    const q = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    $$('.section[data-family]').forEach(sec => {
      let n = 0;
      $$('.card', sec).forEach(card => {
        const s = LIB.sounds[card.dataset.id];
        const okF = f === 'all' || s.family === f || s.category === f;
        const hay = (card.dataset.search || '').toLowerCase();
        const okQ = !q || q.split(/\s+/).every(w => hay.includes(w));
        const ok = okF && okQ;
        card.style.display = ok ? '' : 'none';
        if (ok) n++;
      });
      sec.style.display = n ? '' : 'none';
      const cnt = $('h2 small', sec);
      if (cnt) cnt.textContent = `${n} of ${sec.dataset.total}`;
      shown += n;
    });
    const empty = $('#empty');
    if (empty) empty.style.display = shown ? 'none' : '';
    const u = new URL(location.href);
    if (f === 'all') u.searchParams.delete('f'); else u.searchParams.set('f', f);
    if (q) u.searchParams.set('q', q); else u.searchParams.delete('q');
    history.replaceState(null, '', u);
  }
  pills.forEach(p => p.addEventListener('click', () => { pills.forEach(x => x.classList.remove('on')); p.classList.add('on'); applyFilters(); }));
  if (search) search.addEventListener('input', applyFilters);
  if (pills.length) {
    const u = new URL(location.href);
    const f = u.searchParams.get('f'), q = u.searchParams.get('q');
    if (f) { const p = pills.find(x => x.dataset.filter === f); if (p) { pills.forEach(x => x.classList.remove('on')); p.classList.add('on'); } }
    if (q && search) search.value = q;
    applyFilters();
    if (location.hash) {
      const card = $(location.hash);
      if (card && card.classList.contains('card')) { $('[data-more]', card)?.click(); }
    }
  }

  // subnav highlighting
  const links = $$('.side .sections a[href^="#"]');
  if (links.length && 'IntersectionObserver' in window) {
    const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => { if (en.isIntersecting) { links.forEach(a => a.classList.remove('on')); map.get(en.target.id)?.classList.add('on'); } });
    }, { rootMargin: '-120px 0px -70% 0px' });
    map.forEach((a, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }

  // side nav
  const menu = $('#menu'), scrim = $('#scrim');
  const html = document.documentElement;
  function syncMenu() { if (menu) menu.setAttribute('aria-expanded', html.classList.contains('nav-open') ? 'true' : 'false'); }
  function setNav(open, remember = true) {
    html.classList.toggle('nav-open', open);
    if (remember) { try { localStorage.setItem('sfx-nav', open ? 'open' : 'closed'); } catch (e) {} }
    syncMenu();
  }
  if (menu) menu.addEventListener('click', () => setNav(!html.classList.contains('nav-open')));
  if (scrim) scrim.addEventListener('click', () => setNav(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && html.classList.contains('nav-open') && window.innerWidth < 1024) setNav(false); });
  $$('.side .sections a').forEach(a => a.addEventListener('click', () => { if (window.innerWidth < 1024) setNav(false); }));
  syncMenu();

  // close an open download menu when clicking elsewhere
  document.addEventListener('click', (e) => {
    $$('.dl-menu[open]').forEach(d => { if (!d.contains(e.target)) d.removeAttribute('open'); });
  });

  // toast
  let tt = null;
  function toast(msg) {
    let t = $('.toast');
    if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(tt); tt = setTimeout(() => t.classList.remove('show'), 1400);
  }
  window.sfxToast = toast;

  // theme: the browser's preference unless the person chose; the button flips between light and dark and remembers
  const themeBtn = $('#theme');
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    const next = dark ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('sfx-theme', next); } catch (e) {}
  });
})();
