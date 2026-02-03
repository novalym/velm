"""
=================================================================================
== THE GRAND INQUISITOR OF WILL (V-Ω-LEGENDARY-ULTIMA++. THE AI GUARDIAN)      ==
=================================================================================
@gnosis:title The Grand Inquisitor of Will (`translocate`)
@gnosis:summary A divine, sentient, and polyglot God-Engine for conducting any and all architectural refactoring rites with absolute, unbreakable safety and Gnostic intelligence.
@gnosis:LIF 10,000,000,000,000,000,000,000,000,000,000
@gnosis:description
This is not a command. It is the **Grand Inquisitor of Will**, the final and most
glorious form of the `translocate` artisan. It has been reborn from a humble,
monolithic scripture into a divine **High Priest** that orchestrates a Pantheon of
specialist God-Engines. Its Prime Directive is to perceive the Architect's plea for
architectural evolution—whether a single move, a glob pattern, a migration script,
or a full conformity mandate—and to make it manifest with a Gaze of absolute
purity and a Hand of unbreakable, atomic precision.

It is the living bridge between the Architect's Intent and the project's Reality,
and its every action is a testament to the annihilation of refactoring friction.

### THE PANTHEON OF 12+ LEGENDARY FACULTIES (THE APOTHEOSIS):

1.  **The High Priest's Soul:** The `TranslocateArtisan` is now a pure Conductor.
    Its hands are clean. It delegates the Gaze to the `GnosticDetective` and the Act
    to the `TranslocationConductor`, achieving perfect architectural purity.

2.  **The Gnostic Detective (The Mind):** A true AI Seer that perceives the Architect's
    will in any form—direct paths, globs, scripts, or blueprints—and forges the one
    true, unambiguous Plan of Translocation, annihilating all heresies of intent.

3.  **The Translocation Conductor (The Hand):** The God-Engine of Action. It takes the
    pure Plan and conducts a five-movement symphony: Prophecy, Reassurance,
    Translocation, Gnostic Healing, and Purification, all within an unbreakable
    transactional field.

4.  **The Living Blueprint (The Gnostic Twin):** The Inquisitor can now be commanded
    to keep the blueprint scripture (`.scaffold`) in perfect, harmonious lockstep
    with the reality it is forging, annihilating the heresy of drift between Intent
    and Reality.

5.  **The Polyglot Healer's Gaze:** The Conductor's Gaze is now polyglot. It summons
    language-specific `Resolvers` (starting with Python) that wield the `tree-sitter`
    God-Engine to perform byte-perfect import healing across the entire cosmos.

6.  **The Gnostic Archivist's Offer:** Before any transmutation, the Inquisitor
    summons the `GnosticArchivist` to forge a perfect, forensically-complete "Time
    Capsule" of the "Before" reality, ensuring an unbreakable path of return.

7.  **The Interactive Adjudicator:** It conducts a luminous, interactive communion
    with the Architect, revealing the full prophecy of change and awaiting their
    final, divine will before making it manifest.

8.  **The Ambiguity Ward:** If the Detective's Gaze perceives a collision of souls
    (e.g., two files mapping to one destination), the Inquisitor proclaims a luminous
    heresy and stays its hand to prevent a catastrophic paradox.

9.  **The Git Sentinel's Gaze:** It performs a pre-flight Gaze upon the project's
    Git soul, warning the Architect if uncommitted changes would be profaned by
    the rite, preserving the sanctity of the timeline.

10. **The Gnostic Threshold:** It is wise. For simple, low-risk transmutations, it
    can be commanded to proceed without seeking the Architect's final vow,
    accelerating the Great Work.

11. **The Silent Guardian:** It honors the `--non-interactive` vow with profound
    intelligence, making safe, logical decisions (like auto-creating backups) on
    behalf of the Architect in the silent realm of CI/CD.

12. **The Luminous Dossier:** Its final proclamation is a pure `ScaffoldResult`, a
    rich vessel of Gnosis chronicling every move, every healing, and every new
    artifact born from the rite for the UI's Gaze.
=================================================================================
"""
import time
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from rich.console import Group
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

