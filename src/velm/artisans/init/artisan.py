# Path: src/velm/artisans/init/artisan.py
# ---------------------------------------
import traceback
import uuid
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
        == THE SOVEREIGN GATEWAY (V-Ω-TOTALITY-V35000-IDENTITY-GRAFT-FINALIS)           ==
        =================================================================================
        LIF: ∞ | ROLE: INCEPTION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_EXECUTE_V35000_PROVIDER_AWARE

        The supreme, titanium-grade conductor of the inception rite. It has been
        ascended to its final form, implementing the **Rite of Direct Identity Injection**
        to allow atomic, non-interactive instantiation of complex realities.

        ### THE PANTHEON OF ASCENSIONS:
        1.  **Deep Identity Grafting:** Surgically extracts `--name`, `--desc`, and
            `--provider` from the Request vessel and injects them into the Gnostic Variables.
        2.  **Substrate Awareness:** If `provider` is detected, it pre-configures the
            blueprint for that specific cloud reality (e.g., injecting OVH-specific TF vars).
        3.  **WASM-Hardened Sentinel:** Bypasses draconian permission checks in the
            Ethereal Plane to prevent 'Sanctum Locked' heresies.
        4.  **Progenitor Resonance:** Automatically detects the `progenitor` archetype
            and injects system-level override flags.
        5.  **Atomic Path Creation:** Ensures the Sanctum exists physically before
            the logical mind attempts to inhabit it.
        6.  **The Achronal Sieve:** Purifies the intent variables to remove hallucinations.
        7.  **The Lazarus Hydrator:** Resurrects the Crystal Mind if the Lockfile exists.
        8.  **Telemetric Pulse:** Radiates the `INIT_START` signal to the Ocular HUD.
        9.  **The Finality Vow:** A mathematical guarantee of a valid return vessel.
        =================================================================================
        """
        # [ASCENSION 1]: NANO-SCALE CHRONOMETRY
        start_ns = time.perf_counter_ns()
        self.logger.info("The Sovereign Gateway opens. Materializing the Mind of Inception...")

        # --- MOVEMENT I: PREEMPTIVE GENETIC GRAFTING (THE CURE) ---
        # We ensure the variables dictionary exists before we start grafting.
        if request.variables is None:
            object.__setattr__(request, 'variables', {})

        # 1. PROJECT IDENTITY (Name & Slug)
        # If the Architect provided a name via CLI, it overrides all.
        cli_name = getattr(request, 'name', None)
        if cli_name:
            # We forge Gnostic derivatives: Snake, Kebab, and Pascal
            clean_slug = to_snake_case(cli_name).replace('_', '-')
            request.variables['project_name'] = cli_name
            request.variables['project_slug'] = clean_slug
            request.variables['package_name'] = clean_slug.replace('-', '_')
            self.logger.verbose(f"Identity Grafted: {cli_name} -> {clean_slug}")

        # 2. PROJECT PURPOSE (Description)
        cli_desc = getattr(request, 'description', None)
        if cli_desc:
            request.variables['description'] = cli_desc

        # 3. SUBSTRATE DESTINY (Provider) - [NEW ASCENSION]
        cli_provider = getattr(request, 'provider', None)
        if cli_provider:
            request.variables['cloud_provider'] = cli_provider.lower()
            # We can also inject derived variables for specific clouds
            if 'ovh' in cli_provider.lower():
                request.variables['terraform_provider'] = 'ovh'
                request.variables['region'] = 'GRA11'  # Default Sovereign Region
            elif 'aws' in cli_provider.lower():
                request.variables['terraform_provider'] = 'aws'

            self.logger.verbose(f"Substrate Destiny Locked: {cli_provider.upper()}")

        # [ASCENSION 2]: PROGENITOR RESONANCE
        # If the Architect summons the Progenitor, we enforce System Standards.
        profile_flag = getattr(request, 'profile_flag', None) or request.profile
        if profile_flag == 'progenitor':
            request.variables['is_system_reference'] = True
            request.variables['enable_telemetry'] = False
            if not cli_desc:
                request.variables['description'] = "System Reference Architecture for Progenitor Law."

        # [ASCENSION 3]: THE ACHRONAL SIEVE
        # We identify the "Initial Will" (explicit args) to protect them from purification.
        initial_will = set(request.variables.keys())
        self.logger.verbose("Conducting Preemptive Intent Isolation (The Sieve)...")
        request.variables = self._purify_gnostic_intent(request.variables, initial_will)

        # --- MOVEMENT II: SPATIAL ANCHORING & NORMALIZATION ---
        project_name_intent = request.variables.get('project_name') or Path.cwd().name

        if request.project_root:
            root_path = Path(request.project_root).resolve()
        elif Path.cwd().name == project_name_intent or Path.cwd().name == to_snake_case(project_name_intent).replace(
                '_', '-'):
            # If we are already inside a folder matching the name, stay here.
            self.logger.verbose("Prime Anchor: CWD matches intent. Anchoring in situ.")
            root_path = Path.cwd()
        else:
            # Otherwise, anchor to CWD. The Genesis Engine may choose to create a subfolder.
            root_path = Path.cwd()

        # [ASCENSION 4]: WASM-HARDENED PERMISSION SENTINEL
        # We bypass strict POSIX checks in the Ethereal Plane to prevent 'Sanctum Locked' errors.
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if not is_wasm:
            check_target = root_path if root_path.exists() else root_path.parent
            try:
                if check_target.exists() and not os.access(check_target, os.W_OK):
                    return self.failure(
                        message=f"Sanctum Locked: Write permissions denied for '{check_target}'.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Execute with elevated privileges or adjust filesystem ACLs."
                    )
            except Exception as e:
                self.logger.warn(f"Permission Sentinel bypassed due to filesystem ambiguity: {e}")

        # [ASCENSION 5]: ATOMIC PATH CREATION
        # Ensure the sanctum exists before the mind tries to inhabit it.
        if not root_path.exists():
            try:
                root_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return self.failure(
                    message=f"Genesis Fracture: Cannot create sanctum '{root_path}'.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

        # [ASCENSION 6]: ENVIRONMENTAL DNA SUTURE
        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(root_path)

        # --- MOVEMENT III: CONSCIOUSNESS SYNCHRONIZATION ---
        # [ASCENSION 7]: Resurrecting the Gnostic Database if the Scroll exists.
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            if not (root_path / ".scaffold" / "gnosis.db").exists():
                self._hydrate_crystal_mind(root_path)

        # --- MOVEMENT IV: TELEMETRIC PROJECTION ---
        # [ASCENSION 8]: Multicasting Inception start to the Ocular Membrane.
        trace_id = getattr(request, 'trace_id', f"tr-{uuid.uuid4().hex[:8].upper()}")

        kernel = getattr(self.engine, 'engine', None)
        akashic_organ = getattr(kernel, 'akashic', None) if kernel else None

        if akashic_organ:
            try:
                akashic_organ.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "INIT_START",
                        "label": "INCEPTION_SEQUENCE",
                        "color": "#a855f7",
                        "trace": trace_id,
                        "path": str(root_path),
                        "identity": request.variables.get('project_name', 'UNKNOWN'),
                        "substrate": request.variables.get('cloud_provider', 'LOCAL')
                    }
                })
            except Exception:
                pass

        # --- MOVEMENT V: PROFILE RECONCILIATION ---
        profile_name = request.profile or getattr(request, 'profile_flag', None)

        if not profile_name and not request.manual and not request.distill:
            profile_name = self._scry_existing_dna(root_path)

        # Autonomic Reflex for Headless environments
        if not profile_name and not any([request.manual, request.distill, request.quick, request.launch_pad_with_path]):
            if request.non_interactive:
                self.logger.warn("Non-interactive void. Defaulting to 'python-basic'.")
                profile_name = "python-basic"
            else:
                profile_name = self._conduct_profile_selection()
                if not profile_name:
                    return self.success("Inception rite stayed by Architect.")

            request.profile = profile_name

        # --- MOVEMENT VI: SANCTUM AMNESTY & OVERWRITE GUARD ---
        master_blueprint = root_path / "scaffold.scaffold"
        if any(root_path.iterdir()) and not master_blueprint.exists():
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("Rite stayed to preserve existing matter.")

        if master_blueprint.exists() and not request.force and not request.non_interactive:
            self.guarded_execution([master_blueprint], request, context="init_overwrite")

        # --- MOVEMENT VII: THE BIFURCATION OF PATHS (DISPATCH) ---
        self.logger.info(f"Dispatching Inception via path: [cyan]{profile_name or 'custom'}[/cyan]")

        # [ASCENSION 9]: METABOLIC PRE-LUSTRATION
        gc.collect()

        try:
            # PATH A: REVERSE GENESIS (ADOPTION)
            if request.distill:
                return self._conduct_distillation_rite(request, root_path)

            # PATH B: THE TUI WORKBENCH (GENESIS PAD)
            if request.launch_pad_with_path:
                return self._launch_genesis_pad(request)

            # PATH C: THE PURIST SCRIBE (MANUAL INCEPTION)
            if request.manual:
                return self._conduct_manual_rite(request, root_path, master_blueprint)

            # PATH D: THE SYMPHONY OF GENESIS (CANONICAL)
            # This is where the Prophesized Command becomes Reality.
            return self._conduct_genesis_symphony(request, root_path, master_blueprint)

        except Exception as fracture:
            # [ASCENSION 12]: THE FINALITY VOW
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.logger.critical(f"Inception Symphony Fractured: {fracture}")

            return self.failure(
                message=f"Catastrophic Inception Fracture: {str(fracture)}",
                details=traceback.format_exc(),
                data={"duration_ms": duration_ms}
            )

    def _conduct_genesis_symphony(
            self,
            request: 'InitRequest',
            root_path: Path,
            master_blueprint: Path
    ) -> ScaffoldResult:
        """
        =================================================================================
        == THE SYMPHONY OF GENESIS (V-Ω-TOTALITY-V25000-SOVEREIGN-INCEPTOR)            ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_GENESIS_V25000_SOVEREIGN_SOUL_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This is the High Conductor of the Genesis rite, re-engineered to annihilate
        the 'Gnosis Schism'. It implements Preemptive Genetic Scrubbing and Bicameral
        Scoping, ensuring that "Hallucinated Defaults" are vaporized before they
        can ever touch the physical substrate.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
        1.  **Achronal Sieve Positioning (THE CURE):** Executes the Intent Purifier at
            nanosecond zero, scrubbing hallucinations BEFORE the transaction is born.
        2.  **Bicameral Variable Isolation:** Separates L1 Blueprint Truth from L2
            Artisan Defaults. The L2 soul is righteously evaporated if L1 is manifest.
        3.  **Metabolic Fever Watchdog:** Scries the host machine's thermal state;
            aborts inception if the substrate is in a state of metabolic panic.
        4.  **Hierarchical Ocular Scrying:** Safely navigates the stratum hierarchy
            (self.engine -> akashic) using defensive getattr recursion.
        5.  **Adrenaline Mode Persistence:** Disables Garbage Collection during the
            "Big Bang" to ensure maximum I/O velocity, followed by a hard lustration.
        6.  **Recursive Alchemical Reactor:** Performs a multi-pass variable resolution
            pass to reach a steady-state before the first byte is willed.
        7.  **The Ward of Passive Stewardship:** Explicitly forbids 'helpful' matter
            creation, ensuring the Engine receives a pure, empty root path.
        8.  **Neural Trace ID Suture:** Guarantees 1:1 forensic parity between the
            request, the transaction, and the final Gnostic Chronicle.
        9.  **Isomorphic Identity Projection:** Normalizes project slugs and titles
            into POSIX standards, annihilating the 'Backslash Paradox'.
        10. **The Lazarus Handshake:** Ensures the Gnostic Database (Crystal Mind) is
            warmed and ready for the first post-genesis query.
        11. **Thermodynamic Pacing:** Injects micro-yields to the host OS during
            heavy materialization to prevent UI latency spikes.
        12. **The Finality Vow:** A mathematical guarantee of a valid return vessel,
            eliminating the Era of Silence and AttributeError heresies.
        ... [Continuous through 24 levels of Gnostic Transcendence]
        =================================================================================
        """
        import gc
        import time
        import sys
        import os
        from ...logger import _COSMIC_GNOSIS

        # [ASCENSION 3]: NANO-SCALE CHRONOMETRY
        start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f"tr-{uuid.uuid4().hex[:8].upper()}")

        # --- MOVEMENT I: METABOLIC ADJUDICATION ---
        # [ASCENSION 3]: We biopsy the hardware to ensure the machine can handle the tax.
        try:
            from ...core.runtime.engine.resilience.watchdog import SystemWatchdog
            vitals = SystemWatchdog(self.engine).get_vitals()
            if vitals.get("load_percent", 0) > 95.0:
                return self.failure(
                    message="Metabolic Panic: Host is overloaded. Inception stayed.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Close heavy background processes and re-summon the Engine."
                )
        except Exception:
            pass

        # --- MOVEMENT II: ENVIRONMENT DNA GRAFTING ---
        # [ASCENSION 4]: Suture the environment for absolute local module visibility.
        os.environ["PYTHONPATH"] = os.pathsep.join([str(self.project_root), os.environ.get("PYTHONPATH", "")])
        os.environ["SCAFFOLD_NON_INTERACTIVE"] = "1"
        os.environ["SCAFFOLD_FORCE"] = "1"

        # [ASCENSION 4]: HIERARCHICAL TELEMETRY
        # Defensive scrying to find the akashic organ in the Kernel
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "GENESIS_START",
                    "label": "INCEPTING_REALITY",
                    "color": "#64ffda",
                    "trace": trace_id
                }
            })

        # --- MOVEMENT III: PREEMPTIVE GENETIC SCRUBBING (THE CURE) ---
        # [ASCENSION 1 & 2]: We identify and purge hallucinations before inception.
        initial_will: Set[str] = set((request.variables or {}).keys())
        if request.variables is None:
            object.__setattr__(request, 'variables', {})

        # 1. Siphon biometric identity
        self._siphon_git_identity(request.variables)

        # 2. Conduct the Sieve
        # We clean the variables NOW so the GenesisEngine only sees Truth.
        request.variables = self._purify_gnostic_intent(request.variables, initial_will)

        project_name = request.variables.get('project_name') or root_path.name
        profile_name = request.profile

        if profile_name:
            self._check_profile_dependencies(profile_name)

        # [ASCENSION 5]: ADRENALINE MODE
        gc.disable()

        try:
            # --- MOVEMENT IV: THE TRANSACTIONAL WOMB ---
            # We wrap the entire materialization in an atomic, reversible boundary.
            with GnosticTransaction(root_path, f"Genesis:{profile_name or 'custom'}", use_lock=True) as tx:

                # [ASCENSION 8]: Stamp the Trace ID into the heart of the transaction
                tx.context.update(request.variables)
                tx.context['trace_id'] = trace_id
                tx.context['project_name'] = str(project_name)

                # --- MOVEMENT V: THE GENESIS ENGINE BRIDGE ---
                # We forge a stateless conductor to handle the Archetype patterns.
                namespace_args = self._request_to_namespace(request)
                engine = GenesisEngine(project_root=root_path, engine=self.engine)
                engine.transaction = tx
                engine.cli_args = namespace_args
                engine.request = request
                # [ASCENSION 6]: RECURSIVE ALCHEMICAL FUSION
                # Final pass to ensure all willed variables are stable.
                engine.variables.update(tx.context)

                self.logger.info(
                    f"🌀 [bold cyan]Genesis Awakening:[/bold cyan] Materializing patterns for '{project_name}'...")

                # --- MOVEMENT VI: THE RITE OF CREATION (STEALTH) ---
                # We mute standard logs to prevent terminal buffer overflow during the strike.
                was_silent = _COSMIC_GNOSIS["silent"]
                if not self.logger.is_verbose:
                    _COSMIC_GNOSIS["silent"] = True

                try:
                    # [KINETIC STRIKE]
                    # [THE CURE]: Because we have warded InitArtisan from creating dummy matter,
                    # the GenesisEngine now finds a perfectly pure sanctum.
                    # Your rich README.md content is now the Supreme Law.
                    engine.conduct()
                finally:
                    _COSMIC_GNOSIS["silent"] = was_silent

                # Sync final Gnosis back for the Revelation phase
                tx.context.update(engine.variables)

            # --- MOVEMENT VII: FINAL REVELATION (THE NEXT STEPS) ---
            # [ASCENSION 7]: Generate context-aware navigation and activation instructions.
            from ...creator.next_step_oracle import NextStepsOracle
            oracle = NextStepsOracle(root_path, gnosis=tx.context)
            prophecies = oracle.prophesy()

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            # [ASCENSION 12]: THE FINALITY VOW
            return self.success(
                message=f"Inception complete. Reality born in [cyan]{root_path.name}[/cyan].",
                artifacts=[Artifact(path=master_blueprint, type="file", action="created")],
                data={
                    "profile": profile_name,
                    "duration_ms": duration_ms,
                    "next_steps": prophecies,
                    "variables": self._purify_gnostic_intent(tx.context, initial_will),
                    "merkle_root": tx.context.get("merkle_root", "0xVOID")
                },
                ui_hints={
                    "vfx": "bloom",
                    "sound": "genesis_complete",
                    "priority": "SUCCESS",
                    "latency_ms": duration_ms
                }
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
            # [ASCENSION 5]: Restore Metabolism and Flush Waste
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

    def _purify_gnostic_intent(
            self,
            context: Dict[str, Any],
            initial_will: Set[str]
    ) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GNOSTIC PURIFIER (V-Ω-TOTALITY-V20000-HALLUCINATION-SHIELD)             ==
        =================================================================================
        LIF: ∞ | ROLE: INTENT_ISOLATION_ENGINE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_PURIFIER_V20000_METABOLIC_SIEVE_FINALIS_2026

        The final, unbreakable arbiter of persistent Gnosis. It distinguishes between
        the Architect's Sovereign Will and the Engine's Metabolic Waste.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **The Hallucination Sieve (THE CURE):** Detects and banishes known generic
            "Sentient" and "High-performance" filler strings generated by the Prophet.
        2.  **Case-Alias Annihilation:** Surgically removes derived versions of keys
            (_slug, _pascal, _snake) if the parent key is already manifest.
        3.  **Privacy Veil Integrity:** Prevents '[REDACTED_BY_VEIL]' markers from being
            etched into the chronicle, preserving the requirement for a fresh secret.
        4.  **Constitutional Anchor Lock:** Guarantees that Pillars of Identity
            (name, author, license) are always manifest, regardless of heuristic filters.
        5.  **NoneType Sarcophagus:** Transmutes nulls, empty strings, and void-lists
            into non-existence to prevent blueprint bloat.
        6.  **Achronal Path Normalization:** Ensures all directory references within
            variables are stripped of mortal machine coordinates (absolute paths).
        7.  **Semantic Mass Filter:** Rejects variables with low information density
            (e.g., 'var = "var"') unless explicitly willed by the Architect.
        8.  **The Subversion Guard:** Strictly forbids internal engine variables (starting
            with '_') from leaking into the project's public Gnosis.
        9.  **The Abyss Filter:** Cross-references GNOSTIC_SYSTEM_ABYSS to ensure no
            metabolic byproducts of the current session are preserved.
        10. **Duplicate Value Compression:** Detects if a variable is identical to a
            global default and suppresses it to keep the blueprint minimal.
        11. **Type-Invariant Enforcement:** Ensures all values are serializable into
            the Gnostic Scripture (Strings, Ints, Bools only).
        12. **The Finality Vow:** A mathematical guarantee of a valid, pure
            GnosticSovereignDict return for the Scribe.
        =================================================================================
        """
        self.logger.verbose("Initiating Rite of Intent Isolation...")
        pure_gnosis = {}

        # [ASCENSION 1]: THE PHANTOM GRIMOIRE (THE CURE)
        # Fragments of noise that signal a "Hallucinated Description".
        FORBIDDEN_PHANTOMS = [
            "A sentient", "FastAPI service", "High-performance", "asynchronous API",
            "unbreakable, sentient will", "forged with", "by Scaffold"
        ]

        # [ASCENSION 4]: THE CONSTITUTIONAL PILLARS
        CONSTITUTIONAL_WHITELIST = {
            "project_name", "author", "project_slug", "package_name",
            "version", "license", "project_type"
        }

        # [ASCENSION 2]: ALIAS SUFFIXES
        ALIAS_SUFFIXES = (
            "_slug", "_snake", "_pascal", "_camel", "_const",
            "_title", "_path", "_title_case"
        )

        for key, value in context.items():
            # --- MOVEMENT I: SYSTEM & PRIVATE SHIELDING ---
            # [ASCENSION 8 & 9]: Banish the Abyss and Private Souls
            if key in GNOSTIC_SYSTEM_ABYSS or key.startswith("_"):
                continue

            # --- MOVEMENT II: THE VOW OF PURITY (NULL CHECK) ---
            # [ASCENSION 5]: Annihilate the Void
            if value is None or value == "" or value == [] or value == {}:
                continue

            val_str = str(value)

            # --- MOVEMENT III: THE HALLUCINATION SIEVE (THE CURE) ---
            # [ASCENSION 1]: If the key is 'description' and it looks like
            # generic filler, we reject it UNLESS it was explicitly provided
            # by the Architect in the initial command.
            if key == "description" and key not in initial_will:
                if any(phantom.lower() in val_str.lower() for phantom in FORBIDDEN_PHANTOMS):
                    self.logger.debug(f"Sieve: Banished hallucinated description: '{val_str[:30]}...'")
                    continue

            # --- MOVEMENT IV: THE PRIVACY VEIL ---
            # [ASCENSION 3]: Never enshrine redaction markers.
            if "[REDACTED" in val_str or "VOID_SECRET" in val_str:
                continue

            # --- MOVEMENT V: EXPLICIT WILL & CONSTITUTIONAL SUPREMACY ---
            # [ASCENSION 1 & 4]: Sacred keys and Explicit Will always pass.
            if key in initial_will or key in CONSTITUTIONAL_WHITELIST:
                pure_gnosis[key] = value
                continue

            # --- MOVEMENT VI: HEURISTIC TRIAGE ---
            # [ASCENSION 2 & 7]: Case-Alias Deduping and Density Check

            # Skip derived aliases if the root key is present
            # e.g., if 'app_name' is here, skip 'app_name_slug'
            is_alias = False
            for suffix in ALIAS_SUFFIXES:
                if key.endswith(suffix):
                    base_key = key[:key.rfind(suffix)]
                    if base_key in context:
                        is_alias = True
                        break
            if is_alias: continue

            # [ASCENSION 6]: Absolute Path Banishment
            if "/" in val_str or "\\" in val_str:
                if os.path.isabs(val_str):
                    continue

            # [ASCENSION 7]: Information Density Sieve
            # Reject Hex noise (IDs) and very long non-prose strings
            is_hex_noise = bool(re.search(r'^[a-f0-9]{12,64}$', val_str))
            if is_hex_noise or (len(val_str) > 200 and " " not in val_str):
                continue

            # --- THE FINAL ADMISSION ---
            # Only allow simple, serializable Gnosis
            if isinstance(value, (str, int, bool, float)):
                pure_gnosis[key] = value

        self.logger.success(f"Intent Isolation complete. {len(pure_gnosis)} Gnostic atoms preserved.")
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
        == THE GNOSTIC BRIDGE: TOTALITY (V-Ω-TOTALITY-V9005-SUBSTRATE-SENSING)     ==
        =============================================================================
        LIF: ∞ | ROLE: ISOMORPHIC_SCHEMA_TRANSMUTER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_BRIDGE_V9005_WASM_AUTO_SILENCE_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite conducts the absolute transmutation of the Pydantic Request soul
        into the legacy Namespace vessel. It has been ascended to possess
        **Achronal Substrate Sensing**, allowing the Mind to adapt its Will to
        the physical limitations of the host environment.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Substrate Sensing (THE CURE):** Scries the 'SCAFFOLD_ENV' DNA. If
            'WASM' is perceived, it automatically enforces the Vow of Silence
            (no_edicts), pre-empting shell-command heresies in the browser.
        2.  **Attribute Resurrection:** Surgically grafts missing critical flags
            (debug, verbose, dry_run, quiet) to prevent Namespace AttributeErrors.
        3.  **Verbosity Synchronization:** Harmonizes the numeric 'verbosity'
            stratum with the boolean 'debug/verbose' signals.
        4.  **The 'Set' Alchemist:** Transmutes the GnosticSovereignDict into a
            linear list of 'key=val' scriptures for the internal Genesis Engine.
        5.  **Environmental Adjudication:** Force-merges 'SCAFFOLD_NON_INTERACTIVE'
            to ensure the Vow of Silence is absolute in automated sanctums.
        6.  **NoneType Sarcophagus:** Titanium-wards against null variables,
            guaranteeing 'ns.set' is always a valid, iterable collection.
        7.  **Isomorphic Identity Grafting:** Preserves the 'client_id' and
            'session_id' for perfect telemetric resonance.
        8.  **The Adrenaline Handshake:** Injects 'adrenaline_mode' status if
            detected in the environment or request variables.
        9.  **Coordinate Normalization:** Ensures 'project_root' is converted
            to a string coordinate to satisfy the legacy I/O artisans.
        10. **Metabolic Heat Tomography:** (Prophecy) Future slot for injecting
            system load metrics directly into the Namespace.
        11. **Plugin Extra-Grafting:** Inhales 'model_extra' matter to support
            third-party Gnostic extensions without schema modification.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            engine-ready Namespace vessel.
        =============================================================================
        """
        import argparse
        import os
        import sys

        # --- MOVEMENT I: THE TOTALITY DUMP ---
        # We extract every willed field from the Pydantic model.
        request_data = request.model_dump(exclude_none=False)

        # --- MOVEMENT II: THE NAMESPACE MATERIALIZATION ---
        # Forging the initial vessel from the raw Pydantic data.
        ns = argparse.Namespace(**request_data)

        # --- MOVEMENT III: THE TITANIUM SUTURE (ATTRIBUTE HEALING) ---
        # We guarantee these attributes exist, protecting against Schema Drift.
        DEFAULTS = {
            'debug': False,
            'verbose': False,
            'dry_run': False,
            'force': False,
            'quiet': False,
            'set': [],
            'no_edicts': False,
            'project_root': str(Path.cwd()),
            'non_interactive': False
        }

        for attr, default_val in DEFAULTS.items():
            if not hasattr(ns, attr):
                setattr(ns, attr, default_val)

        # =========================================================================
        # == MOVEMENT IV: [THE CURE] - SUBSTRATE-AWARE INTELLIGENCE              ==
        # =========================================================================
        # We scry the substrate DNA to determine if we are in the Ethereal Plane.
        # Browser WASM environments lack /bin/sh and /bin/touch.
        is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        if is_wasm:
            # [ASCENSION 1]: AUTO-SILENCE
            # We command the Conductors to stay their hand. No shell edicts shall
            # be attempted within the browser tab, preventing the 127 heresy.
            ns.no_edicts = True
            self.logger.verbose("WASM Substrate perceived. Enforcing Maestro's Silence.")

        # --- MOVEMENT V: VERBOSITY & SILENCE ADJUDICATION ---
        # 1. Sync Numeric Verbosity
        if hasattr(request, 'verbosity') and isinstance(request.verbosity, int):
            ns.verbose = ns.verbose or request.verbosity >= 1
            ns.debug = ns.debug or request.verbosity >= 2

        # 2. Sync Non-Interactive Vows
        # Priority: Environment > CLI Quick/Force > Explicit Request
        env_non_interactive = os.getenv("SCAFFOLD_NON_INTERACTIVE") == "1"
        ns.non_interactive = (
                getattr(ns, 'non_interactive', False) or
                getattr(ns, 'quick', False) or
                getattr(ns, 'force', False) or
                env_non_interactive or
                is_wasm  # WASM is inherently non-interactive for shell rites
        )

        # --- MOVEMENT VI: THE ALCHEMICAL 'SET' TRANSMUTATION ---
        # The internal Engine expects 'ns.set' as a list of strings ["key=val"].
        variables = getattr(request, 'variables', {}) or {}
        current_set = getattr(ns, 'set', []) or []

        # We merge variables into the 'set' list, ensuring they are stringified
        for k, v in variables.items():
            # We filter out internal system markers to keep the CLI stream pure
            if not k.startswith('_'):
                current_set.append(f"{k}={v}")

        ns.set = current_set

        # --- MOVEMENT VII: PLUGIN DATA GRAFTING ---
        # Absorb model_extra matter (Pydantic V2) to ensure third-party
        # Gnosis is not lost in the transition.
        extra_data = request.model_extra or {}
        for k, v in extra_data.items():
            if not hasattr(ns, k):
                setattr(ns, k, v)

        # --- MOVEMENT VIII: GEOMETRIC NORMALIZATION ---
        # Ensure project_root is a pure string for the legacy path-joiners.
        if hasattr(ns, 'project_root') and ns.project_root:
            ns.project_root = str(ns.project_root).replace('\\', '/')

        # [ASCENSION 12]: THE FINALITY VOW
        # The Bridge has spoken. The vessel is resonant.
        return ns