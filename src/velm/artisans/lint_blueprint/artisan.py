# Path: src/velm/artisans/lint_blueprint/artisan.py
# -------------------------------------------------

import time
from pathlib import Path
from typing import List, Dict, Any

# --- RICH UI UPLINKS ---
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box
from rich.layout import Layout

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import LintBlueprintRequest
from ...help_registry import register_artisan
from ...core.blueprint_scribe.adjudicator import BlueprintAdjudicator
from ...contracts.heresy_contracts import HeresySeverity, Heresy


@register_artisan("lint-blueprint")
class BlueprintLinterArtisan(BaseArtisan[LintBlueprintRequest]):
    """
    =============================================================================
    == THE ARCHITECT'S LEVEL (V-Ω-STATIC-ANALYZER-ADJUDICATED)                 ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: BLUEPRINT_AUDITOR

    The High Priest of Form. It summons the `BlueprintAdjudicator` to perform a
    deep-tissue scan of a `.scaffold` scripture.

    [CAPABILITIES]:
    1.  **Contextual Strictness:** Automatically detects if the target is an
        Archetype (in `archetypes/`) and enforces metadata laws accordingly.
    2.  **Luminous Reporting:** Renders a beautiful, high-fidelity table of
        heresies using `rich`.
    3.  **Criticality Triage:** Distinguishes between fatal fractures (CRITICAL)
        and stylistic drift (WARNING/INFO/HINT).
    4.  **Forensic Detail:** Includes the specific error code and line number
        for rapid remediation.
    """

    def execute(self, request: LintBlueprintRequest) -> ScaffoldResult:
        start_time = time.monotonic()
        target = (self.project_root / request.target).resolve()

        if not target.exists():
            return self.failure(f"Blueprint '{request.target}' not found.")

        # 1. Divine Strictness Level
        # If the user passed --strict OR the file resides in an 'archetypes' directory,
        # we treat it as a Reusable Archetype and enforce metadata.
        # Otherwise, it is a Local Blueprint, and we allow flexibility.
        is_strict = False

        # Check request flag
        if hasattr(request, 'strict') and request.strict:
            is_strict = True
        # Check environmental context
        elif "archetypes" in str(target.parent).lower():
            is_strict = True

        mode_label = "Strict (Archetype)" if is_strict else "Lenient (Local)"
        self.logger.info(
            f"Leveling the foundation of [cyan]{target.name}[/cyan] in [magenta]{mode_label}[/magenta] mode...")

        # 2. Summon the Adjudicator
        adjudicator = BlueprintAdjudicator(self.project_root)

        try:
            content = target.read_text(encoding='utf-8')
        except Exception as e:
            return self.failure(f"Could not read blueprint: {e}")

        # 3. Conduct the Inquest
        heresies = adjudicator.adjudicate(content, target, enforce_metadata=is_strict)

        # 4. The Judgment of Purity
        if not heresies:
            duration = (time.monotonic() - start_time) * 1000
            self._proclaim_purity(target.name, mode_label, duration)
            return self.success("No heresies found.")

        # 5. The Proclamation of Heresy
        return self._proclaim_heresies(target.name, heresies, mode_label)

    def _proclaim_purity(self, name: str, mode: str, duration_ms: float):
        """Renders the Seal of Approval."""

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", style="green")
        grid.add_column(justify="right", style="dim white")

        grid.add_row("Structure", "VALID")
        grid.add_row("Syntax", "PURE")
        grid.add_row("Safety", "SECURE")
        grid.add_row("Metadata", "COMPLETE" if "Strict" in mode else "SKIPPED")

        panel = Panel(
            Group(
                Text(f"The Blueprint '{name}' is plumb and level.", style="bold green"),
                Text(""),
                grid
            ),
            title=f"[bold green]Ω PURITY CONFIRMED[/bold green] [dim]({duration_ms:.1f}ms)[/dim]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        self.console.print(panel)

    def _proclaim_heresies(self, name: str, heresies: List[Heresy], mode: str) -> ScaffoldResult:
        """Renders the Dossier of Fractures."""

        # Sort by Line Number for readable flow
        sorted_heresies = sorted(heresies, key=lambda h: h.line_num)

        crit_count = 0
        warn_count = 0
        hint_count = 0

        table = Table(
            title=f"[bold white]Inquest Report: {name}[/bold white] [dim]({mode})[/dim]",
            border_style="red" if any(h.severity == HeresySeverity.CRITICAL for h in heresies) else "yellow",
            expand=True,
            box=box.HEAVY_EDGE,
            header_style="bold white"
        )

        table.add_column("Ln", style="magenta", width=4, justify="right")
        table.add_column("Sev", style="bold", width=8, justify="center")
        table.add_column("Heresy & Redemption", style="white", ratio=1)
        table.add_column("Code", style="dim", width=20)

        for h in sorted_heresies:
            # Colorize Severity
            if h.severity == HeresySeverity.CRITICAL:
                sev_display = "[bold red]CRIT[/]"
                crit_count += 1
            elif h.severity == HeresySeverity.WARNING:
                sev_display = "[yellow]WARN[/]"
                warn_count += 1
            elif h.severity == HeresySeverity.INFO:
                sev_display = "[blue]INFO[/]"
                hint_count += 1
            else:
                sev_display = "[dim]HINT[/]"
                hint_count += 1

            # Format Message with Suggestion
            msg_block = Text()
            msg_block.append(h.message, style="bold")
            if h.details:
                msg_block.append(f"\n{h.details}", style="dim")
            if h.suggestion:
                # [ASCENSION]: Use a distinct color for the Path to Redemption
                msg_block.append(f"\n💡 {h.suggestion}", style="italic cyan")

            table.add_row(
                str(h.line_num),
                sev_display,
                msg_block,
                h.code
            )

        self.console.print(table)

        # Final Verdict Logic
        if crit_count > 0:
            summary = f"\n[bold red]✖ Adjudication Failed:[/bold red] {crit_count} Critical Fractures detected."
            self.console.print(summary)
            return self.failure(
                f"Found {len(heresies)} heresies in blueprint ({crit_count} Critical).",
                data={"heresies": [h.model_dump() for h in heresies]}
            )
        else:
            # If only warnings or hints, it is technically a success, but dirty.
            summary = f"\n[bold yellow]⚠ Adjudication Passed with Warnings.[/bold yellow] {warn_count} Warnings, {hint_count} Hints."
            self.console.print(summary)

            # We return success if only warnings/info exist, but include the data for CI checks
            return self.success(
                f"Blueprint is valid (with {len(heresies)} warnings/hints).",
                data={"heresies": [h.model_dump() for h in heresies]}
            )