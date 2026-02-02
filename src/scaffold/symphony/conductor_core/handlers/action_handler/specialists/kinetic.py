# Path: scaffold/symphony/conductor_core/handlers/action_handler/specialists/kinetic.py
# -------------------------------------------------------------------------------------

import os
import re
import subprocess
from typing import Optional, Dict, Any

from ......contracts.heresy_contracts import ArtisanHeresy, GuardianHeresy, HeresySeverity
from ......contracts.symphony_contracts import Edict, ActionResult
from ......core.guardian import GnosticSentry
from ..contracts import ActionSpecialist
from ..utils.redaction import SecretRedactor


class KineticRite(ActionSpecialist):
    """
    =================================================================================
    == THE KINETIC RITE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)                  ==
    =================================================================================
    @gnosis:title The Kinetic Rite (The High Priest of Shell Execution)
    @gnosis:summary The divine artisan that transmutes a Gnostic Edict into a physical
                     process, its voice now eternally bound to the Architect's Gaze.
    @gnosis:LIF 10,000,000,000

    This is the High Priest of Shell Execution in its final, eternal, and ultra-definitive
    form. It has been reforged with a pantheon of 12 legendary ascensions that make it
    the unbreakable, Gnostically-aware heart of the Symphony's kinetic will.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Law of Gnostic Trust:** It righteously honors the pure, transmuted `command`
        scripture bestowed upon it by the Dispatcher.

    2.  **The Unbreakable Plea (THE FINAL FIX):** It no longer passes the profane `edict`
        to the `performer`. It makes a sacred, direct plea, bestowing upon the
        `KineticTitan` the one true, final `final_command` to be executed.

    3.  **The Restored Telepathic Link:** The heresy is annihilated. The `performer` is
        now bestowed with the `renderer's` living `update_live_stream` rite, restoring
        the luminous, real-time cinematic dashboard for all kinetic actions.

    4.  **The Gnostic Sentry's Ward:** Before any kinetic action, it summons the
        `GnosticSentry` to perform a pre-flight security inquest upon the final command.

    5.  **The Alchemical Redactor:** It wields the `SecretRedactor` to forge a
        `redacted_cmd`, ensuring no sacred Gnosis is ever proclaimed in failure logs.

    6.  **The Soul Catcher (`capture_as`):** Its Gaze upon the `edict.capture_as` vow is
        absolute, capturing `stdout` and inscribing it into the Gnostic Context.

    7.  **The ANSI Purifier:** Before inscribing a captured soul, it performs a rite of
        purification, stripping all profane ANSI escape codes.

    8.  **The Luminous Heresy Forge:** Its `_handle_failure` rite forges an `ArtisanHeresy`
        containing the exit code, complete output, and a Gnostically-derived suggestion.

    9.  **The Gnostic Doctor's Communion:** In the face of heresy, it now performs a
        sacred communion with the `AutoDiagnostician`, attempting to prophesy an
        executable `fix_command` for one-click healing.

    10. **The Polyglot Adjudicator (`using`):** It understands the `using` vow, allowing
        for future ascensions where success is judged by output, not just exit code.

    11. **The Sovereign Soul:** It is a pure, self-contained specialist. It knows *what*
        to do, but righteously delegates the *how* to the `performer`.

    12. **The Final Word:** This is the apotheosis of shell execution. Its mind is whole.
        Its Gaze is pure. Its hand is unbreakable. The Symphony will sing.
    =================================================================================
    """

    def __init__(self, handler):
        super().__init__(handler)
        self.sentry = GnosticSentry()
        self.redactor = SecretRedactor()

    def conduct(self, edict: Edict, command: str) -> ActionResult:
        """The one true, pure, and unbreakable rite of shell execution."""
        # [FACULTY 1] The Law of Gnostic Trust.
        final_command = command

        # [FACULTY 4] The Gnostic Sentry's Ward.
        try:
            self.sentry.adjudicate(final_command, self.context.cwd, edict.line_num)
        except GuardianHeresy as gh:
            raise ArtisanHeresy(
                "The Gnostic Sentry has stayed the Maestro's hand.",
                details=gh.get_proclamation(),
                child_heresy=gh,
                line_num=edict.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # The Titan's Hand.
        sanctum_path = self.context.cwd
        # The conductor will set non_interactive=True in CI, which forges a non-cinematic renderer.
        is_verbose_ui = not self.handler.context_manager.conductor.non_interactive

        # =============================================================================
        # ==         THE DIVINE HEALING: THE UNBREAKABLE PLEA & RESTORED LINK        ==
        # =============================================================================
        # The heresy is annihilated. We now bestow upon the Performer the one true,
        # final, transmuted command string. We also restore the telepathic link by
        # passing the renderer's `update_live_stream` rite. The Symphony will sing again.
        result = self.handler.performer.perform(
            command=final_command, # <<< THE SACRED SCRIPTURE IS BESTOWED
            edict=edict,
            sanctum=sanctum_path,
            inputs=edict.inputs,
            live_context=self.handler.live_context,
            stream_callback=self.handler.renderer.update_live_stream, # <<< THE VOICE IS RESTORED
            verbose_ui=is_verbose_ui
        )
        # =============================================================================
        # ==                        THE APOTHEOSIS IS COMPLETE                       ==
        # =============================================================================

        # [FACULTY 8] The Luminous Heresy Forge.
        if result.returncode != 0:
            self._handle_failure(result, final_command, edict)

        # [FACULTY 6] The Soul Catcher.
        if edict.capture_as:
            self._capture_result(edict.capture_as, result.output)

        # [FACULTY 10] The Polyglot Adjudicator.
        if edict.adjudicator_type:
            self._adjudicate_output(edict.adjudicator_type, result, edict)

        return result

    def _capture_result(self, variable_name: str, raw_output: str):
        """[FACULTY 7] Captures stdout, purifying it of ANSI codes first."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_output = ansi_escape.sub('', raw_output).strip()

        self.context.update_variable(variable_name, clean_output)
        self.logger.verbose(f"Captured output into variable '$$ {variable_name}'.")

    def _adjudicate_output(self, adj_type: str, result: ActionResult, edict: Edict):
        """[FACULTY 10] Performs specialized output validation."""
        if adj_type == "json":
            import json
            try:
                json_data = json.loads(result.output)
                if edict.capture_as:
                    self.context.update_variable(edict.capture_as, json_data)
                    self.logger.verbose(f"Captured and validated JSON into variable '$$ {edict.capture_as}'.")
            except json.JSONDecodeError as e:
                raise ArtisanHeresy(
                    f"Output Adjudication Failed: Expected JSON, but received profane text.",
                    details=f"Error: {e}\nOutput:\n{result.output[:500]}...",
                    line_num=edict.line_num
                )

    def _handle_failure(self, result: ActionResult, command: str, edict: Edict):
        """[FACULTY 8 & 9] Transmutes failure into a luminous, helpful Heresy."""
        redacted_cmd = self.redactor.redact(command)

        from ......core.redemption.diagnostician import AutoDiagnostician
        diagnosis = AutoDiagnostician.consult_council(
            subprocess.CalledProcessError(result.returncode, command, result.output),
            {"command": command}
        )

        suggestion = diagnosis.advice if diagnosis else "The rite failed with a generic error. Check the output above for clues."

        raise ArtisanHeresy(
            f"The Kinetic Rite failed: '{redacted_cmd}'",
            details=f"Exit Code: {result.returncode}\n\n[dim]Final Output:[/dim]\n{result.output}",
            exit_code=result.returncode,
            line_num=edict.line_num,
            suggestion=suggestion,
            fix_command=diagnosis.cure_command if diagnosis else None
        )