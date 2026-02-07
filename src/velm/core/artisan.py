# Path: src/velm/core/artisan.py
# -----------------------------
# =========================================================================================
# == THE SACRED ANCESTOR OF ALL ARTISANS (V-Ω-TOTALITY-V2000-LEGENDARY)                ==
# =========================================================================================
# LIF: INFINITY | ROLE: LOGIC_BASE_CONTRACT | RANK: OMEGA_SUPREME
# AUTH: Ω_BASE_ARTISAN_V2000_TOTALITY
# =========================================================================================

from abc import ABC, abstractmethod
from pathlib import Path
import time
import sys
import traceback
from typing import Generic, TypeVar, TYPE_CHECKING, Optional, Any, List, Dict, Union

# --- THE DIVINE SUMMONS ---
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from .kernel.archivist import GnosticArchivist
from ..contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import BaseRequest
from ..logger import get_console, Scribe

if TYPE_CHECKING:
    from .runtime import ScaffoldEngine
    from ..parser_core.parser import ApotheosisParser
    from ..core.alchemist import DivineAlchemist

Req = TypeVar('Req', bound=BaseRequest)


class BaseArtisan(ABC, Generic[Req]):
    """
    =================================================================================
    == THE SOVEREIGN ANCESTOR (V-Ω-TOTALITY-V2000)                                 ==
    =================================================================================
    LIF: INFINITY | ROLE: ANCESTRAL_LOGIC_CONDUCTOR

    The foundational soul of every kinetic limb in the Scaffold Cosmos.
    Provides the standard rites for Success, Failure, and Reality Manipulation.
    """
    _request_context: Optional[Req] = None

    def __init__(self, engine: 'ScaffoldEngine'):
        """
        The Rite of Inception. Binds the Artisan to the God-Engine's Core.
        """
        self.engine = engine
        # Initialize the internal scribe for this specific limb
        self.logger = Scribe(self.name)

    # =========================================================================
    # == THE GNOSTIC SENSES (PROPERTIES)                                     ==
    # =========================================================================

    @property
    def name(self) -> str:
        """Proclaims the unique name of the Artisan."""
        return self.__class__.__name__.replace("Artisan", "")

    @property
    def parser(self) -> 'ApotheosisParser':
        """
        =============================================================================
        == THE UNIFIED FACTORY ANCHOR (V-Ω-THE-CURE)                               ==
        =============================================================================
        [THE CURE]: Surgically anchors the ApotheosisParser to every Artisan.
        Annihilates 'AttributeError: parser' across all timelines.
        """
        # We delegate to the Engine's factory to ensure grammar synchronization
        return self.engine.parser_factory()

    @property
    def alchemist(self) -> 'DivineAlchemist':
        """The Gnostic Conduit to the Transmutation Engine (Jinja)."""
        return self.engine.alchemist

    @property
    def project_root(self) -> Path:
        """
        [THE GNOSTIC ANCHOR]
        Priority resolution of the physical sanctum.
        """
        if self._request_context and self._request_context.project_root:
            root = self._request_context.project_root
            return Path(root).resolve() if isinstance(root, str) else root.resolve()

        if self.engine and self.engine.project_root:
            root = self.engine.project_root
            return Path(root).resolve() if isinstance(root, str) else root.resolve()

        return Path.cwd().resolve()

    @property
    def vitals(self) -> Dict[str, Any]:
        """Scries the current metabolic heat of the host machine."""
        return self.engine.get_system_vitals()

    @property
    def console(self):
        """The Luminous Voice (Standard Console)."""
        return getattr(self.engine, 'console', None) or get_console()

    @property
    def request(self) -> Req:
        """
        The Gnostic Bridge to the active intent.
        Guards against out-of-context access.
        """
        if self._request_context is None:
            raise ArtisanHeresy(
                f"Gnostic Schism: Attempted to access 'self.request' in '{self.name}' outside of an active rite.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Only access 'self.request' within the 'execute' symphony."
            )
        return self._request_context

    # =========================================================================
    # == THE SYMPHONY OF EXECUTION                                           ==
    # =========================================================================

    @abstractmethod
    def execute(self, request: Req) -> ScaffoldResult:
        """
        The Core Logic. To be implemented by every Descendant.
        """
        pass

    def __call__(self, request: Req) -> ScaffoldResult:
        """
        =============================================================================
        == THE CHRONOMETRIC HEARTBEAT (V-Ω-EXECUTION-WRAPPER)                      ==
        =============================================================================
        The magic gateway that wraps 'execute'. Handles timing, state, and cleanup.
        """
        self._request_context = request
        start_time = time.perf_counter()

        # [ASCENSION 8]: Multi-Tenant Identity Guard
        self._validate_identity_moat(request)

        try:
            # Ignite the Rite
            result = self.execute(request)

            # [ASCENSION 5]: Automatic Telemetry Population
            if result and hasattr(result, 'duration_seconds'):
                result.duration_seconds = time.perf_counter() - start_time

            # [ASCENSION 6]: Trace Suture
            if result and not getattr(result, 'trace_id', None):
                object.__setattr__(result, 'trace_id', getattr(request, 'trace_id', 'tr-void'))

            return result
        except Exception as e:
            # [ASCENSION 10]: Catastrophic Error Transmutation
            duration = time.perf_counter() - start_time
            return self.failure(
                message=f"Catastrophic Paradox in {self.name}: {type(e).__name__}",
                details=str(e),
                traceback=traceback.format_exc(),
                duration_seconds=duration
            )
        finally:
            # Dissolve the temporary bond
            self._request_context = None

    # =========================================================================
    # == THE RITES OF PROCLAMATION (RESULTS)                                 ==
    # =========================================================================

    def success(self,
                message: str,
                data: Any = None,
                artifacts: List[Artifact] = None,
                suggestion: Optional[str] = None,
                ui_hints: Optional[Dict[str, Any]] = None,
                **kwargs) -> ScaffoldResult:
        """Forges a pure ScaffoldResult vessel of victory."""
        # [ASCENSION 11]: Automatic Suggestion Prophecy
        if not suggestion and self.engine.predictor:
            next_moves = self.engine.predict_next_move()
            if next_moves:
                suggestion = f"Prophesied Next Step: 'velm {next_moves[0].replace('Request', '').lower()}'"

        return ScaffoldResult(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            suggestion=suggestion,
            ui_hints=ui_hints or {"vfx": "bloom", "sound": "consecration_complete"},
            source=self.name,
            **kwargs
        )

    def failure(self,
                message: str,
                suggestion: str = None,
                details: str = None,
                data: Any = None,
                traceback: str = None,
                ui_hints: Optional[Dict[str, Any]] = None,
                **kwargs) -> ScaffoldResult:
        """Forges a profane ScaffoldResult vessel of lamentation."""
        # [ASCENSION 10]: Automated stack capture
        if not traceback and sys.exc_info()[0]:
            import traceback as tb_module
            traceback = tb_module.format_exc()

        heresy = Heresy(
            message=message, line_num=0, line_content=self.name,
            severity=HeresySeverity.CRITICAL, suggestion=suggestion, details=details
        )

        return ScaffoldResult(
            success=False,
            message=message,
            heresies=[heresy],
            data=data,
            traceback=traceback,
            ui_hints=ui_hints or {"vfx": "shake_red", "sound": "fracture_alert"},
            source=self.name,
            **kwargs
        )

    # =========================================================================
    # == THE KINETIC LIMBS (UTILITIES)                                       ==
    # =========================================================================

    def broadcast(self, method: str, params: Dict[str, Any]):
        """
        =============================================================================
        == THE TELEPATHIC HERALD (V-Ω-UI-BROADCAST)                                ==
        =============================================================================
        Sends a real-time signal to the Ocular Interface (React/Electron).
        """
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": method,
                "params": params,
                "trace_id": getattr(self._request_context, 'trace_id', 'tr-unbound')
            })

    def ask(self, question: str, default: Any = None, choices: List[str] = None) -> Any:
        """
        =============================================================================
        == THE SOCRATIC INQUISITOR (V-Ω-INTERACTIVE-DIALOGUE)                      ==
        =============================================================================
        Performs a managed communion with the Architect.
        Respects non_interactive mode.
        """
        if self._request_context and getattr(self._request_context, 'non_interactive', False):
            self.logger.verbose(f"Non-Interactive mode: Defaulting '{question}' -> {default}")
            return default

        if choices:
            return Prompt.ask(question, choices=choices, default=default, console=self.console)

        if isinstance(default, bool):
            return Confirm.ask(question, default=default, console=self.console)

        return Prompt.ask(question, default=default, console=self.console)

    def guarded_execution(self, targets: List[Path], request: BaseRequest, context: str = "rite") -> bool:
        """[THE GUARDIAN'S OFFER] Standardized logic for pre-flight backups."""
        valid_targets = [t for t in targets if t.exists()]
        if not valid_targets or request.force or request.dry_run or request.preview:
            return True

        archivist = GnosticArchivist(self.project_root)
        if request.non_interactive:
            self.logger.info(f"Non-interactive mode. Auto-archiving {len(valid_targets)} item(s).")
            archivist.create_snapshot(valid_targets, reason=f"auto_{context}")
            return True

        self.console.print(Panel(
            f"This rite will modify {len(valid_targets)} existing scripture(s).\nA safety snapshot can be forged in [cyan].scaffold/backups/[/cyan].",
            title=f"[bold green]🛡️ The Guardian's Offer ({context})[/bold green]", border_style="green"
        ))
        if Confirm.ask("[bold question]Forge safety snapshot?[/bold question]", default=True):
            archivist.create_snapshot(valid_targets, reason=f"manual_{context}")
        else:
            self.logger.warn("Proceeding without a net.")
        return True

    def _validate_identity_moat(self, request: BaseRequest):
        """[ASCENSION 8] Security Ward: Verifies tenant isolation."""
        nov_id = getattr(request, 'novalym_id', None)
        if nov_id == "FORBIDDEN":
            raise ArtisanHeresy("Identity Fracture: This sanctum is barred.", severity=HeresySeverity.CRITICAL)

    def __repr__(self) -> str:
        return f"<Ω_ARTISAN name={self.name} status=VIGILANT>"

# == SCRIPTURE SEALED: THE ANCESTOR HAS ASCENDED ==