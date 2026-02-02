# scaffold/core/simulation/__init__.py

"""
=================================================================================
== THE SANCTUM OF SIMULATION (V-Ω-MODULAR-SINGULARITY)                         ==
=================================================================================
This sanctum houses the God-Engine of Prophecy. It allows the Architect to gaze
into the future consequences of a rite without altering the present reality.

It creates a parallel universe (Sandbox), executes the Architect's Will within it,
and returns a Gnostic Differential of the timeline divergence.
"""
from .conductor import SimulationConductor
from .prophecy import Prophecy, GnosticDiff

__all__ = ["SimulationConductor", "Prophecy", "GnosticDiff"]