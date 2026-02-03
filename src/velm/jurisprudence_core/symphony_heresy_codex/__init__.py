# Path: jurisprudence_core/symphony_heresy_codex/__init__.py
# ---------------------------------------------------------

"""
=================================================================================
== THE LIVING CODEX OF SYMPHONIC LAW (V-Ω-MODULAR-REGISTRY)                    ==
=================================================================================
LIF: ∞

This sanctum aggregates the dispersed Gnostic Laws governing the Language of Will
(.symphony). It unifies them into the one true `SYMPHONY_HERESY_CODEX`.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# --- THE DIVINE SUMMONS OF THE DOMAIN SCROLLS ---
from .lexical import LEXICAL_LAWS
from .kinetic import KINETIC_LAWS
from .metaphysical import METAPHYSICAL_LAWS
from .polyglot import POLYGLOT_LAWS
from .philosophy import PHILOSOPHICAL_LAWS

# --- THE GRAND UNIFICATION ---
SYMPHONY_HERESY_CODEX: Dict[str, GnosticLaw] = {}

# We weave the laws into the singular Codex.
SYMPHONY_HERESY_CODEX.update(LEXICAL_LAWS)
SYMPHONY_HERESY_CODEX.update(KINETIC_LAWS)
SYMPHONY_HERESY_CODEX.update(METAPHYSICAL_LAWS)
SYMPHONY_HERESY_CODEX.update(POLYGLOT_LAWS)
SYMPHONY_HERESY_CODEX.update(PHILOSOPHICAL_LAWS)

__all__ = ["SYMPHONY_HERESY_CODEX"]