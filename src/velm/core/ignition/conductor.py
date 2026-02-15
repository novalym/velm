# Path: scaffold/core/ignition/conductor.py
# =========================================================================================
# == THE OMEGA IGNITION CONDUCTOR (V-Ω-TOTALITY-V20000.1-TITANIUM)                      ==
# =========================================================================================
# LIF: 100,000,000,000 | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_IGNITION_V20000_TOTAL_SUTURE_2026_FINALIS
# =========================================================================================

from __future__ import annotations
import os
import sys
import subprocess
import threading
import time
import signal
import gc
import json
import collections
from pathlib import Path
from typing import Dict, Optional, List, Callable, Any, Set, Tuple, Final

# --- THE DIVINE UPLINKS ---
from .contracts import ExecutionPlan, VitalityState, AuraSigil
from .sentinel.priest import ToolchainSentinel
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 1]: SUBSTRATE SENSING
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

Logger = Scribe("IgnitionConductor")


class IgnitionConductor:
    """
    =================================================================================
    == THE IGNITION CONDUCTOR (V-Ω-TOTALITY)                                       ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_EXECUTOR | RANK: OMEGA_SUPREME

    The sovereign master of the process lifecycle. It transmutes an ExecutionPlan
    into a living, breathing reality within the Operating System.
    """

    def __init__(self, engine: Optional[Any] = None):
        self.engine = engine
        # Map[Merkle_ID, Popen_Instance]
        self._active_processes: Dict[str, subprocess.Popen] = {}
        # Map[Merkle_ID, Telemetry_Thread]
        self._vigils: Dict[str, threading.Thread] = {}
        self._lock = threading.RLock()

        # [ASCENSION 11]: FLAPPING DEFENSE
        self._restart_ledger = collections.defaultdict(list)
        self.FLAP_THRESHOLD = 5  # Max 5 restarts in 60s

    def ignite(self,
               plan: ExecutionPlan,
               on_log: Optional[Callable[[str, str], None]] = None,
               on_fracture: Optional[Callable[[int, str], None]] = None) -> int:
        """
        =============================================================================
        == THE RITE OF IGNITION (V-Ω-STRIKE-RESONANT)                             ==
        =============================================================================
        [ASCENSION 4]: Uses the plan's Merkle Seal as the Causal Anchor.
        """
        plan_id = plan.merkle_seal
        trace_id = getattr(plan, 'trace_id', f"tr-{uuid.uuid4().hex[:8].upper()}")

        with self._lock:
            # 1. COLLISION ADJUDICATION
            if plan_id in self._active_processes:
                if self.get_status(plan_id) == VitalityState.ONLINE:
                    Logger.warn(f"[{trace_id}] Singularity Conflict: Process {plan_id[:8]} is already manifest.")
                    return self._active_processes[plan_id].pid
                else:
                    self.banish(plan_id)

            # 2. FLAPPING PROTECTION
            if self._is_flapping(plan_id):
                raise ArtisanHeresy(
                    f"Metabolic Instability: Plan {plan_id[:8]} is flapping.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify command syntax and environment dependencies."
                )

        # 3. BIOLOGICAL READINESS CHECK (THE SHIELD)
        if plan.support and not plan.support.is_installed:
            raise ArtisanHeresy(
                f"Biological Fracture: {plan.support.manifest_type} unmanifest.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Speak: scaffold runtimes setup --needs {plan.support.manifest_type}"
            )

        # 4. DNA GRAFTING (ENVIRONMENT FUSION)
        # [ASCENSION 6 & 9]: We suture the environment with Trace IDs and Venv paths.
        env = os.environ.copy()
        env.update(plan.env)
        env["SCAFFOLD_TRACE_ID"] = trace_id
        env["PYTHONUNBUFFERED"] = "1"

        # 5. SPATIAL ANCHORING
        # Ensure the sanctum exists before ignition
        if not plan.cwd.exists():
            plan.cwd.mkdir(parents=True, exist_ok=True)

        # 6. KINETIC SPAWN (THE STRIKE)
        creation_flags = 0
        if os.name == 'nt':
            # [ASCENSION 2]: Group Isolation for Windows
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP

        Logger.info(f"[{trace_id}] Igniting Reality: [bold cyan]{plan.aura.value}[/] via {' '.join(plan.command)}")
        self._multicast_hud(trace_id, "IGNITION_START", "#64ffda")

        try:
            proc = subprocess.Popen(
                plan.command,
                cwd=str(plan.cwd),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line-buffered for zero visual latency
                creationflags=creation_flags,
                start_new_session=True if os.name != 'nt' else False
            )

            with self._lock:
                self._active_processes[plan_id] = proc
                self._restart_ledger[plan_id].append(time.time())

            # 7. AWAKEN TELEMETRIC SCRIBES
            # [ASCENSION 8]: Hydraulic Stream Guarding
            threading.Thread(
                target=self._scribe_stream,
                args=(plan_id, proc.stdout, "STDOUT", on_log),
                name=f"Scribe-Out-{plan_id[:4]}",
                daemon=True
            ).start()

            threading.Thread(
                target=self._scribe_stream,
                args=(plan_id, proc.stderr, "STDERR", on_log),
                name=f"Scribe-Err-{plan_id[:4]}",
                daemon=True
            ).start()

            # 8. ENGAGE VITALITY VIGIL
            vigil = threading.Thread(
                target=self._vigil_loop,
                args=(plan_id, proc, on_fracture, trace_id),
                name=f"Vigil-{plan_id[:4]}",
                daemon=True
            )
            vigil.start()
            self._vigils[plan_id] = vigil

            return proc.pid

        except Exception as fracture:
            self._multicast_hud(trace_id, "IGNITION_FRACTURE", "#ef4444")
            Logger.critical(f"Ignition Fracture: {str(fracture)}")
            raise

    def banish(self, plan_id: str):
        """
        =============================================================================
        == THE RITE OF GRACEFUL BANISHMENT (V-Ω-RECURSIVE-REAPER)                  ==
        =============================================================================
        [ASCENSION 2 & 7]: Escalate signal intensity to ensure total dissolution.
        """
        with self._lock:
            proc = self._active_processes.get(plan_id)
            if not proc: return

            Logger.info(f"Banishing Process Soul: {plan_id[:8]} (PID: {proc.pid})")

            # --- MOVEMENT I: SOFT BANISH (SIGTERM) ---
            try:
                if PSUTIL_AVAILABLE:
                    parent = psutil.Process(proc.pid)
                    children = parent.children(recursive=True)

                    # Proclaim termination to the whole bloodline
                    for child in children:
                        try:
                            child.terminate()
                        except:
                            pass
                    parent.terminate()

                    # --- MOVEMENT II: THE COOLING PERIOD ---
                    _, alive = psutil.wait_procs(children + [parent], timeout=2.0)

                    # --- MOVEMENT III: HARD BANISH (SIGKILL) ---
                    for survivor in alive:
                        try:
                            survivor.kill()
                        except:
                            pass
                else:
                    # Fallback for WASM/Legacy: OS-level killpg
                    if os.name != 'nt':
                        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                        time.sleep(0.5)
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.terminate()
                        proc.kill()

            except Exception as e:
                Logger.verbose(f"Banishment friction: {e}")
            finally:
                self._active_processes.pop(plan_id, None)
                self._vigils.pop(plan_id, None)

    def _scribe_stream(self, plan_id: str, stream: Any, name: str, callback: Optional[Callable]):
        """[ASCENSION 8]: Telemetric Stream Splicer with Metabolic Control."""
        try:
            for line in iter(stream.readline, ''):
                if not line: break
                clean_line = line.strip()
                if clean_line:
                    # [STRIKE]: Notify Callback
                    if callback: callback(name, clean_line)

                    # [SUTURING]: Forward to Ocular HUD if possible
                    self._radiate_log(plan_id, name, clean_line)

                    # Also log to global scribe
                    Logger.verbose(f"[{plan_id[:4]}:{name}] {clean_line}")

                    # [ASCENSION 8]: Yield to OS to prevent I/O lock
                    time.sleep(0.001)
        except Exception as e:
            Logger.debug(f"Stream Splicer dissolved: {e}")
        finally:
            if stream: stream.close()

    def _vigil_loop(self, plan_id: str, proc: subprocess.Popen, on_fracture: Optional[Callable], trace_id: str):
        """[ASCENSION 3]: Vitality Heartbeat Monitoring."""
        exit_code = proc.wait()

        with self._lock:
            # Check if this exit was expected (i.e. banished) or a fracture
            if plan_id in self._active_processes:
                self._active_processes.pop(plan_id)
                self._vigils.pop(plan_id, None)

                if exit_code != 0:
                    Logger.error(f"[{trace_id}] Reality Fractured: Process {plan_id[:8]} exited with code {exit_code}")
                    self._multicast_hud(trace_id, "STRIKE_FRACTURED", "#ef4444")
                    if on_fracture:
                        on_fracture(exit_code, "Unexpected Departure")
                else:
                    Logger.success(f"[{trace_id}] Process {plan_id[:8]} has successfully ascended.")
                    self._multicast_hud(trace_id, "STRIKE_ASCENDED", "#64ffda")

    def _is_flapping(self, plan_id: str) -> bool:
        """[ASCENSION 11]: Flapping Sentinel."""
        now = time.time()
        # Prune ancient history
        self._restart_ledger[plan_id] = [ts for ts in self._restart_ledger[plan_id] if now - ts < 60]
        return len(self._restart_ledger[plan_id]) >= self.FLAP_THRESHOLD

    def get_status(self, plan_id: str) -> VitalityState:
        """[ASCENSION 8]: Lifecycle Oracle Query."""
        with self._lock:
            proc = self._active_processes.get(plan_id)
            if not proc: return VitalityState.DORMANT

            # [ASCENSION 3]: Active Tomography
            poll = proc.poll()
            if poll is not None:
                return VitalityState.FRACTURED if poll != 0 else VitalityState.DORMANT

            return VitalityState.ONLINE

    def _multicast_hud(self, trace: str, type: str, color: str):
        """Projects process state to the Ocular HUD."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type,
                        "label": "KINETIC_CONDUCT",
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def _radiate_log(self, plan_id: str, stream: str, content: str):
        """Radiates individual log lines to the Ocular Terminal."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                # We use a specialized log stream method
                self.engine.akashic.broadcast({
                    "method": "novalym/stream_log",
                    "params": {
                        "source": f"IGNITION:{plan_id[:8]}",
                        "stream": stream,
                        "content": content,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass


# =============================================================================
# == THE SOVEREIGN INSTANCE                                                  ==
# =============================================================================
# The singleton conductor for this reality.
Conductor = IgnitionConductor()
