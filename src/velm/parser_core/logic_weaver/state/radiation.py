# Path: parser_core/logic_weaver/state/radiation.py
# -------------------------------------------------

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import GnosticContext


class HUDMulticaster:
    """
    =============================================================================
    == THE HUD MULTICASTER (V-Ω-TELEMETRIC-RADIATOR)                           ==
    =============================================================================
    The neural uplink to the UI. It safely broadcasts state changes without
    creating memory leaks or crashing if the connection to the Ocular Membrane
    is severed.
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    def radiate(self, key: str, value: Any):
        """
        [ASCENSION 4]: SUBSTRATE-AGNOSTIC PROJECTION.
        Sends a pulse to the React interface, but only if the mutation occurs
        in the Root stratum and is a public variable.
        """
        # Only broadcast top-level changes to avoid Ocular noise from macro loops
        if self.ctx.depth == 0 and not key.startswith('_'):
            try:
                # We access engine via a loose reference if available
                engine = self.ctx._context.get('_engine_link')
                if engine and hasattr(engine, 'akashic') and engine.akashic:
                    engine.akashic.broadcast({
                        "method": "novalym/gnosis_shift",
                        "params": {
                            "key": key,
                            "value": str(value),
                            "trace_id": self.ctx._context.get('trace_id', 'unknown')
                        }
                    })
            except Exception:
                pass