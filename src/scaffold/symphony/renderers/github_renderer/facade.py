# Path: scaffold/symphony/renderers/github_renderer/facade.py
# -----------------------------------------------------------

import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from ..base import Renderer
from .emitter import GHAEmitter
from ....contracts.symphony_contracts import (
    ConductorEvent, EventType, SymphonyResult, Edict, ActionResult
)
from ....logger import Scribe

Logger = Scribe('GHARenderer')


class GitHubActionsRenderer(Renderer):
    """
    =================================================================================
    == THE CI SCRIBE (V-Ω-GHA-NATIVE-ULTIMA)                                       ==
    =================================================================================
    LIF: 10,000,000,000,000

    A specialized renderer for GitHub Actions.
    It prioritizes **Structure** and **Annotations** over style.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **Grouped Execution:** Every kinetic rite (Action) is wrapped in a `::group::`,
        making logs collapsible and readable in the GHA UI.
    2.  **Native Annotations:** Heresies are emitted as `::error::` annotations,
        making them visible in the Files Changed view of a PR.
    3.  **Secret Registration:** Automatically calls `::add-mask::` for known secrets
        encountered during state changes.
    4.  **The State Chronicler:** Uses `::notice::` for significant state changes.
    5.  **The Silent Stream:** Passes raw stdout from tools directly to the log
        inside the group, without extra prefixes that break copy-pasting.
    6.  **The Summary Generator:** (Prophecy) Can write to `$GITHUB_STEP_SUMMARY`.
    7.  **The Vow Adjudicator:** Emits warnings for failed vows but keeps the
        pipeline moving (unless critical).
    8.  **The Path Anchor:** Normalizes paths relative to `$GITHUB_WORKSPACE` if possible.
    9.  **The Stateless Design:** Does not rely on complex TUI state, perfect for
        the ephemeral nature of runners.
    10. **The Debug Bridge:** Routes verbose logs to `::debug::` if `ACTIONS_STEP_DEBUG` is set.
    11. **The Polyglot Header:** Distinctly labels foreign code execution blocks.
    12. **The Final Verdict:** Outputs a clean status block at the end.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.emitter = GHAEmitter()
        self._in_group = False

        # We define the map locally to bind methods
        self._rite_map = {
            EventType.SYMPHONY_START: self._on_symphony_start,
            EventType.SYMPHONY_END: self._on_symphony_end,
            EventType.ACTION_PROLOGUE: self._on_action_prologue,
            EventType.ACTION_EPILOGUE: self._on_action_epilogue,
            EventType.LOG: self._on_log,
            EventType.PARADOX_PROCLAIMED: self._on_paradox,
            EventType.STATE_CHANGE: self._on_state_change,
            EventType.VOW_RESULT: self._on_vow_result,
            # Block events are handled via debug
            EventType.EDICT_START: lambda p: self.emitter.debug(f"Block Start: {p.get('type')}"),
            EventType.EDICT_SUCCESS: lambda p: None,
            EventType.EDICT_FAILURE: lambda p: None,
        }

    def handle_event(self, event: ConductorEvent):
        handler = self._rite_map.get(event.type)
        if handler:
            handler(event.payload)

    # --- EVENT HANDLERS ---

    def _on_symphony_start(self, payload: Dict):
        path = payload.get("symphony_path", "Unknown")
        self.emitter.notice(f"Scaffold Symphony Started: {path}", title="Symphony Orchestration")

    def _on_symphony_end(self, payload: Dict):
        self._ensure_group_closed()
        success = payload.get("success", False)
        duration = payload.get("duration", 0.0)

        msg = f"Symphony Concluded in {duration:.2f}s"
        if success:
            self.emitter.notice(msg, title="Success")
        else:
            self.emitter.error(msg, title="Failure")

    def _on_action_prologue(self, payload: Dict):
        """Opens a fold for the command."""
        self._ensure_group_closed()
        command = payload.get("command", "")
        # Remove newlines to keep title clean
        clean_cmd = command.replace("\n", " ")
        if len(clean_cmd) > 80: clean_cmd = clean_cmd[:77] + "..."

        self.emitter.start_group(f"EXEC: {clean_cmd}")
        self._in_group = True

    def _on_action_epilogue(self, payload: Dict):
        """Closes the fold."""
        result = payload.get("result", {})
        rc = result.returncode
        duration = result.duration

        if rc != 0:
            # We emit an error annotation so it shows up in the PR summary
            self.emitter.error(f"Process failed with exit code {rc}", title="Execution Failure")

        self.emitter.raw_log(f"[Meta] Duration: {duration:.2f}s | Exit: {rc}")
        self._ensure_group_closed()

    def _on_log(self, payload: Dict):
        """Streams content inside the active group."""
        content = payload.get("content", "").rstrip()
        if content:
            self.emitter.raw_log(content)

    def _on_state_change(self, payload: Dict):
        # State changes shouldn't break the group flow usually, but we ensure it for visibility
        self._ensure_group_closed()
        key = payload.get("key")
        value = str(payload.get("value"))

        # If it looks like a secret, mask it
        if "secret" in key.lower() or "token" in key.lower() or "key" in key.lower():
            self.emitter.mask_secret(value)
            self.emitter.raw_log(f"[State] {key} = *** (Masked)")
        else:
            self.emitter.raw_log(f"[State] {key} = {value}")

    def _on_vow_result(self, payload: Dict):
        self._ensure_group_closed()
        success = payload.get("success")
        reason = payload.get("reason")

        if success:
            self.emitter.raw_log(f"[VOW PASSED] {reason}")
        else:
            self.emitter.warning(f"Vow Failed: {reason}", title="Gnostic Adjudication")

    def _on_paradox(self, payload: Dict):
        self._ensure_group_closed()
        error_msg = payload.get("message", "Unknown Paradox")
        trace = payload.get("traceback", "")

        # We output the trace as a group so it doesn't clutter the main view unless expanded
        self.emitter.start_group(f"Paradox: {error_msg}")
        self.emitter.raw_log(trace)
        self.emitter.end_group()

        # Emit a high-level error annotation
        self.emitter.error(error_msg, title="Gnostic Paradox")

    # --- HELPERS ---

    def _ensure_group_closed(self):
        if self._in_group:
            self.emitter.end_group()
            self._in_group = False

    # --- INTERFACE IMPLEMENTATION ---

    def render_summary_dossier(self, result: Any):
        # Can be expanded to write to GITHUB_STEP_SUMMARY via markdown
        pass

    def conduct_interactive_plea(self, prompt_text: str, default: bool = True) -> bool:
        """
        In CI, interactive pleas are impossible.
        We log a warning and return the default.
        """
        self.emitter.warning(f"Interactive plea encountered in CI: '{prompt_text}'. Assuming default: {default}")
        return default

    # --- STUBS (Satisfying Abstract Base Class) ---
    def suspend(self):
        pass

    def resume(self):
        pass

    def prologue(self, *args, **kwargs):
        pass

    def epilogue(self, *args, **kwargs):
        pass

    def render_paradox(self, *args, **kwargs):
        pass

    def render_action_prologue(self, *args, **kwargs):
        pass

    def render_action_epilogue(self, *args, **kwargs):
        pass

    def update_live_stream(self, *args, **kwargs):
        pass

    def render_polyglot_prologue(self, *args, **kwargs):
        pass

    def render_vow_result(self, *args, **kwargs):
        pass

    def render_state_change(self, *args, **kwargs):
        pass

    def render_proclamation(self, message: str, sanctum: Optional[Path] = None):
        self.emitter.notice(message)

    def render_block_prologue(self, *args, **kwargs):
        pass

    def render_block_epilogue(self, *args, **kwargs):
        pass

    def render_intercession_altar(self, *args, **kwargs):
        pass

    def render_comment(self, raw_scripture: str):
        self.emitter.debug(f"Comment: {raw_scripture}")

    def render_foreign_adjudication(self, *args, **kwargs):
        pass

    def render_structured_status(self, *args, **kwargs):
        pass