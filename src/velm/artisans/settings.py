import sys
from pathlib import Path
from typing import Optional

from ..core import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces import ScaffoldResult
from ..interfaces.requests import SettingsRequest
from ..settings.manager import SettingsManager
from ..settings.tui import SettingsAltar
from ..utils import find_project_root


@register_artisan("settings")
class SettingsArtisan(BaseArtisan[SettingsRequest]):
    """
    @gnosis:title The Altar of Configuration (`settings`)
    @gnosis:summary An interactive TUI to manage the soul of the Scaffold engine.
    @gnosis:related init weave creator
    @gnosis:keywords config preferences setup runtimes docker ai
    @gnosis:description
    The `settings` command summons the **Altar of Configuration**, a luminous,
    interactive Terminal User Interface (TUI) that allows the Architect to
    tune the very soul of the Velm God-Engine.

    It provides a unified, self-documenting dashboard to:
    1.  **Govern Runtimes:** Choose between System, Hermetic, or Docker execution strategies.
    2.  **Manage the Forge:** Configure template sources, Gist tokens, and auto-updates.
    3.  **Tune the Inquisitor:** Adjust the strictness of the Gnostic Gaze (linting) and security wards.
    4.  **Connect the Cortex:** Configure AI providers (OpenAI, Anthropic, Ollama) and models.
    5.  **Control Telemetry:** Opt-in or out of anonymous usage statistics.

    The Altar is context-aware. If summoned within a project, it allows you to
    override global defaults with project-specific Gnosis.
    """

    def execute(self, request: SettingsRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE RITE OF TUNING (V-Ω-INTERACTIVE-ULTIMA)                                 ==
        =================================================================================
        Conducts the symphony of configuration. It validates the environment,
        initializes the Hierarchy of Truth (SettingsManager), and launches the
        Visual Altar (TUI).
        """
        # 1. The Gnostic Ward of Interaction
        # The Altar is a visual medium. It cannot exist in the void of CI/CD.
        if request.non_interactive or not sys.stdout.isatty():
            return self.failure(
                "The Altar of Configuration requires a living Architect (interactive terminal).",
                suggestion="Edit `~/.scaffold/config.json` or `.scaffold/config.json` directly for automated environments."
            )

        # 2. The Consecration of the Sanctum
        # We attempt to resolve the project root. If found, the Altar will enable
        # the "Project Scope" tab, allowing for granular overrides.
        project_root = request.project_root or self._resolve_project_root()

        scope_label = f"[cyan]{project_root.name}[/cyan]" if project_root else "[dim]Global Scope[/dim]"
        self.logger.info(f"Summoning the Altar for: {scope_label}")

        try:
            # 3. The Awakening of the Manager
            # The Manager handles the "Cascade of Truth" (Defaults < Global < Project < Env).
            # It is the logic engine that the TUI will manipulate.
            manager = SettingsManager(project_root)

            # 4. The Rite of the Visual Interface
            # We summon the TUI, passing the initialized Manager.
            # The TUI takes control of the terminal window.
            altar = SettingsAltar(manager)
            altar.open()

            # 5. The Final Proclamation
            # When the TUI closes, we proclaim success. The Manager has already
            # persisted any changes to disk atomically.
            return self.success("The Architect has refined the soul of the engine.")

        except Exception as e:
            # The Unbreakable Ward of Grace
            # If the TUI crashes (e.g., screen size too small, encoding issues),
            # we catch the paradox and proclaim a helpful heresy.
            return self.failure(
                f"A paradox occurred within the Altar: {e}",
                details=str(e),
                suggestion="Ensure your terminal supports UTF-8 and has sufficient dimensions."
            )

    def _resolve_project_root(self) -> Optional[Path]:
        """
        [THE GAZE OF SCOPE]
        Attempts to find a valid project root to enable project-level settings.
        Delegates to the universal utility to ensure consistent detection logic.
        """
        root, _ = find_project_root(Path.cwd())
        return root