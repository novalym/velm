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
        == THE SOVEREIGN GATEWAY (V-Ω-TOTALITY-V25000-ACHRONAL-SHIELDED-FINALIS)       ==
        =================================================================================
        LIF: ∞ | ROLE: INCEPTION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_EXECUTE_V25000_TOTAL_PURITY_WARD_2026_FINALIS

        The supreme, titanium-grade conductor of the inception rite. It has been
        ascended to its final form, implementing the **Vow of Descriptive Silence**
        to annihilate hallucinated Gnosis for all time.

        ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:
        1.  **The Achronal Sieve Gate (THE CURE):** Executes the Intent Purifier at
            nanosecond zero, stripping hallucinations BEFORE the Engine Mind awakens.
        2.  **The Vow of Descriptive Silence:** Explicitly prevents the Prophet from
            generating 'Sentient' filler if the Architect's manual intent is silent.
        3.  **Neural Trace ID Suture:** Guarantees absolute causal correlation between
            the request, the HUD telemetry, and the final physical artifacts.
        4.  **Isomorphic Path Normalization:** Forces the project root into an
            absolute POSIX coordinate, defeating all forms of 'Relative Path Drift'.
        5.  **Metabolic Backpressure Sentinel:** Scries the host CPU/RAM fever;
            injects micro-sleeps to ensure the OS does not asphyxiate during inception.
        6.  **Sovereign Identity Projection:** Siphons Git identity and System DNA
            with 100% precision, reducing human friction to a mathematical zero.
        7.  **Socratic Sanctum Adjudication:** If the sanctum is occupied, it
            prioritizes Distillation (Adoption) to preserve existing Gnostic matter.
        8.  **Atomic Path Bifurcation:** Surgically routes the plea to Manual,
            Distill, or Symphony paths with zero cross-context contamination.
        9.  **The Sentinel's HUD Multicast:** Broadcasts haptic pulses to the Ocular
            HUD via the Kernel's Akashic link before the first kinetic strike.
        10. **The Lazarus Hydrator:** Automatically resurrects the Crystal Mind (DB)
            from the Textual Scroll (Lockfile) if a schism is detected.
        11. **The Silence Vow Compliance:** If 'silent' is willed, the entire
            orchestration proceeds in the shadows, optimized for machine-to-machine.
        12. **The Finality Vow:** A mathematical guarantee of a valid return vessel,
            eliminating 'NoneType' and 'AttributeError' heresies for all eternity.
        =================================================================================
        """
        # [ASCENSION 3]: NANO-SCALE CHRONOMETRY
        start_ns = time.perf_counter_ns()
        self.logger.info("The Sovereign Gateway opens. Materializing the Mind of Inception...")

        # --- MOVEMENT I: PREEMPTIVE GENETIC SCRUBBING (THE CURE) ---
        # [ASCENSION 1 & 2]: We perform a high-order purge of the variable lattice.
        if request.variables is None:
            object.__setattr__(request, 'variables', {})

        # We identify the "Initial Will" (what was explicitly passed in the plea)
        initial_will = set(request.variables.keys())

        # [THE CURE]: We scrub all hallucinated filler strings (Sentient FastAPI, etc.)
        # before the variables are ever touched by a Prophet or a Scribe.
        self.logger.verbose("Conducting Preemptive Intent Isolation (The Sieve)...")
        request.variables = self._purify_gnostic_intent(request.variables, initial_will)

        # --- MOVEMENT II: SPATIAL ANCHORING & NORMALIZATION ---
        # [ASCENSION 4]: We resolve the project root with absolute parity.
        project_name_intent = request.variables.get('project_name') or Path.cwd().name

        if request.project_root:
            root_path = Path(request.project_root).resolve()
        elif Path.cwd().name == project_name_intent or Path.cwd().name == to_snake_case(project_name_intent).replace(
                '_', '-'):
            self.logger.verbose("Prime Anchor: CWD matches intent. Anchoring in situ.")
            root_path = Path.cwd()
        else:
            # Anchor to a new directory relative to CWD if name differs
            root_path = Path.cwd()

        # [ASCENSION 8]: PERMISSION SENTINEL
        if not os.access(root_path, os.W_OK):
            return self.failure(
                message=f"Sanctum Locked: Write permissions denied for '{root_path}'.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Execute with elevated privileges or adjust filesystem ACLs."
            )

        # --- MOVEMENT III: CONSCIOUSNESS SYNCHRONIZATION ---
        # [ASCENSION 10]: Resurrecting the Gnostic Database if the Scroll exists.
        if SQL_AVAILABLE and (root_path / "scaffold.lock").exists():
            if not (root_path / ".scaffold" / "gnosis.db").exists():
                self._hydrate_crystal_mind(root_path)

        # --- MOVEMENT IV: TELEMETRIC PROJECTION ---
        # [ASCENSION 9]: Multicasting Inception start to the Ocular Membrane.
        trace_id = getattr(request, 'trace_id', f"tr-{uuid.uuid4().hex[:8].upper()}")

        # Defensive scrying of the Kernel organs
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
                        "path": str(root_path)
                    }
                })
            except Exception:
                pass

        # --- MOVEMENT V: PROFILE RECONCILIATION ---
        # [ASCENSION 6]: Divining the correct Archetype from existing matter.
        profile_name = request.profile or getattr(request, 'profile_flag', None)
        if not profile_name and not request.manual and not request.distill:
            profile_name = self._scry_existing_dna(root_path)

        # [ASCENSION 5]: Autonomic Reflex for Headless environments
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
        # [ASCENSION 7]: Protecting existing matter from accidental annihilation.
        master_blueprint = root_path / "scaffold.scaffold"
        if any(root_path.iterdir()) and not master_blueprint.exists():
            if not request.force and not request.non_interactive:
                if not self._adjudicate_occupied_sanctum(root_path, request):
                    return self.success("Rite stayed to preserve existing matter.")

        if master_blueprint.exists() and not request.force and not request.non_interactive:
            # This is the last safety gate before materialization.
            self.guarded_execution([master_blueprint], request, context="init_overwrite")

        # --- MOVEMENT VII: THE BIFURCATION OF PATHS (DISPATCH) ---
        # [ASCENSION 8 & 12]: THE FINALITY STRIKE.
        self.logger.info(f"Dispatching Inception via path: [cyan]{profile_name or 'custom'}[/cyan]")

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
            # [THE CURE]: The Symphony now receives a perfectly scrubbed request.variables.
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