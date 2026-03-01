# Path: src/velm/genesis/genesis_engine/engine.py
# -----------------------------------------------

from __future__ import annotations

import argparse
import time
import os
import sys
import gc
import json
import hashlib
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING, Tuple, List, Union

# --- Module Interfaces ---
from ..genesis_orchestrator import GenesisDialogueOrchestrator
from ..genesis_profiles import PROFILES, DEFAULT_PROFILE_NAME, list_profiles
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.data_contracts import ScaffoldItem
from ...core.alchemist import get_alchemist
from ...logger import Scribe, get_console, _COSMIC_GNOSIS

# --- Reporting & Output ---
from ...utils.dossier_scribe import proclaim_apotheosis_dossier

# --- Core Systems ---
from ...creator.engine.adjudicator import GnosticAdjudicator
from ...core.kernel.transaction import GnosticTransaction
from ...core.sentinel_conduit import SentinelConduit
from ...core.sanctum.factory import SanctumFactory
from ...creator.io_controller import IOConductor
from ...creator.registers import QuantumRegisters

# --- Mixins (Functional Capabilities) ---
from .perception import PerceptionMixin
from .communion import CommunionMixin
from .weaving import WeavingMixin
from .apotheosis import ApotheosisMixin
from .materialization import MaterializationMixin

if TYPE_CHECKING:
    from ...core import ScaffoldEngine
    from ...parser_core.parser import ApotheosisParser

Logger = Scribe("GenesisEngine")


