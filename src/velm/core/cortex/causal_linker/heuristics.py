# Path: core/cortex/causal_linker/heuristics.py
# ---------------------------------------------

"""
=================================================================================
== THE HEURISTIC ADJUDICATOR: ZENITH (V-Ω-TOTALITY-VMAX-VOID-SHIELDED-FINALIS) ==
=================================================================================
LIF: ∞^∞^∞ | ROLE: OPTIMAL_SHARD_SELECTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_HEURISTICS_VMAX_VOID_SHIELD_2026_FINALIS

[THE MANIFESTO]
The supreme final authority for architectural election. This version righteously
implements the **Apophatic Void Shield**, mathematically annihilating the
'NoneType' AttributeError by enforcing safe sensory scrying through the
Kernel's mental strata.

It fuses the parallel SIMD power of the Rust Iron with an indestructible Python
Prophet. It mathematically guarantees that no logic from the SemanticResolver,
the GnosticTensor, or the StructureSentinel is bypassed. It exists solely to
rank and elect shards with Absolute Precision.

Axiom Zero: The Mind shall not fracture even if the Body is unmanifest.
=================================================================================
"""

import re
import collections
import time
import hashlib
import threading
import os
from typing import List, Dict, Optional, Set, Tuple, Any, Final

# --- CORE UPLINKS ---
from .contracts import ShardNode
from .heuristics_data import TECH_SYNERGY, SOVEREIGN_HEARTS, AXIOMATIC_STRATA, REALM_GRAVITY
from ....logger import Scribe

# [ASCENSION 1]: THE BINARY KERNEL PIVOT
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("HeuristicAdjudicator")


