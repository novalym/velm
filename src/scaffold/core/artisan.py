# scaffold/core/artisan.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar, TYPE_CHECKING, Optional, Any, List, Dict

# --- THE DIVINE SUMMONS ---
from rich.panel import Panel
from rich.prompt import Confirm

from .kernel.archivist import GnosticArchivist
from ..contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import BaseRequest
from ..logger import get_console, Scribe

if TYPE_CHECKING:
    from .runtime import ScaffoldEngine

Req = TypeVar('Req', bound=BaseRequest)


class BaseArtisan(ABC, Generic[Req]):
    """
    =================================================================================
    == THE SACRED ANCESTOR OF ALL ARTISANS (V-Ω-ETERNAL-APOTHEOSIS)                ==
    =================================================================================
    @gnosis:title BaseArtisan
    @gnosis:summary The abstract soul and unbreakable Gnostic contract for all logic handlers.
    @gnosis:LIF 10,000,000,000

    This divine scripture defines the very essence of an Artisan. It has been ascended
    with the **Law of Luminous Failure**, a legendary faculty that bestows upon all its
    descendants the power to proclaim a heresy that is not a mute cry, but a rich,
    Gnostic dossier of diagnostic truth.
    ================================ LUMINOSITY =====================================
    """
    _request_context: Optional[Req] = None

    def __init__(self, engine: 'ScaffoldEngine'):
        self.engine = engine

    @property
    def project_root(self) -> Path:
        """
        [THE GNOSTIC ANCHOR - ASCENDED]
        Resolves the true Sanctum.
        Priority:
        1. The Active Request (Contextual Truth)
        2. The Engine's Configuration (System Truth)
        3. The Mortal Coil (CWD - Fallback)
        """
        # 1. Contextual Truth
        if self._request_context and self._request_context.project_root:
            # Ensure request context root is also a Path
            if isinstance(self._request_context.project_root, str):
                return Path(self._request_context.project_root).resolve()
            return self._request_context.project_root.resolve()

        # 2. System Truth (THE FIX)
        if self.engine and self.engine.project_root:
            root = self.engine.project_root
            # Defensive Type Casting: Annihilate the String Heresy
            if isinstance(root, str):
                root = Path(root)
            return root.resolve()

        # 3. Fallback
        return Path.cwd().resolve()

    @property
    def console(self):
        return getattr(self.engine, 'console', None) or get_console()

    @property
    def logger(self) -> 'Scribe':
        return self.engine.logger

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(self, request: Req) -> ScaffoldResult:
        pass

    @property
    def request(self) -> Req:
        """The Gnostic Bridge to the current rite's context."""
        if self._request_context is None:
            raise ArtisanHeresy(
                f"A Gnostic Schism occurred in '{self.name}'. An attempt was made to access the request context outside of a valid rite.",
                suggestion="Ensure all Gnosis is passed directly to helper artisans and that `self.request` is only accessed within the `execute` symphony."
            )
        return self._request_context

    def __call__(self, request: Req) -> ScaffoldResult:
        self._request_context = request
        try:
            return self.execute(request)
        finally:
            self._request_context = None

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

    def success(self,
                message: str,
                data: Any = None,
                artifacts: List[Artifact] = None,
                suggestion: Optional[str] = None,
                ui_hints: Optional[Dict[str, Any]] = None,
                fix_command: Optional[str] = None,
                **kwargs) -> ScaffoldResult:
        """
        =============================================================================
        == THE SUCCESS RITE (V-Ω-LUMINOUS-COMPASS-INFINITE)                        ==
        =============================================================================
        Forges a pure `ScaffoldResult` vessel.

        [ASCENSION LOG]:
        1. **Haptic Resonance:** Accepts `ui_hints` to trigger Ocular bloom/pulse effects.
        2. **Kinetic Seeds:** Accepts `fix_command` to embed executable redemption rites.
        3. **Infinite Horizon:** Accepts `**kwargs` to automatically map any future
           Gnostic fields directly to the result vessel.
        """
        return ScaffoldResult(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            suggestion=suggestion,
            ui_hints=ui_hints or {},
            fix_command=fix_command,
            **kwargs
        )

    def failure(self,
                message: str,
                suggestion: str = None,
                details: str = None,
                data: Any = None,
                traceback: str = None,
                ui_hints: Optional[Dict[str, Any]] = None,
                fix_command: Optional[str] = None,
                **kwargs) -> ScaffoldResult:
        """
        =================================================================================
        == THE LAW OF LUMINOUS FAILURE (V-Ω-APOTHEOSIS-INFINITE)                       ==
        =================================================================================
        Forges a profane `ScaffoldResult` vessel for a failed rite.

        [ASCENSION LOG]:
        1. **Forensic Payload:** Carries `data` and `traceback` for deep debugging.
        2. **Visual Alert:** Accepts `ui_hints` to trigger Ocular glitch/shake effects.
        3. **Redemption Path:** Accepts `fix_command` to offer immediate salvation.
        4. **Infinite Horizon:** Accepts `**kwargs` for future protocol expansions.
        ================================ LUMINOSITY =====================================
        """
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
            ui_hints=ui_hints or {},
            fix_command=fix_command,
            **kwargs
        )

    def partial_success(self, message: str, heresies: List[Heresy], data: Any = None) -> ScaffoldResult:
        """Forges a result for a rite that was partially pure, partially profane."""
        return ScaffoldResult(success=True, message=message, data=data, heresies=heresies)