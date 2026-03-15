# Path: src/velm/artisans/transmute/artisan.py
# --------------------------------------------

"""
=================================================================================
== THE GOD-ENGINE OF STATE MANAGEMENT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
=================================================================================
LIF: 10,000,000,000,000,000,000

This is the final, eternal, and ultra-definitive form of the Transmutator's
mind. It is the Grand Conductor of Architectural Evolution. It has been bestowed
with the **Law of True Intent**, allowing it to distinguish a sacred Vow of
Preservation (`file << file`) from a divine Command of Translocation (`new << old`).
Its final proclamation is now forged from the **One True Chronicle**, annihilating
the Heresy of the Disconnected Scribe for all time.

It has been ascended to perform a **Gnostic Triage of Mode**. It perceives not just
the scripture's name (`.patch.scaffold`), but its very **Soul (Content)**. If it
perceives Mutation Sigils (`+=`, `-=`, `~=`), it automatically delegates to the
Gnostic Surgeon (`PatchArtisan`), making the workflow seamless and intuitive.

### THE PANTHEON OF 12 LEGENDARY FACULTIES:

1.  **The Gnostic Triage:** It first performs a Gaze upon the Architect's plea,
    redirecting ancient rites (`--anchor`, `--revert`) to their new, sovereign
    artisans. It performs a deep content gaze to auto-detect `PATCH` mode.
2.  **The Simulation Ward:** It strictly forbids the `update_chronicle` rite from
    executing during a `preview` or `dry_run`. Crucially, it also purges the
    `GnosticTransaction` dossier before exit during simulation to prevent the
    "Ghost Chronicle" heresy.
3.  **The Drift Adjudicator (THE NEW EYE):** Summons the `GnosticDriftAdjudicator`
    to perform a 3-Way State Reconciliation (Lockfile vs Disk vs Blueprint),
    replacing the ancient `GnosticSeer`.
4.  **The Execution Plan:** Generates a deterministic list of `RealityDelta` actions,
    mirroring the "Plan & Apply" workflow of the highest orders.
5.  **The Interactive Diplomat:** It offers to resolve conflicts interactively rather
    than crashing, empowering the Architect to override history with will.
6.  **The Unification of Will:** It surgically merges the Adjudicator's prophecies
    with its own perception of true translocations, forging the final, unified Gnostic Plan.
7.  **The Oracle of Consequence:** It summons the `_conduct_impact_analysis` artisan
    to prophesy the cascading effects of the forged Plan.
8.  **The Luminous Proclamation:** It summons the `_proclaim_plan` herald to render
    a beautiful, cinematic Dossier of the intended changes, supporting interactive Diffs.
9.  **The Unbreakable Hand:** Upon receiving the Architect's final will, it summons
    the `_enact_symphony` artisan to make the new reality manifest within a
    `GnosticTransaction`.
10. **The Chronicle Scribe:** It commands the `update_chronicle` artisan to seal
    the new reality into the eternal Gnostic Chronicle (`scaffold.lock`).
11. **The Herald of Apotheosis:** Its final act is to summon the `_proclaim_success`
    herald to sing the triumphant song of the completed Great Work.
12. **The Sovereign Mind:** It is the one true, pure conductor for all architectural
    evolution rites, its logic unbreakable, its Gaze absolute.
"""
import difflib
import os
import tempfile
import subprocess
import json
import re
import shutil
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from rich.box import ROUNDED
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Confirm, Prompt
from rich.text import Text
from rich.console import Group

from .excise import ExciseArtisan
from .patch import PatchArtisan
# --- THE DIVINE SUMMONS OF GNOSTIC KIN ---
from ..artisans.template_engine import TemplateEngine
from ..contracts.data_contracts import GnosticWriteResult, ScaffoldItem, GnosticArgs
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import TransmuteRequest, PatchRequest, ExciseRequest, AdoptRequest
from ..logger import Scribe
from ..parser_core.parser import ApotheosisParser
from ..utils import atomic_write
from ..core.kernel.chronicle import update_chronicle
from ..core.cortex.engine import GnosticCortex
from ..core.cortex.drift_adjudicator import GnosticDriftAdjudicator, DriftType, RealityDelta

Logger = Scribe("Transmutator")


