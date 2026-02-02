# Path: core/daemon/resolver/__init__.py
# --------------------------------------
# LIF: INFINITY | ROLE: RESOLVER_GATEWAY
"""
=================================================================================
== THE RESOLVER SUBSYSTEM (V-Ω-DNA-SEQUENCER)                                  ==
=================================================================================
The Gnostic DNA Sequencer.
Determines Identity, Context, and Environment for the Daemon.

[EXPORTS]:
- GnosticRuntimeResolver: The sovereign controller.
"""

from .engine import GnosticRuntimeResolver

__all__ = ["GnosticRuntimeResolver"]