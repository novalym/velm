# Path: scaffold/symphony/renderers/stream_renderer/codex.py
# ----------------------------------------------------------

from typing import Dict


class StreamCodex:
    """
    =================================================================================
    == THE CODEX OF THE RAW STREAM (V-Ω-ASCII-PURITY)                              ==
    =================================================================================
    LIF: 10,000,000,000

    A strictly textual palette. No emojis. No complex glyphs.
    Optimized for parsing by IDEs (VS Code) and CI/CD logs.
    """

    # --- THE SIGILS OF TEXT ---
    ICONS: Dict[str, str] = {
        "start": ">>",  # Action Start
        "stop": "##",  # Action End
        "action": ">>",  # Executing
        "output": "|",  # Stream Line prefix
        "error": "!!",  # Error
        "success": "[OK]",  # Success
        "failure": "[FAIL]",  # Failure
        "warning": "[WARN]",  # Warning
        "info": "--",  # Info
        "meta": "::",  # State Change
        "vow": "??"  # Vow Check
    }

    # --- THE PALETTE OF TRUTH ---
    # Colors are still allowed (ANSI), as most terminals/IDEs render them.
    STYLES: Dict[str, str] = {
        "header": "bold magenta",
        "prologue": "bold cyan",
        "stream_stdout": "white",
        "stream_stderr": "yellow",
        "success": "green",
        "failure": "red",
        "meta": "dim white"
    }

    @classmethod
    def get_icon(cls, key: str) -> str:
        return cls.ICONS.get(key, "")

    @classmethod
    def get_style(cls, key: str) -> str:
        return cls.STYLES.get(key, "white")