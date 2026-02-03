# Path: scaffold/core/persona/manager.py
# --------------------------------------
# LIF: INFINITY | The Sovereign Persona Governor (V-Ω)

import sys
import threading
from typing import Optional, Dict
from .registry import PANTHEON
from ...contracts.persona_contracts import Persona
from ...logger import Scribe

Logger = Scribe("PersonaManager")


class PersonaManager:
    """
    =============================================================================
    == THE PERSONA MANAGER (V-Ω-SINGLETON-CONDUCTOR)                          ==
    =============================================================================
    The single source of truth for the Engine's intent.
    It holds the 'Active Mask' and broadcasts state changes to the Nexus.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PersonaManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized: return
        self._active_persona = PANTHEON["THE_INITIATE"]
        self._initialized = True
        Logger.success("Persona Manager Online. Initialized as 'The Initiate'.")

    @property
    def active(self) -> Persona:
        return self._active_persona

    def assume(self, persona_id: str) -> Persona:
        """The Rite of Assumption: Shifts the Engine's soul."""
        target = next((p for p in PANTHEON.values() if p.id == persona_id), None)

        if not target:
            Logger.error(f"Heresy: Persona '{persona_id}' is unknown to the Pantheon.")
            return self._active_persona

        with self._lock:
            self._active_persona = target

        # [ASCENSION]: Flush Telemetry to signal the shift
        print(f"[PersonaShift] Identity transfigured to: {target.name}", file=sys.stdout)
        sys.stdout.flush()

        Logger.success(f"Lattice frequency aligned to: [bold]{target.name}[/bold]")
        return self._active_persona

    def is_detector_enabled(self, detector_key: str) -> bool:
        """Topological Check: Should we scan this domain?"""
        return detector_key in self._active_persona.detectors or detector_key == "syntax"

    def get_neural_system_prompt(self) -> str:
        """[ASCENSION 2]: Injects Persona DNA into AI prompts."""
        style_prompts = {
            "INITIATE": "Provide only the most minimal, safe code corrections.",
            "MAESTRO": "Be proactive. Generate boilerplate, tests, and future-proof patterns.",
            "SENTINEL": "Focus on security, type safety, and error handling. Be skeptical.",
            "ARCHITECT": "Prioritize structural integrity, clean layers, and modularity.",
            "POET": "Focus on readability, documentation, and the narrative flow of code."
        }
        return style_prompts.get(self._active_persona.style.name, "")