# Path: src/velm/artisans/genesis/conductor.py
# --------------------------------------------

import re
import tempfile
import time
import subprocess
import shutil
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any

# === THE DIVINE SUMMONS OF GNOSTIC KIN ===
from .materializer import GenesisMaterializer, GnosticDowry
from ..distill import DistillArtisan
from ..init import InitArtisan
from ..workspace.artisan import WorkspaceArtisan
from ...contracts.data_contracts import GnosticArgs, ScaffoldItem, GnosticDossier
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.alchemist import get_alchemist
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GenesisRequest, WorkspaceRequest, InitRequest, DistillRequest, LintBlueprintRequest
from ...logger import Scribe
from ...parser_core.parser import parse_structure, ApotheosisParser
from ...prophecy import prophesy_initial_gnosis
from ...utils import fetch_remote_blueprint, to_string_safe
from ...utils.dossier_scribe import DossierScribe
from ...utils.invocation import invoke_scaffold_command

Logger = Scribe("GenesisConductor")


class GenesisArtisan(BaseArtisan[GenesisRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF UNIVERSAL GENESIS (V-Ω-LEGENDARY-APOTHEOSIS-ADJUDICATED)  ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE)

    This is the High Priest of Genesis in its final, eternal form. It has been
    transfigured into a sentient, multi-modal God-Engine, the one true, universal
    entrypoint for all acts of creation. It is a masterpiece of Gnostic Triage,
    its Gaze capable of distinguishing a file from a remote repository, an archetype
    from a directory, a clean slate from a living reality.

    ### THE PANTHEON OF 13 LEGENDARY ASCENSIONS:

    1.  **The Oracle's Gaze (Archetype Resolution):** It no longer just sees file paths.
        It can be commanded with the name of a known Archetype (`scaffold genesis fastapi-service`),
        summoning the `ArchetypeOracle` to find and conduct the correct scripture.

    2.  **The Path of the Void & Path of Apotheosis:** Its Gaze is contextual. If the
        target is an empty directory, it summons the `InitArtisan` to conduct the
        Sacred Dialogue. If the target is a populated reality, it summons the
        `DistillArtisan` to perform the Rite of Reverse Genesis.

    3.  **The Celestial Herald (Universal Fetcher):** Its Gaze transcends the mortal
        realm. It understands `git` URLs and `gh:user/repo` shorthand, cloning entire
        repositories into ephemeral sanctums to find and conduct remote blueprints.

    4.  **The Gnostic Prophet of Defaults:** Before any rite, it summons the `prophesy_initial_gnosis`
        oracle to perceive the environmental context (git user, project name),
        minimizing the need for the Architect's manual Gnosis.

    5.  **The Simulation Gateway:** It is the one true gateway to the Quantum Simulation
        Engine. If it perceives a plea for `--preview` or `--dry-run`, it righteously
        delegates the entire rite to the `SimulationConductor` for a hyper-realistic,
        non-destructive prophecy of the future.

    6.  **The Forensic Inquisitor:** It wraps all parsing and materialization rites in
        an unbreakable ward, transmuting any paradox into a luminous, hyper-diagnostic
        heresy that reveals the full context of the failure.

    7.  **The Herald of Apotheosis:** Upon a successful rite, it summons the universal
        `DossierScribe` to proclaim a beautiful, cinematic summary of the Great Work,
        including telemetry and prophesied next steps.

    8.  **The Grand Symphony of Genesis:** Its `execute` method is no longer a script,
        but a divine, multi-movement symphony, orchestrating the rites of Perception,
        Adjudication, Materialization, and Proclamation with Gnostic clarity.

    9.  **The Pre-Flight Adjudicator (ASCENDED):** It summons the `BlueprintAdjudicator` via the
        `lint-blueprint` artisan to perform a deep-tissue scan of the blueprint's soul BEFORE
        parsing begins. If the blueprint is profane, Genesis halts.

    10. **The Unbreakable Gnostic Contract:** It forges its own pure `GnosticArgs`
        vessel, ensuring all downstream artisans receive the one true, validated
        will of the Architect.

    11. **The Cosmic Triage:** Its Gaze for `.splane` and `.workspace` scriptures remains
        its first and highest law, making it the true conductor of both single realities
        and entire cosmic workspaces.

    12. **The Guardian's Prophecy:** Its collision survey and `guarded_execution` rite
        are now enshrined as a core movement in its symphony, guaranteeing an
        unbreakable vow of safety.

    13. **The Gnostic Seal:** It checks for cryptographic signatures (.sig files) to ensure
        the provenance of the blueprint is trusted.
    =================================================================================
    """
    ALLOWED_EXTENSIONS = {".scaffold", ".blueprint", ".splane", ".workspace"}

    def execute(self, request: GenesisRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF GENESIS (V-Ω-LEGENDARY-APOTHEOSIS-HEALED)             ==
        =================================================================================
        """
        # --- MOVEMENT I: THE COSMIC TRIAGE (SINGLE REALITY VS. WORKSPACE) ---
        if str(request.blueprint_path).endswith((".splane", ".workspace")):
            return self._conduct_workspace_genesis(request)

        self.logger.info(
            f"The God-Engine of Genesis awakens for a single reality: [cyan]{request.blueprint_path}[/cyan]")

        # --- MOVEMENT II: THE PROPHETIC GAZE (PERCEPTION OF INTENT & DEFAULTS) ---
        self._prophesy_defaults(request)
        target_path, is_ephemeral, intent_type = self._resolve_true_intent(request)
        self.logger.info(f"Gnostic Intent Perceived: [yellow]{intent_type}[/yellow] for target '{target_path.name}'")

        # --- MOVEMENT III: THE PATH OF THE VOID & APOTHEOSIS (CONTEXTUAL DELEGATION) ---
        if intent_type == "INITIATE_DIALOGUE":
            return self.engine.dispatch(InitRequest(**request.model_dump()))
        if intent_type == "DISTILL_REALITY":
            return self.engine.dispatch(
                DistillRequest(source_path=str(target_path), output="scaffold.scaffold", **request.model_dump()))

        # --- [THE NEW ASCENSION: THE GNOSTIC SEAL] ---
        # The Gaze of Prudence: We verify the seal *before* parsing the scripture.
        self._verify_gnostic_seal(target_path)
        # ============================================

        # --- [THE NEW ASCENSION: THE PRE-FLIGHT ADJUDICATION] ---
        # Before we read it to build it, we read it to judge it.
        # We skip this for ephemeral (remote) blueprints as they are usually trusted or temp.
        # But for local files, we check.
        if not is_ephemeral and not request.force:
            self._conduct_preflight_adjudication(target_path)
        # ========================================================

        try:
            # --- MOVEMENT IV: THE GNOSTIC INQUEST (PARSING THE PROPHECY) ---
            gnostic_passport = GnosticArgs.from_namespace(request)
            parser, items, commands, edicts, variables, dossier = self._conduct_parsing(
                target_path, gnostic_passport, request.variables, request
            )
            final_vars = {**variables, **request.variables, 'blueprint_path': target_path.name}
            self._consecrate_items_with_origin(items, target_path)
            gnostic_dowry = (parser, items, commands, final_vars, dossier)

            # --- MOVEMENT V: THE GUARDIAN'S OFFER (SAFETY & REASSURANCE) ---
            collisions = self._survey_for_collisions(items, final_vars, request.project_root or Path.cwd())
            self.guarded_execution(collisions, request, context="genesis")

            # --- MOVEMENT VI: THE SIMULATION OR MATERIALIZATION ---
            if request.preview or request.dry_run:
                return self._conduct_simulation(request)
            else:
                # ★★★ THE DIVINE HEALING ★★★
                # The heresy is annihilated. The Conductor now performs its one true duty:
                # it summons the Materializer and then RIGHTEOUSLY RETURNS its pure ScaffoldResult
                # to the cosmos. The profane, redundant `_proclaim_success` rite has been
                # returned to the void. The Gnostic flow is now pure.
                materializer = GenesisMaterializer(self.engine, request, gnostic_dowry, collisions=collisions)
                return materializer.conduct_materialization_symphony()
                # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        finally:
            if is_ephemeral: self._return_to_void(target_path)

    # --- THE SYMPHONY'S MOVEMENTS (SPECIALIST ARTISANS) ---

    def _conduct_preflight_adjudication(self, target_path: Path):
        """
        [ASCENSION 9] The Gnostic Adjudicator.
        Summons the `LintBlueprintArtisan` to judge the soul of the blueprint.
        """
        self.logger.verbose("Summoning the Adjudicator for pre-flight inquest...")

        # We can use the Artisan dispatch system to reuse the Linter's rich output logic!
        lint_req = LintBlueprintRequest(
            target=str(target_path),
            project_root=self.project_root,
            # Genesis usually implies a user is using a finished archetype, so we can be lenient on headers
            # unless they are actively developing it.
            strict=False
        )

        # Dispatch to the Linter Artisan
        lint_result = self.engine.dispatch(lint_req)

        # If Linting failed (Critical Heresies), we HALT Genesis.
        if not lint_result.success:
            raise ArtisanHeresy(
                "Genesis Aborted: The Blueprint is profane.",
                details=lint_result.message,
                suggestion="Fix the structural heresies in the blueprint before materialization."
            )

        self.logger.success("Blueprint Adjudication: PASSED.")

    def _verify_gnostic_seal(self, blueprint_path: Path):
        """
        =============================================================================
        == THE GUARDIAN OF TRUST                                                   ==
        =============================================================================
        Performs a Gaze for a GPG signature and verifies it against the Keyring.
        """
        sig_path = blueprint_path.with_suffix(blueprint_path.suffix + ".sig")
        if not sig_path.exists():
            # If no signature exists, we issue a warning, not a critical heresy.
            self.logger.warn(f"The scripture '{blueprint_path.name}' is unsealed. Proceeding with caution.")
            return

        self.logger.info(f"Gnostic Seal detected for '{blueprint_path.name}'. Adjudicating...")

        gnupghome = Path.home() / ".scaffold" / "gnupg"
        if not gnupghome.exists():
            raise ArtisanHeresy(
                "Gnostic Keyring is a void.",
                suggestion="Import trusted author keys via `scaffold tool keyring add <keyfile>`."
            )

        try:
            result = subprocess.run(
                ["gpg", f"--homedir={gnupghome}", "--verify", str(sig_path), str(blueprint_path)],
                capture_output=True, text=True, check=True
            )
            # GPG prints success info to stderr, which is a heresy of its own.
            self.logger.success(f"Gnostic Seal is Pure. Verified signature:\n{result.stderr}")
        except FileNotFoundError:
            self.logger.warn("`gpg` artisan not found. Cannot verify Gnostic Seal.")
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(
                f"Profane Seal Detected for '{blueprint_path.name}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"GPG Verification Failed:\n{e.stderr}",
                suggestion="Do not run this blueprint. It is untrusted or has been tampered with."
            )

    def _conduct_workspace_genesis(self, request: GenesisRequest) -> ScaffoldResult:
        self.logger.info("Cosmic Scripture perceived. Delegating to the Gnostic Observatory...")
        workspace_request = WorkspaceRequest(
            workspace_command="genesis",
            splane_path=str(request.blueprint_path),
            project_root=request.project_root,
            force=request.force,
            non_interactive=request.non_interactive,
            verbosity=request.verbosity,
            variables=request.variables
        )
        return self.engine.dispatch(workspace_request)

    def _prophesy_defaults(self, request: GenesisRequest):
        """[FACULTY 4] Injects environmental Gnosis into the request variables."""
        if request.non_interactive: return
        self.logger.verbose("The Gnostic Prophet awakens to perceive environmental defaults...")
        defaults = prophesy_initial_gnosis(request.project_root or Path.cwd())
        # Request variables (CLI) have higher precedence
        for key, value in defaults.items():
            if key not in request.variables:
                request.variables[key] = value

    def _resolve_true_intent(self, request: GenesisRequest) -> Tuple[Path, bool, str]:
        """[FACULTY 1 & 2] Determines if the target is a file, archetype, or directory."""
        from ..weave.oracle import ArchetypeOracle
        path_str = to_string_safe(request.blueprint_path)

        # Gaze 1: Is it a remote scripture?
        if re.match(r'^(https?|git@|gh:)', path_str):
            path, is_eph = self._resolve_blueprint_source(path_str, request)
            return path, is_eph, "REMOTE_BLUEPRINT"

        # Gaze 2: Is it an exact file path?
        root = request.project_root or self.project_root
        potential_path = (root / path_str).resolve()
        if potential_path.is_file():
            return potential_path, False, "LOCAL_BLUEPRINT"

        # Gaze 3: Is it a known archetype?
        try:
            oracle = ArchetypeOracle(root)
            archetype_path, _ = oracle.resolve_source(path_str)
            return archetype_path, False, "ARCHETYPE"
        except ArtisanHeresy:
            pass  # Not an archetype, continue the Gaze.

        # Gaze 4: Is it a directory?
        if potential_path.is_dir():
            is_void = not any(p for p in potential_path.iterdir() if not p.name.startswith('.'))
            if is_void:
                return potential_path, False, "INITIATE_DIALOGUE"
            else:
                return potential_path, False, "DISTILL_REALITY"

        # Final Gaze: If it has a known suffix, treat as a (currently missing) file.
        if Path(path_str).suffix in self.ALLOWED_EXTENSIONS:
            return potential_path, False, "LOCAL_BLUEPRINT"

        # If all else fails, assume it's a request for interactive dialogue.
        return root, False, "INITIATE_DIALOGUE"

    def _resolve_blueprint_source(self, path_str: str, request: GenesisRequest) -> Tuple[Path, bool]:
        """[FACULTY 3] The Celestial Herald."""
        # Gist/HTTP/S shorthand
        if re.match(r'^https?://', path_str):
            self.logger.info(f"Communing with the celestial void to fetch: {path_str}")
            fetched_path = fetch_remote_blueprint(path_str, self.console)
            if not fetched_path: raise ArtisanHeresy(f"Could not fetch celestial blueprint: {path_str}")
            return fetched_path, True

        # GH shorthand
        if path_str.startswith("gh:"):
            repo_path = path_str.split(":", 1)[1]
            # Assumes public repo on main branch
            git_url = f"https://github.com/{repo_path}.git"
            return self._clone_remote_repo(git_url), True

        # Full Git URL
        if path_str.startswith("git@") or path_str.endswith(".git"):
            return self._clone_remote_repo(path_str), True

        root = request.project_root or self.project_root
        resolved_path = (root / path_str).resolve()
        return resolved_path, False

    def _clone_remote_repo(self, git_url: str) -> Path:
        """Clones a repo into an ephemeral sanctum and finds the blueprint."""
        sanctum = tempfile.mkdtemp(prefix="scaffold_celestial_")
        self.logger.info(f"Cloning celestial repository '{git_url}' into ephemeral sanctum...")

        # We must import invoke_scaffold_command here to avoid circular dependency at module level
        result = invoke_scaffold_command(
            ['run', 'git', '--eval', f'clone --depth 1 {git_url} .'],
            cwd=sanctum, non_interactive=True
        )
        if result.exit_code != 0:
            shutil.rmtree(sanctum)
            raise ArtisanHeresy("Failed to clone remote repository.", details=result.output)

        # Find the blueprint within the cloned repo
        found = list(Path(sanctum).glob('**/*.scaffold'))
        if not found:
            shutil.rmtree(sanctum)
            raise ArtisanHeresy("No .scaffold scripture found in the remote repository.")

        # If multiple are found, we could ask, but for now we take the first one.
        return found[0]

    def _conduct_parsing(self, target_blueprint: Path, gnostic_passport: GnosticArgs, cli_vars: Dict,
                         request: GenesisRequest) -> GnosticDowry:
        """
        =================================================================================
        == THE GNOSTIC INQUEST (V-Ω-TOTALITY-V1100-PURE-ARTISAN)                       ==
        =================================================================================
        LIF: ∞ | ROLE: ARCHITECTURAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_PARSING_V1100_STATELESS_FINALIS_2026

        [THE MANIFESTO]:
        This rite has been ascended to a PURE ARTISAN. It is now completely stateless,
        receiving all necessary Gnosis (the 'request' object) as a direct dowry. This
        annihilates the 'Gnostic Schism' (accessing self.request) and makes the rite
        perfectly deterministic and forensically auditable.
        =================================================================================
        """
        self.logger.info(f"Conducting pre-flight Gnostic Inquest on '[cyan]{target_blueprint.name}[/cyan]'...")
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE SYNTACTIC MATERIALIZATION ---
        try:
            # The Parser is summoned to deconstruct the atoms of Form.
            # Returns: (parser, items, commands, edicts, variables, dossier)
            parser, items, commands, edicts, variables, dossier = parse_structure(
                target_blueprint, args=gnostic_passport, pre_resolved_vars=cli_vars
            )
        except Exception as e:
            # Forensic Inquest into Parser Collapse
            self.logger.critical(f"Parser Fracture: The Scribe's gaze was shattered by '{target_blueprint.name}'.")
            raise ArtisanHeresy(
                f"Catastrophic Parsing Failure in '{target_blueprint.name}'",
                details=str(e),
                severity=HeresySeverity.CRITICAL,
                suggestion="Check for unclosed braces or invalid indentation at the locus of failure."
            )

        if not parser:
            raise ArtisanHeresy("The blueprint's soul is profane. Gnosis could not be distilled.")

        # --- MOVEMENT II: THE BENEVOLENT ADJUDICATION ---
        # The Court of Form is summoned to validate Metadata and Geometry.
        from ...core.blueprint_scribe.adjudicator import BlueprintAdjudicator
        adjudicator = BlueprintAdjudicator(self.project_root)

        heresies = adjudicator.adjudicate(target_blueprint.read_text(encoding='utf-8'), target_blueprint,
                                          enforce_metadata=False)

        critical_heresies = [h for h in heresies if h.severity == HeresySeverity.CRITICAL]
        if critical_heresies:
            raise ArtisanHeresy(
                f"Adjudication Failed: '{target_blueprint.name}' contains {len(critical_heresies)} critical fractures.",
                details="\n".join([f"- {h.message} (Ln {h.line_num})" for h in critical_heresies]),
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT III: THE ALCHEMICAL SHADOW TRANSMUTATION ---
        # A full in-memory simulation to find missing variables and broken paths.
        self.logger.verbose("Initiating Alchemical Shadow Transmutation (Memory Simulation)...")
        alchemist = get_alchemist()
        combined_vars = {**variables, **cli_vars}

        # Socratic Variable Triage: Ensure every required variable is manifest.
        # [THE CURE]: We now gaze upon 'request.force', received as a pure parameter.
        missing_gnosis = dossier.required - set(combined_vars.keys())
        if missing_gnosis and not request.force:
            raise ArtisanHeresy(
                f"Gnosis Gap: The blueprint requires variables that are not manifest.",
                details=f"Missing: {', '.join(missing_gnosis)}",
                suggestion="Define these variables in the blueprint's '$$' block or pass them via '--set'."
            )

        # Path and Content Simulation
        for item in items:
            try:
                # 1. Simulate Path Transmutation
                transmuted_path = alchemist.transmute(str(item.path), combined_vars)

                # 2. Path Geometry Sanity
                from ...creator.security import PathSentinel
                PathSentinel.adjudicate(transmuted_path, self.project_root)

                # 3. Simulate Content Transmutation (For inline '::' soul)
                if item.content and len(item.content) < 100000:  # 100kb limit
                    alchemist.transmute(item.content, combined_vars)

                # 4. Seed Availability Check (<<)
                if item.seed_path:
                    from ..template_engine import TemplateEngine
                    te = TemplateEngine(self.project_root, silent=True)
                    if not te.locate_seed(item.seed_path):
                        raise FileNotFoundError(f"Celestial Seed '{item.seed_path}' is a void.")

            except Exception as alchemy_heresy:
                raise ArtisanHeresy(
                    f"Alchemical Collapse on Line {item.line_num}: {alchemy_heresy}",
                    details=f"Path in progress: '{item.path}'",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Ensure all variables are defined and paths are relative to the project root."
                )

        # --- MOVEMENT IV: THE RITE OF FINALITY ---
        # Binding the Trace ID for downstream forensics.
        # [THE CURE]: We gaze upon 'request.metadata', received as a pure parameter.
        trace_id = request.metadata.get('trace_id', 'tr-void')
        self.logger.verbose(f"Trace ID [{trace_id}] bound to Gnostic Dowry.")

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.logger.success(f"Gnostic Inquest: [green]PASSED[/green] ({duration_ms:.2f}ms). Reality is stable.")

        # [THE CRITICAL FIX]: TYPE HARMONIZATION
        # 1. Flatten command tuples to strings (Materializer expects List[str])
        # 2. Remove 'edicts' (Materializer expects 5 items, not 6)
        clean_commands = [c[0] if isinstance(c, tuple) else c for c in commands]

        # Bestow the Dowry upon the Materializer (5-Tuple)
        return parser, items, clean_commands, combined_vars, dossier

    def _survey_for_collisions(self, items: List[ScaffoldItem], final_vars: Dict, project_root: Path) -> List[Path]:
        """[FACULTY 12] The Guardian's Prophecy."""
        self.logger.info("The Guardian awakens to survey the mortal realm for collisions...")
        alchemist = get_alchemist()
        return [
            resolved_path for item in items if not item.is_dir
            for resolved_path_str in [alchemist.transmute(str(item.path), final_vars)]
            for resolved_path in [project_root / resolved_path_str] if resolved_path.exists()
        ]

    def _conduct_simulation(self, request: GenesisRequest) -> ScaffoldResult:
        """[FACULTY 5] The Simulation Gateway."""
        from ...core.simulation import SimulationConductor
        # We must reinvoke the command through the simulation engine
        # To do this safely, we pass a new request object to it.
        sim_request = request.model_copy()
        conductor = SimulationConductor(self.engine)
        prophecy = conductor.conduct(sim_request)

        # Proclaim the prophecy
        from ...core.simulation.scribe import ProphecyScribe
        scribe = ProphecyScribe(prophecy)
        scribe.proclaim()

        return ScaffoldResult(success=True, message="Quantum Simulation Complete.")

    def is_silent(self, registers) -> bool:
        return getattr(registers, 'silent', False)

    def _consecrate_items_with_origin(self, items: List[ScaffoldItem], origin: Path):
        provenance = Path(f"remote/{origin.name}") if "scaffold_remote_" in str(origin) else origin
        for item in items:
            item.blueprint_origin = provenance

    def _return_to_void(self, path: Path):
        try:
            # We must clean the whole temp directory, not just the file
            temp_dir = path.parent
            if "scaffold_celestial" in str(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
                self.logger.verbose(f"Ephemeral sanctum '{temp_dir.name}' returned to the void.")
        except Exception:
            pass