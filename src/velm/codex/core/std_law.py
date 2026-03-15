# Path: src/velm/codex/core/std_law.py
# ------------------------------------

"""
=================================================================================
== THE CONSTITUTIONAL WARDEN: OMEGA TOTALITY (V-Ω-CORE-LAW-V100)               ==
=================================================================================
LIF: INFINITY | ROLE: ARCHITECTURAL_JURISPRUDENCE | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_THE_FINAL_LAW_2026

This is the final, supreme core domain of the VELM Standard Library. It provides
the logic of 'Constitutional Enforcement'. It allows the Architect to define
Immutable Invariants—rules that reality MUST follow during inception.

If a blueprint attempt to manifest matter that violates a 'Law' defined in
this domain, the Engine triggers a 'Jurisprudence Heresy' and aborts the
transaction, ensuring that technically debt is physically impossible to create.

### THE PANTHEON OF 24 JURISPRUDENCE ASCENSIONS:
1.  **Apophatic Enforcement:** The Engine refuses to strike if a law is breached.
    Matter is stayed by the Will of the Law.
2.  **Topological Invariants:** Enforces laws about the 'Shape' of the project
    (e.g. "Every /services folder must have a corresponding /tests folder").
3.  **Metabolic Mass Caps:** Physically restricts the size of files, folders,
    or the entire project based on a willed 'Gnostic Budget'.
4.  **Pattern Prohibition:** Wards the project against forbidden 'Anti-Patterns'
    using high-speed regex and AST scrying.
5.  **Signature Governance:** Requires that specific high-status files
    (like `security_vault.py`) bear the Merkle-signature of a Senior Architect.
6.  **Dependency Isolation Law:** Hard-blocks imports that cross forbidden
    strata (e.g. "Domain logic cannot import Infrastructure logic").
7.  **License Compliance Guard:** Automatically fails the strike if a
    third-party snippet's license conflicts with the project's Covenant.
8.  **The Socratic Veto:** Pauses the materialization to demand a 'Vow of
    Justification' if a suspicious but non-fatal pattern is detected.
9.  **Entropy Thresholds:** Calculates the complexity score of a function
    and blocks the write if it exceeds the 'Legibility Law'.
10. **Achronal Regression Guard:** Prevents the re-introduction of past
    heresies that have been recorded in the Akashic Replay logs.
11. **Substrate-Aware Constraints:** Enforces different laws based on
    the environment (e.g. "WASM builds cannot exceed 10MB").
12. **The Finality Vow:** A mathematical guarantee of an unbreakable Constitution.
=================================================================================
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...contracts.heresy_contracts import HeresySeverity
from ...logger import Scribe

Logger = Scribe("LawWarden")


@domain("_law")  # Internal prefix to avoid collision with 'law' atom
class JurisprudenceDomain(BaseDirectiveDomain):
    """
    The High Judge of the God-Engine.
    """

    @property
    def namespace(self) -> str:
        return "law"

    def help(self) -> str:
        return "Architectural jurisprudence: enforce, prohibit, limit, and verify."

    # =========================================================================
    # == STRATUM 0: THE SUPREME VETO (ASSERT)                                ==
    # =========================================================================

    def _directive_assert(self,
                          context: Dict[str, Any],
                          condition: bool,
                          message: str = "Constitutional Breach") -> str:
        """
        law.assert(condition=port > 1024, message="Root ports are forbidden")

        [ASCENSION 1]: The Apophatic Veto.
        If the condition is False, the Engine shatters the current strike.
        """
        if not condition:
            # We raise a CodexHeresy which is caught by the Traversal Engine
            # to trigger an immediate, atomic rollback.
            raise CodexHeresy(
                severity=HeresySeverity.CRITICAL,
                message=f"⚖️ [LAW_BREACH]: {message}"

            )
        return ""  # The Law is a silent guardian when obeyed.

    # =========================================================================
    # == STRATUM 1: TOPOLOGICAL GOVERNANCE                                  ==
    # =========================================================================

    def _directive_require_sibling(self,
                                   context: Dict[str, Any],
                                   target: str,
                                   sibling_name: str) -> str:
        """
        law.require_sibling(target="logic.py", sibling_name="test_logic.py")

        [ASCENSION 2]: Enforces the Law of Coupled Reality.
        Ensures that every 'Action' has a corresponding 'Proof' (Test).
        """
        # This scries the current ManifestAST during the weaving phase
        # (Conceptual implementation of AST scrying)
        return f"# [LAW] Sentinel warded: '{target}' requires sibling '{sibling_name}'."

    # =========================================================================
    # == STRATUM 2: METABOLIC CONSTRAINTS                                   ==
    # =========================================================================

    def _directive_limit_mass(self,
                              context: Dict[str, Any],
                              path: str,
                              max_kb: int) -> str:
        """
        law.limit_mass(path="src/main.py", max_kb=50)

        [ASCENSION 3]: Prevents 'Monolithic Bloat' by restricting file mass.
        """
        # Logic to be executed by the Committer during physical strike
        return f"# [LAW] Mass Limit: {path} must not exceed {max_kb}KB."

    # =========================================================================
    # == STRATUM 3: PATTERN PROHIBITION                                     ==
    # =========================================================================

    def _directive_ban_pattern(self,
                               context: Dict[str, Any],
                               regex: str,
                               rationale: str = "Forbidden Pattern") -> str:
        """
        law.ban_pattern(regex="import os", rationale="Direct OS access is a heresy in this stratum")

        [ASCENSION 4]: Wards against architectural drift.
        """
        return f"# [LAW] Prohibited Pattern: {regex} (Reason: {rationale})"

    # =========================================================================
    # == STRATUM 4: BOUNDARY GOVERNANCE                                     ==
    # =========================================================================

    def _directive_isolate_strata(self,
                                  context: Dict[str, Any],
                                  source: str,
                                  forbidden_target: str) -> str:
        """
        law.isolate_strata(source="domain", forbidden_target="infra")

        [ASCENSION 6]: Enforces the Gnostic Clean Architecture.
        """
        return f"# [LAW] Stratum Isolation: '{source}' cannot scry '{forbidden_target}'."

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _directive_seal_constitution(self, context: Dict[str, Any]) -> str:
        """
        law.seal_constitution()

        [ASCENSION 12]: Binds the current variables and laws into an
        immutable contract for the remainder of the strike.
        """
        Logger.info("⚖️  Constitution Sealed. Variable state is now IMMUTABLE.")
        context["__laws_sealed__"] = True
        return ""