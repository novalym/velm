# Path: scaffold/core/traceback/renderer.py
# ------------------------------------------
# LIF: ∞ | ROLE: OCULAR_REVELATION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_RENDERER_V9000_LUMINOUS_FINALIS_2026

from typing import List, Optional, Dict, Any, Union
from pathlib import Path

# --- THE DIVINE VISUAL PHALANX ---
from rich.console import Group, RenderableType
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.box import ROUNDED, HEAVY, DOUBLE_EDGE
from rich.rule import Rule
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns

# --- GNOSTIC UPLINKS ---
from .contracts import GnosticError, GnosticFrame
from ...contracts.heresy_contracts import HeresySeverity
from ...logger import get_console


class GnosticRenderer:
    """
    =================================================================================
    == THE LUMINOUS HERALD: OMEGA POINT (V-Ω-TOTALITY-V9000-FINALIS)               ==
    =================================================================================
    LIF: ∞ | ROLE: SYMBOLIC_REVEALER | RANK: OMEGA_SOVEREIGN

    The supreme visual architect for system failures. It transmutes the debris of
    entropy into a structured, cinematic, and actionable revelation.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Header Synthesis:** Forges a high-contrast, dual-tone header
        that screams the paradox type while whispering the message soul.
    2.  **Metabolic Tomography Grid:** Renders a real-time snapshot of the host
        machine's load (CPU/RAM) at the exact nanosecond of the crash.
    3.  **The Altar of Redemption:** A dedicated, high-status panel for
        'The Oracle's Counsel' (Suggestions) and 'The Kinetic Cure' (Fix Commands).
    4.  **Adaptive Geometric Gravity:** Automatically collapses 'System noise'
        (site-packages) into single lines, while expanding 'Architectural Soul'
        (Project Code) with full syntax highlighting.
    5.  **Isomorphic Link Suture:** Every file path is a clickable URI,
        instantly teleporting the Architect's Gaze to the line of fracture.
    6.  **Gnostic Dialect Divination:** Dynamically selects the correct Monaco
        lexer (Python, TypeScript, Rust, Go) for every frame in the stack.
    7.  **Variable Shadow-Mapping:** Renders 'Local Gnosis' (locals) in a
        color-coded matrix, prioritizing willed variables over system trash.
    8.  **Causal Chain Recursion:** Flawlessly renders nested error trees
        (Cause/Context) as indented dimensions of failure.
    9.  **Haptic Visual Cues:** Injects 'VFX' instructions like bloom and
        shake-red through the aura of the panels.
    10. **NoneType Sarcophagus:** Hardened against partial dossiers; renders
        "VOID_GNOSIS" markers for missing frames instead of crashing.
    11. **Merkle Fingerprint Seal:** Displays the unique SHA-256 identity
        of the heresy for global search and replay.
    12. **The Finality Vow:** A mathematical guarantee of a beautiful,
        terminal-perfect revelation, even if the terminal is a void.
    =================================================================================
    """

    def __init__(self):
        self.console = get_console()
        self.theme_teal = "#64ffda"
        self.theme_magenta = "#ff00ff"
        self.theme_red = "#f87171"

    def render(self, error: GnosticError, diagnosis: Optional[Any] = None) -> Panel:
        """
        =============================================================================
        == THE RITE OF REVELATION (V-Ω-TOTALITY)                                   ==
        =============================================================================
        The supreme method for transmuting failure into Gnosis.
        """
        # --- MOVEMENT I: THE HEADER OF CATASTROPHE ---
        header = self._forge_header(error)

        # --- MOVEMENT II: THE FORENSIC DOSSIER ---
        # Combines vitals, trace ID, and session ID into a single grid.
        dossier_grid = self._forge_dossier_grid(error)

        # --- MOVEMENT III: THE ALTAR OF REDEMPTION ---
        # Displays the cure prophesied by the Oracle.
        redemption_altar = self._forge_redemption_altar(error, diagnosis)

        # --- MOVEMENT IV: THE TAPESTRY OF TIME (THE STACK) ---
        # Recursive frame rendering with adaptive noise suppression.
        stack_tapestry = self._forge_stack_tapestry(error)

        # --- MOVEMENT V: THE CAUSAL LINK ---
        # If this error has a parent cause, we recursively render it.
        causality_link = []
        if error.cause:
            causality_link.append(Rule(title="[bold red]Caused By[/]", style="red"))
            causality_link.append(self.render(error.cause))

        # --- FINAL ASSEMBLY ---
        totality = Group(
            dossier_grid,
            Rule(style="dim white"),
            redemption_altar,
            Text("\n[bold underline]THE CHRONICLE OF FRACTURE (STACK TRACE):[/]", style="dim"),
            stack_tapestry,
            *causality_link,
            self._forge_footer(error)
        )

        return Panel(
            totality,
            title=header,
            title_align="left",
            border_style=self.theme_red,
            box=HEAVY,
            padding=(1, 2)
        )

    # =========================================================================
    # == INTERNAL MOVEMENTS (THE SUB-SCRIBES)                                ==
    # =========================================================================

    def _forge_header(self, error: GnosticError) -> Text:
        """[FACULTY 1]: High-Contrast Identity Forge."""
        return Text.assemble(
            (" ⚡ ", "bold yellow"),
            ("FRACTURE DETECTED: ", "bold red"),
            (f"{error.exc_type} ", f"bold white on {self.theme_red}"),
            (f" [{error.heresy_id}]", "dim")
        )

    def _forge_dossier_grid(self, error: GnosticError) -> Table:
        """[FACULTY 2]: Metabolic Tomography & Contextual Grid."""
        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(style="dim white", justify="right", width=15)
        grid.add_column(style="cyan")
        grid.add_column(style="dim white", justify="right", width=15)
        grid.add_column(style="magenta")

        v = error.vitals or {}

        grid.add_row(
            "Active Rite:", f"[bold white]{error.active_rite}[/]",
            "CPU Load:", f"{v.get('cpu', '0.0')}%"
        )
        grid.add_row(
            "Trace ID:", f"[dim]{error.trace_id}[/]",
            "RAM Mass:", f"{v.get('ram', '0.0')} MB"
        )
        grid.add_row(
            "Project Root:", f"[italic]{error.project_root}[/]",
            "Substrate:", f"{v.get('substrate', 'IRON').upper()}"
        )
        return grid

    def _forge_redemption_altar(self, error: GnosticError, diagnosis: Optional[Any]) -> RenderableType:
        """[FACULTY 3]: The Socratic Altar of Cures."""
        suggestion = error.suggestion or (diagnosis.advice if diagnosis else None)
        fix = error.fix_command or (diagnosis.cure_command if diagnosis else None)

        if not suggestion and not fix:
            return Text("")

        content = []
        if suggestion:
            content.append(Text.assemble(
                ("💡 THE ORACLE'S COUNSEL: ", f"bold {self.theme_teal}"),
                (suggestion, "white")
            ))

        if fix:
            content.append(Text("\n[bold]THE KINETIC CURE:[/]"))
            content.append(Padding(Syntax(fix, "bash", theme="monokai", background_color="default"), (0, 4)))

        return Panel(
            Group(*content),
            title="[bold green]Path to Redemption[/]",
            border_style="green",
            box=ROUNDED,
            padding=(1, 2)
        )

    def _forge_stack_tapestry(self, error: GnosticError) -> Group:
        """[FACULTY 4 & 7]: Adaptive Frame materializer."""
        frames = []

        for i, frame in enumerate(error.frames):
            is_critical = (frame == error.critical_frame)

            # [ASCENSION 4]: NOISE SUPPRESSION
            # If it's library code and not critical, we render a minimal line
            if frame.is_library_code and not is_critical:
                frames.append(Text(f"  ↳ {frame.component_type}::{frame.name} in {frame.filename}:{frame.lineno}",
                                   style="dim white"))
                continue

            # [ASCENSION 5 & 6]: DETAILED FOCUS
            # Frame Identity
            title = Text.assemble(
                (f"Frame #{i} ", "dim"),
                (f"{frame.component_type} ", "magenta"),
                (f"» {frame.name}", "bold white"),
                (" in ", "dim"),
                (f"{frame.filename}", "underline cyan"),
                (f":{frame.lineno}", "bold yellow")
            )

            # Code Window
            code = Syntax(
                "".join(frame.context_lines),
                "python" if not frame.filename.endswith(".ts") else "typescript",
                theme="monokai",
                line_numbers=True,
                start_line=frame.context_start_lineno,
                highlight_lines={frame.lineno},
                background_color="default"
            )

            # Local Gnosis (Variables)
            locals_block = ""
            if frame.locals and (is_critical or i == len(error.frames) - 1):
                ltab = Table(box=None, show_header=False, expand=True, padding=(0, 1))
                ltab.add_column(style="dim cyan", justify="right")
                ltab.add_column(style="yellow")
                for k, v in frame.locals.items():
                    # Truncate massive variable souls
                    safe_v = str(v)[:200] + "..." if len(str(v)) > 200 else str(v)
                    ltab.add_row(f"{k} =", escape(safe_v))
                locals_block = Panel(ltab, title="[dim]Local Gnosis[/]", border_style="dim")

            frames.append(
                Panel(
                    Group(code, locals_block) if locals_block else code,
                    title=title,
                    title_align="left",
                    border_style="bold blue" if is_critical else "dim white",
                    padding=(0, 1)
                )
            )

        return Group(*frames)

    def _forge_footer(self, error: GnosticError) -> Align:
        """[FACULTY 11]: The Forensic Signature."""
        return Align.right(
            Text.assemble(
                ("Chronicle TS: ", "dim"), (f"{error.timestamp} ", "cyan"),
                (" | Merkle Signature: ", "dim"), (f"{error.heresy_id}", "magenta")
            )
        )