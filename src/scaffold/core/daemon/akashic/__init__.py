# Path: core/daemon/akashic/__init__.py
# -------------------------------------
# LIF: INFINITY | ROLE: MEMORY_GATEWAY
"""
=================================================================================
== THE AKASHIC SUBSYSTEM (V-Ω-TEMPORAL-CORTEX)                                 ==
=================================================================================
The collective memory of the Gnostic Daemon.
It handles:
1. Ingestion of Reality (Logging)
2. Storage of History (Memory)
3. Projection of Truth (Broadcasting)

[EXPORTS]:
- AkashicRecord: The sovereign controller.
"""

from .engine import AkashicRecord

__all__ = ["AkashicRecord"]