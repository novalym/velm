# Path: scaffold/artisans/heal/artisan.py
# ---------------------------------------

"""
=================================================================================
== THE GNOSTIC MENDER (V-Ω-GIT-AWARE-ULTIMA)                                   ==
=================================================================================
LIF: 10,000,000,000,000,000,000

This is the divine artisan in its final form. It heals not just the wounds of the
present (static analysis), but the wounds of the past (Git history).

It now possesses the **Gaze of the Historian**: It can query Git to detect files
that were renamed *without* the Daemon's supervision and retroactively heal their
Gnostic bonds.
"""
import ast
import difflib
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table

# --- THE DIVINE SUMMONS ---
from .contracts import HealingResult, HealingDiagnosis, BaseHealer
from .healers.python_import_healer import PythonImportHealer
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import HealRequest
from ...utils import find_project_root, atomic_write


class HealArtisan(BaseArtisan[HealRequest]):
    """The Grand Orchestrator of Codebase Health."""

    def execute(self, request: HealRequest) -> ScaffoldResult:
        """The Grand Rite of Restoration."""
        start_time = time.time()
        project_root, _ = find_project_root(Path.cwd())
        if not project_root:
            return self.failure("Healing requires a valid project sanctum.")

        # --- MOVEMENT I: THE GAZE OF HISTORY (GIT RENAMES) ---
        # If the user didn't specify a file, we check for global move events.
        git_moves = {}
        if not request.file_path:
            # We automatically detect moves unless specifically told otherwise?
            # Or we make it a flag? For V-Omega, we make it smart: if no path provided, check git.
            git_moves = self._detect_git_renames(project_root)

        if git_moves:
            self.logger.info(f"The Gnostic Historian detected {len(git_moves)} unhealed rename(s) via Git.")
            # We must summon the Cortex to prophesy the healing plan for these moves.
            # This logic mirrors the Sentinel but runs manually here.
            from ...core.cortex.engine import GnosticCortex
            cortex = GnosticCortex(project_root)
            # We don't need a full scan, just enough to map the graph.
            cortex.perceive()

            healing_plan = cortex.prophesy_healing_plan(git_moves)

            if healing_plan:
                # We inject these diagnoses into the workflow
                # BUT wait, the standard flow below assumes we are scanning files for static errors.
                # The Cortex returns a specific plan (File -> [Edicts]).
                # We should execute this plan immediately for the moves.
                self._conduct_historical_healing(healing_plan, project_root, request)

        # --- MOVEMENT II: THE CONSECRATION OF TARGETS ---
        targets, scan_scope = self._resolve_targets_and_scope(request.file_path, project_root)
        if not targets and not git_moves:
            return self.failure("No scriptures found to heal.")

        # --- MOVEMENT III: THE FORGING OF THE POLYGLOT GNOSTIC CONTEXT ---
        if targets:
            self.logger.info("Forging Polyglot Gnostic Context for the Healing Pantheon...")
            context = self._forge_context(targets, project_root, scan_scope)

            # --- MOVEMENT IV: THE SUMMONS OF THE PANTHEON ---
            healers: List[BaseHealer] = [
                PythonImportHealer(project_root, context),
            ]

            # --- MOVEMENT V: THE GRAND DIAGNOSTIC SYMPHONY ---
            all_diagnoses, total_wounds = self._conduct_diagnostic_phase(targets, healers)

            if not total_wounds and not git_moves:
                return self.success(f"The Physician's Gaze is serene. All {len(targets)} scriptures are healthy.")

            if total_wounds:
                self._proclaim_diagnostic_report(all_diagnoses)

            # [FACULTY 10] The Check-Only Sentinel
            if request.check_only:
                if total_wounds > 0:
                    return self.failure(f"Found {total_wounds} wounds across {len(all_diagnoses)} files.",
                                        data={"wounds": total_wounds})
                return self.success("Check complete. No static wounds found.")

            # [ELEVATION 13] GUARDIAN'S OFFER
            patients = list(all_diagnoses.keys())
            self.guarded_execution(patients, request, context="heal")

            # [FACULTY 7] Gnostic Consent
            if total_wounds > 0 and not request.force and not Confirm.ask(
                    f"[bold red]Apply healing to {len(all_diagnoses)} files?[/bold red]", default=True):
                return self.success("The Rite of Healing was stayed by the Architect's will.")

            # --- MOVEMENT VI: THE SURGICAL HEALING RITE ---
            results = self._conduct_healing_phase(all_diagnoses, healers, project_root)
            self._proclaim_results(results)

            healed_count = sum(1 for r in results if r.success and r.changes_made)

            return self.success(f"Rite complete. {healed_count} scriptures healed.")

        return self.success("Historical healing complete.")

    def _detect_git_renames(self, root: Path) -> Dict[Path, Path]:
        """[FACULTY 13] Queries Git for uncommitted renames."""
        moves = {}
        if not (root / ".git").exists(): return moves

        try:
            # porcelain status: R  old -> new
            res = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
            for line in res.stdout.splitlines():
                if line.startswith("R "):
                    parts = line[3:].split(" -> ")
                    if len(parts) == 2:
                        old = (root / parts[0]).resolve()
                        new = (root / parts[1]).resolve()
                        moves[old] = new
        except Exception:
            pass
        return moves

    def _conduct_historical_healing(self, plan: Dict[Path, List[Dict]], root: Path, request: HealRequest):
        """Executes the healing plan derived from Git history."""
        from ...artisans.translocate_core.resolvers import PythonImportResolver

        self.logger.info(f"Healing {len(plan)} files affected by Git renames...")

        # We need a resolver instance. We pass empty maps because the plan is already fully formed.
        resolver = PythonImportResolver(root, {}, {})

        count = 0
        for file_path, edicts in plan.items():
            if not file_path.exists(): continue

            if request.check_only:
                self.console.print(f"[yellow]Would heal:[/yellow] {file_path.name} ({len(edicts)} imports)")
                continue

            try:
                # We use the resolver's ability to execute a pre-calculated plan
                if resolver.conduct_healing_rite(file_path, edicts):
                    self.console.print(f"[green]✔ Healed:[/green] {file_path.relative_to(root)}")
                    count += 1
            except Exception as e:
                self.logger.error(f"Failed to heal {file_path.name}: {e}")

    def _resolve_targets_and_scope(self, raw_path: Optional[str], project_root: Path) -> tuple[List[Path], Path]:
        """[FACULTY 4] The Scoped Gaze."""
        if not raw_path:
            # If no path, scan the whole project (src/)
            scan_scope = project_root
            # Heuristic: Only scan src/ and tests/ to avoid node_modules chaos
            targets = []
            for d in ['src', 'app', 'lib', 'tests']:
                if (project_root / d).exists():
                    targets.extend(list((project_root / d).rglob('*')))

            # Fallback if structure is flat
            if not targets:
                targets = list(project_root.glob("*.py"))

            return [t for t in targets if t.is_file()], scan_scope

        path_obj = Path(raw_path)
        abs_path = path_obj.resolve() if path_obj.is_absolute() else (project_root / path_obj).resolve()

        if not abs_path.exists():
            raise ArtisanHeresy(f"The patient '{raw_path}' cannot be found.")

        scan_scope = abs_path if abs_path.is_dir() else abs_path.parent
        targets = list(scan_scope.rglob('*')) if abs_path.is_dir() else [abs_path]

        return [t for t in targets if t.is_file()], scan_scope

    def _forge_context(self, targets: List[Path], project_root: Path, scan_scope: Path) -> Dict[str, Any]:
        """[FACULTY 2] The Polyglot Context Forge."""
        context = {}
        target_suffixes = {t.suffix for t in targets}

        if '.py' in target_suffixes:
            self.logger.info(f"Building Python Symbol Map...")
            from ...inquisitor.python_inquisitor import PythonCodeInquisitor
            # We scan the WHOLE project to find symbols, even if we only heal one file.
            # Healing requires knowing where everything IS.
            inquisitor = PythonCodeInquisitor(project_root).inquire_project()

            if not inquisitor.symbol_map:
                self.logger.warn("The Python Inquisitor's Gaze returned a void.")
            else:
                context['python_symbol_map'] = inquisitor.symbol_map

        return context

    def _conduct_diagnostic_phase(self, targets: List[Path], healers: List[BaseHealer]) -> tuple[
        Dict[Path, List[HealingDiagnosis]], int]:
        """The pure symphony of diagnosis."""
        all_diagnoses: Dict[Path, List[HealingDiagnosis]] = {}
        total_wounds = 0

        # Only show spinner if we have many targets
        ctx = self.console.status("[bold yellow]Diagnosing...[/bold yellow]") if len(
            targets) > 5 else self.console.print("[dim]Diagnosing...[/dim]")

        if hasattr(ctx, '__enter__'): ctx.__enter__()

        for file_path in targets:
            try:
                # Optimization: Read once
                content = file_path.read_text(encoding='utf-8')
                file_diagnoses = []
                for healer in healers:
                    if healer.can_heal(file_path):
                        file_diagnoses.extend(healer.diagnose(file_path, content))
                if file_diagnoses:
                    all_diagnoses[file_path] = file_diagnoses
                    total_wounds += len(file_diagnoses)
            except Exception:
                continue

        if hasattr(ctx, '__exit__'): ctx.__exit__(None, None, None)

        return all_diagnoses, total_wounds

    def _conduct_healing_phase(self, all_diagnoses: Dict[Path, List[HealingDiagnosis]], healers: List[BaseHealer],
                               project_root: Path) -> List[HealingResult]:
        """The pure symphony of healing."""
        results: List[HealingResult] = []

        for file_path, diagnoses in all_diagnoses.items():
            try:
                original_content = file_path.read_text(encoding='utf-8')
                current_content = original_content

                diagnoses_by_healer: Dict[str, List[HealingDiagnosis]] = {}
                for d in diagnoses:
                    diagnoses_by_healer.setdefault(d.healer_name, []).append(d)

                for healer in healers:
                    if healer.name in diagnoses_by_healer:
                        new_content, was_changed = healer.heal(file_path, current_content,
                                                               diagnoses_by_healer[healer.name])
                        if was_changed:
                            current_content = new_content

                if current_content != original_content:
                    if file_path.suffix == '.py':
                        ast.parse(current_content)  # Syntax check

                    diff = "".join(difflib.unified_diff(
                        original_content.splitlines(keepends=True), current_content.splitlines(keepends=True),
                        fromfile="a/" + file_path.name, tofile="b/" + file_path.name
                    ))
                    atomic_write(file_path, current_content, self.logger, project_root, verbose=False)
                    results.append(HealingResult(file_path, "All", True, True, "Healed", diff))
                else:
                    results.append(HealingResult(file_path, "All", True, False, "No change"))

            except Exception as e:
                self.logger.error(f"Healing failed for '{file_path.name}': {e}")
                results.append(HealingResult(file_path, "All", False, False, str(e)))
        return results

    def _proclaim_diagnostic_report(self, diagnoses_map: Dict[Path, List[HealingDiagnosis]]):
        """[FACULTY 5] The Luminous Diagnostic Dossier."""
        table = Table(title="[bold red]Diagnostic Dossier[/bold red]", box=None)
        table.add_column("Scripture", style="cyan")
        table.add_column("Wound", style="white")

        for path, wounds in diagnoses_map.items():
            for i, w in enumerate(wounds):
                scripture_name = path.name if i == 0 else ""
                table.add_row(scripture_name, w.description)

        self.console.print(Panel(table, border_style="red"))

    def _proclaim_results(self, results: List[HealingResult]):
        """[FACULTY 9] The Luminous Diff Proclamation."""
        for res in results:
            if res.success and res.changes_made:
                self.console.print(f"[green]✔ Healed:[/green] {res.file_path.name}")
                if res.diff:
                    # Show a compact diff (first 5 lines)
                    diff_lines = res.diff.splitlines()[:5]
                    self.console.print(Syntax("\n".join(diff_lines), "diff", theme="monokai"))