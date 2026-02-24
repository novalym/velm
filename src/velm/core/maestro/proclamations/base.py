# Path: core/maestro/proclamations/base.py
# ----------------------------------------

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING
from ....logger import Scribe

if TYPE_CHECKING:
    from ....core.runtime.engine import ScaffoldEngine
    from ....core.alchemist import DivineAlchemist

class ProclamationScribe(ABC):
    """
    =============================================================================
    == THE ANCESTRAL SCRIBE (V-Ω-CONTRACT-ASCENDED)                            ==
    =============================================================================
    LIF: ∞ | ROLE: ETHEREAL_MESSENGER | RANK: OMEGA_SOVEREIGN

    Defines the unbreakable contract for all visual and ethereal messengers.
    It has been healed of the Attribute Schism, capable of parsing variables
    regardless of the ontological shape of its assigned Engine.
    """

    def __init__(self, engine: 'ScaffoldEngine', alchemist: 'DivineAlchemist'):
        self.engine = engine
        self.alchemist = alchemist
        self.logger = Scribe(self.__class__.__name__)
        self.console = getattr(engine, 'console', None)

    @abstractmethod
    def proclaim(self, payload: str, metadata: Dict[str, Any]):
        """Transmutes the payload into the target medium."""
        pass

    def _purify(self, text: str) -> str:
        """
        =============================================================================
        == THE ALCHEMICAL HYDRATOR (V-Ω-APOPHATIC-RESOLUTION)                      ==
        =============================================================================
        [THE CURE]: Surgically extracts variables whether the context is a pure
        Dictionary, a Pydantic Model, or a GnosticSovereignDict, completely
        annihilating the 'dict object has no attribute variables' paradox.
        """
        if not text or not isinstance(text, str):
            return str(text)

        try:
            # 1. Scry the Context
            ctx = getattr(self.engine, 'context', {})

            # 2. Extract the Variables (The Apophatic Suture)
            variables = getattr(ctx, 'variables', ctx if isinstance(ctx, dict) else {})

            # 3. Transmute the Text
            return self.alchemist.transmute(text, variables)
        except Exception as e:
            # The Scribe must never die during a proclamation.
            # If the Alchemy fails, return the raw matter.
            self.logger.debug(f"Hydration paradox averted: {e}")
            return text