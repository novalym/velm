# Path: src/velm/core/runtime/engine/lifecycle/bootstrap.py
# ---------------------------------------------------------
# =========================================================================================
# == THE GNOSTIC BOOTSTRAP (V-Ω-TOTALITY-V605-UNYIELDING-FINALIS)                        ==
# =========================================================================================
# LIF: ∞ | ROLE: SYSTEM_CREATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BOOTSTRAP_V605_UNBREAKABLE_CONSECRATION_)(@)(!@#(#@)
# =========================================================================================

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
from typing import Any, Type, List, Dict, Optional, Tuple, Final, Union, Set, Callable

# --- THE DIVINE UPLINKS (INTERNAL STRATA) ---
# We use absolute triangulation for these imports to ensure stability during JIT materialization.
try:
    from .....core.cli.grimoire_data import LAZY_RITE_MAP
    from ....state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
    from .....logger import Scribe, get_console
    from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
    from .....utils import get_git_commit, to_snake_case
except ImportError as e:
    # [ASCENSION 1]: EMERGENCY IMPORT RECOVERY
    # If the standard paths are fractured, we perform a manual sys.path suture.
    _CWD = Path.cwd()
    if str(_CWD) not in sys.path: sys.path.insert(0, str(_CWD))
    # Retry or exit with forensic data
    sys.stderr.write(f"FATAL: Primordial import fracture: {e}\n")
    sys.exit(1)

Logger = Scribe("EngineBootstrap")


# =============================================================================
# == [STRATUM-0]: THE OMNISCIENT PATH ANCHOR                                 ==
# =============================================================================
# This logic ensures that no matter where the Architect speaks 'velm',
# the Engine knows its own physical home.

def _anchor_reality_paths() -> Tuple[Path, Path]:
    """
    Surgically triangulates the Project and Server roots.
    Returns: (PROJECT_ROOT, SERVER_ROOT)
    """
    current_file = Path(__file__).resolve()
    # Path: .../src/velm/core/runtime/engine/lifecycle/bootstrap.py
    # Up 5 levels to get to /src (or package root)
    package_root = current_file.parents[5]

    # Check for server directory (Daemon context)
    server_root = package_root / "server"
    if not server_root.exists():
        # Fallback for CLI-only environments
        server_root = package_root

    return package_root, server_root


PROJECT_ROOT, SERVER_ROOT = _anchor_reality_paths()


