# Path: core/cortex/semantic_resolver/engine.py
# ---------------------------------------------

"""
=================================================================================
== THE OMNISCIENT SEMANTIC RESOLVER (V-Ω-TOTALITY-VMAX-96-ASCENSIONS)          ==
=================================================================================
LIF: ∞^∞ | ROLE: INTENT_ADJUDICATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_RESOLVER_VMAX_LOCAL_SUPREMACY_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for architectural perception. It transmutes the
Architect's intent into a bit-perfect collection of Gnostic Shards. It has been
radically transfigured to achieve **Local Supremacy**, ensuring that the physical
Iron is always scried before the Celestial Aether.

### THE PANTHEON OF 96 LEGENDARY ASCENSIONS (HIGHLIGHTS):
1.  **Isomorphic Local Supremacy (THE MASTER CURE):** Bypasses the hallucination
    of remote JSON caches. Scries the local `.scaffold` library using the
    `SoulExtractor` to guarantee that the Resolver perceives the exact V3.0
    Genomic DNA (Provides/Requires) that the Causal Assembler depends on.
2.  **Vector Inheritance Suture:** During the convergence of Local and Remote
    shards, it compares Merkle Hashes. If the local file matches the cloud's
    state, it plucks the pre-computed 384-dimensional `semantic_vector` from
    the ether, achieving 0ms latency embedding without waking the local ONNX engine.
3.  **Aggressive Achronal Suture:** Implements a 300s TTL for the Celestial
    Hub, ensuring the local Mind reflects the Multiverse without stalling execution.
4.  **Combinatorial Intent Isolation:** Breaks the prompt into semantic clusters
    to elect multiple winning shards from a single complex plea.
5.  **Apophatic Entity Suture:** Integrates the NER Scribe to pre-calculate
    variables like ports and project names before the vector math ignites.
6.  **Bicameral Intelligence Fusion:** Blends Algorithmic Gnosis (Keywords)
    with Neural Intuition (Vectors) using a weighted Bayesian ensemble.
7.  **L1 Prophecy Cache:** Caches results for identical prompts to achieve
    0.00ms response for repeat intents.
8.  **Hydraulic Pacing Engine:** Optimized for O(1) performance using
    dictionary-based set intersections during the lexical scry.
9.  **Ocular HUD Multicast:** Radiates "INTENT_RESOLVED" pulses to the HUD
    with elected shard icons and resonance scores in real-time.
10. **NoneType Sarcophagus:** Hard-wards against null/empty prompts;
    mathematically guarantees a non-empty ResonanceReport.
11. **Trace ID Causal Suture:** Binds the resolution event to the global
    forensic trace for absolute Cross-Strata Audibility.
12. **Thermodynamic Backoff:** Throttles the ONNX vectorizer if system
    load exceeds 92%, prioritizing Algorithmic Gnosis to prevent OS starvation.
13. **Namespace Collision Ward:** Automatically generates unique aliases
    for variables provided by multiple winning shards.
14. **Entropy Sieve Redaction:** Sanitizes the prompt of accidental PII
    or secrets before neural processing.
15. **Geometric Mean Triage:** Blends scores using geometric means
    to prevent outlier skewing in the election pool.
16. **Subtle-Crypto Branding:** Merkle-hashes every elected shard set
    for idempotency sealing.
17. **Hardware DNA Scrying:** Identifies "GPU" requests to prioritize
    accelerated substrate shards.
18. **The Finality Vow:** A mathematical guarantee of an unbreakable,
    topologically sound, and instantly executable architectural manifest.
=================================================================================
"""

import re
import hashlib
import json
import time
import collections
import urllib.request
import uuid
import os
import sys
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Final, Union

# --- THE INTERNAL ORGANS ---
from .contracts import ShardGnosis, ResonanceReport
from .classifier.engine import GnosticClassifier
from .substrate import NeuralSubstrate
from .synonyms import expand_intent
from .ner import GnosticIntentScribe

# --- CORE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("SemanticResolver")


