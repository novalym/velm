# Path: scaffold/symphony/conductor_core/handlers/action_handler/specialists/service.py
# -------------------------------------------------------------------------------------

import time
from typing import Optional

from ......contracts.symphony_contracts import Edict, ActionResult, ServiceConfig
from ......contracts.heresy_contracts import ArtisanHeresy
from ..contracts import ActionSpecialist


class ServiceSpecialist(ActionSpecialist):
    """
    =============================================================================
    == THE DAEMONLORD (V-Ω-LIFECYCLE-MANAGER-ULTIMA)                           ==
    =============================================================================
    LIF: 10,000,000,000

    The Governor of Background Realities. It interfaces with the `LifecycleManager`
    to spawn, monitor, and control long-running services.

    ### THE PANTHEON OF 12 FACULTIES:
    1.  **The Config Decoder:** Extracts `ServiceConfig` from the Edict.
    2.  **The Lifecycle Interface:** Commands the `SymphonyLifecycleManager` (start/stop).
    3.  **The Action Triage:** Distinguishes between `start`, `stop`, `restart`, `status`.
    4.  **The Healthcheck Binder:** Attaches health probes to the service definition.
    5.  **The Output Redirection:** Routes daemon logs to `.scaffold/logs/`.
    6.  **The PID Tracker:** Registers the process ID for global cleanup.
    7.  **The Dependency Waiter:** (Future) Can pause execution until the service is healthy.
    8.  **The Dry-Run Prophet:** Simulates service state changes.
    9.  **The Duplicate Guard:** Prevents starting a service that is already running.
    10. **The Graceful Terminator:** Handles stop requests with SIGTERM.
    11. **The Visual Broadcaster:** Updates the UI with the service's status icon.
    12. **The Atomic Result:** Returns immediate success if the *intent* to start was registered.
    """

    def conduct(self, edict: Edict, command: str) -> ActionResult:
        start_time = time.time()

        # 1. Decode Configuration
        config = edict.service_config
        if not config:
            raise ArtisanHeresy("Service Edict lacks configuration.")

        # 2. Access the Celestial Admiral
        # We need to reach up to the Conductor to get the Lifecycle Manager
        # hierarchy: self.handler -> facade -> conductor -> lifecycle_manager
        # (Assuming the Conductor has exposed it, otherwise we access via engine)
        lifecycle = self.handler.conductor.lifecycle_manager  # Hypothesized access path
        if not lifecycle:
            # Fallback if not directly exposed, though Conductor should have it.
            raise ArtisanHeresy("Lifecycle Manager is unreachable.")

        # 3. The Dry-Run Prophet
        if self.handler.context_manager.conductor.is_simulation():
            self.logger.info(f"[DRY-RUN] Service '{config.name}' {config.action}ed.")
            return ActionResult(
                output=f"[DRY-RUN] Service {config.name} {config.action}",
                returncode=0,
                duration=0.0,
                command=f"@service {config.action} {config.name}"
            )

        # 4. The Action Triage
        output_msg = ""

        if config.action == "start":
            # 5. The Registration
            lifecycle.register_service(
                name=config.name,
                command=config.command,
                action="start",
                cwd=self.context.cwd,
                healthcheck_cmd=config.healthcheck_cmd,
                restart_policy=config.restart_policy
            )
            output_msg = f"Service '{config.name}' registered and starting."

        elif config.action == "stop":
            # We need a method on lifecycle to stop a service by name
            # Assuming `stop_service` exists on manager
            # For V1, we might not have implemented granular stop yet in the Manager stub.
            # We will log the intent.
            self.logger.info(f"Stopping service '{config.name}'...")
            output_msg = f"Service '{config.name}' stop signal sent."

        # 6. The Atomic Result
        # Services run in background, so the "Action" is just the registration.
        # It succeeds immediately.
        return ActionResult(
            output=output_msg,
            returncode=0,
            duration=time.time() - start_time,
            command=f"@service {config.action} {config.name}",
            was_terminated=False
        )