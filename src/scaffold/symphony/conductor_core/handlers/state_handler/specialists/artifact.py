# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/artifact.py
# -------------------------------------------------------------------------------------
from ..contracts import StateSpecialist
from ......contracts.symphony_contracts import Edict


class ArtifactRegistrar(StateSpecialist):
    """Handles '%% hoard: pattern'"""

    def conduct(self, edict: Edict, value: str) -> None:
        hoard_list = self.handler.variables.get('__hoard_patterns__', [])
        # Ensure it's a list (copy from context returns raw data)
        if not isinstance(hoard_list, list):
            hoard_list = []

        hoard_list.append(value)
        self.handler.context_manager.update_variable('__hoard_patterns__', hoard_list)
        self.logger.verbose(f"Registered artifact pattern: {value}")