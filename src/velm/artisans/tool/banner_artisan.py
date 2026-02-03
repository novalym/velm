# Path: scaffold/artisans/tool/banner_artisan.py
# ----------------------------------------------
from pathlib import Path
import sys

from ...core.artisan import BaseArtisan
from ...interfaces.requests import BannerRequest
from ...interfaces.base import ScaffoldResult, Artifact
from ...contracts.heresy_contracts import ArtisanHeresy
from ...help_registry import register_artisan
from ...utils import atomic_write

# Lazy load pyfiglet
try:
    import pyfiglet

    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False


@register_artisan("banner")
class BannerArtisan(BaseArtisan[BannerRequest]):
    """
    =================================================================================
    == THE HERALD OF FONTS (V-Ω-ASCII-FORGE)                                       ==
    =================================================================================
    @gnosis:title The Banner Forge (`tool banner`)
    @gnosis:summary Generates a beautiful ASCII banner for your project using Pyfiglet.
    @gnosis:description
    This artisan transmutes simple text into majestic ASCII art. It inscribes the
    result into `.scaffold/banner.txt`, which is automatically perceived by the
    CLI's bootloader to brand your project.
    """

    def execute(self, request: BannerRequest) -> ScaffoldResult:
        if not PYFIGLET_AVAILABLE:
            raise ArtisanHeresy(
                "The Banner Forge requires the 'pyfiglet' artisan.",
                suggestion="Speak the plea: `pip install pyfiglet`"
            )

        text = request.text or self.project_root.name.upper()
        font = request.font or "standard"

        self.logger.info(f"Forging banner for '[cyan]{text}[/cyan]' using font '[magenta]{font}[/magenta]'...")

        try:
            # 1. The Rite of Figlet
            ascii_art = pyfiglet.figlet_format(text, font=font)

            # 2. Determine Sanctum
            # Default to project root .scaffold/banner.txt
            if request.output_path:
                target_path = Path(request.output_path).resolve()
            else:
                target_path = self.project_root / ".scaffold" / "banner.txt"

            # 3. The Atomic Inscription
            target_path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(target_path, ascii_art, self.logger, self.project_root)

            # 4. Proclamation
            from rich.panel import Panel
            from rich.text import Text
            from rich.align import Align

            # We display the result to the Architect immediately
            preview = Text(ascii_art, style="bold cyan")
            self.console.print(Panel(
                Align.center(preview),
                title=f"[bold green]Banner Forged: {target_path.name}[/bold green]",
                border_style="green"
            ))

            return self.success(
                f"Banner inscribed to {target_path}",
                artifacts=[Artifact(path=target_path, type="file", action="created")]
            )

        except pyfiglet.FontNotFound:
            raise ArtisanHeresy(
                f"The font '{font}' is unknown to the Figlet archives.",
                suggestion="Try 'standard', 'slant', 'doom', or 'big'."
            )
        except Exception as e:
            raise ArtisanHeresy(f"The Banner Forge shattered: {e}", child_heresy=e)