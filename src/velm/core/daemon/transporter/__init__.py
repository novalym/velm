# Path: core/daemon/transporter/__init__.py
# -----------------------------------------
"""
=================================================================================
== THE KINETIC TRANSPORTER SUBSYSTEM (V-Ω-HYDRODYNAMIC-IO)                     ==
=================================================================================
The Physics Engine of the Gnostic Daemon.
Handles the atomic movement of bytes across the dimensional gap (Socket)
using generator-based streaming and zero-copy slicing.

[EXPORTS]:
- GnosticTransporter: The primary engine.
"""

from .engine import GnosticTransporter

__all__ = ["GnosticTransporter"]