# Path: scaffold/core/kernel/archivist/__init__.py
# ------------------------------------------------

"""
=================================================================================
== THE SANCTUM OF THE ARCHIVIST (V-Ω-TEMPORAL-ENGINE)                          ==
=================================================================================
The Gateway to Eternal Memory.
This module manages the creation (Snapshot), preservation (Retention),
and resurrection (Restoration) of project states.
"""

from .engine import GnosticArchivist
from .contracts import ArchiveConfig, ArchiveResult, RestoreConfig, RestoreResult

__all__ = [
    "GnosticArchivist",
    "ArchiveConfig",
    "ArchiveResult",
    "RestoreConfig",
    "RestoreResult"
]