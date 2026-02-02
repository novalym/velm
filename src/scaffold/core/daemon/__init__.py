# Path: core/daemon/__init__.py
# -----------------------------
# LIF: 100x | ROLE: DAEMON_PACKAGE_GATEWAY

"""
=================================================================================
== THE DAEMONIC SANCTUM (V-Ω-MODULAR-GATEWAY)                                  ==
=================================================================================
This is the public face of the Daemon. It re-exports the GnosticNexus and its
critical components to ensure backward compatibility with the rest of the cosmos.
"""

from .nexus import GnosticNexus
from .serializer import gnostic_serializer
from .resolver import GnosticRuntimeResolver
# [ASCENSION]: 'telepathy' is dead. 'akashic' now holds the memory.

__all__ = ["GnosticNexus", "gnostic_serializer", "GnosticRuntimeResolver"]