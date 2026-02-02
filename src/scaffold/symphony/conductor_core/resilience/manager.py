# Path: scaffold/symphony/conductor_core/resilience/manager.py
# ------------------------------------------------------------

import os
import time
import subprocess
import shlex
import threading
import traceback
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, TYPE_CHECKING, Any, Dict, List, Union, Literal

# --- THE DIVINE SUMMONS OF THE PANTHEON & CONTRACTS ---
from .artifacts import ArtifactKeeper
from .diagnosis import NeuralDiagnostician
from .intercession import IntercessionAltar
from .contracts import IntercessionChoice, IntercessionOutcome, FailureContext
from ....contracts.heresy_contracts import ArtisanHeresy, GuardianHeresy, HeresySeverity
from ....contracts.symphony_contracts import Edict, ActionResult, EdictType
from ....logger import Scribe, get_console

if TYPE_CHECKING:
    from ...conductor.orchestrator import SymphonyConductor
    from ..context import GnosticContextManager

Logger = Scribe('SymphonyResilience')


class SymphonyResilienceManager:
    """
    =================================================================================
    == THE THRONE OF INTERCESSION (V-Ω-RESILIENCE-GOD-ENGINE)                      ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The Sovereign Guardian of Failure. It manages the lifecycle of paradoxes within
    the Symphony, transforming crashes into opportunities for Gnostic insight and
    interactive redemption.
    """

    def __init__(self, conductor: 'SymphonyConductor'):
        self.conductor = conductor
        # [FACULTY 5] The Forensic Scribe
        self.artifact_keeper = ArtifactKeeper(self.conductor.execution_root)
        # [FACULTY 6] The AI Co-Architect
        self.diagnostician = NeuralDiagnostician()
        self.console = get_console()
        # [FACULTY 9] The Luminous Dossier Forge
        self.altar = IntercessionAltar(self.console)

    @property
    def context(self) -> 'GnosticContextManager':
        """[FACULTY 6] The Telepathic Bridge to the Symphony's living memory."""
        return self.conductor.context_manager

    @contextmanager
    def rite_boundary(self, edict: Edict):
        """
        [FACULTY 1] The Rite Boundary.
        An unbreakable ward that wraps every edict execution, now honoring the
        sacred contract of the Gnostic Schism.
        """
        # [THE CORE FIX] The humble, mutable vessel is forged.
        outcome = IntercessionOutcome()

        try:
            yield outcome
        except Exception as heresy:
            # A paradox was perceived. The Rite of Intercession begins.
            # `handle_failure` will either re-raise or set the outcome choice.
            choice_from_altar = self.handle_failure(edict, heresy)
            outcome.choice = choice_from_altar

            # [FACULTY 8] The Heresy Propagator
            # If the Architect chose to skip or retry, we suppress the exception.
            # Otherwise, we allow the heresy to ascend to the main engine loop to halt the symphony.
            if outcome.choice not in [IntercessionChoice.SKIP, IntercessionChoice.RETRY]:
                raise heresy

    def handle_failure(self, edict: Edict, heresy: Exception) -> Optional[IntercessionChoice]:
        """
        [FACULTY 4 & 2] The Gnostic Triage & Pure Gnostic Contract.
        The central hub for processing any and all failures.
        """
        Logger.error(f"Paradox at L{edict.line_num}: {heresy}", exc_info=True)

        result: Optional[ActionResult] = None

        # If it's a known heresy from a subprocess, it will contain the ActionResult
        if isinstance(heresy, ArtisanHeresy) and isinstance(heresy.child_heresy, subprocess.CalledProcessError):
            e = heresy.child_heresy
            result = ActionResult(
                output=(e.stdout or "") + (e.stderr or ""),
                returncode=e.returncode,
                command=str(e.cmd),
                duration=0.0
            )
            self.conductor.engine.update_last_reality(result)

        # [THE CORE FIX] The sacred, immutable vessel is forged with the full Gnosis of the paradox.
        failure_dossier = FailureContext(
            edict=edict,
            heresy=heresy,
            traceback=traceback.format_exc(),
            variables=self.context.variables
        )

        # [FACULTY 5] The Forensic Scribe
        artifact_path = self.artifact_keeper.hoard(result, edict, heresy)

        # [FACULTY 8] The Dry-Run Prophet
        if self.context.conductor.is_simulation:
            Logger.warn("[SIMULATION] Heresy detected but intercession is stayed.")
            return None  # In simulation, we always halt on error.

        # [FACULTY 9] The Luminous Dossier & Intercession
        return self.enter_intercession_altar(failure_dossier, artifact_path)

    def enter_intercession_altar(
            self,
            dossier: FailureContext,
            artifact_path: Optional[str] = None
    ) -> Optional[IntercessionChoice]:
        """
        Summons the interactive TUI for the Architect's judgment.
        """
        # [FACULTY 3] The Unbreakable Ward of Context
        try:
            self.conductor.suspend_renderer()

            # This loop allows returning to the altar after an action like 'shell' or 'edit'
            while True:
                choice = self.altar.summon(
                    edict=dossier.edict,
                    heresy=dossier.heresy,
                    # We pass the last known result from the context for display
                    result=self.context.last_process_result,
                    artifact_path=artifact_path
                )

                if choice == IntercessionChoice.RETRY:
                    self._manual_retry(dossier.edict)
                    return choice
                elif choice == IntercessionChoice.SHELL:
                    self._open_shell()
                    continue
                elif choice == IntercessionChoice.EDIT:
                    path_to_edit = dossier.edict.source_blueprint or self.conductor.symphony_path
                    if path_to_edit:
                        self._summon_editor(path_to_edit)
                    else:
                        Logger.warn("No source blueprint to edit.")
                    continue
                elif choice == IntercessionChoice.DIAGNOSE:
                    self.diagnostician.consult_council(dossier.heresy, {"edict": dossier.edict,
                                                                        "result": self.context.last_process_result})
                    continue
                elif choice == IntercessionChoice.GOOGLE:
                    self.diagnostician._consult_web_oracle(dossier.heresy)
                    continue

                # For SKIP and ABORT, we return the choice to the engine.
                return choice

        except Exception as altar_heresy:
            Logger.error(f"META-HERESY: The Intercession Altar itself has shattered: {altar_heresy}")
            return IntercessionChoice.ABORT
        finally:
            self.conductor.resume_renderer()

    def _manual_retry(self, edict: Edict):
        """A simple proclamation for a manual retry."""
        self.console.rule("[bold yellow]Re-attempting the Broken Rite...[/bold yellow]")

    def _open_shell(self):
        """[FACULTY 2] The Cross-Platform Gnostic Shell Portal."""
        cwd = self.context.cwd
        Logger.warn(f"Entering Gnostic Sub-Shell at [cyan]{cwd}[/cyan]. Type 'exit' to return to the Altar.")

        env = os.environ.copy()
        try:
            for k, v in self.context.raw().items():
                if isinstance(v, (str, int, float, bool, Path)):
                    env[f"SC_VAR_{str(k).upper()}"] = str(v)
        except Exception as e:
            Logger.warn(f"Could not fully anoint shell environment: {e}")

        shell = os.environ.get("SHELL", "bash" if os.name != 'nt' else "cmd.exe")

        self.conductor.suspend_renderer()
        try:
            subprocess.run(shell, cwd=str(cwd), env=env)
        finally:
            self.conductor.resume_renderer()

        self.console.clear()

    def _summon_editor(self, path: Path):
        """Summons the Architect's preferred editor."""
        editor = os.environ.get("EDITOR", "code" if shutil.which("code") else "vi" if os.name != 'nt' else "notepad")
        self.conductor.suspend_renderer()
        try:
            # Use Popen to not block, but wait might be better for edit-and-continue workflow
            subprocess.run([editor, str(path)])
        finally:
            self.conductor.resume_renderer()
        self.console.clear()