class ProviderAdjudicator:
    """
    =============================================================================
    == THE OMEGA PROVIDER ADJUDICATOR (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE)       ==
    =============================================================================
    LIF: 1,000,000,000x | ROLE: ARCHITECTURAL_PROPHET | RANK: OMEGA_SOVEREIGN
    """

    # [PHYSICS CONSTANTS]
    NORMALIZATION_PATTERN: Final[re.Pattern] = re.compile(r'[^a-z0-9]')
    PREFIX_PATTERN: Final[re.Pattern] = re.compile(r'^(capability|logic|urn|shard|vow|trait|dna):', re.IGNORECASE)

    # [THE CURE: STRUCTURAL ENVELOPES]
    UNIVERSAL_ENVELOPES: Final[Set[str]] = {
        "docker", "kubernetes", "system", "bash", "shell", "terraform", "cloud", "iron", "agnostic"
    }

    OCULAR_ENVELOPES: Final[Set[str]] = {
        "react", "vue", "nextjs", "browser", "wasm", "ether", "ui", "ocular", "membrane"
    }

    # [ASCENSION 3]: O(1) LAMINAR NORMALIZATION CACHE
    _NORM_CACHE: Dict[str, str] = {}
    _NORM_LOCK = threading.RLock()

    __slots__ = (
        'engine', 'grimoire', 'logger', '_cache', '_lock', 'capability_map',
        '_state_hash', '_shard_subs_cache', '_rust_oracle', '_is_wasm'
    )

    def __init__(self, global_grimoire: List[ShardNode], engine: Optional[Any] = None):
        """[THE RITE OF ANCHORING]"""
        self.engine = engine
        self.grimoire = global_grimoire
        self.logger = Logger
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        self._cache: Dict[str, ShardNode] = {}
        self._shard_subs_cache: Dict[str, Set[str]] = {}
        self._lock = threading.RLock()
        self._rust_oracle = None

        # --- MOVEMENT I: TOPOLOGICAL DNA MAPPING ---
        self.capability_map: Dict[str, List[ShardNode]] = self._build_normalized_map()
        self._state_hash = self._compute_state_hash()

        # =========================================================================
        # == MOVEMENT II: [ASCENSION 57] - QUANTUM SUBSTRATE SUTURE (RUST)       ==
        # =========================================================================
        if RUST_AVAILABLE and not self._is_wasm:
            try:
                self._rust_oracle = scaffold_core_rs.QuantumAdjudicator()

                rust_payload = []
                for s in self.grimoire:
                    rust_payload.append({
                        "id": s.id,
                        "tier": s.tier,
                        "provides": s.provides,
                        "substrate": s.substrate,
                        "requires": s.requires,  # [THE FIX]: Passing explicit requirements array
                        "version": s.version,
                        "resonance_score": getattr(s, 'resonance_score', 0.0),
                        "semantic_vector": getattr(s, 'semantic_vector', None)
                    })

                self._rust_oracle.ingest_grimoire(rust_payload)
                self.logger.verbose("Quantum Adjudicator (Rust) engaged. Parallel SIMD active.")
            except Exception as e:
                self.logger.debug(f"Quantum Adjudicator deferred: {e}. Clinging to Python Prophet.")
                self._rust_oracle = None

    # =========================================================================
    # ==[THE MASTER CURE]: THE APOPHATIC VOID SHIELD                        ==
    # =========================================================================

    @property
    def variables_altar(self) -> Dict[str, Any]:
        """
        [ASCENSION 1]: THE INDESTRUCTIBLE SENSORY BRIDGE.
        Righteously uses `getattr` to scry the Engine's variable altar.
        Mathematically annihilates the 'NoneType' attribute heresy.
        """
        # We attempt to pierce the Engine's mind. If it is a Void (None),
        # we return a bit-perfect empty dictionary to prevent the fracture.
        return getattr(self.engine, 'variables', {})

    @property
    def is_silent(self) -> bool:
        """[ASCENSION 2]: Safe scrying for the Vow of Silence."""
        if os.environ.get("SCAFFOLD_SILENT") == "1":
            return True
        # Scry the altar safely
        return bool(self.variables_altar.get('silent', False))

    @property
    def active_trace(self) -> str:
        """[ASCENSION 3]: Safe scrying for the Silver Cord."""
        return str(self.variables_altar.get('trace_id', 'tr-adjudicator-void'))

    # =========================================================================
    # == STRATUM I: NORMALIZATION & MAPPING                                  ==
    # =========================================================================

    @classmethod
    def _normalize(cls, text: str) -> str:
        """[ASCENSION 36]: O(1) LAMINAR NORMALIZATION CACHE."""
        if not text: return ""

        cached = cls._NORM_CACHE.get(text)
        if cached is not None: return cached

        with cls._NORM_LOCK:
            cached = cls._NORM_CACHE.get(text)
            if cached is not None: return cached

            # 1. Strip Prefixes
            clean = cls.PREFIX_PATTERN.sub('', text.strip())
            # 2. Extract Geometric Tail
            if '/' in clean:
                clean = clean.split('/')[-1]
            elif '\\' in clean:
                clean = clean.split('\\')[-1]
            # 3. Final Purgation
            result = cls.NORMALIZATION_PATTERN.sub('', clean.lower())

            if len(cls._NORM_CACHE) > 10000: cls._NORM_CACHE.clear()
            cls._NORM_CACHE[text] = result
            return result

    def _build_normalized_map(self) -> Dict[str, List[ShardNode]]:
        cap_map = collections.defaultdict(list)
        DELIMITER_PATTERN = re.compile(r'[/\-_\.]')

        for shard in self.grimoire:
            norm_subs = {self._normalize(sub) for sub in shard.substrate if isinstance(sub, str)}
            self._shard_subs_cache[shard.id] = norm_subs

            raw_intent_sources = shard.provides + [shard.id]

            for raw_cap in raw_intent_sources:
                if not raw_cap: continue
                norm_full = self._normalize(raw_cap)
                cap_map[norm_full].append(shard)

                segments = DELIMITER_PATTERN.split(raw_cap)
                if len(segments) > 1:
                    for i in range(1, len(segments)):
                        stem = "/".join(segments[:i])
                        cap_map[self._normalize(stem)].append(shard)
                        alt_stem = "-".join(segments[:i])
                        cap_map[self._normalize(alt_stem)].append(shard)

                for atom in segments:
                    if len(atom) > 2:
                        norm_atom = self._normalize(atom)
                        if norm_atom not in cap_map or shard not in cap_map[norm_atom]:
                            cap_map[norm_atom].append(shard)

        return dict(cap_map)

    # =========================================================================
    # == STRATUM II: THE OMEGA PROVIDER ELECTION                             ==
    # =========================================================================

    def elect_best_provider(
            self,
            requirement: str,
            active_substrates: Set[str],
            active_nodes: Optional[Dict[str, Any]] = None,
            banned_capabilities: Optional[Set[str]] = None,
            query_dense: Optional[List[float]] = None,
            query_sparse_tokens: Optional[List[str]] = None
    ) -> Optional[ShardNode]:
        """
        =================================================================================
        == THE OMEGA PROVIDER ELECTION: TOTALITY (V-Ω-VMAX-AXIOMATIC-SUTURE)           ==
        =================================================================================
        LIF: ∞^∞^∞ | ROLE: OPTIMAL_SHARD_SELECTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME

        [THE MANIFESTO]
        This method perfectly bridges the Python Semantic Resolver with the Rust Core.
        It forwards the Dense and Sparse vectors untouched, guaranteeing absolute
        fidelity of intention.
        """
        _start_ns = time.perf_counter_ns()
        trace_id = self.active_trace

        if not requirement: return None

        # --- MOVEMENT 0: TOPOLOGICAL PURIFICATION ---
        norm_req = self._normalize(requirement)
        norm_active_subs = {self._normalize(s) for s in active_substrates}
        norm_bans = {self._normalize(b) for b in (banned_capabilities or set())}

        # [ASCENSION 12]: Merkle Intent Cache Key
        sub_fingerprint = hashlib.md5("".join(sorted(list(norm_active_subs))).encode()).hexdigest()[:4]
        ban_fingerprint = hashlib.md5("".join(sorted(list(norm_bans))).encode()).hexdigest()[:4]
        cache_key = f"Ω_PROPHET:{norm_req}:{sub_fingerprint}:{ban_fingerprint}"

        with self._lock:
            if cache_key in self._cache: return self._cache[cache_key]

        # --- MOVEMENT I: DNA & SYNERGY EXTRACTION ---
        willed_shards = list(active_nodes.keys()) if active_nodes else []

        # 1. Determine Dominant Language DNA
        lang_dist = collections.defaultdict(int)
        has_sovereign_heart = False
        for aid in willed_shards:
            s_obj = next((s for s in self.grimoire if s.id == aid), None)
            if s_obj:
                for sub in s_obj.substrate:
                    if sub != "agnostic": lang_dist[sub.lower()] += 1

                # HEART DETECTION (Pauli V3)
                role = str(getattr(s_obj.suture, 'role', 'file')).lower()
                if any(h in role for h in ("heart", "base-api", "citadel", "gateway")):
                    has_sovereign_heart = True

        dominant_lang = max(lang_dist, key=lang_dist.get) if lang_dist else None

        # 2. Project Centroid Preparation (Neural)
        project_centroid = None
        if active_nodes:
            active_vectors = [n.semantic_vector for n in active_nodes.values() if
                              hasattr(n, 'semantic_vector') and n.semantic_vector]
            if active_vectors:
                dim = len(active_vectors[0])
                project_centroid = [sum(v[i] for v in active_vectors) / len(active_vectors) for i in range(dim)]

        # =========================================================================
        # == MOVEMENT II: [STRIKE] - THE IRON ORACLE (RUST ZENITH PATH)          ==
        # =========================================================================
        if self._rust_oracle:
            try:
                # The Python Cortex successfully passes the Dense AND Sparse matrices down into the Iron
                winner_id = self._rust_oracle.elect_best_provider(
                    requirement,
                    list(active_substrates),
                    list(banned_capabilities or set()),
                    project_centroid,
                    willed_shards,
                    query_dense,
                    query_sparse_tokens.copy() if query_sparse_tokens else []
                )
                if winner_id:
                    winner = next((s for s in self.grimoire if s.id == winner_id), None)
                    if winner:
                        return self._finalize_and_cache(winner, requirement, cache_key, _start_ns, trace_id,
                                                        "Quantum Oracle")
            except Exception as rust_fracture:
                self.logger.debug(f"Iron Oracle fractured: {rust_fracture}. Devolving to Python Matrix.")

        # =========================================================================
        # == MOVEMENT III: THE PYTHON PROPHET (AXIOMATIC REINFORCED)             ==
        # =========================================================================
        # This fallback mirrors the exact math of the Rust Adjudicator, guaranteeing
        # safety if running in WASM or if the native extension fails.

        candidates = self.capability_map.get(norm_req)
        if not candidates: return None

        # 1.[ASCENSION 1]: THE PAULI EXCLUSION SIEVE (Axiomatic Aware)
        viable_candidates = []
        for cand in candidates:
            # =====================================================================
            # == AXIOMATIC SOVEREIGN IMMUNITY (RESTORES 104-SHARD DENSITY)       ==
            # =====================================================================
            # Testing, Security, and CI are Bedrock Axioms. They bypass all competitive pruning.
            is_axiomatic = any(cand.id.startswith(p) for p in
                               ("tests/", "test-utils/", "scripts/security/", "ci/", ".github/", ".scaffold/"))

            if not is_axiomatic:
                # Pauli V3: Prevent Heart-Tier collisions (Chimera State)
                role = str(getattr(cand.suture, 'role', 'file')).lower()
                if has_sovereign_heart and any(h in role for h in ("heart", "base-api", "citadel")):
                    continue

                # Standard Competitive Excommunication
                cand_norm_id = self._normalize(cand.id)
                if cand_norm_id in norm_bans: continue

                cand_caps = {self._normalize(c) for c in cand.provides}
                if not cand_caps.isdisjoint(norm_bans): continue

            viable_candidates.append(cand)

        if not viable_candidates: return None
        if len(viable_candidates) == 1:
            return self._finalize_and_cache(viable_candidates[0], requirement, cache_key, _start_ns, trace_id,
                                            "Sole Provider")

        # 2. [ASCENSION 4-7]: THE CALCULUS OF SUPREME ARCHITECTURE
        def rank_score(s: ShardNode) -> Tuple[Any, ...]:
            s_subs = self._shard_subs_cache.get(s.id,
                                                {self._normalize(sub) for sub in s.substrate if isinstance(sub, str)})

            # A. Geometric Substrate Resonance
            sub_gravity = 0
            if "agnostic" in s_subs or not norm_active_subs or not s_subs.isdisjoint(norm_active_subs):
                sub_gravity = 5000.0
            elif not s_subs.isdisjoint(self.UNIVERSAL_ENVELOPES):
                sub_gravity = 2500.0

            # Language Bias Enforcement
            if dominant_lang and dominant_lang not in s_subs and "agnostic" not in s_subs:
                sub_gravity -= 2000.0

            # B. [ASCENSION 2]: ZENITH AXIOM BOOST (+50,000.0 Magnitude)
            # This mathematically ensures that Tests and Security outrank random utils
            axiom_boost = 50000.0 if any(s.id.startswith(p) for p in
                                         ("tests/", "test-utils/", "scripts/security/", "ci/", ".github/",
                                          ".scaffold/")) else 0.0

            # C. Synaptic Synergy [ASCENSION 5]
            synergy_multiplier = 1.0
            for aid in willed_shards:
                if aid in TECH_SYNERGY and s.id in TECH_SYNERGY[aid]:
                    synergy_multiplier += 2.0

            # D.[ASCENSION 7]: Matter Density (Form weight)
            # Higher provided atom count = higher density = better shard.
            density_factor = (len(s.provides) + 1) * 10.0

            # E. Neural Cohesion (SIMD Dot Product Equivalent for Python)
            cohesion = 0.0
            if project_centroid and hasattr(s, 'semantic_vector') and s.semantic_vector:
                cohesion = sum(a * b for a, b in zip(project_centroid, s.semantic_vector))

            # F. Topological Prophecy (Lookahead Equivalent)
            prophecy_boost = getattr(s, 'potential_unlocks', 0) * 35.0

            # G. Sparse Keyword Intersection (If Query Tokens available)
            sparse_score = 0.0
            if query_sparse_tokens:
                query_set = set(query_sparse_tokens)
                shard_set = set(s.provides)
                intersection = len(query_set.intersection(shard_set))
                sparse_score = intersection * 25.0

            # [STRIKE]: Final Magnitude Fusion
            magnitude = (
                    (sub_gravity * synergy_multiplier) +
                    axiom_boost +
                    (REALM_GRAVITY.get(s.tier.lower(), 0.0) * 200.0) +
                    (getattr(s, 'resonance_score', 0.0) * 100.0) +
                    (cohesion * 50.0) +
                    sparse_score +
                    prophecy_boost +
                    density_factor +
                    (200.0 - len(s.requires))
            )

            try:
                version_tuple = tuple(int(p) if p.isdigit() else 0 for p in s.version.split('.'))
            except:
                version_tuple = (1, 0, 0)

            return (magnitude, version_tuple)

        # 3. THE FINAL ELECTION
        sorted_candidates = sorted(viable_candidates, key=rank_score, reverse=True)
        winner = sorted_candidates[0]

        return self._finalize_and_cache(winner, requirement, cache_key, _start_ns, trace_id, "Python Prophet")

    def _finalize_and_cache(self, winner: ShardNode, requirement: str, cache_key: str,
                            start_ns: int, trace_id: str, logic_path: str) -> ShardNode:
        """[THE FINALITY SUTURE]"""
        shard_role = str(getattr(winner.suture, 'role', 'file')).lower()
        if any(h in shard_role for h in ("heart", "base-api", "citadel")):
            winner.match_reason = f"Zenith Sovereign Elected: {winner.id}"
        else:
            winner.match_reason = f"Synaptic Resonance Match (Via {logic_path})"

        # Radiate Pulse to HUD
        if not self.is_silent:
            self._radiate_election_pulse(winner, requirement)

        _tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if _tax_ms > 5.0 and not self.is_silent:
            self.logger.verbose(f"L? Zenith Election for '{requirement}' concluded in {_tax_ms:.2f}ms.")

        # Update Cache
        with self._lock:
            if len(self._cache) > 5000: self._cache.clear()
            self._cache[cache_key] = winner

        return winner

    def _compute_state_hash(self) -> str:
        hasher = hashlib.sha256()
        for cap in sorted(self.capability_map.keys()):
            hasher.update(cap.encode('utf-8'))
            hasher.update(str(len(self.capability_map[cap])).encode('utf-8'))
        return hasher.hexdigest()

    def _radiate_election_pulse(self, winner: ShardNode, requirement: str):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SHARD_ELECTED",
                        "label": f"RESONANCE_STRIKE: {requirement}",
                        "message": f"Candidate [cyan]{winner.id}[/] won election.",
                        "color": "#64ffda",
                        "trace": self.active_trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        engine_mode = "QUANTUM_IRON" if self._rust_oracle else "PYTHON_MATRIX"
        return f"<Ω_HEURISTIC_ADJUDICATOR status=RESONANT mode={engine_mode} mass={len(self.grimoire)}>"