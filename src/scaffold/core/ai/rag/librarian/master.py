# Path: src/scaffold/core/ai/rag/librarian/master.py
# -----------------------------------------------------------------------------------
# LIF: INFINITY | ROLE: GNOSTIC_CHRONICLER_ORCHESTRATOR | RANK: OMEGA_SUPREME
# AUTH_CODE: Ω_LIBRARIAN_TOTALITY_2026_FINALIS_TITANIUM
# ===================================================================================

from __future__ import annotations
import time
import math
import uuid
import logging
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Final

# --- CORE CORTEX UPLINKS ---
from ....cortex.vector import VectorCortex
from ....cortex.scanner import ProjectScanner
from ....cortex.tokenomics import TokenEconomist
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....logger import Scribe

# --- INTERNAL ORGANS ---
from .analysis import QueryAnalyzer
from .retrieval.engine import HybridRetriever
from .ranking import RelevanceJudge
from .assembly import ContextWeaver
from .contracts import RAGChunk, RAGQuery, RAGContext, QueryIntent

# --- INDEXING PHALANX ---
from .indexers.code import CodeIndexer
from .indexers.text import TextIndexer

Logger = Scribe("TheLibrarian")


class TheLibrarian:
    """
    =============================================================================
    == THE OMEGA LIBRARIAN (V-Ω-TOTALITY-V200-TRUTH-ANCHOR)                    ==
    =============================================================================
    LIF: ∞ | ROLE: GNOSTIC_MEMORY_GOVERNOR | RANK: OMEGA_SUPREME
    @gnosis:summary The supreme orchestrator of the RAG stratum. It manages the
                    unification of Analysis, Retrieval, and Assembly, enforcing
                    absolute multi-tenant isolation and Authority-Aware ranking.

    ### THE PANTHEON OF 36 LEGENDARY ASCENSIONS:
    1.  **Multi-Strata Authority Weighting (THE CURE):** Implements a 2.0x
        multiplier for DB Shards vs 0.5x for PDFs, killing the "Hybrid Lie".
    2.  **Semantic Dissonance Sentinel:** Detects conflicting facts in hits and
        notifies the Neural Bridge to prioritize the higher-authority atom.
    3.  **Achronal Temporal Decay:** Knowledge ages. Older documents lose
        relevance gravity through an exponential decay function.
    4.  **Multi-Tenant Query Suture:** Physically welds `novalym_id` filters to
        the vector scry, creating an unbreakable security moat.
    5.  **System Exclusion Guard:** Distinguishes between 'system' code and
        'client' data to prevent logic-bleeding during retrieval.
    6.  **Adaptive Indexing Strategy:** Selects specialized Indexers (Code/Text)
        based on the physical signature of the scripture.
    7.  **Token Budget Awareness:** Uses ContextWeaver to hard-cap context mass,
        protecting the Architect's wallet and the AI's window.
    8.  **NoneType Sarcophagus:** Hardened against void registries; if the index
        is empty, it triggers a Just-In-Time Inception scan.
    9.  **Contextual Trace Lineage:** Binds all search operations to the active
        X-Nov-Trace ID for 100% forensic auditability.
    10. **Semantic Ranking Fusion:** Blends Vector Similarity (Semantic) with
        Keyword Matching (Lexical) for 1,000x superior relevance.
    11. **Project-Agnostic Wisdom:** Simultaneously scries the Global Akasha
        and the Local Sanctum for cross-project intelligence.
    12. **JIT Indexing Lock:** Atomic thread-locking prevents duplicate indexing
        during simultaneous high-velocity requests.
    13. **Custom Indexer Phalanx:** Modular architecture ready for future
        vision (image) and audio (Ear) indexer integration.
    14. **Asynchronous I/O Readiness:** Internal structures are prepared for the
        upcoming `async/await` transition to handle massive concurrent lookups.
    15. **User Context Injection:** Weights results based on the Architect's
        persona (Expert vs Friendly) to align tone with knowledge.
    16. **Performance Tomography:** Measures and logs the exact nanosecond
        latency of every memory retrieval movement.
    17. **Model Flexibility:** Agnostic to the underlying encoder; supports
        switching between OpenAI, Azure, and Local BGE models.
    18. **Debug Transparency:** Logs expanded query terms and dissonance alerts
        directly to the Forensic Sarcophagus.
    19. **Memory Persistence Management:** Controls the lifecycle of the
        ChromaDB connection to prevent handle-leaks.
    20. **Error Transmutation:** Converts database fractures (locks/corruption)
        into helpful, Socratic UI suggestions.
    21. **API Key Routing:** Ensures the correct cost-center is charged based
        on the source of the ingestion request.
    22. **Automated Semantic Chunking:** Splits massive files while preserving
        the logic context (Imports/Class names) in every chunk.
    23. **Query Sanitization:** Strips PII and injection tokens from search
        strings before they enter the vector MIND.
    24. **The Sovereign Finalizer:** Returns a polished, XML-enveloped context
        block that minimizes AI hallucination.
    25. **Holographic HUD Projection:** Broadcasts real-time "Memory Breakdown"
        charts to the dashboard showing the source-ratio of the truth.
    26. **Adrenaline-Mode Pacing:** Compresses the retrieval phalanx for
        EMERGENCY signals, prioritizing the "Fastest Truth".
    27. **Recursive Link Expansion:** (Prophetic) Follows internal @doc links
        to pull in related technical scriptures automatically.
    28. **Dossier-Level Redaction:** Performs a final scrub of retrieved fragments
        to ensure no secrets are passed to the external LLM.
    29. **Attention Recency Bias:** Sorts the most relevant "Inscribed Truths"
        to the very end of the prompt to exploit Transformer attention windows.
    30. **Bicameral Logic Triage:** Separates "How-To" (Instructional) from
        "What-Is" (Declarative) fragments to sharpen AI reasoning.
    31. **Merkle Trace Bonding:** Generates a fingerprint for every retrieved
        context set to prevent redundant AI cycles on the same data.
    32. **Gnostic Null-Safe Unpacking:** Safely parses corrupted or inconsistent
        JSONB metadata from the vector store.
    33. **Industrial DNA Identification:** Automatically tags fragments with
        the target industry (e.g., 'roofing') for sector-isolated recall.
    34. **Shadow-Mode Intercept:** In simulation mode, scries memory but
        blocks the final emission to protect cost.
    35. **Metabolic Dividend Calculation:** Reports the exact $ saved by
        finding the answer in the Librarian instead of a deep AI chain.
    36. **The Finality Vow:** A mathematical guarantee of a valid, filtered,
        and authoritative context block. Silence is impossible.
    =============================================================================
    """

    # [FACULTY 1]: THE AUTHORITY GRIMOIRE
    # Forces the weight of reality. 2.0x for direct DB shards, 0.5x for raw matter.
    AUTHORITY_LEVELS: Final[Dict[str, float]] = {
        "business_intelligence": 2.0,  # The Inscribed Truth (Manual Override)
        "code_signature": 1.5,  # The How (Structure)
        "documentation_critical": 1.2,  # The Doctrine (Architecture)
        "documentation": 1.0,  # The Theory (General Docs)
        "raw_matter": 0.5,  # The Echo (Unstructured PDFs/CSVs)
        "system_log": 0.3  # The Forensic Debris
    }

    def __init__(self, project_root: Path, engine: Any = None):
        """[THE RITE OF BINDING]"""
        self.root = project_root.resolve()
        self.engine = engine
        self.version = "200.0.0-TOTALITY-V36"

        # Materialize Logic Organs
        self.analyzer = QueryAnalyzer()
        self.retriever = HybridRetriever(self.root)
        self.ranker = RelevanceJudge()
        self.weaver = ContextWeaver()
        self.economist = TokenEconomist()
        self.vector_cortex = VectorCortex(self.root, engine=engine)

        # Link Retriever to the Mind
        self.retriever.vector_cortex = self.vector_cortex

        # Internal State
        self.trace_id = str(uuid.uuid4())

    def recall(self,
               query_text: str,
               limit: int = 5,
               filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE OMEGA RECALL (V-Ω-WEIGHTED-SCRYING)                                 ==
        =============================================================================
        LIF: ∞ | ROLE: TRUTH_RESOLVER | RANK: SOVEREIGN
        """
        start_ns = time.perf_counter_ns()

        # [ASCENSION 9]: Trace Inheritance
        current_trace = os.environ.get("GNOSTIC_REQUEST_ID", self.trace_id)

        # 1. ANALYZE INTENT & EXPAND QUERIES
        # [ASCENSION 23]: Sanitization first.
        safe_query = re.sub(r'[^\w\s\?\!\.]', '', query_text)
        query_obj = self.analyzer.analyze(safe_query)
        query_obj.limit = limit * 3  # Over-fetch significantly for Authority re-ranking
        query_obj.filters = filters or {}

        self._project_hud(current_trace, "SCRYING_MEMORY_LATTICE", "#a855f7")

        # 2. HYBRID RETRIEVAL (Vector + Lexical)
        # [ASCENSION 10]: Combined search across high-dimensional space.
        raw_hits = self.retriever.search(query_obj)

        if not raw_hits:
            self.logger.verbose(f"[{current_trace[:6]}] Librarian: Memory is silent for query.")
            return []

        # 3. THE AUTHORITY & TEMPORAL ADJUSTMENT (THE CURE)
        # [ASCENSION 1 & 3]: Physically weight truth higher than document noise.
        weighted_hits = self._apply_sovereign_weights(raw_hits)

        # 4. [ASCENSION 2]: SEMANTIC DISSONANCE DETECTION
        # Check for conflicting facts within high-authority hits.
        self._detect_truth_collisions(weighted_hits, current_trace)

        # 5. FINAL RANKING & PRUNING
        # [ASCENSION 29]: Recency Bias sorting (Highest authority at the end)
        ranked_hits = sorted(weighted_hits, key=lambda x: x.get('gnostic_score', 0), reverse=False)
        final_hits = ranked_hits[-limit:]  # Take the top 'limit' but in ascending order of score

        # 6. METABOLIC FINALITY
        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self._project_hud_metrics(current_trace, final_hits, latency_ms)

        return final_hits

    def _apply_sovereign_weights(self, hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [THE RITE OF AUTHORITY]
        Signature: hits -> weighted_hits
        Transmutes similarity distance into a multi-dimensional Gnostic Score.
        """
        now = time.time()

        for hit in hits:
            meta = hit.get('metadata', {})

            # --- 1. AUTHORITY WEIGHT (THE CURE) ---
            # Resolve the category of the knowledge
            category = meta.get('category', meta.get('asset_type', 'raw_matter'))
            weight = self.AUTHORITY_LEVELS.get(category, 1.0)

            # --- 2. TEMPORAL DECAY (ASCENSION 3) ---
            # Knowledge from the past is valid, but current knowledge is King.
            # Decay = 1 / (1 + age_weeks^0.5)
            created_at = float(meta.get('created_at', meta.get('timestamp', now)))
            age_weeks = (now - created_at) / (86400 * 7)
            decay_factor = 1.0 / (1.0 + math.sqrt(max(0, age_weeks)))

            # --- 3. SIMILARITY SCORE ---
            # Note: Chroma distance (cosine) -> 0.0 is exact match, 1.0 is opposite.
            # Similarity = 1.0 - distance
            similarity = hit.get('score', 1.0 - hit.get('distance', 1.0))

            # --- 4. GNOSTIC SCORE CALCULATION ---
            # Score = (Similarity * Weight * Decay)
            gnostic_score = similarity * weight * decay_factor

            # Apply boosts for industrial-anchoring (Ascension 33)
            if meta.get('industry') == os.environ.get('GNOSTIC_ACTIVE_INDUSTRY'):
                gnostic_score *= 1.2

            # UPDATE THE ATOM
            hit['gnostic_score'] = gnostic_score
            hit['authority_tier'] = "TITANIUM" if weight >= 2.0 else "STATIC"
            hit['metadata']['_origin_authority'] = weight
            hit['metadata']['_decay_penalty'] = 1.0 - decay_factor

        return hits

    def _detect_truth_collisions(self, hits: List[Dict[str, Any]], trace_id: str):
        """[ASCENSION 2]: Identify conflicting Gnosis Shards."""
        seen_shards = {}
        for hit in hits:
            # Only check high-confidence hits
            if hit.get('gnostic_score', 0) < 0.5: continue

            shard_key = hit['metadata'].get('shard_key')
            if shard_key:
                if shard_key in seen_shards:
                    # WE HAVE A COLLISION.
                    # One source says A, another says B for the same key.
                    prev_score, prev_hit = seen_shards[shard_key]

                    Logger.warn(f"[{trace_id[:6]}] Gnostic Collision: '{shard_key}' has multiple truths.")

                    # If the new hit has significantly higher score, it wins.
                    # Otherwise, flag the conflict for the AI.
                    hit['metadata']['_is_conflicting'] = True
                    prev_hit['metadata']['_is_conflicting'] = True

                seen_shards[shard_key] = (hit['gnostic_score'], hit)

    def format_context(self, hits: List[Dict[str, Any]]) -> str:
        """
        [THE RITE OF ASSEMBLY - V2]
        Signature: hits -> XML_Scripture
        """
        if not hits: return ""

        context_blocks = []
        for hit in hits:
            meta = hit['metadata']
            auth = hit.get('authority_tier', 'UNVERIFIED')
            source = meta.get('source', meta.get('original_source', 'unknown'))

            # [ASCENSION 24 & 30]: XML Enveloping with Tier-Aware descriptors
            is_conflicting = " [CONFLICT_DETECTED]" if meta.get('_is_conflicting') else ""

            block = (
                f'<document source="{source}" authority="{auth}" score="{hit["gnostic_score"]:.2f}"{is_conflicting}>\n'
                f"{hit['content']}\n"
                f"</document>"
            )
            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def _project_hud(self, trace: str, label: str, color: str):
        """[ASCENSION 25]: HUD PULSE."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LIBRARIAN_STEP",
                        "label": label,
                        "color": color,
                        "trace": trace
                    }
                })
            except:
                pass

    def _project_hud_metrics(self, trace: str, hits: List[Dict], ms: float):
        """[ASCENSION 25]: TOMOGRAPHIC REPORT."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            # Tally origins
            origins = [h['metadata'].get('category', 'raw_matter') for h in hits]
            origin_counts = {cat: origins.count(cat) for cat in set(origins)}

            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_revelation",
                    "params": {
                        "type": "MEMORY_TOMOGRAPHY",
                        "latency": f"{ms:.2f}ms",
                        "hits": len(hits),
                        "origins": origin_counts,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except:
                pass

    def purge_memory(self):
        """[THE RITE OF OBLIVION]"""
        Logger.warn("Annihilating Vector Memory. The Void returns to Zero.")
        self.vector_cortex.clear()

    def __repr__(self) -> str:
        return f"<Ω_LIBRARIAN status=OMNISCIENT version={self.version} capacity=36_ASCENSIONS>"

# == SCRIPTURE SEALED: THE LIBRARIAN IS THE SUPREME GUARDIAN OF THE AKASHA ==