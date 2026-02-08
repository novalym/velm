# Path: src/velm/core/runtime/middleware/persona_warden.py
# --------------------------------------------------------
# LIF: 10,000,000 | The Gnostic Sentinel of Identity (V-Ω-EPHEMERAL-AWARE)

import time
import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ...persona.manager import PersonaManager
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..engine import ScaffoldEngine


class PersonaWardenMiddleware(Middleware):
    """
    =============================================================================
    == THE PERSONA WARDEN (V-Ω-EPHEMERAL-AWARE)                                ==
    =============================================================================
    The Guardian of the Mask.
    Intercepts every rite to inject the correct Identity, Physics, and Neural Bias.
    Supports ephemeral assumption via request variables.
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

        # 2. RESOLVE EFFECTIVE PERSONA
        # We check if the Architect willed a temporary mask for this specific rite.
        # e.g. `scaffold run ... --set persona=maestro`
        override_name = request.variables.get("persona") if request.variables else None

        # Ask the Manager to adjudicate the hierarchy (Override > Env > Persistent)
        active_persona = self.manager.resolve_effective_persona(override_name)

        # 3. [ASCENSION: NEURAL BIAS INJECTION]
        # We inject the Persona's DNA into the context for the AI and Alchemist.
        request.context["persona_id"] = active_persona.id
        request.context["persona_name"] = active_persona.name
        request.context["persona_style"] = active_persona.style.value
        request.context["neural_system_prompt"] = self.manager.get_neural_system_prompt()

        # Inject physics for the Chaos/Entropy subsystems
        request.context["physics_gravity"] = active_persona.physics_gravity
        request.context["neural_bias"] = active_persona.neural_bias

        # 4. [ASCENSION: KINETIC OVERRIDES]
        # Dynamically inject flags based on the chosen Intent.
        # e.g. Maestro automatically enables auto-redeem for minor heresies.
        if active_persona.auto_redeem:
            if request.variables is None: request.variables = {}
            request.variables["auto_redeem"] = True

        # 5. [ASCENSION: PERMISSION AEGIS]
        # Standard grade users (Initiates) are restricted from destructive rites
        # to prevent accidental annihilation of the cosmos.
        if active_persona.grade.value == "standard" and self._is_destructive(request):
            # We raise a Heresy to halt the pipeline immediately.
            raise ArtisanHeresy(
                message=f"Access Denied: Persona '{active_persona.name}' cannot execute {type(request).__name__}.",
                severity=HeresySeverity.CRITICAL,
                suggestion=(
                    "This rite requires a higher station. "
                    "Switch to a Power User persona (e.g., 'Architect') via `scaffold persona assume architect` "
                    "or pass `--set persona=architect`."
                )
            )

        # --- THE SYMPHONY PROCEEDS ---
        result = next_handler(request)
        # -----------------------------

        # 6. [ASCENSION: ATMOSPHERIC FEEDBACK]
        # We stamp the result so the Cockpit knows how to tint the UI based on the *effective* persona.
        if result and result.data is not None:
            # Handle both Pydantic objects and Dicts (The Cure)
            if isinstance(result.data, dict):
                result.data["_persona"] = {
                    "id": active_persona.id,
                    "tint": active_persona.ui_tint,
                    "gravity": active_persona.physics_gravity,
                    "label": active_persona.name
                }

        return result

    def _is_destructive(self, request: BaseRequest) -> bool:
        """
        Divines if a rite is destructive based on its name or intent.
        """
        name = type(request).__name__
        destructive_keywords = ["Excise", "Prune", "Annihilate", "Delete", "Wipe", "Purge"]

        # Check class name
        if any(k in name for k in destructive_keywords):
            return True

        # Check dynamic command (e.g. `scaffold run ...`)
        command = getattr(request, 'command', '') or ''
        if command and any(k in command.lower() for k in ['rm ', 'delete', 'drop', 'truncate']):
            return True

        return False