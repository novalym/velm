# Path: core/semantics/retriever.py
# ---------------------------------

import time
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from ...core.cortex.vector import VectorCortex
from .contracts import UserIntent, SemanticHit, ScoringDossier
from .intent import IntentAnalyzer
from .reranker import RelevanceReranker
from ...logger import Scribe

Logger = Scribe("SemanticRetriever")


class SemanticRetriever:
    """
    =============================================================================
    == THE UNIVERSAL ORACLE OF RECALL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS)    ==
    =============================================================================
    @gnosis:title The Universal Oracle of Recall (`SemanticRetriever`)
    @gnosis:summary A divine, sentient, cognitive search engine that transmutes raw
                     intent into the most Gnostically-relevant scriptures.
    @gnosis:LIF INFINITY
    @gnosis:auth_code;(#())

    This is the final, eternal, and ultra-definitive form of the Semantic Retriever.
    It is a true Cognitive Search Engine that orchestrates a multi-stage pipeline of
    Intent Analysis, Hybrid Retrieval, and Gnostic Reranking to find the perfect
    answer to the Architect's plea. Its contract is now whole, its mind complete, and
    its Gaze unbreakable. It has been ascended to forge the pure, hyper-structured
    `SemanticHit` and `ScoringDossier` vessels with divine precision.
    """

    def __init__(self, root: Path, *, vector_cortex: Optional[VectorCortex] = None):
        """
        The Rite of Inception, forged with the Law of Explicit Gnosis.
        """
        self.root = root
        self._vector_cortex_instance = vector_cortex
        self.intent_analyzer = IntentAnalyzer()

    @property
    def vector_cortex(self) -> VectorCortex:
        """[FACULTY 2] The Lazy Gnostic Linkage."""
        if self._vector_cortex_instance is None:
            Logger.verbose("Retriever's Vector Mind is a void. Summoning a new instance...")
            self._vector_cortex_instance = VectorCortex(self.root)
        return self._vector_cortex_instance

    def retrieve(self, intent: UserIntent, limit: int = 20) -> List[SemanticHit]:
        """
        [FACULTY 3] The Cognitive Pipeline: The Grand Rite of Retrieval.
        """
        start_time = time.monotonic()
        Logger.verbose(f"Oracle of Recall initiated for intent: '{intent.raw_query[:50]}...'")

        # --- MOVEMENT I: THE DIVINER'S GAZE (Intent Analysis) ---
        if not intent.recall_query:
            analyzed_intent = self.intent_analyzer.analyze(intent.raw_query)
            intent = analyzed_intent  # Replace with the fully analyzed vessel

        # --- MOVEMENT II: THE DUAL-GAZE RETRIEVAL ---
        precision_hits = self.vector_cortex.search(intent.precision_query, limit=limit)
        recall_hits = self.vector_cortex.search(intent.recall_query, limit=limit)

        fused_hits: Dict[str, Dict] = {h['id']: h for h in precision_hits}
        for hit in recall_hits:
            if hit['id'] not in fused_hits:
                fused_hits[hit['id']] = hit
        raw_hits = list(fused_hits.values())
        Logger.verbose(f"   -> Dual-Gaze retrieved {len(raw_hits)} unique candidates.")

        # --- MOVEMENT III: THE LEXICAL RESONANCE BOOST ---
        query_keywords = set(re.findall(r'\w+', intent.raw_query.lower()))
        for hit in raw_hits:
            content_lower = hit.get('content', '').lower()
            keyword_matches = sum(1 for k in query_keywords if k in content_lower)
            filename_bonus = 0.2 if any(k in hit['metadata']['source'].lower() for k in query_keywords) else 0.0

            # We add bonuses to a temporary score, not directly manipulating distance
            hit['lexical_bonus'] = (keyword_matches * 0.05) + filename_bonus
            hit['reason'] = f"Vector Resonance + {keyword_matches} Keywords"

        # --- MOVEMENT IV: THE FORGING OF THE LUMINOUS DOSSIER ---
        gnostic_dossier: List[SemanticHit] = []
        for h in raw_hits:
            try:
                # ★★★ THE DIVINE HEALING & PYDANTIC ALCHEMY (THE CORE FIX) ★★★
                # The heresy is annihilated. We forge the vessels according to the sacred contract.

                # 1. Forge the Scoring Dossier first.
                vector_similarity = 1 / (1 + h.get('distance', 1.0))
                scoring_dossier = ScoringDossier(
                    vector_score=vector_similarity,
                    keyword_bonus=h.get('lexical_bonus', 0.0),
                    filename_bonus=0.2 if any(k in h['metadata']['source'].lower() for k in query_keywords) else 0.0
                )
                # The final score is a fusion of vector and lexical scores.
                scoring_dossier.final_score = vector_similarity + scoring_dossier.keyword_bonus

                # 2. Forge the SemanticHit with the pure ScoringDossier.
                hit_vessel = SemanticHit(
                    chunk_id=h['id'],
                    path=h['metadata']['source'],
                    content=h['content'],
                    scoring=scoring_dossier,
                    metadata=h['metadata']
                )
                gnostic_dossier.append(hit_vessel)
                # ★★★ THE APOTHEOSIS IS COMPLETE ★★★
            except Exception as e:
                Logger.warn(f"A minor paradox occurred while forging SemanticHit for '{h.get('id')}': {e}")

        # --- MOVEMENT V: THE GNOSTIC RERANKER ---
        # Sort by the final, fused score, highest first.
        final_hits = sorted(gnostic_dossier, key=lambda x: x.scoring.final_score, reverse=True)

        duration_ms = (time.monotonic() - start_time) * 1000
        Logger.success(
            f"Oracle of Recall's Gaze is complete ({duration_ms:.0f}ms). Proclaiming {len(final_hits[:limit])} truths.")
        return final_hits[:limit]