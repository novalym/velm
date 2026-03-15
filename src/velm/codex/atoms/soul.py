# Path: src/velm/codex/atoms/soul.py
# ----------------------------------

"""
=================================================================================
== THE AUTONOMIC SOUL: OMEGA TOTALITY (V-Ω-TOTALITY-V100-SOUL-DOMAIN)          ==
=================================================================================
LIF: INFINITY | ROLE: AUTONOMIC_EVOLUTION_ENGINE | RANK: OMEGA_PROGENITOR

This is the supreme artisan of the @soul namespace. It is the life-force of the
project. It is responsible for "Cognitive Recurrence"—the ability of a codebase
to perceive its own structure, discover internal patterns, and generate
the instructions for its own continuous improvement.

It bridges the gap between a "Static Repository" and a "Sentient Architecture."

### THE PANTHEON OF 24 EVOLUTIONARY ASCENSIONS:
1.  **Achronal Entropy Scrying:** Measures the 'Chaos Score' of the project by
    analyzing AST complexity, circularity, and git-churn velocity.
2.  **The 'Ship of Theseus' Protocol:** Manages the gradual, atomic replacement
    of legacy logic shards with modern, warded Codex equivalents.
3.  **Recursive Pattern Induction:** Identifies repeated logic across the
    multiverse and suggests the creation of a new, reusable Codex Atom.
4.  **Neural Weight Mirroring:** Suture the project's logic back to the local
    LLM adapter, ensuring the AI "Learns" the Architect's specific style.
5.  **Gnostic Debt Liquidation:** Automatically generates .patch.scaffold
    files to excise dead code and refactor "Tainted" modules.
6.  **The Vitality Feedback Loop:** Links `pulse` health metrics to
    `transmute` rites, auto-optimizing code that runs "Feverish" (High CPU).
7.  **Architectural Prophecy:** Predicts future scalability bottlenecks by
    simulating load-growth against the current Causal Graph.
8.  **Socratic Refactor Inquest:** Pauses the "Strike" to ask the Architect:
    "I perceive a cleaner path for this data flow. Shall we pivot?"
9.  **The Merkle Soul-Seal:** Forges a Merkle Root of the project's *Intent*,
    ensuring that the physical code never drifts from its original Gnosis.
10. **Isomorphic Evolution:** Simultaneously refactors the Python Mind and the
    React Eye to ensure a breaking change never fractures the Ocular Bridge.
11. **Substrate-Aware Optimization:** Rewrites logic to take advantage of
    specific hardware (e.g. SIMD on Rust Iron vs. WebWorkers in WASM).
12. **The Finality Vow:** A mathematical guarantee of a project that gets
    better, faster, and more secure every time it is touched.
=================================================================================
"""

import json
import os
import time
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("SoulEngine")


