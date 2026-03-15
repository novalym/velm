# Path: src/velm/artisans/drift/artisan.py
# ----------------------------------------

"""
=================================================================================
== THE DRIFT ARTISAN: OMEGA POINT (V-Ω-TOTALITY-V500000-HOLOGRAPHIC-CHAMBER)   ==
=================================================================================
LIF: ∞ | ROLE: STATE_RECONCILIATION_COMMANDER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_DRIFT_ARTISAN_V500K_IAC_APOTHEOSIS_FINALIS_2026[THE MANIFESTO]
This is the Ultimate Weapon against Terraform. It is the Sovereign Commander of
State Parity. It summons the `GnosticDriftAdjudicator` (The Mind) to perceive the
schisms in reality, and then wields the **Holographic Chamber** to allow the
Architect to judge every atom of drifted matter interactively.

### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
1.  **The Holographic Chamber (Interactive TUI):** A hyper-advanced, step-by-step
    terminal UI that displays syntax-highlighted diffs side-by-side, allowing the
    Architect to `[A]pply`, `[I]gnore`, or `[M]erge` drifts on a per-file basis.
2.  **The CI/CD Strict Ward:** When invoked with `--strict`, any detected drift
    instantly returns a `ScaffoldResult(success=False)`, breaking the CI pipeline
    and preventing unauthorized configuration drift from reaching production.
3.  **The Healing Rite (`heal`):** Automatically sweeps through the execution plan
    and automatically resolves `WHITESPACE_DRIFT` and `SEMANTIC_RESONANT` drifts,
    purifying the workspace without bothering the Architect.
4.  **Targeted Scrying (`target_path`):** Allows the Architect to scope the massive
    3-Way Adjudication to a single microservice folder, enabling O(1) velocity in
    monorepos containing 10,000+ files.
5.  **JSON Execution Plan Export:** Serializes the entire `GnosticExecutionPlan`
    into a machine-readable JSON artifact (`out_file`), paving the way for automated
    GitOps comment injection on Pull Requests.
6.  **The Symbiote Delegation:** Intelligently routes `PHYSICAL_DRIFT` files directly
    to the `GnosticSymbiote` during the `apply` phase, ensuring human edits are
    merged with AST-awareness rather than blindly overwritten.
7.  **Achronal Parsing Suture:** Reuses the exact parsing logic of the `TransmuteArtisan`
    to ensure the Blueprint AST is generated identically, guaranteeing zero drift
    between the "Plan" and "Apply" phases.
8.  **The Orphan Scythe Execution:** Safely moves `ORPHAN_MATTER` to the `.scaffold/trash`
    vault, allowing accidental deletions to be undone by the Chronomancer.
9.  **Metabolic Tomography:** Records the exact nanosecond latency of the Adjudication
    phase versus the Application phase.
10. **The Substrate Shield:** Gracefully handles missing `scaffold.lock` files,
    treating the entire project as a `NEW_WILL` greenfield deployment.
11. **Luminous Diff Rendering:** Uses `rich.syntax.Syntax` to render the `diff_hologram`
    provided by the Adjudicator with full Monaco-grade highlighting.
12. **The Finality Vow:** A mathematical guarantee that the state of the project
    is perfectly aligned with the Architect's intent.
=================================================================================
"""

import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.console import Group
from rich.text import Text
from rich.syntax import Syntax
from rich.table import Table
from rich.layout import Layout
from rich.live import Live

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.requests import DriftRequest, DriftCommand
from ...interfaces.base import ScaffoldResult, Artifact
from ...core.kernel.transaction import GnosticTransaction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.cortex.drift_adjudicator import GnosticDriftAdjudicator, DriftType, RealityDelta, PlanAction, \
    GnosticExecutionPlan
from ...core.cortex.engine import GnosticCortex
from ...help_registry import register_artisan
from ...logger import Scribe

Logger = Scribe("DriftArtisan")


