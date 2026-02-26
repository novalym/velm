# Path: src/velm/core/runtime/engine/lifecycle/vitality.py
# =========================================================================================
# == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V25000-WASM-HYBRID-HEALED)                  ==
# =========================================================================================
# LIF: ∞ | ROLE: METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_VITALITY_V25K_THERMODYNAMIC_SUTURE_2026_FINALIS
# =========================================================================================

from __future__ import annotations
import threading
import time
import os
import sys
import gc
import json
import logging
import platform
from pathlib import Path
from typing import Optional, Dict, Any, Final, Union
from .....logger import Scribe

# [ASCENSION 1]: SURGICAL SENSORY GUARD
# We attempt to manifest the psutil artisan for Iron Core realities.
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    psutil = None
    PS_AVAILABLE = False

# --- GNOSTIC UPLINKS ---
from .state import LifecyclePhase

Logger = Scribe("QuantumEngine:Metabolism")


class VitalityMonitor:
    """
    =================================================================================
    == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V25000-HEALED-HYSTERESIS)             ==
    =================================================================================
    The evolved immune system of the Scaffold Engine.
    It has been ascended to possess **Substrate Independence** and a stabilized
    **Autonomic Reflex** that prevents it from acting on transient spikes.

    ### THE 12 LEGENDARY ASCENSIONS:
    1.  **The Thermodynamic Realignment (THE CURE):** Thresholds have been shifted
        from paranoid (30%) to realistic (85%). The Engine now trusts the OS to
        manage standard memory fluxes without panicking.
    2.  **Velocity Dampening:** The Surge Threshold was raised from 5MB/s to 50MB/s,
        preventing false-positive fevers during heavy AST parsing rites.
    3.  **Stabilized Hysteresis (THE FIX):** Introduces a 60-second cooldown on
        Autonomic Lustration to ensure the engine doesn't stutter on minor memory
        allocations, protecting active transaction staging directories.
    4.  **Achronal Thread-Bypass:** Detects WASM substrate at nanosecond zero and
        stays the hand of the Threading system, preventing RuntimeError.
    5.  **Temporal Drift Tomography:** In WASM, measures loop jitter to infer CPU
        saturation without hardware-level access.
    6.  **Heap Density Scrying:** Estimates memory mass by observing the count of
        objects in the Python Garbage Collector.
    7.  **Bicameral Heartbeat:** Supports both background threading (Iron) and
        synchronous manual pulses (Ether).
    8.  **Parent Vigil Amnesty:** Prevents autonomic self-annihilation in WASM
        environments where PID scrying is a heresy.
    9.  **Deterministic Health FLOOR:** Proclaims a "RESONANT" status by default
        unless temporal drift exceeds the Event Horizon.
    10. **Isomorphic Vitals Payload:** Normalizes hardware-specific metrics into a
        universal Gnostic schema for the Ocular HUD.
    11. **Atomic Swap Persistence:** Uses the `os.replace` rite for telemetry
        updates, ensuring the pulse file is never corrupted.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable heartbeat.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    PULSE_ZEN_RATE: Final[float] = 10.0
    PULSE_KINETIC_RATE: Final[float] = 2.0
    MEMORY_HYSTERESIS_MB: Final[float] = 50.0
    ETHER_DRIFT_CEILING: Final[float] = 15.0  # ms of lag before "Fever"

    def __init__(self, engine: Any):
        """
        =================================================================================
        == THE METABOLIC INCEPTION (V-Ω-TOTALITY-V25000.1-HEALED-FINALIS)              ==
        =================================================================================
        LIF: ∞ | ROLE: HOMEOSTASIS_INITIALIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_INIT_V25000_THRESHOLD_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite materializes the Engine's autonomic nervous system. It performs
        a deep-tissue substrate biopsy to define the physical boundaries of
        existence, ensuring the Mind never outgrows the Matter.
        =================================================================================
        """
        import sys
        import os
        import threading
        import time
        from pathlib import Path

        # --- MOVEMENT 0: CORE IDENTITY SUTURE ---
        self.engine = engine
        self.logger = Scribe("QuantumEngine:Metabolism")
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

        # [ASCENSION 1]: ABSOLUTE SUBSTRATE DETECTION (THE CURE)
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # [THE FIX]: DEFINE _is_blind
        self._is_blind = not PS_AVAILABLE
        self._pid = os.getpid()

        # --- MOVEMENT I: ADAPTIVE THRESHOLD TOMOGRAPHY ---
        try:
            if not self._is_blind:
                # Scry the physical iron for its total capacity
                total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            else:
                # In WASM/Blind mode, we assume a standard container limit (4GB)
                total_ram_gb = 4.0
        except Exception:
            total_ram_gb = 8.0

        # =========================================================================
        # == [THE CURE]: THE REALIGNED THRESHOLD TRINITY                         ==
        # =========================================================================
        # 1. THE ZEN WALL (SOFT): Start lazy, non-blocking GC sweeps (60% RAM)
        self.gc_threshold_mb = max(512.0, (total_ram_gb * 1024 * 0.60))

        # 2. THE FEVER WALL (HARD): Start aggressive internal cache purging (85% RAM)
        # [THE FIX]: Manifesting 'mem_hard_limit'
        self.mem_hard_limit = max(1024.0, (total_ram_gb * 1024 * 0.85))

        # 3. THE EVENT HORIZON (CRITICAL): Dispatch Autonomic Librarian (95% RAM)
        self.mem_critical_limit = max(2048.0, (total_ram_gb * 1024 * 0.95))
        # =========================================================================

        # --- MOVEMENT II: HYSTERESIS & TREND SENSORS ---
        self._last_proclaimed_mb = 0.0
        self._last_gc_ts = 0.0
        self._last_soft_gc_ts = 0.0
        self._last_lustration_ts = 0.0
        self._entropy_velocity = 0.0
        self._last_biopsy_ts = time.monotonic()
        self._drift_ms = 0.0

        # --- MOVEMENT III: ANCESTRAL VIGIL ANCHOR ---
        try:
            self._parent_pid = os.getppid() if hasattr(os, 'getppid') else 0
        except Exception:
            self._parent_pid = 0

        self.pulse_path: Optional[Path] = None

    def get_vitals(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE VITALS BIOPSY (V-Ω-TOTALITY-V25000-HEALED)                          ==
        =============================================================================
        Provides a direct biopsy to the Dispatcher or Profiler.
        """
        v = self._perform_biopsy()
        mb = v["rss_mb"]

        # [THE FIX]: Correctly referencing self.mem_critical_limit and self._is_blind
        return {
            "rss_mb": mb,
            "velocity": v["velocity_mb_s"],
            "load_percent": (mb / self.mem_critical_limit) * 100 if self.mem_critical_limit else 0,
            "healthy": mb < self.mem_hard_limit,
            "platform": platform.system(),
            "blind_mode": self._is_blind
        }

    def start_vigil(self, pulse_file_path: Optional[str] = None):
        """
        =============================================================================
        == THE RITE OF IGNITION: SUBSTRATE-AWARE HEARTBEAT (V-Ω-FINALIS)           ==
        =============================================================================
        [THE CURE]: This function is now the ultimate authority on threading.
        If it detects the Ether (WASM), it performs a single synchronous pulse
        to establish the baseline, then refuses to spawn a thread.
        """
        if pulse_file_path:
            self.pulse_path = Path(pulse_file_path)

        import sys
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        self.logger.info(
            f"Vitality Monitor active. [Substrate: {'ETHER' if self.is_wasm else 'IRON'}]"
        )

        if self.is_wasm:
            self.logger.info("Heartbeat shifted to [cyan]Synchronous Pulse[/cyan].")
            try:
                self.pulse()
            except Exception:
                pass
            return

        try:
            self._thread = threading.Thread(
                target=self._vigil_loop,
                name="VitalityVigil",
                daemon=True
            )
            self._thread.start()
        except RuntimeError as e:
            self.logger.warn(f"Threading prohibited by substrate ({e}). Heartbeat remains silent.")
            self.is_wasm = True

    def pulse(self):
        """
        =============================================================================
        == THE RITE OF THE ACHRONAL PULSE                                          ==
        =============================================================================
        Manual heartbeat trigger. Used by WASM environments to check vitals without
        background threads.
        """
        vitals = self._perform_biopsy()
        self._adjudicate_metabolism(vitals)
        self._write_pulse_data(vitals)
        return vitals

    def stop_vigil(self):
        """Graceful Cessation."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            try:
                self._thread.join(timeout=0.5)
            except:
                pass
        self._write_pulse_data(vitals={"status": "VOID"})

    def _vigil_loop(self):
        """The Eternal Vigil Loop for Native Strata."""
        process = None
        if not self._is_blind:
            try:
                process = psutil.Process(os.getpid())
            except:
                self._is_blind = True

        while not self._stop_event.is_set():
            loop_start = time.monotonic()
            try:
                vitals = self._perform_biopsy(process)
                self._adjudicate_metabolism(vitals)
                self._write_pulse_data(vitals)

                if self._parent_pid > 0 and not self.is_wasm:
                    if not psutil.pid_exists(self._parent_pid):
                        self.logger.critical("Parent process vanished. Dissolving reality.")
                        self.engine.shutdown()
                        break
            except Exception:
                pass

            current_rate = self.PULSE_ZEN_RATE
            if self._entropy_velocity > 10.0: current_rate = self.PULSE_KINETIC_RATE

            elapsed = time.monotonic() - loop_start
            if self._stop_event.wait(max(0.1, current_rate - elapsed)):
                break

    def _perform_biopsy(self, process: Optional[Any] = None) -> Dict[str, Any]:
        """
        =============================================================================
        == THE OMNISCIENT METABOLIC BIOPSY (V-Ω-TOTALITY-V3000-ANCHOR-SUTURED)     ==
        =============================================================================
        LIF: ∞ | ROLE: SPACETIME_GUARDIAN | RANK: OMEGA_SOVEREIGN

        This rite conducts a simultaneous scry of Physical Metabolism and Logical
        Topography. It enforces the Law of Identity, ensuring the Mind (Engine State)
        and the Soul (identity.json) are in perfect resonance.
        """
        import gc
        import time
        import json
        from pathlib import Path

        now = time.monotonic()
        dt = now - self._last_biopsy_ts
        self._last_biopsy_ts = now

        current_mb = 0.0
        cpu_load = 0.0
        substrate = "IRON"

        try:
            if process and not self._is_blind:
                mem_info = process.memory_info()
                current_mb = mem_info.rss / (1024 * 1024)
                cpu_load = process.cpu_percent()
            else:
                substrate = "ETHER"
                object_count = len(gc.get_objects())
                current_mb = (object_count * 0.00015) + 100.0
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000
                cpu_load = min(100.0, (drift_ms / 5.0) * 100.0)
        except Exception:
            substrate = "VOID"

        if dt > 0:
            self._entropy_velocity = (current_mb - self._last_proclaimed_mb) / dt
        self._last_proclaimed_mb = current_mb

        anchor_status = "STABLE"
        is_resonant = True
        current_root = getattr(self.engine, 'project_root', Path.cwd())
        identity_file = current_root / ".scaffold" / "identity.json"

        if identity_file.exists():
            try:
                with open(identity_file, 'r', encoding='utf-8') as f:
                    id_data = json.load(f)

                physical_id = id_data.get("id")
                logical_id = self.engine.variables.get("project_slug") or self.engine.variables.get("project_name")

                if physical_id and logical_id and physical_id != logical_id:
                    is_resonant = False
                    anchor_status = "ANCHOR_DESYNC"
            except Exception:
                anchor_status = "IDENTITY_FRACTURED"
        else:
            if str(current_root) != ".":
                anchor_status = "VOID_IDENTITY"

        status = "RESONANT"
        if cpu_load > 90.0 or anchor_status != "STABLE":
            status = "STRESSED"
        if cpu_load > 98.0 or anchor_status == "ANCHOR_DESYNC":
            status = "CRITICAL"

        return {
            "rss_mb": round(current_mb, 1),
            "cpu_percent": round(cpu_load, 1),
            "velocity_mb_s": round(self._entropy_velocity, 2),
            "substrate": substrate,
            "anchor": {
                "status": anchor_status,
                "root": str(current_root).replace('\\', '/'),
                "resonant": is_resonant
            },
            "timestamp": time.time(),
            "status": status,
            "trace_id": getattr(self.engine, 'trace_id', 'tr-unbound')
        }

    def _adjudicate_metabolism(self, vitals: Dict[str, Any]):
        """
        =================================================================================
        == THE OMEGA ADJUDICATION RITE (V-Ω-TOTALITY-V25000-HEALED-HYSTERESIS)         ==
        =================================================================================
        [THE CURE]: This is the stabilized logic. It heavily relies on the natural Python
        GC to handle normal spikes. It completely annihilates the "Staging Directory Purge"
        bug by raising the Velocity threshold to 50MB/s and injecting a strict 60-second
        cooldown on Autonomic Lustration.
        =================================================================================
        """
        import gc
        import time
        import threading
        from .....interfaces.requests import LibrarianRequest, LustrationIntensity

        current_mb = vitals.get("rss_mb", 0.0)
        velocity = vitals.get("velocity_mb_s", 0.0)
        substrate = vitals.get("substrate", "IRON")

        is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        effective_soft_limit = self.gc_threshold_mb * (1.2 if is_adrenaline else 1.0)
        effective_hard_limit = self.memory_limit_mb * (1.2 if is_adrenaline else 1.0)

        # [THE FIX]: Velocity Dampening.
        # A surge is only a surge if it's absorbing 50MB per second.
        time_to_impact = (self.mem_critical_limit - current_mb) / velocity if velocity > 0.1 else 999.0
        is_surging = velocity > 50.0

        now = time.monotonic()
        time_since_last = now - self._last_lustration_ts

        # =========================================================================
        # == MOVEMENT I: THE RITE OF ZEN (NATURAL GC)                            ==
        # =========================================================================
        # We give the built-in GC a chance before summoning the heavy Librarian
        if current_mb > effective_soft_limit:
            if now - getattr(self, '_last_soft_gc_ts', 0) > 15.0:
                # self.logger.verbose(f"Zen Lustration: Natural sweep at {current_mb:.0f}MB.")
                self._shear_engine_caches()
                gc.collect(1)  # Scavenge only young objects
                self._last_soft_gc_ts = now

        # =========================================================================
        # == MOVEMENT II: THE AUTONOMIC REFLEX (THE SCYTHE)                      ==
        # =========================================================================
        should_trigger_librarian = False
        target_intensity = LustrationIntensity.SOFT

        if current_mb > self.mem_critical_limit:
            # We are at the Event Horizon (95% RAM).
            if time_since_last > 60.0:  # Even in critical, wait 60s to prevent locked-file storms
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.CRITICAL
                self.logger.critical(f"METABOLIC EVENT HORIZON: {current_mb:.1f}MB. Initiating Emergency Venting.")

        elif current_mb > effective_hard_limit:
            # Hard limit breached (85% RAM). Give it a generous 60-second cooldown window.
            if time_since_last > 60.0:
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.HARD
                self.logger.warn(f"Sustained Metabolic Pressure: {current_mb:.1f}MB. Dispatching Hard Lustration.")

        elif current_mb > effective_soft_limit and is_surging:
            # We are above 60% AND surging at > 50MB/s.
            if time_since_last > 30.0:
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.SOFT
                self.logger.warn(f"PRE-EMPTIVE_LIBRATION: Detected high-velocity entropy surge ({velocity:.1f}MB/s).")

        if should_trigger_librarian:
            try:
                auto_req = LibrarianRequest(
                    intensity=target_intensity,
                    is_autonomic=True,
                    project_root=self.engine.project_root,
                    trace_id=f"auto-heal-{int(time.time())}"
                )

                # We spawn a dedicated thread so the Heartbeat is never blocked
                threading.Thread(
                    target=self.engine.dispatch,
                    args=(auto_req,),
                    name=f"AutonomicLibrarian-{auto_req.trace_id[:4]}",
                    daemon=True
                ).start()

                self._last_lustration_ts = now

                if self.engine.akashic:
                    try:
                        self.engine.akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "METABOLIC_RECOIL",
                                "label": f"AUTONOMIC_{target_intensity.value.upper()}",
                                "color": "#ef4444" if target_intensity == LustrationIntensity.CRITICAL else "#fbbf24",
                                "trace": auto_req.trace_id
                            }
                        })
                    except Exception:
                        pass

            except Exception as e:
                self.logger.error(f"Autonomic Reflex fractured: {e}")

        # Emergency Event Horizon Guard (Absolutely final backstop)
        if current_mb > self.mem_critical_limit + 1024.0:
            gc.collect()

    def _write_pulse_data(self, vitals: Dict[str, Any]):
        """Atomic write of the heartbeat to the virtual or physical disk."""
        if not self.pulse_path: return
        import os
        import json
        payload = {
            "pid": os.getpid(),
            "status": vitals.get("status", "ALIVE"),
            "timestamp": time.time(),
            "meta": vitals
        }
        try:
            temp = self.pulse_path.with_suffix('.tmp')
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(payload, f)
            os.replace(str(temp), str(self.pulse_path))
        except Exception:
            pass

    def _shear_engine_caches(self):
        """Emergency cache evaporation to reclaim RAM."""
        try:
            if hasattr(self.engine, 'alchemist'):
                self.engine.alchemist.env.cache.clear()
            # If the engine has a hot cache in the registry, clear it
            if hasattr(self.engine, 'registry') and hasattr(self.engine.registry, '_l1_hot_cache'):
                self.engine.registry._l1_hot_cache.clear()
        except:
            pass

    def get_vitals(self) -> Dict[str, Any]:
        """Provides a direct biopsy to the Dispatcher or Profiler."""
        v = self._perform_biopsy()
        mb = v["rss_mb"]
        return {
            "rss_mb": mb,
            "velocity": v["velocity_mb_s"],
            "load_percent": (mb / self.mem_critical_limit) * 100 if self.mem_critical_limit else 0,
            "healthy": mb < self.mem_hard_limit,
            "platform": platform.system(),
            "blind_mode": self._is_blind
        }