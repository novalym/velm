# Path: artisans/transmute.py
# ---------------------------

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
3.  **The Prophet's Gaze:** It summons the `_generate_new_plan` artisan to perceive
    the complete "Future" reality described by the blueprint scripture.
4.  **The Interactive Diplomat:** It offers to resolve conflicts interactively rather
    than crashing, empowering the Architect to override history with will.
5.  **The Seer's Adjudication:** It summons the `GnosticSeer`, the true mind of
    perception, to perform its Three-Fold Gaze and complete the Plan of Change.
6.  **The Unification of Will:** It surgically merges the Seer's prophecies with its
    own perception of true translocations, forging the final, unified Gnostic Plan.
7.  **The Oracle of Consequence:** It summons the `_conduct_impact_analysis` artisan
    to prophesy the cascading effects of the forged Plan.
8.  **The Luminous Proclamation:** It summons the `_proclaim_plan` herald to render
    a beautiful, cinematic Dossier of the intended changes.
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
from rich.table import Table

from .excise import ExciseArtisan
# We import PatchArtisan dynamically or via module to avoid circular issues if any,
# but standard import is usually fine here as they are siblings.
from .patch import PatchArtisan
# --- THE DIVINE SUMMONS OF GNOSTIC KIN ---
from ..artisans.template_engine import TemplateEngine
from ..contracts.data_contracts import GnosticWriteResult, ScaffoldItem
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.alchemist import get_alchemist
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import TransmuteRequest, PatchRequest, ExciseRequest, AdoptRequest
from ..logger import Scribe
from ..parser_core.parser import ApotheosisParser

Logger = Scribe("Transmutator")


