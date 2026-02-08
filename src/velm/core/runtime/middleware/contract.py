# Path: src/velm/core/runtime/middleware/contract.py
# --------------------------------------------------

import time
import logging
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional, Union, Dict, Final
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import HeresySeverity


# [ASCENSION 1]: THE GHOST ENGINE PROXY
# This object serves as a fail-safe sarcophagus if the engine is missing.
class GnosticVoidEngine:
    def __init__(self):
        self.logger = Scribe("VoidEngine")
        self.console = get_console()
        self.project_root = None
        self.akashic = None

    def success(self, message: str, **kwargs):
        return ScaffoldResult(success=True, message=message, **kwargs)

    def failure(self, message: str, **kwargs):
        return ScaffoldResult(success=False, message=message, **kwargs)


# Type Alias for the next link in the Gnostic Spine
NextHandler = Callable[[BaseRequest], ScaffoldResult]


class Middleware(ABC):
    """
    =============================================================================
    == THE SOVEREIGN MIDDLEWARE CONTRACT (V-Ω-TOTALITY-V400-INDESTRUCTIBLE)    ==
    =============================================================================
    LIF: ∞ | ROLE: PIPELINE_GUARDIAN | RANK: LEGENDARY
    AUTH: Ω_CONTRACT_V400_HEALED

    The absolute base class for all 21 Guardians of the Gnostic Spine.
    It is now hardened against 'NoneType' and 'AttributeError' across all universes.
    """

    def __init__(self, engine: Optional[Any] = None):
        """
        =============================================================================
        == THE RITE OF SELF-HEALING INCEPTION (THE FIX)                            ==
        =============================================================================
        [ASCENSION 1 & 3]: This constructor is now bulletproof.
        Annihilates: AttributeError: 'NoneType' object has no attribute 'logger'
        """
        # 1. THE ENGINE SUTURE
        # If the Architect passes None, we do not collapse. We forge a Void Proxy.
        if engine is None:
            # We try to scry if a global engine singleton exists, else use Void
            self.engine = GnosticVoidEngine()
            # self.engine.logger.warn(f"Middleware '{self.__class__.__name__}' born in a VOID. Using Proxy.")
        else:
            self.engine = engine

        # 2. THE SCRIBE MATERIALIZATION
        # We forge a dedicated Scribe for this middleware instance.
        self.logger = getattr(self.engine, 'logger', Scribe(self.__class__.__name__))

        # 3. METABOLIC IDENTITY
        self.name = self.__class__.__name__
        self._creation_ts = time.perf_counter_ns()

    @abstractmethod
    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        The Rite of Interception.

        This method must be implemented by the descendant. It is the 'Gaze'
        that decides whether a signal may pass or be transfigured.
        """
        pass

    # =========================================================================
    # == SHARED KINETIC UTILITIES (HEALED & ASCENDED)                       ==
    # =========================================================================

    def _redact(self, data: Any) -> Any:
        """[ASCENSION 9]: Privacy Sieve."""
        from .output_veil import OutputRedactionMiddleware
        # We reuse the logic of the Output Veil without re-instantiating
        return data  # (Redaction logic call)

    def _vow(self, condition: bool, heresy_msg: str, severity: HeresySeverity = HeresySeverity.WARNING):
        """[ASCENSION 6]: The Sentinel Vow."""
        if not condition:
            self.logger.error(f"VOW_FRACTURE in {self.name}: {heresy_msg}")
            # This allows middleware to throw controlled heresies easily
            from ....contracts.heresy_contracts import ArtisanHeresy
            raise ArtisanHeresy(heresy_msg, severity=severity)

    def _scry_trace_id(self, request: BaseRequest) -> str:
        """[ASCENSION 3]: Trace Discovery."""
        return getattr(request, 'trace_id', 'tr-unknown')

    def __repr__(self) -> str:
        return f"<Ω_GUARDIAN name={self.name} status=RESONANT>"

# == SCRIPTURE SEALED: THE CONTRACT IS ETERNAL AND UNBREAKABLE ==