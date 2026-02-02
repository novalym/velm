# Path: scaffold/core/runtime/middleware/safety.py
# ------------------------------------------------

from pathlib import Path
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class SafetyMiddleware(Middleware):
    """
    =============================================================================
    == THE SHIELD OF PRUDENCE (V-Ω-SAFETY-WARD)                                ==
    =============================================================================
    Intercepts destructive rites and validates them against the Laws of Safety.
    """

    DESTRUCTIVE_RITES = {'delete', 'clean', 'excise', 'uninstall'}
    PROTECTED_PATHS = {Path.home(), Path("/")}

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:

        # 1. Identify Destructive Intent
        command = getattr(request, 'command', None)

        if command in self.DESTRUCTIVE_RITES:
            target_path = getattr(request, 'target_path', None)
            if target_path:
                abs_target = Path(target_path).resolve()

                # 2. The Gaze of the Forbidden
                if abs_target in self.PROTECTED_PATHS:
                    raise ArtisanHeresy(
                        f"Safety Protocol Engaged: Cannot perform '{command}' on protected sanctum '{abs_target}'.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Check your target path. The Engine refuses to annihilate the root."
                    )

                # 3. The Rite of Confirmation (If interactive)
                if not request.force and not request.non_interactive:
                    # We rely on the Artisan to ask, OR we can enforce it here globally.
                    # Enforcing here guarantees safety across ALL artisans.
                    from rich.prompt import Confirm
                    if not Confirm.ask(f"[bold red]SAFETY CHECK:[/bold red] Confirm {command} on {abs_target}?"):
                        return self.engine.success("Rite stayed by Safety Middleware.")

        return next_handler(request)