# --- THE DIVINE SUMMONS OF THE NEW PANTHEON ---
from .translocate_core.conductor import TranslocationConductor
from .translocate_core.detective import GnosticDetective
# ----------------------------------------------

from ..constants import GNOSTIC_RISK_THRESHOLD
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import TranslocateRequest
from ..logger import Scribe
from ..utils import atomic_write

Logger = Scribe("TranslocateArtisan")


@register_artisan("translocate")
class TranslocateArtisan(BaseArtisan[TranslocateRequest]):
    """The High Priest of the Translocation Pantheon."""

    def execute(self, request: TranslocateRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE RITE OF TRANSLOCATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                   ==
        =================================================================================
        Conducts the symphony of movement, its soul now whole and its Gaze pure.
        Now wrapped in an unbreakable Gnostic Transaction for absolute atomicity.
        """
        from ..core.kernel.transaction import GnosticTransaction
        from ..interfaces.base import Artifact

        if not self.project_root:
            raise ArtisanHeresy("The Rite of Translocation must be conducted from within a valid project sanctum.")

        # --- PRE-FLIGHT INQUEST: THE GIT SENTINEL'S GAZE ---
        if not request.force and not request.dry_run:
            self._check_git_status()

        # [FACULTY 2] THE CONTEXTUAL CORTEX
        from ..core.cortex.engine import GnosticCortex
        cortex = GnosticCortex(self.project_root)

        final_artifacts: List[Artifact] = []
        is_simulation = request.dry_run or request.preview
        rite_name = f"Translocate: {request.script or request.to_blueprint or 'manual'}"

        # [FACULTY 1] THE GNOSTIC TRANSACTION
        with GnosticTransaction(self.project_root, rite_name, use_lock=True, simulate=is_simulation) as tx:
            moves: Dict[Path, Path] = {}
            conform_dossier: Dict[str, List] = {}

            is_conform_rite = bool(request.to_blueprint)
            is_script_rite = bool(request.script)
            is_direct_rite = bool(request.paths)

            if sum([is_conform_rite, is_script_rite, is_direct_rite]) > 1:
                raise ArtisanHeresy("A paradox of will: Cannot speak multiple translocation pleas in a single edict.")
            if not any([is_conform_rite, is_script_rite, is_direct_rite]):
                raise ArtisanHeresy(
                    "Heresy of the Void Plea: The translocate rite was spoken without a scripture of will.")

            # --- MOVEMENT I: THE DETECTIVE'S INVESTIGATION (FORGING THE PLAN) ---
            Logger.info("Summoning the Gnostic Detective to perceive the Architect's will...")

            if is_conform_rite:
                detective = GnosticDetective(
                    project_root=self.project_root,
                    source_dir_str=request.conform_from,
                    blueprint_path_str=request.to_blueprint,
                    cli_set_vars=[],
                    non_interactive=request.non_interactive or request.force
                )
                final_moves, full_dossier = detective.investigate()
                moves = final_moves
                conform_dossier = full_dossier
                if "ambiguities" in conform_dossier:
                    self._proclaim_ambiguity_heresy(conform_dossier["ambiguities"])

            # --- MOVEMENT II: THE SYMPHONY OF PROPHECY (SIMULATION) ---
            prophecy_conductor = TranslocationConductor(
                project_root=self.project_root,
                preview=True,
                cortex=cortex,
                transaction=tx
            )
            prophecy_conductor.perceive_will(
                direct_moves=moves,
                script_path=request.script,
                origins=request.paths[:-1] if is_direct_rite and len(request.paths) > 1 else None,
                destinations=request.paths[-1:] if is_direct_rite and len(request.paths) > 1 else None
            )
            prophecy_conductor.conduct()

            # --- MOVEMENT III: THE RITE OF FINAL ADJUDICATION (COMMUNION) ---
            should_proceed, final_backup_path = self._final_adjudication(request, prophecy_conductor, conform_dossier)
            if not should_proceed:
                tx.cancel()
                return self.success("The rite was stayed by the Architect's final will.")

            # --- MOVEMENT IV: THE RITE OF THE LIVING BLUEPRINT (SYNCHRONICITY) ---
            if request.update_blueprint:
                self._update_living_blueprint(request, prophecy_conductor.translocation_map.moves, tx)

            # --- MOVEMENT V: THE MANIFESTATION OF REALITY (EXECUTION) ---
            if is_simulation:
                Logger.info("Quantum Simulation is complete. The mortal realm remains untouched.")
                return self.success("Simulation complete.")

            Logger.info("The Architect's will is absolute. The Unbreakable Hand awakens to make reality manifest...")

            # [THE FIX] THE GNOSTIC HANDSHAKE
            # We bestow the living transaction upon the conductor.
            live_conductor = TranslocationConductor(
                project_root=self.project_root,
                preview=False,
                backup_path=final_backup_path,
                cortex=cortex,
                transaction=tx  # <<< THIS IS THE CRITICAL BESTOWAL OF GNOSIS
            )
            live_conductor.translocation_map = prophecy_conductor.translocation_map
            live_conductor.conduct()

            # [FACULTY 5] THE TELEMETRY BRIDGE
            for res in tx.write_dossier.values():
                final_artifacts.append(Artifact(
                    path=res.path,
                    type="directory" if (tx.project_root / res.path).is_dir() else "file",
                    action=res.action_taken.value,
                    size_bytes=res.bytes_written,
                    checksum=res.gnostic_fingerprint
                ))

            # We must also account for the moved files themselves as artifacts
            for origin, dest in live_conductor.translocation_map.moves.items():
                final_artifacts.append(Artifact(
                    path=dest.relative_to(self.project_root),
                    type="directory" if dest.is_dir() else "file",
                    action="TRANSLOCATED"
                ))

        # --- THE FINAL PROCLAMATION ---
        return self.success(
            "Translocation complete. The new reality is manifest.",
            artifacts=final_artifacts
        )

    def _check_git_status(self):
        """[THE GIT SENTINEL] Ensures the sanctum is clean."""
        if (self.project_root / ".git").exists():
            import subprocess
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project_root).decode()
                if status.strip():
                    Logger.warn("Git Sentinel: The sanctum is dirty. Uncommitted changes may be profaned.")
                    if not Confirm.ask("Proceed anyway?", default=False):
                        raise ArtisanHeresy("Rite stayed by Git Sentinel.")
            except Exception:
                pass

    def _proclaim_ambiguity_heresy(self, ambiguities: Dict[str, List[Path]]):
        """
        =================================================================================
        == THE ORACLE OF DISAMBIGUATION (V-Ω-LEGENDARY-MENTOR)                         ==
        =================================================================================
        LIF: 10,000,000,000

        This divine artisan is a sentient diplomat and Gnostic Mentor. It transmutes a
        profane list of colliding souls into a luminous, interactive Dossier of
        Adjudication. It not only proclaims the heresy but also forges the very
        commands required for its redemption.
        """
        from rich.table import Table
        from rich.text import Text
        from rich.panel import Panel
        from rich.console import Group
        from rich.syntax import Syntax
        from rich.box import ROUNDED
        from ....utils import get_human_readable_size
        import time

        heresy_dossiers = []
        redemption_scroll: List[str] = ["# --- Scroll of Gnostic Redemption ---",
                                        "# Execute these rites to disambiguate reality:"]

        # Sort ambiguities for a deterministic and readable proclamation
        for name, paths in sorted(ambiguities.items()):
            # --- MOVEMENT I: THE FORENSIC INQUEST ---
            # We forge a rich table for each ambiguity, showing its soul.
            heresy_table = Table(
                title=f"[bold]Ambiguous Soul: [cyan]'{name}'[/cyan][/bold]",
                box=ROUNDED, show_header=True, header_style="bold magenta", expand=True
            )
            heresy_table.add_column("Path in Mortal Realm", style="yellow")
            heresy_table.add_column("Type", style="dim", justify="center")
            heresy_table.add_column("Size", style="dim", justify="right")
            heresy_table.add_column("Last Modified", style="dim")

            path_objects = [p.relative_to(self.project_root) for p in paths]

            for path_obj in sorted(path_objects, key=lambda p: str(p)):
                full_path = self.project_root / path_obj
                try:
                    stat = full_path.stat()
                    file_type = "Sanctum" if full_path.is_dir() else "Scripture"
                    size = get_human_readable_size(stat.st_size)
                    mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(stat.st_mtime))
                except FileNotFoundError:
                    file_type, size, mtime = "[red]VOID[/red]", "N/A", "N/A"

                heresy_table.add_row(str(path_obj), file_type, size, mtime)

            heresy_dossiers.append(heresy_table)

            # --- MOVEMENT II: THE FORGING OF THE REDEMPTION EDICT ---
            # We prophesy the command to fix this specific collision.
            # Heuristic: We suggest renaming the second file.
            if len(path_objects) > 1:
                source_to_rename = path_objects[1]
                new_name = f"{source_to_rename.stem}_v2{source_to_rename.suffix}"
                destination = source_to_rename.parent / new_name

                redemption_scroll.append(
                    f"\n# To resolve '{name}', give one soul a new name:"
                )
                redemption_scroll.append(
                    f"scaffold translocate {source_to_rename} {destination}"
                )

        # --- MOVEMENT III: THE MENTOR'S PROCLAMATION ---
        mentor_text = Text.from_markup(
            "The [bold]'conform'[/bold] rite demands a reality of **Unambiguous Souls**. For every scripture in the "
            "prophesied blueprint, there must be only one corresponding scripture in the mortal realm.\n\n"
            "The Detective's Gaze has perceived a Gnostic Schism: multiple scriptures share the same name. "
            "The engine cannot know which soul is the true one. To proceed, you must give each soul a unique identity."
        )

        # --- MOVEMENT IV: THE FINAL ASSEMBLY ---
        # We forge a luminous panel containing the dossiers, the mentorship, and the redemption.
        final_group = Group(
            *heresy_dossiers,
            Panel(mentor_text, title="[bold]The Mentor's Voice[/bold]", border_style="yellow", padding=(1, 2)),
            Panel(Syntax("\n".join(redemption_scroll), "bash", theme="monokai"),
                  title="[bold green]The Scroll of Redemption[/bold green]", border_style="green")
        )

        self.console.print(Panel(
            final_group,
            title="[bold red]Gnostic Adjudication Required: Ambiguous Souls Perceived[/bold red]",
            border_style="red"
        ))

        raise ArtisanHeresy("The rite was stayed to prevent a catastrophic paradox of ambiguity.", exit_code=0)

    def _final_adjudication(self, request: TranslocateRequest, prophecy_conductor: TranslocationConductor,
                            conform_dossier: Dict) -> Tuple[bool, Optional[str]]:
        """
        [THE ORACLE OF ADJUDICATION]
        Performs the final, interactive communion with the Architect to gain consent
        for the transmutation of reality.

        Returns: (should_proceed, final_backup_path)
        """
        force_will = request.force
        is_non_interactive = request.non_interactive
        final_backup_path = request.backup_to

        num_moves = len(prophecy_conductor.translocation_map.moves) if prophecy_conductor.translocation_map else 0
        healed_plans = getattr(prophecy_conductor, 'all_healing_plans', {})
        num_heals = sum(len(plan) for plan in healed_plans.values())
        is_conform_rite = bool(request.to_blueprint)
        num_orphans = len(conform_dossier.get("orphans", {}).get("paths", []))

        if num_moves == 0 and num_heals == 0 and not is_conform_rite:
            Logger.info("The rite is complete. No translocations required.")
            return False, None

        if force_will or is_non_interactive:
            if not force_will:
                Logger.info("Non-interactive mode perceived. Manifesting reality without adjudication.")
            else:
                Logger.info("Architect's will for '--force' is perceived. The Unbreakable Hand awakens...")

            if is_non_interactive and not final_backup_path and not force_will:
                timestamp = int(time.time())
                final_backup_path = f".scaffold/backups/translocate_{timestamp}"
                Logger.info(f"Auto-forging safety snapshot at: [cyan]{final_backup_path}[/cyan]")

            return True, final_backup_path

        # --- Interactive Adjudication ---
        is_low_risk = num_moves <= GNOSTIC_RISK_THRESHOLD
        if is_low_risk and final_backup_path:
            Logger.info(f"Low-risk translocation ({num_moves} file(s)) perceived with backup. Proceeding...")
            return True, final_backup_path

        if not final_backup_path:
            timestamp = int(time.time())
            suggested_backup = f".scaffold/backups/translocate_{timestamp}"
            self.console.print(Panel(
                f"To ensure an unbreakable timeline, a Gnostic Snapshot can be forged at:\n[cyan]{suggested_backup}[/cyan]",
                title="[bold green]🛡️ The Guardian's Offer[/bold green]", border_style="green"
            ))
            if Confirm.ask("[bold question]Forge this safety snapshot?[/bold question]", default=True):
                final_backup_path = suggested_backup
            else:
                Logger.warn("Architect chooses to walk the path without a net.")

        plea = Text.assemble(
            ("[bold question]The Prophecy is prepared. ", "white"),
            (f"{num_moves} translocation(s)", "cyan" if num_moves > 0 else "dim"),
        )
        if num_heals > 0: plea.append(f" and {num_heals} Gnostic healing(s)", style="magenta")
        if is_conform_rite and num_orphans > 0:
            orphan_fate = conform_dossier.get("orphans", {}).get("action", "ignore")
            plea.append(f". {num_orphans} orphaned soul(s) will be ", style="white")
            plea.append(f"{orphan_fate}d", style="yellow")

        plea.append(". Shall this reality be made manifest?[/bold question]", style="white")

        if not Confirm.ask(plea, default=False):
            return False, None

        Logger.info("Architect's will is absolute. The Unbreakable Hand awakens...")
        return True, final_backup_path

    def _update_living_blueprint(self, request: TranslocateRequest, moves: Dict[Path, Path]):
        """
        [THE LIVING BLUEPRINT]
        A divine rite that surgically transmutes the source blueprint to reflect the
        new reality forged by the translocation.
        """
        blueprint_path_str = request.update_blueprint
        if not blueprint_path_str: return

        blueprint_path = (self.project_root / blueprint_path_str).resolve()
        if not blueprint_path.is_file():
            Logger.warn(f"Living Blueprint Gaze averted: The scripture '{blueprint_path.name}' is a void.")
            return

        Logger.info(
            f"The Living Blueprint awakens. Transmuting the scripture of intent: [cyan]{blueprint_path.name}[/cyan]")

        try:
            content = blueprint_path.read_text(encoding='utf-8')
            modified_content = content
            modifications = 0

            for origin, destination in moves.items():
                origin_str = str(origin.relative_to(self.project_root)).replace('\\', '/')
                destination_str = str(destination.relative_to(self.project_root)).replace('\\', '/')

                pattern = r'\b' + re.escape(origin_str) + r'\b'
                if re.search(pattern, modified_content):
                    modified_content = re.sub(pattern, destination_str, modified_content)
                    modifications += 1

            if modifications > 0:
                atomic_write(blueprint_path, modified_content, self.logger, self.project_root)
                Logger.success(f"Successfully inscribed {modifications} transmutation(s) into '{blueprint_path.name}'.")
            else:
                Logger.verbose("No relevant paths found in the blueprint to transmute.")

        except Exception as e:
            raise ArtisanHeresy(
                f"A paradox shattered the Living Blueprint rite for '{blueprint_path.name}'.",
                child_heresy=e
            )