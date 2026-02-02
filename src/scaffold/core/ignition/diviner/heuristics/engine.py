# Path: scaffold/core/ignition/diviner/heuristics/engine.py
# --------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_BAYESIAN_BRAIN_V1

from pathlib import Path
from typing import Dict, List, Tuple
from ...contracts import IgnitionAura
from .node_inquisitor import NodeInquisitor
from .python_inquisitor import PythonInquisitor
from .systems_inquisitor import SystemsInquisitor
from .visual_inquisitor import VisualInquisitor

class BayesianBrain:
    """
    =============================================================================
    == THE BAYESIAN BRAIN (V-Ω-TOTALITY-INFERENCE)                            ==
    =============================================================================
    Orchestrates specialized Inquisitors and sums their resonance to collapse
    the wave function into a single, definitive project Aura.
    """

    def __init__(self):
        self.inquisitors = [
            NodeInquisitor(),
            PythonInquisitor(),
            SystemsInquisitor(),
            VisualInquisitor()
        ]
        self.trace: List[str] = []

    def judge(self, root: Path) -> Tuple[IgnitionAura, float]:
        """
        The Grand Rite of Judgment.
        Weighting findings across all domains of Gnosis.
        """
        matrix: Dict[IgnitionAura, float] = {a: 0.0 for a in IgnitionAura}

        for inquisitor in self.inquisitors:
            try:
                aura, confidence, reasoning = inquisitor.analyze(root)
                if confidence > 0:
                    # Apply resonance to the global matrix
                    matrix[aura] += confidence
                    self.trace.extend(reasoning)
            except Exception as e:
                self.trace.append(f"Inquisitor Fracture ({type(inquisitor).__name__}): {str(e)}")

        # [ASCENSION 11]: COLLAPSE REALITY
        # Sort by total cumulative confidence
        ranked = sorted(matrix.items(), key=lambda x: x[1], reverse=True)
        winner, total_score = ranked[0]

        # [ASCENSION 10]: NORMALIZE CONFIDENCE
        # Final confidence is the winner's share of the total resonance
        final_confidence = min(0.99, total_score) if total_score > 0 else 0.1

        return winner, final_confidence