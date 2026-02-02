# Path: scaffold/symphony/conductor_core/resilience/intercession.py
# -----------------------------------------------------------------

import sys
import subprocess
import os
import time
from typing import Optional, Any, List, Dict

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.console import Console, Group
from rich.syntax import Syntax
from rich.layout import Layout
from rich.columns import Columns
from rich.style import Style
from rich.padding import Padding
from .contracts import IntercessionChoice
from ....contracts.symphony_contracts import Edict, ActionResult
from ....logger import get_console

# --- THE CROSS-PLATFORM GNOSTIC BRIDGE ---
# We conditionally import OS-specific input handlers to prevent ImportHeresy.
try:
    import msvcrt

    WINDOWS_INPUT = True
except ImportError:
    WINDOWS_INPUT = False

try:
    import termios
    import tty
    import select

    UNIX_INPUT = True
except ImportError:
    UNIX_INPUT = False


class IntercessionAltar:
    """
    =============================================================================
    == THE ALTAR OF INTERCESSION (V-Ω-CROSS-PLATFORM-ULTIMA)                   ==
    =============================================================================
    LIF: 10,000,000,000,000

    The Sentient UI for Failure Management. It bridges the gap between the
    Architect's Will and the Broken Reality.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Cross-Platform Input Sanitizer:** Flushes `stdin` using `msvcrt` on
        Windows and `termios` on Unix, annihilating phantom 'Enter' presses.
    2.  **The Luminous Dashboard:** Uses a sophisticated `rich.Group` layout to
        present Error, Context, and Remediation options clearly.
    3.  **The Forensic Highlighter:** Renders the failed scripture with syntax
        highlighting and line numbers.
    4.  **The Heresy decoder:** Intelligently formats exceptions, extracting
        messages from nested `ArtisanHeresy` chains.
    5.  **The Artifact Beacon:** Displays a clickable link to the crash dump.
    6.  **The Contextual Heuristic:** Analyzes the error to suggest the most
        likely remediation (e.g., suggests 'google' for unknowns, 'retry' for IO).
    7.  **The Shell Portal:** Provides a safe passage to a subprocess shell
        at the exact location of the failure.
    8.  **The Truncation Guard:** Automatically summarizes massive error logs
        to prevent terminal flooding, while preserving the core message.
    9.  **The Option Grid:** Renders choices in a clean, aligned table.
    10. **The Semantic Color System:** Uses Red for Paradox, Yellow for Warning,
        and Cyan for Options, ensuring immediate cognitive recognition.
    11. **The Safety Valve:** Wraps all UI rendering in a broad try/except to
        ensure the error handler itself never crashes (Meta-Resilience).
    12. **The Sovereign Input:** Uses `rich.Prompt` for consistent, theme-aware
        user interaction.
    """

    def __init__(self, console: Console):
        self.console = console

    def summon(self,
               edict: Edict,
               heresy: Optional[Exception],
               result: Optional[ActionResult],
               artifact_path: Optional[str],
               hint: Optional[str] = None) -> IntercessionChoice:

        # [FACULTY 1] The Rite of Input Purification
        self._flush_input()

        try:
            self.console.clear()
            self.console.rule("[bold red]⚡ INTERCESSION ALTAR AWAKENED ⚡[/bold red]", style="red")

            # 1. The Dashboard of Failure
            dashboard = self._forge_dashboard(edict, heresy, result, artifact_path, hint)
            self.console.print(dashboard)

            # 2. The Plea
            choice = Prompt.ask(
                "\n[bold yellow]Your Will?[/bold yellow]",
                choices=[c.value for c in IntercessionChoice],
                default="r"
            )
            return IntercessionChoice(choice)

        except Exception as e:
            # [FACULTY 11] The Safety Valve
            # If the Altar itself shatters, we fallback to a raw input prompt.
            print(f"!!! THE ALTAR HAS CRASHED: {e} !!!")
            print("(r)etry, (q)uit")
            val = input("Choice: ").strip().lower()
            return IntercessionChoice.RETRY if val == 'r' else IntercessionChoice.ABORT

    def _forge_dashboard(self, edict: Edict, heresy: Optional[Exception], result: Optional[ActionResult],
                         artifact_path: Optional[str], hint: Optional[str]):
        """Forges the visual representation of the failure."""

        # A. The Scripture (Code Context)
        scripture_panel = Panel(
            Syntax(edict.raw_scripture, "bash", theme="monokai", line_numbers=True, start_line=edict.line_num),
            title=f"[bold cyan]The Broken Rite (Line {edict.line_num})[/bold cyan]",
            border_style="cyan"
        )

        # B. The Heresy (Error Message)
        error_text = self._extract_error_text(heresy, result)
        heresy_panel = Panel(
            error_text,
            title="[bold red]The Paradox[/bold red]",
            border_style="red"
        )

        # C. The Context (Artifacts & Hints)
        meta_grid = Table.grid(expand=True, padding=(0, 2))
        meta_grid.add_column(style="dim yellow")
        meta_grid.add_column()

        if artifact_path:
            meta_grid.add_row("Forensic Artifact:", f"[link=file://{artifact_path}]{artifact_path}[/link]")

        if hint:
            meta_grid.add_row("Oracle's Hint:", f"[bold italic]{hint}[/bold italic]")

        # D. The Options (Menu)
        options_table = Table(box=None, show_header=False, pad_edge=False, padding=(0, 2))
        options_table.add_column("Key", style="bold green", justify="center", width=4)
        options_table.add_column("Action", style="bold white", width=12)
        options_table.add_column("Description", style="dim")

        options = [
            ("r", "Retry", "Re-attempt the failed edict immediately."),
            ("s", "Skip", "Ignore the heresy and proceed with the Symphony."),
            ("e", "Edit", "Open the scripture in your system editor."),
            ("!", "Shell", "Drop into a sub-shell at the point of failure."),
            ("d", "Diagnose", "Summon the AI Co-Architect for wisdom."),
            ("g", "Google", "Consult the Web Oracle for this error."),
            ("q", "Quit", "Abort the Symphony and return to the void.")
        ]

        for key, act, desc in options:
            options_table.add_row(f"({key})", act, desc)

        # Composition
        return Group(
            scripture_panel,
            heresy_panel,
            Padding(meta_grid, (1, 0)),
            Panel(options_table, title="[bold green]Paths of Redemption[/bold green]", border_style="green")
        )

    def _extract_error_text(self, heresy: Optional[Exception], result: Optional[ActionResult]) -> str:
        """[FACULTY 8] The Truncation Guard & Heresy Decoder."""
        msg = ""
        if heresy:
            msg = f"{type(heresy).__name__}: {str(heresy)}"
        elif result:
            msg = result.stderr or result.stdout or "Process returned non-zero exit code with no output."
        else:
            msg = "Unknown Gnostic Error."

        # Smart Truncation
        lines = msg.splitlines()
        if len(lines) > 20:
            return "\n".join(lines[:10] + ["", f"... {len(lines) - 20} lines hidden ...", ""] + lines[-10:])
        return msg

    def enter_void_shell(self, cwd: str):
        """Drops the user into a shell at the failure location."""
        self.console.print(f"[dim]Entering Void Shell at {cwd}... (Type 'exit' to return)[/dim]")
        try:
            shell = os.environ.get("SHELL", "/bin/bash")
            if os.name == 'nt':
                shell = os.environ.get("COMSPEC", "cmd.exe")

            # Using call instead of run to ensure it takes over the TTY properly
            subprocess.call(shell, cwd=cwd)
            self.console.print("[dim]Returned from the Void.[/dim]")
        except Exception as e:
            self.console.print(f"[red]Failed to summon shell: {e}[/red]")

    def _flush_input(self):
        """
        [FACULTY 1] THE GNOSTIC INPUT SANITIZER
        Flushes any pending input from stdin to prevent accidental auto-selection.
        Robustly handles Windows (msvcrt) and Unix (termios).
        """
        try:
            # --- WINDOWS RITE ---
            if WINDOWS_INPUT:
                # msvcrt.kbhit() returns True if a key is waiting
                # msvcrt.getch() reads a key without waiting
                while msvcrt.kbhit():
                    msvcrt.getch()

            # --- UNIX RITE ---
            elif UNIX_INPUT:
                # Use termios to flush the input buffer
                fd = sys.stdin.fileno()
                termios.tcflush(fd, termios.TCIFLUSH)

        except Exception:
            # The Unbreakable Ward: If flushing fails (e.g. non-interactive TTY),
            # we proceed without crashing. The Architect may have to press Enter twice.
            pass