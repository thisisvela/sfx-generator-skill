"""A self-contained audition page: every variant side by side, played at its in-video gain through a limiter,
with an 'over narration' mode, play-all, A-then-B, a redo flag and a note per row, and a copy-notes button.

Audio is embedded as base64 MP3 (or WAV when no MP3 was rendered) and decoded with Web Audio after a click."""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

from . import inspect as insp
from . import levels

CSS = """
:root{--ink:#0a0a0a;--mute:#6b6b6b;--line:#0000000f;--bg:#fff;--card:0 0 0 1px #0000000f,0 1px 2px -1px #0000000f,0 2px 4px 0 #0000000a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
main{max-width:980px;margin:0 auto;padding:40px clamp(18px,5vw,28px) 80px}
h1{font-size:28px;font-weight:500;letter-spacing:-.6px;margin:0 0 6px}h1 em{font-family:Georgia,serif;font-style:italic;font-weight:400}
.sub{color:var(--mute);margin:0 0 28px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 20px}
button{font:inherit;font-size:13px;padding:7px 12px;border-radius:8px;border:1px solid #0000001a;background:#fff;color:var(--ink);cursor:pointer}
button.primary{background:var(--ink);color:#fff;border-color:var(--ink)}button:disabled{opacity:.4;cursor:default}
label.sw{display:inline-flex;gap:6px;align-items:center;font-size:13px;color:var(--mute)}
.row{display:grid;grid-template-columns:44px 1fr;gap:14px;padding:16px 0;border-top:1px solid var(--line)}
.row:last-of-type{border-bottom:1px solid var(--line)}
.row h3{margin:0 0 2px;font-size:15px;font-weight:500}.row .note{color:var(--mute);font-size:13px;margin:0 0 8px}
.wave{display:block;width:100%;height:56px;color:var(--ink)}
.nums{font:12px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--mute);margin:6px 0 0;display:flex;flex-wrap:wrap;gap:4px 18px}
.warn{color:#b3261e;font-size:12px}
.play{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;padding:0}
.tools{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}
.tools input[type=text]{font:inherit;font-size:13px;padding:6px 8px;border:1px solid #0000001a;border-radius:6px;flex:1;min-width:160px}
.tools label{font-size:13px;color:var(--mute);display:inline-flex;gap:5px;align-items:center}
textarea{width:100%;min-height:90px;font:12px/1.5 ui-monospace,Menlo,Consolas,monospace;border:1px solid #0000001a;border-radius:8px;padding:8px;margin-top:10px}
small.hint{color:var(--mute);display:block;margin-top:24px}
@media(max-width:600px){.row{grid-template-columns:40px 1fr}}
"""

