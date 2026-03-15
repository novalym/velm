# Path: core/structure_sentinel/strategies/python_strategy/engine.py
# ------------------------------------------------------------------

from __future__ import annotations
import time
import sys
import os
import traceback
import threading
from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING, List, NamedTuple, Final, Set

# --- THE DIVINE UPLINKS ---
from ..base_strategy import BaseStrategy
from .contracts import SharedContext
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from .....core.kernel.transaction import GnosticTransaction
    from .....creator.io_controller import IOConductor
    from .....logger import Scribe
    from .structural.engine import StructuralFaculty
    from .semantic.engine import SemanticFaculty
    from .frameworks import FrameworkFaculty
    from .testing.engine import TestingFaculty


class RiteConfig(NamedTuple):
    """
    =================================================================================
    == THE RITE CONFIGURATION (V-Ω-IMMUTABLE-DNA)                                  ==
    =================================================================================
    Defines the immutable laws of a single consecration step in the Gnostic Spine.
    """
    label: str
    method_name: str
    requires_source: bool
    critical: bool


class DeadlockRadar:
    """
    =============================================================================
    == THE DEADLOCK RADAR (V-Ω-AUTONOMIC-SNITCH)                               ==
    =============================================================================
    LIF: ∞ | ROLE: ANTI-FREEZE DIAGNOSTICIAN

    A background watchdog that triggers if a specific pipeline step exceeds its
    metabolic time budget. It dumps the exact stack trace of the frozen thread
    directly to stderr, annihilating the "Silent Hang" paradox.
    """

    def __init__(self, timeout_sec: float, step_name: str, target_file: str):
        self.timeout_sec = timeout_sec
        self.step_name = step_name
        self.target_file = target_file
        self.thread_id = threading.get_ident()
        self._timer: Optional[threading.Timer] = None
        self._armed = False

    def _howl(self):
        """The Scream of the Iron. Bypasses all logging locks."""
        frame = sys._current_frames().get(self.thread_id)
        stack_trace = "".join(traceback.format_stack(frame)) if frame else "Stack unmanifest."

        msg = (
            f"\n\x1b[41;1m[DEADLOCK RADAR TRIPPED]\x1b[0m\n"
            f"🚨 Thread {self.thread_id} is FROZEN in pipeline step: '{self.step_name}'\n"
            f"📍 Target Locus: {self.target_file}\n"
            f"⏳ Duration exceeded {self.timeout_sec}s.\n"
            f"🔍 STACK DUMP:\n{stack_trace}\n"
            f"=========================================================\n"
        )
        sys.stderr.write(msg)
        sys.stderr.flush()

    def arm(self):
        """Engages the temporal ward."""
        self._timer = threading.Timer(self.timeout_sec, self._howl)
        self._timer.daemon = True
        self._timer.start()
        self._armed = True

    def disarm(self):
        """Safely disengages the ward upon successful execution."""
        if self._armed and self._timer:
            self._timer.cancel()
            self._armed = False


