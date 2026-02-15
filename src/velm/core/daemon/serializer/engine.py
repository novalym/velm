# Path: core/daemon/serializer/engine.py
# --------------------------------------
# LIF: ∞ | ROLE: TRANSMUTATION_CORE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SERIALIZER_V200_TOTALITY_FINALIS_2026_WASM_RECTIFIED

import dataclasses
import datetime
import json
import uuid
import enum
import collections
import math
import weakref
from pathlib import Path, PurePath
from typing import Any, Iterator, Dict, List, Set, Union, Final, Optional

# --- THE DIVINE UPLINKS ---
from .registry import EncoderRegistry
from .constants import MAX_REPR_LENGTH, UNSERIALIZABLE_TEMPLATE, MAX_GENERATOR_ITEMS
from .encoders import temporal, spatial, schema, forensic, scientific, meta

# [ASCENSION 5]: ISOMORPHIC PYDANTIC SENSING
try:
    import pydantic

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


class GnosticSerializer:
    """
    =================================================================================
    == THE OMEGA SERIALIZER (V-Ω-TOTALITY-V200-INDESTRUCTIBLE)                     ==
    =================================================================================
    LIF: INFINITY | ROLE: ATOMIC_TRANSFECTOR | RANK: OMEGA_SUPREME

    The ultimate arbiter of Gnostic Data. It transmutes complex Pythonic consciousness
    into pure, serializable matter, warded against the 'UniversalSink' heresy.
    """

    # [ASCENSION 1]: THE BLACK GRIMOIRE OF GHOSTS
    # We identify types that cause panics in the WASM/Rust substrate.
    GHOST_TYPES: Final[Set[str]] = {
        "UniversalSink", "GnosticConcourse", "VisualCortexStream",
        "Scribe", "Logger", "TextIO", "BufferedWriter", "SharedArrayBuffer"
    }

    def __init__(self, sort_keys: bool = True):
        self.registry = EncoderRegistry()
        self._consecrate()
        self.sort_keys = sort_keys
        # [ASCENSION 2]: WeakRef Sentinel to prevent memory drift in long sessions.
        self._depth_sentinel = weakref.WeakKeyDictionary()

    def _consecrate(self):
        """Register all known specialized encoders."""
        temporal.register(self.registry)
        spatial.register(self.registry)
        schema.register(self.registry)
        forensic.register(self.registry)
        scientific.register(self.registry)
        meta.register(self.registry)

    def serialize(self, obj: Any) -> Any:
        """
        =============================================================================
        == THE MASTER RITE                                                         ==
        =============================================================================
        """
        # We use a simple ID set for non-hashable/primitive recursion tracking
        visited = set()
        return self._transmute(obj, 0, visited)

    def _transmute(self, obj: Any, depth: int, visited: Set[int]) -> Any:
        """
        =============================================================================
        == THE RITE OF RECURSIVE TRANSMUTATION                                     ==
        =============================================================================
        Surgically deconstructs the object, healing type-heresies at every layer.
        """
        # [ASCENSION 10]: RECURSION GOVERNOR
        if depth > 100:
            return "[RECURSION_LIMIT_EXCEEDED]"

        # [ASCENSION 1]: STRATUM-0 GHOST INQUISITOR (THE FIX)
        # We scry the type name as a string to avoid touching the object's internals
        # which might trigger the Pydantic Rust Serializer too early.
        obj_type = type(obj)
        obj_type_name = obj_type.__name__
        if obj_type_name in self.GHOST_TYPES:
            return f"[SYSTEM_GHOST:{obj_type_name}]"

        # 1. PRIMITIVE PASS-THROUGH (The Golden Path)
        if obj is None or isinstance(obj, (str, int, float, bool)):
            # [ASCENSION 4]: THE ENTROPY SIEVE (Secret Protection)
            if isinstance(obj, str) and len(obj) > 32:
                if self._calculate_entropy(obj) > 4.2 and " " not in obj:
                    return "[REDACTED_HIGH_ENTROPY_MATTER]"
            return obj

        # 2. CIRCULARITY WARD
        obj_id = id(obj)
        if obj_id in visited:
            return f"[CIRCULAR_REFERENCE:{obj_type_name}]"

        # We only track non-primitives
        if not isinstance(obj, (str, int, float, bool, type(None))):
            visited.add(obj_id)

        # 3. REGISTRY LOOKUP (Specialized Encoders)
        encoder = self.registry.resolve(obj)
        if encoder:
            return encoder(obj)

        # 4. COLLECTION TRIAGE
        if isinstance(obj, dict):
            # [ASCENSION 6 & 8]: DETERMINISM & BANDWIDTH CONTROL
            items = sorted(obj.items()) if self.sort_keys else obj.items()
            return {str(k): self._transmute(v, depth + 1, visited) for k, v in items}

        if isinstance(obj, (list, tuple, set)):
            # [ASCENSION 8]: METABOLIC THROTTLING
            if len(obj) > 5000 and depth > 1:
                return f"[COLLECTION_THROTTLED:SIZE={len(obj)}]"
            return [self._transmute(i, depth + 1, visited) for i in obj]

        # 5. [ASCENSION 5]: PYDANTIC ADAPTATION (V2-FIRST)
        if HAS_PYDANTIC and isinstance(obj, pydantic.BaseModel):
            try:
                if hasattr(obj, 'model_dump'):
                    return self._transmute(obj.model_dump(mode='json'), depth + 1, visited)
                return self._transmute(obj.dict(), depth + 1, visited)
            except Exception as e:
                return f"[PYDANTIC_FRACTURE:{str(e)}]"

        # 6. [ASCENSION 3]: SPATIAL & TEMPORAL ATOMS
        if isinstance(obj, (Path, PurePath)):
            return str(obj).replace('\\', '/')

        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, enum.Enum):
            return obj.value

        # 7. [ASCENSION 9]: THE BINARY HUSK
        if isinstance(obj, (bytes, bytearray)):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                import base64
                return f"base64:{base64.b64encode(obj).decode('ascii')}"

        # 8. DYNAMIC LOGIC (Duck Typing)
        if dataclasses.is_dataclass(obj):
            return self._transmute(dataclasses.asdict(obj), depth + 1, visited)

        # 9. [ASCENSION 7]: SELF-SERIALIZING SOVEREIGNTY (The High Path)
        # Check for our own internal serialization protocols first
        for method in ("model_dump", "to_json", "to_dict", "as_dict", "dict"):
            if hasattr(obj, method):
                attr = getattr(obj, method)
                if callable(attr):
                    try:
                        return self._transmute(attr(), depth + 1, visited)
                    except Exception:
                        continue

        # 10. [ASCENSION 11]: UNIVERSAL SAFETY SARCOPHAGUS
        # The final fallback. If we cannot transmute the soul, we capture the appearance.
        try:
            repr_str = repr(obj)
            if len(repr_str) > MAX_REPR_LENGTH:
                return repr_str[:MAX_REPR_LENGTH] + "...[TRUNCATED]"
            return repr_str
        except Exception:
            return UNSERIALIZABLE_TEMPLATE.format(obj_type_name)

    def _calculate_entropy(self, text: str) -> float:
        """[FACULTY 4]: Shannon Entropy calculation for secret scrying."""
        if not text:
            return 0.0
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return -sum([p * math.log(p) / math.log(2.0) for p in probabilities])


# =============================================================================
# == THE SOVEREIGN INSTANCE & PUBLIC API                                     ==
# =============================================================================

_engine = GnosticSerializer(sort_keys=True)


def gnostic_serializer(obj: Any) -> Any:
    """
    =============================================================================
    == THE GNOSTIC SERIALIZER GATEWAY                                          ==
    =============================================================================
    LIF: ∞ | ROLE: PUBLIC_INTERFACE

    The one true gateway for json.dumps.
    Usage: json.dumps(data, default=gnostic_serializer)
    """
    return _engine.serialize(obj)