JS = """
const ctx = new (window.AudioContext||window.webkitAudioContext)();
const limiter = ctx.createDynamicsCompressor();
limiter.threshold.value=-3; limiter.knee.value=0; limiter.ratio.value=20; limiter.attack.value=0.002; limiter.release.value=0.08;
limiter.connect(ctx.destination);
const buffers = {};
async function decode(b64){const bin=atob(b64);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return await ctx.decodeAudioData(u.buffer);}
async function buf(id){ if(!buffers[id]) buffers[id]=await decode(DATA.sounds[id].b64); return buffers[id]; }
let voiceBuf=null;
async function voice(){ if(!voiceBuf && DATA.voice) voiceBuf=await decode(DATA.voice.b64); return voiceBuf; }
const dB=g=>Math.pow(10,g/20);
function inVideo(){return document.getElementById('invideo').checked}
function overVoice(){return document.getElementById('overvoice').checked}
async function play(id, when){
  await ctx.resume();
  const s=DATA.sounds[id]; const b=await buf(id);
  const src=ctx.createBufferSource(); src.buffer=b;
  const g=ctx.createGain(); g.gain.value = inVideo()||overVoice() ? dB(s.gain_db) : 1;
  src.connect(g); g.connect(limiter);
  const t0 = when ?? ctx.currentTime;
  if(overVoice() && DATA.voice){
    const v=await voice(); const vs=ctx.createBufferSource(); vs.buffer=v;
    const vg=ctx.createGain(); vg.gain.value=dB(DATA.voice.gain_db); vs.connect(vg); vg.connect(limiter);
    vs.start(t0);
    src.start(t0 + Math.max(0, DATA.voice.cue - s.lead));
    return t0 + v.duration;
  }
  src.start(t0);
  return t0 + b.duration;
}
async function playAll(){ let t=ctx.currentTime+0.05; for(const id of DATA.order){ t = await play(id, t) + 0.6; } }
async function playAB(a,b){ let t=await play(a); await play(b, t+0.5); }
function notes(){
  const out=[]; for(const id of DATA.order){ const r=document.querySelector(`[data-row="${id}"]`);
    const redo=r.querySelector('.redo').checked, note=r.querySelector('.note-in').value.trim(), pick=r.querySelector('.pick').checked;
    if(redo||note||pick) out.push(`${id}: ${pick?'CHOSEN ':''}${redo?'REDO ':''}${note}`); }
  const ta=document.getElementById('notes'); ta.value=out.join('\\n')||'(no notes)';
  navigator.clipboard && navigator.clipboard.writeText(ta.value).catch(()=>{});
}
document.querySelectorAll('[data-play]').forEach(b=>b.addEventListener('click',()=>play(b.dataset.play)));
document.querySelectorAll('[data-ab]').forEach(b=>b.addEventListener('click',()=>{const [a,c]=b.dataset.ab.split(','); playAB(a,c);}));
document.getElementById('all').addEventListener('click',playAll);
document.getElementById('copy').addEventListener('click',notes);
"""


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build_page(title: str, subtitle: str, rows: list[dict], voice: dict | None = None) -> str:
    """rows: [{id, title, note, x (array), gain_db, lead, report, files}]. voice: {b64, gain_db, cue} or None."""
    data = {"order": [r["id"] for r in rows], "sounds": {}, "voice": voice}
    body = []
    for i, r in enumerate(rows):
        data["sounds"][r["id"]] = {"b64": r["b64"], "gain_db": r["gain_db"], "lead": r["lead"]}
        rep = r.get("report", {})
        nums = " ".join(f"<span>{html.escape(k)} {html.escape(str(v))}</span>" for k, v in rep.items()
                        if k in ("seconds", "loudness_max_lufs", "peak_dbfs", "video_in_mix_lu", "video_capped",
                                 "decay_to_-20dB_s", "centroid_hz", "pitch_track_hz"))
        warn = "".join(f'<div class="warn">{html.escape(w)}</div>' for w in rep.get("warnings", []))
        ab = (f'<button data-ab="{html.escape(rows[0]["id"])},{html.escape(r["id"])}">A then this</button>' if i else "")
        body.append(f"""
<div class="row" data-row="{html.escape(r['id'])}">
  <button class="play" data-play="{html.escape(r['id'])}" aria-label="play {html.escape(r['id'])}">&#9654;</button>
  <div>
    <h3>{html.escape(r['title'])}</h3>
    <p class="note">{html.escape(r['note'])}</p>
    {insp.waveform_svg(r['x'], 900, 56, 300).replace('<svg ', '<svg class="wave" ')}
    <div class="nums">{nums}</div>{warn}
    <div class="tools">{ab}<label><input type="radio" name="pick" class="pick"> choose</label>
      <label><input type="checkbox" class="redo"> redo</label>
      <input type="text" class="note-in" placeholder="note for this one"></div>
  </div>
</div>""")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>
<h1>{title}</h1><p class="sub">{html.escape(subtitle)}</p>
<div class="bar"><button class="primary" id="all">Play all</button>
<label class="sw"><input type="checkbox" id="invideo" checked> at in-video level</label>
<label class="sw"><input type="checkbox" id="overvoice"{'' if voice else ' disabled'}> over narration</label>
<button id="copy">Copy notes</button></div>
{''.join(body)}
<textarea id="notes" readonly placeholder="Your notes appear here when you press Copy notes"></textarea>
<small class="hint">Audio starts after a click. In-video level places each sound against a -14 LUFS narration with the
-6 dBFS peak cap; a limiter sits on the output. No model can hear: these numbers and pictures are a guide, your ears
decide.</small>
</main><script>const DATA={json.dumps(data)};{JS}</script></body></html>"""


def write_audition_page(run, path: Path, voice_wav: Path | None = None, cue: float = 3.3) -> Path:
    rows = []
    for v in run.variants:
        pl = levels.placement(v.x, run.category)
        f = v.files.get("mp3") or v.files.get("wav")
        rows.append({"id": f"{run.base.id}_{v.name}", "title": f"{v.name.upper()}  {run.base.recipe}", "note": v.note,
                     "x": v.x, "gain_db": pl["gain_db"], "lead": run.base.lead, "report": v.report,
                     "b64": _b64(run.out / f)})
    voice = None
    if voice_wav and Path(voice_wav).exists():
        voice = {"b64": _b64(Path(voice_wav)), "gain_db": 0.0, "cue": cue}
    page = build_page(f"<em>{html.escape(run.description)}</em>",
                      f"{len(rows)} variants from the {run.base.id} preset ({run.base.recipe}), category {run.category}",
                      rows, voice)
    path.write_text(page, encoding="utf-8")
    return path
