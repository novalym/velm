# Path: src/velm/core/cortex/semantic_resolver/engine.py
# ---------------------------------------------------------------------------
import re
import json
import time
import math
from pathlib import Path
from typing import List, Dict, Any, Optional

from .contracts import ShardGnosis, ResonanceReport
from .substrate import NeuralSubstrate
from .synonyms import expand_intent
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("SemanticResolver")


class SemanticResolver:
    """
    =============================================================================
    == THE HYPER-INTELLIGENT RESOLVER (V-Ω-TOTALITY-V1000)                     ==
    =============================================================================
    The central brain.
    1. Loads the SCAF-Hub Index (Memory).
    2. Awakens the Neural Substrate (Cortex).
    3. Expands the User's Prompt (Synaptic Web).
    4. Calculates the Hybrid Resonance (Vector + Lexical).
    5. Elects the Sovereign Shards.
    """

    # The Physics of Resonance
    SEMANTIC_THRESHOLD = 0.42  # Minimum vector similarity
    LEXICAL_BOOST = 0.40  # Weight of exact keyword matches
    VIBE_BOOST = 0.25  # Weight of 'vibe' keyword matches

    def __init__(self, registry_path: Path, model_path: Path):
        self.registry_path = registry_path
        self.model_path = model_path

        self.substrate = NeuralSubstrate()
        self.grimoire: List[ShardGnosis] = []
        self._is_warm = False

    def _awaken(self):
        """[THE RITE OF AWAKENING]: Loads Memory and Cortex JIT."""
        if self._is_warm: return
        start_ns = time.perf_counter_ns()

        # 1. Load Memory (The Index)
        if not self.registry_path.exists():
            Logger.warn(f"Celestial Registry not found at {self.registry_path}. Operating in Void Mode.")
        else:
            try:
                data = json.loads(self.registry_path.read_text(encoding='utf-8'))
                raw_list = data.get("registry", [])
                # Transmute JSON to Pydantic
                self.grimoire = [ShardGnosis.model_validate(item) for item in raw_list]
                # Logger.verbose(f"Ingested {len(self.grimoire)} Gnostic Shards from the Index.")
            except Exception as e:
                Logger.error(f"Registry corrupted: {e}")

        # 2. Load Cortex (The Model)
        self.substrate.awaken(self.model_path)

        self._is_warm = True
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        # Logger.debug(f"Resolver awakened in {duration_ms:.2f}ms.")

    def resolve(self, prompt: str) -> List[ShardGnosis]:
        """
        [THE GRAND RITE OF RESOLUTION]
        Input: "I need a fastapi app with auth"
        Output: [Shard(FastAPI), Shard(Clerk), Shard(Postgres)]
        """
        self._awaken()
        start_ns = time.perf_counter_ns()

        # 1. PURIFY AND EXPAND (The Synaptic Web)
        clean_prompt = prompt.lower().strip()
        tokens = self._tokenize(clean_prompt)
        expanded_tokens = expand_intent(tokens)

        # Logger.debug(f"Prompt Expanded: {clean_prompt} -> {list(expanded_tokens)}")

        # 2. VECTORIZE (The Neural Gaze)
        # On WASM, this might return None if not bridged yet; that is fine, we fall back to Lexical.
        query_vector = self.substrate.embed_intent(clean_prompt)

        # 3. THE RESONANCE MATRIX (Scoring)
        scored_candidates = []

        for shard in self.grimoire:
            score, reason = self._calculate_resonance(
                query_vector=query_vector,
                tokens=expanded_tokens,
                shard=shard
            )

            # Apply Threshold
            if score > 0.3:  # Lower threshold to allow Lexical-only matches to pass
                shard.resonance_score = score
                shard.match_reason = reason
                scored_candidates.append(shard)

        # 4. THE ELECTION (Sorting & Culling)
        # Sort by score DESC
        scored_candidates.sort(key=lambda x: x.resonance_score, reverse=True)

        # Pruning Logic: Keep top results that are close to the winner
        final_election = []
        if scored_candidates:
            winner_score = scored_candidates[0].resonance_score
            for s in scored_candidates:
                # Dynamic cutoff: Within 20% of winner, or absolute high confidence
                if s.resonance_score >= (winner_score * 0.75) or s.resonance_score > 0.85:
                    final_election.append(s)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if final_election:
            names = [f"{s.id}({s.resonance_score:.2f})" for s in final_election]
            Logger.success(f"🧠 [RESOLVER] Matched: {', '.join(names)} in {duration_ms:.2f}ms")
        else:
            Logger.warn(f"🧠 [RESOLVER] No resonance found for '{prompt}'.")

        return final_election

    def _calculate_resonance(
            self,
            query_vector: Optional[List[float]],
            tokens: dfset[str],
            shard: ShardGnosis
    ) -> tuple[float, str]:
        """
        [THE HYBRID EQUATION]
        Returns (Score, Reason)
        """
        semantic_score = 0.0
        lexical_score = 0.0
        reasons = []

        # A. Semantic (Vector)
        if query_vector and shard.semantic_vector:
            # Cosine Similarity
            dot_product = sum(q * s for q, s in zip(query_vector, shard.semantic_vector))
            semantic_score = dot_product
            if dot_product > self.SEMANTIC_THRESHOLD:
                reasons.append("Vector")

        # B. Lexical (Keyword)
        # We check ID, Vibe, and Description against Expanded Tokens

        # 1. ID Match (Highest Value)
        # "fastapi" in "api/fastapi"
        shard_id_clean = shard.id.lower().replace("/", " ").replace("-", " ")
        if any(t in shard_id_clean for t in tokens):
            lexical_score += self.LEXICAL_BOOST * 1.5
            reasons.append("ID Match")

        # 2. Vibe Match (Medium Value)
        # "auth" in "@vibe: security, auth, jwt"
        shard_vibe = shard.vibe.lower()
        vibe_hits = sum(1 for t in tokens if t in shard_vibe)
        if vibe_hits > 0:
            lexical_score += (self.VIBE_BOOST * vibe_hits)
            reasons.append(f"Vibe({vibe_hits})")

        # 3. Description Match (Low Value)
        shard_desc = shard.description.lower()
        if any(t in shard_desc for t in tokens):
            lexical_score += 0.1
            reasons.append("Desc")

        # C. Synthesis
        # If we have vectors, we blend. If not, we rely on Lexical.
        if query_vector:
            # Weighted average favoring Vector but boosted by Keywords
            total = (semantic_score * 0.6) + (min(1.0, lexical_score) * 0.4)
            # Boost if BOTH matched
            if semantic_score > 0.4 and lexical_score > 0.2:
                total *= 1.2
        else:
            # Pure Lexical Mode
            total = min(1.0, lexical_score)

        return min(1.0, total), "+".join(reasons)

    def _tokenize(self, text: str) -> List[str]:
        """Simple regex tokenizer."""
        # Split on non-alphanumeric, keep only valid words > 1 char
        return [w for w in re.split(r'[^a-z0-9]', text) if len(w) > 1]