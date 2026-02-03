# Path: scaffold/artisans/distill/core/semantics/reranker.py
# ----------------------------------------------------------

from typing import List, Dict, Any
from .contracts import UserIntent, SemanticHit, QueryIntent
from ...core.cortex.contracts import CortexMemory, FileGnosis


class RelevanceReranker:
    """
    =============================================================================
    == THE JUDGE OF RELEVANCE (V-Ω-INTENT-DRIVEN-GNOSIS)                       ==
    =============================================================================
    LIF: 100,000,000,000,000

    The Second Gaze. This artisan does not just find; it **understands**. It takes
    the raw memories from the Retriever and re-ranks them based on a multi-vector
    analysis of the Architect's true intent and the project's living soul.
    """

    def __init__(self, memory: CortexMemory):
        self.memory = memory

    def rank(self, hits: List[SemanticHit], intent: UserIntent) -> List[SemanticHit]:
        """The Rite of Judgment."""
        if not hits:
            return []

        for hit in hits:
            gnosis = self.memory.find_gnosis_by_path(hit.path)
            if not gnosis:
                continue

            # --- THE MULTI-VECTOR ANALYSIS ---

            # 1. Intent Alignment Boost
            self._apply_intent_boost(hit, intent, gnosis)

            # 2. Entity Match Boost (Lexical Precision)
            self._apply_entity_boost(hit, intent)

            # 3. Temporal Boost (Recency & Churn)
            self._apply_temporal_boost(hit, gnosis)

            # 4. Centrality Boost (Architectural Importance)
            self._apply_centrality_boost(hit, gnosis)

        # Final sort by the new, intelligent score
        return sorted(hits, key=lambda h: h.final_score, reverse=True)

    def _apply_intent_boost(self, hit: SemanticHit, intent: UserIntent, gnosis: FileGnosis):
        """Boosts based on the 'why' of the query."""
        if intent.intent == QueryIntent.REFACTORING:
            # For bug fixes, recent, churny, complex code is more likely relevant.
            if gnosis.days_since_last_change is not None and gnosis.days_since_last_change < 30:
                hit.final_score *= 1.2
                hit.rerank_reasons.append("Boost: High Recency")
            if gnosis.churn_score > 50:
                hit.final_score *= 1.15
                hit.rerank_reasons.append("Boost: High Churn")

        elif intent.intent == QueryIntent.TESTING:
            # Boost test files
            if "test" in hit.path.lower():
                hit.final_score *= 1.5
                hit.rerank_reasons.append("Boost: Test File Alignment")
            else:
                # Penalize non-test files
                hit.final_score *= 0.8

    def _apply_entity_boost(self, hit: SemanticHit, intent: UserIntent):
        """Boosts for exact matches of filenames or symbols."""
        for entity in intent.entities:
            # Boost for matching the filename directly
            if entity.lower() in hit.path.lower():
                hit.final_score *= 1.4
                hit.rerank_reasons.append(f"Boost: Entity Match ({entity})")
            # Boost for matching content within the fragment
            if entity in hit.content_fragment:
                hit.final_score *= 1.2
                hit.rerank_reasons.append(f"Boost: Content Match ({entity})")

    def _apply_temporal_boost(self, hit: SemanticHit, gnosis: FileGnosis):
        """General boost for recently modified files."""
        if gnosis.days_since_last_change is not None and gnosis.days_since_last_change < 14:
            hit.final_score *= 1.1
            hit.rerank_reasons.append("Boost: Recency (<14 days)")

    def _apply_centrality_boost(self, hit: SemanticHit, gnosis: FileGnosis):
        """Boosts architecturally important files."""
        # The ranker already calculated this, we use its score.
        centrality = gnosis.centrality_score
        if centrality > 80:
            hit.final_score *= 1.2
            hit.rerank_reasons.append(f"Boost: High Centrality ({centrality:.0f})")