"""skills/ (Claude Code) and .agents/skills/ (Codex) must be identical copies, and every skill must be well-formed."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mirror_in_sync():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "sync_skills.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_skills_have_frontmatter_and_ledgers():
    for skill in (ROOT / "skills").iterdir():
        md = (skill / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\nname: (\S+)\ndescription: (.+?)\n---\n", md, re.S)
        assert m, f"{skill.name}: SKILL.md needs name and description frontmatter"
        assert m.group(1) == skill.name
        assert (skill / "references" / "lessons.md").exists(), f"{skill.name}: no lessons ledger"
        assert "lessons.md" in md, f"{skill.name}: SKILL.md must tell the agent to read and append the ledger"
        assert (skill / "agents" / "openai.yaml").exists()


def test_install_guide_names_the_repo_and_commands():
    text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    for needle in ("uv tool install", "pipx install", "claude plugin install", ".agents/skills", "sfx --version"):
        assert needle in text, needle
