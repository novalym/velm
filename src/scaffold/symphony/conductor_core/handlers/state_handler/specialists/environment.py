# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/environment.py
# -----------------------------------------------------------------------------------------
import os
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......contracts.symphony_contracts import Edict, EventType
from ..contracts import StateSpecialist


class EnvironmentInjector(StateSpecialist):
    """
    [FACULTY 3] The Alchemist of the Shell.
    Handles '%% env: KEY=VALUE'
    """

    def conduct(self, edict: Edict, value: str) -> None:
        if "=" not in value:
            raise ArtisanHeresy(f"Invalid env assignment: {value}", line_num=edict.line_num)

        key, val = value.split("=", 1)
        key = key.strip()
        val = val.strip()

        # 1. Update OS Environment (For child processes)
        os.environ[key] = val

        # 2. Update Context Memory (For template access: env.KEY)
        self.handler.context_manager.update_variable(f"env.{key}", val)

        # 3. Proclaim
        self.handler.engine._proclaim_event(EventType.STATE_CHANGE, {
            "key": f"ENV:{key}",
            "value": val,
            "relative_sanctum": self.handler.context_manager.cwd
        })