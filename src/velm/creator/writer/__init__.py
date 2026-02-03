# Path: scaffold/creator/writer/__init__.py
# -----------------------------------------
"""
=================================================================================
== THE SANCTUM OF INSCRIPTION (V-Ω-MODULAR-APOTHEOSIS)                         ==
=================================================================================
This sanctum houses the GnosticWriter and its pantheon of specialist artisans.
It exposes the unified facade for all writing operations.
"""
from .engine import GnosticWriter
from .contracts import WriterResult, WriteMode

__all__ = ["GnosticWriter", "WriterResult", "WriteMode"]