# Path: scaffold/symphony/renderers/basic_renderer/emitter.py
# -----------------------------------------------------------

import sys
import datetime
from rich.text import Text
from rich.markup import escape
from .codex import BasicCodex
from ....logger import get_console


class BasicEmitter:
    """
    =================================================================================
    == THE FORENSIC SCRIBE (V-Ω-LINEAR-TIMESTAMP)                                  ==
    =================================================================================
    Writes timestamped, icon-prefixed lines to the console. It is fundamentally
    linear and does not support indentation to prevent the "Staircase Heresy".
    """

    def __init__(self):
        self.console = get_console()
        self.codex = BasicCodex()

    def _write_line(self, message: str, style: str, icon: str, timestamp: bool = True):
        """The atomic write operation."""
        ts = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] " if timestamp else "           "

        text = Text.assemble(
            (ts, "dim"),
            (f"{icon} ", style),
            (message, style)
        )
        self.console.print(text)
        sys.stdout.flush()

    def emit_prologue(self, command: str):
        self._write_line(command, self.codex.STYLES["command"], self.codex.ICONS["action"])

    def emit_epilogue(self, result: dict):
        rc = result.get('returncode', 1)
        duration = result.get('duration', 0.0)
        style = self.codex.STYLES["success"] if rc == 0 else self.codex.STYLES["failure"]
        icon = self.codex.ICONS["success"] if rc == 0 else self.codex.ICONS["failure"]
        msg = f"Rite Concluded (Exit {rc}) in {duration:.2f}s"
        self._write_line(msg, style, icon)

    def emit_stream(self, line: str):
        self._write_line(line, self.codex.STYLES["log_stream"], self.codex.ICONS["stream"], timestamp=False)

    def emit_vow(self, reason: str, success: bool):
        style = self.codex.STYLES["success"] if success else self.codex.STYLES["failure"]
        icon = self.codex.ICONS["vow"]
        self._write_line(reason, style, icon)

    def emit_state(self, key: str, value: str):
        style = self.codex.STYLES["state"]
        icon = self.codex.ICONS["state"]
        self._write_line(f"{key} = {value}", style, icon)