# Path: scaffold/core/ignition/__init__.py
# ----------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_IGNITION_SINGULARITY_V3

"""
=================================================================================
== THE IGNITION ENGINE (SINGULARITY GATEWAY)                                   ==
=================================================================================
The supreme interface for project perception, validation, and execution.
This module unifies the Mind (Diviner), the Shield (Sentinel), and the Hand (Conductor).
=================================================================================
"""

from .conductor import Conductor, IgnitionConductor
from .diviner.engine import IgnitionDiviner
from .contracts import (
    ExecutionPlan,
    IgnitionAura,
    BiologicalSupport,
    NetworkPhysics,
    VitalityState
)
from .diviner.exceptions import DivinationHeresy, VoidSanctumError
from .sentinel.priest import ToolchainSentinel

# [ASCENSION]: THE MASTER ENGINE API
# This is what the rest of Ideabox Quantum imports.
__all__ = [
    "Conductor",
    "IgnitionConductor",
    "IgnitionDiviner",
    "ExecutionPlan",
    "IgnitionAura",
    "BiologicalSupport",
    "NetworkPhysics",
    "VitalityState",
    "ToolchainSentinel",
    "DivinationHeresy",
    "VoidSanctumError"
]