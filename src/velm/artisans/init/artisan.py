# Path: scaffold/artisans/init/artisan.py
# ---------------------------------------
import time
import argparse
import sys
import shutil
from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback
from rich.console import Group
from rich.prompt import Confirm

from .manual import ManualGenesis
from ...contracts.data_contracts import InscriptionAction, GnosticArgs, GnosticWriteResult
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.artisan import BaseArtisan
from ...core.cortex.dependency_oracle import DependencyOracle
from ...core.kernel.transaction import GnosticTransaction
from ...genesis.genesis_engine import GenesisEngine
from ...genesis.genesis_profiles import PROFILES
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import InitRequest, DistillRequest
from ...logger import Scribe
from ...prophecy import prophesy_initial_gnosis

# --- THE DIVINE SUMMONS OF THE CRYSTAL MIND ---
try:
    from ...core.state.gnostic_db import GnosticDatabase

    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

Logger = Scribe("InitArtisan")


class InitArtisan(BaseArtisan[InitRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF INCEPTION (V-Ω-CRYSTAL-AWARE-ULTIMA)                      ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Gateway to creation. It orchestrates the Rite of Inception,
    delegating to the Genesis Engine, the Distiller, or the Manual Creator.
    """

    def execute(self, request: InitRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE SOVEREIGN GATEWAY (V-Ω-TOTALITY-V100.0-FINALIS)                         ==
        =================================================================================
        LIF: ∞ | ROLE: GENESIS_ORCHESTRATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_INIT_EXECUTE_TOTALITY_2026

        [ARCHITECTURAL MANIFESTO]
        This rite is the Singularity Point of creation. It adjudicates between the
        Mortal Realm (existing files) and the Gnostic Ideal (Archetypes). It enforces
        the Law of Intent, ensuring the correct profile is summoned and materialized.
        =================================================================================
        """
        self.logger.info("The Sovereign Gateway opens. Preparing the Rite of Inception...")
        root_path = request.project_root or Path.cwd()
        master_blueprint = root_path / "scaffold.scaffold"

        # --- MOVEMENT 0: THE CENSUS RADIATOR ---
        # [ASCENSION 1]: If the Architect willed a listing, we proclaim the Grimoire and exit.
        if getattr(request, 'list_profiles', False):
            self.logger.verbose("Proclaiming the Census of Manifest Archetypes.")
            self._conduct_profile_selection(just_list=True)
            return self.success("Grimoire Proclaimed. Choose your reality and re-summon the rite.")

        # --- MOVEMENT I: THE RITE OF HYDRATION (CRYSTAL MIND) ---
        # [FACULTY 1]: Re-sync the SQLite soul if the lockfile is manifest.
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            db_path = root_path / ".scaffold" / "gnosis.db"
            if not db_path.exists():
                self._hydrate_crystal_mind(root_path)

        # --- MOVEMENT II: PROFILE RECONCILIATION ---
        # [ASCENSION 2]: Ω-Symmetry Resolution.
        # We unify the Positional Locus and the Explicit Flag into a single intent.
        profile_name = request.profile or getattr(request, 'profile_flag', None)

        # [ASCENSION 3]: HEURISTIC SENSING
        # If the Architect is silent, we scry the sanctum for existing DNA to suggest a profile.
        if not profile_name and not request.manual and not request.distill:
            if (root_path / "package.json").exists():
                self.logger.info("Detected Node.js DNA. Suggesting 'node-basic'.")
                profile_name = "node-basic"
            elif (root_path / "pyproject.toml").exists():
                self.logger.info("Detected Python DNA. Suggesting 'poetry-basic'.")
                profile_name = "poetry-basic"

        # [ASCENSION 4]: THE SOCRATIC MENU
        # If intent is still a void, we summon the full categorized Grimoire.
        if not profile_name and not any([request.manual, request.distill, request.quick, request.launch_pad_with_path]):
            profile_name = self._conduct_profile_selection()
            if not profile_name:
                return self.success("The Rite of Inception was stayed by the Architect.")
            # Inscribe the choice back into the request for the symphony
            request.profile = profile_name

        # --- MOVEMENT III: THE VOID GAZE (SANCTUM AUDIT) ---
        # [FACULTY 2]: Adjudicate if the current sanctum is already occupied.
        if any(root_path.iterdir()) and not master_blueprint.exists():
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("The Rite of Inception was stayed to protect existing matter.")

        # --- MOVEMENT IV: THE GUARDIAN'S VOW ---
        # [FACULTY 3]: Protect the Master Blueprint from accidental profanation.
        if master_blueprint.exists() and not request.force:
            self.guarded_execution([master_blueprint], request, context="init_overwrite")

        # =============================================================================
        # == MOVEMENT V: THE BIFURCATION OF PATHS (DISPATCH)                         ==
        # =============================================================================

        # PATH A: THE RITE OF DISTILLATION (ADOPTION)
        if request.distill:
            return self._conduct_distillation_rite(request, root_path)

        # PATH B: THE RITE OF THE PAD (TUI WORKBENCH)
        if request.launch_pad_with_path:
            return self._launch_genesis_pad(request)

        # PATH C: THE RITE OF MANUAL CREATION (PURIST)
        if request.manual:
            return self._conduct_manual_rite(request, root_path, master_blueprint)

        # PATH D: THE SYMPHONY OF GENESIS (CANONICAL MATERIALIZATION)
        # [THE FINAL STRIKE]: profile_name is now guaranteed or willed by the menu.
        return self._conduct_genesis_symphony(request, root_path, master_blueprint)

    def _hydrate_crystal_mind(self, root_path: Path):
        """[FACULTY 1] Resurrects the SQLite DB from the JSON Lockfile."""
        self.logger.info("Crystal Mind not found. Hydrating from Textual Scroll (scaffold.lock)...")
        try:
            db = GnosticDatabase(root_path)
            db.hydrate_from_lockfile()
        except Exception as e:
            self.logger.warn(f"Hydration failed: {e}. The project will proceed with Memory only.")

    def _adjudicate_occupied_sanctum(self, root_path: Path, request: InitRequest) -> bool:
        """
        =================================================================================
        == THE SOVEREIGN ADJUDICATOR (V-Ω-TOTALITY-V150.0-FINALIS)                     ==
        =================================================================================
        LIF: ∞ | ROLE: SPATIAL_REALITY_TRIAGE | RANK: OMEGA_SUPREME
        AUTH: Ω_SANCTUM_ADJUDICATOR_2026

        [ARCHITECTURAL MANIFESTO]
        This rite performs a deep forensic audit of the target sanctum. It identifies
        Gnostic Signatures (our own artifacts) and grants them amnesty, while
        categorizing foreign matter into "Historical" (Git), "Metabolic" (node_modules),
        or "Unknown" (Conflict) to guide the Architect's choice.
        =================================================================================
        """
        from rich.table import Table
        from rich.prompt import Prompt
        from rich.panel import Panel

        # [ASCENSION 1]: THE AMNESTY GRIMOIRE
        # These markers are recognized as the Engine's own soul. They do not trigger
        # the "Occupied" heresy.
        GNOSTIC_DNA: Final[Set[str]] = {
            ".scaffold", "scaffold.lock", ".heartbeat",
            "daemon_traffic.jsonl", "journal.jsonl", "daemon.pulse"
        }

        # 1. THE CENSUS OF REALITY
        try:
            # We perform a single, atomic scan of the target sanctum.
            mortal_remnants = [
                entry for entry in root_path.iterdir()
                if entry.name not in GNOSTIC_DNA
            ]
        except Exception as e:
            # In the event of a path paradox, we play it safe and assume occupation.
            self.logger.warn(f"Spatial scan faltered: {e}")
            return True

        # [ASCENSION 2]: THE VOID AMNESTY
        # If the only items in the folder are our own Gnostic DNA, the sanctum is pure.
        if not mortal_remnants:
            self.logger.verbose("Sanctum scan complete: Only internal Gnostic DNA perceived. Proceeding.")
            return True

        # 2. THE FORENSIC TRIAGE
        # We categorize the remnants to provide a high-status suggestion.
        has_git = (root_path / ".git").exists()
        has_manifest = any(f.name in ("package.json", "pyproject.toml", "go.mod") for f in mortal_remnants)

        # [ASCENSION 3]: TELEMETRY PULSE
        # Signal the Ocular HUD that a Reality Collision is being adjudicated.
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "REALITY_COLLISION",
                    "label": "ADJUDICATING_OCCUPIED_SANCTUM",
                    "color": "#fbbf24",  # Kinetic Gold
                    "trace": getattr(request, 'trace_id', 'tr-init-triage')
                }
            })

        # --- MOVEMENT I: THE REVELATION TABLE ---
        table = Table(box=None, expand=True, padding=(0, 2))
        table.add_column("Classification", style="cyan", width=20)
        table.add_column("Artifact", style="white")
        table.add_column("Gnostic Weight", justify="right", style="dim")

        for entry in mortal_remnants[:10]:  # Limit Gaze to prevent terminal flood
            icon = "📁" if entry.is_dir() else "📄"
            table.add_row(
                "Git_Sanctuary" if entry.name == ".git" else "Foreign_Matter",
                f"{icon} {entry.name}",
                f"{entry.stat().st_size} bytes" if entry.is_file() else "N/A"
            )

        self.console.print(Panel(
            Group(
                Text.from_markup(
                    f"The Oracle has perceived [bold yellow]{len(mortal_remnants)}[/bold yellow] foreign soul(s) in [cyan]'{root_path.name}'[/cyan]."),
                Text(""),
                table,
                Text(""),
                Text("An unplanned materialization may lead to a Structural Schism.", style="italic dim")
            ),
            title="[bold red]REALITY_COLLISION_DETECTED[/bold red]",
            border_style="red"
        ))

        # --- MOVEMENT II: THE PROPHETIC SUGGESTION ---
        suggestion = "continue"
        if has_git:
            suggestion = "distill"  # Highly likely to be an existing project
        elif has_manifest:
            suggestion = "distill"  # Legacy project without git?

        # --- MOVEMENT III: THE SACRED CHOICE ---
        choice = Prompt.ask(
            "Adjudicate the path forward:",
            choices=["abort", "continue", "distill"],
            default=suggestion
        )

        if choice == "distill":
            # [ASCENSION 12]: THE PATH OF ADOPTION
            # We transmute the current InitRequest into a DistillRequest mid-symphony.
            request.distill = True
            self.logger.info("The Architect has chosen the Path of Adoption (Distillation).")
            return True

        elif choice == "continue":
            # [ASCENSION 5]: THE VOW OF RISK
            # The Architect takes responsibility for the resulting entropy.
            self.logger.warn("The Great Work continues in an occupied sanctum. Purity not guaranteed.")
            return True

        # [ASCENSION 0]: THE HALT
        return False

    def _conduct_manual_rite(self, request: InitRequest, root_path: Path, master_blueprint: Path) -> ScaffoldResult:
        """[FACULTY 8] Creates a minimal blueprint via System Forge."""
        manual_creator = ManualGenesis(self.project_root, self.engine)

        with GnosticTransaction(root_path, "Rite of Manual Inception", use_lock=True) as tx:
            artifact = manual_creator.conduct(request, tx)

            if not request.variables:
                defaults = prophesy_initial_gnosis(root_path)
                tx.context.update(defaults)

        return self.success(
            f"Manual Genesis complete. {artifact.path.name} created.",
            artifacts=[artifact]
        )

    def _conduct_genesis_symphony(self, request: InitRequest, root_path: Path,
                                  master_blueprint: Path) -> ScaffoldResult:
        """
        =================================================================================
        == THE SYMPHONY OF GENESIS (V-Ω-TOTALITY-V100.0-FINALIS)                       ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_GENESIS_CONDUCTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_GENESIS_SYMPHONY_V100_TOTAL_MATERIALIZATION

        [ARCHITECTURAL MANIFESTO]
        This rite governs the transition from the Void to the Manifest. It orchestrates
        the alignment of the Gnostic DNA (Profiles) with the physical hardware (Disk),
        wrapped in a transactional shield that guarantees absolute consistency.
        =================================================================================
        """
        # [ASCENSION 1]: CHRONOMETRIC ANCHOR
        # We capture the inception time at the absolute event horizon.
        start_time = time.monotonic()

        # [FACULTY 0]: THE MATTER STABILIZER
        # Ensure variables are manifest to prevent the "NoneType" heresy.
        if request.variables is None:
            object.__setattr__(request, 'variables', {})

        # --- MOVEMENT I: PROFILE RESOLUTION & DNA SELECTION ---
        # [ASCENSION 2]: OMNISCIENT PROFILE TRIAGE
        # We resolve the profile name, falling back to the Gnostic Default if willed.
        profile_name = request.profile
        if not profile_name and getattr(request, 'quick', False):
            from ...genesis.genesis_profiles import DEFAULT_PROFILE_NAME
            profile_name = DEFAULT_PROFILE_NAME
            request.profile = profile_name

        # [FACULTY 5]: THE DEPENDENCY ORACLE
        # Before we strike the disk, we scry the host for the required artisans.
        if profile_name:
            self._check_profile_dependencies(profile_name)

        try:
            # --- MOVEMENT II: THE TRANSACTIONAL WOMB ---
            # [FACULTY 4]: We conduct the entire symphony within a reversible reality.
            with GnosticTransaction(root_path, f"Genesis: {profile_name or 'custom'}", use_lock=True) as tx:

                # [ASCENSION 3]: HUD RESONANCE
                # Broadcast the inception signal to the Ocular HUD (ST-3)
                if self.engine.akashic:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "GENESIS_INCEPTION",
                            "label": f"BIRTHING_{str(profile_name or 'CUSTOM').upper()}",
                            "color": "#64ffda",
                            "trace": getattr(request, 'trace_id', tx.tx_id)
                        }
                    })

                # [FACULTY 10]: THE ANNIHILATION OF THE DOUBLE GIT HERESY
                if (root_path / ".git").exists():
                    self.logger.verbose("Git Sanctuary detected. Suppressing duplicate initialization.")
                    request.variables['use_git'] = False

                # --- MOVEMENT III: THE GENESIS BRIDGE ---
                # [FACULTY 7]: Transmute the modern Request into the legacy Namespace.
                # This bridge ensures backward compatibility with the GenesisEngine's soul.
                namespace_args = self._request_to_namespace(request)

                # [ASCENSION 4]: THE ENGINE MATERIALIZATION
                # Summon the specialized creation engine.
                engine = GenesisEngine(project_root=root_path, engine=self.engine)
                engine.cli_args = namespace_args

                # [ASCENSION 5]: CONTEXTUAL DNA SUTURE
                # Synchronize the Architect's variables with the Transactional Vault.
                tx.context.update(request.variables)

                # --- MOVEMENT IV: THE RITE OF CREATION ---
                # [THE KINETIC STRIKE]
                # The engine walks the blueprint, stage by stage.
                engine.conduct()

                # [ASCENSION 6]: PHYSICAL VALIDATION
                # We verify that the master blueprint has been inscribed.
                if not master_blueprint.exists() and not request.dry_run:
                    self.logger.warn(f"The Primary Scripture '{master_blueprint.name}' is unmanifest.")

            # --- MOVEMENT V: THE REVELATION ---
            # [ASCENSION 7]: PROPHETIC NEXT STEPS
            # We summon the Oracle to predict the Architect's next move.
            from ...creator.next_step_oracle import NextStepsOracle
            oracle = NextStepsOracle(root_path, gnosis=request.variables)
            prophecies = oracle.prophesy()

            # [ASCENSION 8]: METABOLIC FINALITY
            duration_ms = (time.monotonic() - start_time) * 1000

            self.logger.success(f"Apotheosis Complete. Reality '{root_path.name}' forged in {duration_ms:.2f}ms.")

            return self.success(
                message=f"Inception complete. Reality born in [cyan]{root_path.name}[/cyan].",
                artifacts=[Artifact(path=master_blueprint, type="file", action="created")],
                data={
                    "profile": profile_name,
                    "duration_ms": duration_ms,
                    "next_steps": prophecies,
                    "session_id": tx.tx_id
                },
                ui_hints={
                    "vfx": "bloom",
                    "sound": "genesis_complete",
                    "next_suggested_action": prophecies[0] if prophecies else None
                }
            )

        except ArtisanHeresy as e:
            # [ASCENSION 9]: HERESY ATTRIBUTION
            # Ensure the heresy carries the signature of its creator.
            if not e.details: e.details = f"Raised by {self.__class__.__name__}"
            raise e

        except Exception as catastrophic_paradox:
            # [ASCENSION 10]: THE EMERGENCY SARCOPHAGUS
            # If the symphony shatters, perform a forensic dump and rollback.
            self._handle_catastrophic_paradox(catastrophic_paradox)
            raise ArtisanHeresy(
                "GENESIS_SYMPHONY_FRACTURE: The creation rite collapsed.",
                child_heresy=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL
            )

    def _conduct_profile_selection(self, just_list: bool = False) -> Optional[str]:
        """
        [THE RITE OF CHOICE]
        Uses the new 'profiles.py' API to show a rich, categorized menu.
        """
        from rich.prompt import Prompt
        from rich.table import Table
        from ...genesis.genesis_profiles import list_profiles, get_categories

        table = Table(title="[bold cyan]The Grimoire of Manifest Archetypes[/bold cyan]", box=None, expand=True)
        table.add_column("Key", style="bold yellow")
        table.add_column("Category", style="magenta")
        table.add_column("Description", style="white")

        available = list_profiles()
        for p in available:
            table.add_row(p['name'], p.get('category', 'General'), p['description'])

        self.console.print(Panel(table, border_style="cyan", title="[bold white]Ω_PROFILES[/bold white]"))

        if just_list: return None

        choices = [p['name'] for p in available]
        return Prompt.ask("Select an Archetype to materialize", choices=choices)


    def _conduct_distillation_rite(self, request: InitRequest, root: Path) -> ScaffoldResult:
        """[FACULTY 7] Delegates to DistillArtisan."""
        from ...interfaces.requests import DistillRequest
        from ...artisans.distill import DistillArtisan

        self.logger.info("Adopting current reality into a Gnostic Blueprint...")

        distill_req = DistillRequest(
            source_path=str(root),
            output="scaffold.scaffold",
            project_root=root,
            force=request.force,
            dry_run=request.dry_run,
            non_interactive=request.non_interactive,
            variables=request.variables
        )

        artisan = DistillArtisan(self.engine)
        return artisan.execute(distill_req)

    def _launch_genesis_pad(self, request: InitRequest) -> ScaffoldResult:
        """[FACULTY 8] Summons the TUI."""
        from ...artisans.pad import PadArtisan
        from ...interfaces.requests import PadRequest

        pad_req = PadRequest(pad_name="genesis", project_root=request.project_root)
        artisan = PadArtisan(self.engine)
        return artisan.execute(pad_req)

    def _check_profile_dependencies(self, profile_name: str):
        """[FACULTY 5] Scries the profile's DNA for system-level dependencies."""
        from ...genesis.genesis_profiles import get_profile
        profile_data = get_profile(profile_name)
        if not profile_data: return

        overrides = profile_data.get("gnosis_overrides", {})

        # [ASCENSION 3]: INTELLIGENT NEED-SENSING
        # We derive 'needs' from the overrides.
        needs = []
        mapping = {
            "use_docker": "docker",
            "use_poetry": "poetry",
            "use_git": "git"
        }
        for key, binary in mapping.items():
            if overrides.get(key): needs.append(binary)

        if overrides.get("project_type") == "node": needs.append("npm")
        if overrides.get("project_type") == "go": needs.append("go")

        if needs:
            oracle = DependencyOracle(self.project_root)
            # Silence the oracle unless it finds a fracture
            oracle.adjudicate(needs, auto_install=False)

    def _handle_catastrophic_paradox(self, e: Exception):
        """[FACULTY 12] Forensic logging."""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.logger.critical(f"Genesis Engine Collapse: {str(e)}", exc_info=True)

        error_panel = Panel(
            Group(
                Text.from_markup(f"[bold red]The Genesis Engine has encountered a paradox.[/bold red]"),
                Text(f"Exception: {type(e).__name__}: {str(e)}", style="white"),
                Traceback.from_exception(exc_type, exc_value, exc_traceback, show_locals=False, width=100)
            ),
            title="[bold red]Catastrophic Failure in Init Rite[/bold red]",
            border_style="red",
            expand=False
        )
        self.console.print(error_panel)

    def _request_to_namespace(self, request: InitRequest) -> argparse.Namespace:
        """
        =================================================================================
        == THE NAMESPACE FORGE (V-Ω-LEGENDARY-BRIDGE-HEALED)                             ==
        =================================================================================
        [THE CURE]: Surgically sanitizes the 'set' keyword to prevent KeyError and
        multiple-value heresies in the GenesisEngine.
        """
        # Ensure variables strata is grounded
        variables = request.variables or {}

        # Transmute the internal dictionary to the legacy "key=value" list format
        # This satisfies the GenesisEngine's thirst for the '--set' CLI dialect.
        set_vars = [f"{k}={v}" for k, v in variables.items()]

        # [ASCENSION] The Silent Mode Adjudicator
        # Determines if the Engine should speak or remain in the shadows.
        is_silent_mode = getattr(request, 'non_interactive', False) or \
                         getattr(request, 'quick', False) or \
                         getattr(request, 'force', False)

        # Extract extra data, shielding the 'set' and 'lint' keys from duplicate injection
        extra_data = request.model_extra or {}
        sanitized_extra = {k: v for k, v in extra_data.items() if k not in ('set', 'lint')}

        return argparse.Namespace(
            launch_pad_with_path=getattr(request, 'launch_pad_with_path', False),
            quick=getattr(request, 'quick', False),
            profile=getattr(request, 'profile', None),
            type=getattr(request, 'type', 'project'),
            from_remote=getattr(request, 'from_remote', None),
            manual=getattr(request, 'manual', False),
            distill=getattr(request, 'distill', False),
            force=getattr(request, 'force', False),
            non_interactive=is_silent_mode,
            silent=(request.verbosity < 0),
            verbose=(request.verbosity > 0),
            dry_run=getattr(request, 'dry_run', False),
            preview=getattr(request, 'preview', False),
            audit=getattr(request, 'audit', False),
            # [HEALED]: Explicitly mapping the sutured attribute from the previous rite
            lint=getattr(request, 'lint', False),
            # [HEALED]: Resolving the 'set' KeyError by providing the alchemized list
            set=set_vars,
            no_edicts=getattr(request, 'no_edicts', False),
            ignore=[],
            **sanitized_extra
        )