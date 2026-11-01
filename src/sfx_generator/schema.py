"""Recipes and their parameter schemas.

A recipe is a function of keyword parameters that returns a (n, 2) float array at 48 kHz. Each parameter is
declared once, with its type, default, range, step, unit and meaning; the CLI, the tuning page, the skill and the
tests all read that declaration. `defaults()` reproduce the recipe's canonical sound.

    @recipe("pop", family="pops", doc="A round bubble pop", params=[
        P("f0", 600, 100, 3000, 1, "Hz", "pitch at the start"),
        SEED(101)])
    def pop(*, f0, seed): ...
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np


@dataclass(frozen=True)
class Param:
    name: str
    default: Any
    min: float | None = None
    max: float | None = None
    step: float | None = None
    unit: str = ""
    doc: str = ""
    kind: str = "float"          # float | int | seed | bool | choice
    choices: tuple = ()

    def coerce(self, v):
        if self.kind == "bool":
            return bool(v)
        if self.kind in ("int", "seed"):
            return int(round(float(v)))
        if self.kind == "choice":
            if v not in self.choices:
                raise ValueError(f"{self.name}: {v!r} is not one of {self.choices}")
            return v
        return float(v)

    def check(self, v):
        v = self.coerce(v)
        if self.kind in ("float", "int"):
            if self.min is not None and v < self.min:
                raise ValueError(f"{self.name}={v} is below its minimum {self.min}")
            if self.max is not None and v > self.max:
                raise ValueError(f"{self.name}={v} is above its maximum {self.max}")
        return v

    def as_dict(self):
        d = {"name": self.name, "kind": self.kind, "default": self.default, "unit": self.unit, "doc": self.doc}
        if self.kind in ("float", "int"):
            d.update(min=self.min, max=self.max, step=self.step)
        if self.kind == "choice":
            d["choices"] = list(self.choices)
        return d


def P(name, default, min=None, max=None, step=None, unit="", doc="", kind="float"):
    """A float parameter (or an int with kind='int')."""
    return Param(name, default, min, max, step, unit, doc, kind)


def I(name, default, min=None, max=None, unit="", doc=""):
    return Param(name, default, min, max, 1, unit, doc, "int")


def SEED(default, doc="the noise seed: change it for a sibling of the same sound"):
    return Param("seed", default, 0, 2 ** 31 - 1, 1, "", doc, "seed")


def B(name, default, doc=""):
    return Param(name, default, None, None, None, "", doc, "bool")


def C(name, default, choices, doc=""):
    return Param(name, default, None, None, None, "", doc, "choice", tuple(choices))


@dataclass
class Recipe:
    id: str
    fn: Callable[..., np.ndarray]
    params: list[Param]
    family: str
    doc: str
    tips: str = ""                       # what the parameters do to the sound, for the skill and the page
    by_name: dict = field(default_factory=dict)

    def __post_init__(self):
        self.by_name = {p.name: p for p in self.params}

    def defaults(self) -> dict:
        return {p.name: p.default for p in self.params}

    def validate(self, params: dict | None = None, strict=True) -> dict:
        """Fill defaults, coerce types, check ranges. Unknown names raise."""
        out = self.defaults()
        for k, v in (params or {}).items():
            if k not in self.by_name:
                raise ValueError(f"recipe {self.id} has no parameter {k!r}; it has {sorted(self.by_name)}")
            out[k] = self.by_name[k].check(v) if strict else self.by_name[k].coerce(v)
        return out

    def render(self, params: dict | None = None) -> np.ndarray:
        x = self.fn(**self.validate(params))
        x = np.asarray(x, dtype=float)
        if x.ndim == 1:
            x = np.stack([x, x], axis=1) / np.sqrt(2)
        return x

    def schema(self) -> dict:
        return {"id": self.id, "family": self.family, "doc": self.doc, "tips": self.tips,
                "params": [p.as_dict() for p in self.params]}


REGISTRY: dict[str, Recipe] = {}


def recipe(id: str, *, family: str, doc: str, params: list[Param], tips: str = ""):
    """Register a recipe function. The function must accept exactly the declared parameters as keywords."""
    def deco(fn):
        names = [p.name for p in params]
        if len(set(names)) != len(names):
            raise ValueError(f"recipe {id}: duplicate parameter names")
        REGISTRY[id] = Recipe(id, fn, list(params), family, doc, tips)
        return fn
    return deco


def get(id: str) -> Recipe:
    import sfx_generator.recipes  # noqa: F401  (registers everything)
    if id not in REGISTRY:
        raise KeyError(f"no recipe {id!r}; recipes: {sorted(REGISTRY)}")
    return REGISTRY[id]


def all_recipes() -> dict[str, Recipe]:
    import sfx_generator.recipes  # noqa: F401
    return dict(REGISTRY)
