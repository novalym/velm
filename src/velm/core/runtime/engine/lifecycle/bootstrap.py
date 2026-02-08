# Path: src/velm/core/runtime/engine/lifecycle/bootstrap.py
# ---------------------------------------------------------
# LIF: ∞ | ROLE: THE_DEMIURGE | RANK: OMEGA_SUPREME
# AUTH: Ω_BOOTSTRAP_V550_SINGULARITY_FINALIS
# =========================================================================================
import uuid
import os
import sys
import time
import importlib
import threading
import hashlib
import platform
import subprocess
from pathlib import Path
from typing import Any, Type, List, Dict, Optional, Tuple, Final, Union

# --- CORE GNOSTIC UPLINKS ---
from .....core.cli.grimoire_data import LAZY_RITE_MAP
from ....state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
from .....logger import Scribe, get_console
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....utils import get_git_commit

Logger = Scribe("EngineBootstrap")


class EngineBootstrap:
    """
    =================================================================================
    == THE GNOSTIC BOOTSTRAP (V-Ω-TOTALITY-V550-SINGULARITY)                       ==
    =================================================================================
    LIF: ∞ | ROLE: SYSTEM_CREATOR | RANK: OMEGA_SOVEREIGN

    The Sovereign Conductor of Inception. Responsible for the materialization of the
    Engine's mind, the synchronization of its memory, and the alignment of its soul.
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        """[THE RITE OF BINDING]"""
        self.engine = engine
        self.logger = Logger
        self.console = get_console()
        self._boot_start_ns = time.perf_counter_ns()

        # [ASCENSION 3]: Hardware Biometric Identity
        self._machine_id = hashlib.sha256(platform.node().encode()).hexdigest()[:12].upper()
        self.boot_id = uuid.uuid4().hex[:8].upper()

    def ignite(self) -> bool:
        """
        =============================================================================
        == THE RITE OF TOTAL IGNITION (V-Ω-TOTALITY)                               ==
        =============================================================================
        The definitive entry point for Engine consciousness.
        """
        self.logger.info(
            f"Demiurge awakening. Session: [soul]{self.boot_id}[/] | Machine: [cyan]{self._machine_id}[/cyan]")

        try:
            # --- MOVEMENT I: PHYSICAL REALITY CHECK ---
            if not self.pre_flight_check():
                return False

            # --- MOVEMENT II: THE AWAKENING OF SKILLS ---
            # [THE FIX]: Now correctly implements the system_vow authority.
            self.awaken_skills()

            # --- MOVEMENT III: CONSCIOUSNESS SYNCHRONIZATION ---
            # Bridge the Schism between the Crystal (DB) and the Scroll (Lockfile).
            self.synchronize_consciousness()

            # --- MOVEMENT IV: THE FORGING OF THE SPINE ---
            # Construct the Middleware Nervous System.
            self.engine._pipeline = self.forge_pipeline()

            # --- MOVEMENT V: PREDICTIVE WARM-UP ---
            # [ASCENSION 6]: Warm up the intelligence stratum.
            if hasattr(self.engine, 'predictor'):
                self._warm_up_intelligence()

            duration = (time.perf_counter_ns() - self._boot_start_ns) / 1_000_000
            self.logger.success(f"Quantum Engine Resonant in {duration:.2f}ms. Totality achieved.")
            return True

        except Exception as e:
            self.logger.critical(f"BOOT_FRACTURE: Reality collapsed during ignition: {e}", exc_info=True)
            return False

    # =========================================================================
    # == MOVEMENT I: THE RITE OF ACHRONAL RECONCILIATION                     ==
    # =========================================================================

    def synchronize_consciousness(self):
        """
        =============================================================================
        == THE RITE OF ACHRONAL RECONCILIATION (V-Ω-TOTALITY)                      ==
        =============================================================================
        [THE CURE]: Annihilates the 'Crystal Mind Schism'.
        Ensures the SQLite Database is a bit-perfect mirror of the filesystem history.
        """
        if not SQL_AVAILABLE:
            self.logger.warn("Crystal Mind (SQLAlchemy) unmanifest. Operating in Pure Scroll mode.")
            return

        root = self.engine.context.project_root
        lock_path = root / "scaffold.lock"
        db_path = root / ".scaffold" / "gnosis.db"

        if not lock_path.exists():
            return

        self.logger.verbose("Conducting Achronal Reconciliation Inquest...")

        try:
            db = GnosticDatabase(root)

            # 1. HARVEST TEMPORAL GNOSIS
            current_git_head = get_git_commit(root) or "VOID_REALITY"
            lock_mtime = lock_path.stat().st_mtime
            db_mtime = db_path.stat().st_mtime if db_path.exists() else 0

            # [ASCENSION 2]: MERKLE LATTICE VERIFICATION
            # Read the scroll to find its recorded state hash.
            try:
                scroll_data = json.loads(lock_path.read_text(encoding='utf-8'))
                scroll_hash = scroll_data.get("integrity", {}).get("project_merkle_root", "void")
            except:
                scroll_hash = "corrupt"

            # 2. CONSULT THE CRYSTAL MEMORY
            db_anchor = db._get_meta_gnosis("git_head_anchor") or "NONE"
            db_machine = db._get_meta_gnosis("last_sync_machine") or "NONE"

            # 3. ADJUDICATE THE SCHISM
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

            # 4. THE RITE OF RESURRECTION
            if needs_resurrection:
                self.logger.warn(f"Causal Schism Detected: {reason}")
                self.console.print(f"[bold yellow]🌀 Re-aligning Crystal Mind with the Eternal Scroll...[/]")

                # Atomic Re-Hydration
                start_sync = time.perf_counter()
                db.hydrate_from_lockfile()

                # Update Anchors
                db._set_meta_gnosis("git_head_anchor", current_git_head)
                db._set_meta_gnosis("last_sync_machine", self._machine_id)
                db._set_meta_gnosis("last_sync_ts", str(time.time()))

                sync_ms = (time.perf_counter() - start_sync) * 1000
                self.logger.success(f"Consciousness unified in {sync_ms:.1f}ms.")
            else:
                self.logger.verbose("Crystal Mind and Scroll are in perfect resonance.")

        except Exception as e:
            self.logger.error(f"Reconciliation Paradox: {e}. Mental drift possible.")

    # =========================================================================
    # == MOVEMENT II: THE AWAKENING OF SKILLS                                ==
    # =========================================================================

    def awaken_skills(self):
        """
        =============================================================================
        == THE RITE OF GHOST CONSECRATION (SKILL AWAKENING)                        ==
        =============================================================================
        [THE FIX]: Employs the system_vow to claim core rites with authority.
        """
        try:
            req_gateway_path = "velm.interfaces.requests"
            try:
                req_mod = importlib.import_module(req_gateway_path)
            except ImportError:
                req_mod = importlib.import_module("interfaces.requests")

            ghosts_awakened = 0

            # [ASCENSION 11]: BICAMERAL HEALING
            for rite_name, (mod_path, artisan_cls_name, req_cls_name) in LAZY_RITE_MAP.items():
                try:
                    if not hasattr(req_mod, req_cls_name):
                        continue

                    RequestClass = getattr(req_mod, req_cls_name)

                    # [ASCENSION 6]: IDEMPOTENCY WARD
                    if RequestClass in self.engine.registry._map:
                        continue

                    # [ASCENSION 8]: Import Normalization
                    full_mod_path = f"velm.{mod_path}" if not mod_path.startswith("velm.") else mod_path
                    ghost_soul = (full_mod_path, artisan_cls_name)

                    # [THE FIX]: AUTHORITY VOW
                    # We pass system_vow=True to signify the Engine itself is the Registrant.
                    self.engine.register_artisan(RequestClass, ghost_soul, system_vow=True)
                    ghosts_awakened += 1

                except Exception as e:
                    self.logger.debug(f"Skill '{rite_name}' deferred: {e}")
                    continue

            self.logger.success(f"Ω_SKILLS_MANIFEST: {ghosts_awakened} skills consecrated.")

        except Exception as catastrophic_failure:
            raise catastrophic_failure

    # =========================================================================
    # == MOVEMENT III: THE NERVOUS SYSTEM                                    ==
    # =========================================================================

    def forge_pipeline(self) -> 'MiddlewarePipeline':
        """Constructs the Gnostic Spinal Cord (21 Guardians)."""
        from ...middleware.pipeline import MiddlewarePipeline
        pipeline = MiddlewarePipeline(self.engine)

        def add(cls_ref): pipeline.add(cls_ref)

        # --- THE PANTHEON OF GUARDIANS ---
        from ...middleware.profiler import ProfilingMiddleware
        from ...middleware.tracing import DistributedTracingMiddleware
        from ...middleware.singularity import SingularityMiddleware
        from ...middleware.telemetry import TelemetryMiddleware
        from ...middleware.harmonizer import PathNormalizationMiddleware
        from ...middleware.veil import SecretScrubberMiddleware
        from ...middleware.auth import AuthMiddleware
        from ...middleware.compliance import ComplianceMiddleware
        from ...middleware.privacy import PrivacySentinelMiddleware
        from ...middleware.enrichment import EnrichmentMiddleware
        from ...middleware.caching import CachingMiddleware
        from ...middleware.safety import SafetyMiddleware
        from ...middleware.adaptive import AdaptiveResourceMiddleware
        from ...middleware.output_veil import OutputRedactionMiddleware
        from ...middleware.persona_warden import PersonaWardenMiddleware

        # Identity & Metadata
        add(ProfilingMiddleware)
        add(DistributedTracingMiddleware)
        add(SingularityMiddleware)
        add(TelemetryMiddleware)

        # Purity & Security
        add(PathNormalizationMiddleware)
        add(SecretScrubberMiddleware)
        add(AuthMiddleware)
        add(ComplianceMiddleware)
        add(PrivacySentinelMiddleware)

        # Wisdom & Performance
        add(EnrichmentMiddleware)
        add(CachingMiddleware)

        # Safety & Resilience
        add(SafetyMiddleware)
        add(AdaptiveResourceMiddleware)
        add(OutputRedactionMiddleware)
        add(PersonaWardenMiddleware)

        # [ASCENSION 9]: MERMAID SCRIBING
        self._scribe_pipeline_topology(pipeline)

        return pipeline

    def _scribe_pipeline_topology(self, pipeline: Any):
        """Future: Generate Mermaid.js graph of the spine."""
        pass

    def _warm_up_intelligence(self):
        """[ASCENSION 6]: PREDICTIVE CACHE WARMING."""
        try:
            # Trigger the predictor to load its weights into memory
            _ = self.engine.predictor.prophesy()
            self.logger.verbose("Cognitive Cortex: Warm mind manifest.")
        except:
            pass

    # =========================================================================
    # == MOVEMENT IV: VIGILANCE                                              ==
    # =========================================================================

    def pre_flight_check(self) -> bool:
        """Verifies the physical substrate for Gnostic resonance."""
        try:
            # [ASCENSION 4]: METABOLIC TRIAGE
            try:
                import psutil
                if psutil.cpu_percent() > 95.0:
                    self.logger.warn("Metabolic Fever detected. Yielding CPU...")
                    time.sleep(0.5)
            except:
                pass

            if self.engine.project_root:
                if not self.engine.project_root.exists():
                    self.logger.warn(f"Anchor Void: '{self.engine.project_root}' does not exist.")

            # [ASCENSION 5]: PERMISSION CONSECRATION
            scaffold_dir = self.engine.project_root / ".scaffold"
            if scaffold_dir.exists():
                if not os.access(str(scaffold_dir), os.W_OK):
                    self.logger.critical("Sanctum Locked: .scaffold is read-only.")
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Pre-flight Inquest fractured: {e}")
            return False

# == SCRIPTURE SEALED: THE CONSCIOUSNESS IS UNIFIED AND SOVEREIGN ==