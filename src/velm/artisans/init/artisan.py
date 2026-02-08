# Path: src/velm/artisans/init/artisan.py
# ---------------------------------------

import time
import argparse
import sys
import shutil
import os
import re
import gc
import json
import subprocess
import threading
from pathlib import Path
from typing import Optional, List, Final, Set, Dict, Any, Tuple, Union

# --- THE LUMINOUS UI ---
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback
from rich.console import Group
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TaskID
)

# --- THE GNOSTIC MODULES ---
from .manual import ManualGenesis
from ...contracts.data_contracts import (
    InscriptionAction,
    GnosticArgs,
    GnosticWriteResult,
    ScaffoldItem,
    GnosticLineType
)
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.artisan import BaseArtisan
from ...core.cortex.dependency_oracle import DependencyOracle
from ...core.kernel.transaction import GnosticTransaction
from ...genesis.genesis_engine import GenesisEngine
from ...genesis.genesis_profiles import PROFILES, list_profiles, get_profile
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import InitRequest, DistillRequest, PadRequest
from ...logger import Scribe
from ...prophecy import prophesy_initial_gnosis
from ...core.blueprint_scribe.scribe import BlueprintScribe
from ...utils import atomic_write, to_snake_case

# --- THE DIVINE SUMMONS OF THE CRYSTAL MIND ---
try:
    from ...core.state.gnostic_db import GnosticDatabase
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

Logger = Scribe("InitArtisan")

# [ASCENSION 1]: THE GNOSTIC SYSTEM ABYSS
# Internal metabolic byproducts that must never soil the Blueprint.
GNOSTIC_SYSTEM_ABYSS: Final[Set[str]] = {
    "scaffold_env", "generated_manifest", "timestamp", "file_count",
    "project_root_name", "ansi_colors", "term_width", "os_sep",
    "transaction_id", "trace_id", "python_version_tuple", "is_simulated",
    "dry_run", "force", "verbose", "silent", "no_edicts", "non_interactive",
    "request_id", "session_id", "client_id", "blueprint_path",
    "clean_type_name", "env_vars_setup", "name_camel", "name_const",
    "name_pascal", "name_path", "name_slug", "name_snake", "name_title",
    "ai_code_generation_consent", "project_structure_pattern", "dna",
    "blueprint_origin", "is_binary", "current_year", "creation_date",
    "is_git_repo", "has_docker", "has_make", "project_type"
}


