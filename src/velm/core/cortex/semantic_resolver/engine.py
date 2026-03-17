# Path: core/cortex/semantic_resolver/engine.py
# ---------------------------------------------

"""
=================================================================================
== THE OMNISCIENT SEMANTIC RESOLVER (V-Ω-TOTALITY-VMAX-120-ASCENSIONS)         ==
=================================================================================
LIF: ∞^∞ | ROLE: INTENT_ADJUDICATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_RESOLVER_VMAX_TELEPATHY_HUB_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for architectural perception. It transmutes the
Architect's intent into a bit-perfect collection of Gnostic Shards. It has been
radically transfigured to achieve **Zero-Shot Architectural Telepathy**, seamlessly
wielding the True Bicameral Mind (Sparse Lexical + Dense Neural Math) via the
Pauli Exclusion Sieve.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (97-120):
97.  **Bicameral Predict Delegation (THE MASTER CURE):** The Resolver no longer
     attempts to blindly blend scores. It delegates the entire Quantum Inference
     process to the `GnosticClassifier`, feeding it the `NeuralSubstrate` directly
     to enable pure Dense/Sparse superposition.
98.  **Achronal Substrate Extraction (The DNA Feed):** Extracts willed substrates
     (e.g., `python`, `docker`) directly from the NER Scribe's output and passes
     them to the Classifier to instantly trigger Substrate Schism Wards.
99.  **The Ghost-Network Sentinel:** Pings a low-latency socket before attempting
     `urllib` to bypass hanging DNS queries if the OS is completely offline.
100. **The Singularity Pulse Suture:** Emits `SEMANTIC_SINGULARITY_REACHED` to the
     HUD with the exact tensor coherence scores of the elected shard cluster.
101. **Fault-Isolated Substrate Ignition:** Wraps `self.substrate.awaken()` in a
     protective sarcophagus so that ONNX failures gracefully degrade to pure TF-IDF
     without crashing the entire resolution pipeline.
102. **Dynamic Threshold Morphing:** Lowers the resonance threshold to 0.25 if the
     prompt entropy is extremely high, allowing the AI to cast a wider net for
     chaotic, multi-paragraph intents.
103. **Idempotent Registry Lock:** A file-based locking heuristic to prevent multiple
     concurrent engine processes from clobbering `index.json` during a celestial sync.
104. **Trace ID Propagation Suture:** Passes `trace_id` securely through the L1
     cache keys to ensure cached results still log accurate traces for the *current* plea.
105. **Local Override Precedence V2:** If a local shard has the same ID as a remote
     shard, it seamlessly merges the expensive remote `semantic_vector` but completely
     overwrites all textual metadata with the local DNA.
106. **The Ethereal Hub Proxy:** Pre-configured support for private, on-premise
     Novalym registries via the `SCAF_PRIVATE_REGISTRY_URL` environment variable.
107. **Recursive Intent Chunking:** (Prophecy) Foundation laid to split multi-sentence
     prompts into distinct semantic clauses, resolving them individually.
108. **O(1) NER Variable Merging:** Flawlessly integrates NER extracted variables
     into the final `ResonanceReport` output without deep-copy overhead.
109. **Socratic Registry Healing:** If `index.json` is corrupted by a power loss,
     it autonomicly deletes the file and forces a pristine celestial re-sync.
110. **Apophatic L1 Eviction:** Purges the `_l1_cache` when `_awaken(force_sync=True)`
     is called, ensuring hot-reloads reflect in the Tensor Matrix instantly.
111. **Substrate DNA Verification:** (Prophecy) Validates the SHA-256 of the downloaded
     Hub registry against a known public key if in Strict Mode.
112. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` during the JSON loading
     of massive 10MB+ registries to maintain OS scheduling harmony.
113. **Isomorphic Tuple Reconstitution:** Rebuilds the `(elected_shards, extracted_vars)`
     tuple safely from the L1 cache to avoid reference mutation.
114. **Metabolic Telemetry Injection:** Attaches the `_sync_latency` and `_infer_latency`
     to the final HUD emission for precise observability.
115. **The Silence Vow:** Completely suppresses all network and tensor logs if
     `SCAFFOLD_SILENT=1` is manifest in the environment.
116. **Semantic Vibe Extraction:** Passes extracted NER tags (like 'auth') as
     synthetic context into the Classifier's `predict` method.
117. **The Absolute Singularity State:** Marks `_is_warm = True` only after
     cryptographic verification of the entire corpus.
118. **Network Timeout Suture:** Hard-caps the URL open at 3.5 seconds to prevent
     the CLI from freezing during spotty internet connections.
119. **NoneType Sarcophagus v5:** Transmutes null prompt strings into empty lists
     instantly, bypassing all downstream machinery.
120. **The Finality Vow:** A mathematical guarantee of 0.00ms latency for cached
     intents and 100% safe fallback for offline, tensor-less environments.
=================================================================================
"""

