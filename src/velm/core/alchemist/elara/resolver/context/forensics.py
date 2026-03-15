# Path: core/alchemist/elara/resolver/context/forensics.py
# --------------------------------------------------------

import json
import hashlib
import math
from typing import Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .engine import LexicalScope

class TomographyScanner:
    """
    =============================================================================
    == THE TOMOGRAPHY SCANNER (V-Ω-HOLOGRAPHIC-STATE)                          ==
    =============================================================================
    LIF: ∞ | ROLE: MERKLE_STATE_EXPORTER
    Exports sanitized, JSON-safe views of the variable hierarchy.
    """

    @classmethod
    def scry_dossier(cls, scope: 'LexicalScope') -> Dict[str, Any]:
        """[ASCENSION 155]: HOLOGRAPHIC TOMOGRAPHY."""
        with scope._lock:
            def _sieve(data):
                if isinstance(data, (str, int, float, bool, type(None))):
                    if isinstance(data, str) and len(data) > 32:
                        prob =[float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]
                        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
                        if entropy > 4.2: return "[REDACTED_BY_ENTROPY_VEIL]"
                    return data
                if isinstance(data, dict): return {k: _sieve(v) for k, v in data.items()}
                if isinstance(data, (list, tuple, set)): return [_sieve(x) for x in data]
                return f"/* OBJ: {type(data).__name__} */"

            return {
                "v": "3.4.0-Ω",
                "id": scope._id,
                "name": scope.name,
                "depth": scope.depth,
                "variables": _sieve(dict(scope.local_vars)),
                "provenance": scope._provenance,
                "merkle_seal": cls.fingerprint(scope),
                "metabolism": scope._telemetry_stats
            }

    @classmethod
    def fingerprint(cls, scope: 'LexicalScope') -> str:
        """Merkle State Hash."""
        raw = "|".join(sorted(list(scope.local_vars.keys()))) + "".join(scope._merkle_chain[-5:])
        return hashlib.sha256(raw.encode()).hexdigest()[:12].upper()