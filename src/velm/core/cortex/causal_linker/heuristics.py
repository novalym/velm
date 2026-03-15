# Path: core/cortex/causal_linker/heuristics.py
# ---------------------------------------------


"""
=================================================================================
== THE HEURISTIC ADJUDICATOR: APOTHEOSIS (V-Ω-TOTALITY-VMAX-GNOSTIC-ORACLE)    ==
=================================================================================
LIF: ∞^∞ | ROLE: CAPABILITY_ARBITRATION_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_HEURISTICS_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for capability arbitration. It has been
re-engineered to perform high-fidelity matching across the multiversal rift,
annihilating the 'Hyphen-Underscore' and 'Prefix-Namespace' paradoxes. It
establishes the Law of Genomic Normalization, ensuring that Shard IDs and
Abstract Capabilities resonate at the Absolute Semantic Root.
=================================================================================
"""

import re
import collections
import time
import hashlib
import threading
import math
from typing import List, Dict, Optional, Set, Tuple, Any, Final, Union

# --- CORE UPLINKS ---
from .contracts import ShardNode
from ....logger import Scribe

Logger = Scribe("HeuristicAdjudicator")


class ProviderAdjudicator:
    """
    =============================================================================
    == THE GNOSTIC ORACLE (V-Ω-CAPABILITY-ARBITRATOR)                          ==
    =============================================================================
    LIF: ∞ | ROLE: OPTIMAL_SHARD_SELECTOR | RANK: OMEGA_SUPREME

    The high-status judge that ensures the most resonant, elegant, and
    reliable shards are wove into the project's soul.
    """

    # [PHYSICS CONSTANTS]
    # The atomic sieve for semantic normalization
    NORMALIZATION_PATTERN: Final[re.Pattern] = re.compile(r'[^a-z0-9]')
    # The prefix incinerator (Covers all known Gnostic sigils)
    PREFIX_PATTERN: Final[re.Pattern] = re.compile(r'^(capability|logic|urn|shard|vow|trait):', re.IGNORECASE)

    # [ARCHITECTURAL JURISPRUDENCE]
    # Weighting the Strata of Reality
    TIER_GRAVITY: Final[Dict[str, float]] = {
        "soul": 10.0,  # Core Domain (Highest Priority)
        "mind": 5.0,  # Service Layer
        "body": 2.0,  # Infrastructure
        "iron": 1.0,  # Hardware / OS
        "void": 0.0  # Fractured matter
    }

    # [THE CURE: STRUCTURAL ENVELOPES]
    # Shards that can satisfy multiple realities simultaneously
    UNIVERSAL_ENVELOPES: Final[Set[str]] = {
        "docker", "kubernetes", "system", "bash", "shell",
        "terraform", "cloud", "iron", "agnostic", "universal"
    }

    OCULAR_ENVELOPES: Final[Set[str]] = {
        "react", "vue", "nextjs", "browser", "wasm",
        "ether", "ui", "ocular", "membrane"
    }

    def __init__(self, global_grimoire: List[ShardNode], engine: Optional[Any] = None):
        """
        [THE RITE OF ANCHORING]
        Initializes the Oracle and materializes the Normalized Capability Map.
        """
        self.engine = engine
        self.grimoire = global_grimoire
        self.logger = Logger

        # [ASCENSION 11 & 15]: HYDRAULIC ELECTION CACHE
        self._cache: Dict[str, ShardNode] = {}
        self._lock = threading.RLock()

        # --- THE MASTER CURE: ATOMIC SUTURE ---
        # Build the capability map immediately using the new Genomic Sieve.
        self.capability_map: Dict[str, List[ShardNode]] = self._build_normalized_map()

        # [ASCENSION 10]: MERKLE STATE FINGERPRINT
        self._state_hash = self._compute_state_hash()

    def _normalize(self, text: str) -> str:
        """
        =============================================================================
        == THE GENOMIC SIEVE (V-Ω-TOTALITY-PREFIX-ANNIHILATOR)                     ==
        =============================================================================
        [THE MASTER CURE]: This function is the single source of truth for resonance.
        1. Strips Gnostic Prefixes (capability:).
        2. Isolates the Geometric Tail (namespace/shard -> shard).
        3. Annihilates Delimiters (-, _, .).

        Example: 'system/python-core' -> 'pythoncore'
        Example: 'capability:python-core' -> 'pythoncore'
        """
        if not text:
            return ""

        # 1. Strip Prefixes (capability:docker -> docker)
        clean = self.PREFIX_PATTERN.sub('', text.strip())

        # 2. Extract Geometric Tail (system/pydantic-v2 -> pydantic-v2)
        # We only care about the atomic identity, not the namespace
        if '/' in clean:
            clean = clean.split('/')[-1]
        elif '\\' in clean:
            clean = clean.split('\\')[-1]

        # 3. Final Purgation (pydantic-v2 -> pydanticv2)
        # Lowers case and removes all non-alphanumeric matter
        return self.NORMALIZATION_PATTERN.sub('', clean.lower())

    def _build_normalized_map(self) -> Dict[str, List[ShardNode]]:
        """
        =============================================================================
        == THE NORMALIZED MAP FORGE (V-Ω-IMPLICIT-IDENTITY)                        ==
        =============================================================================
        [ASCENSION 3]: Every shard is its own leader. Automatically treats the
        Shard's ID as a primary provided capability, normalized to the Absolute Root.
        """
        cap_map = collections.defaultdict(list)

        for shard in self.grimoire:
            # 1. THE LAW OF IMPLICIT IDENTITY
            # The shard ID (minus namespace) is a primary capability.
            # Example: 'system/pydantic-v2' provides 'pydanticv2'
            norm_id = self._normalize(shard.id)
            cap_map[norm_id].append(shard)

            # 2. THE PROVIDES GAZE
            # Inhale all explicitly stated capabilities warded in the v3.0 Header.
            for cap in shard.provides:
                norm_cap = self._normalize(cap)
                if norm_cap != norm_id:
                    cap_map[norm_cap].append(shard)

        return dict(cap_map)

    def elect_best_provider(self, requirement: str, active_substrates: Set[str]) -> Optional[ShardNode]:
        """
        =============================================================================
        == THE RITE OF THE SUPREME ELECTION (V-Ω-TOTALITY-VMAX)                    ==
        =============================================================================
        LIF: ∞ | ROLE: OPTIMAL_SHARD_SELECTOR | RANK: OMEGA

        [THE MANIFESTO]
        Adjudicates the worth of candidate shards against the Architect's requirements
        using multidimensional gravity and DNA resonance.
        """
        # [ASCENSION 1]: GENOMIC NORMALIZATION
        norm_req = self._normalize(requirement)

        # --- MOVEMENT I: THE CACHE PROBE ---
        # [ASCENSION 15]: Hydraulic Cache
        # Cache Key = Requirement + Normalized Substrate Fingerprint
        sub_key = '|'.join(sorted([self._normalize(s) for s in active_substrates]))
        cache_key = f"{norm_req}:{sub_key}"

        with self._lock:
            if cache_key in self._cache:
                return self._cache[cache_key]

        # --- MOVEMENT II: CANDIDATE BIOPSY ---
        candidates = self.capability_map.get(norm_req, [])
        if not candidates:
            # [ASCENSION 16]: NoneType Sarcophagus
            return None

        # --- MOVEMENT III: THE SCALES OF JUDGMENT (SCORING) ---
        def rank_score(s: ShardNode) -> Tuple[Any, ...]:
            """
            =========================================================================
            == THE CALCULUS OF RESONANCE (V-Ω-VMAX)                                ==
            =========================================================================
            A multi-layered tuple used for sorting. Higher values win.
            """
            # 1. Substrate DNA Resonance (The Iron Rule)
            # [ASCENSION 3 & 5]: Normalize and check for Agnostic amnesty.
            s_subs = {self._normalize(sub) for sub in s.substrate}

            dna_gravity = 0
            if "agnostic" in s_subs or not s_subs.isdisjoint(active_substrates) or not active_substrates:
                dna_gravity = 3  # Perfect Language Match
            elif not s_subs.isdisjoint(self.UNIVERSAL_ENVELOPES):
                dna_gravity = 2  # Infrastructure Bridge
            elif not s_subs.isdisjoint(self.OCULAR_ENVELOPES):
                dna_gravity = 1  # Visual/UI Refraction

            # 2. Tier Sovereignty (The Law of Gravity)
            # [ASCENSION 2]: soul > mind > body > iron
            tier_val = self.TIER_GRAVITY.get(s.tier.lower(), 0.0)

            # 3. Modernity Matrix (SemVer)
            # [ASCENSION 18]: Higher versions of the same soul win ties.
            try:
                v_parts = s.version.split('.')
                version_tuple = tuple(int(p) if p.isdigit() else 0 for p in v_parts)
            except Exception:
                version_tuple = (1, 0, 0)

            # 4. Categorical Gravity [ASCENSION 19]
            category_boost = 1.0
            if self.engine and hasattr(self.engine, 'active_intent'):
                if s.category.lower() in str(self.engine.active_intent).lower():
                    category_boost = 2.5

            # 5. Elegance Factor (Complexity Sieve) [ASCENSION 5 & 14]
            # Fewer requirements = higher elegance.
            # We subtract requirements count from 100 to make it a reward.
            elegance = 100 - len(s.requires)

            # 6. Lexical/Neural Resonance
            # [ASCENSION 4]: Clamped score from the Resolver
            resonance = s.resonance_score or 0.0

            # RETURN THE ADJUDICATION TUPLE
            return (
                dna_gravity,  # 1st Priority: Does it run?
                tier_val,  # 2nd Priority: Is it foundational?
                resonance,  # 3rd Priority: Does it match the vibe?
                category_boost,  # 4th Priority: Is it in the right domain?
                elegance,  # 5th Priority: Is it simple?
                version_tuple  # 6th Priority: Is it modern?
            )

        # --- MOVEMENT IV: THE ELECTION ---
        # Sort candidates descending by their Gnostic Rank
        viable = sorted(candidates, key=rank_score, reverse=True)
        winner = viable[0]

        # =========================================================================
        # == MOVEMENT V: THE SURGICAL INCRIPTION (RATIONALE)                     ==
        # =========================================================================
        # [ASCENSION 12]: Socratic Reasoning
        # We record exactly why the Oracle chose this shard for the Forensic Ledger.
        winner.match_reason = (
            f"Elected to satisfy '{requirement}' | "
            f"Resonance: {winner.resonance_score:.2f} | "
            f"Tier: {winner.tier.upper()} | "
            f"Substrate Match: {'TRUE' if winner.substrate else 'AGNOSTIC'}"
        )

        # --- MOVEMENT VI: AKASHIC SYNC (HUD) ---
        # [ASCENSION 17 & 24]: Radiate the success peak to the UI
        self._radiate_election_pulse(winner, requirement)

        # 3. ENSHRINE IN CACHE
        with self._lock:
            # We cap cache mass to prevent memory fever
            if len(self._cache) > 2000:
                self._cache.clear()
            self._cache[cache_key] = winner

        return winner

    def _compute_state_hash(self) -> str:
        """
        =============================================================================
        == THE RITE OF THE MERKLE SEAL (V-Ω-TOTALITY)                             ==
        =============================================================================
        [ASCENSION 10]: Forges the Merkle Root of the active election matrix.
        Ensures structural integrity across multiversal timelines.
        """
        hasher = hashlib.sha256()
        # Sort capabilities to ensure deterministic hashing of the Mind
        for cap in sorted(self.capability_map.keys()):
            hasher.update(cap.encode('utf-8'))
            # Hash the number of providers for this capability
            hasher.update(str(len(self.capability_map[cap])).encode('utf-8'))
        return hasher.hexdigest()

    def _radiate_election_pulse(self, winner: ShardNode, requirement: str):
        """
        =============================================================================
        == THE OCULAR EVENT RADIATOR (V-Ω-TOTALITY-V86-HUD-MULTICAST)              ==
        =============================================================================
        LIF: ∞ | ROLE: ATMOSPHERIC_SIGNALER | RANK: MASTER
        """
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                trace_id = getattr(self.engine.context, 'session_id', 'tr-unbound')
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SHARD_ELECTED",
                        "label": f"RESONANCE_STRIKE: {requirement}",
                        "message": f"Candidate [cyan]{winner.id}[/] won election with {winner.resonance_score:.2f} confidence.",
                        "color": "#64ffda",
                        "trace": trace_id,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                # [ASCENSION 16]: THE UNBREAKABLE WARD
                # Telemetry failure must never compromise physical reality.
                pass

    def __repr__(self) -> str:
        status = "RESONANT" if self.capability_map else "VOID"
        return f"<Ω_HEURISTIC_ADJUDICATOR status={status} matrix_hash={self._state_hash[:12]} grimoire_mass={len(self.grimoire)}>"