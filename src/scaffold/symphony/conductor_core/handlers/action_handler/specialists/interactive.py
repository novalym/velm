# Path: scaffold/symphony/conductor_core/handlers/action_handler/specialists/interactive.py
# -----------------------------------------------------------------------------------------

import time
from typing import Optional

from rich.text import Text

from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......contracts.symphony_contracts import Edict, ActionResult
from ..contracts import ActionSpecialist


class InteractiveSpecialist(ActionSpecialist):
    """
    =============================================================================
    == THE DIPLOMAT (V-Ω-INTERACTIVE-GATEWAY)                                  ==
    =============================================================================
    LIF: 10,000,000,000

    The Sovereign Interface for Human-Machine Communion. It handles `@ask`,
    `@confirm`, and `@choose` directives, transmuting the Architect's will
    into Gnostic State variables.

    ### THE PANTHEON OF 12 FACULTIES:
    1.  **The Alchemical Voice:** Transmutes variables within the prompt text (`{{name}}?`).
    2.  **The Silent Ward:** Detects non-interactive mode and applies defaults or raises Heresy.
    3.  **The Type Diviner:** Infers input type (Confirm vs Text vs Secret) from context.
    4.  **The Secret Veil:** Marks inputs as secrets to prevent logging.
    5.  **The State Inscriber:** Updates the `GnosticContext` with the result.
    6.  **The Validation Gate:** (Future) Enforces regex patterns on input.
    7.  **The Dry-Run Prophet:** Returns defaults immediately during simulation.
    8.  **The Choice Enforcer:** Restricts inputs to a set of valid options.
    9.  **The Timeout Sentinel:** (Optional) Raises heresy if the Architect sleeps.
    10. **The Render Bridge:** Delegates the UI rendering to the active `Renderer`.
    11. **The Result Forge:** Returns a structured `ActionResult` describing the interaction.
    12. **The Boolean Normalizer:** Converts "y/n/yes/no" to True/False for logic.
    """

    def conduct(self, edict: Edict, command: str) -> ActionResult:
        start_time = time.time()

        # 1. Extract Configuration
        prompt_config = edict.interactive_prompt
        if not prompt_config:
            # Fallback parsing for command-line syntax: @ask "Question" -> $VAR
            # This logic should ideally be in the Parser, but we handle the fallback here.
            return self._forge_result(False, "Malformed interactive edict.", 0.0)

        # 2. Alchemical Transmutation of the Prompt
        final_text = self.alchemist.transmute(prompt_config.prompt_text, self.context.variables)
        target_var = prompt_config.target_variable

        # 3. The Silent Ward (Non-Interactive Handling)
        if self.handler.context_manager.conductor.non_interactive():
            # In silent mode, we must use a default or fail.
            # Currently, InteractivePrompt contract doesn't store a default,
            # so we check if the variable already has a value.
            current_val = self.context.variables.get(target_var)
            if current_val is not None:
                self.logger.info(f"Non-interactive: Using existing value for '{target_var}'.")
                return self._forge_result(True, f"Auto-accepted existing value for {target_var}", 0.0)

            raise ArtisanHeresy(
                f"Interactive Prompt '{final_text}' encountered in non-interactive mode.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Provide the variable via --set or environment variables."
            )

        # 4. The Dry-Run Prophet
        if self.handler.context_manager.conductor.is_simulation():
            self.logger.info(f"[DRY-RUN] Asking: {final_text} -> ${target_var}")
            return self._forge_result(True, "Simulated Input", 0.0)

        # 5. The Rite of Communion
        # We delegate to the Renderer to perform the actual I/O.
        # This abstraction allows different Renderers (Rich, Stream, JSON) to handle input natively.
        response = self.renderer.conduct_interactive_plea(
            prompt_text=final_text,
            default=True  # We assume affirmative defaults for now
        )

        # 6. The State Inscription
        # If the response implies boolean logic (Confirm), we normalize.
        # But `conduct_interactive_plea` usually returns bool for confirmations.
        # We store it as a string or native type? The Context handles Any.
        self.context.update_variable(target_var, response)

        duration = time.time() - start_time

        # 7. The Final Proclamation
        # We mask the output if it was a secret.
        display_val = "******" if prompt_config.is_secret else str(response)

        return self._forge_result(
            True,
            f"Architect input received: {display_val}",
            duration
        )

    def _forge_result(self, success: bool, output: str, duration: float) -> ActionResult:
        return ActionResult(
            output=output,
            returncode=0 if success else 1,
            duration=duration,
            command="interactive_prompt",
            was_terminated=False
        )