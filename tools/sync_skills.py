"""Mirror skills/ into .agents/skills/ so Codex finds the skills in a clone of this repository.

  python tools/sync_skills.py          # copy
  python tools/sync_skills.py --check  # exit 1 if the mirror differs (used by the tests)

skills/ is the source of truth. Claude Code reads it through .claude-plugin/plugin.json; Codex reads
.agents/skills/ by native discovery.
"""
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "skills"
DST = ROOT / ".agents" / "skills"


def differs(a: Path, b: Path) -> list[str]:
    out = []
    if not b.exists():
        return [f"missing {b}"]
    cmp = filecmp.dircmp(a, b, ignore=["__pycache__"])
    for n in cmp.left_only:
        out.append(f"only in source: {a / n}")
    for n in cmp.right_only:
        out.append(f"only in mirror: {b / n}")
    for n in cmp.diff_files:
        out.append(f"differs: {a / n}")
    for sub in cmp.subdirs:
        out += differs(a / sub, b / sub)
    return out


def main():
    if "--check" in sys.argv:
        d = differs(SRC, DST)
        if d:
            print("\n".join(d))
            print("run: python tools/sync_skills.py")
            sys.exit(1)
        print("skills mirror in sync")
        return
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
    print(f"copied {SRC} -> {DST}")


if __name__ == "__main__":
    main()
