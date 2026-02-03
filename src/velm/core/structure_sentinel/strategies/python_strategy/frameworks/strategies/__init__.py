# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/strategies/__init__.py
# ----------------------------------------------------------------------------------------------------------------------------------

from .fastapi import FastAPIStrategy
from .flask import FlaskStrategy
from .typer import TyperStrategy
from .django import DjangoStrategy

ALL_STRATEGIES = [
    FastAPIStrategy,
    FlaskStrategy,
    TyperStrategy,
    DjangoStrategy
]