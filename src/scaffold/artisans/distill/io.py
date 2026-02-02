# Path: scaffold/artisans/distill/io.py
# -------------------------------------

import difflib
from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.syntax import Syntax

# Adjusted imports relative to: scaffold/artisans/distill/io.py
from ...utils import atomic_write
from ...logger import Scribe, get_console
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("DistillIO")

try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class IOHandler:
    """
    =============================================================================
    == THE SCRIBE OF OUTPUT (V-Ω-LUMINOUS-IO)                                  ==
    =============================================================================
    Handles the physical manifestation of the Distillation Rite.
    It manages the Disk, the Screen, and the Clipboard.
    """

    @staticmethod
    def proclaim_diff(output_path: Path, new_content: str):
        """
        [FACULTY 9] The Luminous Diff.
        Shows the Architect exactly how reality will shift if they proceed.
        """
        if not output_path.exists():
            return

        Logger.info("Performing a Gaze of Comparison...")

        try:
            old_content = output_path.read_text(encoding='utf-8')

            diff_lines = list(difflib.unified_diff(
                old_content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=f"a/{output_path.name} (Current)",
                tofile=f"b/{output_path.name} (Prophecy)"
            ))

            diff_text = "".join(diff_lines)

            if diff_text:
                get_console().print(Panel(
                    Syntax(diff_text, "diff", theme="monokai"),
                    title="[yellow]Prophecy of Gnostic Drift[/yellow]",
                    border_style="yellow"
                ))
            else:
                Logger.success("No Gnostic Drift perceived. The scriptures are identical.")

        except Exception as e:
            Logger.warn(f"Could not compute diff for '{output_path.name}': {e}")

    @staticmethod
    def copy_to_clipboard(content: str):
        """
        [FACULTY 11] The Teleport.
        Sends the Gnosis directly to the system clipboard for immediate use.
        """
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(content)
                Logger.success("Gnostic Context copied to System Clipboard.")
            except Exception as e:
                Logger.warn(f"Clipboard access denied: {e}")
        else:
            Logger.warn("The 'pyperclip' artisan is missing. Install it to use --clipboard.")

    @staticmethod
    def inscribe(content: str, output_path: Optional[str], project_root: Path, force: bool) -> Optional[Path]:
        """
        [FACULTY 12] The Atomic Inscription.
        Writes the blueprint to disk using the Atomic Scribe to prevent corruption.
        """
        if not output_path:
            return None

        # Resolve path relative to project root if not absolute
        target = Path(output_path)
        if not target.is_absolute():
            target = project_root / target

        # We assume the caller (Artisan) has already handled overwrite confirmation prompts.
        # Here we just execute the write.
        res = atomic_write(target, content, Logger, sanctum=project_root, force=force)

        if not res.success:
            # We raise a heresy to halt the process if the write fails physically
            raise ArtisanHeresy(
                f"The final inscription rite failed for '{target.name}'.",
                details=res.message
            )

        return target