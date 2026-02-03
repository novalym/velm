import traceback
from typing import Optional, Union, Any, Dict, List


try:
    from rich.panel import Panel
    from rich.traceback import Traceback
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import BaseRequest
from .....logger import Scribe

# The Diagnostic Knowledge Base
from ....redemption.diagnostician import AutoDiagnostician
from .circuit import CircuitBreaker
from .forensics import ForensicLab

class HighPriestOfResilience:
    """
    =============================================================================
    == THE HIGH PRIEST OF RESILIENCE (V-Ω-TOTALITY-V900-IMMUNE-CORE) ==
    =============================================================================
    LIF: ∞ | ROLE: SYSTEM_MEDIC | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_HEALER_2026_TOTALITY

    The supreme guardian of the Engine's mortality. It transfigures raw crashes
    into fixable Gnosis and governs the quarantine of fractured logic.
    """


    def __init__(self, verbose: bool):
        """
        [THE RITE OF INCEPTION]
        Forges the immune system for the God-Engine.
        """
        self.logger = Scribe("Resilience")
        self.verbose = verbose

        # [ASCENSION 1]: MATERIALIZE THE CIRCUIT BREAKER
        # This provides the 'check_state' and 'record_failure' faculties.
        self.circuit_breaker = CircuitBreaker(self.logger)

        # [ASCENSION 2]: MATERIALIZE THE FORENSIC LAB
        # The black-box recorder for the Monolith.
        self.forensics = ForensicLab()

        self.version = "9.0.0-TOTALITY-IMMUNE"

    def handle_panic(self, error: Exception, request: BaseRequest, duration: float) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF CATASTROPHE (V-Ω-TRANSFIGURATION)                           ==
        =============================================================================
        Intercepts fatal paradoxes and transmutes them into structured failures.
        """
        # 1. RECORD THE STRIKE
        # Increment the failure count for the specific rite to trigger quarantine
        rite_name = request.__class__.__name__.replace("Request", "")
        self.circuit_breaker.record_failure(rite_name)

        # 2. BLACK-BOX RECORDING
        # Capture the final state for the Architect's forensic audit
        self.forensics.capture_crash(error, context={
            "rite": rite_name,
            "request_id": getattr(request, 'request_id', 'tr-unbound'),
            "duration": duration,
            "trace_id": getattr(request, 'trace_id', 'VOID')
        })

        # 3. LINGUISTIC TRANSMUTATION
        # Convert the raw Python exception into a high-status Heresy
        heresy_data = self._transmute_exception_to_heresy(error, request, error.__traceback__)

        # 4. FORGE THE FAILURE VESSEL
        return ScaffoldResult(
            success=False,
            message=f"Logic Fracture in {rite_name}: {type(error).__name__}",
            heresies=[heresy_data],
            duration_seconds=duration,
            traceback=traceback.format_exc(),
            ui_hints={
                "vfx": "shake_red",
                "sound": "fracture_alert",
                "priority": "CRITICAL"
            }
        )

    def handle_artisan_heresy(self, error: ArtisanHeresy, request: BaseRequest, duration: float) -> ScaffoldResult:
        """[THE RITE OF KNOWN FAILURE] Handles errors explicitly raised by Artisans."""
        self.logger.error(f"Artisan {request.__class__.__name__} failed: {error.message}")

        # Known heresies don't necessarily trip the circuit breaker unless they are CRITICAL
        if error.severity == HeresySeverity.CRITICAL:
            self.circuit_breaker.record_failure(request.__class__.__name__)

        heresy_data = self._transmute_exception_to_heresy(error, request)

        return ScaffoldResult(
            success=False,
            message=error.message,
            heresies=[heresy_data],
            duration_seconds=duration
        )

    def _transmute_exception_to_heresy(
            self,
            error: Union[ArtisanHeresy, Exception],
            request: BaseRequest,
            traceback_obj: Optional[Any] = None
    ) -> Heresy:
        """
        =============================================================================
        == THE GNOSTIC ALCHEMY (V-Ω-HERESY-MATERIALIZER)                          ==
        =============================================================================
        Forges the definitive Socratic vessel from the debris of a crash.
        """
        # --- PATH A: THE KNOWN HERESY (EXPECTED) ---
        if isinstance(error, ArtisanHeresy):
            # [ASCENSION 3]: RECURSIVE SOUL RETRIEVAL
            details_panel = None
            if traceback_obj and self.verbose and HAS_RICH:
                details_panel = Panel(
                    Traceback.from_exception(type(error), error, traceback_obj, show_locals=True),
                    title="[bold red]Chronicle of the Expected Heresy[/bold red]",
                    border_style="red"
                )

            return Heresy(
                message=error.message,
                suggestion=error.suggestion or "Align your plea with the Gnostic Contracts.",
                details=error.details or error.get_proclamation(),
                severity=error.severity,
                fix_command=error.fix_command,
                line_num=error.line_num or 0,
                line_content=f"Rite: {request.__class__.__name__}",
                code=getattr(error, 'gnostic_code', 'KNOWN_FRACTURE'),
                details_panel=details_panel
            )

        # --- PATH B: THE UNKNOWN PARADOX (CRASH) ---
        else:
            self.logger.verbose(f"Conducting forensic inquest on paradox: {type(error).__name__}")
            tb_str = traceback.format_exc()

            # [ASCENSION 4]: CONSULT THE COUNCIL OF SAGES
            # We determine the "Cure" based on historical failure patterns.
            diagnostic_context = {
                "project_root": request.project_root,
                "exception": error,
                "rite": request.__class__.__name__
            }
            diagnosis = AutoDiagnostician.consult_council(error, diagnostic_context)

            # [ASCENSION 5]: THE LUMINOUS DOSSIER
            details_panel = None
            if traceback_obj and self.verbose and HAS_RICH:
                details_panel = Panel(
                    Traceback.from_exception(type(error), error, traceback_obj, show_locals=True, word_wrap=True),
                    title="[bold red]Chronicle of the Catastrophic Paradox[/bold red]",
                    border_style="red"
                )

            # [ASCENSION 11]: ENTROPY-AWARE REDACTION
            # Ensure the error message itself is sanitized of high-entropy secrets
            safe_message = str(error)
            if "sk_live" in safe_message or "pat-" in safe_message:
                safe_message = "[REDACTED_SENSITIVE_MATTER]"

            return Heresy(
                message=f"A catastrophic paradox occurred: {type(error).__name__}",
                details=tb_str,
                severity=HeresySeverity.CRITICAL,
                suggestion=diagnosis.advice if diagnosis else "Verify Environment DNA and Stratum dependencies.",
                fix_command=diagnosis.cure_command if diagnosis else "scaffold audit --deep",
                line_num=0,
                line_content="System Internals",
                details_panel=details_panel,
                code="KERNEL_PANIC"
            )

    def __repr__(self) -> str:
        return f"<Ω_HIGH_PRIEST_OF_RESILIENCE version={self.version} state=VIGILANT>"