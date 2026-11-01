"""`sfx tune <preset|recipe>`: a localhost server and a page whose sliders come from the recipe's schema.

On every change the page POSTs the parameters; the server renders with the same Python code as the CLI (one source
of truth), measures the result, and returns 16-bit WAV audio (base64) with the numbers, a waveform and a spectrogram.
Nothing is written to disk until 'Save preset' or 'Export' is pressed.

Endpoints (JSON in, JSON out):
  GET  /                 the page
  GET  /state            recipe schema, the preset's params, the original render, the narration clip if any
  POST /render           {params, post:{width, lr_offset_ms, gain_db}} -> {wav_b64, report, waveform_svg, spec_png_b64}
  POST /save             {id, params, category, use, lead, ...} -> writes <cwd>/<id>.json (or `path`, inside <cwd>)
  POST /export           {id, params, post, formats} -> writes <cwd>/<id>.{wav,ogg,mp3}

The server listens on 127.0.0.1 only, and it answers a POST only when the Host header names this server and the
request carries a JSON content type (a page on another site cannot send that without a CORS preflight, which is
never granted), so no other web page open in the browser can make it write files. Ids are slugs; a save path
must stay inside the save folder.
"""
from __future__ import annotations

import base64
import io
import json
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
import soundfile as sf

from .. import inspect as insp
from .. import levels, presets, render, schema
from ..blocks import SR, norm

PAGE = Path(__file__).with_name("page.html")


def post_process(x: np.ndarray, post: dict | None) -> np.ndarray:
    """Stereo width (mid/side), a left/right offset in ms, and gain. Applied after the recipe, before measuring."""
    post = post or {}
    width = float(post.get("width", 1.0))
    off = float(post.get("lr_offset_ms", 0.0))
    gain = float(post.get("gain_db", 0.0))
    if width != 1.0:
        mid = (x[:, 0] + x[:, 1]) / 2
        side = (x[:, 0] - x[:, 1]) / 2 * width
        x = np.stack([mid + side, mid - side], axis=1)
    if off:
        n = int(abs(off) * SR / 1000)
        if n:
            y = np.zeros((len(x) + n, 2))
            if off > 0:
                y[: len(x), 0] = x[:, 0]
                y[n:, 1] = x[:, 1]
            else:
                y[n:, 0] = x[:, 0]
                y[: len(x), 1] = x[:, 1]
            x = y
    if width != 1.0 or off:
        x = norm(x)
    if gain:
        x = x * 10 ** (gain / 20)
    return x


def wav16_b64(x: np.ndarray) -> str:
    buf = io.BytesIO()
    sf.write(buf, np.clip(x, -1, 1).astype(np.float32), SR, format="WAV", subtype="PCM_16")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class State:
    def __init__(self, what: str):
        try:
            self.preset = presets.find(what)
            self.recipe = schema.get(self.preset.recipe)
        except KeyError:
            self.recipe = schema.get(what)
            self.preset = presets.Preset(id=what, recipe=what, params=self.recipe.defaults(), what=self.recipe.doc)
        self.original = levels.master(self.recipe.render(self.preset.params), self.preset.mood,
                                      presence_amount=self.preset.presence)
        self.voice = None
        clip = Path(__file__).resolve().parents[1] / "site" / "narration.mp3"
        if clip.exists():
            self.voice = {"b64": base64.b64encode(clip.read_bytes()).decode("ascii"), "cue": 3.3}

    def render_payload(self, params: dict, post: dict | None, with_pictures=True) -> dict:
        pres = float((post or {}).get("presence", self.preset.presence))
        x = post_process(levels.master(self.recipe.render(self.recipe.validate(params, strict=False)),
                                       self.preset.mood, presence_amount=pres), post)
        rep = insp.report(x, self.preset.category)
        out = {"wav_b64": wav16_b64(x), "report": rep, "seconds": len(x) / SR}
        if with_pictures:
            spec = _spec_png_bytes(x)
            out["spec_png_b64"] = base64.b64encode(spec).decode("ascii")
            out["waveform_svg"] = insp.waveform_svg(x, 900, 72, 300)
        return out


def _spec_png_bytes(x: np.ndarray) -> bytes:
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = insp.spectrogram_png(x, Path(d) / "s.png", width=600, height=180)
        return p.read_bytes()


ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}")


def safe_id(value) -> str:
    """A preset id that is a file name and nothing more (no separators, no leading dot)."""
    s = str(value or "").strip()
    if not ID_RE.fullmatch(s) or ".." in s:
        raise ValueError(f"id {s!r} must be letters, digits, _ . - (no path separators)")
    return s


def inside(path: Path, folder: Path) -> Path:
    """`path` resolved, refused unless it is inside `folder`."""
    p = Path(path).resolve()
    folder = folder.resolve()
    if folder != p and folder not in p.parents:
        raise ValueError(f"path {path!s} is outside the save folder {folder}")
    return p


def make_handler(state: State, save_dir: Path, port: int):
    local_hosts = {f"127.0.0.1:{port}", f"localhost:{port}", f"[::1]:{port}"}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj, code=200):
            data = json.dumps(obj).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/":
                body = PAGE.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif self.path == "/state":
                pl = levels.placement(state.original, state.preset.category, level_lu=state.preset.level_lu,
                                      mood=state.preset.mood)
                self._json({"schema": state.recipe.schema(), "preset": state.preset.to_dict(),
                            "category_lu": levels.CATEGORY_LU, "original": state.render_payload(state.preset.params, None),
                            "placement": pl, "voice": state.voice})
            else:
                self._json({"error": "not found"}, 404)

        def _local(self) -> bool:
            """True for the page this server served; a request from any other site fails one of these."""
            host = (self.headers.get("Host") or "").lower()
            origin = self.headers.get("Origin")
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if host not in local_hosts or ctype != "application/json":
                return False
            return origin is None or origin.lower() in {f"http://{h}" for h in local_hosts}

        def do_POST(self):
            if not self._local():
                self._json({"error": "only the tuning page may call this server"}, 403)
                return
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n) or b"{}")
            try:
                if self.path == "/render":
                    self._json(state.render_payload(req.get("params", {}), req.get("post"), req.get("pictures", True)))
                elif self.path == "/save":
                    pr = presets.Preset.from_dict({**state.preset.to_dict(), **req,
                                                   "id": safe_id(req.get("id", state.preset.id)),
                                                   "params": state.recipe.validate(req.get("params", {}), strict=False)})
                    path = inside(req.get("path") or save_dir / f"{pr.id}.json", save_dir)
                    pr.validate().save(path)
                    self._json({"saved": str(path)})
                elif self.path == "/export":
                    params = state.recipe.validate(req.get("params", {}), strict=False)
                    pres = float((req.get("post") or {}).get("presence", state.preset.presence))
                    x = post_process(levels.master(state.recipe.render(params), state.preset.mood,
                                                   presence_amount=pres), req.get("post"))
                    stem = save_dir / safe_id(req.get("id", state.preset.id))
                    files = render.export(x, stem, tuple(req.get("formats", ["wav", "ogg", "mp3"])))
                    self._json({"exported": {k: str(v) for k, v in files.items()}})
                else:
                    self._json({"error": "not found"}, 404)
            except Exception as e:   # the page shows the message
                self._json({"error": str(e)}, 400)
    return H


def serve(what: str, port: int = 8765, open_browser: bool = True, save_dir: Path | None = None):
    state = State(what)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(state, save_dir or Path.cwd(), port))
    url = f"http://127.0.0.1:{port}/"
    print(f"tuning {state.preset.id} ({state.recipe.id}) at {url}  (Ctrl-C to stop)")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
