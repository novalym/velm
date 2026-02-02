# Path: scaffold/core/runtime/middleware/persona_warden.py
# --------------------------------------------------------
# LIF: 10,000,000 | The Gnostic Sentinel of Identity (V-Ω-REALIGNED)

import time
import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ...persona.manager import PersonaManager

if TYPE_CHECKING:
    from ..engine import ScaffoldEngine


class PersonaWardenMiddleware(Middleware):
    """
    =============================================================================
    == THE PERSONA WARDEN (V-Ω-REALIGNED-INCEPTION)                           ==
    =============================================================================
    The Guardian of the Mask. Realigned to satisfy the Pipeline's constructor law.
    """

    def __init__(self, engine: Optional['ScaffoldEngine'] = None):
        """
        [THE RITE OF INCEPTION - REALIGNED]
        Now accepts the engine instance to prevent the '2 were given' heresy.
        """
        super().__init__(engine)
        self.engine = engine
        self.logger = logging.getLogger("PersonaWarden")
        # Access the singleton PersonaManager
        self.manager = PersonaManager()

        if self.engine:
            self.logger.debug("PersonaWarden anchored to God-Engine.")

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Conducts the Rite of Identity Injection.
        """
        # 1. ENSURE CONTEXT MATERIALLY EXISTS
        if request.context is None:
            request.context = {}

        # 2. FETCH THE ACTIVE MASK FROM THE MANAGER
        # We perform this at the start of every request to support real-time switching
        active_persona = self.manager.active

        # 3. [ASCENSION: NEURAL BIAS]
        # Injects the specific 'Thinking Style' for the AI Co-Pilot
        request.context["persona_name"] = active_persona.name
        request.context["persona_style"] = active_persona.style.value
        request.context["neural_style"] = self.manager.get_neural_system_prompt()

        # 4. [ASCENSION: KINETIC OVERRIDES]
        # Dynamically inject flags based on the chosen Intent
        if active_persona.auto_redeem:
            request.variables["auto_redeem"] = True

        # 5. [ASCENSION: PERMISSION AEGIS]
        # Standard grade users are restricted from destructive rites
        if active_persona.grade.value == "standard" and self._is_destructive(request):
            return ScaffoldResult(
                success=False,
                message=f"Access Denied: Persona '{active_persona.name}' cannot execute {type(request).__name__}.",
                suggestion="Elevate your User Grade to 'Power' or 'Developer' in Settings."
            )

        # --- THE SYMPHONY PROCEEDS ---
        result = next_handler(request)
        # -----------------------------

        # 6. [ASCENSION: ATMOSPHERIC FEEDBACK]
        # We stamp the result so the Cockpit knows how to tint the UI
        if result.data is None:
            result.data = {}

        if isinstance(result.data, dict):
            result.data["_persona"] = {
                "id": active_persona.id,
                "tint": active_persona.ui_tint,
                "gravity": active_persona.physics_gravity,
                "label": active_persona.name
            }

        return result

    def _is_destructive(self, request: BaseRequest) -> bool:
        name = type(request).__name__
        return any(k in name for k in ["Excise", "Garden", "Purge", "Annihilate"])