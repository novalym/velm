# Path: scaffold/artisans/studio.py
# ---------------------------------

from pathlib import Path

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import StudioRequest


class StudioArtisan(BaseArtisan[StudioRequest]):
    """
    @gnosis:title The Architect's Sanctum (`studio`)
    @gnosis:summary Launches the full TUI Design Studio for interactive project management.
    """

    def execute(self, request: StudioRequest) -> ScaffoldResult:
        """
        The Rite of Immersion.
        Summons the GnosticShell to take control of the terminal.
        """
        # 1. Resolve the Sanctum
        start_path = Path(request.path).resolve() if request.path else Path.cwd()

        if not start_path.is_dir():
            raise ArtisanHeresy(f"The Gnostic Gaze found only a void. Sanctum does not exist at: '{start_path}'")

        self.logger.info(f"Awakening the Design Studio in: [cyan]{start_path}[/cyan]")

        try:
            # 2. The Divine Summons (Lazy Import)
            # We import here to avoid heavy TUI dependencies during CLI startup.
            from ..studio.app import GnosticShell

            # 3. The Rite of Interface
            app = GnosticShell(start_path=start_path)
            app.run()

            return self.success("The Architect has returned from the Sanctum.")

        except ImportError as e:
            if "textual" in str(e).lower():
                raise ArtisanHeresy(
                    "The Studio requires the 'textual' artisan.",
                    suggestion="Speak the plea: `pip install textual`"
                ) from e
            raise e
        except Exception as e:
            raise ArtisanHeresy(f"The Studio shattered: {e}", child_heresy=e) from e