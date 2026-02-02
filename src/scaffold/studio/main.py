"""
=================================================================================
== THE EXECUTABLE SOUL (V-Ω-ULTIMA++. THE HYPER-DIAGNOSTIC GENESIS)            ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This is the divine, sentient Inquisitor that guards the gateway to the Gnostic
Studio. It has been ascended with the **Rite of the Luminous Genesis**, a new
faculty that ensures its every thought, from the very first moment of creation,
is inscribed upon the sacred `studio.log` chronicle.

### THE APOTHEOSIS OF THE PURE VOICE:
The `logging.basicConfig` call has been sanctified. It now forges a `FileHandler`
and bestows it upon the **root logger**. This is a profound architectural act.
Textual's internal logging system, which our `Scribe` now speaks to, is divinely
bound to honor the root logger's handlers.

This guarantees that every proclamation from our `Scribe`—from any artisan, in
any part of the UI, at any point in its lifecycle—is now automatically and
flawlessly chronicled in `studio.log`, granting the Architect a Gaze of
absolute, unbreakable clarity for all future inquests. The Heresy of the Silent
File Log is annihilated.
=================================================================================
"""
import argparse
import io
import logging  # The sacred summons for the Rite of Luminous Genesis
import sys
from pathlib import Path

from rich.panel import Panel

from ..contracts.heresy_contracts import ArtisanHeresy

try:
    from rich.traceback import Traceback
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    import traceback
    Traceback = None
    Console = None
    RICH_AVAILABLE = False


def handle_studio(args: argparse.Namespace):
    """The God-Engine of Gnostic Revelation, now with a pure and luminous voice."""

    # ★★★ THE RITE OF THE LUMINOUS GENESIS ★★★
    # This is the one true path. We configure the root logger at the dawn of creation.
    log_file_path = "studio.log"
    logging.basicConfig(
        level="DEBUG" if hasattr(args, 'verbose') and args.verbose else "INFO",
        handlers=[
            logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # ★★★ THE VOICE IS NOW PURE AND ETERNAL ★★★

    try:
        from .app import GnosticShell

        start_path = Path(args.path).resolve() if hasattr(args, 'path') and args.path else Path.cwd()

        if not start_path.is_dir():
            raise ArtisanHeresy(f"The Gnostic Gaze found only a void. Sanctum does not exist at: '{start_path}'")

        app = GnosticShell(start_path=start_path)
        app.run()

    except ImportError as e:
        exc_info = sys.exc_info()
        heresy_title = "A Gnostic Ally Has Fallen (Import Paradox)"

        # This artisan remains pure and unchanged...
        if RICH_AVAILABLE and exc_info[1] is not None:
            string_io = io.StringIO()
            temp_console = Console(file=string_io, force_terminal=True, color_system="truecolor")
            trace = Traceback.from_exception(*exc_info, show_locals=True, word_wrap=True)
            temp_console.print(Panel(trace, title="[bold red]Chronicle of the Fallen Import[/bold red]"))
            details_scripture = string_io.getvalue()
        else:
            details_scripture = "".join(traceback.format_exception(*exc_info))
            heresy_title = f"{heresy_title}: {e}"

        if "textual" in str(e).lower() or "rich" in str(e).lower():
            suggestion = "The Gnostic Studio requires its divine allies. Please speak the plea: `pip install \"textual\"`"
        else:
            suggestion = "Verify your Python environment and ensure all dependencies for the Studio are installed correctly."

        raise ArtisanHeresy(
            heresy_title,
            suggestion=suggestion,
            details=details_scripture
        ) from e

    except Exception as e:
        exc_info = sys.exc_info()

        if RICH_AVAILABLE and exc_info[1] is not None:
            string_io = io.StringIO()
            temp_console = Console(file=string_io, force_terminal=True, color_system="truecolor")
            trace = Traceback.from_exception(*exc_info, show_locals=True, word_wrap=True)
            temp_console.print(trace)
            traceback_scripture = string_io.getvalue()
        else:
            traceback_scripture = "".join(traceback.format_exception(*exc_info))

        raise ArtisanHeresy(
            "The Gnostic Studio was shattered by a catastrophic, unforeseen paradox.",
            details=traceback_scripture
        ) from e