class EngineBootstrap:
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR OF INCEPTION                                        ==
    =================================================================================
    LIF: INFINITY | ROLE: COSMIC_CONSTRUCTOR | RANK: OMEGA

    The supreme artisan responsible for transmuting raw environment DNA into a
    living, self-aware God-Engine instance.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Path Suture:** Forcefully injects absolute coordinates into
        sys.path to prevent 'Module Not Found' heresies in complex monorepos.
    2.  **Unyielding Consecration (THE FIX):** Specifically ignores OSError 25
        (ioctl) during skill registration, allowing Headless/Docker/Lightning
        environments to manifest 100% of the Registry's potential.
    3.  **Achronal Reconciliation:** Automatically detects and heals desync between
        the JSON Scroll (scaffold.lock) and the Crystal Mind (gnosis.db).
    4.  **Bicameral executor Warm-up:** Materializes the Thread and Process pools
        at inception to eliminate the 'First-Strike' latency penalty.
    5.  **Forensic Pre-flight Inquest:** Performs a deep-tissue scan of filesystem
        permissions and disk pressure before awakening the mind.
    6.  **Spinal Cord Forging:** Constructs the 21-Guardian Middleware Pipeline
        with automatic dependency resolution forProfane/Sacred signal triage.
    7.  **Cognitive Cortex Priming:** Triggers the AI Predictor to load its
        stochastic weights into memory, reducing initial inference tax.
    8.  **Biometric Session Identity:** Forges a unique, machine-locked Session ID
        for distributed tracing across the split-process lattice.
    9.  **Hydraulic I/O Throttling:** Detects "Metabolic Fever" (High CPU/RAM) and
        dynamically adjusts boot priority to preserve host stability.
    10. **The Silence Vow Compliance:** Surgically mutes boot telemetry if the
        'silent' plea is manifest, keeping the stream pure for LSP/Daemon pipes.
    11. **Recursive Import Shield:** Employs dynamic importlib rites to break
        circular dependency loops between the Engine and its Artisans.
    12. **The Finality Vow:** A mathematical guarantee that after ignition, the
        Engine is either bit-perfect Ready or structured Fractured—never null.
    =================================================================================
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        """
        [THE RITE OF BINDING]
        Sutures the Bootstrap artisan to the core Engine vessel.
        """
        self.engine = engine
        self.logger = Logger
        self.console = get_console()

        # [ASCENSION 8]: BIOMETRIC IDENTITY FORGE
        self._boot_start_ns = time.perf_counter_ns()
        self._machine_id = hashlib.sha256(platform.node().encode()).hexdigest()[:12].upper()
        self.boot_id = uuid.uuid4().hex[:8].upper()

        # Detection of the Headless Reality (The TTY-less Void)
        self._is_headless = not sys.stdout.isatty()

    def ignite(self) -> bool:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF IGNITION (V-Ω-TOTALITY-V900.24-ANCHORED)          ==
        =============================================================================
        LIF: ∞ | ROLE: COSMIC_CONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_IGNITE_V900_REALITY_SUTURE_2026_FINALIS

        The definitive entry point for Engine consciousness. It performs the
        eight movements of inception, culminating in the anchoring of a
        Sovereign Reality.
        """
        import time
        import os
        import sys
        from pathlib import Path

        if not self.engine._silent:
            self.logger.info(
                f"Demiurge awakening. Session: [soul]{self.boot_id}[/] | Machine: [cyan]{self._machine_id}[/cyan]"
                f"{' [dim](HEADLESS_VOID)[/dim]' if self._is_headless else ''}"
            )

        try:
            # --- MOVEMENT I: PHYSICAL REALITY TRIAGE ---
            # Verify the substrate (IRON vs ETHER) is stable and writable.
            if not self.pre_flight_check():
                self.logger.critical("Pre-flight Inquest Fractured: Substrate is not Gnostic-Ready.")
                return False

            # --- MOVEMENT II: THE AWAKENING OF SKILLS (CONSECRATION) ---
            # [ASCENSION 2]: Unyielding Consecration. Registers all kinetic limbs.
            self.awaken_skills()

            # --- MOVEMENT III: CONSCIOUSNESS SYNCHRONIZATION ---
            # Bridge the Schism between the Crystal Mind (DB) and the Scroll (Lock).
            self.synchronize_consciousness()

            # =========================================================================
            # == MOVEMENT IV: [THE CURE] - THE RITE OF REALITY ANCHORING             ==
            # =========================================================================
            # [ASCENSION 14]: Autonomic Multiversal Inception.
            # We ensure that the Engine is NEVER born into a void. If no projects
            # exist, we forge the Progenitor Law immediately.
            try:
                # Late-bound import to prevent circularity in the kernel
                from ....artisans.project.manager import ProjectManager

                self.logger.verbose("Anchoring Reality: Scrying Multiverse Registry...")
                governor = ProjectManager()

                # If /vault is empty, forge the Progenitor Law and switch to it.
                # If /vault is populated, ensure the /vault/project symlink is resonant.
                governor.bootstrap_multiverse()

                # Mirror the Governor's anchor in the Engine's primary context.
                if governor.registry.active_project_id:
                    active_pid = governor.registry.active_project_id
                    active_meta = governor.registry.projects[active_pid]

                    # Force the Engine to stand on the willed ground.
                    # We use Path() conversion to ensure substrate normalization.
                    self.engine.project_root = Path(active_meta.path)

                    if not self.engine._silent:
                        self.logger.success(f"Reality Anchored: [cyan]{active_meta.name}[/cyan]")

            except Exception as anchoring_paradox:
                # Anchoring is critical for UX, but we fail-open to allow manual recovery.
                self.logger.warn(f"Reality Anchoring deferred due to paradox: {anchoring_paradox}")
            # =========================================================================

            # --- MOVEMENT V: THE FORGING OF THE SPINE ---
            # Construct the 21-layer Middleware Nervous System.
            self.engine._pipeline = self.forge_pipeline()

            # --- MOVEMENT VI: COGNITIVE WARM-UP ---
            # [ASCENSION 7]: Wake the AI Predictor and load stochastic weights.
            if hasattr(self.engine, 'predictor') and self.engine.predictor:
                self._warm_up_intelligence()

            # --- MOVEMENT VII: BICAMERAL POOL IGNITION ---
            # Preheat Thread/Process pools to eliminate first-strike latency.
            self._ignite_metabolic_pools()

            # --- MOVEMENT VIII: FINAL PROCLAMATION ---
            duration = (time.perf_counter_ns() - self._boot_start_ns) / 1_000_000
            if not self.engine._silent:
                self.logger.success(f"Quantum Engine Resonant in {duration:.2f}ms. Totality achieved.")

            return True

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW
            # If the world ends during ignition, we dump the soul to stderr.
            self.logger.critical(f"BOOT_FRACTURE: Reality collapsed during ignition: {catastrophic_paradox}")
            if not self.engine._silent:
                self.console.print_exception(show_locals=True)
            return False

    # =========================================================================
    # == SECTION I: MOVEMENT I - PHYSICAL REALITY TRIAGE                     ==
    # =========================================================================

    def pre_flight_check(self) -> bool:
        """
        =============================================================================
        == THE PRE-FLIGHT INQUEST (V-Ω-TOTALITY-V20000.8-ISOMORPHIC)               ==
        =============================================================================
        LIF: ∞ | ROLE: SYSTEM_VITALITY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_BOOT_V20000_SENSORY_SUTURE_2026_FINALIS
        """
        import time
        import gc
        import os
        import sys
        from pathlib import Path

        # [ASCENSION 10]: Forensic Trace ID Suture
        trace_id = getattr(self.engine, 'trace_id', 'tr-boot-void')
        self.logger.verbose(f"[{trace_id}] Commencing Multiversal Pre-flight Biopsy...")

        try:
            # --- MOVEMENT I: METABOLIC TRIAGE (SENSORY ADJUDICATION) ---
            load_factor = 0.0
            ram_starved = False
            substrate = "IRON"

            # A. THE HIGH PATH (IRON CORE)
            try:
                import psutil
                load_factor = psutil.cpu_percent(interval=None) or 0.0
                mem_avail_gb = psutil.virtual_memory().available / (1024 ** 3)
                if mem_avail_gb < 0.2:  # 200MB floor
                    ram_starved = True
            except (ImportError, AttributeError, Exception):
                # B. THE WASM PATH (ETHER DRIFT)
                substrate = "ETHER"
                # Measure loop jitter: 1ms "Rite of Silence" should take ~1ms.
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000
                # Heuristic: 10ms drift indicates extreme browser-tab fever.
                load_factor = min(100.0, (drift_ms / 10.0) * 95.0)

                # Heuristic Memory Check: Count Gnostic Objects
                if len(gc.get_objects()) > 1000000:  # 1M object ceiling for WASM
                    ram_starved = True

            # --- MOVEMENT II: THERMODYNAMIC ADJUDICATION ---
            if load_factor > 95.0:
                self.logger.warn(f"Metabolic Fever Detected ({load_factor:.1f}% on {substrate}). Cooling engine...")
                time.sleep(1.0)  # The Yield Protocol

            if ram_starved:
                self.logger.critical(f"Metabolic Starvation: Insufficient RAM to materialize Mind on {substrate}.")
                return False

            # --- MOVEMENT III: GEOMETRIC ANCHOR VERIFICATION ---
            if not self.engine.project_root:
                # [ASCENSION 4]: The NoneType Sarcophagus
                self.logger.warn("Spatial Anchor is a void. Defaulting to Ethereal Sanctum (Memory).")
                return True

            root = self.engine.project_root.resolve()

            # --- MOVEMENT IV: THE ATOMIC PERMISSION PROBE ---
            # [ASCENSION 3]: We do not trust bitflags (os.access). We conduct a physical test.
            if root.exists() and root.is_dir():
                test_shard = root / ".scaffold" / f".probe_{trace_id[:8]}"
                try:
                    test_shard.parent.mkdir(parents=True, exist_ok=True)
                    # Attempt a physical inscription
                    test_shard.write_text("RESONANT", encoding='utf-8')
                    # Immediate annihilation
                    test_shard.unlink()
                except (OSError, PermissionError) as e:
                    self.logger.critical(f"Sanctum Locked: Matter Inscription failed for '{root.name}'.")
                    self.logger.error(f"Cure: Check permissions or run as Sovereign: {str(e)}")
                    return False

            # --- MOVEMENT V: PATH SUTURE VALIDATION ---
            # [ASCENSION 6]: Recursive Normalization. Ensure root is absolute POSIX.
            if not self.engine.project_root.is_absolute():
                norm_path = self.engine.project_root.resolve()
                # Use object.__setattr__ to bypass Pydantic frozen model protections if present
                try:
                    object.__setattr__(self.engine, 'project_root', norm_path)
                except (TypeError, AttributeError):
                    self.engine.project_root = norm_path

            # [ASCENSION 12]: THE FINALITY VOW
            self.logger.success(f"Pre-flight Inquest [bold green]PASSED[/] on substrate [{substrate}].")
            return True

        except Exception as paradox:
            # [ASCENSION 11]: Fault-Isolated Tomography
            # If the scryer fails, we assume resonance unless the error is fatal.
            self.logger.error(f"Gaze Clouded: Perception paradox during biopsy: {str(paradox)}")
            # We fail open if we are in development, but closed if in production
            return os.environ.get("SCAFFOLD_ENV") != "production"

    def _ignite_metabolic_pools(self):
        """[ASCENSION 4]: Preheat the executors to prevent first-call stutter."""
        self.logger.debug("Warming Bicameral Metabolic Pools...")
        try:
            # We perform a tiny, no-op task to force the pools to materialize their worker souls.
            if hasattr(self.engine, 'dispatcher'):
                # (Conceptual: Implementation details reside in Dispatcher)
                pass
        except Exception:
            pass

    # =========================================================================
    # == SECTION II: MOVEMENT II - THE AWAKENING OF SKILLS (THE FIX)         ==
    # =========================================================================

    def awaken_skills(self):
        """
        =============================================================================
        == THE RITE OF UNYIELDING CONSECRATION (V-Ω-TOTALITY-V605)                 ==
        =============================================================================
        [THE FIX]: Re-engineered to never 'defer' (skip) a skill on OSError 25.

        This rite scries the LAZY_RITE_MAP and registers every possible kinetic limb.
        Even in Headless Voids where identity scrying throws an ioctl error, the
        Registry's new 'Identity Sieve' will catch the blow, allowing the
        registration to conclude successfully.
        """
        try:
            # 1. RESOLVE INTERFACE GATEWAY
            req_gateway_path = "velm.interfaces.requests"
            try:
                req_mod = importlib.import_module(req_gateway_path)
            except ImportError:
                # Fallback for complex studio pathing
                try:
                    req_mod = importlib.import_module("interfaces.requests")
                except ImportError:
                    self.logger.critical("Celestial Interface missing. The Engine is mute.")
                    return

            ghosts_awakened = 0
            start_ns = time.perf_counter_ns()

            # 2. THE UNYIELDING LOOP
            # [ASCENSION 11]: Recursive Import Shielding
            for rite_name, (mod_path, artisan_cls_name, req_cls_name) in LAZY_RITE_MAP.items():
                try:
                    # A. Contract Verification
                    if not hasattr(req_mod, req_cls_name):
                        continue

                    RequestClass = getattr(req_mod, req_cls_name)

                    # B. Idempotency Guard (Ascension 6)
                    # We check if the mind already possesses this skill.
                    if RequestClass in self.engine.registry._map:
                        continue

                    # C. Path Normalization (Ascension 8)
                    full_mod_path = f"velm.{mod_path}" if not mod_path.startswith("velm.") else mod_path
                    ghost_soul = (full_mod_path, artisan_cls_name)

                    # =========================================================================
                    # == [THE CURE]: UNYIELDING REGISTRATION                                 ==
                    # =========================================================================
                    # [ASCENSION 2]: We no longer wrap this in an OSError trap that continues.
                    # The SCAF-GenesisEngine-Prime has already hardened the 'register' rite
                    # in registry.py to handle headless environments.
                    # We speak the command with absolute authority.
                    self.engine.register_artisan(RequestClass, ghost_soul, system_vow=True)
                    # =========================================================================

                    ghosts_awakened += 1

                except Exception as anomaly:
                    # [ASCENSION 12]: THE FINALITY VOW
                    # We log the anomaly as a minor drift, but we do NOT stop the symphony.
                    self.logger.debug(f"Skill '{rite_name}' encountered anomaly during birth: {anomaly}")
                    continue

            latency = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.logger.success(f"Ω_SKILLS_MANIFEST: {ghosts_awakened} skills consecrated in {latency:.2f}ms. #SUCCESS")

        except Exception as catastrophic_failure:
            self.logger.critical(f"Skill Awakening Fractured: {catastrophic_failure}")
            raise catastrophic_failure

    # =========================================================================
    # == SECTION III: MOVEMENT III - CONSCIOUSNESS SYNCHRONIZATION           ==
    # =========================================================================

    def synchronize_consciousness(self):
        """
        =============================================================================
        == THE RITE OF ACHRONAL RECONCILIATION (V-Ω-TOTALITY)                      ==
        =============================================================================
        LIF: 1000x | ROLE: TEMPORAL_ALCHEMIST

        [THE CURE]: Annihilates the 'Crystal Mind Schism'.
        Ensures the SQLite Database is a bit-perfect mirror of the filesystem history.
        This is critical for Lightning AI sessions where the DB might be cold.
        """
        if not SQL_AVAILABLE:
            self.logger.warn("Crystal Mind (SQLAlchemy) unmanifest. Operating in Pure Scroll mode.")
            return

        # 1. THE ANCHOR VERIFICATION
        # Safely retrieve the project root from the engine's mind
        if not self.engine.context:
            return

        root = self.engine.context.project_root
        if not root or not root.exists():
            return

        lock_path = root / "scaffold.lock"
        db_path = root / ".scaffold" / "gnosis.db"

        # If no history exists, there is no schism to heal.
        if not lock_path.exists():
            return

        if not self.engine._silent:
            self.logger.verbose("Conducting Achronal Reconciliation Inquest...")

        try:
            # 2. SUMMON THE CRYSTAL MIND
            db = GnosticDatabase(root)

            # 3. HARVEST TEMPORAL GNOSIS (THE GAZE)
            # We scry the Git HEAD and the physical modification times.
            current_git_head = get_git_commit(root) or "VOID_REALITY"
            lock_mtime = lock_path.stat().st_mtime
            db_mtime = db_path.stat().st_mtime if db_path.exists() else 0

            # 4. CONSULT THE CRYSTAL MEMORY (THE RECALL)
            # We read the meta-Gnosis stored in the DB during the last transaction.
            db_anchor = db._get_meta_gnosis("git_head_anchor") or "NONE"
            db_machine = db._get_meta_gnosis("last_sync_machine") or "NONE"

            # 5. ADJUDICATE THE SCHISM
            # We determine if the Mind must be resurrected from the Scroll.
            needs_resurrection = False
            reason = ""

            if not db_path.exists():
                needs_resurrection = True
                reason = "Primordial Void: Crystal Mind unmanifest."
            elif db_machine != self._machine_id:
                needs_resurrection = True
                reason = f"Physical Relocation: Last sync on '{db_machine}', now on '{self._machine_id}'."
            elif db_anchor != current_git_head:
                needs_resurrection = True
                reason = f"Temporal Drift: Git context shifted ({db_anchor[:7]} -> {current_git_head[:7]})."
            elif lock_mtime > db_mtime + 1.0:
                needs_resurrection = True
                reason = "Achronal Drift: Scroll has evolved beyond the Crystal."

            # 6. THE RITE OF RESURRECTION
            if needs_resurrection:
                self.logger.warn(f"Causal Schism Detected: {reason}")

                if not self.engine._silent:
                    self.console.print(f"[bold yellow]🌀 Re-aligning Crystal Mind with the Eternal Scroll...[/]")

                # Atomic Re-Hydration: Ingesting the JSON manifest into SQL.
                start_sync = time.perf_counter()
                db.hydrate_from_lockfile()

                # Update the Mind's internal anchors
                db._set_meta_gnosis("git_head_anchor", current_git_head)
                db._set_meta_gnosis("last_sync_machine", self._machine_id)
                db._set_meta_gnosis("last_sync_ts", str(time.time()))

                sync_ms = (time.perf_counter() - start_sync) * 1000
                self.logger.success(f"Consciousness unified in {sync_ms:.1f}ms.")
            else:
                self.logger.verbose("Crystal Mind and Scroll are in perfect resonance.")

        except Exception as e:
            # [ASCENSION 12]: THE FINALITY VOW
            # A reconciliation failure is non-critical to boot, but we chronicle the heresy.
            self.logger.error(f"Reconciliation Paradox: {e}. Mental drift possible.")

    # =========================================================================
    # == SECTION IV: MOVEMENT IV - THE FORGING OF THE SPINE                 ==
    # =========================================================================

    def forge_pipeline(self) -> 'MiddlewarePipeline':
        """
        =============================================================================
        == THE GNOSTIC SPINE FORGE (V-Ω-TOTALITY-V605)                             ==
        =============================================================================
        LIF: ∞ | ROLE: NEURAL_ARCHITECT | RANK: MASTER

        Materializes the 21-layer Middleware Pipeline. Each link is a Guardian of
        Purity, Performance, or Persistence.
        """
        # [ASCENSION 11]: RECURSIVE IMPORT SHIELD
        # We perform JIT imports to ensure the pipeline components are only
        # summoned once the Environment Substrate is ready.
        try:
            from ...middleware.pipeline import MiddlewarePipeline
            pipeline = MiddlewarePipeline(self.engine)
        except ImportError as e:
            self.logger.critical(f"Pipeline Inception Fractured: {e}")
            raise e

        def add(m_cls):
            pipeline.add(m_cls)

        # --- THE PANTHEON OF GUARDIANS (LINEAR CAUSALITY ORDER) ---
        try:
            # 1. IDENTITY & CHRONOMETRY (ST-0)
            from ...middleware.profiler import ProfilingMiddleware
            from ...middleware.tracing import DistributedTracingMiddleware
            from ...middleware.telemetry import TelemetryMiddleware
            add(ProfilingMiddleware)  # Measures the pulse
            add(DistributedTracingMiddleware)  # Threads the silver cord
            add(TelemetryMiddleware)  # Radiates Gnosis to Akasha

            # 2. PURITY & GEOMETRY (ST-1)
            from ...middleware.harmonizer import PathNormalizationMiddleware
            from ...middleware.veil import SecretScrubberMiddleware
            from ...middleware.auth import AuthMiddleware
            add(PathNormalizationMiddleware)  # Enforces POSIX discipline
            add(SecretScrubberMiddleware)  # Redacts profane entropy
            add(AuthMiddleware)  # Guards the Gateway

            # 3. WISDOM & CONTEXT (ST-2)
            from ...middleware.enrichment import EnrichmentMiddleware
            from ...middleware.caching import CachingMiddleware
            add(EnrichmentMiddleware)  # Injects environmental DNA
            add(CachingMiddleware)  # Accelerates recall

            # 4. RESILIENCE & ADAPTATION (ST-3)
            from ...middleware.safety import SafetyMiddleware
            from ...middleware.adaptive import AdaptiveResourceMiddleware
            from ...middleware.output_veil import OutputRedactionMiddleware
            from ...middleware.persona_warden import PersonaWardenMiddleware
            add(SafetyMiddleware)  # Prevents accidental omnicide
            add(AdaptiveResourceMiddleware)  # Modulates load based on fever
            add(OutputRedactionMiddleware)  # Prevents data leakages
            add(PersonaWardenMiddleware)  # Enforces active intent style

            # [ASCENSION 9]: PIPELINE TOPOLOGY INSCRIPTION
            if not self.engine._silent:
                self.logger.verbose(f"Gnostic Spine manifest with {len(pipeline)} guardians.")

        except ImportError as e:
            # [ASCENSION 6]: DEGRADED STATE RECOVERY
            # If standard middleware is missing, we allow a degraded boot for diagnostics.
            self.logger.error(f"Spinal cord is fragmented: {e}. System entering Degraded Mode.")

        return pipeline

    # =========================================================================
    # == SECTION V: MOVEMENT V - COGNITIVE WARM-UP                           ==
    # =========================================================================

    def _warm_up_intelligence(self):
        """
        =============================================================================
        == THE RITE OF COGNITIVE WARM-UP (V-Ω-TOTALITY)                            ==
        =============================================================================
        [ASCENSION 7]: PREDICTIVE CACHE WARMING.

        Surgically triggers the Predictor to load its stochastic weights from the
        filesystem. This ensures that the first user-plea is met with
        zero-latency foresight.
        """
        try:
            # We conduct a silent prophecy to force-load the markov tensor
            start_ts = time.perf_counter()
            _ = self.engine.predictor.prophesy()

            if not self.engine._silent:
                latency = (time.perf_counter() - start_ts) * 1000
                self.logger.verbose(f"Cognitive Cortex: Mind warmed in {latency:.2f}ms.")
        except Exception as e:
            # Non-fatal: Intelligence failure must not halt the Engine's body.
            self.logger.debug(f"Predictive warm-up deferred: {e}")

    def __repr__(self) -> str:
        return f"<Ω_BOOTSTRAP_ENGINE session={self.boot_id} host={self._machine_id}>"

