# Path: core/daemon/nexus/__init__.py
# -----------------------------------
# LIF: INFINITY | ROLE: NEXUS_GATEWAY
"""
=================================================================================
== THE NEXUS SUBSYSTEM (V-Ω-SOVEREIGN-COORDINATOR)                             ==
=================================================================================
The central nervous system of the Daemon.
Orchestrates Network (Scout/Gatekeeper), Memory (Akashic), and Logic (Dispatcher).

[EXPORTS]:
- GnosticNexus: The primary controller class.
"""

from .engine import GnosticNexus

__all__ = ["GnosticNexus"]