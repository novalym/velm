# Path: core/daemon/serializer/__init__.py
# ----------------------------------------
# LIF: INFINITY | ROLE: TRANSLATION_GATEWAY
"""
=================================================================================
== THE SERIALIZER SUBSYSTEM (V-Ω-UNIVERSAL-TRANSLATOR)                         ==
=================================================================================
The Alchemical Transmuter.
Converts complex Python objects into JSON-safe primitives.

[EXPORTS]:
- gnostic_serializer: The primary hook for json.dumps.
"""

from .engine import GnosticSerializer, gnostic_serializer

__all__ = ["GnosticSerializer", "gnostic_serializer"]