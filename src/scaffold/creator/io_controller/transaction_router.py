# Path: scaffold/creator/io_controller/transaction_router.py
from __future__ import annotations
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Dict

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

if TYPE_CHECKING:
    from ...core.kernel import GnosticTransaction
    from .contracts import RoutingDecision

Logger = Scribe("TransactionRouter")


class TransactionRouter:
    """
    =================================================================================
    == THE GNOSTIC ROUTER OF REALMS (V-Ω-ASCENDED-ULTIMA)                          ==
    =================================================================================
    This divine artisan is a pure, sentient mind. Its Gaze determines the one
    true physical destination for an I/O rite, adjudicating between the Mortal
    Realm (direct writes) and the Ephemeral Staging Realm (transactional writes).
    It is the unbreakable Gnostic compass for the Hand of Creation.
    =================================================================================
    """

    def __init__(self, transaction: Optional["GnosticTransaction"]):
        self.transaction = transaction
        # Ascension X: The Chronocache of Resolution
        self._resolution_cache: Dict[str, Path] = {}
        Logger.verbose(f"Gnostic Router consecrated. Transactional state: {'ACTIVE' if transaction else 'INERT'}")

    def resolve(self, logical_path_str: str) -> Path:
        """
        Adjudicates the final physical path for an operation.
        Returns a pure Path object, honoring the Law of the Pure Contract.
        """
        # Ascension V: The Unbreakable Ward of the Void
        if not logical_path_str:
            raise ArtisanHeresy("The Router received a void plea. A path must be proclaimed.")

        # Ascension IV: The Gnostic Path Purity
        if "{{" in logical_path_str:
            raise ArtisanHeresy(
                f"The Router received an untransmuted path: '{logical_path_str}'. The Alchemist must act first.")

        # Ascension X: The Chronocache
        if logical_path_str in self._resolution_cache:
            return self._resolution_cache[logical_path_str]

        resolved_path: Path
        if self.transaction:
            # The transaction itself knows how to construct the staging path.
            # We delegate this sacred duty to it and receive a pure Path object.
            resolved_path = self.transaction.get_staging_path(logical_path_str)
            # Ascension VI: The Luminous Voice
            Logger.verbose(f"Path '{logical_path_str}' routed to Ephemeral Staging Realm.")
        else:
            # If no transaction, the logical path becomes the physical path within the sanctum.
            # The PhysicalOperations artisan will join this with the Sanctum Root.
            resolved_path = Path(logical_path_str)
            Logger.verbose(f"Path '{logical_path_str}' routed to Mortal Realm.")

        self._resolution_cache[logical_path_str] = resolved_path
        return resolved_path