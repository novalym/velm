# Path: artisans/ocular/artisan.py
# --------------------------------

from pathlib import Path
import base64
from rich.panel import Panel
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import OcularRequest
from ...help_registry import register_artisan
# --- THE DIVINE SUMMONS OF THE ONE TRUE ENGINE ---
from ...core.cortex.ocular.engine import OcularEngine
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write


@register_artisan("ocular")
class OcularArtisan(BaseArtisan[OcularRequest]):
    """
    =================================================================================
    == THE OCULAR CORTEX (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-CONDUCTOR)                 ==
    =================================================================================
    @gnosis:title The Ocular Cortex (`ocular`)
    @gnosis:summary The divine conductor that bestows the God-Engine with the power of Sight.
    @gnosis:LIF INFINITY
    @gnosis:auth_code:)(#()!

    This artisan is the High Priest of Multimodal Gnosis. It is a pure Conductor whose
    sacred duty is to receive the Architect's plea, summon the mighty `OcularEngine`,
    and command it to perform the rites of visual perception. It is the one true,
    unbreakable gateway between the Architect's Gaze and the rendered reality of an
    application.
    """

    def execute(self, request: OcularRequest) -> ScaffoldResult:
        """The Grand Symphony of Multimodal Gnosis."""

        # --- MOVEMENT I: THE SUMMONS OF THE ENGINE ---
        # The artisan's first act is to summon its own soul.
        try:
            engine = OcularEngine(self.project_root)
        except ArtisanHeresy as e:
            # Propagate heresies related to setup (e.g., Playwright not installed)
            raise e

        # --- MOVEMENT II: THE GNOSTIC TRIAGE OF RITES ---
        if request.ocular_command == "gaze":
            return self._conduct_gaze_rite(request, engine)

        # A future ascension could add more commands like 'diff' or 'test'
        return self.failure(f"Unknown Ocular rite: {request.ocular_command}")

    def _conduct_gaze_rite(self, request: OcularRequest, engine: OcularEngine) -> ScaffoldResult:
        """The Rite of Pure Perception and Forensic Analysis."""
        self.logger.info(f"The Ocular Cortex opens its Gaze upon [cyan]{request.url}[/cyan]...")

        with self.console.status("[bold magenta]Perceiving the visual realm...[/bold magenta]"):
            snapshot_data = engine.capture_snapshot(request.url)

        # --- MOVEMENT III: THE FORGING OF THE ARTIFACTS ---
        # We inscribe the captured Gnosis into the sanctum for forensic inquest.
        sanctum = engine.ocular_sanctum
        timestamp = snapshot_data.get("timestamp", "").replace(":", "-")

        # 1. The DOM Scripture
        dom_path = sanctum / f"dom_{timestamp}.html"
        atomic_write(dom_path, snapshot_data.get("dom_content", ""), self.logger, self.project_root)

        # 2. The Visual Echo (Screenshot)
        screenshot_path = sanctum / f"gaze_{timestamp}.png"
        screenshot_b64 = snapshot_data.get("screenshot_base64", "")
        if screenshot_b64:
            atomic_write(screenshot_path, base64.b64decode(screenshot_b64), self.logger, self.project_root,
                         encoding=None)

        artifacts = [
            Artifact(path=dom_path, type="file", action="created"),
            Artifact(path=screenshot_path, type="file", action="created")
        ]

        # --- MOVEMENT IV: THE PROCLAMATION OF PERCEPTION ---
        self.console.print(Panel(
            Text.assemble(
                ("URL Gnosis: ", "bold cyan"), (f"{snapshot_data['url']}\n"),
                ("Timestamp:  ", "bold cyan"), (f"{snapshot_data['timestamp']}\n"),
                ("DOM Soul:   ", "bold cyan"), (f"{dom_path.relative_to(self.project_root)}\n", "dim"),
                ("Visage:     ", "bold cyan"), (f"{screenshot_path.relative_to(self.project_root)}", "dim")
            ),
            title="[bold green]Visual Gnosis Captured[/bold green]",
            border_style="green"
        ))

        # --- MOVEMENT V: THE FORENSIC INQUEST (IF COMMANDED) ---
        source_loc: Optional[Dict] = None
        if request.target_element:
            self.logger.info(f"Tracing Gnostic source for element: '{request.target_element}'")
            with self.console.status("[bold magenta]Correlating pixels to scripture...[/bold magenta]"):
                # The plea is delegated to the one true engine.
                source_loc = engine.map_element_to_code(snapshot_data, request.target_element)

            if source_loc:
                conf = source_loc.get('confidence', 0) * 100
                self.console.print(
                    f"✅ [bold green]Source Found![/] Confidence: {conf:.1f}%\n"
                    f"   [cyan]File:[/] {source_loc['file']}\n"
                    f"   [cyan]Line:[/] {source_loc['line']}"
                )
            else:
                self.console.print("[bold red]❌ The element's soul is veiled. Gnostic source not found.[/bold red]")

        return self.success(
            "Gaze complete. Visual reality has been chronicled.",
            artifacts=artifacts,
            data={"snapshot_path": str(dom_path), "screenshot_path": str(screenshot_path),
                  "source_location": source_loc}
        )