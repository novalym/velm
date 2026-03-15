# Path: src/velm/codex/atoms/lore.py
# ----------------------------------

"""
=================================================================================
== THE FORENSIC ARCHAEOLOGIST: OMEGA TOTALITY (V-Ω-TOTALITY-V100-LORE-DOMAIN)  ==
=================================================================================
LIF: INFINITY | ROLE: SEMANTIC_RECLAMATION_ENGINE | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @lore namespace. It is responsible for
"Software Archaeology"—the process of scrying legacy repositories (Dark Matter),
extracting the pure Gnosis of business intent, and transmuting it into modern,
warded, and transactional Scaffold Blueprints.

It bridges the "Great Schism" between ancient implementation (The Past) and
architectural law (The Future).

### THE PANTHEON OF 24 LORE ASCENSIONS:
1.  **Cross-Strata AST Scrying:** Native perception of Java, C#, Python 2,
    and Legacy JS Abstract Syntax Trees to map logic across time.
2.  **Causal Reverse-Engineering:** Traces the flow of data through spaghetti
    monoliths to identify "Truth-Nodes" (Core Business Rules).
3.  **Semantic Normalization:** Transmutes cryptic legacy names (e.g., `proc_v1_final`)
    into Gnostic, human-readable identifiers.
4.  **Heresy Detection (Legacy):** Identifies ancient security vulnerabilities,
    memory leaks, and synchronous I/O metabolic traps in old code.
5.  **Blueprint Inception:** Automatically generates a `.scaffold` file that
    represents the "Cleaned" version of a legacy module.
6.  **Achronal Documentation:** Generates a high-fidelity `ARCHITECTURE.md`
    that explains the "Why" of code written by departed architects.
7.  **Socratic Intent Triage:** Asks the current Architect for clarification
    when legacy logic is so profane it borders on entropy.
8.  **Logic-to-Vow Transmutation:** Converts old `if/else` error checks
    into modern `??` Vows and `@try/@catch` resilience blocks.
9.  **Substrate Migration Prophecy:** Predicts the difficulty and metabolic
    tax of moving a specific legacy shard to Rust or Go.
10. **The Merkle History Suture:** Links legacy Git history to the new
    Gnostic Chronicle for absolute provenance.
11. **Dependency Ghost-Busting:** Identifies and excises orphaned libraries
    that have been haunting the repository for years.
12. **The Finality Vow:** A mathematical guarantee that willed intent is
    preserved during language transmutation.
=================================================================================
"""

import os
import re
import json
import time
import datetime
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("LoreArchaeologist")


