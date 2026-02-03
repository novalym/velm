# Path: scaffold/core/runtime/middleware/healing.py
# -------------------------------------------------

import subprocess
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....core.redemption.diagnostician import AutoDiagnostician


class SelfHealingMiddleware(Middleware):
    """
    =============================================================================
    == THE PHOENIX (V-Ω-ACTIVE-RESURRECTION)                                   ==
    =============================================================================
    LIF: 10,000,000,000

    Intercepts failures. Consults the Gnostic Doctor. Applies the cure.
    Resurrects the request.
    """

    MAX_RESURRECTIONS = 1

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        attempts = 0

        while True:
            # 1. Attempt the Rite
            result = next_handler(request)

            # 2. If Pure, Return
            if result.success:
                return result

            # 3. The Gaze of the Doctor
            # If we have retries left and the result contains a Heresy with a Fix
            if attempts < self.MAX_RESURRECTIONS and result.heresies:
                heresy = result.heresies[0]
                fix = heresy.fix_command or AutoDiagnostician.diagnose(Exception(heresy.message))

                if fix:
                    # 4. The Rite of Self-Repair
                    self.logger.warn(f"The Phoenix perceives a cure: `{fix}`")

                    should_heal = request.force or (not request.non_interactive and self._ask_permission(fix))

                    if should_heal:
                        try:
                            self.logger.info(f"Administering cure...")
                            # Execute the fix (in the shell)
                            subprocess.run(fix, shell=True, check=True, capture_output=True)
                            self.logger.success("Cure applied. Resurrecting the original rite...")

                            attempts += 1
                            continue  # Retry the loop

                        except Exception as e:
                            self.logger.error(f"The Cure failed: {e}")
                            # Fall through to return original failure

            # Return the failure if we couldn't heal or ran out of retries
            return result

    def _ask_permission(self, fix: str) -> bool:
        from rich.prompt import Confirm
        return Confirm.ask(f"[bold green]Attempt Auto-Fix?[/bold green] (`{fix}`)")