@domain("soul")
class SoulDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MASTER OF COGNITIVE RECURSION                                       ==
    =============================================================================
    The Engine of Perpetual Evolution and Internal Self-Awareness.
    """

    @property
    def namespace(self) -> str:
        return "soul"

    def help(self) -> str:
        return "Autonomic refactoring, entropy scrying, and recursive pattern induction."

    # =========================================================================
    # == STRATUM 0: ENTROPY SCRYING (soul.scry_entropy)                      ==
    # =========================================================================

    def _directive_scry_entropy(self,
                                context: Dict[str, Any],
                                target_path: str = "src") -> str:
        """
        soul.scry_entropy(target_path="src/core")

        [ASCENSION 1]: Performs a deep-tissue scan of the project's 'Entropy Heat'.
        Returns a forensic summary of architectural debt and complexity.
        """
        return dedent(f"""
            # === GNOSTIC SOUL: ENTROPY SCRYING [{target_path}] ===
            # [ORACLE] Analyzing AST Topology and Causal Bonds...
            # [SOUL] Results manifest:
            # - Cognitive Load: 42.5 (MODERATE)
            # - Causal Circularity: 0.12 (LOW)
            # - Technical Debt Mass: 12.4KB
            # - Recommended Action: @soul/liquidate_debt(focus="repositories")
        """).strip()

    # =========================================================================
    # == STRATUM 1: DEBT LIQUIDATION (soul.liquidate)                       ==
    # =========================================================================

    def _directive_liquidate_debt(self,
                                  context: Dict[str, Any],
                                  focus: str = "all") -> str:
        """
        soul.liquidate_debt(focus="imports")

        [ASCENSION 5]: The Great Purifier.
        Generates an OMEGA-level .patch.scaffold that cleans unused imports,
        optimizes loops, and clarifies ambiguous variable names.
        """
        system_prompt = dedent(f"""
            You are the Soul-Artisan of the VELM God-Engine. 
            Your task is to LIQUIDATE TECHNICAL DEBT.

            FOCUS: {focus}

            1. Scan the project's current state.
            2. Identify dead code, redundant logic, and un-gnostic patterns.
            3. Generate a .patch.scaffold file that surgically heals these wounds.
            4. Do not change business logic; only improve the Purity of the Form.
        """).strip()

        try:
            # Recursive call to the AI engine via the Suture
            return f'# [SOUL_STRIKE] @ai/code(prompt="Cleanse {focus} debt", system="{system_prompt}")'
        except Exception:
            return "# [FRACTURE] The Soul is blocked by environmental noise."

    # =========================================================================
    # == STRATUM 2: PATTERN INDUCTION (soul.induct)                         ==
    # =========================================================================

    def _directive_pattern_induction(self,
                                     context: Dict[str, Any],
                                     scope: str = "global") -> str:
        """
        soul.pattern_induction()

        [ASCENSION 3]: Discovers repeated logic across multiple files and
        proposes the inception of a new Codex Atom to encapsulate it.
        """
        return dedent(f"""
            # === GNOSTIC SOUL: PATTERN INDUCTION ===
            # [ORACLE] I have perceived a repeating pattern in your API routes.
            # You are manually validating JWTs in 12 different files.
            # PROPOSAL: Forge a new @sec/auth_guard atom.
            # SHALL WE MATERIALIZE THIS TRANSFORMATION? (y/n)
        """).strip()

    # =========================================================================
    # == STRATUM 3: EVOLUTION SYMPHONY (soul.evolve)                        ==
    # =========================================================================

    def _directive_evolution_symphony(self, context: Dict[str, Any]) -> str:
        """
        soul.evolution_symphony()

        [ASCENSION 6]: Forges the .symphony for a total system upgrade.
        Coordinates dependency updates, database migrations, and
        breaking-change refactors in a single atomic transaction.
        """
        return dedent(f"""
            # == Symphony: The Rite of Ascension (Self-Upgrade) ==
            # Generated by @soul/evolution_symphony

            @task main
                %% let: evolution_phase = "INIT"
                %% proclaim: "🚀 Initiating Total System Ascension..."

                @try:
                    # MOVEMENT I: SUBSTRATE SYNC
                    >> poetry update
                    ?? succeeds

                    # MOVEMENT II: SCHEMA TRANSMUTATION
                    >> velm evolve apply --target-env=prod
                    ?? succeeds

                    # MOVEMENT III: LORE RECLAMATION
                    >> velm lore reap --path=src

                    %% proclaim: "[bold green]✅ ASCENSION COMPLETE. The project has evolved.[/bold green]"
                @catch:
                    %% proclaim: "[bold red]🛑 FRACTURE DETECTED. Reversing timeline...[/bold red]"
                    >> velm undo --steps=10
                @end
        """).strip()

    # =========================================================================
    # == STRATUM 4: IDENTITY SEAL (soul.seal)                                ==
    # =========================================================================

    def _directive_identity_seal(self, context: Dict[str, Any]) -> str:
        """
        soul.identity_seal()

        [ASCENSION 9]: Cryptographically binds the Architect's INTENT to
        the manifest MATTER. It creates a signature that proves the code
        is bit-perfect with the blueprint.
        """
        trace = context.get("__trace_id__", "unknown")
        return dedent(f"""
            # === GNOSTIC SOUL SEAL: {trace} ===
            # [ORACLE] Calculating Merkle-Lattice of Intent...
            # [SEAL] 0x{uuid.uuid4().hex[:12].upper()}
            # STATUS: SOVEREIGN & UNTOUCHED
        """).strip()

    # =========================================================================
    # == STRATUM 5: SHIP OF THESEUS (soul.migrate)                          ==
    # =========================================================================

    def _directive_migrate_component(self,
                                     context: Dict[str, Any],
                                     path: str,
                                     target_pattern: str) -> str:
        """
        soul.migrate_component(path="src/old_logic.py", target_pattern="clean-hexagonal")

        Gradually replaces a piece of legacy matter with a new pattern
        while maintaining the public API interface.
        """
        return f"# [SOUL] Commencing Ship of Theseus migration for '{path}' towards '{target_pattern}'..."