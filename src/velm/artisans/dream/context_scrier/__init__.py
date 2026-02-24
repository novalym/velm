# Path: artisans/dream/context_scrier/__init__.py
# -----------------------------------------------

"""
=================================================================================
== THE CONTEXT SCRIER SANCTUM (V-Ω-FORENSIC-ANALYSIS)                          ==
=================================================================================
@gnosis:title The Context Scrier
@gnosis:summary The sensory organ that perceives the current state of reality.
@gnosis:LIF 50x

This directory houses the logic for analyzing existing projects to enable
**Incremental Dreaming**. It allows the AI to "See" the code before it writes.
"""

from .engine import ContextScrier
from .contracts import RealityState, ProjectDNA

__all__ = ["ContextScrier", "RealityState", "ProjectDNA"]