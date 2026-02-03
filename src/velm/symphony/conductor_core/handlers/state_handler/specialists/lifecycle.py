# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/lifecycle.py
# --------------------------------------------------------------------------------------
import os
import signal
from ..contracts import StateSpecialist
from ......contracts.symphony_contracts import Edict


class ProcessReaper(StateSpecialist):
    """Handles '%% kill: PID_OR_VAR'"""

    def conduct(self, edict: Edict, value: str) -> None:
        pid_val = value.strip()

        # Resolve variable if it's not a number
        if not pid_val.isdigit():
            pid_val = self.handler.variables.get(pid_val)

        if not pid_val:
            self.logger.warn(f"Kill command ignored: PID '{value}' resolved to void.")
            return

        try:
            pid_int = int(pid_val)
            if not self.handler.is_dry_run:
                os.kill(pid_int, signal.SIGTERM)
                self.logger.success(f"Terminated process {pid_int}.")
            else:
                self.logger.info(f"[DRY-RUN] Would kill process {pid_int}")
        except Exception as e:
            self.logger.warn(f"Failed to kill process {pid_val}: {e}")


class TunnelWeaverLink(StateSpecialist):
    """Handles '%% tunnel: spec'"""

    def conduct(self, edict: Edict, value: str) -> None:
        if hasattr(self.handler.conductor, 'lifecycle_manager'):
            self.handler.conductor.lifecycle_manager.register_tunnel(value)
        else:
            self.logger.warn("Lifecycle Manager missing. Tunnel ignored.")