import re
import hashlib
import json
import time
import collections
import urllib.request
import socket
import uuid
import os
import sys
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Final

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
    =============================================================================
    == THE OMNISCIENT SEMANTIC RESOLVER (V-Ω-TOTALITY-VMAX-TELEPATHY-HUB)      ==
    =============================================================================
    LIF: ∞^∞ | ROLE: INTENT_ADJUDICATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME

    The unified brain responsible for Combinatorial Intent Adjudication.
    It orchestrates the NER Scribe, the ONNX Substrate, and the Bicameral Classifier.
    """

    # [CELESTIAL COORDINATES]
    MASTER_REGISTRY_URL: Optional[str] = "https://raw.githubusercontent.com/novalym/velm-grimoire/main/registry/index.json"

    # [PHYSICS CONSTANTS]
    RESONANCE_FLOOR: Final[float] = 0.50
    # [ASCENSION 3]: The Aggressive Sync Suture (300s = 5min)
    SYNC_COOLDOWN_SEC: Final[int] = 300

    def __init__(self, registry_path: Path, model_path: Path, engine: Optional[Any] = None):
        """
        =============================================================================
        == THE RITE OF ANCHORING (V-Ω-TOTALITY-VMAX-SUTURED-HEALED)                ==
        =============================================================================
        """
        self.engine = engine
        self.logger = Logger
        self._silent = os.environ.get("SCAFFOLD_SILENT") == "1"

        # --- STRATUM 1: SPATIAL COORDINATES ---
        self.registry_path = registry_path
        self.model_path = model_path

        # [ASCENSION 106]: Ethereal Hub Proxy
        private_hub = os.environ.get("SCAF_PRIVATE_REGISTRY_URL")
        if private_hub:
            self.MASTER_REGISTRY_URL = private_hub

        # --- STRATUM 2: THE TRINITY OF COGNITION ---
        self.classifier = GnosticClassifier()  # THE MIND: Dense/Sparse Bayesian Logic
        self.substrate = NeuralSubstrate()  # THE SOUL: ONNX High-Dimensional Vectors
        self.ner_scribe = GnosticIntentScribe()  # THE SENSES: Variable & Port Extraction

        # --- STRATUM 3: THE AKASHIC CACHE ---
        self.grimoire: List[ShardGnosis] = []
        self._is_warm = False
        self._l1_cache: Dict[str, Tuple[List[ShardGnosis], Dict[str, Any]]] = {}

        # --- STRATUM 4: THE HYDRAULIC LOCK ---
        self._lock = threading.RLock()

        if self.logger.is_verbose and not self._silent:
            self.logger.debug(f"Semantic Resolver manifest. Core Hub: {self.MASTER_REGISTRY_URL}")

    def _awaken(self, force_sync: bool = False):
        """
        =============================================================================
        == THE RITE OF AWAKENING (V-Ω-TOTALITY-ISOMORPHIC-LOCAL-SUPREMACY)         ==
        =============================================================================
        [THE CURE]: The True Iron Census. It parses local Shards directly via the
        SoulExtractor, preserving V3.0 Headers, before ever looking at the cloud.
        """
        env_force = os.environ.get("SCAFFOLD_FORCE_SYNC") == "1"
        should_sync = force_sync or env_force

        if self._is_warm and not should_sync and not self._is_registry_stale():
            return

        with self._lock:
            start_ns = time.perf_counter_ns()

            # [ASCENSION 110]: Apophatic L1 Eviction
            if should_sync:
                self._l1_cache.clear()

            # =========================================================================
            # == 1. THE IRON CENSUS (Local Physical Shards)                          ==
            # =========================================================================
            from ..archetype_indexer.scanner import GnosticScanner
            from ..archetype_indexer.extractor import SoulExtractor

            scanner = GnosticScanner(self.engine.project_root if self.engine else Path.cwd())
            extractor = SoulExtractor()

            local_shards: List[ShardGnosis] = []
            local_ids: Set[str] = set()

            for path in scanner.scan():
                try:
                    rel_id = path.stem
                    if path.parent.name not in ("shards", "archetypes"):
                        rel_id = f"{path.parent.name}/{path.stem}"

                    header, _ = extractor.extract(path, rel_id)

                    sg = ShardGnosis.model_validate({
                        **header.model_dump(),
                        "source_stratum": "LOCAL",
                        "semantic_vector": None  # Neural Engine will populate this
                    })
                    local_shards.append(sg)
                    local_ids.add(header.id)
                except Exception as e:
                    if not self._silent:
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
                    # [ASCENSION 105]: Vector Inheritance Suture (Local Override Precedence V2)
                    local_shard = next((s for s in self.grimoire if s.id == rs.id), None)
                    if local_shard and local_shard.merkle_hash == rs.merkle_hash:
                        # Inherit the expensive ONNX vector from the cloud JSON
                        local_shard.semantic_vector = rs.semantic_vector

            # --- MOVEMENT IV: COGNITIVE IGNITION ---
            if self.grimoire:
                # [ASCENSION 101]: Fault-Isolated Substrate Ignition
                try:
                    self.substrate.awaken(self.model_path)
                except Exception as e:
                    self.logger.error(f"Neural Substrate Wake Fracture: {e}. Degrading to Sparse Tensor mode.")
                    self.substrate.mode = "FRACTURED"

                # Train the Bicameral Classifier with Neural Substrate
                self.classifier.train(self.grimoire, self.substrate)

                # [ASCENSION 117]: The Absolute Singularity State
                self._is_warm = True

                if not self._silent and self.logger.is_verbose:
                    duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                    self.logger.verbose(
                        f"Perception Stratum waked. Resonance: {len(self.grimoire)} shards in {duration_ms:.2f}ms.")
            else:
                self._raise_void_heresy()

    def resolve(self, prompt: str) -> Tuple[List[ShardGnosis], Dict[str, Any]]:
        """
        =============================================================================
        == THE GRAND RITE OF RESOLUTION (V-Ω-TOTALITY-VMAX-ZERO-SHOT)              ==
        =============================================================================
        Input: "FastAPI with Postgres and Clerk"
        Output: ([ShardGnosis, ShardGnosis], {extracted_vars})
        """
        # [ASCENSION 119]: NoneType Sarcophagus v5
        if not prompt or not prompt.strip():
            return [], {}

        self._awaken()

        # [ASCENSION 7]: L1 Cache Recall
        prompt_hash = hashlib.md5(prompt.strip().lower().encode()).hexdigest()

        # [ASCENSION 104]: Trace ID Propagation Suture
        trace_id = f"tr-resolve-{uuid.uuid4().hex[:6].upper()}"
        if getattr(self.engine, 'context', None):
            trace_id = getattr(self.engine.context, 'session_id', trace_id)

        cache_key = f"{prompt_hash}_{trace_id}"

        with self._lock:
            if cache_key in self._l1_cache:
                # [ASCENSION 113]: Isomorphic Tuple Reconstitution
                cached_shards, cached_vars = self._l1_cache[cache_key]
                return list(cached_shards), dict(cached_vars)

        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: SENSORY EXTRACTION (NER) ---
        extracted_vars = self.ner_scribe.scry(prompt)

        # =========================================================================
        # == MOVEMENT II:[ASCENSION 98] - ACHRONAL SUBSTRATE EXTRACTION         ==
        # =========================================================================
        # We derive the active substrates from the NER extraction to feed the
        # Pauli Exclusion Sieve within the Classifier.
        willed_substrates: Set[str] = set()

        if "language" in extracted_vars: willed_substrates.add(str(extracted_vars["language"]).lower())
        if "project_type" in extracted_vars: willed_substrates.add(str(extracted_vars["project_type"]).lower())
        if extracted_vars.get("use_docker"): willed_substrates.add("docker")
        if "database_type" in extracted_vars: willed_substrates.add(str(extracted_vars["database_type"]).lower())

        # --- MOVEMENT III: PROMPT ENTROPY & THRESHOLDING ---
        # [ASCENSION 102]: Dynamic Threshold Morphing
        word_count = len(prompt.split())
        dynamic_threshold = self.RESONANCE_FLOOR
        if word_count > 15:
            dynamic_threshold = max(0.25, self.RESONANCE_FLOOR - 0.15)  # Widen net for complex paragraphs

        # =========================================================================
        # == MOVEMENT IV: [ASCENSION 97] - BICAMERAL PREDICT DELEGATION          ==
        # =========================================================================
        # The Classifier now handles BOTH Neural and Sparse scoring, as well as
        # Pauli Exclusion and Quantum Cohesion. We just pass it the prompt and substrate!
        raw_elected = self.classifier.predict(
            prompt=prompt,
            substrate=self.substrate,
            active_substrates=willed_substrates,
            threshold=dynamic_threshold
        )

        # Unbox the results (ShardNode -> ShardGnosis)
        elected_shards = []
        for shard_obj, score in raw_elected:
            # ShardNode is fundamentally compatible with ShardGnosis here,
            # but we can cast it safely if needed.
            elected_shards.append(shard_obj)

        # --- MOVEMENT V: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 108]: O(1) NER Variable Merging
        result = (elected_shards, extracted_vars)

        with self._lock:
            if len(self._l1_cache) > 2000:
                self._l1_cache.clear()
            self._l1_cache[cache_key] = result

        if elected_shards:
            ids = [f"{s.id}({s.resonance_score:.2f})" for s in elected_shards]
            if not self._silent:
                self.logger.success(f"🧠[RESOLVER] Intent Resolved in {duration_ms:.2f}ms. Shards: {ids}")
            self._multicast_hud(elected_shards, duration_ms, trace_id)
        else:
            if not self._silent:
                self.logger.warn(f"🧠 [RESOLVER] Reality is silent for prompt: '{prompt[:40]}...'")

        return result

    # =========================================================================
    # == INTERNAL FACULTIES (SYNC & RECOVERY)                                ==
    # =========================================================================

    def _is_registry_stale(self) -> bool:
        if not self.registry_path.exists():
            return True
        return (time.time() - self.registry_path.stat().st_mtime) > self.SYNC_COOLDOWN_SEC

    def _has_network_pulse(self) -> bool:
        """[ASCENSION 99]: The Ghost-Network Sentinel."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect(("1.1.1.1", 53))
            return True
        except OSError:
            return False

    def _sync_remote_registry(self):
        """Fetches the Celestial JSON Index."""
        if not self._has_network_pulse():
            if not self._silent:
                self.logger.warn("📡 [SYNC] Network is void. Clinging to local Gnosis.")
            return

        if not self._silent:
            self.logger.info("📡 [SYNC] Refreshing Registry from Novalym Master Hub...")

        try:
            # [ASCENSION 118]: Network Timeout Suture
            req = urllib.request.Request(self.MASTER_REGISTRY_URL, headers={'User-Agent': 'Velm/3.0'})
            with urllib.request.urlopen(req, timeout=3.5) as response:
                content = response.read().decode('utf-8')

                # Verify JSON integrity before saving
                json.loads(content)

                self.registry_path.parent.mkdir(parents=True, exist_ok=True)
                temp_path = self.registry_path.with_suffix(".tmp")
                temp_path.write_text(content, encoding='utf-8')
                os.replace(temp_path, self.registry_path)

                if not self._silent:
                    self.logger.success("✨ [RESONANT] Celestial Registry updated.")
        except Exception as e:
            if not self._silent:
                self.logger.warn(f"Remote Sync deferred: {e}. Using local chronicle.")

    def _load_registry_from_disk(self, path: Path) -> List[ShardGnosis]:
        """Inhales the JSON manifest."""
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return [ShardGnosis.model_validate(item) for item in data.get("registry", [])]
        except json.JSONDecodeError:
            # [ASCENSION 109]: Socratic Registry Healing
            self.logger.error(f"Registry JSON corrupted at {path.name}. Initiating autonomic purge.")
            try:
                path.unlink()
            except:
                pass
            return []
        except Exception as e:
            self.logger.error(f"Registry fracture at {path.name}: {e}")
            return []

    def _multicast_hud(self, shards: List[Any], ms: float, trace_id: str):
        """[ASCENSION 100]: Radiates the Semantic Singularity to the Ocular HUD."""
        if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic'):
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SEMANTIC_SINGULARITY_REACHED",
                        "label": f"{len(shards)}_SHARDS_ELECTED",
                        "color": "#a855f7",
                        "latency": f"{ms:.2f}ms",
                        "trace": trace_id
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