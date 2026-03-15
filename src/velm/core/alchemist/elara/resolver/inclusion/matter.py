# Path: core/alchemist/elara/resolver/inclusion/matter.py
# -----------------------------------------------------------

import time
from typing import Any, TYPE_CHECKING
from ......logger import Scribe
from .resolver import InclusionResolver

if TYPE_CHECKING:
    from ..context import LexicalScope

Logger = Scribe("Inclusion:Matter")


class MatterInceptor:
    """
    =============================================================================
    == THE MATTER INCEPTOR (V-Ω-TOTALITY)                                      ==
    =============================================================================
    ROLE: PHYSICAL_INJECTION_CONDUCTOR
    Handles {% include %} by transmuting external scriptures into the stream.
    """

    @classmethod
    def include(cls, emissary: Any, path_str: str, scope: 'LexicalScope', ignore_missing: bool = False) -> str:
        """
        =========================================================================
        == THE RITE OF MATTER INCEPTION                                        ==
        =========================================================================
        """
        scripture = InclusionResolver.scry_iron(path_str, scope)

        if not scripture:
            if ignore_missing: return ""
            raise FileNotFoundError(f"Inclusion Fracture: Matter '{path_str}' is unmanifest.")

        Logger.info(f"🌀 [INCLUSION] Weaving matter from '{path_str}'...")

        # Transmute using the Engine Reference
        # We merge global mind with local scope for the sub-pass
        current_gnosis = {**scope.global_ctx.variables, **scope.local_vars}

        try:
            # [ASCENSION 40]: Geometric alignment is handled by the parent Emitter
            # receiving this string.
            return emissary.engine.transmute(scripture, current_gnosis)
        except Exception as e:
            Logger.error(f"Inclusion Logic Fracture in '{path_str}': {e}")
            return f"/* INCLUSION_FRACTURE: {path_str} */"