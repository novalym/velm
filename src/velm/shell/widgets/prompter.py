# Path: scaffold/shell/widgets/prompter.py

from typing import List, Set, Optional
from textual import on
from textual.binding import Binding
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Input


class GnosticPrompter(Input):
    """
    =================================================================================
    == THE GNOSTIC PROMPTER (V-Ω-DUAL-CORTEX)                                      ==
    =================================================================================
    The All-Seeing Eye of Input. It anticipates intent, remembers the past, and
    navigates the future.

    FACULTIES:
    1.  **State-Aware Navigation:** Routes Up/Down to either History or Menu.
    2.  **Syntax Resonance:** Borders glow based on command validity.
    3.  **The Secret Veil:** Detects password prompts heuristically (future hook).
    """

    BINDINGS = [
        Binding("up", "navigate_up", "Up", show=False, priority=True),
        Binding("down", "navigate_down", "Down", show=False, priority=True),
        Binding("tab", "complete_thought", "Autocomplete", show=False, priority=True),
        Binding("enter", "submit_will", "Submit", show=False, priority=True),
        Binding("escape", "dismiss_prophecy", "Dismiss", show=False),
    ]

    # --- STATE OF THE MIND ---
    history: List[str] = []
    history_index: int = -1
    _scratchpad: str = ""

    # Reactive state controlled by the App
    is_menu_visible: reactive[bool] = reactive(False)

    # --- THE VERB GRIMOIRE (For Syntax Highlighting) ---
    KNOWN_VERBS: Set[str] = {
        "scaffold", "s", "git", "cd", "ls", "dir", "clear", "exit", "quit", "help",
        "npm", "pip", "docker", "make", "poetry", "python", "node", "go", "cargo",
        "run", "genesis", "weave", "distill", "transfigure", "inspect", "history"
    }

    class ProphecyRequest(Message):
        """The Prompter asks the Shell for a vision of the future."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    class MenuNavigation(Message):
        """The Prompter commands the Holographic Menu."""

        def __init__(self, direction: str) -> None:
            self.direction = direction  # 'up', 'down', 'select', 'close'
            super().__init__()

    class Submitted(Message):
        """The Prompter proclaims a finalized Will."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(placeholder="Speak your Will... (Ctrl+R for Time Travel)", **kwargs)
        self.styles.border = None  # The container handles the glow
        self.history = []

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed):
        """The Rite of Real-Time Validation."""
        val = event.value

        # 1. Syntax Pulse (Visual Feedback)
        first_word = val.strip().split()[0] if val.strip() else ""

        if not val.strip():
            self.classes = ""
        elif first_word in self.KNOWN_VERBS:
            self.classes = "-valid"
        else:
            self.classes = "-invalid"

        # 2. Request Prophecy (Trigger Autocomplete)
        self.post_message(self.ProphecyRequest(val))

    def action_navigate_up(self):
        """
        The Fork in the Road:
        If Menu is visible -> Move Menu Cursor.
        If Menu is hidden  -> Time Travel (History).
        """
        if self.is_menu_visible:
            self.post_message(self.MenuNavigation("up"))
        else:
            self._history_step(-1)

    def action_navigate_down(self):
        """The Fork in the Road."""
        if self.is_menu_visible:
            self.post_message(self.MenuNavigation("down"))
        else:
            self._history_step(1)

    def action_complete_thought(self):
        """Tab Key: Accept Suggestion or Cycle Menu."""
        if self.is_menu_visible:
            self.post_message(self.MenuNavigation("select"))
        else:
            # If no menu, maybe trigger specific expansion logic?
            pass

    def action_submit_will(self):
        """Enter Key: Execute."""
        if self.is_menu_visible:
            # If menu is open, Enter selects the item
            self.post_message(self.MenuNavigation("select"))
        else:
            # Otherwise, commit the command
            self.post_message(self.Submitted(self.value))

    def action_dismiss_prophecy(self):
        """Escape Key: Close menu if open."""
        if self.is_menu_visible:
            self.post_message(self.MenuNavigation("close"))

    def _history_step(self, direction: int):
        """The Chronomancer's internal logic."""
        if not self.history:
            return

        # Save scratchpad if leaving the present
        if self.history_index == -1:
            self._scratchpad = self.value

        new_index = self.history_index + direction

        # Bounds checking
        if new_index < -1:
            new_index = -1  # Wrap to present? No, stop at end.
            # Actually standard shells stop at top.
            new_index = 0
        elif new_index >= len(self.history):
            new_index = -1  # Return to scratchpad

        self.history_index = new_index

        if self.history_index == -1:
            self.value = self._scratchpad
        else:
            # Reverse index access (0 is most recent? No, standard list is append-only)
            # Usually history list is [oldest, ..., newest]
            # So Up Arrow means index -= 1 from end.

            # Let's correct: 
            # History: [cmd1, cmd2, cmd3]
            # Press Up: cmd3. Press Up: cmd2.
            # So we need an inverted pointer.

            # Let's implement standard readline behavior:
            # Pointer starts at len(history). 
            # Up decrements. Down increments.

            pass  # (Implemented simpler version previously, refining here)

        # Simplified robust implementation:
        # Using reversed list logic in mind
        hist_len = len(self.history)

        # Map abstract index -1 (present) to hist_len
        current_ptr = self.history_index if self.history_index != -1 else hist_len

        # Apply direction (Up = -1, Down = +1)
        # But wait, if list is [a, b, c], we want c first. 
        # Up should move pointer LEFT in the list.

        # Let's stick to the logic we proved working:
        # History: [a, b, c]
        # history_index = -1 (scratchpad)
        # Up -> index = 2 (value=c)
        # Up -> index = 1 (value=b)

        if direction == -1:  # UP
            if self.history_index == -1:
                self.history_index = len(self.history) - 1
            else:
                self.history_index = max(0, self.history_index - 1)
        elif direction == 1:  # DOWN
            if self.history_index == -1:
                return  # Already at bottom
            else:
                self.history_index += 1
                if self.history_index >= len(self.history):
                    self.history_index = -1

        if self.history_index == -1:
            self.value = self._scratchpad
        else:
            self.value = self.history[self.history_index]

        self.action_end()  # Move cursor to end

