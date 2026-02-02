# Path: scaffold/symphony/conductor_core/handlers/base.py
# -------------------------------------------------------
from __future__ import annotations
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union, Callable

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe, get_console
from ....core.alchemist import get_alchemist

if TYPE_CHECKING:
    from ..engine import SymphonyEngine
    from ...conductor.orchestrator import SymphonyConductor
    from ...execution.interface import KineticInterface
    from ..resilience import SymphonyResilienceManager
    from ..context import GnosticContextManager
    from ...renderers.base import Renderer
    from ....core.alchemist import DivineAlchemist

Logger = Scribe('BaseHandler')


class BaseHandler:
    """
    =================================================================================
    == THE ANCESTRAL SOUL OF HANDLERS (V-Ω-PROPERTIES-HEALED)                      ==
    =================================================================================
    LIF: 10,000,000,000,000

    Synced with the GnosticContextManager properties.
    """

    def __init__(
            self,
            conductor: 'SymphonyConductor',
            engine: Optional['SymphonyEngine'] = None,
            performer: Optional['KineticInterface'] = None,
            resilience_manager: Optional['SymphonyResilienceManager'] = None,
            context_manager: Union['GnosticContextManager', Any] = None
    ):
        self._conductor = conductor
        self._engine = engine
        self._performer = performer
        self._resilience_manager = resilience_manager
        self._context_manager = context_manager

        self._alchemist = getattr(conductor, 'alchemist', get_alchemist())
        self._renderer = getattr(conductor, 'renderer', None)

        self.console = get_console()
        self.logger = Logger

        if not self._engine and hasattr(conductor, 'engine'):
            self._engine = conductor.engine

    @property
    def conductor(self):
        return self._conductor

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    @property
    def performer(self):
        return self._performer

    @property
    def resilience_manager(self):
        return self._resilience_manager

    @property
    def context_manager(self):
        return self._context_manager

    @property
    def alchemist(self):
        return self._alchemist

    @property
    def renderer(self):
        if self._renderer: return self._renderer
        if self._conductor and hasattr(self._conductor, 'renderer'):
            return self._conductor.renderer
        return None

    @property
    def variables(self) -> Dict[str, Any]:
        """Accesses context variables as a property."""
        if self._context_manager:
            return self._context_manager.variables  # Property access, no ()
        return {}

    @property
    def root(self) -> Path:
        """Accesses project root as a property."""
        if self._context_manager:
            val = self._context_manager.project_root  # Property access
            if callable(val): return val()
            return val
        return Path.cwd()

    def _redact_secrets(self, text: str) -> str:
        if not text: return ""
        for key in ['api_key', 'secret', 'token', 'password', 'key']:
            text = re.sub(f'({key}\\s*[:=]\\s*)([\'"]?)([^\\s\'"]+)([\'"]?)', r'\1\2******\4', text,
                          flags=re.IGNORECASE)
        return text

    def _validate_architecture(self):
        if not self._context_manager:
            raise ArtisanHeresy("Handler Heresy: No Gnostic Context Manager found.")
        if not self._engine:
            raise ArtisanHeresy("Handler Heresy: No Symphony Engine found.")