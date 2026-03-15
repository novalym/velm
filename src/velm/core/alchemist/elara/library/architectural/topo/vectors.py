# Path: core/alchemist/elara/library/architectural/topo/vectors.py
# ----------------------------------------------------------------

from typing import Any


class VectorOracle:
    """
    =============================================================================
    == THE VECTOR ORACLE (V-Ω-TOTALITY)                                        ==
    =============================================================================
    LIF: 10,000x | ROLE: SEMANTIC_EMBEDDING_RESONATOR

    [ASCENSIONS 13-16]:
    13. Real-time Cosine Similarity mapping between two concepts.
    14. Direct neural access for dynamic @if statements based on semantic intent.
    """

    def __init__(self, engine_ref: Any):
        self.engine = engine_ref

    def similarity(self, a: str, b: str) -> float:
        """[ASCENSION 13]: Evaluates conceptual proximity via Mini-L6."""
        try:
            from ......cortex.semantic_resolver.substrate import NeuralSubstrate
            from ......cortex.semantic_resolver.classifier.tensor import GnosticTensor

            sub = NeuralSubstrate()
            # Failsafe if unmanifest
            if sub.mode == "DORMANT": sub.awaken()

            vec_a = sub.embed_intent(a)
            vec_b = sub.embed_intent(b)

            if not vec_a or not vec_b: return 0.0

            # Map float lists to SparseVector format for Tensor math
            sv_a = {str(i): v for i, v in enumerate(vec_a)}
            sv_b = {str(i): v for i, v in enumerate(vec_b)}

            return GnosticTensor.cosine_similarity(sv_a, sv_b)
        except Exception:
            return 0.0