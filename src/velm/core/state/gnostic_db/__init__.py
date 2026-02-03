# Path: scaffold/core/state/gnostic_db/__init__.py
# ------------------------------------------------

"""
=================================================================================
== THE CRYSTAL MIND SANCTUM (V-Ω-MODULAR-ACCESS)                               ==
=================================================================================
The public gateway to the SQLite persistence layer.
"""

# Graceful degradation if SQLAlchemy is missing
try:
    from sqlalchemy import __version__
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

if SQL_AVAILABLE:
    from .engine import GnosticDatabase
    from .models import RiteModel, ScriptureModel, BondModel, Base
else:
    GnosticDatabase = None
    RiteModel = None
    ScriptureModel = None
    BondModel = None
    Base = None

__all__ = [
    "GnosticDatabase",
    "RiteModel",
    "ScriptureModel",
    "BondModel",
    "Base",
    "SQL_AVAILABLE"
]