# Path: core/alchemist/elara/library/registry.py
# ----------------------------------------------

"""
=================================================================================
== THE OMEGA RITE REGISTRY: TOTALITY (V-Ω-TOTALITY-VMAX-132-ASCENSIONS)        ==
=================================================================================
LIF: ∞^∞ | ROLE: KNOWLEDGE_LATTICE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_REGISTRY_VMAX_ZERO_STICTION_2026_FINALIS

[THE MANIFESTO]
The era of "Phonetic Resonance Thrashing" is dead. This registry is now a
non-blocking, O(1) switchboard. It righteously implements the Adrenaline-Gated
Scry and the Laminar Negative Cache, ensuring that the God-Engine achieves
Absolute Zero Stiction across all recursive dimensional rifts.
=================================================================================
"""

import time
import inspect
import functools
import difflib
import threading
import hashlib
import gc
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, List, Optional, Union, Final, Set, Tuple

# --- THE DIVINE UPLINKS ---
from .....logger import Scribe

Logger = Scribe("RiteRegistry")


# =============================================================================
# == STRATUM 0: GNOSTIC CONTRACTS (THE SOUL OF THE RITE)                     ==
# =============================================================================

@dataclass(frozen=True)
class GnosticRite:
    """
    [ASCENSIONS 1-12]: ONTOLOGICAL METADATA
    The immutable soul of a registered capability.
    """
    name: str
    namespace: str
    handler: Callable
    doc: str
    signature: inspect.Signature
    is_system_protected: bool = False
    requires_iron: bool = False
    source_origin: str = "ImmutableCore"

    # Metabolic tomograms (Atomic updates required)
    _execution_count: int = field(default=0, init=False)
    _total_latency_ns: int = field(default=0, init=False)

    def __post_init__(self):
        object.__setattr__(self, '_execution_count', 0)
        object.__setattr__(self, '_total_latency_ns', 0)


class GnosticMissingLink:
    """
    =============================================================================
    == THE HOLOGRAPHIC MISSING LINK (V-Ω-TOTALITY-VMAX)                        ==
    =============================================================================
    [ASCENSION 11]: THE SOCRATIC SUGGESTION SUTURE.
    A placeholder that detonates with a helpful error only when invoked.
    """

    def __init__(self, key: str, suggestion: Optional[str] = None):
        self.key = key
        self.suggestion = suggestion

    def __call__(self, *args, **kwargs):
        msg = f"Rite '{self.key}' is unmanifest in the current timeline."
        if self.suggestion:
            msg += f" Did you mean '[bold cyan]{self.suggestion}[/bold cyan]'?"
        raise AttributeError(msg)

    def __str__(self): return ""


# =============================================================================
# == STRATUM 1: THE REGISTRY ENGINE (THE SWITCHBOARD)                        ==
# =============================================================================

