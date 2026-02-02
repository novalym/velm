# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/variable.py
# -------------------------------------------------------------------------------------
from typing import Any
from ..contracts import StateSpecialist
from ..utils.type_diviner import TypeDiviner
from ......contracts.symphony_contracts import Edict, EventType


class VariableInscriber(StateSpecialist):
    """
    [FACULTY 1] The Scribe of Variables.
    Handles '%% let: x = y', '%% set: ...', '%% var: ...'
    """

    def conduct(self, edict: Edict, value: str) -> None:
        # Determine Key and Value Expression
        # If edict.state_key is 'let', the value string holds "key = val"
        # If the user used "%% let: key = val", 'key' is 'let', value is 'key = val'

        # 1. Parse Assignment
        if "=" in value:
            key_part, val_part = value.split("=", 1)
            target_key = key_part.strip()
            val_expr = val_part.strip()
        else:
            # Boolean flag case: "%% let: debug" -> debug = True
            target_key = value.strip()
            val_expr = "true"

        # 2. Secret Resolution
        if edict.secret_source:
            resolved_value = self.handler.context_manager.resolve_secret(edict.secret_source)
            self._update_and_announce(target_key, resolved_value, is_secret=True)
            return

        # 3. Alchemical Transmutation (Recursive)
        # We must transmute the RIGHT side of the equals sign again,
        # because the first transmutation in Dispatcher only resolved the whole string.
        # e.g. "my_var = {{ other_var }}" -> "my_var = value"

        # Actually, the Dispatcher transmuted the whole "key = {{val}}" string.
        # So val_expr is likely already resolved.
        # But just in case of nested jinja or quotes:

        clean_val = val_expr.strip("'").strip('"')

        # 4. Type Divination
        final_value = TypeDiviner.divine(clean_val)

        # 5. Inscription
        self._update_and_announce(target_key, final_value)

    def _update_and_announce(self, key: str, value: Any, is_secret: bool = False):
        self.handler.context_manager.update_variable(key, value)

        display_val = "******" if is_secret else str(value)
        if len(display_val) > 50: display_val = display_val[:47] + "..."

        self.handler.engine._proclaim_event(EventType.STATE_CHANGE, {
            "key": key,
            "value": display_val,
            "relative_sanctum": self.handler.context_manager.cwd  # Property access
        })