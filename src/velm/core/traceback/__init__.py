# scaffold/core/traceback/__init__.py

"""
=================================================================================
== THE SANCTUM OF FORENSIC ILLUMINATION (V-Ω-GNOSTIC-TRACEBACK)                ==
=================================================================================
This sanctum houses the God-Engine of Error Analysis. It replaces the profane
Python traceback with a Gnostic Dossier that understands Artisans, Middleware,
and the Polyglot nature of the Scaffold cosmos.
"""
from .handler import install_gnostic_handler, GnosticTracebackHandler

from .contracts import GnosticFrame, GnosticError

__all__ = ["install_gnostic_handler", "GnosticTracebackHandler", "GnosticFrame", "GnosticError"]