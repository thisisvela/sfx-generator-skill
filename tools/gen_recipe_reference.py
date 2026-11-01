"""Regenerate skills/make-sound-effect/references/recipes.md from the recipe schemas and the presets.

  python tools/gen_recipe_reference.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sfx_generator import presets, schema  # noqa: E402

OUT = ROOT / "skills" / "make-sound-effect" / "references" / "recipes.md"


def main():
    recs = schema.all_recipes()
    lib = presets.load_all()
    by_recipe = {}
    for p in lib.values():
        by_recipe.setdefault(p.recipe, []).append(p)
    families = {}
    for r in recs.values():
        families.setdefault(r.family, []).append(r)
    lines = ["# Recipes and parameters", "",
             "Generated from the schemas by `python tools/gen_recipe_reference.py`; do not edit by hand.",
             "Every parameter has a default, a range, a step, a unit and a meaning. `sfx schema <recipe>` prints the same.",
             "", "## Presets by use", "", "| id | family | category | lead | LU | use |", "|---|---|---|---|---|---|"]
    for p in lib.values():
        lines.append(f"| `{p.id}` | {p.family} | {p.category} | {p.lead} | {p.level_lu:+d} | {p.use} |")
    lines += ["", "## Families", ""]
    for fam, rs in families.items():
        lines.append(f"### {fam}")
        lines.append("")
        for r in rs:
            ps = ", ".join(f"`{p.id}`" for p in by_recipe.get(r.id, []))
            lines.append(f"#### `{r.id}`" + (f" (presets: {ps})" if ps else ""))
            lines.append("")
            lines.append(r.doc)
            if r.tips:
                lines.append("")
                lines.append(f"*Tips:* {r.tips}")
            lines.append("")
            lines.append("| parameter | default | range | unit | meaning |")
            lines.append("|---|---|---|---|---|")
            for p in r.params:
                rng = f"{p.min}..{p.max} step {p.step}" if p.kind in ("float", "int") else p.kind
                lines.append(f"| `{p.name}` | {p.default} | {rng} | {p.unit} | {p.doc} |")
            lines.append("")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(recs)} recipes, {len(lib)} presets)")


if __name__ == "__main__":
    main()
