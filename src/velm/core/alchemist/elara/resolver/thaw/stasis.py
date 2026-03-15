import hashlib
import json
from typing import Any, Dict, Set, Optional

class StasisAnchor:
    """
    =============================================================================
    == THE STASIS ANCHOR (V-Ω-TOTALITY)                                        ==
    =============================================================================
    LIF: ∞ | ROLE: ENTROPY_ADJUDICATOR | RANK: MASTER
    [ASCENSION 146]: Merkle-Lattice oscillation detection.
    """
    MAX_MUTATIONS: int = 12

    @classmethod
    def calculate_fingerprint(cls, value: Any) -> str:
        """Forges a bit-perfect hash of the current logical state."""
        if isinstance(value, (dict, list)):
            return hashlib.md5(json.dumps(value, sort_keys=True).encode()).hexdigest()
        return hashlib.md5(str(value).encode()).hexdigest()

    @classmethod
    def scry_oscillation(cls, fingerprint: str, chain: Set[str]) -> bool:
        """Returns True if this state has been perceived before in this timeline."""
        return fingerprint in chain