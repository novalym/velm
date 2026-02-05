# Path: scaffold/artisans/init/artisan.py
# ---------------------------------------
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
from ...genesis.genesis_profiles import PROFILES, QUICK_START_PROFILE_NAME
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
        self.logger.info("The Sovereign Gateway opens. Preparing the Rite of Inception...")
        root_path = request.project_root or Path.cwd()

        # [FACULTY 1] THE RITE OF HYDRATION (SQLITE RECOVERY)
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            db_path = root_path / ".scaffold" / "gnosis.db"
            if not db_path.exists():
                self._hydrate_crystal_mind(root_path)

        # [FACULTY 2] THE VOID GAZE (CONTEXT CHECK)
        # We perform a smart check. If the directory is not empty, we offer to Adopt or Distill.
        if any(root_path.iterdir()) and not (root_path / "scaffold.scaffold").exists():
            # If --force is used, we skip this check and assume the user wants to init here.
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("The Rite of Inception was stayed.")

        # [FACULTY 3] THE GUARDIAN'S OFFER
        master_blueprint = root_path / "scaffold.scaffold"
        if master_blueprint.exists():
            self.guarded_execution([master_blueprint], request, context="init_overwrite")

        # --- PATH A: THE RITE OF DISTILLATION (ADOPTION) ---
        if request.distill:
            return self._conduct_distillation_rite(request, root_path)

        # --- PATH B: THE RITE OF THE PAD (TUI) ---
        if request.launch_pad_with_path:
            return self._launch_genesis_pad(request)

        # --- PATH C: THE RITE OF MANUAL CREATION (OUROBOROS) ---
        if request.manual:
            return self._conduct_manual_rite(request, root_path, master_blueprint)

        # --- PATH D: THE SYMPHONY OF GENESIS (STANDARD) ---
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
        """[FACULTY 2] Interactive triage for non-empty directories."""
        self.logger.warn(f"The Sanctum '{root_path.name}' is not empty.")

        # Smart Suggestion based on content
        suggestion = "continue"
        if (root_path / ".git").exists():
            suggestion = "distill"  # Likely an existing project

        from rich.prompt import Prompt
        self.console.print("[yellow]This reality is already populated.[/yellow]")
        choice = Prompt.ask(
            "Choose your path:",
            choices=["abort", "continue", "distill"],
            default=suggestion
        )

        if choice == "distill":
            request.distill = True
            return True
        elif choice == "continue":
            return True

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
        == THE SYMPHONY OF GENESIS (V-Ω-TOTALITY-V2-HEALED)                            ==
        =================================================================================
        LIF: 100x | ROLE: KINETIC_GENESIS_CONDUCTOR | RANK: OMEGA
        """

        # [FACULTY 0] THE MATTER STABILIZER
        # Ensure variables are manifest to prevent the "NoneType" or "KeyError" heresy.
        if request.variables is None:
            # We use object.__setattr__ to bypass Pydantic's frozen model protection if active
            object.__setattr__(request, 'variables', {})

        # [FACULTY 5] THE DEPENDENCY ORACLE & SMART PROFILE SELECTION
        if not request.profile and not getattr(request, 'quick', False):
            if (root_path / "package.json").exists():
                request.profile = "node-basic"
                self.logger.info("Detected Node.js environment. Selecting 'node-basic' profile.")
            elif (root_path / "pyproject.toml").exists():
                request.profile = "python-universal"
                self.logger.info("Detected Python environment. Selecting 'python-universal' profile.")

        profile_name = request.profile or (QUICK_START_PROFILE_NAME if getattr(request, 'quick', False) else None)
        if profile_name:
            self._check_profile_dependencies(profile_name)

        try:
            # [FACULTY 4] THE TRANSACTIONAL WOMB
            with GnosticTransaction(root_path, f"Genesis: {profile_name or 'custom'}", use_lock=True) as tx:

                # [FACULTY 10] THE ANNIHILATION OF THE DOUBLE GIT HERESY
                if (root_path / ".git").exists():
                    self.logger.verbose("Git Repository detected. Suppressing duplicate initialization.")
                    request.variables['use_git'] = False

                # [FACULTY 7] THE GENESIS BRIDGE
                # We forge the Namespace with surgical precision to bridge the Legacy Gap.
                namespace_args = self._request_to_namespace(request)

                engine = GenesisEngine(project_root=root_path, engine=self.engine)
                engine.cli_args = namespace_args

                # Synchronize the Gnostic Context with the Transactional Vault
                tx.context.update(request.variables)

                # Conduct the Rite of Creation
                engine.conduct()

            return self.success(
                f"Inception complete. The soul of the project resides in [cyan]{master_blueprint.name}[/cyan].",
                artifacts=[Artifact(path=master_blueprint, type="file", action="created")]
            )

        except ArtisanHeresy as e:
            if not e.details: e.details = f"Raised by {e.__class__.__name__}"
            raise e
        except Exception as e:
            self._handle_catastrophic_paradox(e)
            raise ArtisanHeresy("Genesis Failed", child_heresy=e)

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
        """[FACULTY 5] Uses the Oracle to check tools required by the profile."""
        profile_data = PROFILES.get(profile_name)
        if not profile_data: return

        overrides = profile_data.get("gnostic_overrides", {})
        needs = []
        if overrides.get("use_docker"): needs.append("docker")
        if overrides.get("use_poetry"): needs.append("poetry")
        if overrides.get("use_git"): needs.append("git")
        if overrides.get("project_type") == "node": needs.append("npm")
        if overrides.get("project_type") == "go": needs.append("go")

        if needs:
            oracle = DependencyOracle(self.project_root)
            try:
                # We verify but do not auto-install in Init phase to keep it fast
                if not oracle.adjudicate(needs, auto_install=False):
                    self.logger.warn("Some tools for this profile are missing. Genesis may falter.")
            except Exception:
                pass

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