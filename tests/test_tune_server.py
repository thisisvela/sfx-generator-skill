"""The tuning server only takes orders from its own page, and writes only inside its save folder."""
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from sfx_generator.tune import server


@pytest.fixture(scope="module")
def tuner(tmp_path_factory):
    save_dir = tmp_path_factory.mktemp("tune")
    state = server.State("ping")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.make_handler(state, save_dir, 0))
    port = httpd.server_address[1]
    # the handler was built for port 0; rebuild it for the real port
    httpd.RequestHandlerClass = server.make_handler(state, save_dir, port)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{port}", save_dir
    httpd.shutdown()


def post(url, body, headers=None):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_state_and_render(tuner):
    base, _ = tuner
    with urllib.request.urlopen(base + "/state", timeout=10) as r:
        st = json.loads(r.read())
    assert st["preset"]["id"] == "ping" and st["schema"]["id"] == "ping"
    code, out = post(base + "/render", {"params": st["preset"]["params"], "pictures": False})
    assert code == 200 and out["seconds"] > 0.1 and "wav_b64" in out


def test_save_inside_folder_only(tuner):
    base, save_dir = tuner
    code, out = post(base + "/save", {"id": "ping_test", "params": {}})
    assert code == 200 and (save_dir / "ping_test.json").exists(), out
    code, out = post(base + "/save", {"id": "ping_test", "params": {}, "path": str(save_dir.parent / "escaped.json")})
    assert code == 400 and "outside" in out["error"]
    assert not (save_dir.parent / "escaped.json").exists()
    code, out = post(base + "/export", {"id": "../escaped", "params": {}, "formats": ["wav"]})
    assert code == 400 and "id" in out["error"]
    assert not (save_dir.parent / "escaped.wav").exists()


def test_other_origins_are_refused(tuner):
    base, _ = tuner
    code, out = post(base + "/save", {"id": "x", "params": {}}, headers={"Origin": "https://evil.example"})
    assert code == 403
    code, out = post(base + "/save", {"id": "x", "params": {}}, headers={"Host": "evil.example"})
    assert code == 403
    req = urllib.request.Request(base + "/save", data=b'{"id":"x","params":{}}', method="POST",
                                 headers={"Content-Type": "text/plain"})     # what a cross-site fetch can send
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(req, timeout=10)
    assert e.value.code == 403