class PythonStructureStrategy(BaseStrategy):
    """
    =================================================================================
    == THE GOVERNOR OF THE MANIFOLD (V-Ω-TOTALITY-VMAX-HYPER-DIAGNOSTIC)           ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_PYTHON_VMAX_DIAGNOSTIC_SUTURE_FINALIS_2026

    The absolute final authority on the Python code-manifold. 
    It has been radically transfigured to achieve **Zero-Stiction Concurrency**.
    The global `RLock` is annihilated. Faculties are lazy-loaded. Deadlocks are
    perceived and screamed to `stderr` in real-time.
    =================================================================================
    """

    # [ASCENSION 2]: O(1) Abyssal Fast-Fail
    ABYSSAL_ZONES: Final[Set[str]] = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea',
        '.vscode', 'dist', 'build', '.pytest_cache', '.ruff_cache'
    }

    # [ASCENSION 10]: The Memory-Mapped Sieve (5MB Limit)
    MAX_FILE_MASS_BYTES: Final[int] = 5 * 1024 * 1024

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        super().__init__("Python")

        # --- THE GNOSTIC PIPELINE (THE SPINAL FLOW) ---
        self._pipeline: Final[List[RiteConfig]] = [
            # I. FORM: The Mason forges the physical sanctum.
            RiteConfig("Structural Integrity", "ensure_structure", False, True),

            # II. MIND: The Librarian indexes the public soul and handles exports.
            RiteConfig("Semantic Discovery", "register_symbols", True, False),

            # III. LINK: The Electrician wires the frameworks and dependencies.
            RiteConfig("Framework Resonance", "wire_components", True, False),

            # IV. SHADOW: The Inquisitor materializes the verification gate.
            RiteConfig("Testing Symbiosis", "ensure_test_shadow", True, False),
        ]

        # [ASCENSION 3]: Lazy Faculty Caching (Thread-Local to prevent cross-contamination)
        self._local_state = threading.local()

    # =========================================================================
    # == LAZY FACULTY MATERIALIZATION (THE CURE FOR BOOT BLOAT)              ==
    # =========================================================================

    @property
    def structural(self) -> 'StructuralFaculty':
        if not hasattr(self._local_state, 'structural'):
            from .structural.engine import StructuralFaculty
            self._local_state.structural = StructuralFaculty(self.logger)
        return self._local_state.structural

    @property
    def semantic(self) -> 'SemanticFaculty':
        if not hasattr(self._local_state, 'semantic'):
            from .semantic.engine import SemanticFaculty
            self._local_state.semantic = SemanticFaculty(self.logger)
        return self._local_state.semantic

    @property
    def frameworks(self) -> 'FrameworkFaculty':
        if not hasattr(self._local_state, 'frameworks'):
            from .frameworks import FrameworkFaculty
            self._local_state.frameworks = FrameworkFaculty(self.logger)
        return self._local_state.frameworks

    @property
    def testing(self) -> 'TestingFaculty':
        if not hasattr(self._local_state, 'testing'):
            from .testing.engine import TestingFaculty
            self._local_state.testing = TestingFaculty(self.logger)
        return self._local_state.testing

    # =========================================================================
    # == THE GRAND RITE OF CONSECRATION                                      ==
    # =========================================================================

    def consecrate(
            self,
            path: Path,
            project_root: Path,
            transaction: Optional["GnosticTransaction"] = None,
            io_conductor: Optional["IOConductor"] = None,
            gnosis: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        =================================================================================
        == THE OMEGA PIPELINE (V-Ω-STATELESS-EXECUTION)                                ==
        =================================================================================
        """
        start_ns = time.perf_counter_ns()
        thread_id = threading.get_ident()

        # --- MOVEMENT 0: APOPHATIC FAST-FAIL (THE CURE) ---
        # [ASCENSION 2]: Annihilate processing for the Abyss before generating objects.
        abs_path = path.resolve()
        path_parts = set(abs_path.parts)
        if self.ABYSSAL_ZONES.intersection(path_parts):
            return

        # [ASCENSION 13]: The Subversion Guard
        # Never mutate internal Engine config files dynamically via this pipeline
        if ".scaffold" in path_parts and abs_path.suffix == ".py":
            return

        # --- MOVEMENT I: CONTEXTUAL INCEPTION ---
        # The Context is entirely stateless and unique to this thread's execution.
        shared_context = SharedContext(
            project_root=project_root.resolve(),
            transaction=transaction,
            logger=self.logger,
            io_conductor=io_conductor
        )

        # [ASCENSION 4]: AST Consciousness Passing (The Dowry)
        # We inject a shared cache into the local Gnosis so faculties can pass
        # parsed syntax trees to each other, saving massive I/O tax.
        active_gnosis = gnosis or {}
        if "_ast_cache" not in active_gnosis:
            active_gnosis["_ast_cache"] = {}

        # --- MOVEMENT II: SPATIAL & MASS ADJUDICATION ---
        staged_exists = False
        if transaction:
            try:
                rel = abs_path.relative_to(project_root)
                staged_exists = transaction.is_file_in_staging(rel)
            except ValueError:
                pass

        physical_exists = abs_path.exists()

        # [ASCENSION 16 & 18]: The Ghost File Suture
        if not physical_exists and not staged_exists:
            return

        # [ASCENSION 10]: Memory-Mapped Sieve
        if physical_exists and abs_path.is_file():
            try:
                if abs_path.stat().st_size > self.MAX_FILE_MASS_BYTES:
                    self.logger.warn(f"Metabolic Override: '{abs_path.name}' exceeds 5MB limit. Bypassing pipeline.")
                    return
            except OSError:
                pass

        # Triage the nature of the shard
        is_source_file = (
                (physical_exists or staged_exists)
                and abs_path.suffix == '.py'
        )

        # [ASCENSION 6]: Heuristic Pipeline Routing
        # If it's an __init__.py, it only needs structural and semantic rites, not frameworks.
        is_dunder_init = abs_path.name == '__init__.py'

        # --- MOVEMENT III: THE KINETIC PIPELINE STRIKE ---
        stats = {"success": 0, "failed": 0, "skipped": 0}

        # [ASCENSION 5]: Direct Iron Radiation Tracker
        debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        for step in self._pipeline:
            # A. PRE-STRIKE TRIAGE
            if step.requires_source and not is_source_file:
                stats["skipped"] += 1
                continue

            # [ASCENSION 6]: Heuristic Skip
            if is_dunder_init and step.method_name in ("wire_components", "ensure_test_shadow"):
                stats["skipped"] += 1
                continue

            # B. THE KINETIC EXECUTION
            rite_start_ns = time.perf_counter_ns()

            # [ASCENSION 1]: THE DEADLOCK RADAR (THE SNITCH)
            # We arm a 5-second timer. If this step freezes (e.g., waiting on disk I/O),
            # the Radar will scream the stack trace to the terminal.
            radar = DeadlockRadar(timeout_sec=5.0, step_name=step.label, target_file=abs_path.name)
            radar.arm()

            try:
                # 1. FACULTY DISPATCH
                faculty = self._resolve_faculty(step.method_name)
                rite = getattr(faculty, step.method_name)

                # 2. CONDUCT RITE
                if step.method_name == "ensure_structure":
                    rite(abs_path, shared_context, gnosis=active_gnosis)
                else:
                    rite(abs_path, shared_context)

                # 3. METABOLIC TOMOGRAPHY
                duration_ms = (time.perf_counter_ns() - rite_start_ns) / 1_000_000

                # [ASCENSION 5]: Direct Iron Radiation for Heavy Rites
                if debug_mode and duration_ms > 50.0:
                    sys.stderr.write(
                        f"\x1b[90m[T:{thread_id}] {step.label} on {abs_path.name}: {duration_ms:.2f}ms\x1b[0m\n")
                    sys.stderr.flush()

                stats["success"] += 1

            except Exception as paradox:
                # [ASCENSION 15]: SOCRATIC ERROR TRIAGE & FAULT ISOLATION
                stats["failed"] += 1

                tb_str = traceback.format_exc()
                error_msg = f"\n\x1b[41;1m[GOVERNOR:FRACTURE]\x1b[0m {step.label} on {abs_path.name}\n{tb_str}\n"

                # Radiate the fracture to stderr immediately for real-time autopsy.
                sys.stderr.write(error_msg)
                sys.stderr.flush()

                if step.critical:
                    # [ASCENSION 14]: Achronal State Rollback
                    if transaction:
                        self.logger.critical(f"Lattice Collapse in '{step.label}'. Cancelling transaction.")
                        transaction.cancel()
                    break
                else:
                    self.logger.warn(f"   -> [Non-Critical] {step.label} deferred: {str(paradox)}")

            finally:
                # [ASCENSION 22]: The Finality Vow (Disarm the Radar)
                radar.disarm()

                # [ASCENSION 9]: Hydraulic Thread Yielding
                # If we successfully processed a step, yield tiny fraction to OS scheduler
                if not debug_mode:
                    time.sleep(0.001)

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 19]: Haptic Progress Multicast
        if transaction and hasattr(transaction.engine, 'akashic') and transaction.engine.akashic:
            try:
                transaction.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "PIPELINE_COMPLETE",
                        "label": f"CONSECRATED: {abs_path.name}",
                        "color": "#64ffda",
                        "trace": transaction.tx_id[:8]
                    }
                })
            except Exception:
                pass

        if self.logger.is_verbose and total_duration_ms > 10.0:
            self.logger.debug(
                f"Governor: Consecration of '{abs_path.name}' concluded in {total_duration_ms:.2f}ms. "
                f"({stats['success']}s, {stats['failed']}f, {stats['skipped']}k)"
            )

    def _resolve_faculty(self, method_name: str):
        """
        Maps the requested rite to the correct internal organ (Lazy Loaded).
        """
        if "structure" in method_name: return self.structural
        if "symbols" in method_name: return self.semantic
        if "wire" in method_name: return self.frameworks
        if "test" in method_name: return self.testing
        return self.structural

    def __repr__(self) -> str:
        return (
            f"<Ω_PYTHON_GOVERNOR status=RESONANT mode=STATELESS_CONCURRENCY "
            f"version=VMAX-DIAGNOSTIC-SUTURE>"
        )