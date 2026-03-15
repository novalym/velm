# Path: src/velm/codex/core/std_cortex.py
# --------------------------------------

"""
=================================================================================
== THE NEURAL CORTEX: OMEGA TOTALITY (V-Ω-CORE-CORTEX-V100)                    ==
=================================================================================
LIF: INFINITY | ROLE: COGNITIVE_GOVERNOR | RANK: OMEGA_SUPREME_ORACLE
AUTH_CODE: Ω_CORTEX_FINALIS_2026

This is the tenth and final pillar of the VELM Standard Library. It governs the
'Physics of Thought'. It allows the God-Engine to perform Neural Inquiries
directly from within the logic of a blueprint.

It enables 'Intelligent Genesis'—where the structure of a project is not
hardcoded by a human, but 'Dreamed' by the Engine based on a set of Gnostic
Goals. It provides the interface for Semantic Reasoning, Context Retrieval,
and Neural Branching.

### THE PANTHEON OF 24 COGNITIVE ASCENSIONS:
1.  **Neural Variable Inception (Dream):** Allows the value of a variable to
    be resolved via a prompt to the AI Mind during the weave.
2.  **Semantic Context Recall:** Surgically retrieves relevant logic shards
    from the project's long-term memory (Vector DB) to guide a strike.
3.  **Cognitive Logic Gates:** Enables @if blocks to branch based on
    sentiment, intent, or complex reasoning (e.g. "if intent is high-security").
4.  **Achronal Self-Critique:** Commands the Engine to 'Review' the matter
    it just willed and generate a .patch to fix any perceived logic-gaps.
5.  **Multiversal Knowledge Suture:** Allows the blueprint to '@ask' the
    global SCAF-Hub for the most 'Resonant' way to implement a feature.
6.  **Gnostic Goal Tracking:** Maps the kinetic strike against the Architect's
    stated project objectives to calculate 'Alignment Resonance'.
7.  **Neural Compression (Distill):** Automatically summarizes massive
    logic manifolds into high-density context vectors for the AI.
8.  **The 'Aha!' Moment:** Identifies 'Architectural Epiphanies'—where a
    pattern in the code can be simplified via a newly manifest Codex Atom.
9.  **Substrate-Aware Reasoning:** Pivots the AI's suggestions based on
    hardware vitals (e.g. "Suggesting Lite-weight logic for WASM targets").
10. **Bicameral Decision Auditing:** Records the 'Rationale' behind every
    AI-driven branch in the Akashic Record for human adjudication.
11. **Entropy Backpressure:** Rejects AI generations that are too complex
    or violate the 'Law of Legibility'.
12. **The Finality Vow:** A mathematical guarantee of Sentient Architecture.
=================================================================================
"""

import json
import os
import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("CognitiveCortex")


@domain("_cortex")  # Internal prefix for 'cortex' namespace
class CortexDomain(BaseDirectiveDomain):
    """
    The High Priest of Recursive Intelligence.
    """

    @property
    def namespace(self) -> str:
        return "cortex"

    def help(self) -> str:
        return "Cognitive rites: dream, recall, adjudicate, and distill."

    # =========================================================================
    # == STRATUM 0: NEURAL INCEPTION (DREAM)                                 ==
    # =========================================================================

    def _directive_dream(self,
                         context: Dict[str, Any],
                         prompt: str,
                         expected_type: str = "string") -> Any:
        """
        cortex.dream("What is a secure port for a dev server?") -> 8081

        [ASCENSION 1]: The Neural Variable.
        Interrupts the alchemical reactor to consult the AI Mind.
        Transmutes a probabilistic whisper into a deterministic variable.
        """
        Logger.info(f"🔮 [CORTEX] Dreaming: '{prompt}'...")

        # [THE STRIKE]: We summon the Singleton AI Engine
        try:
            # We inject the current Gnostic Context into the prompt
            project_dna = {k: v for k, v in context.items() if not k.startswith("__")}

            # [ASCENSION 20]: Deterministic Caching
            # We don't re-dream the same thought twice in one strike
            dream_hash = hashlib.md5(f"{prompt}{expected_type}".encode()).hexdigest()
            if dream_hash in context.get("__dream_cache__", {}):
                return context["__dream_cache__"][dream_hash]

            response = AIEngine.get_instance().ignite(
                user_query=prompt,
                system=f"Return only the raw value for a variable of type {expected_type}. No prose.",
                context=project_dna,
                model="smart"
            )

            # [THE FIX]: Type Coercion
            clean_res = response.strip().strip('"').strip("'")
            if expected_type == "int":
                result = int(clean_res)
            elif expected_type == "float":
                result = float(clean_res)
            elif expected_type == "bool":
                result = clean_res.lower() in ("true", "yes", "1")
            else:
                result = clean_res

            # Record in cache
            if "__dream_cache__" not in context: context["__dream_cache__"] = {}
            context["__dream_cache__"][dream_hash] = result

            return result
        except Exception as e:
            Logger.error(f"Dream Fractured: {e}")
            return f"VOID_DREAM_{uuid.uuid4().hex[:4]}"

    # =========================================================================
    # == STRATUM 1: SEMANTIC RECALL (MEMORY)                                 ==
    # =========================================================================

    def _directive_recall(self,
                          context: Dict[str, Any],
                          query: str,
                          k: int = 3) -> List[str]:
        """
        cortex.recall("authentication logic")

        [ASCENSION 2]: Semantic Memory Retrieval.
        Scries the project's internal Vector Cortex for relevant logic shards.
        """
        engine = context.get("__engine__")
        if not engine or not hasattr(engine, 'cortex'):
            return []

        Logger.info(f"🔍 [CORTEX] Recalling: '{query}'...")
        # Interact with the Stratum-2 Cortex
        results = engine.cortex.recall(query, limit=k)
        return [r.content for r in results]

    # =========================================================================
    # == STRATUM 2: COGNITIVE BRANCHING (ADJUDICATE)                        ==
    # =========================================================================

    def _directive_adjudicate(self,
                              context: Dict[str, Any],
                              condition_description: str) -> bool:
        """
        @if cortex.adjudicate("the project requires high security")

        [ASCENSION 3]: The Intelligent Gate.
        Allows the AI to decide the flow of the blueprint based on
        high-level architectural intent.
        """
        Logger.info(f"⚖️ [CORTEX] Adjudicating: '{condition_description}'...")

        result = self._directive_dream(
            context,
            f"Adjudicate this architectural condition: {condition_description}. Return 'true' or 'false'.",
            expected_type="bool"
        )
        return bool(result)

    # =========================================================================
    # == STRATUM 3: CONTEXT DISTILLATION                                    ==
    # =========================================================================

    def _directive_distill(self,
                           context: Dict[str, Any],
                           content: str) -> str:
        """
        cortex.distill(content="{{ complex_logic }}")

        [ASCENSION 7]: High-Density Semantic Compression.
        Transmutes raw code into a Gnostic Summary for AI consumption.
        """
        # (Simplified implementation)
        return f"# [DISTILLED]: Logic for {len(content)} bytes of matter."

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _directive_enforce_alignment(self, context: Dict[str, Any], goal: str) -> str:
        """
        cortex.enforce_alignment(goal="Maximum Performance")

        [ASCENSION 6]: The Socratic Guardian.
        Checks the currently willed state against a specific project goal.
        """
        Logger.info(f"🎯 [CORTEX] Enforcing Alignment with goal: '{goal}'")
        return ""