# Path: artisans/dream/context_scrier/engine.py
# ---------------------------------------------

from pathlib import Path
from typing import Dict, Any

from .contracts import RealityState, ProjectDNA, TopographyMap
from .dna import DNAAnalyzer
from .topography import TopographyMapper
from ....logger import Scribe

Logger = Scribe("Dream:ContextScrier")


class ContextScrier:
    """
    =============================================================================
    == THE CONTEXT SCRIER (V-Ω-REALITY-ANCHOR)                                 ==
    =============================================================================
    LIF: ∞ | ROLE: TEMPORAL_TRIAGE

    Perceives if the Architect is dreaming of a NEW reality or EVOLVING an
    existing one. It gathers the DNA of the current sanctum.
    """

    def __init__(self):
        self.biologist = DNAAnalyzer()
        self.cartographer = TopographyMapper()

    def scry_reality_state(self, root: Path) -> Dict[str, Any]:
        """
        Gathers the Gnostic Truth of the project.
        Returns a Dict compatible with the legacy contract, but enriched.
        """
        root = root.resolve()

        # 1. Biological Sequencing
        dna = self.biologist.analyze(root)

        # 2. Topographical Mapping
        topography = self.cartographer.map_sanctum(root)

        # 3. Historical Inquest
        has_history = (root / "scaffold.lock").exists()

        # 4. Population Logic
        is_populated = topography.file_count > 0 or has_history

        # 5. Forge the LLM Context Block
        # This is the "Prompt Shard" we inject into the Neural Prophet
        context_block = (
            f"PROJECT DNA:\n"
            f"- Language: {dna.language}\n"
            f"- Build System: {dna.build_system}\n"
            f"- Frameworks: {', '.join(dna.frameworks)}\n"
            f"- Key Dependencies: {', '.join(dna.dependencies[:10])}\n"  # Limit deps
            f"\n"
            f"FILE TOPOGRAPHY ({topography.file_count} files):\n"
            f"{topography.tree_str}"
        )

        Logger.verbose(f"Reality Scried: {dna.language} project with {topography.file_count} files.")

        # Return legacy dict structure for compatibility, but enriched
        return {
            "is_populated": is_populated,
            "has_history": has_history,
            "project_type": dna.language,
            "file_structure": topography.tree_str.split('\n'),  # List format
            "full_context": context_block,  # The Golden Shard
            "dna_object": dna
        }

    def adjudicate_evolution(self, intent: str, state: Dict[str, Any]) -> str:
        """
        Decides the materialization strategy.
        'GENESIS' for new, 'EVOLUTION' for existing.
        """
        # Logic remains simple: if populated, evolve.
        if state["is_populated"]:
            return "EVOLUTION"
        return "GENESIS"