class GenesisEngine(PerceptionMixin, CommunionMixin, WeavingMixin, ApotheosisMixin, MaterializationMixin):
    """
    The Core Orchestrator for Project Genesis.

    This class manages the end-to-end lifecycle of initializing a new software project.
    It coordinates the following phases:
    1.  **Environment Detection:** Analyzes the runtime (Native vs WASM/Emscripten) and
        adjusts I/O strategies accordingly.
    2.  **Intent Resolution:** Determines if the user wants to use a template,
        import an existing repo, or start an interactive wizard.
    3.  **Path Normalization:** Enforces absolute POSIX paths to prevent symlink
        recursion or cross-platform path separator issues.
    4.  **Transactional Execution:** Wraps file generation in an ACID-compliant
        transaction to ensure atomicity (all-or-nothing writes).
    """

    def __init__(self, project_root: Path, engine: "ScaffoldEngine"):
        """
        Initializes the engine and establishes bindings to the core runtime subsystems.
        """
        # --- System Binding ---
        self.engine = engine
        self.console = get_console()
        self.logger = Logger

        # --- Path Canonicalization ---
        # We resolve paths immediately to pierce symlinks and ensure a stable root anchor.
        # base_path: The directory containing the project.
        # project_root: The specific target directory for the project.
        self.project_root = project_root.resolve()
        self.base_path = self.project_root.parent if self.project_root else Path.cwd().resolve()

        # --- Template Engine (Alchemist) ---
        # Lazy-loaded to prevent circular imports during module initialization.
        self.alchemist = get_alchemist(engine=self.engine)

        # --- State Containers ---
        self.cli_args: Optional[argparse.Namespace] = None
        self.variables: Dict[str, Any] = {}
        self.pre_resolved_vars: Dict[str, Any] = {}
        self.orchestrator: Optional[GenesisDialogueOrchestrator] = None
        self.transaction: Optional[GnosticTransaction] = None

        # --- Request Initialization ---
        # Ensure critical flags (adrenaline_mode, trace_id) are never None.
        self.request: Any = argparse.Namespace(
            adrenaline_mode=False,
            trace_id=os.environ.get("SCAFFOLD_TRACE_ID", f"tr-gen-{uuid.uuid4().hex[:8].upper()}")
        )

        # --- I/O Abstraction Layer ---
        # We use the SanctumFactory to determine the correct filesystem driver.
        # In WASM environments, this correctly maps 'file://' to the IDBFS persistent storage.
        self.sanctum = SanctumFactory.forge(str(self.project_root), engine=self.engine)

        # --- Virtual Registers ---
        # Initialize proxy registers for the IOConductor. This allows I/O operations
        # to be routed through the transaction manager before the transaction formally begins.
        proxy_regs = QuantumRegisters(
            sanctum=self.sanctum,
            project_root=self.project_root,
            transaction=None,  # Bound later during execution
            trace_id=self.request.trace_id
        )
        self.io_conductor = IOConductor(proxy_regs)

        # --- Validation & Integrity ---
        # SentinelConduit handles external linting/analysis binaries.
        # GnosticAdjudicator validates blueprint structure against internal rules.
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

        # --- Execution Plans ---
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []
        self.items: List[ScaffoldItem] = []

        # --- Process Identification ---
        # Set process title for easier identification in system monitors (Native only).
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: genesis-engine [{self.project_root.name}]")
        except ImportError:
            pass

        self.logger.debug(
            f"GenesisEngine initialized. Root: {self.project_root.name} | Substrate: {self.sanctum.kind.name}"
        )

    @property
    def non_interactive(self) -> bool:
        """Helper accessor for CI/CD modes."""
        return getattr(self.cli_args, 'non_interactive', False)

    def conduct(self) -> None:
        """
        Executes the Genesis sequence.

        Flow:
        1.  Validate inputs and environment.
        2.  Resolve the specific blueprint/template source.
        3.  Parse and compile the blueprint into an instruction set.
        4.  Execute the build transaction.
        5.  Generate a summary report.
        """
        # --- Phase 1: Pre-flight Checks ---
        if not self.cli_args:
            raise ArtisanHeresy("GenesisEngine initialized without arguments. Aborting.")

        # Check system load to prevent hanging on resource-constrained environments (e.g. Browser Main Thread).
        self._conduct_metabolic_triage()

        try:
            # Check if target directory is empty.
            is_empty = self._is_sanctum_void()

            # CLI Flags
            is_force_willed = getattr(self.cli_args, 'force', False)
            is_distill_willed = getattr(self.cli_args, 'distill', False)
            is_silent_willed = getattr(self.cli_args, 'silent', False)

            self.logger.info("Initializing Genesis sequence...")

            # --- Phase 2: Conflict Resolution ---
            # If the directory is not empty, we offer to adopt/distill existing code unless --force is used.
            if (not is_empty and not is_force_willed) or is_distill_willed:
                self._offer_distillation_or_genesis()

            # The 'Dowry' contains the compiled instructions for the materializer.
            # Type: (Variables, ScaffoldItems, PostRunCommands, ParserInstance)
            dowry: Optional[Tuple[Dict, List[ScaffoldItem], List[Any], 'ApotheosisParser']] = None

            # --- Phase 3: Route Selection ---

            # Route A: TUI Pad (Interactive Dashboard)
            if getattr(self.cli_args, 'launch_pad_with_path', False):
                self.logger.info("Launching Interactive Genesis Pad.")
                dowry = self._conduct_pad_rite()

            # Route B: Remote URL (Git/Gist)
            elif getattr(self.cli_args, 'from_remote', None):
                self.logger.info(f"Fetching remote blueprint: {self.cli_args.from_remote}")
                self._conduct_celestial_rite(self.cli_args.from_remote)
                return

            # Route C: Manual Empty Init
            elif getattr(self.cli_args, 'manual', False):
                self.logger.info("Initializing empty project (Manual Mode).")
                self._conduct_manual_rite()
                return

            # Route D: Standard Archetype/Template
            elif getattr(self.cli_args, 'quick', False) or getattr(self.cli_args, 'profile', None):
                profile_name = getattr(self.cli_args, 'profile', None) or DEFAULT_PROFILE_NAME

                # Verify we aren't nesting a project inside itself
                self._verify_spatial_sanity(profile_name)

                archetype_info = PROFILES.get(profile_name)
                if not archetype_info:
                    available = [p['name'] for p in list_profiles()]
                    raise ArtisanHeresy(
                        f"Template '{profile_name}' not found.",
                        suggestion=f"Available templates: {', '.join(available)}"
                    )

                self.logger.success(f"Template '{profile_name}' selected. Starting build.")
                dowry = self._conduct_archetype_rite(archetype_info)

            else:
                # Route E: Interactive Wizard
                self.logger.info("No template specified. Starting interactive wizard.")
                dowry = self._conduct_dialogue_rite()

            # --- Phase 4: Materialization ---
            if dowry:
                final_gnosis, gnostic_plan, post_run_commands, parser = dowry

                # Ensure critical metadata exists for the lockfile
                if not final_gnosis.get('project_type'):
                    final_gnosis['project_type'] = (
                            getattr(self.cli_args, 'profile', None) or
                            final_gnosis.get('clean_type_name', 'generic')
                    )

                if not final_gnosis.get('project_name'):
                    final_gnosis['project_name'] = self.project_root.name

                if not final_gnosis.get('project_slug'):
                    from ...utils import to_kebab_case
                    final_gnosis['project_slug'] = to_kebab_case(final_gnosis['project_name'])

                # Set internal state
                self.post_run_commands = self._normalize_commands(post_run_commands)
                self.items = gnostic_plan
                self.variables = final_gnosis

                # EXECUTE BUILD
                registers = self._write_and_materialize(
                    final_gnosis=final_gnosis,
                    gnostic_plan=gnostic_plan,
                    post_run_commands=self.post_run_commands,
                    parser=parser
                )

                # Ensure disk buffers are flushed (Native OS only)
                if os.name != 'nt' and hasattr(os, 'sync'):
                    try:
                        os.sync()
                    except:
                        pass

                # --- Phase 5: Reporting ---
                if not is_silent_willed:
                    actual_root = (getattr(registers, 'project_root', None) or self.project_root)

                    try:
                        if hasattr(actual_root, 'resolve'):
                            actual_root_display = actual_root.resolve()
                        else:
                            actual_root_display = actual_root
                    except Exception:
                        actual_root_display = actual_root

                    # Record to global history
                    self._enshrine_in_akasha(final_gnosis, actual_root_display)

                    # Display final summary to user
                    proclaim_apotheosis_dossier(
                        telemetry_source=registers,
                        gnosis=final_gnosis,
                        project_root=actual_root_display,
                        title="✨ Project Created Successfully ✨",
                        subtitle=f"Location: {actual_root_display.name}"
                    )
            else:
                self.logger.info("Operation cancelled by user.")

        except ArtisanHeresy:
            # Pass through known errors for standard formatting
            raise
        except Exception as e:
            # Wrap unknown errors in a structured handler
            raise self._transmute_conduct_error(e)

    def _normalize_commands(self, commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """
        Normalizes post-run command tuples to a consistent 3-element format.
        (Command, LineNumber, UndoCommand)
        """
        normalized = []
        for cmd in commands:
            if isinstance(cmd, tuple):
                if len(cmd) == 3:
                    normalized.append(cmd)
                elif len(cmd) == 2:
                    normalized.append((cmd[0], cmd[1], None))
                else:
                    normalized.append((str(cmd[0]), 0, None))
            elif isinstance(cmd, str):
                normalized.append((cmd, 0, None))
        return normalized

    def _conduct_metabolic_triage(self):
        """
        Checks system resources (CPU/RAM).
        If running in a constrained environment (like a browser main thread),
        it calculates drift to prevent freezing the UI.
        """
        import gc
        import time
        import sys
        import os

        # Skip check if user explicitly requested max performance
        if getattr(self.request, "adrenaline_mode", False):
            return

        try:
            load_factor = 0.0
            substrate = "IRON"

            # Check Native Metrics
            try:
                import psutil
                load_factor = psutil.cpu_percent(interval=None)
            except (ImportError, AttributeError, Exception):
                # Fallback: WASM/Virtual Environment Heuristics
                # Measure time-drift of a short sleep to infer CPU saturation
                substrate = "ETHER"
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift = (t1 - t0) * 1000  # ms
                load_factor = min(100.0, (drift / 5.0) * 90.0)

            # --- Resource Management ---
            if load_factor > 90.0:
                self.logger.warn(
                    f"High system load detected ({load_factor:.1f}% on {substrate}). Throttling execution.")

                # Notify UI of slowdown if connected
                akashic = getattr(self.engine, 'akashic', None)
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "SYSTEM_FEVER",
                                "label": "METABOLIC_THROTTLE",
                                "color": "#f59e0b",
                                "value": load_factor
                            }
                        })
                    except:
                        pass

                # Yield to OS/Browser event loop
                yield_time = 0.5 if substrate == "IRON" else 0.05
                time.sleep(yield_time)

                # Aggressive GC if memory pressure is suspected
                if load_factor > 98.0:
                    gc.collect()
                else:
                    gc.collect(1)

                # Lower process priority on Native Windows to keep UI responsive
                if hasattr(os, 'nice') and substrate == "IRON":
                    try:
                        os.nice(1)
                    except:
                        pass

            # Memory Check (Native only)
            if substrate == "IRON":
                try:
                    import psutil
                    mem = psutil.virtual_memory()
                    if mem.percent > 95.0:
                        self.logger.critical("Memory critically low. Clearing internal caches.")
                        if hasattr(self.engine, 'alchemist'):
                            self.engine.alchemist.env.cache.clear()
                        gc.collect()
                except:
                    pass

        except Exception:
            # Triage should never crash the engine; fail open.
            pass

    def _verify_spatial_sanity(self, profile_name: str):
        """Warns if the user is creating a project with the same name as the parent folder (recursive nesting)."""
        if self.project_root.name == self.variables.get('project_name'):
            self.logger.debug("Project name matches directory name. Proceeding with in-place generation.")

    def _enshrine_in_akasha(self, gnosis: Dict, root: Path):
        """Logs the successful creation to the persistent history file."""
        try:
            from ...core.ai.akasha import AkashicRecord
            akasha = AkashicRecord()
            akasha.enshrine(
                rite_name="Genesis",
                content=f"Reality forged at {root}",
                metrics={"duration": 1.0},
                variables=gnosis
            )
        except Exception:
            pass

    def _transmute_conduct_error(self, e: Exception) -> ArtisanHeresy:
        """
        Converts generic Python exceptions into structured, user-friendly error reports.
        """
        msg = str(e)
        suggestion = "Please check the documentation or logs for more details."

        if "permission" in msg.lower():
            suggestion = "The directory is locked. Check file permissions or run with sudo."
        elif "disk full" in msg.lower():
            suggestion = "Disk space is full. Clear space and retry."

        return ArtisanHeresy(
            f"Execution Error: {type(e).__name__}",
            details=msg,
            child_heresy=e,
            suggestion=suggestion,
            severity=HeresySeverity.CRITICAL
        )