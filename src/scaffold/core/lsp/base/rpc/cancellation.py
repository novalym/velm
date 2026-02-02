# Path: core/lsp/base/rpc/cancellation.py
# -----------------------------------------

import threading
from typing import Optional


class OperationCancelled(Exception):
    """
    [THE SEVERANCE]
    Raised when a Rite is aborted by the Architect's new intent.
    """
    pass


class CancellationToken:
    """
    =============================================================================
    == THE CANCELLATION TOKEN (V-Ω-VOLATILE-MEMORY)                            ==
    =============================================================================
    LIF: 10,000,000 | ROLE: INTERRUPT_SIGNAL

    A shared object passed deep into the call stack.
    Artisans must perform the `check()` rite every ~100ms of CPU time.
    """

    def __init__(self):
        self._event = threading.Event()
        self._is_cancelled = False

    def cancel(self):
        """[RITE]: ABORT - Signals that the operation is moot."""
        self._is_cancelled = True
        self._event.set()

    @property
    def is_cancellation_requested(self) -> bool:
        return self._is_cancelled

    def check(self):
        """
        [THE GAZE OF RELEVANCE]
        Raises OperationCancelled if the Architect has moved on.
        """
        if self._is_cancelled:
            raise OperationCancelled("The Architect's Will has shifted.")

    @classmethod
    def none(cls) -> 'CancellationToken':
        """Returns a dummy token that is never cancelled."""
        t = cls()
        # Override cancel to do nothing
        t.cancel = lambda: None
        return t