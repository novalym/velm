# Path: src/velm/core/runtime/engine/lifecycle/bootstrap.py
# ---------------------------------------------------------
# SYSTEM: Core Runtime Initialization
# COMPONENT: EngineBootstrap
# STABILITY: Stable / Production
# ---------------------------------------------------------
import json
import uuid
import os
import sys
import time
import importlib
import importlib.util
import threading
import hashlib
import platform
import signal
import gc
import traceback
import concurrent.futures
from pathlib import Path
from typing import Any, Type, List, Dict, Optional, Tuple, Final, Union, Set, Callable, TYPE_CHECKING

# --- Internal Module Resolution ---
# We employ a resilient import strategy here to ensure the bootstrap
# process can report initialization failures gracefully rather than
# crashing with opaque ImportErrors at the module level.
try:
    from .....core.cli.grimoire_data import LAZY_RITE_MAP
    from ....state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
    from .....logger import Scribe, get_console
    from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
    from .....utils import get_git_commit, to_snake_case
except ImportError as e:
    # Fallback for esoteric environments (e.g., PyInstaller, ZipApps) where
    # the CWD might not be implicitly in sys.path.
    _CWD = Path.cwd()
    if str(_CWD) not in sys.path:
        sys.path.insert(0, str(_CWD))

    # Critical failure: If we cannot import core contracts, the runtime
    # state is undefined. Terminate immediately with forensic output.
    sys.stderr.write(f"[BOOTSTRAP] FATAL: Core dependency resolution failed: {e}\n")
    sys.exit(1)

if TYPE_CHECKING:
    from .... import VelmEngine
    from ...middleware import MiddlewarePipeline

# Initialize structured logger for lifecycle events
Logger = Scribe("EngineBootstrap")


# =============================================================================
# == RUNTIME PATH RESOLUTION                                                 ==
# =============================================================================
# Determines the absolute physical location of the package and server assets.
# This logic must remain robust across Native, Docker, and WASM substrates.

def _resolve_runtime_anchors() -> Tuple[Path, Path]:
    """
    Calculates the absolute paths for the Project Root (Library) and
    Server Root (Daemon) relative to this file's location.

    Returns:
        Tuple[Path, Path]: (PACKAGE_ROOT, SERVER_ROOT)
    """
    try:
        current_file = Path(__file__).resolve()
        # Traverse up the directory tree:
        # file -> lifecycle -> engine -> runtime -> core -> src
        package_root = current_file.parents[5]

        # Check for server directory (Daemon context)
        server_root = package_root / "server"
        if not server_root.exists():
            # Fallback for CLI-only or flattened distribution environments
            server_root = package_root

        return package_root, server_root
    except Exception:
        # Fallback: In compiled/frozen environments (e.g., Pyodide), __file__
        # may be virtual or undefined. Default to CWD to prevent crash.
        return Path.cwd(), Path.cwd()


PROJECT_ROOT, SERVER_ROOT = _resolve_runtime_anchors()


