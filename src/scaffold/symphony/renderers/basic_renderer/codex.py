# Path: scaffold/symphony/renderers/basic_renderer/codex.py
# ---------------------------------------------------------
from typing import Dict

class BasicCodex:
    """The visual language of the Forensic Scribe."""
    ICONS: Dict[str, str] = {
        "action": "⚙️", "vow": "⚖️", "state": "🔮",
        "success": "✔", "failure": "✘", "prologue": "▶", "epilogue": "■",
        "stream": "│"
    }
    STYLES: Dict[str, str] = {
        "command": "bold cyan", "success": "green", "failure": "red",
        "vow": "magenta", "state": "yellow", "prologue": "dim", "epilogue": "dim",
        "log_stream": "white"
    }