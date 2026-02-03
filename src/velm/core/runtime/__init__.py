# Path: scaffold/core/runtime/__init__.py
# ---------------------------------------

"""
=================================================================================
== THE RUNTIME SANCTUM (V-Ω-MODULAR-GENESIS)                                   ==
=================================================================================
This package is the heart of the execution model. It exposes the `ScaffoldEngine`
facade, while hiding the complexity of its component systems.
"""
from .engine import ScaffoldEngine

__all__ = ["ScaffoldEngine"]