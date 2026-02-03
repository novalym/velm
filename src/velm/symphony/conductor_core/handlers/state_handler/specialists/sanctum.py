# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/sanctum.py
# ------------------------------------------------------------------------------------
from ..contracts import StateSpecialist
from ..utils.path_resolver import PathResolver
from ......contracts.symphony_contracts import Edict, EventType

class SanctumShifter(StateSpecialist):
    """
    [FACULTY 2] The Shifter of Realities.
    Handles '%% sanctum: path/to/dir'
    """
    def conduct(self, edict: Edict, value: str) -> None:
        # 1. Resolve Path
        new_path = PathResolver.resolve(self.handler.context_manager, value)

        # 2. Verify Existence
        if not new_path.exists():
            if self.handler.is_dry_run:
                self.logger.info(f"[DRY-RUN] Would create and enter sanctum: {new_path}")
            else:
                new_path.mkdir(parents=True, exist_ok=True)

        # 3. Shift Reality
        if not self.handler.is_dry_run:
            self.handler.context_manager.set_sanctum(str(new_path))

        # 4. Proclaim Change
        self.handler.engine._proclaim_event(EventType.STATE_CHANGE, {
            "key": "sanctum",
            "value": str(new_path),
            "relative_sanctum": new_path
        })
        self.logger.verbose(f"Sanctum shifted to: {new_path}")