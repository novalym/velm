# Path: core/daemon/dispatcher/__init__.py
# ----------------------------------------
# LIF: INFINITY | ROLE: DISPATCHER_GATEWAY
"""
=================================================================================
== THE DISPATCHER SUBSYSTEM (V-Ω-CEREBRAL-CORTEX)                              ==
=================================================================================
The decision engine of the Gnostic Daemon.
It handles:
1. Triage (Validation & Routing)
2. Resource Allocation (Thread Pools)
3. Execution (The Will)
4. Forensic Error Handling

[EXPORTS]:
- GnosticDispatcher: The sovereign controller.
"""

from .engine import GnosticDispatcher

__all__ = ["GnosticDispatcher"]