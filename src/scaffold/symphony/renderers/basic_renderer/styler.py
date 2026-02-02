# Path: scaffold/symphony/renderers/basic_renderer/styler.py
# ----------------------------------------------------------

from typing import Dict, Tuple


class BasicStyler:
    """
    =================================================================================
    == THE CODEX OF FORENSIC AESTHETICS (V-Ω-SEMANTIC-PALETTE)                     ==
    =================================================================================
    LIF: 10,000,000,000

    Defines the visual language of the linear log. Unlike the Cinematic renderer,
    this palette prioritizes readability, grep-ability, and clear status indicators
    for CI/CD logs.
    """

    # --- THE SIGILS OF STATE ---
    ICONS: Dict[str, str] = {
        "symphony_start": "🎼",
        "symphony_end": "🏁",
        "action": "⚙️",
        "vow": "⚖️",
        "state": "🧠",
        "logic": "🔀",
        "loop": "Hx",
        "success": "✔",
        "failure": "✘",
        "warning": "⚠️",
        "info": "ℹ️",
        "polyglot": "🔮",
        "secret": "🔒",
        "intercession": "🛡️"
    }

    # --- THE PALETTE OF TRUTH ---
    STYLES: Dict[str, str] = {
        "timestamp": "dim white",
        "header": "bold magenta",
        "command": "bold cyan",
        "success": "green",
        "error": "bold red",
        "warning": "yellow",
        "path": "blue underline",
        "value": "magenta",
        "key": "cyan",
        "log_stream": "dim white"
    }

    @classmethod
    def get_icon(cls, key: str) -> str:
        """Retrieves the sacred sigil for a concept."""
        return cls.ICONS.get(key, "•")

    @classmethod
    def get_style(cls, key: str) -> str:
        """Retrieves the color of truth for a concept."""
        return cls.STYLES.get(key, "white")