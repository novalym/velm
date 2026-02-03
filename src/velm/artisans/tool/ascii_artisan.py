# Path: scaffold/artisans/tool/ascii_artisan.py
# ---------------------------------------------

import sys
from pathlib import Path
from typing import Tuple, List

from ...core.artisan import BaseArtisan
from ...interfaces.requests import AsciiRequest
from ...interfaces.base import ScaffoldResult
from ...contracts.heresy_contracts import ArtisanHeresy
from ...help_registry import register_artisan
from ...utils import atomic_write

# --- THE DIVINE SUMMONS (WITH GRACEFUL DEGRADATION) ---
try:
    from PIL import Image, ImageEnhance

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    from rich.text import Text
    from rich.syntax import Syntax
    from rich.panel import Panel
    from rich.prompt import Prompt

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import pyperclip

    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


@register_artisan("ascii")
class AsciiArtisan(BaseArtisan[AsciiRequest]):
    """
    =================================================================================
    == THE SIGIL FORGER (V-Ω-ULTRA-DEFINITIVE-INTEGRATED)                          ==
    =================================================================================
    @gnosis:title The Sigil Forger (`tool ascii`)
    @gnosis:summary Transmutes a raster image into a luminous, colored ASCII scripture,
                     ready for direct integration into your codebase.
    @gnosis:LIF 10,000,000,000,000
    """

    CHARSET_MAP = {
        "detailed": "@%#*+=-:. ",
        "simple": "@#=-. ",
        "block": "█▇▆▅▄▃▂  ",
        "double": "▀▄"  # Special case
    }

    def execute(self, request: AsciiRequest) -> ScaffoldResult:
        self._check_dependencies(request)

        # [ASCENSION 10] The Interactive Plea
        image_path = request.image_path
        if not image_path:
            path_str = Prompt.ask("[bold cyan]Enter the path to the image scripture[/bold cyan]")
            image_path = Path(path_str)

        image_path = image_path.resolve()
        if not image_path.exists():
            return self.failure(f"The source image is a void: {image_path}")

        self.logger.info(f"The Sigil Forger awakens its Gaze upon: [cyan]{image_path.name}[/cyan]")

        try:
            with Image.open(image_path) as img:
                # --- MOVEMENT I: THE GAZE & ALCHEMICAL ENHANCEMENT ---
                # [ASCENSION 5] The Contrast Enhancer
                if request.contrast:
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(request.contrast)

                # [ASCENSION 4] The Palette Quantizer
                if request.colors:
                    img = img.quantize(colors=request.colors, method=Image.MAXCOVERAGE)
                    img = img.convert("RGB")  # Re-convert to RGB after quantization

                aspect_ratio = img.height / img.width if img.width > 0 else 1
                new_height = int(aspect_ratio * request.width * 0.55)

                # [ASCENSION 8] The Unbreakable Ward of The Void
                if request.width <= 0 or new_height <= 0:
                    raise ArtisanHeresy("Image dimensions result in a void. Please provide a larger width.")

                resized_img = img.resize((request.width, new_height))
                grayscale_img = resized_img.convert("L")

                # --- MOVEMENT II: THE TRANSMUTATION ---
                segments = self._transmute_image_to_segments(resized_img, grayscale_img, request)

                # --- MOVEMENT III: THE SCRIPTURE FORGE ---
                output_scripture = self._forge_output_scripture(segments, request)

                # --- MOVEMENT IV: THE FINAL PROCLAMATION ---
                self._proclaim_output(output_scripture, request)

                return self.success("The image's soul has been transmuted into Gnostic scripture.")

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy("A paradox occurred during the Rite of Transmutation.", child_heresy=e)

    def _check_dependencies(self, request: AsciiRequest):
        if not PILLOW_AVAILABLE:
            raise ArtisanHeresy("The Sigil Forger requires 'Pillow'.", suggestion="Speak: `pip install Pillow`")
        if not RICH_AVAILABLE:
            raise ArtisanHeresy("The Sigil Forger requires 'rich'.", suggestion="Speak: `pip install rich`")
        if request.clipboard and not PYPERCLIP_AVAILABLE:
            raise ArtisanHeresy("The Clipboard Conduit requires 'pyperclip'.",
                                suggestion="Speak: `pip install pyperclip`")

    def _transmute_image_to_segments(self, color_img, gray_img, request: AsciiRequest) -> List[Tuple[str, str]]:
        segments = []
        char_ramp = self.CHARSET_MAP.get(request.charset, self.CHARSET_MAP["detailed"])

        # [ASCENSION 7] The Dual-Block Renderer
        if request.charset == 'double':
            for y in range(0, gray_img.height - 1, 2):
                for x in range(gray_img.width):
                    # Top pixel
                    r1, g1, b1, *_ = color_img.getpixel((x, y))
                    # Bottom pixel
                    r2, g2, b2, *_ = color_img.getpixel((x, y + 1))
                    # We use the top half block char, with foreground as bottom color and background as top color
                    # Rich text handles this beautifully.
                    style = f"rgb({r2},{g2},{b2}) on rgb({r1},{g1},{b1})"
                    segments.append(("▄", style))
                segments.append(("\n", "default"))
            return segments

        # Standard character ramp logic
        for y in range(gray_img.height):
            for x in range(gray_img.width):
                luminosity = gray_img.getpixel((x, y))
                if request.invert: luminosity = 255 - luminosity

                char_index = int((luminosity / 255) * (len(char_ramp) - 1))
                char = char_ramp[len(char_ramp) - 1 - char_index]

                style = "default"
                if request.style == "color":
                    r, g, b, *_ = color_img.getpixel((x, y))
                    style = f"rgb({r},{g},{b})"

                segments.append((char, style))
            segments.append(("\n", "default"))
        return segments

    def _forge_output_scripture(self, segments: List[Tuple[str, str]], request: AsciiRequest) -> str:
        if request.lang == "raw":
            return "".join([char for char, style in segments])

        # [ASCENSION 11] THE GNOSTIC SCRIBE (`repr()`)
        # This is the CORE FIX. `repr(char)` correctly escapes newlines and other special characters.
        segments_repr = ",\n".join([f'    ({repr(char)}, "{style}")' for char, style in segments])

        # [ASCENSION 2 & 3] The Variable Alchemist & Quantum Simplifier
        if request.no_function:
            return f"""
# Auto-forged by the Scaffold Sigil Forger
{request.var_name} = [
{segments_repr}
]
"""

        if request.lang == "js":
            return f"""
// Auto-forged by the Scaffold Sigil Forger
export const {request.var_name} = () => {{
    const segments = [
{segments_repr.replace('(', '[').replace(')', ']')}
    ];
    // This requires a helper function to render segments with ANSI codes.
    return segments.map(([char, style]) => char).join(''); 
}};
"""
        # Default to Python
        else:
            return f"""
from rich.text import Text

# This scripture was auto-forged by the 'scaffold tool ascii' artisan.
def {request.var_name}() -> Text:
    \"\"\"Proclaims the sacred Sigil of the project.\"\"\"

    segments = [
{segments_repr}
    ]

    return Text.assemble(*segments)
"""

    def _proclaim_output(self, scripture: str, request: AsciiRequest):
        if request.clipboard:
            pyperclip.copy(scripture)
            self.logger.success("The Gnostic scripture has been inscribed into the ephemeral realm (clipboard).")
            return

        if request.append_to:
            target_path = request.append_to.resolve()
            if not target_path.exists():
                raise ArtisanHeresy(f"Cannot perform Alchemical Graft: '{target_path}' is a void.")

            content = target_path.read_text(encoding='utf-8')
            if request.marker not in content:
                raise ArtisanHeresy(
                    f"Cannot perform Alchemical Graft: Marker '{request.marker}' not found in '{target_path.name}'.")

            import re
            marker_regex = re.escape(request.marker)
            new_content = re.sub(marker_regex, scripture.strip(), content, count=1)

            atomic_write(target_path, new_content, self.logger, self.project_root)
            self.logger.success(f"Successfully performed Alchemical Graft upon [cyan]{target_path.name}[/cyan].")
            return

        if request.output:
            target_path = request.output.resolve()
            atomic_write(target_path, scripture, self.logger, self.project_root)
            self.logger.success(f"The Gnostic scripture has been inscribed at [cyan]{target_path}[/cyan].")
            return

        self.console.print(Panel(
            Syntax(scripture.strip(), request.lang, theme="monokai", line_numbers=True),
            title="[bold green]The Transmuted Scripture[/bold green]",
            subtitle="[dim]Inscribe this Gnosis into your project's soul.[/dim]",
            border_style="green"
        ))