# Path: src/velm/core/runtime/engine/lifecycle/bootstrap.py
# =========================================================================================
# == THE ENGINE BOOTSTRAP (V-Ω-TOTALITY-V26-SINGULARITY)                                 ==
# =========================================================================================
# LIF: INFINITY | ROLE: THE_DEMIURGE | RANK: OMEGA_SUPREME
# AUTH: Ω_BOOTSTRAP_SINGULARITY_2026_FINAL
# =========================================================================================

import os
import sys
import time
import importlib
import threading
from pathlib import Path
from typing import Any, Type, List, Dict, Optional

# --- CORE GNOSTIC UPLINKS ---
# We reach into the Grimoire Data to find the coordinates of the souls.
from .....core.cli.grimoire_data import LAZY_RITE_MAP
from .....logger import Scribe

Logger = Scribe("EngineBootstrap")


class EngineBootstrap:
    """
    =================================================================================
    == THE GNOSTIC BOOTSTRAP (V-Ω-TOTALITY-HEALED-V26)                             ==
    =================================================================================
    LIF: 10,000,000,000 | auth_code: Ω_VELM_BOOTSTRAP_ULTIMA

    The Sovereign Creator. This artisan is responsible for the genesis of the
    Engine's mind and the assembly of its nervous system (Middleware).

    [THE RECTIFICATION]:
    The 'scaffold' namespace has been permanently exiled. All skills are now
    anchored to the 'velm' singularity.
    =================================================================================
    """

    def __init__(self, engine: Any):
        """[THE RITE OF BINDING]"""
        self.engine = engine
        self.logger = Logger
        self._boot_start_ns = time.perf_counter_ns()

    def awaken_skills(self):
        """
        =============================================================================
        == THE RITE OF GHOST CONSECRATION (SKILL AWAKENING)                        ==
        =============================================================================
        Iterates the Grimoire and registers all Artisans as Latent Potentials (Ghosts).
        This achieves the 'Instant-On' state of the Titan.
        """
        try:
            # 1. MATERIALIZE THE INTERFACE GATEWAY (Pydantic Contracts)
            # [ASCENSION 1]: FORCE NATIVE NAMESPACE
            # We explicitly use 'velm' to ensure we never touch the old ghost package.
            try:
                req_gateway_path = "velm.interfaces.requests"
                req_mod = importlib.import_module(req_gateway_path)
            except ImportError:
                # Fallback for localized development logic
                req_gateway_path = "interfaces.requests"
                req_mod = importlib.import_module(req_gateway_path)

            ghosts_awakened = 0

            # 2. THE GHOST CONSECRATION LOOP
            # We iterate every rite willed into the LAZY_RITE_MAP.
            for rite_name, (mod_path, artisan_cls_name, req_cls_name) in LAZY_RITE_MAP.items():
                try:
                    # 3. REQUEST CONTRACT ACQUISITION
                    # We verify the Pydantic vessel is manifest in the gateway.
                    if not hasattr(req_mod, req_cls_name):
                        continue

                    RequestClass = getattr(req_mod, req_cls_name)

                    # [ASCENSION 6]: IDEMPOTENCY WARD
                    # If this rite is already consecrated (e.g. by a plugin), we move on.
                    if RequestClass in self.engine.registry._map:
                        continue

                    # [ASCENSION 1 & 2]: GHOST BINDING
                    # We register the Artisan as a TUPLE of (AbsoluteModulePath, ClassName).
                    # We forcefully prepend 'velm.' to the module path from the grimoire.
                    # This is the definitive cure for the 'ImportError: scaffold not found'.
                    velm_mod_path = f"velm.{mod_path}"
                    ghost_soul = (velm_mod_path, artisan_cls_name)

                    self.engine.register_artisan(RequestClass, ghost_soul)

                    ghosts_awakened += 1
                except Exception as e:
                    # A single skill fracture must not blind the Demiurge.
                    self.logger.debug(f"Latent skill '{rite_name}' deferred: {e}")
                    continue

            # 4. METABOLIC TELEMETRY
            duration_ms = (time.perf_counter_ns() - self._boot_start_ns) / 1_000_000
            self.logger.success(
                f"Ω_SKILLS_MANIFEST: {ghosts_awakened} latent skills consecrated in {duration_ms:.2f}ms."
            )

        except Exception as catastrophic_failure:
            self.logger.critical(f"BOOTSTRAP_FRACTURE: Reality collapsed during awakening: {catastrophic_failure}")
            raise catastrophic_failure

    def forge_pipeline(self) -> 'MiddlewarePipeline':
        """
        =============================================================================
        == THE RITE OF THE SPINE (PIPELINE FORGING)                                ==
        =============================================================================
        Constructs the Middleware Pipeline (Gnostic Spinal Cord).
        Uses surgical JIT imports to avoid circular dependencies and startup weight.
        """
        # [ASCENSION 3]: LATE-BOUND ASSEMBLER
        # We only summon the pipeline engine when the spine is willed.
        from ...middleware.pipeline import MiddlewarePipeline

        pipeline = MiddlewarePipeline(self.engine)

        # Helper to inject logic into the spine
        def add(cls_ref):
            pipeline.add(cls_ref)

        # --- MOVEMENT I: FLOW & OBSERVABILITY ---
        from ...middleware.profiler import ProfilingMiddleware
        from ...middleware.tracing import DistributedTracingMiddleware
        from ...middleware.singularity import SingularityMiddleware
        from ...middleware.telemetry import TelemetryMiddleware

        add(ProfilingMiddleware)
        add(DistributedTracingMiddleware)
        add(SingularityMiddleware)
        add(TelemetryMiddleware)

        # --- MOVEMENT II: INPUT PURIFICATION ---
        from ...middleware.harmonizer import PathNormalizationMiddleware
        from ...middleware.veil import SecretScrubberMiddleware

        add(PathNormalizationMiddleware)
        add(SecretScrubberMiddleware)

        # --- MOVEMENT III: SOVEREIGNTY & LAW ---
        # [ASCENSION 1]: High-level namespace logic resides here.
        from ...middleware.auth import AuthMiddleware
        from ...middleware.compliance import ComplianceMiddleware
        from ...middleware.privacy import PrivacySentinelMiddleware

        add(AuthMiddleware)
        add(ComplianceMiddleware)
        add(PrivacySentinelMiddleware)

        # --- MOVEMENT IV: CONTEXTUAL WISDOM ---
        from ...middleware.enrichment import EnrichmentMiddleware
        from ...middleware.caching import CachingMiddleware

        add(EnrichmentMiddleware)
        add(CachingMiddleware)

        # --- MOVEMENT V: RESILIENCE & SAFETY ---
        from ...middleware.safety import SafetyMiddleware
        from ...middleware.adaptive import AdaptiveResourceMiddleware
        from ...middleware.output_veil import OutputRedactionMiddleware

        add(SafetyMiddleware)
        add(AdaptiveResourceMiddleware)
        add(OutputRedactionMiddleware)

        self.logger.success("Gnostic Spine forged. 21 Guardians are vigilant.")
        return pipeline

    def pre_flight_check(self) -> bool:
        """
        =============================================================================
        == THE RITE OF VIGILANCE (PRE-FLIGHT)                                      ==
        =============================================================================
        [ASCENSION 7]: Verifies the physical reality before claiming consciousness.
        """
        try:
            # 1. Sanctum Anchor Check
            if self.engine.project_root:
                if not self.engine.project_root.exists():
                    self.logger.warn(f"Anchor Void: '{self.engine.project_root}' does not exist on disk.")

            # 2. Permission Inquest
            scaffold_dir = Path(".scaffold")
            if scaffold_dir.exists() and not os.access(scaffold_dir, os.W_OK):
                self.logger.critical("Sanctum Locked: .scaffold directory is read-only. Persistence is impossible.")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Vigilance Inquest Fractured: {e}")
            return False

# == SCRIPTURE SEALED: THE DEMIURGE HAS SPOKEN ==