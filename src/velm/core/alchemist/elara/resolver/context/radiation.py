# Path: core/alchemist/elara/resolver/context/radiation.py
# --------------------------------------------------------

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import LexicalScope

class HUDMulticaster:
    """
    =============================================================================
    == THE HUD MULTICASTER (V-Ω-TELEMETRIC-RADIATOR)                           ==
    =============================================================================
    Sends state shifts to the React HUD without polluting the memory heap.
    """

    @classmethod
    def radiate(cls, scope: 'LexicalScope', key: str, value: Any):
        """[ASCENSION 154]: Substrate-Aware Radiation."""
        # Only broadcast top-level changes to avoid Ocular noise
        if scope.depth == 0 and not key.startswith('_'):
            try:
                engine = scope.global_ctx.variables.get('__engine__')
                if engine and hasattr(engine, 'akashic') and engine.akashic:
                    is_secret = any(s in key.lower() for s in ('key', 'secret', 'pass', 'auth'))
                    display_val = "[REDACTED]" if is_secret else str(value)
                    if len(display_val) > 256: display_val = display_val[:253] + "..."

                    engine.akashic.broadcast({
                        "method": "novalym/gnosis_shift",
                        "params": {
                            "scope_id": scope._id,
                            "key": key,
                            "value": display_val,
                            "trace": scope.global_ctx.trace_id,
                            "depth": scope.depth
                        }
                    })
            except Exception:
                pass