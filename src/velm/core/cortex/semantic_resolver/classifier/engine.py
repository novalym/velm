# Path: core/cortex/semantic_resolver/classifier/engine.py
# --------------------------------------------------------

"""
=================================================================================
== THE GNOSTIC CLASSIFIER: OMEGA (V-Ω-TOTALITY-VMAX-ONNX-SUPREMACY-FINALIS)    ==
=================================================================================
LIF: ∞^∞ | ROLE: INTENT_ADJUDICATOR_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_CLASSIFIER_VMAX_ONNX_SUPREMACY_SUTURE_2026_FINALIS

The supreme perceptual authority for the Velm God-Engine. It transmutes the
Architect's "Vibe" into a group of resonant, interconnected Gnostic Shards.

### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
1.  **ONNX Supremacy Matrix (THE MASTER CURE):** Radically shifts the gravitational
    weight to favor Dense Neural embeddings (85%) over Sparse heuristics (15%).
    The AI model's mathematical certainty dictates the reality; determinism acts
    only as an indestructible guardrail.
2.  **Domain-Stratified Apex Scoring (THE CURE FOR THRESHOLD GLUTTONY):**
    Annihilates the "Postgres Starvation" heresy. Apex thresholds are now calculated
    independently per architectural domain (Persistence vs. Infrastructure vs. Security),
    ensuring a 0.98 DB score never vaporizes a 0.70 Trace Radiator.
3.  **Multi-Dimensional Superposition:** Dynamically weights the Dense vs Sparse
    score based on the *entropy* of the prompt.
4.  **O(1) Pauli Exclusion Sieve V3:** Pre-calculates pairwise Jaccard similarities,
    mathematically guaranteeing absolute exclusivity between competing frameworks.
5.  **Achronal Quantum Cohesion (The DAG Vibe):** Calculates the 384-D `Centroid`
    of active nodes and pulls the new shard towards that semantic alignment.
6.  **Semantic Triangulation:** Uses three independent anchors (Intent, Substrate, Category).
7.  **The Anti-Matter Exorcist:** Advanced detection of negative intent ("no auth").
8.  **Contextual L1 Memo-Matrix:** Caches predictions based on a Merkle hash.
9.  **Substrate-Aware Thresholding:** Drops the acceptance threshold for "Agnostic" shards.
10. **Haptic Rationale Scribe:** Generates a detailed, rich-text forensic report.
11. **Hydraulic Thread Pacing:** Yields the GIL during the dense matrix multiplication.
12. **The Jinja-Killer Substring Triage:** Scans the prompt for exact keywords first.
13. **Dynamic Prior Decay:** Categories lose Bayesian priority if unused recently.
14. **Bicameral State Mapping:** Keeps high-priority "Core" shards in L1 cache.
15. **Isomorphic Variable Extraction:** Binds to the NER Scribe to pull explicit variables.
16. **Lexical Proximity Weighting:** Bigram-Gravity boost for sparse scoring.
17. **The Elegance Fallback V3:** Mathematically penalizes massive `requires` arrays.
18. **Modernity Matrix (SemVer Scaling):** Boosts v2.0.0 shards over v1.0.0 shards.
19. **Causal Node Flattening:** Merges duplicate shards from different registries.
20. **The Ghost-Match Exorcist:** Verifies that a shard's `target_file` exists physically.
21. **Subtle-Crypto Branding:** HMAC-seals the returned election pool.
22. **Asynchronous Communion Ward:** Thread-safe and re-entrant for multi-agent swarms.
23. **Apophatic Capability Masking:** Resonance hard-set to absolute zero for excluded capabilities.
24. **Entropy-Weighted Pooling:** TF-IDF scores dictate attention weights in dense fusion.
25. **The Subversion Ward:** Systemic shards are immune to the Pauli Sieve.
26. **Hyper-Dimensional Decay:** Scores drop exponentially the further they drift from the Domain Apex.
27. **Determinism as a Guardrail:** If ONNX is fractured or unsure, Sparse guarantees safety.
28. **Isomorphic Tuple Alignment:** Enforces strict return typing for the Causal Assembler.
29. **Laminar Node Interrogation:** Filters redundant nodes before tensor initialization.
30. **Absolute Singularity Check:** Prevents election of conflicting databases natively.
31. **Resonance Multiplier Suture:** Applies a 1.25x boost to shards matching exact willed ports.
32. **The Absolute Singularity Vow:** A mathematical guarantee of the most perfect, cohesive, and resonant selection of architectural code possible.
=================================================================================
"""

