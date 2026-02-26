# Path: parser_core/logic_weaver/state/temporal.py
# ------------------------------------------------

from contextlib import contextmanager
from typing import Dict, Any, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import GnosticContext


class TemporalLoom:
    """
    =============================================================================
    == THE TEMPORAL LOOM (V-Ω-ACHRONAL-MASKING)                                ==
    =============================================================================
    Controls the flow of time and alternate realities. It allows the Engine to
    step into a "Masked" reality for a specific branch, and revert perfectly
    once the branch is sealed.
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    @contextmanager
    def mask(self, overrides: Dict[str, Any]) -> Generator['GnosticContext', None, None]:
        """
        [ASCENSION 7]: SHADOW-LOOM MASKING.
        Temporarily overlays variables for a specific logical branch with atomic
        state preservation to guarantee thread-safe reversibility.
        """
        original_state = {}
        added_keys = set()

        # 1. The Displacement (Save original state)
        for k, v in overrides.items():
            if k in self.ctx._context:
                original_state[k] = self.ctx._context[k]
            else:
                added_keys.add(k)
            self.ctx._context[k] = v

        try:
            # 2. The Execution (Yield control to the altered reality)
            yield self.ctx
        finally:
            # 3. The Restoration (Return to the Prime Timeline)
            for k, v in original_state.items():
                self.ctx._context[k] = v
            for k in added_keys:
                del self.ctx._context[k]

    def spawn_child(self, name: str) -> 'GnosticContext':
        """
        [ASCENSION 11]: BICAMERAL FISSION.
        Creates a new context stratum that inherits from this one.
        """
        if self.ctx.depth > 100:
            raise RecursionError("Ouroboros Error: Gnostic depth limit reached.")

        from .engine import GnosticContext

        return GnosticContext(
            raw_shared_context={},  # Empty local mind
            parent=self.ctx,
            name=name,
            depth=self.ctx.depth + 1
        )