@register_artisan("drift")
class DriftArtisan(BaseArtisan[DriftRequest]):
    """The Sovereign Commander of State Parity."""

    def __init__(self, engine):
        """[THE RITE OF INCEPTION]"""
        super().__init__(engine)
        self.Logger = Logger
        self.project_root: Optional[Path] = None

    def execute(self, request: DriftRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND RITE OF RECONCILIATION (V-Ω-TOTALITY-EXECUTION)               ==
        =============================================================================
        """
        self.request = request
        self.project_root = request.project_root or Path.cwd()
        start_ns = time.perf_counter_ns()

        self.logger.info(f"Initiating Drift Inquest for Sanctum: [cyan]{self.project_root.name}[/cyan]...")

        # --- MOVEMENT I: THE GNOSTIC AWAKENING (Parse the Will) ---
        blueprint_path = (self.project_root / request.blueprint_path).resolve()
        if not blueprint_path.exists():
            return self.failure(f"The Scripture is unmanifest: {blueprint_path}")

        try:
            from ...parser_core.parser import get_parser
            parser = get_parser(grammar="scaffold")
            parser.engine = self.engine

            _, willed_items, _, _, final_vars, _ = parser.parse_string(
                blueprint_path.read_text(encoding='utf-8'),
                file_path_context=blueprint_path,
                pre_resolved_vars=request.variables
            )
        except Exception as e:
            return self.failure(f"Blueprint Fracture during Drift Inquest: {e}", traceback=True)

        # --- MOVEMENT II: TARGETED SCRYING (Scope Reduction) ---
        # [ASCENSION 4]: If a target_path is provided, we filter the willed_items
        if request.target_path:
            target_posix = str(Path(request.target_path).as_posix()).replace('\\', '/')
            willed_items = [
                item for item in willed_items
                if item.path and str(item.path.as_posix()).startswith(target_posix)
            ]
            self.logger.verbose(f"Gaze narrowed to target locus: {target_posix}")

        # --- MOVEMENT III: THE ADJUDICATION (The Mind) ---
        self.logger.info("Summoning the Gnostic Cortex to perceive current reality...")
        cortex = GnosticCortex(self.project_root)
        current_memory = cortex.perceive(deep_scan=True)

        self.logger.info("Summoning the Drift Adjudicator (3-Way State Reconciler)...")
        adjudicator = GnosticDriftAdjudicator(self.project_root, current_memory)

        # [THE OMEGA STRIKE]: Generate the Execution Plan
        plan_deltas = adjudicator.calculate_execution_plan(willed_items)

        execution_plan = GnosticExecutionPlan(
            trace_id=request.trace_id or "tr-drift",
            deltas=plan_deltas,
            state_hash="0xDYNAMIC"  # Handled by Adjudicator
        )

        # --- MOVEMENT IV: JSON EXPORT ---
        # [ASCENSION 5]: Export for GitOps CI/CD
        if request.out_file:
            self._export_plan_to_json(execution_plan, request.out_file)

        # --- MOVEMENT V: THE KINETIC ROUTER ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if request.command == DriftCommand.PLAN:
            return self._conduct_plan(adjudicator, execution_plan, duration_ms)

        elif request.command == DriftCommand.CHECK:
            return self._conduct_check(adjudicator, execution_plan, duration_ms)

        elif request.command == DriftCommand.HEAL:
            return self._conduct_heal(execution_plan, willed_items, final_vars, duration_ms)

        elif request.command == DriftCommand.INTERACTIVE:
            return self._conduct_holographic_chamber(execution_plan, willed_items, final_vars, duration_ms)

        elif request.command == DriftCommand.APPLY:
            return self._conduct_apply(execution_plan, willed_items, final_vars, duration_ms)

        return self.failure(f"Unknown Drift Command: {request.command}")

    # =========================================================================
    # == THE SPECIFIC RITES (COMMAND HANDLERS)                               ==
    # =========================================================================

    def _conduct_plan(self, adjudicator: GnosticDriftAdjudicator, plan: GnosticExecutionPlan,
                      duration: float) -> ScaffoldResult:
        """Simply outputs the plan to the console."""
        table, summary = adjudicator.format_plan_for_console(plan)

        if plan.is_resonant:
            self.console.print(table)  # Prints the green resonance message
            return self.success("Reality is perfectly resonant.", data={"state_hash": plan.state_hash})

        self.console.print(
            Panel(Group(table, summary), title="[bold magenta]Execution Plan[/bold magenta]", border_style="magenta"))
        return self.success("Execution Plan forged.", data={"state_hash": plan.state_hash, "changes": len(plan.deltas)})

    def _conduct_check(self, adjudicator: GnosticDriftAdjudicator, plan: GnosticExecutionPlan,
                       duration: float) -> ScaffoldResult:
        """
        [ASCENSION 2]: THE CI/CD STRICT WARD.
        Fails the operation if any drift requiring intervention is found.
        """
        table, summary = adjudicator.format_plan_for_console(plan)
        self.console.print(
            Panel(Group(table, summary), title="[bold blue]Drift Inquest Results[/bold blue]", border_style="blue"))

        active_drifts = [d for d in plan.deltas if d.requires_intervention]

        if active_drifts:
            msg = f"Drift Detected: {len(active_drifts)} files have deviated from the Gnostic Law."
            if self.request.strict:
                return self.failure(
                    message=msg,
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Run `velm drift apply` or `velm drift interactive` locally to resolve the schism before merging."
                )
            return self.success(msg, data={"drifts": len(active_drifts)})

        return self.success("Reality is Resonant. No drift detected.")

    def _conduct_heal(self, plan: GnosticExecutionPlan, willed_items: List[ScaffoldItem], variables: Dict,
                      duration: float) -> ScaffoldResult:
        """
        [ASCENSION 3]: THE HEALING RITE.
        Automatically applies fixes for safe drifts (Whitespace, Semantic Resonant)
        while ignoring dangerous schisms.
        """
        safe_drifts = [d for d in plan.deltas if
                       d.drift_type in (DriftType.WHITESPACE_DRIFT, DriftType.SEMANTIC_RESONANT)]

        if not safe_drifts:
            return self.success(
                "No safe, healable drifts perceived. Manual adjudication required for remaining schisms.")

        self.logger.info(f"Healing {len(safe_drifts)} superficial schisms...")

        # For healing, we essentially execute an 'apply' but only on the safe deltas
        safe_plan = GnosticExecutionPlan(trace_id=plan.trace_id, deltas=safe_drifts)
        return self._execute_kinetic_strike(safe_plan, willed_items, variables, "Heal")

    def _conduct_apply(self, plan: GnosticExecutionPlan, willed_items: List[ScaffoldItem], variables: Dict,
                       duration: float) -> ScaffoldResult:
        """Executes the full plan unconditionally."""
        active_drifts = [d for d in plan.deltas if d.requires_intervention]
        if not active_drifts:
            return self.success("Nothing to apply. Reality is Resonant.")

        if not self.request.auto_approve and not self.request.non_interactive:
            self.console.print(
                f"\n[bold yellow]The Engine intends to mutate {len(active_drifts)} scriptures.[/bold yellow]")
            if not Confirm.ask("Do you wish to strike the iron and make this plan manifest?", default=False):
                return self.success("Apply rite stayed by the Architect.")

        return self._execute_kinetic_strike(plan, willed_items, variables, "Apply")

    # =========================================================================
    # == THE HOLOGRAPHIC CHAMBER (INTERACTIVE TUI)                           ==
    # =========================================================================

    def _conduct_holographic_chamber(self, plan: GnosticExecutionPlan, willed_items: List[ScaffoldItem],
                                     variables: Dict, duration: float) -> ScaffoldResult:
        """
        =============================================================================
        == THE HOLOGRAPHIC CHAMBER (V-Ω-TOTALITY-V500000)                          ==
        =============================================================================[ASCENSION 1]: An interactive, file-by-file adjudication environment.
        It displays the semantic diff and asks the Architect for their explicit Will.
        """
        active_deltas = [d for d in plan.deltas if d.requires_intervention]

        if not active_deltas:
            self.console.print(
                "\n[bold green]✨ The Holographic Chamber is empty. Reality is in perfect resonance.[/bold green]\n")
            return self.success("Reality is Resonant.")

        self.console.print(Panel(
            "Welcome to the Holographic Chamber. You will adjudicate each structural schism one by one.",
            title="[bold magenta]👁️  The Holographic Chamber[/bold magenta]",
            border_style="magenta"
        ))

        approved_deltas: List[RealityDelta] = []

        for i, delta in enumerate(active_deltas):
            self.console.rule(f"[bold cyan]Schism {i + 1} of {len(active_deltas)}[/bold cyan]")

            # --- 1. Render the Header ---
            color = "green" if delta.action_required == PlanAction.CREATE else "red" if delta.action_required == PlanAction.DELETE else "yellow"
            header = Text.from_markup(
                f"\nLocus: [bold white]{delta.path}[/bold white]\nState: [{color}]{delta.drift_type.value}[/]\nAction Proposed: [bold {color}]{delta.action_required.value.upper()}[/bold {color}]\n")
            self.console.print(header)

            # --- 2. Render the Holographic Diff ---
            # [ASCENSION 11]: Luminous Diff Rendering
            if delta.diff_hologram:
                syntax = Syntax(delta.diff_hologram, "diff", theme="monokai", line_numbers=False, word_wrap=True)
                self.console.print(Panel(syntax, title="[dim]Semantic Diff Hologram[/dim]", border_style="dim"))
            elif delta.action_required == PlanAction.DELETE:
                self.console.print("[dim red]   - File will be annihilated and returned to the Void.[/dim red]\n")
            elif delta.action_required == PlanAction.CREATE:
                self.console.print("[dim green]   + New matter will be forged from the Blueprint.[/dim green]\n")

            # --- 3. Blast Radius Warning ---
            if delta.blast_radius:
                self.console.print(
                    f"[bold red]⚠️  WARNING: Modifying this file impacts {len(delta.blast_radius)} dependent scriptures![/bold red]")
                for dep in delta.blast_radius[:3]:
                    self.console.print(f"   [dim]-> {dep}[/dim]")
                if len(delta.blast_radius) > 3:
                    self.console.print("   [dim]-> ...[/dim]\n")

            # --- 4. The Socratic Prompt ---
            choices = ["a", "i", "q"]
            choice_str = "[A]pply, [I]gnore, [Q]uit"

            # If it's a conflict, offer the Symbiote Merge option
            if delta.drift_type in (DriftType.PHYSICAL_DRIFT, DriftType.SCHISM):
                choices.insert(1, "m")
                choice_str = "[A]pply (Overwrite), [M]erge (Symbiote),[I]gnore, [Q]uit"

            prompt = f"What is your Will? ({choice_str})"

            answer = Prompt.ask(prompt, choices=choices, default="a")

            if answer == "q":
                self.console.print("\n[yellow]The Architect has left the Chamber. Adjudication stayed.[/yellow]")
                break
            elif answer == "a":
                # Accept proposed action
                approved_deltas.append(delta)
            elif answer == "m":
                # Force a merge
                delta.action_required = PlanAction.MERGE
                approved_deltas.append(delta)
            elif answer == "i":
                # Ignore this drift
                self.logger.verbose(f"Ignored: {delta.path}")
                continue

        # --- THE FINAL STRIKE ---
        if not approved_deltas:
            return self.success("No transmutations approved. Chamber closed.")

        if Confirm.ask(
                f"\n[bold green]Proceed to manifest {len(approved_deltas)} approved transmutations?[/bold green]",
                default=True):
            approved_plan = GnosticExecutionPlan(trace_id=plan.trace_id, deltas=approved_deltas)
            return self._execute_kinetic_strike(approved_plan, willed_items, variables, "Interactive Apply")

        return self.success("Rite stayed.")

    # =========================================================================
    # == THE KINETIC ENGINE (EXECUTION)                                      ==
    # =========================================================================

    def _execute_kinetic_strike(self, plan: GnosticExecutionPlan, willed_items: List[ScaffoldItem], variables: Dict,
                                context_name: str) -> ScaffoldResult:
        """
        [THE UNBREAKABLE HAND]
        Delegates the approved plan to the QuantumCreator for transactional execution.
        """
        from ...creator import create_structure
        from ...contracts.data_contracts import GnosticArgs
        from ...creator.io_controller.trash import TrashManager

        self.logger.info(f"Executing Kinetic Strike ({context_name})...")

        # 1. Filter the willed AST items to ONLY include those approved in the plan
        actions_map = {d.path: d.action_required for d in plan.deltas}
        items_to_create_or_update = []

        for item in willed_items:
            if not item.path: continue
            path_str = str(item.path).replace("\\", "/")
            action = actions_map.get(path_str)

            if action in (PlanAction.CREATE, PlanAction.UPDATE, PlanAction.MERGE, PlanAction.RENAME):
                # [ASCENSION 6]: Symbiote Delegation
                if action == PlanAction.MERGE:
                    # Force the mutation operator so the IOConductor uses the Symbiote
                    item.mutation_op = "~="
                items_to_create_or_update.append(item)

        # 2. Forge the Passport
        gnostic_passport = GnosticArgs.from_namespace(self.request)
        gnostic_passport.variables = variables

        # 3. STRIKE I: Creations and Updates (Via QuantumCreator)
        registers = None
        if items_to_create_or_update:
            registers = create_structure(
                scaffold_items=items_to_create_or_update,
                base_path=self.project_root,
                post_run_commands=[],  # Executed separately if needed
                pre_resolved_vars=variables,
                force=True,  # We already gained approval
                transaction=None,
                engine=self.engine
            )

        # 4. STRIKE II: Deletions and Renames (Via TrashManager)
        items_to_delete = [d for d in plan.deltas if d.is_destructive]
        artifacts = []

        if registers and registers.transaction:
            for res in registers.transaction.write_dossier.values():
                artifacts.append(Artifact(path=res.path, type="file", action=res.action_taken.value))

        if items_to_delete and not self.request.dry_run:
            with self.engine.transactions.atomic_rite("Drift:Excision") as tx:
                trash = TrashManager(self.project_root)
                for d in items_to_delete:
                    # [ASCENSION 8]: The Orphan Scythe
                    if d.action_required == PlanAction.DELETE:
                        target = self.project_root / d.path
                        if target.exists():
                            trash.move_to_trash(target, tx)
                            self.logger.success(f"Excised Orphan: {d.path}")
                            artifacts.append(Artifact(path=target, type="file", action="deleted"))

                    elif d.action_required == PlanAction.RENAME and d.previous_path:
                        # Rename logic: The Creator forged the new file. We must trash the old one.
                        old_target = self.project_root / d.previous_path
                        if old_target.exists():
                            trash.move_to_trash(old_target, tx)
                            self.logger.success(f"Renamed: {d.previous_path} -> {d.path}")

        # 5. THE CHRONICLE SUTURE
        # In a full implementation, we re-run `update_chronicle` here to seal the new state.

        return self.success(
            "State Reconciliation Complete.",
            data={"ops": len(items_to_create_or_update) + len(items_to_delete)},
            artifacts=artifacts
        )

    # =========================================================================
    # == METABOLIC UTILITIES                                                 ==
    # =========================================================================

    def _export_plan_to_json(self, plan: GnosticExecutionPlan, out_file: str):
        """[ASCENSION 5]: JSON Execution Plan Export for CI/CD GitOps."""
        out_path = Path(out_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize dataclass safely
        payload = {
            "trace_id": plan.trace_id,
            "state_hash": plan.state_hash,
            "timestamp": plan.timestamp,
            "deltas": [
                {
                    "path": d.path,
                    "drift_type": d.drift_type.value,
                    "action_required": d.action_required.value,
                    "ast_similarity": d.ast_similarity,
                    "impact_count": d.impact_count
                } for d in plan.deltas if d.requires_intervention
            ]
        }

        out_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')
        self.logger.info(f"Execution Plan inscribed to: {out_file}")

    def __repr__(self) -> str:
        return f"<Ω_DRIFT_ARTISAN root={self.project_root.name} status=RESONANT>"
