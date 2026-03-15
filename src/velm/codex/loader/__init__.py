# Path: src/velm/codex/loader/__init__.py
# ---------------------------------------

"""
=================================================================================
== THE OMNISCIENT CODEX LOADER (V-Ω-TOTALITY-V24-ASCENDED)                     ==
=================================================================================
LIF: INFINITY | ROLE: KNOWLEDGE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

This is the central nervous system for all external and internal logic modules.
By separating the Loader into a full Subsystem, we achieve unparalleled
fault-tolerance, hot-reloading, and schema extraction.
=================================================================================
"""
from .registry import CodexRegistry
from ..contract import BaseDirectiveDomain


def domain(name: str):
    """
    [THE SACRED DECORATOR]
    Registers a class as a Codex Domain handler in the God-Engine.

    Usage:
        @domain("cloud")
        class CloudDomain(BaseDirectiveDomain): ...
    """

    def decorator(cls):
        # Instantiate and consecrate
        CodexRegistry.register_domain(name, cls())
        return cls

    return decorator


__all__ = ["CodexRegistry", "domain", "BaseDirectiveDomain"]