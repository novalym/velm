# Path: scaffold/core/state/__init__.py
# -------------------------------------
"""
=================================================================================
== THE SACRED GATEWAY TO THE STATE SINGULARITY (V-Ω-ETERNAL-APOTHEOSIS)        ==
=================================================================================
"""

from .store import Store
from .ledger import ActiveLedger
from .machine import GnosticRite
from .snapshot import GnosticSnapshot

# Graceful export for environments without SQLAlchemy
try:
    from .gnostic_db import GnosticDatabase
except ImportError:
    GnosticDatabase = None

__all__ = [
    "Store",
    "ActiveLedger",
    "GnosticRite",
    "GnosticSnapshot",
    "GnosticDatabase"
]