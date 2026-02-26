# Path: parser_core/logic_weaver/state/forensics.py
# -------------------------------------------------

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import GnosticContext


class HolographicTomographer:
    """
    =============================================================================
    == THE HOLOGRAPHIC TOMOGRAPHER (V-Ω-MERKLE-STATE-SCRIER)                   ==
    =============================================================================
    Generates deterministic, cryptographically-sound snapshots of the entire
    Gnostic Hierarchy for the Ocular HUD and the Transaction Chronicle.
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    def scry(self, include_parents: bool = True) -> str:
        """
        [ASCENSION 8]: HOLOGRAPHIC TOMOGRAPHY.
        Exports a sanitized, JSON-safe view of the variable hierarchy.
        """
        return json.dumps(self._export_dict(include_parents), indent=2)

    def fingerprint(self) -> str:
        """
        [ASCENSION 9]: MERKLE-STATE FINGERPRINTING.
        Forges a deterministic cryptographic seal of the active variables.
        """
        canonical = json.dumps(self._export_dict(False), sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _export_dict(self, include_parents: bool = True) -> Dict[str, Any]:
        """Recursively builds the holographic data map."""

        def _sanitize(val):
            if isinstance(val, Path): return str(val).replace('\\', '/')
            if isinstance(val, set): return sorted(list(val))
            return val

        # Local Stratum (Redact internal engine keys starting with '_')
        data = {k: _sanitize(v) for k, v in self.ctx._context.items() if not k.startswith('_')}

        if include_parents and self.ctx.parent:
            data[f"PARENT_{self.ctx.parent.name.upper()}"] = self.ctx.parent.forensics._export_dict(True)

        return data