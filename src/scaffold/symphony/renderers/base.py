# scaffold/symphony/renderers/base.py
# -----------------------------------------
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Any, List, TYPE_CHECKING, Union, Dict

if TYPE_CHECKING:
    from ..conductor import SymphonyConductor
    from ...contracts.symphony_contracts import ConductorEvent, SymphonyResult, Edict, ActionResult


class Renderer(ABC):
    """
    =================================================================================
    == THE SACRED CONTRACT OF THE VOICE (V-Ω-SUSPENDABLE)                          ==
    =================================================================================
    LIF: 10,000,000,000,000
    """

    def __init__(self, conductor: 'SymphonyConductor'):
        self.conductor = conductor

    @abstractmethod
    def suspend(self):
        """
        [THE RITE OF SILENCE]
        Pauses any active Live displays or spinners to allow another Artisan
        (like the Intercession Altar) to take control of the terminal.
        """
        pass

    @abstractmethod
    def resume(self):
        """
        [THE RITE OF RETURN]
        Resumes the Live display after the interruption.
        """
        pass

    # --- Legacy / Optional Hooks ---
    def conduct_interactive_plea(self, prompt_text: str, default: bool = True): ...

    def render_summary_dossier(self, result: 'SymphonyResult'): ...

    def render_paradox(self, heresy: Exception, traceback_obj: Any, captured_output: Optional[str] = None): ...

    def render_action_prologue(self, edict: 'Edict', transmuted_command: str, sanctum: Path): ...

    def render_action_epilogue(self, live_context: Any, result: 'ActionResult'): ...

    def update_live_stream(self, live_context: Any, line: Union[str, Any]): ...

    def render_polyglot_prologue(self, edict: 'Edict', sanctum: Path): ...

    def render_vow_result(self, is_pure: bool, reason: str, edict: 'Edict'): ...

    def render_state_change(self, key: str, value: str, relative_sanctum: Path): ...

    def render_proclamation(self, message: str, sanctum: Optional[Path] = None): ...

    def render_block_prologue(self, edict: 'Edict', title: str): ...

    def render_block_epilogue(self, edict: 'Edict'): ...

    def render_intercession_altar(self, edict: 'Edict', heresy: Exception): ...

    def render_comment(self, raw_scripture: str): ...

    def render_foreign_adjudication(self, results: List[Any], edict: 'Edict'): ...

    def render_structured_status(self, proclamations: List[Dict], line_num: int): ...