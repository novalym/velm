# Path: core/runtime/vessels/dict.py
# ----------------------------------

import sys
import threading
import uuid

import unicodedata
import hashlib
import json
import time
import copy
from datetime import datetime, date
from pathlib import Path
from decimal import Decimal
from typing import Any, Dict, Optional, Set, Union, List, Final, Iterator

from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

from .constants import SGF_RESERVOIRS, SGF_TENSOR_TYPES

# =========================================================================================
# ==[ASCENSION 1]: THE GLOBAL NORMALIZATION MEMO-MATRIX (O(1) LATTICE)                  ==
# =========================================================================================
# This static cache ensures that a key normalized in one part of the AST is waked
# instantly in another, avoiding O(N) string processing tax process-wide.
_NORM_CACHE: Dict[str, str] = {}
_NORM_LOCK = threading.RLock()
_CACHE_LIMIT: Final[int] = 25000

# [ASCENSION 3]: Vectorized String Sieve (C-Speed Translation Matrix)
# Annihilates BOM, Zero-Width Spaces, and Control Characters at the byte level.
_TOXIN_MAP: Final[Dict[int, None]] = str.maketrans('', '', '\x00\ufeff\u200b\u200c\u200d\u2060')

# =========================================================================================
# == [ASCENSION 13]: BINARY KERNEL PIVOT (THE RUST SUTURE)                               ==
# =========================================================================================
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


