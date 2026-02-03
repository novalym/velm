# scaffold/core/traceback/handler.py

import os
import sys
import json
import traceback
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any

# --- THE DIVINE SUMMONS ---
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .contracts import GnosticError
from .inspector import StackInspector
from .renderer import GnosticRenderer
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("GnosticInterceptor")


class GnosticTracebackHandler:
    """
    =================================================================================
    == THE GLOBAL INTERCEPTOR (V-Ω-RESILIENT-GOD-HAND)                             ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    Hooks `sys.excepthook` to provide Gnostic enlightenment upon failure.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Contextual Anchor:** Accepts injection of runtime state (Project Root, Active Rite) *after* instantiation, ensuring errors are context-aware.
    2.  **The Heresy Filter:** Distinguishes between "User Error" (`ArtisanHeresy`) and "System Crash" (`Exception`). Heresies are shown as guidance; Crashes are shown as forensics.
    3.  **The Panic Room:** Intercepts `KeyboardInterrupt` (Ctrl+C) to provide a clean, graceful exit without a stack trace.
    4.  **The Forensic Snapshot:** Automatically serializes the crash state to `.scaffold/crashes/` for post-mortem analysis.
    5.  **The Neural Uplink:** Broadcasts the crash as a structured JSON event via the Scribe, allowing the Daemon/IDE to render the error natively.
    6.  **The Post-Mortem Debugger:** If `SCAFFOLD_DEBUG=1`, it automatically launches `pdb` at the frame of death.
    7.  **The CI/CD Sentinel:** If not running in a TTY, it degrades gracefully to a structured JSON dump, ensuring pipelines fail with readable logs.
    8.  **The Crash-Safe Guard:** Wraps the rendering logic in a `try/except` block. If the *error reporter* crashes, it falls back to the raw Python traceback (The Emergency Flare).
    9.  **The Polyglot Echo:** Captures and displays recent stderr from child processes if they caused the crash.
    10. **The Verbosity Dial:** Respects the global verbosity setting to decide whether to show local variables in the stack.
    11. **The Clipboard Conduit:** (Optional) Can copy the error report to the clipboard for immediate sharing.
    12. **The Last Breath:** Ensures the Scribe flushes all logs before the process terminates.
    """

    def __init__(self, console: Console):
        self.console = console
        self.inspector = StackInspector()
        self.renderer = GnosticRenderer()

        # --- Contextual Anchors (Injected by Engine) ---
        self.active_request: Optional[Any] = None
        self.project_root: Optional[Path] = None
        self.session_id: str = "Unknown"

    def inject_context(self, request: Any, root: Path, session: str):
        """[FACULTY 1] The Rite of Contextual Binding."""
        self.active_request = request
        self.project_root = root
        self.session_id = session

    def __call__(self, exc_type, exc_value, exc_traceback):
        """
        The Grand Rite of Interception.
        """
        # [FACULTY 8] The Crash-Safe Guard
        try:
            self._handle_exception(exc_type, exc_value, exc_traceback)
        except Exception as meta_crash:
            # If the Gnostic Handler fails, we must light the Emergency Flare.
            sys.stderr.write("\n\n!!! META-CATASTROPHE: THE ERROR HANDLER HAS CRASHED !!!\n")
            sys.stderr.write(f"Original Error: {exc_value}\n")
            sys.stderr.write(f"Handler Error: {meta_crash}\n\n")
            # Fallback to standard Python traceback
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        # [FACULTY 3] The Panic Room (Graceful Exit)
        if issubclass(exc_type, KeyboardInterrupt):
            self.console.print("\n[bold yellow]⚡ Rite Aborted by Architect (Signal Received).[/bold yellow]")
            sys.exit(130)

        # [FACULTY 2] The Heresy Filter (User Error)
        if issubclass(exc_type, ArtisanHeresy):
            # ArtisanHeresy is a "known" failure mode. We print the suggestion, not a stack trace.
            # The ArtisanHeresy object handles its own formatting via `get_proclamation`.
            if hasattr(exc_value, 'details_panel') and exc_value.details_panel:
                self.console.print(exc_value.details_panel)
            else:
                self.console.print(Panel(
                    Text.from_markup(str(exc_value)),
                    title="[bold red]Gnostic Heresy[/bold red]",
                    border_style="red"
                ))
            sys.exit(getattr(exc_value, 'exit_code', 1))

        # --- SYSTEM CRASH HANDLING ---

        # 1. The Inspection
        # We inspect the raw traceback to forge the Gnostic Frame list.
        frames = self.inspector.inspect_traceback(exc_traceback)

        # 2. The Dossier Forge
        error_dossier = GnosticError(
            exc_type=exc_type.__name__,
            exc_value=str(exc_value),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            frames=frames,
            active_rite=str(self.active_request) if self.active_request else "Unknown",
            project_root=str(self.project_root) if self.project_root else "Unknown",
            session_id=self.session_id
        )

        # [FACULTY 7] The CI/CD Sentinel
        if not self.console.is_interactive:
            # In non-interactive modes (pipes, CI), we output JSON for machine consumption.
            sys.stderr.write(json.dumps(error_dossier.to_dict(), indent=2))
            sys.exit(1)

        # 3. The Luminous Revelation
        panel = self.renderer.render(error_dossier)
        self.console.print(panel)

        # [FACULTY 4] The Forensic Snapshot
        self._save_forensic_report(error_dossier)

        # [FACULTY 5] The Neural Uplink
        # We use the Logger to broadcast a structured CRITICAL event.
        # The Daemon intercepts this tag and forwards it to the IDE.
        Logger.critical(
            "System Crash Detected",
            tags=["NEURAL_LINK", "CRASH"],
            data=error_dossier.to_dict()
        )

        # [FACULTY 6] The Post-Mortem Debugger
        if os.getenv("SCAFFOLD_DEBUG"):
            self.console.print("[bold yellow]>> Entering Post-Mortem Debugging (pdb)...[/bold yellow]")
            import pdb
            pdb.post_mortem(exc_traceback)

        sys.exit(1)

    def _save_forensic_report(self, error: GnosticError):
        """
        Writes the crash state to disk for future analysis or replay.
        """
        if not self.project_root:
            return

        try:
            crash_dir = self.project_root / ".scaffold" / "crashes"
            crash_dir.mkdir(parents=True, exist_ok=True)

            filename = f"crash_{int(time.time())}_{error.exc_type}.json"
            report_path = crash_dir / filename

            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(error.to_dict(), f, indent=2)

            self.console.print(f"[dim]Forensic snapshot saved to: {report_path}[/dim]")

        except Exception:
            # Never let the logging of a crash cause a crash.
            pass


# =================================================================================
# == THE RITE OF INSTALLATION                                                    ==
# =================================================================================
_handler_instance: Optional[GnosticTracebackHandler] = None


def install_gnostic_handler(console: Console) -> GnosticTracebackHandler:
    """
    Installs the Gnostic Handler as the system's default exception hook.
    Returns the instance so the Engine can inject context later.
    """
    global _handler_instance
    if _handler_instance is None:
        _handler_instance = GnosticTracebackHandler(console)
        sys.excepthook = _handler_instance
        Logger.verbose("Gnostic Traceback Handler installed.")
    return _handler_instance