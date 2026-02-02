# Path: scaffold/artisans/distill/core/causality/engine.py
# --------------------------------------------------------

from pathlib import Path
from typing import Dict, List, Any

from .....core.cortex.contracts import CortexMemory
from .....logger import Scribe
from .contracts import CausalityProfile, ImpactReport
from .graph_walker import GraphWalker

Logger = Scribe("CausalEngine")


class CausalEngine:
    """
    =================================================================================
    == THE CAUSAL ENGINE (V-Ω-FACADE-ULTIMA)                                       ==
    =================================================================================
    LIF: ∞

    The Sovereign Interface for Causal Analysis. It acts as the bridge between
    the Oracle (who asks "What is related?") and the GraphWalker (who calculates
    the physics of the web).
    """

    def __init__(self, root: Path, silent: bool = False):
        self.root = root
        self.silent = silent

    def calculate_impact(
            self,
            memory: CortexMemory,
            seeds: List[str],
            current_scores: Dict[str, int],
            profile: CausalityProfile = None
    ) -> Dict[str, int]:
        """
        [THE RITE OF IMPACT]
        Propagates relevance from Seed files to their dependencies and dependents.
        Returns the updated scores map (merged with input).
        """
        if not seeds:
            return current_scores

        # 1. Forge the Physics Profile
        # If none provided, use the default laws of the universe.
        active_profile = profile or CausalityProfile()

        if not self.silent:
            Logger.info(f"Causal Engine: Awakening GraphWalker for {len(seeds)} seed(s)...")

        # 2. Summon the Walker
        walker = GraphWalker(memory, active_profile)

        # 3. Execute the Walk
        # We perform the walk. The walker handles max-pooling and decay.
        report = walker.walk(seeds, current_scores)

        # 4. Merge Results
        # We respect the highest score found (either pre-existing or newly calculated).
        final_scores = current_scores.copy()
        for path, new_score in report.scores.items():
            if path in final_scores:
                final_scores[path] = max(final_scores[path], new_score)
            else:
                final_scores[path] = new_score

        if not self.silent:
            Logger.success(
                f"Causal Engine: Analysis Complete.\n"
                f"   • Nodes Touched: {report.visited_count}\n"
                f"   • Depth Reached: {report.max_depth_reached}\n"
                f"   • Hubs Dampened: {len(report.hubs_encountered)}"
            )

        return final_scores