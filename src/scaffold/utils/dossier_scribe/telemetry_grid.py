# Path: scaffold/utils/dossier_scribe/telemetry_grid.py
# -----------------------------------------------------

from __future__ import annotations
import math
import platform
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.console import Group

from ... import __version__ as scaffold_ver


class TelemetryScribe:
    """
    =================================================================================
    == THE SCRIBE OF TELEMETRY (V-Ω-HUD-FOCUSED-COMPATIBLE)                        ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan acts as a **High-Density HUD**, visualizing the invisible forces:
    Time, Entropy (Bytes), Identity (User/Git), and Cognition (AI Usage).
    """

    def __init__(
            self,
            telemetry_source: Any,
            gnosis: Dict,
            project_root: Path,
            # [COMPATIBILITY FIX] Explicitly accept positional args from DossierScribe
            transmutation_plan: Optional[Dict] = None,
            ai_telemetry: Optional[Dict] = None,
            environment_gnosis: Optional[Dict] = None,
            performance_metrics: Optional[Dict] = None,
            **kwargs
    ):
        self.regs = telemetry_source
        self.gnosis = gnosis
        self.root = project_root

        # Store context
        self.transmutation_plan = transmutation_plan or {}
        self.ai_stats = ai_telemetry or {}
        self.env_stats = environment_gnosis or {}
        self.perf_stats = performance_metrics or {}

    def forge(self) -> Panel:
        """The Grand Rite of Statistical Visualization."""

        # We build a grid of 3 main columns:
        # 1. KINETIC (Files, Bytes, Velocity)
        # 2. TEMPORAL & IDENTITY (Time, User, Git)
        # 3. COGNITIVE (AI usage, if any) or SYSTEM (OS/Python)

        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)

        # --- COLUMN 1: KINETIC (THE WORK DONE) ---
        kinetic_panel = self._forge_kinetic_column()

        # --- COLUMN 2: IDENTITY (THE CONTEXT) ---
        identity_panel = self._forge_identity_column()

        # --- COLUMN 3: SYSTEM/AI (THE ENGINE) ---
        system_panel = self._forge_system_column()

        grid.add_row(kinetic_panel, identity_panel, system_panel)

        # We wrap it in a Panel with a subtle style, as it complements the Tree.
        return Panel(
            grid,
            title="[bold dim]II. Gnostic Telemetry[/bold dim]",
            border_style="dim",
            padding=(0, 1)
        )

    def _forge_kinetic_column(self) -> Table:
        """Visualizes the physical changes."""
        t = Table.grid(padding=(0, 1))
        t.add_column(justify="right", style="dim cyan")
        t.add_column(style="bold white")

        # Files
        files = getattr(self.regs, 'files_forged', 0)
        t.add_row("Files Forged:", str(files))

        # Directories
        dirs = getattr(self.regs, 'sanctums_forged', 0)
        t.add_row("Sanctums:", str(dirs))

        # Mass (Bytes)
        bytes_written = getattr(self.regs, 'bytes_written', 0)
        t.add_row("Total Mass:", self._fmt_bytes(bytes_written))

        return t

    def _forge_identity_column(self) -> Table:
        """Visualizes who, when, and where (version control)."""
        t = Table.grid(padding=(0, 1))
        t.add_column(justify="right", style="dim yellow")
        t.add_column(style="bold white")

        # User
        user = self.env_stats.get('user') or "Architect"
        t.add_row("Architect:", user)

        # Git
        branch = self.env_stats.get('git_branch')
        if branch and branch != "void":
            t.add_row("Git Branch:", f"[magenta]{branch}[/magenta]")

        # Duration
        # We prioritize performance metrics passed in, else calculate from registers
        duration = self.perf_stats.get('duration_ms', 0) / 1000
        if duration == 0 and hasattr(self.regs, 'get_duration'):
            duration = self.regs.get_duration()

        t.add_row("Duration:", f"{duration:.3f}s")

        return t

    def _forge_system_column(self) -> Table:
        """Visualizes the machine spirit or AI cognition."""
        t = Table.grid(padding=(0, 1))
        t.add_column(justify="right", style="dim green")
        t.add_column(style="bold white")

        # AI Check
        tokens = self.ai_stats.get('tokens_total', 0) if self.ai_stats else 0

        if tokens > 0:
            # Show AI Stats if active
            model = self.ai_stats.get('model', 'Unknown')
            cost = self.ai_stats.get('cost_usd', 0.0)
            t.add_row("Neural Cortex:", f"[magenta]{model}[/magenta]")
            t.add_row("Tokens:", str(tokens))
            t.add_row("Est. Cost:", f"${cost:.4f}")
        else:
            # Show System Stats if AI dormant
            py_ver = self.env_stats.get('python') or platform.python_version()
            os_name = self.env_stats.get('os') or platform.system()

            t.add_row("Python:", py_ver)
            t.add_row("System:", os_name)
            t.add_row("Scaffold:", f"v{scaffold_ver}")

        return t

    def _fmt_bytes(self, size: int) -> str:
        """A tiny artisan for byte formatting."""
        if size == 0: return "0 B"
        power = 1024
        n = size
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        er = 0
        while n >= power:
            n /= power
            er += 1
        return f"{n:.1f} {power_labels.get(er, '')}B"