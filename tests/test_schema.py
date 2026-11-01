"""Schema: every parameter has a kind, a default inside its range, a step and a meaning; defaults reproduce the
preset; the preset's params are exactly the recipe's params; unknown or out-of-range values are rejected."""
import numpy as np
import pytest

from sfx_generator import presets, schema

RECIPES = schema.all_recipes()
ALL = presets.load_all()


@pytest.mark.parametrize("rid", sorted(RECIPES))
def test_params_declared(rid):
    rec = RECIPES[rid]
    assert rec.doc and rec.family
    names = {p.name for p in rec.params}
    assert "seed" in names, "every recipe has a seed"
    for p in rec.params:
        assert p.doc, f"{rid}.{p.name} has no meaning"
        if p.kind in ("float", "int"):
            assert p.min is not None and p.max is not None and p.step, f"{rid}.{p.name} needs min, max, step"
            assert p.min <= p.default <= p.max, f"{rid}.{p.name} default outside its range"
    # the function accepts exactly these names
    import inspect as pyinspect
    sig = pyinspect.signature(rec.fn)
    assert set(sig.parameters) == names, f"{rid}: function parameters differ from the schema"


@pytest.mark.parametrize("rid", sorted(RECIPES))
def test_defaults_render(rid):
    x = RECIPES[rid].render()
    assert x.ndim == 2 and len(x) > 100 and not np.isnan(x).any()


@pytest.mark.parametrize("sid", sorted(ALL))
def test_preset_matches_schema(sid):
    pr = ALL[sid]
    rec = RECIPES[pr.recipe]
    assert set(pr.params) == set(rec.by_name), f"{sid}: preset params differ from recipe params"
    rec.validate(pr.params)
    pr.validate()
    assert pr.use and pr.what, f"{sid}: needs a use and a what"


def test_rejects_unknown_and_out_of_range():
    rec = RECIPES["pop"]
    with pytest.raises(ValueError):
        rec.validate({"nope": 1})
    with pytest.raises(ValueError):
        rec.validate({"f0": 1e9})


def test_cli_command_only_lists_changes():
    assert presets.cli_command(ALL["pop"]) == "sfx render pop -o pop"
    assert "d=0.45" in presets.cli_command(ALL["whoosh_short"])


def test_schema_dict_round_trips():
    for rid, rec in RECIPES.items():
        s = rec.schema()
        assert s["id"] == rid and len(s["params"]) == len(rec.params)
