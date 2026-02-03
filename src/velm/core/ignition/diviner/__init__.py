# Path: scaffold/core/ignition/diviner/__init__.py
# ------------------------------------------------
# LIF: INFINITY // AUTH_CODE: DIVINER_SINGULARITY_SEAL

"""
The Diviner Singularity.
Deterministic reality perception for the Gnostic Forge.
"""

from .engine import IgnitionDiviner
from ..contracts import ExecutionPlan, IgnitionAura, BiologicalSupport
from .exceptions import DivinationHeresy, VoidSanctumError

__all__ = [
    "IgnitionDiviner",
    "ExecutionPlan",
    "IgnitionAura",
    "BiologicalSupport",
    "DivinationHeresy",
    "VoidSanctumError"
]