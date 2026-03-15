# Path: core/alchemist/elara/resolver/context/primitives.py
# ---------------------------------------------------------

from typing import Dict, Any

class PrimitiveInjector:
    """
    =============================================================================
    == THE PRIMITIVE INJECTOR (V-Ω-TOTALITY)                                   ==
    =============================================================================
    LIF: 10,000x | ROLE: BASE_LOGIC_SEEDER
    Inscribes the fundamental laws of Python logic into the primordial Mind.
    Isolated to allow seamless future addition of new Base Rites.
    """

    @classmethod
    def inject(cls, local_vars: Dict[str, Any]):
        """Sutures standard Pythonic capabilities into the local stratum."""
        local_vars.update({
            "range": range, "enumerate": enumerate, "zip": zip, "sorted": sorted,
            "min": min, "max": max, "sum": sum, "any": any, "all": all,
            "dict": dict, "list": list, "set": set, "abs": abs, "round": round,
            "bool": bool, "int": int, "str": str, "float": float,
            "hasattr": hasattr, "getattr": getattr, "isinstance": isinstance,
            "_v": local_vars, "True": True, "False": False, "None": None
        })