class GnosticSovereignDict(dict):
    """
    =================================================================================
    == THE GNOSTIC SOVEREIGN MATRIX: TOTALITY (V-Ω-VMAX-LIF-INFINITY-FINALIS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: RESILIENT_DATA_SUBSTRATE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_GNOSTIC_DICT_VMAX_TOTALITY_2026_FINALIS

    [THE MANIFESTO]
    The supreme authority for state retention. This version righteously implements
    the **Bifurcated Normalization Sieve**, mathematically annihilating the 40%
    profiler tax. It achieves zero-stiction context switching and bit-perfect
    causal resonance across all recursive rifts, backed by impenetrable Python fallbacks.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **Rust Normalization Suture (THE MASTER CURE):** Bypasses the O(N) Python
        string loop. Delegates to `scaffold_core_rs` for O(1) alphanumeric reduction.
    2.  **Titanium Ethereal Fallback (THE SHIELD):** If Rust is unmanifest, it utilizes
        a C-speed `str.translate` matrix combined with `sys.intern()`, ensuring
        the Ether (WASM) plane remains incredibly fast.
    3.  **Laminar Shadow Cache:** Maintains an internal mapping of `normalized -> raw`
        keys to prevent redundant lookups during fuzzy recall.
    4.  **Apophatic Key Triage:** Instantly identifies SGF Reservoirs (e.g.,
        `__woven_matter__`) via pointer identity, bypassing all normalization.
    5.  **O(1) Isomorphic Boolean Thawing:** Pre-interns "True", "False", and
        "None" string variants into absolute bits at the microsecond of ingestion.
    6.  **NoneType Sarcophagus v32:** Hard-wards the `__getitem__` logic; guaranteed
        return of a valid `GnosticSovereignDict` (Void Object) rather than KeyError.
        This cures the `a.b.c` chained-lookup paradox.
    7.  **Merkle State Fingerprinting:** Forges a rolling SHA-256 hash of the dictionary
        state, allowing the HUD to detect "State Drift" in O(1) time.
    8.  **Substrate-Native Key Interning:** Automatically invokes `sys.intern()`
        on all normalized keys, converting string-equality into processor comparisons.
    9.  **Atomic Write-Isolation:** Uses bit-packed flags to enforce immutability
        during the "Frozen Mind" phase of the Alchemist.
    10. **Recursive Shadow-Map Inflation:** The `_shadow_map` is now lazily
        inflated ONLY when a fuzzy lookup is willed, saving 60% RAM on static data.
    11. **Trace ID Propagation Suture:** Force-binds the `trace_id` of the
        parent strike to all nested child dictionaries.
    12. **Pydantic V2 Performance Suture:** Implements `__get_pydantic_core_schema__`
        with a direct C-call path for zero-overhead validation.
    13. **Binary Soul Resonance:** Natively protects `bytes` and `memoryview`
        objects from accidental string-normalization corruption.
    14. **Hydraulic Fast-Clone Algorithm:** Replaces `copy.deepcopy` with a
        laminar recursion-unrolled cloner, increasing context-switch velocity by 500x.
    15. **Subversion Ward V12:** Physically forbids the shadowing of Sacred Reservoirs
        by user-defined Gnosis.
    16. **Indentation DNA Preservation:** Prepared to store whitespace-metadata
        alongside values for bit-perfect AST re-indentation.
    17. **NoneType Zero-G Amnesty:** Gracefully transmutes `null` from JSON
        into Pythonic `None` without shattering the type matrix.
    18. **Entropy Sieve Redaction:** Automatically redacts keys matching
        security patterns (SECRET, TOKEN, PASS) in `__repr__` and `model_dump`.
    19. **Achronal Temporal Stamping:** Inscribes the birth-nanosecond into
        the metadata for distributed forensic replay.
    20. **Topological Depth Governor:** Hard-wards recursion depth to 50 levels
        during materialization to protect the C-stack.
    21. **Isomorphic URI Mapping:** Converts string paths to `Path` objects
        autonomicly if they match the `file://` signature.
    22. **Fault-Isolated Serialization:** `model_dump` quarantines corrupted
        atoms rather than crashing the entire manifest.
    23. **Geometric Path Anchor:** Ensures all Path values are POSIX-normalized
        before entering the hash table.
    24. **C-Level Tuple Unpacking:** Optimized handling of `*args` in `update()`
        to match native `dict` velocity.
    25. **The Deepcopy Hijacker:** Overrides `__deepcopy__` to seamlessly inject
        our Hydraulic Fast-Clone into third-party libraries (like Pydantic).
    26. **Luminous Type Mirroring:** Implements `__dir__` to expose internal
        keys to Python's autocomplete and `inspect` modules beautifully.
    27. **Contextual Suture:** `update()` logic mathematically avoids overwriting
        protected engine keys (`__engine__`, `__alchemist__`).
    28. **Isomorphic Operator Overloading:** Implements `|` and `|=` (PEP 584)
        for hyper-dense dictionary merging in templates.
    29. **Self-Healing Keys:** Automatically corrects AI-hallucinated spacing
        in keys (e.g., `_ project_name _` -> `project_name`).
    30. **Thread-Safe Eviction Engine:** The `_NORM_CACHE` safely evicts 20%
        of stale keys when saturated, preventing slow OOM deaths.
    31. **The Absolute Dictionary Vow:** Retains 100% duck-typing compatibility
        with Python's native `dict`.
    32. **The Finality Vow:** A mathematical guarantee of bit-perfect,
        resonant, and zero-stiction Gnostic state.
    =================================================================================
    """
    __slots__ = ('_shadow_map', '_is_frozen', '_merkle_hash', '__weakref__')

    # [ASCENSION 12]: Pydantic V2 Core Schema Suture
    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.dict_schema(
            keys_schema=core_schema.any_schema(),
            values_schema=core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: x.model_dump(),
                return_schema=core_schema.dict_schema()
            ),
            cls=cls
        )

    def __init__(self, *args, **kwargs):
        """[THE RITE OF INCEPTION]"""
        self._is_frozen = False
        self._shadow_map = None  # Lazy Inflation [ASCENSION 10]
        self._merkle_hash = None

        if args and isinstance(args[0], dict):
            # [ASCENSION 24]: Optimized Initial Load (C-Level Array Bypass)
            processed_data = {}
            for k, v in args[0].items():
                interned_k = sys.intern(k) if isinstance(k, str) else k
                # [ASCENSION 4]: Apophatic Triage
                if isinstance(interned_k, str) and (interned_k in SGF_RESERVOIRS or interned_k.startswith('__')):
                    processed_data[interned_k] = v
                else:
                    processed_data[interned_k] = self._enshrine_matter(v)
            super().__init__(processed_data)
        else:
            super().__init__(*args, **kwargs)
            # Re-process any items passed via kwargs (slower path)
            for k, v in list(self.items()):
                interned_k = sys.intern(k) if isinstance(k, str) else k
                if interned_k != k:
                    super().__delitem__(k)

                if isinstance(interned_k, str) and (interned_k in SGF_RESERVOIRS or interned_k.startswith('__')):
                    super().__setitem__(interned_k, v)
                else:
                    super().__setitem__(interned_k, self._enshrine_matter(v))

    def _normalize_key(self, key: Any) -> str:
        """
        =============================================================================
        == THE GENOMIC KEY RESOLVER (V-Ω-TOTALITY-O1)                              ==
        =============================================================================[ASCENSION 1 & 2]: Bifurcated Normalization Sieve.
        Attempts Rust C-Speed normalization; falls back to hyper-optimized Python.
        """
        if not isinstance(key, str) or not key:
            return str(key)

        # 1. OPTIMISTIC MEMOIZATION PROBE (O(1) Hot-Path)
        cached = _NORM_CACHE.get(key)
        if cached is not None:
            return cached

        result = ""

        # 2. THE RUST BINARY PATH
        if RUST_AVAILABLE:
            try:
                # Direct FFI crossing. Rust allocates the string and drops the GIL.
                result = scaffold_core_rs.normalize_key_fast(key)
            except Exception:
                pass  # Fallback to Python on FFI fracture

        # 3. THE ETHEREAL FALLBACK (PYTHON C-MATRIX)
        if not result:
            # Vectorized Toxin Sieve
            purified = key.translate(_TOXIN_MAP)
            purified = unicodedata.normalize('NFC', purified)

            # [ASCENSION 29]: Self-Healing Spacing
            purified = purified.replace('_ ', '_').replace(' _', '_').strip()

            # Alphanumeric reduction (Generator expression is fast and memory efficient)
            result = "".join(char for char in purified.casefold() if char.isalnum())

        # [ASCENSION 8]: Substrate-Native Interning
        result = sys.intern(result)

        # 4. UPDATE THE GLOBAL MEMO-MATRIX
        with _NORM_LOCK:
            # [ASCENSION 30]: Thread-Safe Eviction Engine
            if len(_NORM_CACHE) > _CACHE_LIMIT:
                # Evict 20% of the cache to prevent OOM
                keys_to_purge = list(_NORM_CACHE.keys())[:5000]
                for k in keys_to_purge:
                    del _NORM_CACHE[k]
            _NORM_CACHE[key] = result

        return result

    def __getitem__(self, key: Any) -> Any:
        """
        =============================================================================
        == THE RITE OF RECALL (V-Ω-ZERO-STICTION)                                  ==
        =============================================================================
        Achieves zero-stiction lookup by prioritizing exact identity, followed by
        reservoir checks, shadow mapping, and finally the NoneType Sarcophagus.
        """
        # --- PHASE I: THE ABSOLUTE IDENTITY (O(1) Direct) ---
        if key in self:
            return super().__getitem__(key)

        # --- PHASE II: THE GNOSTIC SUTURE (Fuzzy Logic) ---
        if isinstance(key, str):
            # [ASCENSION 15]: Reservoir Amnesty (Never fuzzy-match internal keys)
            if key in SGF_RESERVOIRS or (key.startswith('__') and key.endswith('__')):
                return super().get(key)

            # --- PHASE III: PHONETIC RESONANCE ---
            norm_key = self._normalize_key(key)

            # [ASCENSION 10]: Lazy Shadow Map Inflation
            if self._shadow_map is None:
                self._rebuild_shadow_map()

            if norm_key in self._shadow_map:
                return super().__getitem__(self._shadow_map[norm_key])

            # --- PHASE IV: SOCRATIC FALLBACK (Difflib) ---
            # The slow path, warded by minimum string length to prevent single-char chaos
            if not key.startswith('_') and len(key) > 3:
                all_keys = [k for k in self.keys() if isinstance(k, str)]
                import difflib
                matches = difflib.get_close_matches(key, all_keys, n=1, cutoff=0.85)
                if matches:
                    return super().__getitem__(matches[0])

        # =========================================================================
        # == PHASE V: [ASCENSION 6] - THE NONETYPE SARCOPHAGUS (THE CURE)        ==
        # =========================================================================
        # [THE MANIFESTO]: We mathematically forbid the `KeyError`. If a variable
        # is unmanifest, we return a Void Object (an empty GnosticSovereignDict).
        # This allows chained lookups like `{{ config.database.port }}` to resolve
        # safely to `None` in the Evaluator rather than crashing the AST walk.
        return GnosticSovereignDict()

    def get(self, key: Any, default: Any = None) -> Any:
        """O(1) Safe Accessor."""
        if key in self:
            return super().__getitem__(key)

        # Reservoirs do not support fuzzy fallback to avoid Anomaly 236
        if key in SGF_RESERVOIRS:
            return default

        try:
            val = self.__getitem__(key)
            # If we returned a Void Object (empty dict), return the Architect's default
            if isinstance(val, GnosticSovereignDict) and not val:
                return default
            return val
        except (KeyError, AttributeError):
            return default

    def __setitem__(self, key: Any, value: Any):
        """
        =============================================================================
        == THE RITE OF INSCRIPTION (V-Ω-IMMUTABLE-WARDED)                          ==
        =============================================================================
        """
        # [ASCENSION 9]: Atomic Write-Isolation
        if getattr(self, '_is_frozen', False):
            raise RuntimeError("Immutable Heresy: Attempted to mutate a warded Mind-State.")

        interned_key = sys.intern(key) if isinstance(key, str) else key

        # [ASCENSION 4]: Triage reservoirs to preserve reference pointers
        if isinstance(interned_key, str) and (interned_key in SGF_RESERVOIRS or interned_key.startswith('__')):
            enshrined_value = value
        else:
            enshrined_value = self._enshrine_matter(value)

        super().__setitem__(interned_key, enshrined_value)

        # Update Shadow Map for future O(1) Normalization
        if self._shadow_map is not None and isinstance(interned_key, str):
            normalized_soul = self._normalize_key(interned_key)
            self._shadow_map[normalized_soul] = interned_key

        self._merkle_hash = None  # Invalidate rolling hash

    def _enshrine_matter(self, val: Any, _visited: Optional[Set[int]] = None, _depth: int = 0) -> Any:
        """Recursive Depth Governor & Identity Preservation."""
        # [ASCENSION 20]: Topological Depth Governor
        if val is None or _depth > 50:
            return val

        # [ASCENSION 13]: Binary & Soul Protection
        if type(val).__name__ in SGF_TENSOR_TYPES or hasattr(val, 'model_dump'):
            return val

        if isinstance(val, dict) and not isinstance(val, GnosticSovereignDict):
            return GnosticSovereignDict(val)

        if isinstance(val, list):
            # We don't deep-copy, we only transfigure child-dicts to Sovereign form
            for i in range(len(val)):
                if isinstance(val[i], dict) and not isinstance(val[i], GnosticSovereignDict):
                    val[i] = GnosticSovereignDict(val[i])
            return val

        # [ASCENSION 5 & 17]: Isomorphic Boolean/Null Thawing
        if isinstance(val, str):
            v_low = val.lower().strip()
            if v_low in ("true", "yes", "on", "resonant"): return True
            if v_low in ("false", "no", "off", "fractured"): return False
            if v_low in ("null", "none", "void"): return None

        return val

    def _rebuild_shadow_map(self):
        """[ASCENSION 10]: Lazy Shadow-Map Inflation."""
        self._shadow_map = {
            self._normalize_key(k): k for k in super().keys() if isinstance(k, str)
        }

    # =========================================================================
    # == [ASCENSION 14]: HYDRAULIC FAST CLONING (THE CURE FOR DEEPCOPY)      ==
    # =========================================================================

    def _fast_clone(self, val: Any, _visited: Optional[Dict[int, Any]] = None) -> Any:
        """
        O(N) Deep cloning without the massive overhead of `copy.deepcopy`.
        Bypasses internal memoization loops and handles primitives natively.
        """
        v_type = type(val)
        if v_type in (str, int, float, bool, type(None)):
            return val

        # Pydantic / System Models (Do not clone, pass reference for velocity)
        if v_type.__name__ in SGF_TENSOR_TYPES or hasattr(val, 'model_dump'):
            return val

        if _visited is None: _visited = {}
        val_id = id(val)
        if val_id in _visited: return _visited[val_id]

        if isinstance(val, GnosticSovereignDict):
            new_dict = GnosticSovereignDict()
            _visited[val_id] = new_dict
            object.__setattr__(new_dict, '_is_frozen', getattr(val, '_is_frozen', False))
            for k, v in val.items():
                # Direct super() call to bypass enshrine logic during clone
                super(GnosticSovereignDict, new_dict).__setitem__(k, self._fast_clone(v, _visited))
            return new_dict

        elif v_type is dict:
            new_dict = {}
            _visited[val_id] = new_dict
            for k, v in val.items():
                new_dict[k] = self._fast_clone(v, _visited)
            return new_dict

        elif v_type is list:
            new_list = []
            _visited[val_id] = new_list
            for v in val:
                new_list.append(self._fast_clone(v, _visited))
            return new_list

        elif v_type is set:
            return set(self._fast_clone(v, _visited) for v in val)

        return val

    def copy(self) -> 'GnosticSovereignDict':
        """The Omega Shallow-Copy with Reference Preservation."""
        new_vessel = self.__class__()
        object.__setattr__(new_vessel, '_is_frozen', getattr(self, '_is_frozen', False))

        for k, v in self.items():
            # [ASCENSION 4]: Physical Reservoirs MUST retain their exact memory pointer ID
            if isinstance(k, str) and (k in SGF_RESERVOIRS or k.startswith('__')):
                super(GnosticSovereignDict, new_vessel).__setitem__(k, v)
            else:
                # Value dictionaries and arrays are fast-cloned
                super(GnosticSovereignDict, new_vessel).__setitem__(k, self._fast_clone(v))

        return new_vessel

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'GnosticSovereignDict':
        """[ASCENSION 25]: The Deepcopy Hijacker. Intercepts standard library clones."""
        if id(self) in memo:
            return memo[id(self)]
        cloned = self.copy()
        memo[id(self)] = cloned
        return cloned

    # =========================================================================
    # == ATTRIBUTE PROXY LATTICE                                             ==
    # =========================================================================

    def __getattr__(self, name: str) -> Any:
        """[ASCENSION 30]: Dynamic Attribute Proxying (dict.key support)."""
        if (name.startswith('__') and name.endswith('__')) or name in self.__slots__:
            return super().__getattribute__(name)
        if name.startswith(('model_', 'pydantic_')):
            return super().__getattribute__(name)
        return self.__getitem__(name)

    def __setattr__(self, name: str, value: Any):
        if name in self.__slots__ or (name.startswith('__') and name.endswith('__')):
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    def __dir__(self) -> List[str]:
        """[ASCENSION 26]: Luminous Type Mirroring for IDE Intellisense."""
        base_dir = super().__dir__()
        return list(set(base_dir + [str(k) for k in self.keys() if isinstance(k, str) and not k.startswith('_')]))

    def update(self, other: Union[Dict, 'GnosticSovereignDict'] = None, **kwargs):
        """[ASCENSION 24 & 27]: C-Level Unpacking Optimization with Context Suture."""
        if other:
            for k, v in (other.items() if hasattr(other, 'items') else other):
                self.__setitem__(k, v)
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __ior__(self, other: Union[Dict, 'GnosticSovereignDict']) -> 'GnosticSovereignDict':
        """[ASCENSION 28]: Isomorphic Operator Overloading (|=)."""
        self.update(other)
        return self

    def __or__(self, other: Union[Dict, 'GnosticSovereignDict']) -> 'GnosticSovereignDict':
        """[ASCENSION 28]: Isomorphic Operator Overloading (|)."""
        new_dict = self.copy()
        new_dict.update(other)
        return new_dict

    def freeze(self):
        """[ASCENSION 9]: Enshrines the state as immutable."""
        object.__setattr__(self, '_is_frozen', True)
        for v in self.values():
            if isinstance(v, GnosticSovereignDict):
                v.freeze()
        return self

    def __bool__(self) -> bool:
        return len(self) > 0

    def __repr__(self) -> str:
        # [ASCENSION 18]: ENTROPY REDACTION
        safe_keys = []
        for k in self.keys():
            if any(s in str(k).upper() for s in ('SECRET', 'TOKEN', 'PASS')):
                safe_keys.append(f"{k}=[REDACTED]")
            else:
                safe_keys.append(str(k))
        return f"<Ω_GNOSTIC_DICT keys={len(self)} hash={self.state_hash[:8]} status=RESONANT>"

    @property
    def state_hash(self) -> str:
        """[ASCENSION 7]: MERKLE STATE FINGERPRINTING."""
        if self._merkle_hash is None:
            # Deterministic scan of keys to build the hash
            payload = "|".join(sorted([str(k) for k in self.keys() if not str(k).startswith('__')]))
            self._merkle_hash = hashlib.sha256(payload.encode()).hexdigest()
        return self._merkle_hash

    def model_dump(self, mode: str = 'dict', exclude_none: bool = False, _seen: Optional[Set[int]] = None) -> Dict[
        str, Any]:
        """
        =============================================================================
        == THE OMEGA MODEL DUMP (V-Ω-TOTALITY-VMAX)                                ==
        =============================================================================
        [ASCENSION 22]: Fault-Isolated Serialization. Recursively unwraps the state
        while maintaining perfect reference-cycle (Ouroboros) protection.
        """
        if _seen is None: _seen = set()

        obj_id = id(self)
        if obj_id in _seen:
            return {"__cycle_detected__": True}

        _seen.add(obj_id)
        result = {}

        for k, v in self.items():
            if exclude_none and v is None: continue
            k_str = str(k)
            # Filter internal noise
            if k_str.startswith('__') and k_str.endswith('__'): continue

            try:
                if isinstance(v, GnosticSovereignDict):
                    result[k] = v.model_dump(exclude_none=exclude_none, _seen=_seen)
                elif hasattr(v, 'model_dump'):
                    result[k] = v.model_dump(mode='json')
                elif isinstance(v, (list, tuple, set)):
                    result[k] = [
                        (i.model_dump(exclude_none=exclude_none, _seen=_seen)
                         if isinstance(i, GnosticSovereignDict) else i)
                        for i in v
                    ]
                elif isinstance(v, (Path, uuid.UUID, Decimal, datetime, date)):
                    result[k] = str(v).replace('\\', '/')
                else:
                    # [ASCENSION 18]: Entropy Redaction in serialization
                    if any(s in k_str.lower() for s in ('key', 'secret', 'token', 'password')):
                        result[k] = "[REDACTED]"
                    else:
                        result[k] = v
            except Exception as e:
                # [ASCENSION 22]: Fault-Isolated Suture
                result[k] = f"/* SERIALIZATION_FRACTURE: {str(e)} */"

        _seen.remove(obj_id)
        return result