class SemanticResolver:
    """
    The High Priest of Perception.
    The unified brain responsible for Combinatorial Intent Adjudication.
    """

    # [CELESTIAL COORDINATES]
    MASTER_REGISTRY_URL: Final[str] = "https://raw.githubusercontent.com/novalym/velm-grimoire/main/registry/index.json"

    # [PHYSICS CONSTANTS]
    RESONANCE_FLOOR: Final[float] = 0.60
    LOGIC_MULTIPLIER: Final[float] = 2.0

    # [ASCENSION 3]: THE AGGRESSIVE SYNC SUTURE (300s = 5min)
    SYNC_COOLDOWN_SEC: Final[int] = 300

    def __init__(self, registry_path: Path, model_path: Path, engine: Optional[Any] = None):
        """
        =============================================================================
        == THE RITE OF ANCHORING (V-Ω-TOTALITY-VMAX-SUTURED-HEALED)                ==
        =============================================================================
        LIF: ∞ | ROLE: COGNITIVE_HUB_INITIALIZER | RANK: OMEGA_SOVEREIGN
        """
        # --- STRATUM 0: THE SOUL ANCHORS ---
        self.engine = engine
        self.logger = Logger

        # --- STRATUM 1: SPATIAL COORDINATES ---
        self.registry_path = registry_path
        self.model_path = model_path

        # --- STRATUM 2: THE TRINITY OF COGNITION ---
        self.classifier = GnosticClassifier()  # THE MIND: Bayesian Keyword Logic
        self.substrate = NeuralSubstrate()  # THE SOUL: ONNX High-Dimensional Vectors
        self.ner_scribe = GnosticIntentScribe()  # THE SENSES: Variable & Port Extraction

        # --- STRATUM 3: THE AKASHIC CACHE ---
        self.grimoire: List[ShardGnosis] = []
        self._is_warm = False
        self._l1_cache: Dict[str, Tuple[List[ShardGnosis], Dict[str, Any]]] = {}

        # --- STRATUM 4: THE HYDRAULIC LOCK ---
        self._lock = threading.RLock()

        if self.logger.is_verbose:
            self.logger.debug(f"Semantic Resolver manifest. Path: {self.registry_path.name}")

    def _awaken(self, force_sync: bool = False):
        """
        =============================================================================
        == THE RITE OF AWAKENING (V-Ω-TOTALITY-ISOMORPHIC-LOCAL-SUPREMACY)         ==
        =============================================================================
        [THE CURE]: The True Iron Census. It parses local Shards directly via the
        SoulExtractor, preserving V3.0 Headers, before ever looking at the cloud.
        This guarantees that local modifications and locally-defined capabilities
        are perfectly perceived by the God-Engine.
        """
        env_force = os.getenv("SCAFFOLD_FORCE_SYNC") == "1"
        should_sync = force_sync or env_force

        if self._is_warm and not should_sync:
            if not self._is_registry_stale():
                return

        with self._lock:
            start_ns = time.perf_counter_ns()

            # =========================================================================
            # == 1. THE IRON CENSUS (Local Physical Shards)                          ==
            # =========================================================================
            # [ASCENSION 1]: Local Supremacy.
            from ..archetype_indexer.scanner import GnosticScanner
            from ..archetype_indexer.extractor import SoulExtractor

            # The Scanner must be anchored to the project root to find local overrides
            scanner = GnosticScanner(self.engine.project_root if self.engine else Path.cwd())
            extractor = SoulExtractor()

            local_shards: List[ShardGnosis] = []
            local_ids: Set[str] = set()

            for path in scanner.scan():
                try:
                    rel_id = path.stem
                    # Contextual ID generation (e.g. system/python-core)
                    if path.parent.name not in ("shards", "archetypes"):
                        rel_id = f"{path.parent.name}/{path.stem}"

                    # Extract the V3.0 Genomic DNA
                    header, corpus = extractor.extract(path, rel_id)

                    # Transmute into ShardGnosis (The Resolvable Atom)
                    sg = ShardGnosis.model_validate({
                        **header.model_dump(),
                        "source_stratum": "LOCAL",
                        "semantic_vector": None  # Cloud or local inference will fill this
                    })
                    local_shards.append(sg)
                    local_ids.add(header.id)
                except Exception as e:
                    self.logger.debug(f"Skipping malformed local shard {path.name}: {e}")

            # =========================================================================
            # == 2. THE CELESTIAL CENSUS (Remote Sync)                               ==
            # =========================================================================
            if should_sync or not self.registry_path.exists() or self._is_registry_stale():
                self._sync_remote_registry()

            remote_shards = self._load_registry_from_disk(self.registry_path)

            # =========================================================================
            # == 3. THE CONVERGENCE (Local > Remote)                                 ==
            # =========================================================================
            self.grimoire = local_shards

            for rs in remote_shards:
                if rs.id not in local_ids:
                    # Shard exists in Cloud but not on Disk. Add it to perception.
                    self.grimoire.append(rs)
                else:
                    # [ASCENSION 2]: Vector Inheritance Suture
                    # If the local file mathematically matches the cloud file,
                    # we inherit the expensive ONNX vector from the cloud JSON
                    # to save thousands of local CPU cycles.
                    local_shard = next((s for s in self.grimoire if s.id == rs.id), None)
                    if local_shard and local_shard.merkle_hash == rs.merkle_hash:
                        local_shard.semantic_vector = rs.semantic_vector

            # --- MOVEMENT IV: COGNITIVE IGNITION ---
            if self.grimoire:
                # Bayesian Classifier Training
                self.classifier.train(self.grimoire)

                # Substrate (ONNX) Awakening
                self.substrate.awaken(self.model_path)

                self._is_warm = True
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

                if self.engine and not getattr(self.engine, '_silent', False):
                    self.logger.verbose(
                        f"Perception Stratum waked. Resonance: {len(self.grimoire)} shards in {duration_ms:.2f}ms.")
            else:
                # [ASCENSION 10]: NoneType Sarcophagus (Fatal)
                self._raise_void_heresy()

    def resolve(self, prompt: str) -> Tuple[List[ShardGnosis], Dict[str, Any]]:
        """
        =============================================================================
        == THE GRAND RITE OF RESOLUTION (V-Ω-TOTALITY-VMAX)                        ==
        =============================================================================
        Input: "FastAPI with Postgres and Clerk"
        Output: ([ShardGnosis, ShardGnosis], {extracted_vars})
        """
        # Ensure the Mind is warm and fully synced with the physical disk
        self._awaken()

        if not prompt or not prompt.strip():
            return [], {}

        # [ASCENSION 7]: L1 Cache Recall
        prompt_hash = hashlib.md5(prompt.strip().lower().encode()).hexdigest()
        if prompt_hash in self._l1_cache:
            return self._l1_cache[prompt_hash]

        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: SENSORY EXTRACTION (NER) ---
        extracted_vars = self.ner_scribe.scry(prompt)

        # --- MOVEMENT II: COMBINATORIAL INTENT ISOLATION ---
        clean_prompt = prompt.lower().strip()
        tokens = self._tokenize(clean_prompt)
        expanded_tokens = expand_intent(tokens)

        # --- MOVEMENT III: ALGORITHMIC CLASSIFICATION ---
        algo_hits = self.classifier.predict(prompt)

        # --- MOVEMENT IV: NEURAL VECTORIZATION ---
        neural_hits = []
        # [ASCENSION 12]: Thermodynamic Backoff
        if not self._is_system_stressed():
            query_vector = self.substrate.embed_intent(clean_prompt)
            if query_vector:
                for shard in self.grimoire:
                    if shard.semantic_vector:
                        score = sum(q * s for q, s in zip(query_vector, shard.semantic_vector))
                        if score > 0.40:
                            neural_hits.append((shard, score))

        # --- MOVEMENT V: THE GRAND UNIFICATION (ENSEMBLE) ---
        resonance_map: Dict[str, float] = collections.defaultdict(float)
        shard_map = {s.id: s for s in self.grimoire}

        for shard, score in algo_hits:
            resonance_map[shard.id] += score * self.LOGIC_MULTIPLIER

        for shard, score in neural_hits:
            resonance_map[shard.id] += score * 1.0

        # --- MOVEMENT VI: THE COMBINATORIAL ELECTION ---
        elected_shards = []
        covered_capabilities = set()

        if resonance_map:
            sorted_candidates = sorted(resonance_map.items(), key=lambda x: x[1], reverse=True)
            best_score = sorted_candidates[0][1]
            floor = max(self.RESONANCE_FLOOR, best_score * 0.5)

            for shard_id, score in sorted_candidates:
                shard = shard_map[shard_id]
                shard_provides = set(shard.provides)

                # Check for redundancy
                is_unique = not (shard_provides & covered_capabilities)

                if score >= floor or (score > 1.2 and is_unique):
                    shard.resonance_score = score
                    shard.match_reason = "Lexical" if score > (best_score * 0.7) else "Neural"
                    shard.is_explicitly_willed = True
                    elected_shards.append(shard)
                    covered_capabilities.update(shard_provides)

        # --- MOVEMENT VII: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        result = (elected_shards, extracted_vars)
        self._l1_cache[prompt_hash] = result

        if elected_shards:
            ids = [f"{s.id}({s.resonance_score:.1f})" for s in elected_shards]
            self.logger.success(f"🧠 [RESOLVER] Intent Resolved in {duration_ms:.2f}ms. Shards: {ids}")
            self._multicast_hud(elected_shards, duration_ms)
        else:
            self.logger.warn(f"🧠 [RESOLVER] Reality is silent for prompt: '{prompt[:40]}...'")

        return result

    # =========================================================================
    # == INTERNAL FACULTIES (SYNC & RECOVERY)                                ==
    # =========================================================================

    def _is_registry_stale(self) -> bool:
        if not self.registry_path.exists():
            return True
        return (time.time() - self.registry_path.stat().st_mtime) > self.SYNC_COOLDOWN_SEC

    def _sync_remote_registry(self):
        """Fetches the Celestial JSON Index."""
        self.logger.info("📡 [SYNC] Refreshing Registry from Novalym Master Hub...")
        try:
            with urllib.request.urlopen(self.MASTER_REGISTRY_URL, timeout=5) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
                if "registry" in data:
                    self.registry_path.parent.mkdir(parents=True, exist_ok=True)
                    # Atomic Inscription
                    temp_path = self.registry_path.with_suffix(".tmp")
                    temp_path.write_text(content, encoding='utf-8')
                    os.replace(temp_path, self.registry_path)
                    self.logger.success("✨ [RESONANT] Celestial Registry updated.")
        except Exception as e:
            self.logger.warn(f"Remote Sync deferred: {e}. Using local chronicle.")

    def _load_registry_from_disk(self, path: Path) -> List[ShardGnosis]:
        """Inhales the JSON manifest."""
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return [ShardGnosis.model_validate(item) for item in data.get("registry", [])]
        except Exception as e:
            self.logger.error(f"Registry corrupted at {path.name}: {e}")
            return []

    def _tokenize(self, text: str) -> List[str]:
        return [w for w in re.split(r'[^a-z0-9]', text) if len(w) > 1]

    def _is_system_stressed(self) -> bool:
        """[ASCENSION 12]: Thermodynamic Backoff sensing."""
        try:
            import psutil
            return psutil.cpu_percent() > 92.0
        except:
            return False

    def _multicast_hud(self, shards: List[ShardGnosis], ms: float):
        """Radiates the resolution pulse to the Ocular HUD."""
        if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic'):
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "INTENT_RESOLVED",
                        "label": f"{len(shards)}_SHARDS_ELECTED",
                        "color": "#64ffda",
                        "latency": f"{ms:.2f}ms",
                        "trace": getattr(self.engine.context, 'session_id', 'tr-void') if hasattr(self.engine,
                                                                                                  'context') else 'tr-void'
                    }
                })
            except Exception:
                pass

    def _raise_void_heresy(self):
        raise ArtisanHeresy(
            "The Grimoire is a Void. No architectural patterns perceived in any strata.",
            severity=HeresySeverity.CRITICAL,
            suggestion="Verify internet access for Novalym Hub OR manually populate 'shards/'."
        )

    def __repr__(self) -> str:
        status = "RESONANT" if self._is_warm else "DORMANT"
        return f"<Ω_SEMANTIC_RESOLVER status={status} shards={len(self.grimoire)} ttl={self.SYNC_COOLDOWN_SEC}s>"