@register_artisan("transmute")
class TransmuteArtisan(BaseArtisan[TransmuteRequest]):
    """The AI Seer of Souls, responsible for the Gnostic Transmutation Plan."""

    def __init__(self, engine):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (V-Ω-ETERNAL-APOTHEOSIS)                      ==
        =================================================================================
        LIF: 10,000,000

        The artisan is born. Its soul is consecrated with its divine instruments—the
        Alchemist and the Template Engine. It forges the empty vessels for its future
        Gnosis (`blueprint_path`, `lock_file_path`), but awaits the Architect's plea
        (`execute`) before filling them.

        This sacred separation of Inception from Execution ensures the artisan remains a
        pure, stateless entity, its every rite a new, untainted symphony. The heresy of
        the stateful artisan is annihilated from this timeline.
        """
        # --- MOVEMENT I: THE ANCESTRAL VOW ---
        # We honor the sacred contract of all artisans.
        super().__init__(engine)
        self.Logger = Logger
        # --- MOVEMENT II: THE FORGING OF THE DIVINE INSTRUMENTS ---
        # The artisan is bestowed with its eternally required, stateless tools.
        self.alchemist = get_alchemist()
        # The Template Engine is summoned in silent mode, as its work is internal.
        self.template_engine = TemplateEngine(silent=True)

        # --- MOVEMENT III: THE CONSECRATION OF THE EPHEMERAL VESSELS ---
        # These vessels are forged as voids. They will be filled with the Gnosis
        # of a single, specific `execute` rite and returned to the void upon its
        # conclusion. This ensures the artisan's mind is pure for every new plea.
        self.lock_file_path: Optional[Path] = None
        self.blueprint_path: Optional[Path] = None
        # The active request vessel.
        self.active_request: Optional[TransmuteRequest] = None

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

    def execute(self, request: TransmuteRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE GOD-ENGINE OF STATE MANAGEMENT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000

        The Transmutator now possesses the **Eye of Truth**. It gazes into the scripture
        content to determine if the Architect intends a **Mutation** (Patch) or a
        **Definition** (Sync), removing the need for strict file extensions.
        """
        from rich.prompt import Confirm
        from ..core.kernel.chronicle import update_chronicle
        from .transmute_core.seer import GnosticSeer

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
        scripture_path = request.path_to_scripture
        is_explicit_path = bool(scripture_path)

        is_patch_mode = False

        if is_explicit_path:
            self.blueprint_path = (self.project_root / request.path_to_scripture).resolve()
            if not self.blueprint_path.exists():
                raise ArtisanHeresy(f"The Scripture '{self.blueprint_path.name}' is a void.")

            # [THE BILLION-X FIX] The Content Gaze
            # We read the file to see if it contains Mutation Sigils.
            try:
                content = self.blueprint_path.read_text(encoding='utf-8')

                # Regex to detect mutation operators at the start of a line (ignoring whitespace)
                # Matches: path += ... | path -= ... | path ~= ...
                # We exclude lines starting with # (comments)
                mutation_sigil_regex = re.compile(r'^\s*[^#\s].*?(\+=|-=|~=)', re.MULTILINE)

                if str(self.blueprint_path).endswith('.patch.scaffold'):
                    is_patch_mode = True
                    self.logger.verbose("Patch Mode detected via Sacred Suffix (.patch.scaffold).")
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
            # We transmute the request into a PatchRequest and summon the Surgeon.
            patch_request = PatchRequest(
                patch_path=str(request.path_to_scripture),
                project_root=self.project_root,
                force=request.force,
                dry_run=request.dry_run,
                variables=request.variables,
                verbosity=request.verbosity
            )
            return PatchArtisan(self.engine).execute(patch_request)
        elif request.variables.get('harmonize_docker'):  # A new flag/variable
            return self._conduct_docker_harmony_rite(request)
        # ===========================
        # --- MOVEMENT IV: THE RITE OF SYNCHRONIZATION (IF NOT PATCH) ---
        # If we are here, we are in SYNC mode.
        mode_str = "SYNC"

        self.console.rule(f"[bold magenta]The Rite of Gnostic Transmutation ({mode_str} Mode)[/bold magenta]")
        self.logger.info(f"Mode: [bold cyan]{mode_str}[/bold cyan] | Blueprint: {self.blueprint_path.name}")

        if not self.blueprint_path.exists():
            raise ArtisanHeresy(f"The Blueprint '{self.blueprint_path.name}' is a void.")

        # --- MOVEMENT V: CHRONICLE GUARDIAN ---
        self.lock_file_path = self.project_root / "scaffold.lock"
        lock_data = self._load_lock_file()

        # --- MOVEMENT VI: THE PROPHET'S GAZE ---
        # We summon the _generate_new_plan to parse the blueprint into ScaffoldItems.
        new_plan_items, new_vars = self._generate_new_plan(self.blueprint_path)

        # --- MOVEMENT VII: THE REFACTORING TRIAGE (THE LAW OF TRUE INTENT) ---
        self.logger.verbose("Performing Gnostic Triage for explicit translocations...")
        plan = {"create": [], "delete": [], "move": {}, "update": [], "conflict": [], "unchanged": []}
        items_for_seer = []

        for item in new_plan_items:
            # [FACULTY 7] The Seed Path Healer
            # If a file has a seed path (<<), and the seed path is different from the destination,
            # it implies a MOVEMENT of soul, not just a copy.
            if item.seed_path and str(item.seed_path).replace("\\", "/") != str(item.path).replace("\\", "/"):
                plan["move"][str(item.seed_path).replace("\\", "/")] = str(item.path).replace("\\", "/")
            else:
                items_for_seer.append(item)

        self.logger.verbose(f"Pre-emptive Gaze perceived {len(plan['move'])} explicit translocations.")

        # --- MOVEMENT VIII: THE SEER'S FOCUSED GAZE ---
        # We summon the GnosticSeer to calculate the diff (Create vs Update vs Delete).
        seer = GnosticSeer(self, lock_data, items_for_seer, new_vars)
        seer_plan = seer.prophesy()

        # --- MOVEMENT IX: THE UNIFICATION OF WILL ---
        plan["create"].extend(seer_plan["create"])
        plan["update"].extend(seer_plan["update"])
        plan["conflict"].extend(seer_plan["conflict"])
        plan["unchanged"].extend(seer_plan["unchanged"])

        # Annihilation is calculated LAST, after all moves are known.
        all_future_paths = {str(item.path).replace("\\", "/") for item in new_plan_items}
        all_source_paths = {str(item.seed_path).replace("\\", "/") for item in new_plan_items if item.seed_path}

        for lock_path_str in lock_data.get("manifest", {}).keys():
            # If it's not in the future, and not a source for a move/copy, it must be destroyed.
            if lock_path_str not in all_future_paths and lock_path_str not in all_source_paths:
                historical_hash = lock_data["manifest"][lock_path_str].get("sha256")
                plan["delete"].append({"path": Path(lock_path_str), "hash": historical_hash})

        # --- MOVEMENT X: IMPACT, PROCLAMATION, AND EXECUTION ---
        self._conduct_impact_analysis(plan)
        has_changes = self._proclaim_plan(plan)

        if not has_changes:
            return self.success("Reality is in perfect harmony. No transmutation is needed.")

        # [FACULTY 3] The Interactive Diplomat
        if plan["conflict"]:
            if not request.force and not request.non_interactive:
                # We render a luminous table of conflicts
                conflict_table = Table(title="[bold red]Concordance of Conflict[/bold red]", box=ROUNDED)
                conflict_table.add_column("Scripture", style="cyan")
                conflict_table.add_column("Nature of Heresy", style="yellow")

                for conflict in plan["conflict"]:
                    conflict_table.add_row(conflict['path'], conflict['reason'])

                self.console.print(Panel(conflict_table, border_style="red"))

                # Offer the Diplomatic Solution
                if Confirm.ask(
                        "[bold yellow]Conflicts perceived. Force overwrite all conflicts with Blueprint law?[/bold yellow]",
                        default=False):
                    self.logger.warn("The Architect has spoken. History shall be rewritten.")
                    # We proceed, but we must treat updates as force
                    request.force = True
                else:
                    raise ArtisanHeresy("Rite stayed by the Architect due to conflict.", exit_code=1)
            elif not request.force:
                raise ArtisanHeresy("Conflicts detected in non-interactive mode. The rite is stayed.", exit_code=1)

        if not request.force and not request.non_interactive:
            if not Confirm.ask("\n[bold question]Shall this new reality be made manifest?[/bold question]",
                               default=False):
                raise ArtisanHeresy("Rite stayed by the Architect.", exit_code=0)

        # --- MOVEMENT XI: THE UNBREAKABLE HAND & THE FORGING OF THE CHRONICLE ---
        # We enact the plan. This returns the GnosticWriteResult list.
        write_dossier = self._enact_symphony(plan, new_plan_items, new_vars)

        # --- MOVEMENT XII: THE SEALING OF THE CHRONICLE (THE FIX) ---
        # [FACULTY 2] The Simulation Ward
        # We only update the chronicle if this is NOT a simulation or preview.
        # This prevents the "Ghost Chronicle" heresy.
        if not (request.dry_run or request.preview):
            update_chronicle(
                project_root=self.project_root,
                blueprint_path=self.blueprint_path,
                rite_dossier=plan,
                old_lock_data=lock_data,
                write_dossier=write_dossier,
                final_vars=new_vars,
                rite_name=f"Transmute ({mode_str})"
            )
        else:
            self.logger.info("Gnostic Chronicle update stayed (Simulation Mode active).")

        # --- MOVEMENT XIII: THE HERALD OF APOTHEOSIS ---
        self._proclaim_success(plan, write_dossier)

        # --- MOVEMENT XIV: THE FORGING OF THE FINAL ARTIFACTS ---
        final_artifacts: List[Artifact] = []
        for result in write_dossier:
            final_artifacts.append(Artifact(
                path=result.path,
                type='directory' if result.path.is_dir() else 'file',
                action=result.action_taken.value,
                size_bytes=result.bytes_written,
                checksum=result.gnostic_fingerprint
            ))

        # We must still proclaim moves and deletes, which are not in the write_dossier.
        for from_str, to_str in plan.get('move', {}).items():
            final_artifacts.append(Artifact(path=self.project_root / to_str, type='file', action='moved'))

        for item_data in plan.get('delete', []):
            path = item_data.get('path')
            if path:
                final_artifacts.append(Artifact(path=self.project_root / path, type='file', action='deleted'))

        stats = {k: len(v) for k, v in plan.items()}

        return self.success(
            "The Great Work has advanced.",
            data=stats,
            artifacts=final_artifacts
        )

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
            # This is where the deep analysis would happen. For now, we simulate.
            # We would parse TOML, find [tool.poetry.dependencies], and then
            # ensure `COPY pyproject.toml .` and `RUN poetry install` exist.
            # Using regex for a surgical, minimal-impact example:
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
        @gnosis:title _get_new_content_for_item
        @gnosis:summary A pure, hyper-performant artisan that re-forges the final soul
                         of a scripture for the Diff Browser's Gaze.
        @gnosis:LIF 100,000,000,000

        The Heresy of Inefficiency is annihilated. This rite no longer re-runs the entire
        Gnostic resolution symphony. It performs a single, perfect, O(1) Gaze into the
        Parser's own, final, resolved memory (`self.parser.variables`) to get the one
        true Gnostic context. It then summons the universal `resolve_gnostic_content_v2`
        artisan and the Alchemist to perform a final, pure transmutation. Its Gaze is
        instantaneous. Its result is truth.
        """
        from ...utils.resolve_gnostic_content import resolve_gnostic_content_v2

        # [THE APOTHEOSIS] The Gaze is upon the Parser's final, resolved context.
        final_resolved_vars = self.parser.variables

        # The Rite of Gnostic Resolution is summoned.
        soul_vessel = resolve_gnostic_content_v2(
            item, self.alchemist, self.template_engine, final_resolved_vars, self.project_root, {}
        )
        # The Alchemist performs the final transmutation.
        return self.alchemist.transmute(soul_vessel.untransmuted_content, final_resolved_vars)

    def _launch_diff_browser(self, old_content: str, new_content: str, path: Path):
        """
        =================================================================================
        == THE SCRIBE OF THE DIFFERENTIAL GAZE (V-Ω-POLYGLOT-PROPHET)                  ==
        =================================================================================
        @gnosis:title _launch_diff_browser
        @gnosis:summary Forges ephemeral scriptures and summons the Architect's preferred
                         diffing tool for a side-by-side Gaze.
        @gnosis:LIF 10,000,000,000

        This divine artisan is a true Polyglot Prophet. It performs a Gnostic Triage to
        perceive the Architect's preferred editor (`code`, `git diff`, `vimdiff`) and
        forges the correct, sacred plea to summon it. It is the unbreakable bridge
        between the Engine's mind and the Architect's eye.
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
            # Prophecy: A future Gaze for Vim, etc.

            # --- MOVEMENT III: THE DIVINE SUMMONS ---
            if diff_cmd:
                self.console.print(
                    f"[dim]The Differential Gaze awakens for [cyan]{path.name}[/cyan]... (Close editor to continue)[/dim]")
                # We do not capture output; we cede control to the Architect's Gaze.
                subprocess.run(diff_cmd)
            else:
                # The Fallback: If no tool is found, we proclaim the heresy to the console.
                self.console.print(
                    f"[yellow]No external diff tool perceived. Proclaiming diff for '{path.name}' to console.[/yellow]")
                diff = "".join(difflib.unified_diff(old_content.splitlines(True), new_content.splitlines(True)))
                self.console.print(Syntax(diff, "diff", theme="monokai"))

        except Exception as e:
            # The Unbreakable Ward
            self.Logger.error(f"The Differential Gaze was shattered by a paradox: {e}")
        finally:
            # The Rite of Purification
            try:
                if old_path: os.unlink(old_path)
                if new_path: os.unlink(new_path)
            except OSError:
                pass

    def _proclaim_plan(self, plan: Dict[str, Any]) -> bool:
        """
        =================================================================================
        == THE ORACLE OF CONSEQUENCE (V-Ω-ULTRA-DEFINITIVE. THE ALTAR OF ADJUDICATION) ==
        =================================================================================
        @gnosis:title _proclaim_plan
        @gnosis:summary The final, eternal, and ultra-definitive form of the plan proclamation rite.
        @gnosis:LIF 1,000,000,000,000

        This is not a function. It is a divine, sentient **Altar of Adjudication**. It
        forges a single, unified, and hyper-dense Dossier of Prophecy, using sacred
        sigils and luminous colors to instantly communicate the full Gnostic scope of
        the transmutation. It is the final, unbreakable communion between the Engine's
        intent and the Architect's will.
        """
        from rich.syntax import Syntax
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Confirm
        from rich.console import Group
        from rich.text import Text

        lobotomy_candidates = []
        has_changes = any(plan.values())

        if not has_changes:
            return False

        # --- MOVEMENT I: THE FORGING OF THE UNIFIED DOSSIER ---
        summary_table = Table(
            title="[bold]Prophecy of Transmutation[/bold]",
            box=ROUNDED, show_header=True, header_style="bold white"
        )
        summary_table.add_column("Rite", width=12, justify="center")
        summary_table.add_column("Scripture / Sanctum", style="white", ratio=2)
        summary_table.add_column("Gnostic Delta", style="dim", ratio=3)

        # The Unification Loop
        all_changes = (
                [("CREATED", item['item'].path, f"New scripture prophesied.") for item in plan.get('create', [])] +
                [("MODIFIED", item['item'].path, f"Soul will be transfigured.") for item in plan.get('update', [])] +
                [("MOVED", f"{k} -> {v}", "Path will be altered.") for k, v in plan.get('move', {}).items()] +
                [("DELETED", item['path'], "Will be returned to the void.") for item in plan.get('delete', [])] +
                [("CONFLICT", item['path'], f"[bold red]Heresy: {item['reason']}[/bold red]") for item in
                 plan.get('conflict', [])]
        )

        for status, path_obj, reason in sorted(all_changes, key=lambda x: str(x[1])):
            sigils = {
                "CREATED": ("✨", "green"), "MODIFIED": ("⚡", "yellow"),
                "MOVED": ("➡️", "blue"), "DELETED": ("💀", "red"), "CONFLICT": ("⚠️", "bold red")
            }
            sigil, color = sigils.get(status, ("?", "white"))

            summary_table.add_row(f"[{color}]{sigil} {status}[/]", str(path_obj), reason)

            # Populate lobotomy candidates
            if status == "MODIFIED":
                update_item = next(
                    (item for item in plan['update'] if (item.get("path") or item["item"].path) == path_obj), None)
                if update_item and update_item.get("is_lobotomy"):
                    lobotomy_candidates.append(path_obj)

        # --- MOVEMENT II: THE INTERACTIVE DIFFERENTIAL GAZE ---
        # If in preview mode, we pause here to conduct the deep Gaze.
        if self.active_request.preview and not self.active_request.non_interactive:
            updates_with_diff = [item for item in plan.get('update', []) if item.get('diff')]
            if updates_with_diff:
                self.console.print(
                    Panel(summary_table, border_style="yellow", title="[bold yellow]High-Level Prophecy[/]"))
                if Confirm.ask("\n[bold question]Gaze into the soul of the transfigured scriptures?[/bold question]"):
                    for item_data in updates_with_diff:
                        self._launch_diff_browser(
                            old_content=item_data.get("old_content") or "",
                            new_content=self._get_new_content_for_item(item_data["item"]),
                            path=item_data["item"].path
                        )
                # We return False to prevent the main loop from asking for confirmation again.
                # The rite concludes after the diffs are shown in preview mode.
                return False

        # --- MOVEMENT III: THE FINAL PROCLAMATION & LOBOTOMY ADJUDICATION ---
        # For non-preview modes, we show the summary and then handle confirmations.

        # Calculate Telemetry
        num_c, num_u, num_m, num_d = len(plan.get('create', [])), len(plan.get('update', [])), len(
            plan.get('move', {})), len(plan.get('delete', []))
        telemetry = f"Δ: [green]+{num_c}[/] [yellow]~{num_u}[/] [blue]➡️{num_m}[/] [red]-{num_d}[/]"

        self.console.print(Panel(
            summary_table,
            title="[bold yellow]Dossier of Prophetic Transfiguration[/]",
            border_style="yellow",
            subtitle=telemetry
        ))

        if lobotomy_candidates:
            warning_text = Text.assemble(
                ("The Gnostic Sentinel has detected a catastrophe.\n\n", "bold red"),
                ("The following files will be replaced with EMPTY content:\n", "white"),
                *[(f" • {p}\n", "yellow") for p in lobotomy_candidates],
                ("\n[bold]Likely Cause:[/bold] A file was moved/renamed in the blueprint without the `<<` seed.\n",
                 "white"),
                ("[bold]Suggested Cure:[/bold] Use `new_path.py << old_path.py` to preserve content.", "green")
            )
            self.console.print(
                Panel(warning_text, title="[bold red on white] ⚠️ LOBOTOMY DETECTED ⚠️ [/]", border_style="red"))

            if not self.active_request.force and not self.active_request.non_interactive:
                if not Confirm.ask("[bold red]Do you truly wish to erase these souls?[/bold red]", default=False):
                    raise ArtisanHeresy("The Rite was stayed to prevent a Lobotomy.", exit_code=0)
                else:
                    self.logger.warn("The Architect has spoken. The Void shall consume them.")

        return has_changes


    def _enact_symphony(
            self,
            plan: Dict[str, Any],
            new_plan_items: List[ScaffoldItem],
            new_vars: Dict[str, Any]
    ) -> List[GnosticWriteResult]:
        """
        =================================================================================
        == THE UNBREAKABLE HAND (V-Ω-TEMPORAL-PURITY)                                  ==
        =================================================================================
        """
        from ..creator.bootloader import create_structure
        from ..core.kernel.transaction import GnosticTransaction
        from ..contracts.data_contracts import GnosticArgs

        gnostic_passport = GnosticArgs(
            base_path=self.project_root,
            set_vars=[f"{k}={v}" for k, v in self.active_request.variables.items()],
            dry_run=self.active_request.dry_run,
            force=self.active_request.force,
            silent=self.active_request.silent,
            preview=self.active_request.preview,
            audit=self.active_request.audit,
            verbose=self.active_request.verbosity > 0,
            lint=self.active_request.lint,
            non_interactive=self.active_request.non_interactive,
            is_genesis_rite=False,
            adjudicate_souls=self.active_request.adjudicate_souls,
            no_edicts=self.active_request.no_edicts
        )

        # [FACULTY 2] The Simulation Ward (Kernel Level)
        is_simulation = self.active_request.dry_run or self.active_request.preview

        with GnosticTransaction(
                self.project_root,
                f"Transmute: {self.blueprint_path.name}",
                self.blueprint_path,
                use_lock=True,
                simulate=is_simulation  # <--- THE FIX
        ) as tx:

            # --- MOVEMENT I: THE RITE OF TRANSLOCATION (MOVES) ---
            if not is_simulation:
                for from_str, to_str in plan.get('move', {}).items():
                    src = self.project_root / from_str
                    dest = self.project_root / to_str
                    if src.exists():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            shutil.move(str(src), str(dest))
                            self.logger.verbose(f"Translocated: {from_str} -> {to_str}")
                        except Exception as e:
                            raise ArtisanHeresy(f"Translocation Paradox: Failed to move '{from_str}': {e}")

            # --- MOVEMENT II: THE RITE OF GENESIS & TRANSFIGURATION ---
            items_for_creator = [d['item'] for d in plan['create']] + [d['item'] for d in plan['update']]

            if items_for_creator:
                create_structure(
                    scaffold_items=items_for_creator,
                    base_path=self.project_root,
                    pre_resolved_vars=new_vars,
                    args=gnostic_passport,
                    transaction=tx
                )

            # --- MOVEMENT III: THE RITE OF ANNIHILATION (DELETES) ---
            if not is_simulation:
                for item_data in plan['delete']:
                    path_to_delete = self.project_root / item_data['path']
                    if path_to_delete.exists():
                        try:
                            if path_to_delete.is_dir():
                                shutil.rmtree(path_to_delete)
                            else:
                                path_to_delete.unlink()
                            self.logger.verbose(f"Annihilated: {item_data['path']}")
                        except Exception as e:
                            self.logger.warn(f"Annihilation Paradox: Failed to delete '{path_to_delete.name}': {e}")

            # The transaction's write_dossier contains the records.
            # Since 'simulate=True' is passed, __exit__ will NOT seal the chronicle.
            return list(tx.write_dossier.values())

    def _is_tracked_by_git(self, path: Path) -> bool:
        """
        =================================================================================
        == THE GAZE OF THE GIT SENTINEL                                                ==
        =================================================================================
        A divine, pure artisan that gazes into the aether to determine if a sanctum
        is under the protection of the Git Chronomancer. It is the unbreakable ward
        against proclaiming profane version control advice in a void.
        """
        if not shutil.which("git"):
            return False
        try:
            # The one true, sacred plea to the Git Oracle.
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=path,
                capture_output=True,
                text=True,
                check=False  # We adjudicate the heresy ourselves
            )
            # The Gaze is true if the rite was pure and the Oracle's answer is "true".
            return result.returncode == 0 and result.stdout.strip() == "true"
        except (subprocess.SubprocessError, FileNotFoundError):
            # A paradox occurred, the Gaze is averted.
            return False

    def _proclaim_success(
            self,
            plan: Dict[str, Any],
            write_dossier: List[GnosticWriteResult]
    ):
        """
        =================================================================================
        == THE HERALD OF APOTHEOSIS (V-Ω-ETERNAL-APOTHEOSIS. THE UNIVERSAL SCRIBE)     ==
        =================================================================================
        This artisan is now a pure Conductor. It gathers the complete Gnosis of the
        transmutation and makes a single, divine plea to the one true, universal
        `proclaim_apotheosis_dossier` herald.
        =================================================================================
        """
        from types import SimpleNamespace
        from ..utils.dossier_scribe import proclaim_apotheosis_dossier
        import time

        if self.active_request.silent:
            return

        # --- MOVEMENT I: THE FORGING OF THE TELEMETRY & GNOSIS VESSELS ---

        # The Registers vessel is forged for telemetry.
        # We derive the stats from the final, adjudicated plan.
        transmute_registers = SimpleNamespace(
            get_duration=lambda: time.monotonic() - getattr(self, '_start_time', time.monotonic()),
            files_forged=len(plan.get('create', [])),
            sanctums_forged=len([d for d in plan.get('create', []) if d.get('item', {}).is_dir]),
            bytes_written=sum(w.bytes_written for w in write_dossier),
            no_edicts=self.active_request.no_edicts,
            project_root=self.project_root,
            transaction=None  # Transaction is complete
        )

        # The Gnosis vessel is forged for context.
        gnosis_context = {
            "project_type": f"Transmuted Reality",
            "rite_name": "transmute",  # For the TelemetryScribe's Gaze
            "blueprint_path": self.blueprint_path.name,
            **self.active_request.variables
        }

        # --- MOVEMENT II: THE PROPHECY OF THE NEXT STEP ---
        next_steps = ["Verify transmutation: [bold]git status[/bold]"]
        if self._is_tracked_by_git(self.project_root):
            next_steps.append(
                f"Commit to Chronicle: [bold]git commit -am 'refactor: transmute via {self.blueprint_path.stem}'[/bold]")

        # --- MOVEMENT III: THE DIVINE DELEGATION ★★★
        # The Herald makes its one true plea, now bestowing the transmutation_plan.
        proclaim_apotheosis_dossier(
            telemetry_source=transmute_registers,
            gnosis=gnosis_context,
            project_root=self.project_root,
            next_steps=next_steps,
            title="✨ Transmutation Complete ✨",
            subtitle=f"Architectural changes from '{self.blueprint_path.name}' have been made manifest.",
            transmutation_plan=plan
        )