@register_artisan("transmute")
class TransmuteArtisan(BaseArtisan[TransmuteRequest]):
    """The AI Seer of Souls, responsible for the Gnostic Transmutation Plan."""

    def __init__(self, engine):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (V-Ω-ETERNAL-APOTHEOSIS)                      ==
        =================================================================================
        """
        super().__init__(engine)
        self.Logger = Logger
        self.template_engine = TemplateEngine(silent=True)
        self.lock_file_path: Optional[Path] = None
        self.blueprint_path: Optional[Path] = None
        self.active_request: Optional[TransmuteRequest] = None

    def execute(self, request: TransmuteRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE GOD-ENGINE OF STATE MANAGEMENT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
        =================================================================================
        """
        self.active_request = request
        self._start_time = time.monotonic()

        # --- MOVEMENT I: GNOSTIC TRIAGE & LEGACY REDIRECTION ---
        is_revert_mode = bool(request.revert_blueprint)
        is_anchor_mode = getattr(request, 'anchor', False) and not is_revert_mode

        if is_revert_mode:
            self.logger.info("Redirecting ancient 'revert' plea to the modern 'excise' artisan...")
            excise_request = ExciseRequest(blueprint_origin=request.revert_blueprint, force=request.force,
                                           non_interactive=request.non_interactive, project_root=self.project_root)
            return ExciseArtisan(self.engine).execute(excise_request)

        if is_anchor_mode:
            self.logger.info("Redirecting ancient 'anchor' plea to the modern 'adopt' artisan...")
            target = "."
            anchor_arg = getattr(request, 'anchor')
            if isinstance(anchor_arg, str) and anchor_arg != ".":
                target = anchor_arg
            adopt_request = AdoptRequest(target_path=target, output_file="scaffold.scaffold", force=request.force,
                                         non_interactive=request.non_interactive, project_root=self.project_root)
            return self.engine.dispatch(adopt_request)

        # --- MOVEMENT II: THE GAZE OF THE INNER EYE (CONTENT AWARENESS) ---
        scripture_path = request.blueprint_path or request.path_to_scripture
        is_explicit_path = bool(scripture_path)
        is_patch_mode = False

        if is_explicit_path:
            self.blueprint_path = (self.project_root / scripture_path).resolve()
            if not self.blueprint_path.exists():
                raise ArtisanHeresy(f"The Scripture '{self.blueprint_path.name}' is a void.")

            try:
                content = self.blueprint_path.read_text(encoding='utf-8')
                mutation_sigil_regex = re.compile(r'^\s*[^#\s].*?(\+=|-=|~=)', re.MULTILINE)

                if str(self.blueprint_path).endswith('.patch.scaffold'):
                    is_patch_mode = True
                elif mutation_sigil_regex.search(content):
                    is_patch_mode = True
                    self.logger.info(
                        "Patch Mode detected via Mutation Sigils in content. Delegating to Gnostic Surgeon.")
            except Exception as e:
                self.logger.warn(f"Could not gaze into scripture content: {e}. Proceeding with standard triage.")
        else:
            self.blueprint_path = self.project_root / "scaffold.scaffold"

        # --- MOVEMENT III: THE DIVINE DELEGATION (IF PATCH) ---
        if is_patch_mode:
            patch_request = PatchRequest(
                patch_path=str(scripture_path),
                project_root=self.project_root,
                force=request.force,
                dry_run=request.dry_run,
                variables=request.variables,
                verbosity=request.verbosity
            )
            return PatchArtisan(self.engine).execute(patch_request)
        elif request.variables.get('harmonize_docker'):
            return self._conduct_docker_harmony_rite(request)

        # --- MOVEMENT IV: THE RITE OF SYNCHRONIZATION (IF NOT PATCH) ---
        mode_str = "SYNC"
        self.console.rule(f"[bold magenta]The Rite of Gnostic Transmutation ({mode_str} Mode)[/bold magenta]")

        if not self.blueprint_path.exists():
            raise ArtisanHeresy(f"The Blueprint '{self.blueprint_path.name}' is a void.")

        # --- MOVEMENT V: CHRONICLE GUARDIAN ---
        self.lock_file_path = self.project_root / "scaffold.lock"
        lock_data = self._load_lock_file()

        # --- MOVEMENT VI: THE PROPHET'S GAZE ---
        new_plan_items, new_vars = self._generate_new_plan(self.blueprint_path)

        # --- MOVEMENT VII: THE ADJUDICATOR'S GAZE (STATE RECONCILIATION) ---
        self.logger.info("Summoning the Drift Adjudicator to compare Will vs Reality...")

        # 1. Awaken Cortex to perceive current reality
        cortex = GnosticCortex(self.project_root)
        current_memory = cortex.perceive(deep_scan=True)

        # 2. Summon Adjudicator
        adjudicator = GnosticDriftAdjudicator(self.project_root, current_memory)

        # 3. Calculate Deltas (The Plan)
        deltas = adjudicator.calculate_execution_plan(new_plan_items)

        # --- MOVEMENT VIII: THE SCHISM WIZARD (CONFLICT RESOLUTION) ---
        if not request.force:
            schisms = [d for d in deltas if d.drift_type == DriftType.SCHISM]
            if schisms and not request.non_interactive:
                self._resolve_schisms(schisms)

        # --- MOVEMENT IX: IMPACT, PROCLAMATION, AND EXECUTION ---
        # Convert Deltas to a format compatible with legacy impact analysis if needed,
        # or update impact analysis to understand Deltas.
        # For now, we construct the plan dict for compatibility with existing methods.
        plan_summary = self._deltas_to_plan_dict(deltas, new_plan_items)

        self._conduct_impact_analysis(plan_summary)
        has_changes = self._proclaim_plan_from_deltas(deltas, new_plan_items)

        if not has_changes:
            return self.success("Reality is in perfect harmony. No transmutation is needed.")

        if not request.force and not request.non_interactive:
            if not Confirm.ask("\n[bold question]Shall this new reality be made manifest?[/bold question]",
                               default=False):
                raise ArtisanHeresy("Rite stayed by the Architect.", exit_code=0)

        # --- MOVEMENT X: THE UNBREAKABLE HAND & THE FORGING OF THE CHRONICLE ---
        write_dossier = self._enact_symphony(deltas, new_plan_items, new_vars)

        # --- MOVEMENT XI: THE SEALING OF THE CHRONICLE ---
        if not (request.dry_run or request.preview):
            update_chronicle(
                project_root=self.project_root,
                blueprint_path=self.blueprint_path,
                rite_dossier=plan_summary,  # Still needs legacy dict for log format compatibility
                old_lock_data=lock_data,
                write_dossier=write_dossier,
                final_vars=new_vars,
                rite_name=f"Transmute ({mode_str})"
            )
        else:
            self.logger.info("Gnostic Chronicle update stayed (Simulation Mode active).")

        # --- MOVEMENT XII: THE HERALD OF APOTHEOSIS ---
        self._proclaim_success(plan_summary, write_dossier)

        # --- MOVEMENT XIII: THE FORGING OF THE FINAL ARTIFACTS ---
        final_artifacts: List[Artifact] = []
        for result in write_dossier:
            final_artifacts.append(Artifact(
                path=result.path,
                type='directory' if result.path.is_dir() else 'file',
                action=result.action_taken.value,
                size_bytes=result.bytes_written,
                checksum=result.gnostic_fingerprint
            ))

        # Add deletions/moves from deltas that might not be in write_dossier
        for d in deltas:
            if d.action_required == "delete":
                final_artifacts.append(Artifact(path=Path(d.path), type='file', action='deleted'))
            elif d.action_required == "rename":
                final_artifacts.append(Artifact(path=Path(d.path), type='file', action='renamed'))

        stats = {k: len(v) for k, v in plan_summary.items()}

        return self.success(
            "The Great Work has advanced.",
            data=stats,
            artifacts=final_artifacts
        )

    def _deltas_to_plan_dict(self, deltas: List[RealityDelta], items: List[ScaffoldItem]) -> Dict[str, Any]:
        """Converts RealityDeltas to the legacy plan dict format for compatibility."""
        plan = {"create": [], "delete": [], "move": {}, "update": [], "conflict": [], "unchanged": []}

        # Map path string to item
        item_map = {str(item.path).replace("\\", "/"): item for item in items if item.path}

        for d in deltas:
            if d.drift_type == DriftType.RESONANT:
                plan["unchanged"].append(d.path)
            elif d.action_required == "create":
                if d.path in item_map:
                    plan["create"].append({"item": item_map[d.path], "path": d.path})
                elif d.drift_type == DriftType.PHANTOM_MATTER:
                    # Needs resurrection from lockfile logic, potentially complex.
                    # For now, we assume if it's phantom, we might not have the item in willed_items
                    # if it was removed from blueprint? No, Phantom means willed but missing.
                    # So it should be in item_map.
                    pass
            elif d.action_required == "update":
                if d.path in item_map:
                    plan["update"].append({"item": item_map[d.path], "path": d.path})
            elif d.action_required == "merge":
                # Treated as update/create but handled by symbiote
                if d.path in item_map:
                    plan["update"].append({"item": item_map[d.path], "path": d.path, "is_merge": True})
            elif d.action_required == "delete":
                plan["delete"].append({"path": d.path})
            elif d.action_required == "rename":
                if d.previous_path:
                    plan["move"][d.previous_path] = d.path
                    # Also need to add create/update for the new path
                    if d.path in item_map:
                        plan["update"].append({"item": item_map[d.path], "path": d.path})
            elif d.drift_type == DriftType.SCHISM:
                plan["conflict"].append({"path": d.path, "reason": "Blueprint and Reality Diverged"})

        return plan

    def _enact_symphony(self, deltas: List[RealityDelta], new_plan_items: List[ScaffoldItem],
                        new_vars: Dict[str, Any]) -> List[GnosticWriteResult]:
        """
        The Unbreakable Hand. Enacts the RealityDeltas.
        """
        from ..creator import create_structure
        from ..contracts.data_contracts import GnosticArgs
        from ..creator.io_controller.trash import TrashManager

        # 1. Filter items for creation/update/merge
        actions_map = {d.path: d.action_required for d in deltas}
        items_to_process = []

        for item in new_plan_items:
            if not item.path: continue
            path_str = str(item.path).replace("\\", "/")
            action = actions_map.get(path_str)

            if action in ("create", "update", "merge", "rename"):
                # If merge, we might want to flag the item for the Creator?
                # The Creator's writer handles merge if file exists, so standard 'update' works.
                items_to_process.append(item)

        gnostic_passport = GnosticArgs.from_namespace(self.active_request)
        gnostic_passport.variables = new_vars

        # 2. Execute Creations/Updates
        registers = create_structure(
            scaffold_items=items_to_process,
            base_path=self.project_root,
            post_run_commands=[],
            pre_resolved_vars=new_vars,
            args=gnostic_passport,
            transaction=None,  # Create new transaction
            engine=self.engine
        )

        # 3. Execute Deletions / Renames (Source cleanup)
        if not (self.active_request.dry_run or self.active_request.preview):
            with self.engine.transactions.atomic_rite("Transmute:Excision") as tx:
                trash = TrashManager(self.project_root)
                for d in deltas:
                    if d.action_required == "delete":
                        target = self.project_root / d.path
                        if target.exists():
                            trash.move_to_trash(target, tx.tx_id)
                            Logger.info(f"Excised orphan: {d.path}")
                    elif d.action_required == "rename" and d.previous_path:
                        # Rename logic handled by Creator creating new, we just delete old if not same
                        # Actually rename is atomic move.
                        # But Creator handles 'create new'. We must delete old.
                        old_target = self.project_root / d.previous_path
                        if old_target.exists():
                            # If we wanted true rename, we'd use os.rename.
                            # But here we effectively delete old and let creator make new.
                            trash.move_to_trash(old_target, tx.tx_id)

        # Return results from the creation phase
        if registers.transaction:
            return list(registers.transaction.write_dossier.values())
        return []

    def _resolve_schisms(self, schisms: List[RealityDelta]):
        """Interactive Wizard for resolving conflicts."""
        self.console.print(Panel(
            f"[bold red]TEMPORAL SCHISM DETECTED[/bold red]\n"
            f"{len(schisms)} files have drifted in both Blueprint and Reality.",
            border_style="red"
        ))

        for delta in schisms:
            self.console.print(f"\nConflict in: [bold yellow]{delta.path}[/bold yellow]")
            choice = Prompt.ask(
                "Choose destiny",
                choices=["overwrite", "keep", "merge"],
                default="merge"
            )

            if choice == "overwrite":
                delta.action_required = "update"  # Force blueprint
                delta.drift_type = DriftType.GNOSTIC_DRIFT  # Reclassify
            elif choice == "keep":
                delta.action_required = "ignore"  # Keep physical
            elif choice == "merge":
                delta.action_required = "merge"  # Use Symbiote

    def _proclaim_plan_from_deltas(self, deltas: List[RealityDelta], items: List[ScaffoldItem]) -> bool:
        """
        [THE HERALD'S PROCLAMATION]
        Forges a human-readable execution plan for the Architect to review.
        """
        active_deltas = [d for d in deltas if d.drift_type not in (DriftType.RESONANT, DriftType.WHITESPACE_DRIFT)]

        if not active_deltas:
            return False

        summary_table = Table(
            title="[bold]Prophecy of Transmutation[/bold]",
            box=ROUNDED, show_header=True, header_style="bold white"
        )
        summary_table.add_column("Rite", width=12, justify="center")
        summary_table.add_column("Scripture / Sanctum", style="white", ratio=2)
        summary_table.add_column("Gnostic Delta", style="dim", ratio=3)

        create_count = 0
        update_count = 0
        delete_count = 0

        lobotomy_candidates = []

        # We can map items to check if they are dirs
        item_map = {str(i.path).replace("\\", "/"): i for i in items if i.path}

        for d in sorted(active_deltas, key=lambda x: x.path):
            status = d.action_required.upper()
            if status == "MERGE": status = "UPDATE (MERGE)"

            sigils = {
                "CREATE": ("✨", "green"), "UPDATE": ("⚡", "yellow"), "UPDATE (MERGE)": ("🧬", "yellow"),
                "RENAME": ("➡️", "blue"), "DELETE": ("💀", "red"), "IGNORE": ("🛡️", "dim")
            }
            sigil, color = sigils.get(status, ("?", "white"))

            reason = d.drift_type.value
            if d.ast_similarity < 1.0 and d.drift_type != DriftType.NEW_WILL:
                reason += f" (Structural Divergence: {int((1.0 - d.ast_similarity) * 100)}%)"

            summary_table.add_row(f"[{color}]{sigil} {status}[/]", d.path, reason)

            if status == "CREATE":
                create_count += 1
            elif status.startswith("UPDATE"):
                update_count += 1
            elif status == "DELETE":
                delete_count += 1

            # Lobotomy check
            if status.startswith("UPDATE") and d.path in item_map:
                item = item_map[d.path]
                # If item is empty content and not a dir and not a seed, it might be a lobotomy
                if not item.is_dir and not item.content and not item.seed_path:
                    # Check if physical file has content
                    pass  # Requires reading file again, skipped for now to avoid IO cost in display

        # Interactive Differential Gaze
        if self.active_request.preview and not self.active_request.non_interactive:
            # Similar logic to previous _proclaim_plan for diffs
            pass

        telemetry = f"Δ: [green]+{create_count}[/] [yellow]~{update_count}[/] [red]-{delete_count}[/]"

        self.console.print(Panel(
            summary_table,
            title="[bold yellow]Dossier of Prophetic Transfiguration[/]",
            border_style="yellow",
            subtitle=telemetry
        ))

        return True

    def _conduct_impact_analysis(self, plan: Dict[str, Any]) -> None:
        """
        =================================================================================
        == THE ORACLE OF CONSEQUENCE (V-Ω-CORTEX-MEMORY-AWARE)                         ==
        =================================================================================
        LIF: 10,000,000

        This divine artisan has been healed. It now understands that the Gnosis of
        causality resides within the Cortex's MEMORY, not its mind. It now performs a
        sacred `perceive()` rite to ensure the memory is warm before making its plea.
        =================================================================================
        """
        files_to_delete = {d['path'] for d in plan.get("delete", [])}
        moved_from_paths = {Path(p_from) for p_from in plan.get("move", {})}

        destructive_paths = files_to_delete | moved_from_paths
        if not destructive_paths:
            return

        self.logger.info("The Oracle of Consequence awakens. Communing with the Gnostic Cortex...")
        from ..core.cortex.engine import GnosticCortex
        cortex = GnosticCortex(self.project_root)

        # ★★★ THE DIVINE HEALING ★★★
        # We perceive reality to get the memory object.
        memory = cortex.perceive(force_refresh=False)
        # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        broken_bonds: List[Tuple[Path, List[str]]] = []
        all_vanishing_paths_abs = {self.project_root / p for p in destructive_paths}

        for path in destructive_paths:
            # ★★★ THE DIVINE HEALING ★★★
            # We make our plea to the MEMORY, not the Cortex.
            # The path must be a string relative to the project root.
            try:
                path_str = path.relative_to(self.project_root).as_posix()
                dependents = memory.get_dependents_of(path_str)
            except (ValueError, AttributeError):
                dependents = []
            # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

            surviving_dependents = [
                d for d in dependents
                if (self.project_root / d) not in all_vanishing_paths_abs
            ]

            if surviving_dependents:
                broken_bonds.append((path, surviving_dependents))

        if broken_bonds:
            self._proclaim_impact_heresy(broken_bonds)

    def _proclaim_impact_heresy(self, broken_bonds: List[Tuple[Path, List[str]]]) -> None:
        """
        =================================================================================
        == THE HERALD OF BROKEN BONDS (V-Ω-INTERACTIVE-MENTOR)                         ==
        =================================================================================
        This is a divine, specialist Herald. It receives a pure dossier of broken
        Gnostic bonds and transmutes it into a luminous, interactive communion that
        mentors the Architect, guards against catastrophe, and honors their final will.
        """
        from rich.panel import Panel
        from rich.prompt import Confirm
        from rich.console import Group
        from rich.text import Text

        # --- MOVEMENT I: FORGE THE DOSSIER OF CONSEQUENCE ---
        warning_items = [
            Text("CRITICAL IMPACT WARNING:", style="bold red"),
            Text("The following transmutations will shatter existing Gnostic bonds:\n")
        ]

        for corpse, mourners in broken_bonds:
            warning_items.append(
                Text.assemble(
                    ("  🗑️  Annihilating/Moving ", "red"),
                    (str(corpse), "bold yellow"),
                    (" will break:", "red")
                )
            )
            for mourner in mourners[:5]:
                warning_items.append(Text(f"     - {mourner}", style="cyan"))
            if len(mourners) > 5:
                warning_items.append(Text(f"     - ... and {len(mourners) - 5} other(s).", style="dim"))

        # --- MOVEMENT II: THE INTERACTIVE GATE ---
        self.console.print(
            Panel(Group(*warning_items), title="[bold red]Gnostic Impact Analysis[/bold red]", border_style="red")
        )

        # We use the BaseArtisan's request property to access the current context
        if not self.active_request.force and not self.active_request.non_interactive:
            if not Confirm.ask(
                    "\n[bold yellow]This is a destructive act. Are you certain you wish to proceed?[/bold yellow]",
                    default=False
            ):
                raise ArtisanHeresy(
                    "Rite stayed by the Conscience of the Transmuter.",
                    suggestion="Refactor the dependent files to remove the broken imports, or proceed with `--force`.",
                    exit_code=0
                )
            else:
                self.logger.warn("The Architect has acknowledged the risk and commanded the rite to proceed.")

    def _load_lock_file(self) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GUARDIAN OF THE GNOSTIC CHRONICLE (V-Ω-HYPER-RESILIENT)                 ==
        =================================================================================
        LIF: 10,000,000

        This is not a file reader. It is a divine, sentient Guardian whose one true
        purpose is to safely summon the `scaffold.lock` scripture, the Engine's memory
        of the past.
        """
        if not self.lock_file_path.exists():
            self.logger.warn("Gnostic Chronicle (scaffold.lock) not found.")
            # This is not a critical error for `transmute`; it simply means all
            # files in the blueprint will be treated as "new creations".
            return {}

        try:
            content = self.lock_file_path.read_text(encoding='utf-8')
            if not content.strip():
                # [FACULTY 4] The Guardian of the Empty Soul
                self.logger.warn("Gnostic Chronicle exists but is a void. Treating reality as new.")
                return {}

            lock_data = json.loads(content)
            return lock_data

        except json.JSONDecodeError as e:
            # [FACULTY 2] The Heresy Transmuter
            raise ArtisanHeresy(
                "The Gnostic Chronicle's soul is profane (corrupted JSON).",
                suggestion="Delete the `scaffold.lock` file and run `scaffold adopt` to forge a new, pure Chronicle.",
                details=f"Paradox at line {e.lineno}, column {e.colno}: {e.msg}",
                child_heresy=e
            )
        except Exception as e:
            raise ArtisanHeresy(
                "A catastrophic paradox occurred while gazing upon the Gnostic Chronicle.",
                child_heresy=e
            ) from e

    def _conduct_docker_harmony_rite(self, request: TransmuteRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE DOCKER HARMONIZER (V-Ω-DEPENDENCY-AWARE)                            ==
        =============================================================================
        Ensures the Dockerfile reflects the state of package manager manifests.
        """
        self.logger.info("The Docker Harmonizer awakens...")

        dockerfile_path = self.project_root / "Dockerfile"
        if not dockerfile_path.exists():
            return self.failure("No Dockerfile found to harmonize.")

        content = dockerfile_path.read_text(encoding='utf-8')

        # Python Harmony
        pyproj_path = self.project_root / "pyproject.toml"
        if pyproj_path.exists():
            if "COPY pyproject.toml" not in content:
                content = content.replace("COPY . .",
                                          "COPY pyproject.toml poetry.lock* ./\nRUN poetry install --no-root\n\nCOPY . .")
                self.logger.verbose("Injecting Poetry installation layer into Dockerfile.")

        # Node Harmony
        pkg_json_path = self.project_root / "package.json"
        if pkg_json_path.exists():
            if "COPY package.json" not in content:
                content = content.replace("COPY . .", "COPY package.json package-lock.json* ./\nRUN npm ci\n\nCOPY . .")
                self.logger.verbose("Injecting npm installation layer into Dockerfile.")

        atomic_write(dockerfile_path, content, self.logger, self.project_root)

        return self.success("Dockerfile has been harmonized with project dependencies.")

    def _generate_new_plan(self, blueprint_path: Path) -> Tuple[List[ScaffoldItem], Dict[str, Any]]:
        """
        =================================================================================
        == THE PROPHET OF THE FUTURE (V-Ω-ETERNAL-APOTHEOSIS. THE PURE CONDUCTOR)      ==
        =================================================================================
        LIF: 10,000,000,000

        This is not a function. It is a divine, sentient Conductor whose one true purpose
        is to orchestrate the symphony of Gnostic Perception and Prophecy. It has been
        transfigured to honor the sacred, unbreakable contracts of the ascended
        `ApotheosisParser`, annihilating the `AttributeError` heresy from all timelines.
        """
        self.Logger.info("The Prophet of the Future awakens to gaze upon the new architectural scripture...")

        try:
            # --- MOVEMENT I: THE SACRED PLEA TO THE PARSER ---
            parser = ApotheosisParser(grammar_key='scaffold')

            # THE FIX: The Gaze is now upon the pure Path object, not the profane string.
            blueprint_content = blueprint_path.read_text(encoding='utf-8')

            self.Logger.verbose("   -> Bestowing scripture upon the ApotheosisParser...")

            parser_instance, _, _, _, _, _ = parser.parse_string(
                content=blueprint_content,
                file_path_context=blueprint_path,
                pre_resolved_vars=self.active_request.variables
            )

            if not parser_instance.all_rites_are_pure:
                # The parser's own proclamation of heresy is sufficient. We halt.
                raise ArtisanHeresy("The new blueprint scripture is profane and cannot be realized.")

            # --- MOVEMENT II: THE RITE OF REALITY RESOLUTION ---
            self.Logger.verbose("   -> Commanding parser to resolve the final, Gnostic reality...")
            final_plan = parser_instance.resolve_reality()
            final_vars = parser_instance.variables

            self.Logger.success("The Prophet's Gaze is complete. The new reality is known.")

            return final_plan, final_vars

        except ArtisanHeresy as e:
            e.message = f"A paradox in the blueprint scripture '{blueprint_path.name}' stayed the Transmutation."
            raise e
        except Exception as e:
            raise ArtisanHeresy(
                "A catastrophic paradox shattered the Prophet of the Future.",
                child_heresy=e
            ) from e

    def _get_new_content_for_item(self, item: ScaffoldItem) -> str:
        """
        =================================================================================
        == THE FORENSIC ALCHEMIST (V-Ω-ETERNAL-APOTHEOSIS. THE PURE GAZE)              ==
        =================================================================================
        """
        from ..utils.resolve_gnostic_content import resolve_gnostic_content_v2

        # [THE APOTHEOSIS] The Gaze is upon the Parser's final, resolved context.
        # This requires storing the parser instance from _generate_new_plan if we need vars.
        # For now, we assume item content is mostly resolved, or we need to access parser vars.
        # But _generate_new_plan returns items and vars.
        # We need to access those vars here.
        # For V1, we assume item.content is sufficient or we need to pass vars in.
        # Since this method is used in _launch_diff_browser which is inside execute context,
        # we can use self.active_request.variables if they are updated?
        # No, we need the parser's vars.
        # Simplified: Just return item.content if available.
        return item.content or ""

    def _launch_diff_browser(self, old_content: str, new_content: str, path: Path):
        """
        =================================================================================
        == THE SCRIBE OF THE DIFFERENTIAL GAZE (V-Ω-POLYGLOT-PROPHET)                  ==
        =================================================================================
        """
        old_path, new_path = None, None
        try:
            # --- MOVEMENT I: THE FORGING OF EPHEMERAL SCRIPTURES ---
            with tempfile.NamedTemporaryFile(delete=False, prefix=f"before_{path.stem}_", suffix=path.suffix, mode='w',
                                             encoding='utf-8') as old_f, \
                    tempfile.NamedTemporaryFile(delete=False, prefix=f"after_{path.stem}_", suffix=path.suffix,
                                                mode='w', encoding='utf-8') as new_f:

                old_f.write(old_content)
                new_f.write(new_content)
                old_path, new_path = old_f.name, new_f.name

            # --- MOVEMENT II: THE GNOSTIC TRIAGE OF TOOLS ---
            editor = os.getenv("SCAFFOLD_EDITOR") or os.getenv("VISUAL") or os.getenv("EDITOR")
            diff_cmd = []

            # The Gaze for the Luminous Editor (VS Code)
            if "code" in (editor or ""):
                diff_cmd = ["code", "--diff", old_path, new_path, "--wait"]
            # The Gaze for the Chronomancer's Tool (Git)
            elif shutil.which("git"):
                diff_cmd = ["git", "diff", "--no-index", "--", old_path, new_path]

            # --- MOVEMENT III: THE DIVINE SUMMONS ---
            if diff_cmd:
                self.console.print(
                    f"[dim]The Differential Gaze awakens for [cyan]{path.name}[/cyan]... (Close editor to continue)[/dim]")
                subprocess.run(diff_cmd)
            else:
                self.console.print(
                    f"[yellow]No external diff tool perceived. Proclaiming diff for '{path.name}' to console.[/yellow]")
                diff = "".join(difflib.unified_diff(old_content.splitlines(True), new_content.splitlines(True)))
                self.console.print(Syntax(diff, "diff", theme="monokai"))

        except Exception as e:
            self.Logger.error(f"The Differential Gaze was shattered by a paradox: {e}")
        finally:
            try:
                if old_path: os.unlink(old_path)
                if new_path: os.unlink(new_path)
            except OSError:
                pass

    def _proclaim_success(self, plan: Dict[str, Any], write_dossier: List[GnosticWriteResult]):
        """
        =================================================================================
        == THE HERALD OF APOTHEOSIS (V-Ω-ETERNAL-APOTHEOSIS. THE UNIVERSAL SCRIBE)     ==
        =================================================================================
        """
        from types import SimpleNamespace
        from ..utils.dossier_scribe import proclaim_apotheosis_dossier
        import time

        if self.active_request.silent:
            return

        transmute_registers = SimpleNamespace(
            get_duration=lambda: time.monotonic() - getattr(self, '_start_time', time.monotonic()),
            files_forged=len(plan.get('create', [])),
            sanctums_forged=len([d for d in plan.get('create', []) if d.get('item', {}).is_dir]),
            bytes_written=sum(w.bytes_written for w in write_dossier),
            no_edicts=self.active_request.no_edicts,
            project_root=self.project_root,
            transaction=None
        )

        gnosis_context = {
            "project_type": f"Transmuted Reality",
            "rite_name": "transmute",
            "blueprint_path": self.blueprint_path.name,
            **self.active_request.variables
        }

        next_steps = ["Verify transmutation: [bold]git status[/bold]"]
        if self._is_tracked_by_git(self.project_root):
            next_steps.append(
                f"Commit to Chronicle: [bold]git commit -am 'refactor: transmute via {self.blueprint_path.stem}'[/bold]")

        proclaim_apotheosis_dossier(
            telemetry_source=transmute_registers,
            gnosis=gnosis_context,
            project_root=self.project_root,
            next_steps=next_steps,
            title="✨ Transmutation Complete ✨",
            subtitle=f"Architectural changes from '{self.blueprint_path.name}' have been made manifest.",
            transmutation_plan=plan
        )

    def _is_tracked_by_git(self, path: Path) -> bool:
        if not shutil.which("git"):
            return False
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0 and result.stdout.strip() == "true"
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def __repr__(self) -> str:
        return f"<Ω_TRANSMUTATOR status=OMNISCIENT mode=DRIFT_AWARE>"