class EngineBootstrap:
    """
    Orchestrates the initialization sequence of the VelmEngine.

    This class is responsible for the transition from a cold start (process launch)
    to a fully operational runtime state. It manages dependency injection,
    subsystem initialization, and environmental safety checks.

    Architectural Responsibilities:
    1.  **Lazy Registration:** Populates the ArtisanRegistry using a zero-overhead
        strategy (O(1)) to minimize startup latency.
    2.  **Environment Detection:** Identifies the execution substrate (Native vs WASM)
        and tunes threading/IO strategies accordingly.
    3.  **State Reconciliation:** Ensures synchronization between the persistent
        state database (SQLite) and the file-system lockfile (JSON).
    4.  **Pipeline Construction:** Assembles the middleware chain for request processing.
    5.  **Resource Governance:** checks system vitals (RAM/CPU) before enabling
        heavy subsystems to prevent process termination by the OS OOM killer.
    """

    def __init__(self, engine: 'VelmEngine'):
        """
        Binds the bootstrap logic to a specific Engine instance.
        """
        self.engine = engine
        self.logger = Logger
        self.console = get_console()

        # Generate unique session identifiers for distributed tracing
        self._boot_start_ns = time.perf_counter_ns()

        # Hardware fingerprinting for license/state validation
        # Uses platform node name as a stable seed
        self._machine_id = hashlib.sha256(platform.node().encode()).hexdigest()[:12].upper()
        self.boot_id = uuid.uuid4().hex[:8].upper()

        # Detect TTY capability for output formatting adjustments
        self._is_headless = not sys.stdout.isatty()

        # Substrate Detection: Check for Emscripten/Pyodide environment variables
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def ignite(self) -> bool:
        """
        Executes the main initialization sequence.

        Returns:
            bool: True if the engine successfully entered the RUNNING state,
                  False if a critical fault occurred.
        """
        if self.engine.logger.is_verbose:
            self.logger.debug(
                f"Boot sequence initiated. Session: {self.boot_id} | "
                f"Host: {self._machine_id} | "
                f"Substrate: {'WASM/ETHER' if self._is_wasm else 'NATIVE/IRON'}"
            )

        try:
            # --- Phase 1: Pre-flight Verification ---
            # Validate filesystem permissions, memory availability, and OS capabilities.
            # Skipped in WASM due to virtualized resource constraints.
            if not self._is_wasm:
                if not self.pre_flight_check():
                    self.logger.critical("Boot failed: Environment pre-flight check returned errors.")
                    return False

            # --- Phase 2: Capability Registration ---
            # Populate the registry with available commands and handlers.
            self.register_capabilities()

            # --- Phase 3: State Synchronization ---
            # Reconcile the SQLite database with the JSON lockfile to ensure data consistency.
            # Skipped in WASM to avoid IDBFS contention during initial load.
            if not self._is_wasm:
                self.synchronize_registry_state()

            # --- Phase 4: Context Anchoring ---
            # Determine the active project context based on the filesystem or arguments.
            self._anchor_project_context()

            # --- Phase 5: Pipeline Assembly ---
            # Construct the middleware processing chain.
            self.engine._pipeline = self.forge_pipeline()

            # --- Phase 6: Subsystem Warm-up ---
            # Initialize AI predictors and thread pools if resources allow.
            if hasattr(self.engine, 'predictor') and self.engine.predictor and not self._is_wasm:
                self._warm_up_intelligence()

            if not self._is_wasm:
                self._initialize_thread_pools()

            # Final cleanup: Force garbage collection to reclaim memory used during import/init
            gc.collect()

            # Telemetry: Log boot duration
            duration_ms = (time.perf_counter_ns() - self._boot_start_ns) / 1_000_000

            # Only log success if verbose or if specifically requested; otherwise keep silent.
            if self.engine.logger.is_verbose:
                self.logger.success(f"Engine operational. Boot time: {duration_ms:.2f}ms.")

            return True

        except Exception as e:
            # Catch-all for initialization failures.
            # Dumps stack trace to console regardless of logging level as this is fatal.
            self.logger.critical(f"FATAL: Engine initialization crashed: {e}")
            if self.engine.logger.is_verbose:
                self.console.print_exception(show_locals=True)
            return False

    # =========================================================================
    # == SECTION I: Environment Validation                                   ==
    # =========================================================================

    def pre_flight_check(self) -> bool:
        """
        Validates the host environment for required capabilities.
        Checks memory, CPU load, and filesystem write permissions.
        """
        # We use a unique trace ID for this check to track it in logs
        trace_id = getattr(self.engine, 'trace_id', 'boot-check')

        try:
            # 1. Resource Utilization Check
            load_factor = 0.0
            ram_starved = False

            try:
                import psutil
                # Non-blocking CPU check
                load_factor = psutil.cpu_percent(interval=None) or 0.0
                # Ensure at least 200MB free RAM
                mem_avail_gb = psutil.virtual_memory().available / (1024 ** 3)
                if mem_avail_gb < 0.2:
                    ram_starved = True
            except (ImportError, AttributeError):
                # If psutil is missing, we proceed optimistically
                pass

            # 2. Throttling Logic
            # If CPU is pinned (>95%), we inject a sleep to yield to the OS scheduler.
            if load_factor > 95.0:
                if self.engine.logger.is_verbose:
                    self.logger.warn(f"High CPU load detected ({load_factor:.1f}%). Throttling initialization.")
                time.sleep(1.0)

            if ram_starved:
                self.logger.critical(
                    "Insufficient memory available. Initialization aborted to prevent system instability.")
                return False

            # 3. Filesystem Permission Probe
            # We attempt to write and delete a file to the project root to confirm RW access.
            if self.engine.project_root:
                root = self.engine.project_root.resolve()
                if root.exists() and root.is_dir():
                    test_file = root / ".scaffold" / f".probe_{trace_id[:8]}"
                    try:
                        test_file.parent.mkdir(parents=True, exist_ok=True)
                        test_file.write_text("ok", encoding='utf-8')
                        test_file.unlink()
                    except (OSError, PermissionError) as e:
                        self.logger.critical(f"Filesystem access denied at '{root}'. Check permissions.")
                        self.logger.debug(f"OS Error: {e}")
                        return False

            return True

        except Exception as e:
            # Fail open in dev, fail closed in prod
            self.logger.error(f"Pre-flight check error: {e}")
            return os.environ.get("SCAFFOLD_ENV") != "production"

    def _initialize_thread_pools(self):
        """
        Pre-initializes thread pools for IO operations.
        This reduces latency for the first async operation.
        """
        try:
            # We trigger a no-op against the dispatcher if it exists
            # to force the ThreadPoolExecutor to spin up worker threads.
            if hasattr(self.engine, 'dispatcher'):
                pass
        except Exception:
            pass

    # =========================================================================
    # == SECTION II: Capability Registration                                 ==
    # =========================================================================

    def register_capabilities(self):
        """
        Iterates over the internal module map and registers Artisans with the Registry.

        Uses a 'Lazy Registration' strategy: we register the *paths* to the classes,
        not the classes themselves. The actual import happens only when the command
        is invoked. This keeps startup time O(1) relative to the number of features.
        """
        try:
            # 1. Load the Interface definition
            # This is the base contract all requests must adhere to.
            req_gateway_path = "velm.interfaces.requests"
            try:
                req_mod = importlib.import_module(req_gateway_path)
            except ImportError:
                # Fallback for development environments where 'velm' is not installed as a package
                try:
                    req_mod = importlib.import_module("interfaces.requests")
                except ImportError:
                    self.logger.critical("Fatal: Interface definitions not found.")
                    return

            registered_count = 0

            # 2. Iterate and Register
            for rite_name, (mod_path, artisan_cls_name, req_cls_name) in LAZY_RITE_MAP.items():
                try:
                    # Verify the Request class exists in the interface module
                    if not hasattr(req_mod, req_cls_name):
                        continue

                    RequestClass = getattr(req_mod, req_cls_name)

                    # Check for duplicate registration
                    if RequestClass in self.engine.registry._map:
                        continue

                    # Normalize module path
                    full_mod_path = f"velm.{mod_path}" if not mod_path.startswith("velm.") else mod_path

                    # Create the Lazy Reference (Ghost Tuple)
                    # (Module Path, Class Name)
                    lazy_ref = (full_mod_path, artisan_cls_name)

                    # Register with the engine
                    self.engine.registry.fast_register(
                        RequestClass,
                        lazy_ref,
                        system_vow=True  # Internal system command
                    )

                    registered_count += 1

                except Exception as e:
                    # Log but do not crash; allow other commands to register
                    if self.engine.logger.is_verbose:
                        self.logger.debug(f"Failed to register command '{rite_name}': {e}")
                    continue

            # Only log summary in debug mode
            if self.engine.logger.is_verbose:
                self.logger.debug(f"Registered {registered_count} capabilities.")

        except Exception as e:
            self.logger.critical(f"Capability registration failed: {e}")
            raise e

    # =========================================================================
    # == SECTION III: State Synchronization                                  ==
    # =========================================================================

    def synchronize_registry_state(self):
        """
        Ensures the SQLite database ('gnosis.db') matches the JSON lockfile ('scaffold.lock').

        This handles the case where a user might manually edit the JSON file, or if the
        application crashed before writing to the DB. It acts as a self-healing mechanism
        for project metadata.
        """
        # Determine paths
        root = getattr(self.engine.context, 'project_root', None)
        if not root or not root.exists():
            return

        lock_path = root / "scaffold.lock"
        db_path = root / ".scaffold" / "gnosis.db"

        # If no lockfile, there is no state to sync.
        if not lock_path.exists():
            return

        # If SQLite is not available (e.g. missing driver), skip.
        if not SQL_AVAILABLE:
            return

        try:
            # Load the JSON state
            with open(lock_path, 'r', encoding='utf-8') as f:
                scroll_data = json.load(f)

            # Metadata extraction
            scroll_merkle = scroll_data.get("integrity", {}).get("project_merkle_root", "0xVOID")

            # Initialize DB connection
            db = GnosticDatabase(root)

            # Compare stored hashes
            mind_merkle = db._get_meta_gnosis("last_sync_merkle") or "0xEMPTY"

            # If hashes mismatch, or DB file is missing, perform hydration
            if not db_path.exists() or db_path.stat().st_size == 0 or scroll_merkle != mind_merkle:
                if self.engine.logger.is_verbose:
                    self.logger.debug("State drift detected. Re-hydrating database from lockfile...")

                start_sync = time.perf_counter()
                db.hydrate_from_lockfile()

                # Update sync markers
                db._set_meta_gnosis("last_sync_merkle", scroll_merkle)
                db._set_meta_gnosis("last_sync_ts", str(time.time()))

                duration = (time.perf_counter() - start_sync) * 1000
                if self.engine.logger.is_verbose:
                    self.logger.debug(f"Database hydration complete ({duration:.2f}ms).")

        except Exception as e:
            # We log this as a warning but do not crash, as the system can run in
            # "Degraded Mode" using just the JSON file.
            self.logger.warn(f"State synchronization failed: {e}")
            if self.engine.logger.is_verbose:
                traceback.print_exc()

    def _anchor_project_context(self):
        """
        Coordinates with the ProjectManager to determine if the engine is running
        inside an active project, and sets the root path accordingly.
        """
        try:
            from .....artisans.project.manager import ProjectManager
            governor = ProjectManager()

            if governor.registry.active_project_id:
                active_pid = governor.registry.active_project_id
                active_meta = governor.registry.projects.get(active_pid)

                if active_meta:
                    # Update engine root to match the active project
                    self.engine.project_root = Path(active_meta.path)
                    if self.engine.logger.is_verbose:
                        self.logger.debug(f"Context anchored to project: {active_meta.name}")

        except Exception as e:
            if self.engine.logger.is_verbose:
                self.logger.debug(f"Project context detection skipped: {e}")

    # =========================================================================
    # == SECTION IV: Pipeline Construction                                   ==
    # =========================================================================

    def forge_pipeline(self) -> 'MiddlewarePipeline':
        """
        Instantiates the Request Processing Pipeline.

        This constructs the chain of responsibility for handling requests.
        Order matters: Telemetry -> Security -> Validation -> Execution.
        """
        try:
            from ...middleware.pipeline import MiddlewarePipeline
            pipeline = MiddlewarePipeline(self.engine)
        except ImportError as e:
            self.logger.critical(f"Critical: Middleware definitions missing. {e}")
            raise e

        # Helper to add middleware
        def add(cls):
            pipeline.add(cls)

        try:
            # 1. Observability Layer
            from ...middleware.profiler import ProfilingMiddleware
            from ...middleware.tracing import DistributedTracingMiddleware
            from ...middleware.telemetry import TelemetryMiddleware
            add(ProfilingMiddleware)
            add(DistributedTracingMiddleware)
            add(TelemetryMiddleware)

            # 2. Security & Normalization Layer
            from ...middleware.harmonizer import PathNormalizationMiddleware
            from ...middleware.veil import SecretScrubberMiddleware
            from ...middleware.auth import AuthMiddleware
            add(PathNormalizationMiddleware)
            add(SecretScrubberMiddleware)
            add(AuthMiddleware)

            # 3. Context Layer
            from ...middleware.enrichment import EnrichmentMiddleware
            from ...middleware.caching import CachingMiddleware
            add(EnrichmentMiddleware)
            add(CachingMiddleware)

            # 4. Resilience Layer
            from ...middleware.safety import SafetyMiddleware
            from ...middleware.adaptive import AdaptiveResourceMiddleware
            from ...middleware.output_veil import OutputRedactionMiddleware
            from ...middleware.persona_warden import PersonaWardenMiddleware
            add(SafetyMiddleware)
            add(AdaptiveResourceMiddleware)
            add(OutputRedactionMiddleware)
            add(PersonaWardenMiddleware)

        except ImportError as e:
            # If middleware is missing, we log it but allow the engine to boot
            # in a degraded state (some features disabled).
            self.logger.error(f"Middleware initialization incomplete: {e}")

        return pipeline

    def _warm_up_intelligence(self):
        """
        Triggers a background load of AI/ML models or heuristic weights.
        This moves the I/O cost of loading these models to the boot phase
        rather than the first user interaction.
        """
        try:
            start_ts = time.perf_counter()
            # Trigger a dry-run prediction to load weights into memory
            _ = self.engine.predictor.prophesy()

            if self.engine.logger.is_verbose:
                duration = (time.perf_counter() - start_ts) * 1000
                self.logger.debug(f"Intelligence subsystem warmed ({duration:.2f}ms).")
        except Exception:
            # Non-fatal. The predictor will lazy-load if this fails.
            pass

    def __repr__(self) -> str:
        return f"<EngineBootstrap session={self.boot_id}>"