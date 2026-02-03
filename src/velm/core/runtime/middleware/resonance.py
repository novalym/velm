# Path: scaffold/core/runtime/middleware/resonance.py
# ---------------------------------------------------
import os
import subprocess
import shlex
from pathlib import Path
from typing import List

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....settings.manager import SettingsManager


class ResonanceMiddleware(Middleware):
    """
    =============================================================================
    == THE HARMONIC RESONATOR (V-Ω-LIFECYCLE-HOOKS)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Enables user-defined side-effects (Hooks) before and after every Rite.
    The Engine becomes an Event Bus for the Operating System.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        settings = SettingsManager(request.project_root)
        rite_slug = type(request).__name__.replace("Request", "").lower()

        # 1. Pre-Resonance (Before the Rite)
        self._trigger_hooks(settings, f"hooks.pre_{rite_slug}", request)

        # 2. The Rite
        result = next_handler(request)

        # 3. Post-Resonance (After the Rite)
        hook_phase = "post" if result.success else "fail"
        self._trigger_hooks(settings, f"hooks.{hook_phase}_{rite_slug}", request)

        return result

    def _trigger_hooks(self, settings: SettingsManager, hook_key: str, request: BaseRequest):
        """Summons the shell to execute the Architect's will."""
        commands = settings.get(hook_key)

        if not commands:
            return

        # Normalize to list
        if isinstance(commands, str):
            commands = [commands]

        self.logger.verbose(f"Resonance detected: Triggering '{hook_key}'...")

        env = self._forge_env(request)
        cwd = request.project_root or Path.cwd()

        for cmd in commands:
            try:
                # We run hooks with shell=True to allow complex scripting
                # This is a power-user feature, so we assume they know the risks.
                subprocess.run(
                    cmd,
                    shell=True,
                    cwd=cwd,
                    env=env,
                    check=False,  # Hooks should not crash the main rite
                    stdout=subprocess.DEVNULL,  # Silence the hooks unless verbose?
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                self.logger.warn(f"Hook '{cmd}' faltered: {e}")

    def _forge_env(self, request: BaseRequest) -> dict:
        """Injects context into the hook environment."""
        env = os.environ.copy()
        env["SCAFFOLD_RITE"] = type(request).__name__
        env["SCAFFOLD_ROOT"] = str(request.project_root or "")
        return env