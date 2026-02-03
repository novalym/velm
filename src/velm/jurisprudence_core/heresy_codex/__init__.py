# Path: jurisprudence_core/heresy_codex/__init__.py
# -------------------------------------------------

"""
=================================================================================
== THE LIVING CODEX OF HERESIES (V-Ω-MODULAR-REGISTRY-FINALIS)                 ==
=================================================================================
LIF: ∞

This sanctum aggregates the dispersed Gnostic Laws from all domains of the
Scaffold Cosmos, EXCLUDING the Symphony, which maintains its own sovereign
codex. It unifies them into the one true `HERESY_CODEX`.

It is the single source of truth for the `GnosticAdjudicator`.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# --- THE DIVINE SUMMONS OF THE DOMAIN SCROLLS ---
from .lexical import LEXICAL_LAWS
from .architectural import ARCHITECTURAL_LAWS
from .security import SECURITY_LAWS
from .hygiene import HYGIENE_LAWS
from .supply_chain import SUPPLY_LAWS
from .infra import INFRA_LAWS
from .perf import PERFORMANCE_LAWS
from .data import DATA_LAWS
from .meta import META_HERESY_LAWS

# --- THE GRAND UNIFICATION ---
HERESY_CODEX: Dict[str, GnosticLaw] = {}

# We weave the laws into the singular Codex.
HERESY_CODEX.update(LEXICAL_LAWS)
HERESY_CODEX.update(ARCHITECTURAL_LAWS)
HERESY_CODEX.update(SECURITY_LAWS)
HERESY_CODEX.update(HYGIENE_LAWS)
HERESY_CODEX.update(SUPPLY_LAWS)
HERESY_CODEX.update(INFRA_LAWS)
HERESY_CODEX.update(PERFORMANCE_LAWS)
HERESY_CODEX.update(DATA_LAWS)
HERESY_CODEX.update(META_HERESY_LAWS)

__all__ = ["HERESY_CODEX"]