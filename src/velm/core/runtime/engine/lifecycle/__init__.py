# Path: core/runtime/engine/lifecycle/__init__.py
# -----------------------------------------------

"""
=================================================================================
== THE LIFECYCLE SUBSYSTEM (V-Ω-BIOLOGICAL-KERNEL)                             ==
=================================================================================
Manages the existence of the God-Engine.

[PHASES]:
1. GENESIS (Bootstrap): Skill Awakening & Pipeline Forging.
2. VIGIL (Vitality): Metabolic Monitoring & Heartbeat.
3. DRAIN (Shutdown): Graceful resource release & Transaction rollback.
4. VOID (Termination): Final exit.

[EXPORTS]:
- EngineBootstrap: The Creator.
- VitalityMonitor: The Preserver.
- ShutdownManager: The Destroyer.
- EngineState: The Phases of Being.
"""

from .bootstrap import EngineBootstrap
from .vitality import VitalityMonitor
from .shutdown import ShutdownManager
from .state import EngineState, LifecyclePhase

__all__ = [
    "EngineBootstrap",
    "VitalityMonitor",
    "ShutdownManager",
    "EngineState",
    "LifecyclePhase"
]