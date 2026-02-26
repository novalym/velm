# Path: src/velm/artisans/lint_blueprint/artisan.py
# -------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_LINTER_V25000_TOTAL_PERCEPTION_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# =========================================================================================

import time
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# --- RICH UI UPLINKS ---
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box
from rich.syntax import Syntax

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import LintBlueprintRequest
from ...help_registry import register_artisan
from ...core.blueprint_scribe.adjudicator import BlueprintAdjudicator
from ...contracts.heresy_contracts import HeresySeverity, Heresy
from ...parser_core.parser import parse_structure
from ...utils.gnosis_discovery import discover_required_gnosis


@register_artisan("lint-blueprint")
class BlueprintLinterArtisan(BaseArtisan[LintBlueprintRequest]):
    """
    =============================================================================
    == THE OMEGA BLUEPRINT LINTER (V-Ω-TOTALITY-V25000-SCOPE-AWARE)            ==
    =============================================================================
    LIF: ∞ | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN

    The absolute authority on structural and logical purity. It performs a
    multi-phase inquest to ensure that the mind (Gnosis) and matter (Form)
    of a blueprint are in perfect resonance.
    =============================================================================
    """

    def execute(self, request: LintBlueprintRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND INQUEST (CONDUCT)                                             ==
        =============================================================================
        """
        start_time = time.monotonic()

        # 1. GEOMETRIC ANCHORING
        # [ASCENSION 11]: Path Isomorphism
        target = (self.project_root / request.target).resolve()

        if not target.exists():
            return self.failure(f"Rite Stayed: The scripture '{request.target}' is unmanifest.")

        # 2. ADJUDICATE MODE
        # [ASCENSION 9]: Strictness Dial
        is_strict = request.strict or "archetypes" in str(target.parent).lower()
        mode_label = "Strict (Archetype)" if is_strict else "Lenient (Local)"

        self.logger.info(f"Leveling the foundation of [cyan]{target.name}[/cyan] in [magenta]{mode_label}[/magenta]...")

        try:
            # --- PHASE I: THE RITE OF INHALATION (PARSING) ---
            # [THE CURE]: We materialize the full Parser to learn the Macro Registry.
            # This is the "Mind" that the static analyzer was previously missing.
            parser, items, commands, edicts, variables, dossier = parse_structure(
                target,
                args=request,
                pre_resolved_vars=request.variables
            )

            # --- PHASE II: THE RITE OF ADJUDICATION (STATIC) ---
            # Conduct standard structural and metadata checks.
            adjudicator = BlueprintAdjudicator(self.project_root)
            content = target.read_text(encoding='utf-8')

            # The static adjudicator handles base syntax and metadata rules.
            heresies = adjudicator.adjudicate(content, target, enforce_metadata=is_strict)

            # --- PHASE III: THE OMEGA SUTURE (DYNAMIC DISCOVERY) ---
            # [THE CURE 2]: We re-run discovery using the Parser's Macro Registry.
            # This incinerates false-positives for macro arguments.

            self.logger.verbose("Inquisitor: Adjudicating Gnosis Gap with Macro Awareness...")

            enriched_dossier = discover_required_gnosis(
                execution_plan=items,
                post_run_commands=commands,
                blueprint_vars=variables,
                macros=parser.macros  # <<< THE SUTURE
            )

            # 1. Transform missing variables into high-status Heresies
            if enriched_dossier.missing:
                for missing_var in enriched_dossier.missing:
                    # [ASCENSION 4]: Socratic Path to Redemption
                    heresies.append(Heresy(
                        message=f"Undefined Variable '${{{missing_var}}}' detected.",
                        severity=HeresySeverity.WARNING,
                        suggestion=f"Define '$$ {missing_var} = ...' or pass it via '--set'.",
                        line_num=0,  # Global context
                        code="UNDEFINED_VAR",
                        details=f"Variable is referenced in the plan but unmanifested in any stratum."
                    ))

            # --- PHASE IV: THE REVELATION ---
            duration = (time.monotonic() - start_time) * 1000

            if not heresies:
                self._proclaim_purity(target.name, mode_label, duration)
                return self.success("The Lattice is Pure. No heresies perceived.")

            # Sort heresies by line number for causal flow
            sorted_heresies = sorted(heresies, key=lambda h: h.line_num)

            # [ASCENSION 7]: Substrate-Aware Proclamation
            if self.silent:
                return self.success("Inquest Concluded.", data={"heresies": [h.to_dict() for h in sorted_heresies]})

            return self._proclaim_heresies(target.name, sorted_heresies, mode_label, content)

        except Exception as e:
            # [ASCENSION 10]: THE NONE-TYPE SARCOPHAGUS
            self.logger.critical(f"Inquest Fractured: {e}")
            return self.failure(
                message=f"Forensic Collapse: {type(e).__name__}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == OCULAR PROJECTION (UI RITES)                                        ==
    # =========================================================================

    def _proclaim_purity(self, name: str, mode: str, duration_ms: float):
        """Renders the Luminous Seal of Approval."""
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", style="green")
        grid.add_column(justify="right", style="dim white")

        grid.add_row("Structure", "VALID")
        grid.add_row("Syntax", "PURE")
        grid.add_row("Scope", "RESONANT")
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

    def _proclaim_heresies(self, name: str, heresies: List[Heresy], mode: str, raw_content: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE DOSSIER OF FRACTURES (RICH REPORT)                                  ==
        =============================================================================
        """
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

        crit_count = 0
        lines = raw_content.splitlines()

        for h in heresies:
            if h.severity == HeresySeverity.CRITICAL:
                sev_label, crit_count = "[bold red]CRIT[/]", crit_count + 1
            elif h.severity == HeresySeverity.WARNING:
                sev_label = "[yellow]WARN[/]"
            else:
                sev_label = "[dim]INFO[/]"

            # [ASCENSION 6]: Forensic Snippet Mirroring
            msg_block = Text()
            msg_block.append(h.message, style="bold")

            if h.line_num > 0 and h.line_num <= len(lines):
                # Include a syntax-highlighted snippet of the offending line
                snippet = lines[h.line_num - 1].strip()
                msg_block.append(f"\n   [dim]> {snippet}[/]", style="dim italic")

            if h.details:
                msg_block.append(f"\n{h.details}", style="dim")

            if h.suggestion:
                msg_block.append(f"\n💡 {h.suggestion}", style="italic cyan")

            table.add_row(str(h.line_num) if h.line_num > 0 else "G", sev_label, msg_block, h.code)

        self.console.print(table)

        # FINAL ADJUDICATION
        if crit_count > 0:
            return self.failure(
                f"Materialization Risk: {crit_count} Critical Fractures perceived.",
                data={"heresies": [h.to_dict() if hasattr(h, 'to_dict') else h.__dict__ for h in heresies]}
            )

        return self.success(
            "Adjudication Passed (with minor imperfections).",
            data={"heresies": [h.to_dict() if hasattr(h, 'to_dict') else h.__dict__ for h in heresies]}
        )

    def __repr__(self) -> str:
        return f"<Ω_BLUEPRINT_LINTER version=25000.0 status=VIGILANT>"