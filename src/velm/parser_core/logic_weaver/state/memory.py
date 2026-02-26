# Path: parser_core/logic_weaver/state/memory.py
# ----------------------------------------------

from typing import Any, TYPE_CHECKING
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from .engine import GnosticContext


class MemoryStratum:
    """
    =============================================================================
    == THE MEMORY STRATUM (V-Ω-RECURSIVE-TRUTH-RESOLVER)                       ==
    =============================================================================
    Manages the inscription, retrieval, and warded locking of Gnostic variables.
    It controls the "Ascent of Truth", checking the local mind before querying
    the ancestral lineage.
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    def get(self, key: str, default: Any = None) -> Any:
        """
        [ASCENSION 3]: PROTOPLAST INHERITANCE WITH CYCLIC WARD.
        Scries the local mind, then righteously ascends to the parent if
        the truth is unmanifest in this stratum.
        """
        # 1. Local Search (The Immediate Present)
        if key in self.ctx._context:
            return self.ctx._context[key]

        # 2. Recursive Ascent (The Ancestral Past)
        if self.ctx.parent:
            return self.ctx.parent.memory.get(key, default)

        # 3. Final Fallback (The Void)
        return default

    def set(self, key: str, value: Any, source: str = "internal", lock: bool = False):
        """
        [THE RITE OF INSCRIPTION]
        Inscribes truth into the local stratum and updates the provenance ledger.
        """
        if key in self.ctx._locks:
            raise PermissionError(f"Gnostic Schism: Key '{key}' is warded against mutation.")

        self.ctx._context[key] = value
        self.ctx.provenance[key] = source

        if lock:
            self.ctx._locks.add(key)

        # Multicast shift to HUD via the Radiator Organ
        self.ctx.radiator.radiate(key, value)