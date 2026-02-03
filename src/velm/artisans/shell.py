from pathlib import Path
from ..core.artisan import BaseArtisan
from ..interfaces.requests import BaseRequest
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult


class ShellRequest(BaseRequest):
    """A plea to enter the Gnostic Cockpit."""
    initial_command: str = None


@register_artisan("shell")
class ShellArtisan(BaseArtisan[ShellRequest]):
    """
    The Gateway to the Gnostic Cockpit.
    Summons the TUI environment.
    """

    def execute(self, request: ShellRequest) -> ScaffoldResult:
        from ..shell.app import GnosticShell

        self.logger.info("Summoning the Gnostic Shell...")

        # Initialize the App
        app = GnosticShell(project_root=self.project_root)

        # Run the App
        # This blocks until the user exits the shell
        app.run()

        return self.success("Session Concluded.")