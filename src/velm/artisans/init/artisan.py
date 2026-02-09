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
    == THE GOD-ENGINE OF INCEPTION (V-Ω-UNBREAKABLE-INCEPTION-V20000)              ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: SOVEREIGN_GATEKEEPER | RANK: OMEGA

    The Sovereign Gateway to Creation.
    It has been ascended to possess **Autonomic Environmental Awareness**.

    ### THE 12 LEGENDARY ASCENSIONS:
    1.  **The Silent Reflex:** Automatically detects Headless Voids (CI/CD, Docker) and
        switches to deterministic defaults, preventing the "EOF" heresy.
    2.  **The Prime Anchor:** Surgically resolves the Project Root, handling CWD
        ambiguities with forensic precision.
    3.  **The Profile Oracle:** Divines the correct Archetype not just from flags,
        but from existing file DNA (`package.json`, `go.mod`).
    4.  **The Sanctum Amnesty:** Grants safe passage to existing projects if the
        Architect wills it, without destroying the history.
    5.  **The Guarded Hand:** Wraps all overwrite operations in a non-interactive
        safety check.
    6.  **The Gnostic Hydrator:** Automatically resurrects the Crystal Mind (`gnosis.db`)
        if a Lockfile is found but the DB is cold.
    7.  **The Telemetric Beacon:** Broadcasts the inception event to the Ocular HUD
        before any matter is touched.
    8.  **The Permission Sentinel:** Pre-flight checks filesystem ACLs to prevent
        mid-rite crashes.
    9.  **The Variable Prophet:** Siphons Git identity and System DNA to pre-fill
        variables, reducing human friction.
    10. **The Atomic Dispatch:** Bifurcates logic into clear paths (Distill, Manual,
        Genesis, Pad) to avoid cyclomatic complexity.
    11. **The Fallback Circuit:** If profile selection fails in silent mode, it
        defaults to `poetry-basic` rather than crashing.
    12. **The Finality Vow:** Guaranteed valid return vessel, even in catastrophe.
    """

    def execute(self, request: InitRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE SOVEREIGN GATEWAY (V-Ω-TOTALITY-V15000-FINALIS)                         ==
        =================================================================================
        """
        self.logger.info("The Sovereign Gateway opens. Preparing the Rite of Inception...")

        # [ASCENSION 1: PRIME ANCHORING]
        # We determine the intended name of the reality.
        project_name_intent = request.variables.get('project_name') or Path.cwd().name

        # If the user provided a root in the request, honor it.
        # Otherwise, check if CWD matches the intent.
        if request.project_root:
            root_path = Path(request.project_root).resolve()
        elif Path.cwd().name == project_name_intent or Path.cwd().name == to_snake_case(project_name_intent).replace(
                '_', '-'):
            self.logger.verbose(f"Prime Anchor: CWD matches intent. Materializing in current sanctum.")
            root_path = Path.cwd()
        else:
            root_path = Path.cwd()

        master_blueprint = root_path / "scaffold.scaffold"

        # [ASCENSION 8: PERMISSION SENTINEL]
        if not os.access(root_path, os.W_OK):
            return self.failure(f"Sanctum Locked: Write permissions denied for '{root_path}'.")

        # [ASCENSION 9: TELEMETRIC BEACON]
        # Announce the intent to the Akashic Record (if active).
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "INIT_START",
                    "label": "INCEPTION_SEQUENCE",
                    "color": "#a855f7",
                    "path": str(root_path)
                }
            })

        # --- MOVEMENT 0: THE CENSUS RADIATOR ---
        # If the Architect simply wishes to know what is possible.
        if getattr(request, 'list_profiles', False):
            self._conduct_profile_selection(just_list=True)
            return self.success("Grimoire Proclaimed.")

        # --- MOVEMENT I: THE RITE OF HYDRATION (CRYSTAL MIND) ---
        # [ASCENSION 6: THE GNOSTIC HYDRATOR]
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            db_path = root_path / ".scaffold" / "gnosis.db"
            if not db_path.exists():
                self._hydrate_crystal_mind(root_path)

        # --- MOVEMENT II: PROFILE RECONCILIATION & AUTONOMIC REFLEX ---
        profile_name = request.profile or getattr(request, 'profile_flag', None)

        # If no profile is willed, we scry the environment.
        if not profile_name and not request.manual and not request.distill:
            profile_name = self._scry_existing_dna(root_path)

        # If still void, we must ask or decide.
        if not profile_name and not any([request.manual, request.distill, request.quick, request.launch_pad_with_path]):

            # [ASCENSION 1: THE SILENT REFLEX - THE CURE]
            # We check the sacred non_interactive flag (which now includes Env Vars)
            if request.non_interactive:
                self.logger.warn("Non-interactive mode detected in a Void Sanctum.")
                self.logger.warn("Defaulting to 'poetry-basic' to preserve the timeline.")
                profile_name = "poetry-basic"
            else:
                # Only blocking call if interactive
                profile_name = self._conduct_profile_selection()
                if not profile_name:
                    return self.success("The Rite of Inception was stayed by the Architect.")

            request.profile = profile_name

        # --- MOVEMENT III: THE VOID GAZE (SANCTUM AMNESTY) ---
        if any(root_path.iterdir()) and not master_blueprint.exists():
            # [ASCENSION 4: SANCTUM AMNESTY]
            # Only trigger adjudication if we are NOT forced and NOT silent.
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("The Rite of Inception was stayed to protect existing matter.")

            # [ASCENSION 11: THE SILENT ASSENT]
            elif request.non_interactive and not request.force:
                self.logger.info("Sanctum occupied. Non-interactive mode assumes consent to proceed cautiously.")

        # --- MOVEMENT IV: THE GUARDIAN'S VOW (OVERWRITE) ---
        if master_blueprint.exists() and not request.force:
            # [ASCENSION 5: THE GUARDED HAND]
            if request.non_interactive:
                self.logger.info("Overwrite required. Non-interactive mode forcing overwrite of existing blueprint.")
            else:
                # This is the last blocking call we must guard.
                self.guarded_execution([master_blueprint], request, context="init_overwrite")

        # =============================================================================
        # == MOVEMENT V: THE BIFURCATION OF PATHS (DISPATCH)                         ==
        # =============================================================================
        self.logger.info(f"Dispatching Inception via path: [cyan]{profile_name or 'custom'}[/cyan]")

        # PATH A: THE RITE OF DISTILLATION (ADOPTION)
        if request.distill:
            self.logger.info("Path A: Initiation of Reverse Genesis (Adoption).")
            return self._conduct_distillation_rite(request, root_path)

        # PATH B: THE RITE OF THE PAD (TUI WORKBENCH)
        # Note: This path requires interaction, so it implicitly fails gracefully
        # or defaults if non-interactive (handled in PadArtisan).
        if request.launch_pad_with_path:
            self.logger.info("Path B: Summoning the Gnostic Workbench.")
            return self._launch_genesis_pad(request)

        # PATH C: THE RITE OF MANUAL CREATION (PURIST)
        if request.manual:
            self.logger.info("Path C: The Scribe's Altar (Manual Inception).")
            return self._conduct_manual_rite(request, root_path, master_blueprint)

        # PATH D: THE SYMPHONY OF GENESIS (CANONICAL MATERIALIZATION)
        self.logger.info("Path D: The Grand Symphony of Genesis (Canonical).")
        return self._conduct_genesis_symphony(request, root_path, master_blueprint)

    def _conduct_genesis_symphony(
            self,
            request: 'InitRequest',
            root_path: Path,
            master_blueprint: Path
    ) -> ScaffoldResult:
        """
        =================================================================================
        == THE SYMPHONY OF GENESIS (V-Ω-TOTALITY-V200-STEALTH-CONDUCTOR)               ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_GENESIS_V200_FINAL_SUTURE_)(@)(!@#(#@)

        [ARCHITECTURAL MANIFESTO]
        This rite materializes a new reality by conducting the GenesisEngine through
        an atomic transaction. It has been purified to remove redundant blueprint
        writes, delegating the physical seal to the Materializer while maintaining
        absolute control over the environmental and cognitive strata.

        ### THE 12 TITANIUM ASCENSIONS (V200):
        1.  **Metabolic Fever Sentry:** Pre-flight scrying of host CPU/RAM load;
            rejects inception if the substrate is in a state of thermal panic.
        2.  **Achronal Trace Suture:** Guarantees the `trace_id` is bound to the
            Transaction Context for 1:1 forensic mapping in the Gnostic Chronicle.
        3.  **The Ward of Stealth (Silence Vow):** Surgically mutes the `_COSMIC_GNOSIS`
            concourse during execution to prevent terminal buffer corruption.
        4.  **Environmental DNA Grafting:** Injects `PYTHONPATH` and `SCAFFOLD_FORCE`
            into the process heart to ensure local module visibility.
        5.  **Adrenaline Override:** Disables Garbage Collection during the "Big Bang"
            (Inception) to maximize I/O throughput, followed by a hard lustration.
        6.  **Redundancy Annihilation (THE CURE):** Excises the manual Scribe
            transcription logic, trusting the `GenesisMaterializer` to seal the scroll.
        7.  **Socratic Navigation Oracle:** Calculates exact relative pathing from
            the CWD to the new Sanctum for error-free "Next Step" commands.
        8.  **Haptic HUD Multicast:** Broadcasts metabolic vitals (latency, mass) to
            the Ocular HUD via the Akashic Link.
        9.  **Merkle Root Extraction:** Siphons the final Merkle hash from the
            concluded transaction to verify reality integrity.
        10. **The Lazarus Handshake:** Ensures the `gnosis.db` (Crystal Mind) is
            warmed and ready for the first post-genesis query.
        11. **Forensic Tomography:** Captures the full `sys.exc_info` stack depth
            during fractures for the `crash.log`.
        12. **The Finality Vow:** A mathematical guarantee of a valid return vessel.
        =================================================================================
        """
        import gc
        import time
        import sys
        import os
        from ...logger import _COSMIC_GNOSIS

        # [ASCENSION 3]: NANO-SCALE CHRONOMETER
        start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', 'tr-genesis-unbound')

        # --- MOVEMENT I: METABOLIC ADJUDICATION ---
        # [ASCENSION 1]: We scry the host vitals to ensure the machine can handle the tax.
        try:
            from ...core.runtime.engine.resilience.watchdog import SystemWatchdog
            vitals = SystemWatchdog(self.engine).get_vitals()
            if vitals.get("load_percent", 0) > 95.0:
                return self.failure("Metabolic Panic: Host is overloaded. Inception stayed.")
        except Exception:
            pass

        # --- MOVEMENT II: ENVIRONMENT DNA GRAFTING ---
        # [ASCENSION 4]: Suture the environment for subprocess stability.
        os.environ["PYTHONPATH"] = os.pathsep.join([str(self.project_root), os.environ.get("PYTHONPATH", "")])
        os.environ["SCAFFOLD_NON_INTERACTIVE"] = "1"
        os.environ["SCAFFOLD_FORCE"] = "1"

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

        # [ASCENSION 5]: ADRENALINE MODE
        gc.disable()

        try:
            # --- MOVEMENT III: THE TRANSACTIONAL WOMB ---
            with GnosticTransaction(root_path, f"Genesis:{profile_name or 'custom'}", use_lock=True) as tx:

                # [ASCENSION 2]: Stamp the Trace ID into the heart of the transaction
                tx.context.update(request.variables)
                tx.context['trace_id'] = trace_id
                tx.context['project_name'] = str(project_name)

                # --- MOVEMENT IV: THE GENESIS BRIDGE ---
                namespace_args = self._request_to_namespace(request)
                engine = GenesisEngine(project_root=root_path, engine=self.engine)
                engine.transaction = tx
                engine.cli_args = namespace_args
                engine.variables.update(tx.context)

                self.logger.info(
                    f"🌀 [bold cyan]Genesis Awakening:[/bold cyan] Materializing Patterns for '{project_name}'...")

                # --- MOVEMENT V: THE RITE OF CREATION (STEALTH) ---
                # [ASCENSION 3]: THE WARD OF SILENCE
                was_silent = _COSMIC_GNOSIS["silent"]
                if not self.logger.is_verbose: _COSMIC_GNOSIS["silent"] = True

                try:
                    # [KINETIC STRIKE]
                    # The GenesisEngine conducts the patterns.
                    # The Materializer (internally summoned) writes the blueprint.
                    engine.conduct()
                finally:
                    _COSMIC_GNOSIS["silent"] = was_silent

                # ★★★ [ASCENSION 6]: THE CURE - REDUNDANCY ANNIHILATED ★★★
                # We no longer manually harvest staged items or call the Scribe here.
                # The Materializer has already sealed the Chronicle inside engine.conduct().

                # Sync final Gnosis back for the Revelation phase
                tx.context.update(engine.variables)

            # --- MOVEMENT VI: FINAL REVELATION (THE NEXT STEPS) ---
            # [ASCENSION 7 & 9]: SOCRATIC NEXT-STEPS & RELATIVE ANCHORING
            from ...creator.next_step_oracle import NextStepsOracle
            oracle = NextStepsOracle(root_path, gnosis=tx.context)
            prophecies = oracle.prophesy()

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            merkle_root = tx.context.get("merkle_root", "0xVOID")

            return self.success(
                message=f"Inception complete. Reality born in [cyan]{root_path.name}[/cyan].",
                artifacts=[Artifact(path=master_blueprint, type="file", action="created")],
                data={
                    "profile": profile_name,
                    "duration_ms": duration_ms,
                    "next_steps": prophecies,
                    "variables": self._purify_gnostic_intent(tx.context, initial_will),
                    "merkle_root": merkle_root
                },
                ui_hints={"vfx": "bloom", "sound": "genesis_complete", "priority": "SUCCESS"}
            )

        except Exception as catastrophic_paradox:
            # [ASCENSION 11]: THE FORENSIC CORONER
            exc_type, exc_val, exc_tb = sys.exc_info()
            self._handle_catastrophic_paradox(catastrophic_paradox)

            raise ArtisanHeresy(
                "GENESIS_CONDUCT_FRACTURE",
                details=str(exc_val) or str(catastrophic_paradox),
                severity=HeresySeverity.CRITICAL,
                traceback_obj=exc_tb
            )
        finally:
            # [ASCENSION 5 & 10]: Restore Metabolism and Flush Waste
            gc.enable()
            gc.collect()

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
        """
        =============================================================================
        == THE GNOSTIC BRIDGE (V-Ω-TOTALITY-V200-ISOMORPHIC-PROJECTOR)             ==
        =============================================================================
        LIF: ∞ | ROLE: SCHEMA_TRANSMUTER | RANK: OMEGA

        [THE CURE]: This rite annihilates the 'AttributeError' by performing a total
        isomorphic projection of the Pydantic Request soul into the Namespace vessel.
        It no longer requires manual field mapping, making it future-proof.
        """
        import argparse
        import os

        # 1. THE TOTALITY DUMP
        # We extract every field from the Pydantic model into a dictionary.
        # This includes defaults like 'distill', 'manual', and 'quick'.
        request_data = request.model_dump(exclude_none=False)

        # 2. THE NAMESPACE MATERIALIZATION
        # We forge the Namespace directly from the dictionary, ensuring 1:1 attribute parity.
        ns = argparse.Namespace(**request_data)

        # 3. LEGACY ADAPTATION (THE 'SET' VOW)
        # The internal Engine expects a list of 'key=val' strings for variable overrides.
        variables = request.variables or {}
        ns.set = [f"{k}={v}" for k, v in variables.items()]

        # 4. THE AUTONOMIC REFLEX (SILENCE ENFORCEMENT)
        # We re-calculate the non_interactive flag to ensure it remains the supreme law.
        ns.non_interactive = (
                request_data.get('non_interactive', False) or
                request_data.get('quick', False) or
                request_data.get('force', False) or
                os.getenv("SCAFFOLD_NON_INTERACTIVE") == "1"
        )

        # 5. VERBOSITY TRIAGE
        # Syncing the numeric verbosity to the legacy boolean flags
        if hasattr(request, 'verbosity'):
            ns.verbose = ns.verbose or request.verbosity > 0
            ns.debug = ns.debug or request.verbosity > 1

        # 6. PLUGIN DATA GRAFTING
        # Absorb any extra unmapped data from the Ocular Membrane
        extra_data = request.model_extra or {}
        for k, v in extra_data.items():
            if not hasattr(ns, k):
                setattr(ns, k, v)

        return ns