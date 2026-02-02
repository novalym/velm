# Path: artisans/holocron/engine.py
# ---------------------------------

import re
import time
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Any

from .graph import CallGraphOracle, CallNode
from .curator import AICurator
from .slicer import SurgicalSlicer
from .contracts import HolocronCandidate

# --- THE DIVINE SUMMONS ---
from ...core.cortex.engine import GnosticCortex
from ...core.semantics.retriever import SemanticRetriever
from ...core.semantics.contracts import UserIntent, QueryIntent
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("HolocronEngine")


class HolocronEngine:
    """
    =================================================================================
    == THE HOLOCRON MANTLE (V-Ω-FORENSIC-SINGULARITY-ULTIMA)                       ==
    =================================================================================
    LIF: INFINITY
    @auth_code: )#@()#(!!

    This is the final, ascended form of the Holocron's internal mind.
    It no longer "dumps code." It "conducts a forensic inquiry."
    """

    def __init__(self, root: Path, cortex: GnosticCortex):
        self.root = root
        self.cortex = cortex
        self.graph = CallGraphOracle(root)
        self.retriever = SemanticRetriever(root, vector_cortex=self.cortex.vector_cortex)
        self.curator = AICurator()
        self.ai = AIEngine.get_instance()

    def forge_virtual_context(self, intent_text: str, depth: int = 2) -> str:
        """The Grand Symphony of Forensic Perception."""
        t_start = time.monotonic()

        # --- MOVEMENT I: INTENT TRIAGE ---
        # We determine if the Architect is hunting a bug or building a feature.
        is_forensic = any(k in intent_text.lower() for k in ["bug", "error", "crash", "fix", "issue", "fails"])
        Logger.info(f"Holocron mode: {'[red]FORENSIC[/red]' if is_forensic else '[cyan]STRUCTURAL[/cyan]'}")

        # --- MOVEMENT II: THE SEEDING ---
        intent_obj = UserIntent(raw_query=intent_text)
        seeds = self.retriever.retrieve(intent_obj, limit=5)
        seed_paths = [s.path for s in seeds]

        # --- MOVEMENT III: CAUSAL TRACING ---
        # We gather the inventory from the Cortex Memory.
        inventory = self.cortex.perceive().inventory
        files = [self.root / i.path for i in inventory if i.category == 'code']

        self.graph.build_index(files)
        # We trace the impact to find the "Chain of Causality"
        graph_hits = self.graph.trace_impact(seed_paths, depth=depth)
        all_relevant_paths = set(seed_paths) | graph_hits

        # --- MOVEMENT IV: AI CURATION (The Filter of Wisdom) ---
        candidates = []
        for path in all_relevant_paths:
            gnosis = self.cortex.perceive().find_gnosis_by_path(Path(path))
            summary = f"Language: {gnosis.language if gnosis else 'unknown'} | Churn: {gnosis.churn_score if gnosis else 0}"
            candidates.append(HolocronCandidate(
                path=path,
                score=1.0 if path in seed_paths else 0.5,
                reason="Direct Intent" if path in seed_paths else "Causal Link",
                summary=summary
            ))

        selected_paths = self.curator.curate(intent_text, candidates)

        # --- MOVEMENT V: SURGICAL SLICING (The Extraction of the Soul) ---
        # If we are in forensic mode, we command the slicer to be conservative.
        # We want the WHOLE body of the functions on the causal path.
        keywords = re.findall(r'\w+', intent_text.lower())
        slicer = SurgicalSlicer(self.root, keywords)

        # [ASCENSION: FIDELITY TUNING]
        # In forensic mode, we don't just skeletonize; we preserve implementation.
        sliced_files = slicer.slice(selected_paths)

        # --- MOVEMENT VI: THE GNOSTIC NARRATIVE (The Final Synthesis) ---
        # We ask a 'fast' AI to summarize the interaction between these files.
        narrative = self._forge_narrative(intent_text, sliced_files)

        # --- MOVEMENT VII: ASSEMBLY OF THE DOSSIER ---
        dossier = [
            f"# 🏛️ HOLOCRON FORENSIC DOSSIER",
            f"# Intent: {intent_text}",
            f"# Mode: {'Forensic (Deep Gaze)' if is_forensic else 'Structural (Skeletal)'}",
            f"# Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## 🧠 ARCHITECTURAL HYPOTHESIS",
            narrative,
            "\n## 📜 RELEVANT SCRIPTURES"
        ]

        for path, content in sliced_files.items():
            gnosis = self.cortex.perceive().find_gnosis_by_path(Path(path))

            # [ASCENSION: TEMPORAL GNOSIS INJECTION]
            provenance = ""
            if gnosis:
                provenance = f"# [PROVENANCE] Author: {gnosis.author_count} souls | Last changed: {gnosis.days_since_last_change}d ago"

            dossier.append(f"### 📍 {path}")
            dossier.append(provenance)
            dossier.append(f"<!-- GNOSTIC_ANCHOR: {path} -->")
            dossier.append(f"```python\n{content}\n```\n")

        duration = time.monotonic() - t_start
        dossier.append(f"\n# --- Telemetry: Symphony concluded in {duration:.2f}s ---")

        return "\n".join(dossier)

    def _forge_narrative(self, intent: str, sliced_files: Dict[str, str]) -> str:
        """Summons the AI Scribe to explain the causal friction."""
        context_preview = ""
        for path, content in sliced_files.items():
            # Only give the first 50 lines per file to the AI to save tokens for the narrative
            lines = content.splitlines()[:50]
            context_preview += f"\nFile: {path}\n```python\n" + "\n".join(lines) + "\n```\n"

        prompt = f"""
        You are a Senior Gnostic Architect. I have performed a causal trace on a codebase.

        USER INTENT: "{intent}"

        CAUSAL SCRIPTURES:
        {context_preview}

        TASK:
        1. Briefly explain how these files interact regarding the user's intent.
        2. Identify the most likely "Friction Point" where a bug or architectural flaw exists.
        3. Keep your response dense, technical, and limited to 150 words.
        """

        try:
            return self.ai.ignite(
                user_query=prompt,
                system="You are the Voice of the Holocron. Provide absolute technical clarity.",
                model="fast"
            )
        except Exception as e:
            return f"The Narrative Scribe is silent (Paradox: {e}). Gaze upon the scriptures below."