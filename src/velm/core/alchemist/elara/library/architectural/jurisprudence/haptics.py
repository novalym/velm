# Path: core/alchemist/elara/library/architectural/jurisprudence/haptics.py
# -------------------------------------------------------------------------

from typing import Any
from ...registry import register_rite


@register_rite("radiate")
def radiate_to_hud(value: Any, label: str, color: str = "#64ffda", **kwargs) -> Any:
    """
    =============================================================================
    == THE HAPTIC RADIATOR (V-Ω-TOTALITY)                                      ==
    =============================================================================
    [ASCENSION 49]: Haptic Projection.
    Allows an ELARA blueprint to send a visual pulse directly to the React HUD
    during the middle of a generation cycle!
    """
    ctx = kwargs.get('context', {})
    engine = ctx.get('__engine__')

    if engine and hasattr(engine, 'akashic') and engine.akashic:
        try:
            engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "BLUEPRINT_SIGNAL",
                    "label": label,
                    "color": color,
                    "value": str(value)[:100]
                }
            })
        except Exception:
            pass

    return value