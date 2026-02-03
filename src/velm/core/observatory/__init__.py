# Path: scaffold/core/observatory/__init__.py
# -------------------------------------------
"""
=================================================================================
== THE SACRED GATEWAY TO THE OBSERVATORY (V-Ω-SINGLETON-ACCESS)                ==
=================================================================================
This scripture exposes the Gnostic Observatory to the rest of the cosmos.
It instantiates the Sovereign Manager, ensuring a single source of truth for
project state across the entire runtime.
"""

from .manager import ObservatoryManager
from .contracts import ProjectEntry, ProjectHealth, ProjectType, ObservatoryState

# The Sovereign Instance
# All artisans must commune with this instance to perceive the workspace.
Observatory = ObservatoryManager()

__all__ = [
    "Observatory",
    "ObservatoryManager",
    "ProjectEntry",
    "ProjectHealth",
    "ProjectType",
    "ObservatoryState"
]