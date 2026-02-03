# Path: core/runtime/engine/lifecycle/bootstrap.py
# ------------------------------------------------

import os
import sys
import time
import importlib
import threading
from pathlib import Path
from typing import Any, Type, List, Dict
from .....core.cli.grimoire_data import LAZY_RITE_MAP
from .....logger import Scribe


# [ASCENSION 1]: JIT IMPORT GUARD
# We defer importing the Middleware classes until `forge_pipeline` is called
# to prevent module-level execution cost at startup.

class EngineBootstrap:
    """
    =============================================================================
    == THE BOOTSTRAP (V-Ω-JIT-CONSECRATION)                                    ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: THE_CREATOR

    Orchestrates the awakening of the Engine.
    1.  **Ghost Consecration:** Registers 100+ skills as lazy tuples.
    2.  **Spine Assembly:** Constructs the Middleware Pipeline.
    3.  **Pre-Flight Checks:** Verifies environmental integrity.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Scribe("EngineBootstrap")
        self._boot_start = time.perf_counter()

    def awaken_skills(self):
        """
        [THE RITE OF GHOSTS]
        Iterates the Grimoire and registers all Artisans as Ghosts (Lazy Tuples).
        This reduces boot time from seconds to milliseconds.
        """
        try:
            # 1. Materialize the Interface Gateway
            # We need the Pydantic models to register the keys.
            try:
                req_mod = importlib.import_module("scaffold.interfaces.requests")
            except ImportError:
                req_mod = importlib.import_module("interfaces.requests")

            count = 0
            ghosts = 0

            # 2. Iterate the Grimoire
            for rite_name, (mod_path, artisan_cls_name, req_cls_name) in LAZY_RITE_MAP.items():
                try:
                    # Resolve Request Class
                    if not hasattr(req_mod, req_cls_name):
                        continue

                    RequestClass = getattr(req_mod, req_cls_name)

                    # Idempotency check (Don't overwrite if manually registered)
                    if RequestClass in self.engine.registry._map:
                        continue

                    # [THE MIRACLE]: Register the Ghost (Tuple)
                    # The Registry knows how to inflate this JIT when 'get()' is called.
                    ghost_data = (f"scaffold.{mod_path}", artisan_cls_name)
                    self.engine.register_artisan(RequestClass, ghost_data)

                    ghosts += 1
                except Exception:
                    continue

            duration = (time.perf_counter() - self._boot_start) * 1000
            # self.logger.debug(f"Awakened {ghosts} latent skills in {duration:.2f}ms.")

        except ImportError as e:
            self.logger.critical(f"Core Grimoire manifest missing. Skill awakening aborted: {e}")

    def forge_pipeline(self):
        """
        [THE RITE OF THE SPINE]
        Constructs the Middleware Pipeline.
        Uses surgical imports to avoid circular dependencies and startup weight.
        """

        from ...middleware.pipeline import MiddlewarePipeline
        from ...middleware.contract import Middleware

        pipeline = MiddlewarePipeline(self.engine)
        ENABLE_TRACING = os.environ.get("SCAFFOLD_TRACE") == "1"

        def add(cls_ref):
            pipeline.add(cls_ref)

        # --- IMPORT MIDDLEWARE (SURGICAL) ---
        # =========================================================================
        # == THE CURE: PRIMARY SOVEREIGNTY GUARD                                 ==
        # =========================================================================
        # This MUST be added first (or very early) to ensure all subsequent
        # database interactions are shrouded.
        from ...middleware.privacy import PrivacySentinelMiddleware
        add(PrivacySentinelMiddleware)
        # =========================================================================
        # 1. Flow & Observability
        from ...middleware.profiler import ProfilingMiddleware
        from ...middleware.tracing import DistributedTracingMiddleware
        from ...middleware.singularity import SingularityMiddleware
        from ...middleware.telemetry import TelemetryMiddleware

        add(ProfilingMiddleware)
        add(DistributedTracingMiddleware)
        add(SingularityMiddleware)
        add(TelemetryMiddleware)

        # 2. Input Hygiene
        from ...middleware.harmonizer import PathNormalizationMiddleware
        from ...middleware.veil import SecretScrubberMiddleware

        add(PathNormalizationMiddleware)
        add(SecretScrubberMiddleware)

        # 3. Policy & Security
        from ...middleware.auth import AuthMiddleware
        from ...middleware.compliance import ComplianceMiddleware

        add(AuthMiddleware)
        add(ComplianceMiddleware)

        # 4. Context & Data
        from ...middleware.enrichment import EnrichmentMiddleware
        from ...middleware.caching import CachingMiddleware

        add(EnrichmentMiddleware)
        add(CachingMiddleware)

        # 5. Execution Guard
        from ...middleware.safety import SafetyMiddleware

        add(SafetyMiddleware)

        # 6. Output Hygiene
        from ...middleware.output_veil import OutputRedactionMiddleware

        add(OutputRedactionMiddleware)

        # 7. Adaptive Resilience (New)
        from ...middleware.adaptive import AdaptiveResourceMiddleware
        add(AdaptiveResourceMiddleware)

        return pipeline

    def pre_flight_check(self) -> bool:
        """
        [THE RITE OF VIGILANCE]
        Verifies the integrity of the runtime environment before ignition.
        """
        try:
            # 1. Check Root Access
            if self.engine.project_root:
                if not self.engine.project_root.exists():
                    self.logger.warn(f"Project Anchor {self.engine.project_root} is a void.")

            # 2. Check Write Access to Scaffold Dir
            scaffold_dir = Path(".scaffold")
            if scaffold_dir.exists() and not os.access(scaffold_dir, os.W_OK):
                self.logger.warn(".scaffold directory is read-only. Persistence will fail.")

            return True
        except Exception as e:
            self.logger.error(f"Pre-flight fracture: {e}")
            return False

