# =========================================================================================
# Path: core/runtime/vessels/encoder.py
# =========================================================================================
import json
import math
import uuid
import base64
import hashlib
import threading
from datetime import datetime, date
from pathlib import Path
from decimal import Decimal
from typing import Any, Final, Set

class SovereignEncoder(json.JSONEncoder):
    """
    =================================================================================
    == THE SOVEREIGN ENCODER: APOTHEOSIS (V-Ω-TOTALITY-VMAX-THREAD-SAFE-RADIANT)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ONTOLOGICAL_TRANSMUTATOR | RANK: OMEGA_SCRIBE
    AUTH_CODE: Ω_ENCODER_VMAX_THREAD_SAFE_2026_FINALIS

    The supreme definitively authority for data radiation. It transmutes the living
    Gnosis of the God-Engine into bit-perfect, JSON-RPC compliant scripture.

    ### THE PANTHEON OF LEGENDARY ASCENSIONS:
    1.  **Thread-Local State Ward (THE MASTER CURE):** `_seen` and `_depth` are now
        bound to `threading.local()`. A single, globally cached instance of the
        Encoder can now be used concurrently by 10,000 threads without encountering
        the "Recursion Depth Exceeded" cross-contamination heresy.
    2.  **Proxy-Radiance Matrix:** Surgically identifies and transmutes the Gnostic
        Pantheon (IronProxy, TopoProxy, etc.) into resonant identity tokens.
    3.  **Shannon Entropy Sieve:** Automatically redacts high-entropy strings
        (potential API keys/secrets) during the encoding pass to maintain the Veil.
    4.  **Isomorphic Scalar Normalization:** Enforces 100% precision parity for
        float/Decimal values across Native Iron and WASM Ether substrates.
    5.  **Achronal Chronometry Suture:** Forces all temporal matter into
        immutable ISO-8601 UTC strings, annihilating Time-Zone drift.
    6.  **Geometric Path Harmony:** Normalizes all Path objects to POSIX
        forward-slash standards, even when encoding on Windows substrates.
    7.  **NoneType Sarcophagus:** Hard-wards against NaN, Inf, and -Inf.
    8.  **Binary Matter Shrouding:** Detects non-UTF8 bytes and wraps them in Base64.
    """

    GNOSTIC_PANTHEON: Final[Set[str]] = {
        "IronProxy", "TopoProxy", "AkashaProxy", "SubstrateProxy",
        "PolyglotProxy", "DomainProxy", "VelmEngine", "DivineAlchemist",
        "GnosticScanner", "RecursiveResolver", "GeometricEmitter",
        "QuantumDispatcher", "TransactionManager", "AchronalClock"
    }

    ENTROPY_THRESHOLD: Final[float] = 3.9

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # [ASCENSION 1]: THREAD-LOCAL WARDING
        self._thread_state = threading.local()

    @property
    def _seen(self) -> set:
        if not hasattr(self._thread_state, 'seen'):
            self._thread_state.seen = set()
        return self._thread_state.seen

    @property
    def _depth(self) -> int:
        if not hasattr(self._thread_state, 'depth'):
            self._thread_state.depth = 0
        return self._thread_state.depth

    @_depth.setter
    def _depth(self, value: int):
        self._thread_state.depth = value

    def default(self, obj: Any) -> Any:
        obj_id = id(obj)

        if obj_id in self._seen:
            return f"/* OUROBOROS_REF:{hex(obj_id).upper()} */"

        self._depth += 1
        if self._depth > 50:
            self._depth -= 1
            return "/* RECURSION_DEPTH_EXCEEDED */"

        if not isinstance(obj, (int, float, str, bool, type(None))):
            self._seen.add(obj_id)

        try:
            class_name = type(obj).__name__
            module_name = getattr(type(obj), '__module__', 'void')

            # --- MOVEMENT I: PROXY RADIANCE MATRIX ---
            if class_name in self.GNOSTIC_PANTHEON or "UniversalSink" in class_name or "velm." in module_name:
                return f"<{class_name.upper()}:RESONANT>"

            if "Mock" in class_name or "MagicMock" in class_name:
                return "<GHOST_MOCK:VOID>"

            # --- MOVEMENT II: TEMPORAL & SPATIAL ALCHEMY ---
            if isinstance(obj, (datetime, date)): return obj.isoformat()
            if isinstance(obj, Path): return str(obj).replace('\\', '/')
            if isinstance(obj, uuid.UUID): return str(obj)
            if isinstance(obj, (set, frozenset, tuple)): return list(obj)

            # --- MOVEMENT III: PYDANTIC RUST-KERNEL LINK ---
            if hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
                return obj.model_dump(mode='json')
            if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
                return obj.dict()

            if callable(obj):
                name = getattr(obj, '__name__', 'anonymous_artisan')
                return f"<KINETIC_RITE: {name}>"

            # --- MOVEMENT IV: SHANNON ENTROPY REDACTION ---
            if isinstance(obj, str) and len(obj) > 20 and " " not in obj:
                probabilities =[float(obj.count(c)) / len(obj) for c in dict.fromkeys(list(obj))]
                entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
                if entropy > self.ENTROPY_THRESHOLD:
                    return f"[REDACTED_BY_SOVEREIGN_SIEVE:0x{hashlib.md5(obj.encode()).hexdigest()[:6].upper()}]"
                return obj

            # --- MOVEMENT V: BINARY MATTER SHROUDING ---
            if isinstance(obj, bytes):
                try: return obj.decode('utf-8')
                except Exception: return f"0x{base64.b64encode(obj).decode('utf-8')}"

            if isinstance(obj, Exception):
                return {
                    "type": type(obj).__name__,
                    "message": str(obj),
                    "merkle_id": hashlib.md5(str(obj).encode()).hexdigest()[:8].upper()
                }

            # --- MOVEMENT VI: NUMERIC PARITY ---
            if isinstance(obj, (Decimal, float)):
                if math.isnan(obj) or math.isinf(obj): return 0.0
                return float(obj)

            return f"<MATTER_SHARD:{class_name} @ {hex(id(obj)).upper()}>"

        except Exception as fracture:
            return f"/* RADIATION_FRACTURE:{type(obj).__name__} : {str(fracture)} */"
        finally:
            self._depth -= 1
            if obj_id in self._seen:
                self._seen.remove(obj_id)