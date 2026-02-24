# Path: artisans/dream/neural_engine/prophet.py
# ---------------------------------------------

import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

from ....core.ai.engine import AIEngine
from ....core.ai.contracts import NeuralPrompt
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe
from .constitution import forge_system_prompt
from .validator import NeuralInquisitor

Logger = Scribe("Dream:NeuralProphet")


class NeuralProphet:
    """
    =============================================================================
    == THE NEURAL PROPHET (V-Ω-GENERATIVE-ARCHITECT)                           ==
    =============================================================================
    LIF: ∞ | ROLE: DYNAMIC_BLUEPRINT_FORGER
    """
    MAX_RETRIES = 2

    def __init__(self, engine):
        self.engine = engine
        self.ai = AIEngine.get_instance()
        # [ASCENSION]: We inject the engine into the Inquisitor for Shadow Parsing
        self.inquisitor = NeuralInquisitor(engine=self.engine)

    def forge_blueprint(self, intent: str, project_root: Path) -> Tuple[str, float]:
        """The Rite of Genesis (Creation)."""
        return self._commune(intent, "GENESIS", {})

    def forge_evolution(self, intent: str, context: Dict[str, Any]) -> Tuple[str, float]:
        """The Rite of Evolution (Mutation)."""
        Logger.info(f"🧬 The Neural Prophet is analyzing the existing organism for evolution...")

        project_type = context.get("project_type", "generic")
        files = ", ".join(context.get("file_structure", []))

        evolution_context = (
            f"CURRENT REALITY:\n"
            f"- Type: {project_type}\n"
            f"- Topography: {files}\n"
            f"\n"
            f"DIRECTIVE: The user wants to EVOLVE this project. "
            f"Generate a `.scaffold` blueprint that adds the requested feature. "
            f"Use `+=` to append to config files if needed, or create new files that integrate smoothly."
        )

        return self._commune(intent, "EVOLUTION", {"project_context": evolution_context})

    def _commune(self, intent: str, mode: str, extra_context: Dict[str, str]) -> Tuple[str, float]:
        """The Shared Communion Logic."""
        system_prompt = forge_system_prompt()

        # Inject context into user query
        full_query = f"Architect's Intent ({mode}): '{intent}'\n"
        if "project_context" in extra_context:
            full_query += f"\n{extra_context['project_context']}\n"
        full_query += "\nForge the .scaffold blueprint now."

        prompt = NeuralPrompt(
            user_query=full_query,
            system_instruction=system_prompt,
            model_hint="smart",
            max_tokens_override=8000,
            use_rag=True
        )

        attempts = 0
        total_cost = 0.0
        last_error = ""

        while attempts <= self.MAX_RETRIES:
            attempts += 1
            try:
                revelation = self.ai.active_provider.commune(prompt)
                total_cost += revelation.cost_usd

                clean_content = self.inquisitor.purify(revelation.content)

                # [ASCENSION]: The Shadow Parse occurs here
                is_valid, error_msg = self.inquisitor.adjudicate(clean_content)

                if is_valid:
                    Logger.success(
                        f"✨ Prophecy Resonant ({mode}). Model: {revelation.model_used} | Cost: ${total_cost:.4f}")
                    return clean_content, total_cost

                Logger.warn(f"Prophecy Fractured (Attempt {attempts}): {error_msg}")
                last_error = error_msg

                # The Self-Healing Loop: We feed the parser error back to the AI
                prompt.user_query += f"\n\n[SYSTEM ERROR]: Your previous output contained syntax errors: {error_msg}\n\nPlease regenerate the blueprint fixing this error. Output ONLY valid .scaffold code."

            except Exception as e:
                Logger.error(f"Neural Transmission Failed: {e}")
                raise ArtisanHeresy(f"Neural Prophecy Fractured: {e}", severity=HeresySeverity.CRITICAL)

        raise ArtisanHeresy(
            f"The Neural Prophet failed to manifest a valid {mode.lower()} blueprint.",
            details=f"Last Validation Error: {last_error}",
            severity=HeresySeverity.CRITICAL
        )
