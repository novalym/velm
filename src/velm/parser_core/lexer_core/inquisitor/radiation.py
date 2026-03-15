# Path: parser_core/lexer_core/inquisitor/radiation.py
# ----------------------------------------------------

from typing import Any
from ....contracts.data_contracts import GnosticLineType

class InquisitorRadiator:
    """Sends classification pulses to the Ocular HUD."""

    AURA_MAP = {
        GnosticLineType.FORM: "#64ffda",      # Teal
        GnosticLineType.VARIABLE: "#f59e0b",  # Amber
        GnosticLineType.LOGIC: "#3b82f6",     # Blue
        GnosticLineType.POST_RUN: "#a855f7",  # Purple
        GnosticLineType.VOW: "#ec4899",       # Pink
    }

    @classmethod
    def radiate(cls, parser: Any, line_type: GnosticLineType):
        if parser.engine and hasattr(parser.engine, 'akashic') and parser.engine.akashic:
            try:
                color = cls.AURA_MAP.get(line_type, "#94a3b8")
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LEXICAL_TRIAGE",
                        "label": line_type.name,
                        "color": color,
                        "trace": getattr(parser, 'parse_session_id', 'void')
                    }
                })
            except Exception:
                pass