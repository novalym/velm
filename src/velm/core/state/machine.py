# Path: scaffold/core/state/machine.py
from contextlib import contextmanager
from .store import Store
from .ledger import ActiveLedger
from .contracts import LedgerOperation
from ...core.state.contracts import LedgerEntry

@contextmanager
def GnosticRite(rite_name: str, initial_vars: dict):
    """
    The one true, sacred context manager for ALL Scaffold operations.
    It wraps a rite in a transactional, reversible, and state-aware boundary.
    """
    try:
        Store.load_snapshot(initial_vars)
        ActiveLedger.begin_rite()
        # The rite is now conducted in the mortal realm.
        yield
        # The rite was pure. The Gnosis is committed.
        ActiveLedger.commit_rite()
    except Exception:
        # A heresy was perceived. The Gnosis is reverted.
        ActiveLedger.rollback()
        # The heresy is re-proclaimed to the higher realms.
        raise