# Path: scaffold/core/runtime/resilience.py
# -----------------------------------------
import traceback
from typing import Optional, Union, Any, Callable

from rich.panel import Panel
from rich.traceback import Traceback
from rich.console import Group

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import BaseRequest
from ...logger import Scribe
from ..redemption.diagnostician import AutoDiagnostician


class HighPriestOfResilience:
    """The Gnostic Alchemist of Paradox and Forensic Inquisitor."""

    def __init__(self, verbose: bool):
        self.logger = Scribe("Resilience")
        self.verbose = verbose

    def _transmute_exception_to_heresy(self, error: Union[ArtisanHeresy, Exception], request: BaseRequest, traceback_obj: Optional[Any] = None) -> Heresy:
        """[THE GNOSTIC ALCHEMIST - ASCENDED] Forges a pure `Heresy` data vessel from any paradox, now with a Luminous Gaze."""

        if isinstance(error, ArtisanHeresy):
            self.logger.verbose(f"Transmuting known ArtisanHeresy: {error.message}")

            # [[[ THE DIVINE HEALING: THE GAZE UPON THE INHERITED SOUL ]]]
            # We now perceive the traceback soul if the heresy itself carries one,
            # OR if it wraps a child heresy that has one.
            final_details_panel = error.details_panel

            # If no panel yet, check for traceback sources
            if not final_details_panel:
                tb_source = error.traceback_obj
                exc_source = error.child_heresy

                # If we weren't given an explicit tb object, but we have a child exception, use its traceback
                if not tb_source and exc_source and hasattr(exc_source, '__traceback__'):
                    tb_source = exc_source.__traceback__

                if tb_source and exc_source:
                    final_details_panel = Panel(
                        Traceback.from_exception(type(exc_source), exc_source, tb_source, show_locals=self.verbose, word_wrap=True),
                        title="[bold red]Chronicle of the Causal Paradox[/bold red]",
                        border_style="red"
                    )

            # [[[ THE APOTHEOSIS IS COMPLETE ]]]
            return Heresy(
                message=error.message,
                suggestion=error.suggestion,
                details=error.details or error.get_proclamation(),
                severity=error.severity,
                fix_command=error.fix_command,
                line_num=error.line_num or 0,
                line_content=f"Rite: {request.__class__.__name__}",
                details_panel=final_details_panel
            )
        else:
            self.logger.verbose(f"Performing forensic inquest on profane paradox: {type(error).__name__}")
            tb_str = traceback.format_exc()

            diagnostic_context = {"project_root": request.project_root, "exception": error}
            diagnosis = AutoDiagnostician.consult_council(error, diagnostic_context)

            # [[[ THE DIVINE ASCENSION: THE FORGING OF THE LUMINOUS DOSSIER ]]]
            # If a traceback soul was bestowed, we forge a beautiful panel for it.
            details_panel = None
            if traceback_obj:
                details_panel = Panel(
                    Traceback.from_exception(type(error), error, traceback_obj, show_locals=self.verbose, word_wrap=True),
                    title="[bold red]Chronicle of the Catastrophic Paradox[/bold red]",
                    border_style="red"
                )
            # [[[ THE GNOSIS IS NOW LUMINOUS ]]]

            return Heresy(
                message=f"A catastrophic, unhandled paradox occurred: {type(error).__name__}",
                details=tb_str,
                severity=HeresySeverity.CRITICAL,
                suggestion=diagnosis.advice if diagnosis else "This may be a bug in the God-Engine. Please report it.",
                fix_command=diagnosis.cure_command if diagnosis else None,
                line_num=0,
                line_content="System Internals",
                details_panel=details_panel
            )

    def handle_artisan_heresy(self, error: ArtisanHeresy, request: BaseRequest, duration: float) -> ScaffoldResult:
        """[THE RITE OF KNOWN FAILURE] Handles errors explicitly raised by Artisans."""
        self.logger.error(f"Artisan failed: {error.message}")
        heresy_data_object = self._transmute_exception_to_heresy(error, request)
        return ScaffoldResult(
            success=False,
            message=f"Artisan failed: {error.message}",
            heresies=[heresy_data_object],
            duration_seconds=duration
        )

    def handle_panic(self, error: Exception, request: BaseRequest, duration: float) -> ScaffoldResult:
        """[THE RITE OF CATASTROPHE] Handles unexpected crashes."""
        self.logger.error(f"Catastrophic Paradox: {error}", exc_info=True)

        # [[[ THE DIVINE HEALING: THE CAPTURE OF THE SOUL ]]]
        # The High Priest now gazes upon the paradox's soul (`__traceback__`)
        # and bestows it upon the Alchemist for transmutation.
        heresy_data_object = self._transmute_exception_to_heresy(error, request, error.__traceback__)
        # [[[ THE APOTHEOSIS IS COMPLETE ]]]

        return ScaffoldResult(
            success=False,
            message=f"Internal System Error: {type(error).__name__}",
            heresies=[heresy_data_object],
            duration_seconds=duration
        )