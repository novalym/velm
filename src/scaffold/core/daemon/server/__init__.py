# Path: core/daemon/server/__init__.py
# ------------------------------------
# LIF: INFINITY | ROLE: SUBSYSTEM_GATEWAY
"""
=================================================================================
== THE DAEMON SERVER SUBSYSTEM (V-Ω-LIFECYCLE-MANAGER)                         ==
=================================================================================
The beating heart of the Gnostic Daemon.
This package manages the physical existence of the process.

[EXPORTS]:
- DaemonServer: The primary lifecycle controller.
"""

from .engine import DaemonServer

__all__ = ["DaemonServer"]