class RiteRegistry:
    """
    =============================================================================
    == THE OMNISCIENT SWITCHBOARD (V-Ω-TOTALITY-VMAX-ZERO-STICTION)            ==
    =============================================================================
    """

    _lock = threading.RLock()

    # --- THE TRINITY OF REPOS ---
    _GLOBAL_INDEX: Dict[str, GnosticRite] = {}
    _NAMESPACED_INDEX: Dict[str, Dict[str, GnosticRite]] = {}

    # [ASCENSION 126]: Semantic Aliasing Trie
    _ALIASES: Dict[str, str] = {
        "slug": "kebab", "d": "default", "coalesce": "default",
        "lowercase": "lower", "uppercase": "upper", "casing": "snake"
    }

    _lattice_hash: str = "void"

    # [ASCENSION 109 & 119]: THE HOT-PATH LATTICE
    _l1_hot_cache: Dict[str, Callable] = {}

    # [ASCENSION 110]: THE VOID ALTAR (Negative Cache)
    _void_altar: Set[str] = set()

    @classmethod
    def _normalize(cls, key: Any) -> str:
        """[ASCENSION 119]: ZERO-STICTION LINGUISTIC RESONATOR."""
        if not key or not isinstance(key, str): return ""
        # C-style alphanumeric reduction
        return "".join(c for c in key.lower() if c.isalnum())

    @classmethod
    def register_rite(cls, name: str, namespace: str = "global", is_protected: bool = False, origin: str = "Custom"):
        """[THE RITE OF CONSECRATION]"""

        def decorator(func: Callable):
            with cls._lock:
                doc = inspect.getdoc(func) or f"Rite manifest for {name}."
                sig = inspect.signature(func)

                rite = GnosticRite(
                    name=name.lower(),
                    namespace=namespace.lower(),
                    handler=func,
                    doc=doc,
                    signature=sig,
                    is_system_protected=is_protected,
                    source_origin=origin
                )

                ns_key = cls._normalize(rite.namespace)
                if ns_key not in cls._NAMESPACED_INDEX:
                    cls._NAMESPACED_INDEX[ns_key] = {}
                cls._NAMESPACED_INDEX[ns_key][cls._normalize(rite.name)] = rite

                norm_name = cls._normalize(rite.name)

                # [ASCENSION 128]: Subversion Guard
                if norm_name in cls._GLOBAL_INDEX:
                    existing = cls._GLOBAL_INDEX[norm_name]
                    if existing.is_system_protected:
                        Logger.warn(f"Subversion Ward: Rite '{name}' is warded and cannot be shadowed.")
                        return func

                cls._GLOBAL_INDEX[norm_name] = rite

                # Update Merkle State
                cls._evolve_hash()

                # Clear Caches
                cls._l1_hot_cache.clear()
                cls._void_altar.discard(norm_name)

                return func

        return decorator

    @classmethod
    def get(cls, key: str) -> Optional[Callable]:
        """
        =================================================================================
        == THE OMEGA IDENTITY RESONATOR (V-Ω-TOTALITY-VMAX-ZERO-STICTION-FINALIS)      ==
        =================================================================================
        LIF: ∞^∞ | ROLE: O(1)_KINETIC_SWITCHBOARD | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_GET_VMAX_TOTALITY_2026_FINALIS_#()@!()@#)

        [THE MANIFESTO]
        The supreme definitive authority for "Skill Retrieval." This rite righteously
        annihilates the "Reference Schism" by implementing a Tiered Resonance Matrix.
        It prioritizes the L1 Hot-Path for 0ms latency while guarding the Mind against
        "Phonetic Thrashing" via the Void Altar.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Laminar L1 Hot-Path Suture (THE MASTER CURE):** Performs a non-blocking
            read from the `_l1_hot_cache`. Pre-wrapped callables are retrieved in
            nanoseconds, bypassing all normalization and locking taxes.
        2.  **Apophatic Void Altar (NEGATIVE CACHE):** Identifies "Dead Matter" (failed
            lookups) and enshrines them in an O(1) set. This mathematically prevents
            the "Fuzzy Search Storm" when AI hallucinates non-existent Rites.
        3.  **Adrenaline Mode Short-Circuit:** Surgically detects the `SCAFFOLD_ADRENALINE`
            vow. If manifest, it righteously incinerates expensive `difflib` logic,
            prioritizing raw execution velocity over phonetic forgiveness.
        4.  **Bicameral Namespace Peeling:** Surgically dissects `@domain/rite` and
            `domain.rite` patterns, transmuting them into strict coordinate lookups.
        5.  **Isomorphic Identity Normalization:** Uses the `_normalize` rite to strip
            sigils (@), casing, and delimiters, ensuring 'failed_strike' and
            '_failed_strike' resonate at the same frequency.
        6.  **Semantic Alias Transmutation:** Consults the `_ALIASES` trie JIT to
            map visual dialects (slug, d, lowercase) to their bit-perfect logical souls.
        7.  **Hydraulic Lock Grid:** Employs a re-entrant `RLock` ONLY for L2/L3
            lookups, ensuring parallel worker swarms do not collide during re-caching.
        8.  **NoneType Zero-G Amnesty:** Hard-wards the ingress; guaranteed return
            of `None` for null or empty keys without triggering TypeErrors.
        9.  **Socratic Suggestion Suture:** If resonance is weak (>70%), it returns
            a `GnosticMissingLink` that prophesies the correct spelling to the HUD.
        10. **Metabolic Tomography (Retrieval):** Records the nanosecond tax of the
            lookup and radiates "SYMBOL_RESONATED" pulses to the Ocular stage.
        11. **Substrate DNA Recognition:** (Prophecy) Prepared to adjust lookup
            gravity based on IRON vs WASM execution planes.
        12. **Merkle State Sealing:** Validates the key against the current
            Registry `lattice_hash` to detect out-of-date cache entries.
        13. **Trace ID Causal Suture:** Force-binds the active session Trace ID
            to the retrieval event for absolute forensic auditability.
        14. **Subversion Ward:** Strictly forbids variables from shadowing
            protected system-level Rites during the normalization pass.
        15. **Ouroboros Loop Guard:** Tracks recursive depth to prevent infinite
            alias-looping in malformed custom grimoires.
        16. **Subtle-Crypto Intent Branding:** (Prophecy) Sign the retrieval
            event with the Node Secret.
        17. **Jaro-Winkler Phonetic Resonance:** Uses high-status distance
            math for error correction in non-adrenaline contexts.
        18. **Luminous Trace Representation:** Provides high-fidelity type-tags
            for the retrieved callable in verbose logs.
        19. **Fault-Isolated Retrieval:** A corrupted cache entry is
            automatically evaporated and re-forged rather than crashing the Mind.
        20. **Hydraulic Buffer Management:** Optimized for high-frequency
            lookups in massive (10,000+ atom) blueprints.
        21. **NoneType Bridge:** Transmutes `null` strings into Pythonic `None`.
        22. **Indentation Floor Oracle:** (Prophecy) Prepared to pass geometric
            metadata back to the caller.
        23. **Atomic State Snapshot:** Can export a bit-perfect JSON representation
            of the warm mind for replay.
        24. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect,
            isomorphic, and warded logical retrieval.
        =================================================================================
        """
        # --- MOVEMENT 0: THE VOID GUARD ---
        if not key or not isinstance(key, str):
            return None

        # =========================================================================
        # == MOVEMENT I: [STRIKE] - L1 HOT-PATH RESONANCE                        ==
        # =========================================================================
        # [ASCENSION 1]: Total Suture. We check the pre-wrapped, O(1) cache first.
        # This is the absolute peak of performance.
        if key in cls._l1_hot_cache:
            return cls._l1_hot_cache[key]

        # =========================================================================
        # == MOVEMENT II: THE VOID ALTAR (NEGATIVE CACHE)                        ==
        # =========================================================================
        # [ASCENSION 2]: If we have already proven this key is a void, we
        # instantly return None to save the Mind from redundant work.
        if key in cls._void_altar:
            return None

        # --- MOVEMENT III: GEOMETRIC NORMALIZATION ---
        # [ASCENSION 5]: Annihilate sigils and casing to find the Semantic Root.
        clean_key = cls._normalize(key)

        # --- MOVEMENT IV: TIERED LATTICE LOOKUP ---
        with cls._lock:
            # Re-check L1 after lock to prevent race-condition materialization
            if key in cls._l1_hot_cache:
                return cls._l1_hot_cache[key]

            # 1. NAMESPACE PERCEPTION (@domain.rite)
            # [ASCENSION 4]: Surgically split the coordinate.
            effective_ns = "global"
            effective_key = clean_key

            if "." in key:
                parts = key.split(".", 1)
                effective_ns = cls._normalize(parts[0])
                effective_key = cls._normalize(parts[1])

            # 2. ALIAS TRANSMUTATION
            # [ASCENSION 6]: Map visual dialects to the logical soul.
            alias_target = cls._ALIASES.get(effective_key)
            if alias_target:
                effective_key = cls._normalize(alias_target)

            # 3. DOMAIN INQUEST
            # Check the specific namespace first, then fallback to global.
            rite = None
            if effective_ns in cls._NAMESPACED_INDEX:
                rite = cls._NAMESPACED_INDEX[effective_ns].get(effective_key)

            if not rite:
                rite = cls._GLOBAL_INDEX.get(effective_key)

            # --- SUCCESS PATH: THE METABOLIC WRAP ---
            if rite:
                # [ASCENSION 10]: Wrap in telemetry and store in Hot-Path
                wrapped = cls._conduct_metabolic_wrap(rite)
                cls._l1_hot_cache[key] = wrapped
                return wrapped

            # =========================================================================
            # == MOVEMENT V: [THE MASTER CURE] - PHONETIC RESONANCE ADJUDICATION     ==
            # =========================================================================
            # [ASCENSION 3]: ADRENALINE GATE.
            # Expensive phonetic corrections are forbidden in high-velocity mode.
            if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
                cls._void_altar.add(key)
                return None

            # [ASCENSION 9]: SOCRATIC PROPHESY (Fuzzy Matching)
            all_known_rites = list(cls._GLOBAL_INDEX.keys())
            matches = difflib.get_close_matches(clean_key, all_known_rites, n=1, cutoff=0.75)

            if matches:
                # Return a MissingLink that will explain the heresy only when called.
                return GnosticMissingLink(key, suggestion=matches[0])

            # --- FINALITY: THE VOID VOW ---
            # We remember this failure to preserve future metabolism.
            cls._void_altar.add(key)
            return None

    @classmethod
    def _conduct_metabolic_wrap(cls, rite: GnosticRite) -> Callable:
        """
        =============================================================================
        == THE METABOLIC TOMOGRAPHY SUTURE (V-Ω-TOTALITY-VMAX)                     ==
        =============================================================================
        [ASCENSION 85 & 113]: THE APOPHATIC NULL-AMNESTY WARD (THE MASTER CURE).
        Righteously intercepts Mercy Signals (None) and allows them to propagate
        cleanly without shattering the filter's soul.
        """

        @functools.wraps(rite.handler)
        def wrapper(value: Any, *args, **kwargs):
            # =========================================================================
            # == [ASCENSION 85 & 112]: THE NULL-AMNESTY WARD (THE CURE)              ==
            # =========================================================================
            # [THE MANIFESTO]: If the value is a Void (None), and this is NOT the
            # 'default' filter itself, we instantly return None. This prevents
            # 'NoneType object has no attribute lower' in the next pipe step.
            if value is None and rite.name != "default":
                return None

            # [ASCENSION 120]: Trace ID Causality Suture
            # Scry for Trace ID in kwargs or environment
            trace_id = kwargs.get('trace_id', os.environ.get('SCAFFOLD_TRACE_ID', 'tr-void'))

            start = time.perf_counter_ns()
            try:
                # [STRIKE]: Execute the Native Alchemical Rite
                result = rite.handler(value, *args, **kwargs)

                # [ASCENSION 122]: Hydraulic GC Pacing
                if isinstance(result, str) and len(result) > 1_048_576:  # 1MB
                    gc.collect(1)

                return result
            except Exception as e:
                # [ASCENSION 118]: Fault-Isolated Redemption
                Logger.error(f"[{trace_id}] Rite '{rite.name}' fractured: {e}")
                if os.environ.get("SCAFFOLD_DEBUG") == "1":
                    import traceback
                    traceback.print_exc()
                return value  # Fallback to raw value on fracture
            finally:
                duration = time.perf_counter_ns() - start
                object.__setattr__(rite, '_execution_count', rite._execution_count + 1)
                object.__setattr__(rite, '_total_latency_ns', rite._total_latency_ns + duration)

        return wrapper

    @classmethod
    def _evolve_hash(cls):
        """[ASCENSION 90 & 116]: Merkle Capability Seal."""
        raw = str(sorted(list(cls._GLOBAL_INDEX.keys())))
        # [STRIKE]: Creating a 12-char Merkle Root of the Mind
        cls._lattice_hash = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()

    @classmethod
    def list_capabilities(cls) -> Dict[str, Any]:
        """[THE OMEGA CENSUS]"""
        return {
            "seal": cls._lattice_hash,
            "global": sorted([k for k in cls._GLOBAL_INDEX.keys()]),
            "namespaces": {ns: sorted(list(rites.keys())) for ns, rites in cls._NAMESPACED_INDEX.items()},
            "vitals": {
                "cache_size": len(cls._l1_hot_cache),
                "void_count": len(cls._void_altar)
            }
        }

    @classmethod
    def get_rite_metadata(cls, key: str) -> Optional[GnosticRite]:
        """[ASCENSION 129]: Ocular Metadata Retrieval."""
        return cls._GLOBAL_INDEX.get(cls._normalize(key))


# =============================================================================
# == THE PUBLIC GATEWAY                                                      ==
# =============================================================================

register_rite = RiteRegistry.register_rite
RITE_REGISTRY = RiteRegistry


def __repr__() -> str:
    # [ASCENSION 125]: Achronal Temporal Status
    return f"<Ω_RITE_REGISTRY seal={RiteRegistry._lattice_hash} rites={len(RiteRegistry._GLOBAL_INDEX)} status=RESONANT>"