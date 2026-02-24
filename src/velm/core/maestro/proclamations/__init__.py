# Path: src/velm/core/maestro/proclamations/__init__.py
# ----------------------------------------------------

"""
=================================================================================
== THE PROCLAMATION PANTHEON (V-Ω-TOTALITY-V200)                               ==
=================================================================================
LIF: ∞ | ROLE: SYMBOLIC_REVEALER | RANK: OMEGA_SOVEREIGN

The unified entry point for the Engine's voice. It houses the specialist Scribes
responsible for transmuting Gnosis into visual and ethereal light.
"""

from .router import dispatch_proclamation
from .base import ProclamationScribe

__all__ = ["dispatch_proclamation", "ProclamationScribe"]