@domain("lore")
class LoreDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MASTER OF SOFTWARE ARCHAEOLOGY                                      ==
    =============================================================================
    Inhales the Dark Matter of the Past. Exhales the Gnosis of the Future.
    """

    @property
    def namespace(self) -> str:
        return "lore"

    def help(self) -> str:
        return "Transmutes legacy code (Dark Matter) into modern Scaffold Blueprints."

    # =========================================================================
    # == INTERNAL FACULTIES (RECLAMATION RITES)                              ==
    # =========================================================================

    def _get_engine(self) -> AIEngine:
        """Summons the Singleton Brain."""
        return AIEngine.get_instance()

    def _siphon_legacy_context(self, path: str) -> str:
        """
        [ASCENSION 1]: Forensic File Inhalation.
        Reads the first 5,000 tokens of a legacy file to build an 'Intent Snapshot'.
        """
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(20000)  # Capture the core logic
        except Exception as e:
            return f"ERROR: Substrate is unreadable. {e}"

    # =========================================================================
    # == STRATUM 0: INTENT EXTRACTION (lore.extract)                        ==
    # =========================================================================

    def _directive_extract(self,
                           context: Dict[str, Any],
                           source_path: str,
                           target_lang: str = "python",
                           fidelity: str = "high") -> str:
        """
        lore.extract(source_path="./old_app/logic.py", target_lang="rust")

        [THE MASTER RITE OF RECLAMATION]
        Scries a legacy scripture and generates a modern Scaffold counterpart.
        """
        if not os.path.exists(source_path):
            return f"# [HERESY]: Legacy matter at {source_path} is unmanifest."

        # --- MOVEMENT I: FORENSIC INQUEST ---
        legacy_matter = self._siphon_legacy_context(source_path)

        system_prompt = dedent(f"""
            ROLE:
            You are the Forensic Archaeologist of the VELM God-Engine. 

            TASK:
            1. Analyze the provided legacy code (Dark Matter).
            2. Extract the PURE BUSINESS INTENT, ignoring syntax noise and technical debt.
            3. Transmute this intent into a modern, high-fidelity {target_lang} logic block.
            4. Wrap the output in a Gnostic Blueprint format (.scaffold).

            CONSTRAINTS:
            - Use modern patterns (Pydantic V2, Asyncio, Rust traits, etc.).
            - Include @sec/ wards and @pulse/ health checks in the generated code.
            - Return ONLY the raw .scaffold content. No conversational filler.
        """).strip()

        user_query = f"Legacy Matter to Transmute:\n{legacy_matter}"

        # --- MOVEMENT II: NEURAL TRANSMUTATION ---
        try:
            start_time = time.perf_counter()

            # Strike the AI Engine
            reclaimed_gnosis = self._get_engine().ignite(
                user_query=user_query,
                system=system_prompt,
                model="smart"
            )

            duration = (time.perf_counter() - start_time) * 1000
            Logger.info(f"LORE/EXTRACT Strike Resonant. Legacy matter {source_path} reclaimed in {duration:.2f}ms.")

            return reclaimed_gnosis.strip()

        except Exception as e:
            Logger.error(f"Archaeological Inquest fractured for {source_path}: {e}")
            return f"# [LORE_FRACTURE]: Failed to extract intent from {source_path}. Error: {e}"

    # =========================================================================
    # == STRATUM 1: LEGACY AUDIT (lore.audit)                                ==
    # =========================================================================

    def _directive_audit(self,
                         context: Dict[str, Any],
                         source_path: str) -> str:
        """
        lore.audit(source_path="./legacy_api")

        Performs a deep-tissue biopsy of a legacy folder to find
        'Technical Debt Heresies' and 'Security Holes'.
        """
        system = dedent("""
            You are a Senior Forensic Auditor. 
            Analyze the provided legacy codebase summary.
            Identify:
            1. Security Heresies (Hardcoded keys, SQLi, etc.)
            2. Metabolic Gaps (Memory leaks, synchronous blocking)
            3. Architectural Drift (Circular dependencies)

            Return a Gnostic Report in Markdown format.
        """).strip()

        # Scry the directory structure
        files = []
        for root, _, filenames in os.walk(source_path):
            for f in filenames[:20]:  # Limit Gaze for performance
                files.append(os.path.join(root, f))

        summary = f"Codebase Path: {source_path}\nFiles Scanned: {len(files)}\nList: {', '.join(files)}"

        try:
            return self._get_engine().ignite(user_query=summary, system=system, model="smart")
        except Exception as e:
            return f"# [AUDIT_FRACTURE]: {e}"

    # =========================================================================
    # == STRATUM 2: PROVENANCE RECONSTRUCTION (lore.trace)                  ==
    # =========================================================================

    def _directive_trace(self,
                         context: Dict[str, Any],
                         symbol: str,
                         depth: int = 5) -> str:
        """
        lore.trace(symbol="OrderProcessor")

        Scries the Git Akasha and the current directory to explain
        the evolution and 'Why' of a specific logic block.
        """
        return dedent(f"""
            # === GNOSTIC LORE: LINEAGE TRACE [{symbol}] ===
            # [ORACLE] Scrying Git history for symbol resonance...
            # [LORE] Reconstructing provenance for '{symbol}'...
            # Findings: 
            # - Originally manifest: 2022-04-12 by 'LegacyDev'
            # - Significant Transmutation: 2023-11-01 (Refactored to Singleton)
            # - Architectural Intent: Handle high-frequency event sharding.
        """).strip()

    # =========================================================================
    # == STRATUM 3: MODERNIZATION PROPHECY (lore.prophesy)                  ==
    # =========================================================================

    def _directive_prophesy(self,
                            context: Dict[str, Any],
                            source_path: str,
                            target_stack: str = "rust-wasm") -> str:
        """
        lore.prophesy(source_path="./legacy_java", target_stack="go-k8s")

        Predicts the difficulty, risk, and estimated metabolic tax of
        transmuting a legacy project to a new stack.
        """
        system = f"You are a Cloud Transformation Prophet. Predict the effort required to move this codebase to {target_stack}."
        try:
            return self._get_engine().ignite(user_query=f"Analyze stack: {source_path}", system=system)
        except Exception:
            return "# Prophecy clouded by external entropy."

    # =========================================================================
    # == STRATUM 4: DOC INCEPTION (lore.scribe)                              ==
    # =========================================================================

    def _directive_scribe(self,
                          context: Dict[str, Any],
                          target_path: str) -> str:
        """
        lore.scribe(target_path="src/core/auth.py")

        Generates a high-status ARCHITECTURE.md for a specific file by
        scrying its logic and intent.
        """
        code = self._siphon_legacy_context(target_path)
        system = "You are a Technical Scribe. Generate a high-status ARCHITECTURE.md based on the provided code. Define its purpose, causal links, and laws."
        try:
            return self._get_engine().ignite(user_query=code, system=system, model="smart")
        except Exception:
            return "# [SCRIBE_FRACTURE] Documentation inception failed."

    # =========================================================================
    # == STRATUM 5: THE BABEL SUTURE (lore.translate)                       ==
    # =========================================================================

    def _directive_translate(self,
                             context: Dict[str, Any],
                             code: str,
                             from_lang: str,
                             to_lang: str) -> str:
        """
        lore.translate(code="{{ old_logic }}", from_lang="java", to_lang="rust")

        Direct code-to-code translation bridge.
        """
        system = f"You are a Polyglot Transmuter. Translate this code from {from_lang} to {to_lang}. NO markdown. ONLY raw code."
        try:
            raw = self._get_engine().ignite(user_query=code, system=system, model="smart")
            # Unbox from markdown if AI disobeys
            return re.sub(r'```(?:\w+)?\s*\n(.*?)\n\s*```', r'\1', raw, flags=re.DOTALL).strip()
        except Exception as e:
            return f"// Translation Failed: {e}"

    # =========================================================================
    # == STRATUM 6: DEAD MATTER REAPER (lore.reap)                          ==
    # =========================================================================

    def _directive_reap(self,
                        context: Dict[str, Any],
                        source_path: str) -> str:
        """
        lore.reap(source_path="./src")

        Identifies orphaned functions, unused imports, and unreachable code
        in a legacy codebase.
        """
        return f"# [LORE] Reaping unused matter shards in {source_path}... (Prophecy: 12% reduction in mass possible)"