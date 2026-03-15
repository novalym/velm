import textwrap
import time
from typing import Any, Set, Optional, List
from .bulkhead import RecursiveBulkhead
from .stasis import StasisAnchor
from .lustration import ApophaticExorcist
from .alchemy import ThawAlchemist
from ..context import LexicalScope
from ......logger import Scribe

Logger = Scribe("OuroborosBreaker")


class OuroborosBreaker:
    """
    =============================================================================
    == THE OUROBOROS BREAKER (V-Ω-TOTALITY-VMAX-168-ASCENSIONS)                ==
    =============================================================================
    LIF: ∞^∞ | ROLE: RECURSIVE_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME

    The supreme conductor of the Thaw Sanctum. It orchestrates the specialized
    organs to reach absolute logical stasis.
    """

    @classmethod
    def thaw(
            cls,
            value: Any,
            scope: LexicalScope,
            engine_ref: Any,
            depth: int = 0,
            causal_chain: Optional[Set[str]] = None,
            _mutation_count: int = 0
    ) -> Any:
        """
        =========================================================================
        == THE RITE OF RECURSIVE THAWING (V-Ω-TOTALITY-VMAX)                   ==
        =========================================================================
        [THE MASTER CURE]: Implements the Modular Thaw Protocol.
        """
        # --- PHASE 0: THE VOID GUARD ---
        if value is None or (isinstance(value, str) and not value.strip()):
            return value

        # --- PHASE 1: THE BULKHEAD ---
        if RecursiveBulkhead.is_saturated():
            return ApophaticExorcist.incinerate(value)

        # --- PHASE 2: POLYMORPHIC WALK ---
        if isinstance(value, list):
            return [cls.thaw(item, scope, engine_ref, depth + 1, causal_chain) for item in value]

        if isinstance(value, dict):
            return {k: cls.thaw(v, scope, engine_ref, depth + 1, causal_chain) for k, v in value.items()}

        if not isinstance(value, str):
            return value

        # --- PHASE 3: STASIS ADJUDICATION ---
        if "{{" not in value and "{%" not in value:
            return ApophaticExorcist.normalize_final_form(value)

        causal_chain = causal_chain or set()
        fingerprint = StasisAnchor.calculate_fingerprint(value.strip())

        if StasisAnchor.scry_oscillation(fingerprint, causal_chain):
            # Oscillation detected. Break the loop.
            return ApophaticExorcist.incinerate(value.strip())

        causal_chain.add(fingerprint)

        # =========================================================================
        # == PHASE 4: THE KINETIC STRIKE                                         ==
        # =========================================================================
        # [THE CURE]: Strip visual gravity (Laminar Dedent)
        pure_soul_matter = textwrap.dedent(value)

        try:
            RecursiveBulkhead.enter()

            # Execute sub-transmutation
            transmuted = ThawAlchemist.strike(engine_ref, pure_soul_matter, scope, depth)

            # [ASCENSION 122]: Entropy Velocity Check
            if _mutation_count >= StasisAnchor.MAX_MUTATIONS:
                return ApophaticExorcist.incinerate(transmuted)

            # [ASCENSION 123]: Check for stasis
            if transmuted.strip() == value.strip():
                # Potential unresolvable phantoms?
                if "{{" in transmuted or "{%" in transmuted:
                    return ApophaticExorcist.incinerate(transmuted)
                return ApophaticExorcist.normalize_final_form(transmuted.strip())

            # [RECURSIVE STRIKE]: Sink into deeper strata
            return cls.thaw(
                transmuted,
                scope,
                engine_ref,
                depth + 1,
                causal_chain,
                _mutation_count + 1
            )

        except Exception as fracture:
            Logger.debug(f"L? Thaw fracture at depth {depth}: {fracture}")
            return ApophaticExorcist.incinerate(value)

        finally:
            RecursiveBulkhead.exit()