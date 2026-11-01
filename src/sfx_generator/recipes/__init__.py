"""All recipe families. Importing this package registers every recipe in `sfx_generator.schema.REGISTRY`.

One module per family. Each recipe declares its parameters (name, kind, default, min, max, step, unit, meaning)
and its defaults reproduce the canonical preset. Add a family here when you add a module.
"""
from . import (  # noqa: F401
    whoosh, anticipation, impact, shimmer, glitch, chime, pops, ticks, clicks, pings, ui, question, error, camera,
    notify, keys, foley, game, signal, water, ambience, nature, combat, world,
)
