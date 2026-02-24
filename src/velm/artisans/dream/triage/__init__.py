# Path: artisans/dream/triage/__init__.py
# ---------------------------------------

"""
=================================================================================
== THE TRIAGE SANCTUM (V-Ω-INTENT-DISCRIMINATOR)                               ==
=================================================================================
@gnosis:title The Intent Diviner
@gnosis:summary The high-speed switching station that routes natural language
                 to the correct architectural subsystem.
@gnosis:LIF INFINITY

It determines if the Architect intends to:
1.  **FORGE** (Genesis): Create new reality.
2.  **MUTATE** (Mutation): Change existing reality.
3.  **WIELD** (Tooling): Operate machinery (zip, lint, test).
4.  **INQUIRE** (Inquiry): Seek wisdom.
"""

from .engine import IntentDiviner
from .contracts import DreamIntent

__all__ = ["IntentDiviner", "DreamIntent"]