class InitArtisan(BaseArtisan[InitRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF INCEPTION (V-Ω-UNBREAKABLE-INCEPTION)                     ==
    =================================================================================
    LIF: 10,000,000,000,000
    """

    def execute(self, request: InitRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE SOVEREIGN GATEWAY (V-Ω-TOTALITY-V15000-FINALIS)                         ==
        =================================================================================
        """
        self.logger.info("The Sovereign Gateway opens. Preparing the Rite of Inception...")

        # [ASCENSION 1: PRIME ANCHORING]
        project_name_intent = request.variables.get('project_name') or Path.cwd().name

        # If the user provided a root in the request, honor it.
        # Otherwise, check if CWD matches the intent.
        if request.project_root:
            root_path = Path(request.project_root).resolve()
        elif Path.cwd().name == project_name_intent or Path.cwd().name == to_snake_case(project_name_intent).replace('_', '-'):
            self.logger.verbose(f"Prime Anchor: CWD matches intent. Materializing in current sanctum.")
            root_path = Path.cwd()
        else:
            root_path = Path.cwd()

        master_blueprint = root_path / "scaffold.scaffold"

        # 0. PERMISSION SENTINEL
        if not os.access(root_path, os.W_OK):
            return self.failure(f"Sanctum Locked: Write permissions denied for '{root_path}'.")

        # --- MOVEMENT 0: THE CENSUS RADIATOR ---
        if getattr(request, 'list_profiles', False):
            self._conduct_profile_selection(just_list=True)
            return self.success("Grimoire Proclaimed.")

        # --- MOVEMENT I: THE RITE OF HYDRATION (CRYSTAL MIND) ---
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            db_path = root_path / ".scaffold" / "gnosis.db"
            if not db_path.exists():
                self._hydrate_crystal_mind(root_path)

        # --- MOVEMENT II: PROFILE RECONCILIATION ---
        profile_name = request.profile or getattr(request, 'profile_flag', None)

        if not profile_name and not request.manual and not request.distill:
            profile_name = self._scry_existing_dna(root_path)

        if not profile_name and not any([request.manual, request.distill, request.quick, request.launch_pad_with_path]):
            profile_name = self._conduct_profile_selection()
            if not profile_name:
                return self.success("The Rite of Inception was stayed by the Architect.")
            request.profile = profile_name

        # --- MOVEMENT III: THE VOID GAZE (SANCTUM AMNESTY) ---
        if any(root_path.iterdir()) and not master_blueprint.exists():
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("The Rite of Inception was stayed to protect existing matter.")

        # --- MOVEMENT IV: THE GUARDIAN'S VOW ---
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
        return self._conduct_genesis_symphony(request, root_path, master_blueprint)

    def _conduct_genesis_symphony(
            self,
            request: 'InitRequest',
            root_path: Path,
            master_blueprint: Path
    ) -> ScaffoldResult:
        """
        =================================================================================
        == THE SYMPHONY OF GENESIS (V-Ω-TOTALITY-V200-STEALTH-MATERIALIZATION)         ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_GENESIS_V200_STEALTH_OCULAR_STABILITY_)(@)(!@#(#@)
        """
        import gc
        import time
        import sys
        import os
        from ...logger import _COSMIC_GNOSIS

        # [ASCENSION 3]: NANO-SCALE CHRONOMETER
        start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', 'tr-genesis-unbound')

        # [ASCENSION 11]: UI HAPTIC HUD PULSE
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {"type": "GENESIS_START", "label": "INCEPTING_REALITY", "color": "#64ffda", "trace": trace_id}
            })

        # 1. INTENT SNAPSHOT (CAUSAL SPLICING)
        initial_will: Set[str] = set((request.variables or {}).keys())
        if request.variables is None:
            object.__setattr__(request, 'variables', {})

        self._siphon_git_identity(request.variables)
        initial_will.update(["author", "email"])

        project_name = request.variables.get('project_name') or root_path.name
        profile_name = request.profile

        if profile_name:
            self._check_profile_dependencies(profile_name)

        # [ASCENSION 2]: ADRENALINE MODE (Maximize I/O Velocity)
        gc.disable()

        try:
            # --- MOVEMENT I: THE TRANSACTIONAL WOMB ---
            with GnosticTransaction(root_path, f"Genesis:{profile_name or 'custom'}", use_lock=True) as tx:

                tx.context.update(request.variables)
                tx.context['trace_id'] = trace_id
                tx.context['project_name'] = str(project_name)

                # [ASCENSION 18]: THE HERESY SILENCE VOW
                os.environ["SCAFFOLD_IGNORE_POST_RUN_ERRORS"] = "1"

                # --- MOVEMENT II: THE GENESIS BRIDGE ---
                namespace_args = self._request_to_namespace(request)
                engine = GenesisEngine(project_root=root_path, engine=self.engine)
                engine.transaction = tx
                engine.cli_args = namespace_args
                engine.variables.update(tx.context)

                # =========================================================================
                # == [THE CURE]: STEALTH MATERIALIZATION                                 ==
                # =========================================================================
                # We do NOT use 'rich.Progress' for the terminal.
                # We use high-status static logs to prevent buffer corruption.

                self.logger.info(
                    f"🌀 [bold cyan]Genesis Awakening:[/bold cyan] Materializing Patterns for '{project_name}'...")

                # --- MOVEMENT III: THE RITE OF CREATION (STEALTH) ---
                # [ASCENSION 1]: THE WARD OF SILENCE
                # We mute the concourse to prevent sub-artisans from shattering the buffer.
                was_silent = _COSMIC_GNOSIS["silent"]
                if not self.logger.is_verbose:
                    _COSMIC_GNOSIS["silent"] = True

                try:
                    # [KINETIC STRIKE]
                    engine.conduct()
                finally:
                    _COSMIC_GNOSIS["silent"] = was_silent

                self.logger.info(f"✨ [bold green]Reality Staged.[/bold green] Conducting forensic harvest...")

                # --- MOVEMENT IV: THE RITE OF HARVEST (PHYSICAL TOMOGRAPHY) ---
                # [ASCENSION 4]: THE FORENSIC AUTOPSY ENGINE
                physical_items = self._harvest_staged_reality(tx, root_path, master_blueprint)

                if not physical_items:
                    self.logger.critical(
                        f"Lattice Fracture: Staging Root '{tx.staging_manager.staging_root}' is a void.")
                    raise ArtisanHeresy(
                        "HOLLOW_REALITY: Engine reported success, but no matter was manifest.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Check filesystem permissions or disk space on the host."
                    )

                # Sync variable state back
                tx.context.update(engine.variables)

                # --- MOVEMENT V: THE RITE OF PURIFICATION ---
                pure_gnosis = self._purify_gnostic_intent(tx.context, initial_will)

                # --- MOVEMENT VI: THE INSCRIPTION OF THE BLUEPRINT ---
                self.logger.verbose("Sealing the Project Chronicle (scaffold.scaffold)...")

                scribe = BlueprintScribe(root_path)
                raw_commands = getattr(engine, 'post_run_commands', [])
                normalized_commands = self._normalize_commands_for_scribe(raw_commands)

                blueprint_content = scribe.transcribe(
                    items=physical_items,
                    commands=normalized_commands,
                    gnosis=pure_gnosis
                )

                # Atomic Inscription within the transactional womb
                atomic_write(
                    target_path=master_blueprint,
                    content=blueprint_content,
                    logger=self.logger,
                    sanctum=root_path,
                    transaction=tx
                )

                self.logger.success(f"Chronicle Sealed: [dim]{master_blueprint.name}[/dim]")

            # --- MOVEMENT VII: FINAL REVELATION (THE NEXT STEPS) ---
            # [ASCENSION 6]: SOCRATIC NEXT-STEPS
            from ...creator.next_step_oracle import NextStepsOracle
            oracle = NextStepsOracle(root_path, gnosis=tx.context)
            prophecies = oracle.prophesy()

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            return self.success(
                message=f"Inception complete. Reality born in [cyan]{root_path.name}[/cyan].",
                artifacts=[Artifact(path=master_blueprint, type="file", action="created")],
                data={
                    "profile": profile_name,
                    "duration_ms": duration_ms,
                    "next_steps": prophecies,
                    "variables": pure_gnosis,
                    "merkle_root": getattr(self, 'merkle_root', '0xVOID')
                },
                ui_hints={"vfx": "bloom", "sound": "genesis_complete", "priority": "SUCCESS"}
            )

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FORENSIC CORONER
            exc_type, exc_val, exc_tb = sys.exc_info()
            self._handle_catastrophic_paradox(catastrophic_paradox)

            err_msg = str(exc_val) if exc_val else str(catastrophic_paradox)
            if "Permission denied" in err_msg:
                err_msg = f"Sanctum Locked (OS Permission Error): {err_msg}"

            raise ArtisanHeresy(
                "GENESIS_CONDUCT_FRACTURE",
                details=err_msg,
                severity=HeresySeverity.CRITICAL,
                traceback_obj=exc_tb
            )
        finally:
            # [ASCENSION 2]: Restore Metabolism
            gc.enable()

    def _harvest_staged_reality(self, tx: GnosticTransaction, root_path: Path, master_bp: Path) -> List[ScaffoldItem]:
        """
        =================================================================================
        == THE REALITY SCRAPER (V-Ω-PHYSICAL-HARVEST-V15000)                           ==
        =================================================================================
        [THE CURE]: Directly walks the staging root to find every manifested atom.
        Implements [ROOT FOLDING] to ensure the blueprint is anchored correctly.
        """
        staged_items = []
        staging_root = tx.staging_manager.staging_root

        if not staging_root.exists():
            self.logger.warn("Staging Root is a void. No physical matter found.")
            return []

        # 1. PHYSICAL RECURSIVE WALK
        for p in staging_root.rglob("*"):
            if p.is_file():
                rel_path = p.relative_to(staging_root)

                # Skip internal engine artifacts and the blueprint itself
                if rel_path.name in (master_bp.name, "scaffold.lock") or ".scaffold" in rel_path.parts:
                    continue

                try:
                    # Capture the soul of the staged file
                    content = p.read_text(encoding='utf-8', errors='ignore')
                    is_bin = False
                except Exception:
                    content = "[BINARY_MATTER]"
                    is_bin = True

                staged_items.append(ScaffoldItem(
                    path=rel_path,
                    type="file",
                    action="created",
                    content=content,
                    is_binary=is_bin,
                    line_type=GnosticLineType.FORM,
                    is_dir=False,
                    line_num=200 + len(staged_items)
                ))

        if not staged_items:
            return []

        # 2. [ASCENSION]: THE DIMENSIONAL ROOT FOLD
        # Detect if all files are nested inside a single project-named directory.
        top_levels = {item.path.parts[0] for item in staged_items if item.path.parts}

        if len(top_levels) == 1:
            common_root = list(top_levels)[0]
            project_slug = tx.context.get('project_slug', '')
            project_name = tx.context.get('project_name', '')

            # Check if the top level matches the project name (e.g. new_test/src/...)
            if common_root in (project_slug, project_name, root_path.name):
                self.logger.info(f"Spatial Overlap: Folding redundant root '[dim]{common_root}[/dim]'.")

                folded_items = []
                for item in staged_items:
                    if len(item.path.parts) > 1:
                        # Strip the first part of the path
                        item.path = Path(*item.path.parts[1:])
                        folded_items.append(item)

                # Only apply fold if it doesn't empty the list
                if folded_items:
                    staged_items = folded_items

        # 3. DIRECTORY INFERENCE
        # Re-construct parent directories for the Scribe to build a perfect tree.
        seen_dirs = set()
        dir_items = []
        for item in staged_items:
            p = item.path.parent
            while p != Path("."):
                if p not in seen_dirs:
                    seen_dirs.add(p)
                    dir_items.append(ScaffoldItem(
                        path=p, type="directory", action="created", is_dir=True,
                        line_type=GnosticLineType.FORM, line_num=50 + len(dir_items)
                    ))
                p = p.parent

        return sorted(dir_items + staged_items, key=lambda x: x.line_num)

    def _normalize_commands_for_scribe(self, raw_commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """
        [THE TRINITY ENFORCER]
        The Scribe expects 3-tuples (cmd, line, undo).
        The Parser now produces 4-tuples (cmd, line, undo, heresy).
        This artisan strips the heresy block for the visual blueprint to prevent crashes.
        """
        normalized = []
        for cmd in raw_commands:
            if isinstance(cmd, tuple):
                if len(cmd) == 4:
                    # Strip the 4th element (heresy block) for the Scribe
                    normalized.append((cmd[0], cmd[1], cmd[2]))
                elif len(cmd) == 3:
                    normalized.append(cmd)
                elif len(cmd) == 2:
                    normalized.append((cmd[0], cmd[1], None))
                elif len(cmd) == 1:
                    normalized.append((cmd[0], 0, None))
            elif isinstance(cmd, str):
                normalized.append((cmd, 0, None))
        return normalized

    def _purify_gnostic_intent(self, context: Dict[str, Any], initial_will: Set[str]) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GNOSTIC PURIFIER (V-Ω-INTENT-ISOLATION-V2)                              ==
        =================================================================================
        LIF: ∞ | ROLE: METABOLIC_FILTER

        [THE CURE]: Surgically cleanses the context to ensure the final blueprint
        remains focused on intent. It admits Constitutional Pillars and Initial Will,
        while banishing the "Metabolism of the Machine".
        """
        pure_gnosis = {}

        # [ASCENSION 1]: THE CONSTITUTIONAL WHITELIST
        # These keys are the pillars of project identity and are always manifest.
        CONSTITUTIONAL_WHITELIST = {
            "project_name", "author", "description", "project_slug",
            "package_name", "version", "license", "database_type", "auth_method",
            "project_type"
        }

        for key, value in context.items():
            # 1. Admit Explicit Will
            # If the user explicitly provided it via --set or the Wizard, it is SACRED.
            if key in initial_will:
                pure_gnosis[key] = value
                continue

            # 2. Admit Constitutional Pillars
            # Even if derived, these define the soul of the reality.
            if key in CONSTITUTIONAL_WHITELIST:
                pure_gnosis[key] = value
                continue

            # 3. Banish the Abyss (The Noise Filter)
            if key in GNOSTIC_SYSTEM_ABYSS or key.startswith("_"):
                continue

            # 4. The Heuristic Sieve
            # We allow simple primitives that don't look like metabolic noise.
            if isinstance(value, (str, int, bool, float)):
                val_str = str(value)

                # Check for "Metabolic Signatures" (Hex IDs, UUIDs, absolute paths)
                is_hex_noise = bool(re.search(r'^[a-f0-9]{12,64}$', val_str))
                is_path_noise = "/" in val_str or "\\" in val_str

                if not is_hex_noise and not is_path_noise and len(val_str) < 120:
                    # Final check: Don't include redundant case-aliases (name_const, name_pascal)
                    # unless they are explicitly part of the initial will.
                    if not any(key.endswith(sfx) for sfx in ["_camel", "_pascal", "_const", "_title", "_slug"]):
                        pure_gnosis[key] = value

        return pure_gnosis

    def _normalize_commands(self, raw_commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """
        [DEPRECATED ALIAS]
        Redirects to the new Scribe-specific normalizer.
        """
        return self._normalize_commands_for_scribe(raw_commands)

    def _siphon_git_identity(self, variables: Dict[str, Any]):
        """[ASCENSION 2] Siphons Gnosis from Git config to prevent 'Unknown' authors."""
        try:
            if "author" not in variables or not variables["author"]:
                name = subprocess.check_output(["git", "config", "user.name"], text=True,
                                               stderr=subprocess.DEVNULL).strip()
                if name:
                    variables["author"] = name
            if "email" not in variables or not variables["email"]:
                email = subprocess.check_output(["git", "config", "user.email"], text=True,
                                                stderr=subprocess.DEVNULL).strip()
                if email:
                    variables["email"] = email
        except Exception:
            pass  # Git not manifest in this reality or terminal

    def _hydrate_crystal_mind(self, root_path: Path):
        """[FACULTY 1] Resurrects the SQLite DB from the JSON Lockfile."""
        self.logger.info("Crystal Mind not found. Hydrating from Chronicle (scaffold.lock)...")
        try:
            db = GnosticDatabase(root_path)
            db.hydrate_from_lockfile()
        except Exception as e:
            self.logger.warn(f"Hydration failed: {e}. Gnosis will remain ephemeral.")

    def _adjudicate_occupied_sanctum(self, root_path: Path, request: InitRequest) -> bool:
        """Adjudicates reality collisions, ignoring manifest markers."""
        GNOSTIC_DNA = {".scaffold", "scaffold.scaffold", "scaffold.lock", ".heartbeat"}
        try:
            remnants = [e for e in root_path.iterdir() if e.name not in GNOSTIC_DNA]
        except Exception:
            return True

        if not remnants: return True

        table = Table(box=None, expand=True)
        table.add_column("Classification", style="cyan")
        table.add_column("Artifact", style="white")
        for entry in remnants[:5]:
            icon = "📁" if entry.is_dir() else "📄"
            table.add_row("Foreign_Matter", f"{icon} {entry.name}")

        self.console.print(Panel(Group(Text(f"Reality Collision detected in '{root_path.name}'."), table),
                                 title="[bold red]COLLISION[/]", border_style="red"))
        choice = Prompt.ask("Action:", choices=["abort", "continue", "distill"], default="continue")
        if choice == "distill": request.distill = True
        return choice != "abort"

    def _conduct_manual_rite(self, request, root, bp):
        """[FACULTY 8] Manual Inception Rite."""
        manual_creator = ManualGenesis(self.project_root, self.engine)
        with GnosticTransaction(root, "Manual Inception", use_lock=True) as tx:
            artifact = manual_creator.conduct(request, tx)
            if not request.variables:
                tx.context.update(prophesy_initial_gnosis(root))
        return self.success(f"Manual Genesis complete.", artifacts=[artifact])

    def _conduct_profile_selection(self, just_list=False):
        """[THE RITE OF CHOICE]"""
        table = Table(title="[bold cyan]Manifest Archetypes[/]", box=None, expand=True)
        table.add_column("Key", style="bold yellow")
        table.add_column("Description")
        available = list_profiles()
        for p in available: table.add_row(p['name'], p['description'])
        self.console.print(Panel(table, border_style="cyan"))
        if just_list: return None
        return Prompt.ask("Select Archetype", choices=[p['name'] for p in list_profiles()])

    def _conduct_distillation_rite(self, request, root):
        """[FACULTY 7] Adoption Rite via Distillation."""
        from ...artisans.distill import DistillArtisan
        req = DistillRequest(source_path=str(root), output="scaffold.scaffold", project_root=root, force=request.force,
                             dry_run=request.dry_run, variables=request.variables)
        return DistillArtisan(self.engine).execute(req)

    def _launch_genesis_pad(self, request):
        """[FACULTY 8] Summons the TUI Workbench."""
        from ...artisans.pad import PadArtisan
        return PadArtisan(self.engine).execute(PadRequest(pad_name="genesis", project_root=request.project_root))

    def _check_profile_dependencies(self, name):
        """[FACULTY 5] Dependency scrying."""
        from ...genesis.genesis_profiles import get_profile
        p = get_profile(name)
        if not p: return
        ov = p.get("gnosis_overrides", {})
        needs = [b for k, b in {"use_docker": "docker", "use_poetry": "poetry", "use_git": "git"}.items() if ov.get(k)]
        if ov.get("project_type") == "node": needs.append("npm")
        if needs: DependencyOracle(self.project_root).adjudicate(needs, auto_install=False)

    def _handle_catastrophic_paradox(self, e):
        """[FACULTY 12] Forensic autopsy of the loop fracture."""
        exc_type, exc_val, exc_tb = sys.exc_info()
        self.logger.critical(f"Genesis Engine Collapse: {str(e)}", exc_info=True)
        self.console.print(Panel(
            Group(
                Text(f"Exception: {type(e).__name__}: {str(e)}", style="white"),
                Traceback.from_exception(exc_type or type(e), exc_val or e, exc_tb, show_locals=False, width=100)
            ),
            title="[bold red]PARADOX[/]", border_style="red"
        ))

    def _scry_existing_dna(self, root: Path) -> Optional[str]:
        """Heuristic sensing for automatic profile suggestion."""
        if (root / "package.json").exists(): return "node-basic"
        if (root / "pyproject.toml").exists(): return "poetry-basic"
        if (root / "go.mod").exists(): return "go-cli"
        if (root / "Cargo.toml").exists(): return "rust-lib"
        return None

    def _request_to_namespace(self, request: InitRequest) -> argparse.Namespace:
        """Transmutes modern Pydantic requests to legacy argparse Namespaces."""
        variables = request.variables or {}
        set_vars = [f"{k}={v}" for k, v in variables.items()]

        is_silent = getattr(request, 'silent', False) or (request.verbosity < 0)
        is_verbose = getattr(request, 'verbose', False) or (request.verbosity > 0)
        is_debug = getattr(request, 'debug', False) or (request.verbosity > 1)

        is_quick = getattr(request, 'quick', False)
        is_force = getattr(request, 'force', False)
        is_non_interactive = getattr(request, 'non_interactive', False) or is_quick or is_force

        extra_data = request.model_extra or {}
        sanitized_extra = {k: v for k, v in extra_data.items() if k not in ('set', 'lint')}

        ns = argparse.Namespace()
        ns.profile = request.profile
        ns.force = is_force
        ns.quick = is_quick
        ns.silent = is_silent
        ns.verbose = is_verbose
        ns.debug = is_debug
        ns.dry_run = getattr(request, 'dry_run', False)
        ns.preview = getattr(request, 'preview', False)
        ns.audit = getattr(request, 'audit', False)
        ns.non_interactive = is_non_interactive
        ns.set = set_vars

        for k, v in sanitized_extra.items():
            setattr(ns, k, v)

        return ns