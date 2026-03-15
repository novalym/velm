import re
from typing import Any, Final
from ......logger import Scribe

Logger = Scribe("Thaw:Exorcist")


class ApophaticExorcist:
    """
    =============================================================================
    == THE APOPHATIC EXORCIST (V-Ω-TOTALITY)                                   ==
    =============================================================================
    LIF: 1,000,000x | ROLE: SIGIL_INCINERATOR | RANK: MASTER
    [ASCENSION 147]: Absolute Quiescence Enforcement.
    """
    # High-priority regex phalanx
    RE_PHANTOMS: Final[re.Pattern] = re.compile(r'\{\{.*?\}\}|\{%.*?%\}')

    @classmethod
    def incinerate(cls, matter: Any) -> Any:
        """
        [THE MASTER CURE]
        Righteously transmutates remaining phantoms into bit-perfect empty 
        strings to prevent Topological Collapse in the physical iron.
        """
        if not isinstance(matter, str):
            return matter

        if "{{" in matter or "{%" in matter:
            purified = cls.RE_PHANTOMS.sub('', matter).strip()
            Logger.warn(f"   -> Absolute Quiescence: Sigils incinerated in matter: [dim]{matter[:30]}...[/dim]")
            return purified

        return matter

    @classmethod
    def normalize_final_form(cls, value: Any) -> Any:
        """[ASCENSION 115]: THE LINGUISTIC PURITY SUTURE."""
        if not isinstance(value, str):
            return value

        v_low = value.lower().strip()

        # NoneType Bridge
        if v_low in ("true", "yes", "on", "resonant"): return True
        if v_low in ("false", "no", "off", "fractured"): return False
        if v_low in ("none", "null", "void"): return None

        if value.isdigit():
            try:
                return int(value)
            except ValueError:
                return value

        return value