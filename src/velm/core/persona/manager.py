# Path: src/velm/core/persona/manager.py
# --------------------------------------
# LIF: INFINITY | The Sovereign Persona Governor (V-Ω-PERSISTENT)

import sys
import os
import json
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Union

from .registry import PANTHEON, DEFAULT_PERSONA
from ...contracts.persona_contracts import Persona, WorkflowStyle
from ...logger import Scribe

Logger = Scribe("PersonaManager")


class PersonaManager:
    """
    =============================================================================
    == THE PERSONA MANAGER (V-Ω-SINGLETON-CONDUCTOR-PERSISTENT)                ==
    =============================================================================
    The single source of truth for the Engine's intent.

    ### THE ASCENDED FACULTIES:
    1.  **Atomic Persistence:** Remembers the active mask across CLI invocations via
        `~/.scaffold/persona.lock`.
    2.  **Environmental Override:** Obeys `SCAFFOLD_PERSONA` for CI/CD automation.
    3.  **Contextual Neural Bias:** Generates dynamic system prompts based on the
        current task (Coding vs. Architecture vs. Security).
    4.  **Haptic Broadcasting:** Signals state changes to the Ocular UI.
    """
    _instance = None
    _lock = threading.RLock()

    # The Global Persistance Anchor
    _STATE_FILE = Path.home() / ".scaffold" / "persona.lock"

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PersonaManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized: return

        self._active_persona: Persona = self._resurrect_state()
        self._initialized = True

        # Log only if not silent env
        if os.getenv("SCAFFOLD_SILENT") != "1":
            Logger.debug(f"Persona Manager Online. Mask: '[cyan]{self._active_persona.name}[/cyan]'.")

    @property
    def active(self) -> Persona:
        """Returns the currently enshrined Persona."""
        return self._active_persona

    def resolve_effective_persona(self, override_name: Optional[str] = None) -> Persona:
        """
        [THE RITE OF EPHEMERAL ASSUMPTION]
        Determines the persona for a *specific* operation.
        Priority:
        1. Explicit Override (CLI flag: --as-persona=maestro)
        2. Environment Variable (SCAFFOLD_PERSONA=sentinel)
        3. Persisted State (The Mask worn by the Manager)
        """
        # 1. Explicit Override
        if override_name:
            target = self._lookup(override_name)
            if target: return target

        # 2. Environment Override
        env_persona = os.getenv("SCAFFOLD_PERSONA")
        if env_persona:
            target = self._lookup(env_persona)
            if target: return target

        # 3. Persistent State
        return self._active_persona

    def assume(self, persona_id: str, persist: bool = True) -> Persona:
        """
        [THE RITE OF TRANSFIGURATION]
        Permanently shifts the Engine's global soul.
        """
        target = self._lookup(persona_id)

        if not target:
            Logger.error(f"Heresy: Persona '{persona_id}' is unknown to the Pantheon.")
            return self._active_persona

        with self._lock:
            self._active_persona = target
            if persist:
                self._persist_state()

        # [ASCENSION]: Flush Telemetry to signal the shift to the TUI/IDE
        # The Middleware will pick this up for the HUD update.
        Logger.success(f"Lattice frequency aligned to: [bold]{target.name}[/bold]")
        return self._active_persona

    def is_detector_enabled(self, detector_key: str) -> bool:
        """Topological Check: Should we scan this domain?"""
        return detector_key in self._active_persona.detectors or detector_key == "syntax"

    def get_neural_system_prompt(self, task_context: str = "general") -> str:
        """
        [ASCENSION 2]: DYNAMIC PROMPT INJECTION.
        Injects Persona DNA into AI prompts, tailored for the specific task.
        """
        base_prompt = f"You are acting as {self._active_persona.name}. "

        style_prompts = {
            "INITIATE": (
                "Adopt a cautious, learning-oriented mindset. "
                "Explain concepts clearly. Prefer safety over speed. "
                "Do not assume advanced knowledge."
            ),
            "MAESTRO": (
                "Act with high velocity and confidence. "
                "Generate boilerplate aggressively. Assume the user wants results, not lectures. "
                "Prioritize modern, idiomatic patterns."
            ),
            "SENTINEL": (
                "Adopt a paranoid, security-first mindset. "
                "Scrutinize every input. Assume hostile intent. "
                "Prioritize type safety, boundary checks, and error handling above all else."
            ),
            "ARCHITECT": (
                "Think in systems and patterns. "
                "Prioritize structural integrity, clean layering (SOLID), and long-term maintainability. "
                "Avoid quick hacks. Suggest refactors where appropriate."
            ),
            "POET": (
                "Focus on the narrative quality of the code. "
                "Prioritize readability, luminous documentation, and elegant naming. "
                "Code is literature."
            )
        }

        bias = style_prompts.get(self._active_persona.style.name, "")

        # [FUTURE]: Integrate task_context (e.g. "if task=='security', amplify Sentinel traits")
        return f"{base_prompt} {bias}"

    def _lookup(self, name_or_id: str) -> Optional[Persona]:
        """Scries the Pantheon for a matching soul."""
        key = name_or_id.upper().strip()
        # Direct ID match
        if key in PANTHEON:
            return PANTHEON[key]

        # Name search
        for p in PANTHEON.values():
            if p.name.upper() == key or p.id == key:
                return p
        return None

    def _persist_state(self):
        """[THE RITE OF MEMORY]: Writes the active mask to disk."""
        try:
            self._STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            state = {"active_id": self._active_persona.id, "last_updated": str(os.getpid())}
            self._STATE_FILE.write_text(json.dumps(state))
        except Exception as e:
            Logger.warn(f"Failed to persist Persona state: {e}")

    def _resurrect_state(self) -> Persona:
        """[THE RITE OF RECALL]: Loads the mask from disk."""
        # 1. Check Env First (Override persistence)
        env_persona = os.getenv("SCAFFOLD_PERSONA")
        if env_persona:
            target = self._lookup(env_persona)
            if target: return target

        # 2. Check Disk
        if self._STATE_FILE.exists():
            try:
                data = json.loads(self._STATE_FILE.read_text())
                target_id = data.get("active_id")
                target = self._lookup(target_id)
                if target: return target
            except Exception:
                pass

        # 3. Default
        return DEFAULT_PERSONA