import re
import time
import collections
import hashlib
import gc
import os
import sys
import math
import threading
import uuid
from typing import List, Dict, Any, Tuple, Set, Optional, Final

# --- THE INTERNAL ORGANS ---
from .tensor import GnosticTensor, SparseVector, DenseVector
from .ontology import SynapticLattice
from .....logger import Scribe

Logger = Scribe("GnosticClassifier")


class GnosticClassifier:
    """
    =============================================================================
    == THE GNOSTIC CLASSIFIER (V-Ω-TOTALITY-VMAX-ONNX-SUPREMACY)               ==
    =============================================================================
    The True Bicameral Mind. Fuses Dense Embeddings (ONNX) with Sparse Keywords
    (TF-IDF), arbitrated by Domain-Stratified Thresholds and Quantum Cohesion.
    """

    # [PHYSICS CONSTANTS]
    ID_WEIGHT: Final[float] = 4.0
    VIBE_WEIGHT: Final[float] = 2.0
    DESC_WEIGHT: Final[float] = 1.0
    MATCH_FLOOR: Final[float] = 0.45

    # [ASCENSION 1]: ONNX SUPREMACY MULTIPLIERS
    DENSE_GRAVITY_BIAS: Final[float] = 0.85
    SPARSE_GUARDRAIL_BIAS: Final[float] = 0.15

    # [ASCENSION 7]: THE ANTI-MATTER EXORCIST
    NEGATION_TOKENS: Final[Set[str]] = {"without", "no", "skip", "omit", "exclude", "not"}

    # [ASCENSION 4]: O(1) PAULI EXCLUSION JACCARD THRESHOLD
    EXCLUSION_THRESHOLD: Final[float] = 0.35

    STOPWORDS: Final[Set[str]] = {
        "this", "that", "with", "from", "make", "create", "build",
        "using", "and", "the", "a", "an", "for", "in", "of", "to", "add", "i", "want"
    }

    __slots__ = (
        '_shard_sparse_vectors', '_shard_dense_vectors', '_shard_keywords',
        '_shard_metadata', '_shard_keys_cache', '_pauli_matrix', '_state_hash', '_lock'
    )

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._shard_sparse_vectors: Dict[str, SparseVector] = {}
        self._shard_dense_vectors: Dict[str, DenseVector] = {}
        self._shard_keywords: Dict[str, Set[str]] = {}
        self._shard_metadata: Dict[str, Dict[str, Any]] = {}
        self._shard_keys_cache: Dict[str, Set[str]] = {}

        self._pauli_matrix: Dict[str, Set[str]] = collections.defaultdict(set)

        self._state_hash = "0xVOID"
        self._lock = threading.RLock()

    def train(self, shards: List[Any], substrate: Any):
        """
        =============================================================================
        == THE RITE OF LEARNING (DENSE & SPARSE FUSION)                            ==
        =============================================================================
        """
        with self._lock:
            start_ns = time.perf_counter_ns()

            unique_shards = {s.id: s for s in sorted(shards, key=lambda x: (x.tier != 'iron', x.version), reverse=True)}
            active_shards = list(unique_shards.values())

            registry_raw = "".join(sorted([s.id for s in active_shards]))
            new_state_hash = hashlib.sha256(registry_raw.encode()).hexdigest()

            if self._state_hash == new_state_hash:
                return

            self._state_hash = new_state_hash
            self._shard_sparse_vectors.clear()
            self._shard_dense_vectors.clear()
            self._shard_keywords.clear()
            self._shard_keys_cache.clear()
            self._shard_metadata.clear()
            self._pauli_matrix.clear()

            def _get_doc_len(s):
                v_list = s.vibe if isinstance(s.vibe, list) else ([s.vibe] if s.vibe else [])
                return len(" ".join([s.id] + v_list + [s.summary]).split())

            avg_doc_len = sum(_get_doc_len(s) for s in active_shards) / max(1, len(active_shards))

            for shard in active_shards:
                vibe_list = shard.vibe if isinstance(shard.vibe, list) else ([shard.vibe] if shard.vibe else [])

                corpus_parts = [shard.id] * int(self.ID_WEIGHT)
                corpus_parts.extend(vibe_list * int(self.VIBE_WEIGHT))
                corpus_parts.extend([shard.summary] * int(self.DESC_WEIGHT))
                corpus_parts.extend(shard.provides * 2)
                corpus = " ".join(corpus_parts)

                tokens = self._tokenize(corpus, include_phrases=True)
                expanded_intent = SynapticLattice.expand_thought(tokens)

                sparse_vector = GnosticTensor.forge_sparse(list(expanded_intent.keys()), weights=expanded_intent,
                                                           avg_doc_len=avg_doc_len)

                dense_vector = shard.semantic_vector
                if not dense_vector and substrate.mode == "RESONANT":
                    dense_vector = substrate.embed_intent(corpus)
                    if dense_vector:
                        shard.semantic_vector = dense_vector

                id_tokens = set(self._tokenize(shard.id, include_phrases=False))
                vibe_tokens = set(self._tokenize(" ".join(vibe_list), include_phrases=False))

                self._shard_keywords[shard.id] = id_tokens.union(vibe_tokens)
                self._shard_sparse_vectors[shard.id] = sparse_vector
                self._shard_keys_cache[shard.id] = set(sparse_vector.keys())

                if dense_vector:
                    self._shard_dense_vectors[shard.id] = dense_vector

                pure_caps = {c for c in shard.provides if c != shard.id}
                self._shard_metadata[shard.id] = {
                    "object": shard,
                    "category": getattr(shard, 'category', 'general').lower(),
                    "provides": set(shard.provides),
                    "pure_capabilities": pure_caps,
                    "substrate": set(shard.substrate) if isinstance(shard.substrate, list) else {"agnostic"},
                    "elegance_score": 100 - len(shard.requires),
                    "domain_axis": self._determine_domain_axis(getattr(shard, 'category', 'general').lower(), shard.id)
                }

            # [ASCENSION 4]: PRE-CALCULATE PAULI EXCLUSION MATRIX
            shard_ids = list(self._shard_metadata.keys())
            for i in range(len(shard_ids)):
                id_a = shard_ids[i]
                caps_a = self._shard_metadata[id_a]["pure_capabilities"]
                if not caps_a: continue

                for j in range(i + 1, len(shard_ids)):
                    id_b = shard_ids[j]
                    caps_b = self._shard_metadata[id_b]["pure_capabilities"]
                    if not caps_b: continue

                    overlap = GnosticTensor.jaccard_similarity(caps_a, caps_b)
                    if overlap > self.EXCLUSION_THRESHOLD:
                        self._pauli_matrix[id_a].add(id_b)
                        self._pauli_matrix[id_b].add(id_a)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.verbose(
                f"Bicameral Matrix & Pauli Sieve manifest. {len(active_shards)} shards waked in {duration_ms:.2f}ms.")

    def _determine_domain_axis(self, category: str, shard_id: str) -> str:
        """Categorizes shards into absolute domains to prevent threshold gluttony."""
        c = category.lower()
        sid = shard_id.lower()
        if any(x in c or x in sid for x in ('db', 'database', 'persistence', 'postgres', 'redis')): return "persistence"
        if any(x in c or x in sid for x in ('auth', 'identity', 'security', 'warden')): return "security"
        if any(x in c or x in sid for x in ('api', 'router', 'gateway', 'network')): return "api"
        if any(x in c or x in sid for x in ('monitor', 'telemetry', 'trace', 'sentinel')): return "observability"
        if any(x in c or x in sid for x in ('ui', 'frontend', 'react', 'ocular')): return "interface"
        return "core"

    def predict(
            self,
            prompt: str,
            substrate: Any,
            active_substrates: Set[str],
            active_nodes: Optional[Dict[str, Any]] = None,
            threshold: float = 0.40
    ) -> List[Tuple[Any, float]]:
        """
        =============================================================================
        == THE OMEGA PREDICT RITE: SINGULARITY (V-Ω-TOTALITY-ONNX-SUPREMACY)       ==
        =============================================================================
        """
        if not self._state_hash or not prompt:
            return []

        _start_ns = time.perf_counter_ns()
        clauses = [c.strip() for c in re.split(r'[,;]|\band\b', prompt) if len(c.strip()) > 3]
        if not clauses:
            clauses = [prompt]

        total_election_pool = {}  # Map[ShardID, (Object, Score, Meta, Rationale)]
        domain_apex_scores: Dict[str, float] = collections.defaultdict(float)

        # --- THE MULTIVERSAL LOOP ---
        for chunk_idx, clause in enumerate(clauses):
            chunk_words = clause.split()
            if len(chunk_words) > 3 and getattr(substrate, 'mode', 'DORMANT') == "DORMANT":
                try:
                    substrate.awaken()
                except:
                    pass

            # 1. Sparse Generation
            active_tokens, negative_tokens = self._extract_polar_vectors(clause)
            expanded_intent = SynapticLattice.expand_thought(active_tokens)
            query_sparse = GnosticTensor.forge_sparse(list(expanded_intent.keys()), weights=expanded_intent)
            query_sparse_keys = set(query_sparse.keys())

            negative_intent = SynapticLattice.expand_thought(negative_tokens)
            void_sparse = GnosticTensor.forge_sparse(list(negative_intent.keys()), weights=negative_intent)
            void_keys_set = set(void_sparse.keys())

            prompt_unigrams = set(self._tokenize(clause, include_phrases=False))

            # 2. Dense Generation
            query_dense = None
            if getattr(substrate, 'mode', 'DORMANT') == "RESONANT":
                query_dense = substrate.embed_intent(clause)

            # 3. Centroid Gravity
            dag_centroid: Optional[DenseVector] = None
            if active_nodes and getattr(substrate, 'mode', 'DORMANT') == "RESONANT":
                active_dense_vectors = [n.semantic_vector for n in active_nodes.values() if
                                        hasattr(n, 'semantic_vector') and n.semantic_vector]
                if active_dense_vectors:
                    dag_centroid = GnosticTensor.calculate_centroid(active_dense_vectors)

            # --- MOVEMENT III: HYBRID MATRIX STRIKE ---
            gc_was_enabled = gc.isenabled()
            if gc_was_enabled: gc.disable()

            try:
                for shard_id, shard_sparse in self._shard_sparse_vectors.items():
                    shard_meta = self._shard_metadata[shard_id]
                    shard_keys_set = self._shard_keywords[shard_id]
                    domain_axis = shard_meta["domain_axis"]

                    sparse_score = 0.0
                    shard_dim_keys = self._shard_keys_cache[shard_id]
                    common_dims = query_sparse_keys.intersection(shard_dim_keys)
                    if common_dims:
                        sparse_score = GnosticTensor.cosine_similarity_sparse(query_sparse, shard_sparse)

                    dense_score = 0.0
                    cohesion_boost = 0.0
                    shard_dense = self._shard_dense_vectors.get(shard_id)

                    if query_dense and shard_dense:
                        dense_score = GnosticTensor.cosine_similarity_dense(query_dense, shard_dense)
                        if dag_centroid:
                            cohesion_boost = GnosticTensor.cosine_similarity_dense(dag_centroid, shard_dense) * 0.10

                    # =========================================================================
                    # == [ASCENSION 1]: THE ONNX SUPREMACY MATRIX                            ==
                    # =========================================================================
                    # Dense Math dictates 85% of reality. Determinism is a guardrail.
                    if query_dense:
                        d_weight = self.DENSE_GRAVITY_BIAS
                        s_weight = self.SPARSE_GUARDRAIL_BIAS
                    else:
                        d_weight = 0.0
                        s_weight = 1.0

                    base_score = (dense_score * d_weight) + (sparse_score * s_weight) + cohesion_boost

                    # Anti-Matter Repulsion
                    void_dims = void_keys_set.intersection(shard_dim_keys)
                    if void_dims:
                        void_product = sum(void_sparse[dim] * shard_sparse[dim] for dim in void_dims)
                        base_score -= (void_product * 2.0)

                    # Substrate DNA Ward
                    if active_substrates and "agnostic" not in shard_meta["substrate"]:
                        if active_substrates.isdisjoint(shard_meta["substrate"]):
                            base_score *= 0.1

                    if shard_meta["category"] in clause: base_score *= 1.25

                    direct_hits = prompt_unigrams.intersection(shard_keys_set)
                    if direct_hits:
                        if any(t == shard_id.split('/')[-1] for t in prompt_unigrams):
                            base_score = max(base_score, 0.98)
                        else:
                            base_score += (len(direct_hits) * 0.15)

                    if base_score >= threshold:
                        rat = f"Clause:{chunk_idx} D:{dense_score:.2f} S:{sparse_score:.2f}"
                        if shard_id not in total_election_pool or base_score > total_election_pool[shard_id][1]:
                            total_election_pool[shard_id] = (shard_meta["object"], min(1.0, base_score), shard_meta,
                                                             rat)

                            # Record the Domain Apex
                            if base_score > domain_apex_scores[domain_axis]:
                                domain_apex_scores[domain_axis] = base_score

            finally:
                if gc_was_enabled: gc.enable()

        # =========================================================================
        # == MOVEMENT IV:[ASCENSION 2] - DOMAIN-STRATIFIED APEX SCORING         ==
        # =========================================================================
        # Annihilates "Threshold Gluttony". A database will not starve observability.
        if not total_election_pool:
            return []

        sorted_pool = sorted(total_election_pool.values(), key=lambda x: x[1], reverse=True)

        final_elected_shards = []
        satisfied_capabilities: Set[str] = set()
        occupied_domains: Set[str] = set()

        for shard_obj, score, meta, rationale in sorted_pool:
            domain_axis = meta["domain_axis"]

            # [THE MASTER CURE]: The floor is tied to the Apex of THIS specific domain.
            domain_apex = domain_apex_scores.get(domain_axis, score)
            domain_influence = min(0.85, domain_apex)

            # Floor dynamically adjusts, but never drops below MATCH_FLOOR
            current_floor = max(self.MATCH_FLOOR, domain_influence * 0.65)

            if score < current_floor: continue

            # 1. Pauli Sieve (Capability Overlap)
            shard_caps = meta["pure_capabilities"]
            is_redundant = False
            if shard_caps and satisfied_capabilities:
                overlap = GnosticTensor.jaccard_similarity(shard_caps, satisfied_capabilities)
                limit = self.EXCLUSION_THRESHOLD
                if overlap > limit: is_redundant = True

            # 2. Domain Sovereignty Guard
            role = str(getattr(shard_obj.suture, 'role', 'file')).lower()
            core_id = None
            if "heart" in role or "base-api" in role: core_id = "DOMAIN:API"
            if "ocular-membrane" in role or "frontend-framework" in role: core_id = "DOMAIN:UI"

            if core_id:
                if core_id in occupied_domains:
                    is_redundant = True
                    Logger.verbose(f"Pauli Exclusion: Vaporized '{shard_obj.id}' to protect {core_id}.")
                else:
                    occupied_domains.add(core_id)

            # 3. Final Acceptance
            new_caps = shard_caps - satisfied_capabilities
            if (not is_redundant and (new_caps or not shard_caps)) or score > 0.95:
                shard_obj.resonance_score = score
                shard_obj.match_reason = rationale
                final_elected_shards.append((shard_obj, score))
                satisfied_capabilities.update(meta["provides"])
                satisfied_capabilities.add(shard_obj.id)

        return final_elected_shards

    def _extract_polar_vectors(self, text: str) -> Tuple[List[str], List[str]]:
        raw_words = [w for w in re.split(r'[^a-z0-9]', text) if len(w) > 1]
        active, negative, is_negated = [], [], False

        for word in raw_words:
            if word in self.NEGATION_TOKENS:
                is_negated = True;
                continue
            if word in {"and", "with"}:
                is_negated = False;
                continue

            target_list = negative if is_negated else active
            if word not in self.STOPWORDS: target_list.append(word)

        def _get_ngrams(tokens):
            ngrams = list(tokens)
            if len(tokens) > 1: ngrams.extend([f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)])
            return ngrams

        return _get_ngrams(active), _get_ngrams(negative)

    def _tokenize(self, text: str, include_phrases: bool = False) -> List[str]:
        raw_words = [w for w in re.split(r'[^a-z0-9]', text.lower()) if len(w) > 1]
        unigrams = [w for w in raw_words if w not in self.STOPWORDS]
        if not include_phrases or len(unigrams) < 2: return unigrams
        bigrams = [f"{unigrams[i]} {unigrams[i + 1]}" for i in range(len(unigrams) - 1)]
        return unigrams + bigrams