# Path: scaffold/symphony/conductor_core/lifecycle/manager.py
# -----------------------------------------------------------

import os
import shutil
import signal
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING

from .contracts import ServiceConfig, ServiceState
from .supervisor import ServiceSupervisor
from ....logger import Scribe
from ....core.net.tunnel import TunnelWeaver
from ....utils.core_utils import unbreakable_ward_of_annihilation

if TYPE_CHECKING:
    from ..conductor.orchestrator import SymphonyConductor

Logger = Scribe('SymphonyLifecycle')


class SymphonyLifecycleManager:
    """
    =================================================================================
    == THE CELESTIAL ADMIRAL (V-Ω-LIFECYCLE-GOD-ENGINE)                            ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Governor of Background Realities. It orchestrates the birth, life,
    resurrection, and death of all Services and Tunnels.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Supervisor Fleet:** Manages a legion of `ServiceSupervisor` threads.
    2.  **The Tunnel Weaver Integration:** Natively commands the `TunnelWeaver`.
    3.  **The Phoenix Protocol:** Auto-resurrection logic delegated to Supervisors.
    4.  **The Health Sentinel:** Aggregates telemetry from all Supervisors.
    5.  **The Graceful Reaper:** Tiered Shutdown Strategy (SIGTERM -> SIGKILL).
    6.  **The Orphan Hunter:** Tracks PIDs of all spawned processes globally.
    7.  **The Ephemeral Ward:** Wields `unbreakable_ward_of_annihilation` to PROTECT USER DATA.
    8.  **The Telepathic Broadcaster:** Emits `SERVICE_STATE` events to the Bus.
    9.  **The Thread-Safe Registry:** Uses `RLock` for all state mutations.
    10. **The Manifest Guard:** Explicitly checks mode before deleting anything.
    11. **The Log Aggregator:** Ensures logs are captured.
    12. **The Sovereign Soul:** Decoupled from the Engine.
    """

    def __init__(self, conductor: 'SymphonyConductor'):
        self.conductor = conductor
        self.scribe = Logger

        # State
        self.services: Dict[str, ServiceSupervisor] = {}
        self.active_tunnels: List[int] = []  # PIDs of tunnels
        self.all_spawned_pids: List[int] = []  # Global PID registry for cleanup

        self._lock = threading.RLock()
        self.tunnel_weaver = TunnelWeaver()

    def prologue(self):
        """The Rite of Preparation."""
        self.cleanup(was_pure=True, duration=0, ephemeral_sanctum=None)  # Ensure clean slate
        self.tunnel_weaver = TunnelWeaver()  # Fresh weaver
        self.all_spawned_pids.clear()
        self.services.clear()

    def register_service(self, name: str, command: str, action: str, cwd: Path, **kwargs):
        """
        [THE RITE OF COMMISSION]
        Commissions a new Service Supervisor.
        """
        with self._lock:
            # If service exists, kill it first
            if name in self.services:
                self.scribe.warn(f"Service '{name}' redefined. Restarting...")
                self.services[name].stop()
                self.services[name].join()
                del self.services[name]

            # Forge Configuration
            # Note: We extract environment from the current context if needed
            env = kwargs.get('env', {})

            config = ServiceConfig(
                name=name,
                command=command,
                cwd=cwd,
                action=action,
                healthcheck_cmd=kwargs.get('healthcheck'),
                restart_policy=kwargs.get('restart', 'on-failure'),
                env=env
            )

            supervisor = ServiceSupervisor(config, self)
            self.services[name] = supervisor
            supervisor.start()

    def register_tunnel(self, spec: str):
        """
        [THE RITE OF THE WORMHOLE]
        Commands the TunnelWeaver.
        """
        # We need the current sanctum URI from context if possible
        sanctum_uri = ""  # Future: Extract from context if needed

        try:
            pid = self.tunnel_weaver.weave(spec, sanctum_uri)
            with self._lock:
                self.active_tunnels.append(pid)
                self.all_spawned_pids.append(pid)

            # Broadcast state
            self.broadcast_state(f"tunnel:{pid}", ServiceState.RUNNING)
        except Exception as e:
            raise Exception(f"Failed to weave tunnel '{spec}': {e}") from e

    def register_pid(self, pid: int):
        """Registers a PID for the Orphan Hunter."""
        with self._lock:
            self.all_spawned_pids.append(pid)

    def broadcast_state(self, name: str, state: ServiceState):
        """Emits state change to the Event Bus."""
        if self.conductor.engine:
            self.conductor.engine._proclaim_event("SERVICE_STATE", {
                "name": name,
                "state": state.value,
                "timestamp": time.time()
            })

    def cleanup(self, was_pure: bool, duration: float, ephemeral_sanctum: Optional[Path]):
        """
        =================================================================================
        == THE RITE OF UNIVERSAL REST (V-Ω-TIERED-ANNIHILATION-SAFEGUARDED)            ==
        =================================================================================
        Performs the shutdown sequence. This is the most dangerous rite.
        It is guarded by the **Unbreakable Ward**.
        """
        self.scribe.info("Initiating Lifecycle Cleanup...")

        # 1. Collapse Tunnels
        self.tunnel_weaver.close_all()

        # 2. Stop Services
        with self._lock:
            if self.services:
                self.scribe.info(f"Collapsing {len(self.services)} active service(s)...")
                for s in self.services.values():
                    s.stop()

                # Wait for them to die gracefully
                for s in self.services.values():
                    s.join(timeout=2)

        # 3. The Orphan Hunter (Final Sweep)
        # Kill any PIDs we registered that might still be alive
        for pid in self.all_spawned_pids:
            try:
                os.kill(pid, 0)  # Check if alive
                self.scribe.verbose(f"Reaping orphaned PID {pid}...")
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass  # Already dead

        # 4. THE ADJUDICATION OF THE PROVING GROUND
        # This is where we delete files. BE EXTREMELY CAREFUL.

        if ephemeral_sanctum:
            # Check for user override
            if self.conductor.request.no_cleanup:
                self.scribe.info(
                    f"Cleanup stayed by Architect's will (--no-cleanup). Sanctum preserved: {ephemeral_sanctum}")
                return

            # Check for Mode
            if not self.conductor.request.rehearse:
                # Should be impossible if logic upstream is correct, but we double-check.
                self.scribe.warn("Ephemeral sanctum provided but not in Rehearsal mode. Skipping deletion for safety.")
                return

            # THE UNBREAKABLE WARD OF ANNIHILATION
            self.scribe.info(f"Preparing to annihilate ephemeral sanctum: {ephemeral_sanctum}")

            try:
                # This function (from utils.core_utils) performs the 4-Gate Safety Check:
                # 1. Not None
                # 2. Not Root/System
                # 3. Not Project Root
                # 4. Matches "scaffold_rehearsal_" pattern
                unbreakable_ward_of_annihilation(
                    path_to_delete=ephemeral_sanctum,
                    project_root=self.conductor.context_manager.project_root(),
                    rite_name="Symphony Rehearsal Cleanup"
                )

                # If the Ward passes, we strike.
                shutil.rmtree(ephemeral_sanctum, ignore_errors=True)
                self.scribe.success("The ephemeral reality has returned to the void.")

            except Exception as e:
                self.scribe.critical(f"CLEANUP PARADOX: {e}")
                self.scribe.warn(f"Sanctum '{ephemeral_sanctum}' was NOT deleted due to safety violation.")

        else:
            # In Manifest Mode (Default), ephemeral_sanctum is None.
            # We do NOTHING.
            self.scribe.verbose("Manifest Mode: No ephemeral sanctum to cleanse. Reality is preserved.")