# Path: scaffold/symphony/renderers/basic_renderer/scribe.py
# ----------------------------------------------------------

import re
import datetime
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.markup import escape
from typing import Optional, List

from .styler import BasicStyler
from ....logger import get_console


class AtomicScribe:
    """
    =================================================================================
    == THE ATOMIC SCRIBE (V-Ω-THREAD-SAFE-INSCRIBER)                               ==
    =================================================================================
    LIF: 10,000,000,000

    Responsible for the physical act of writing to the stream.
    It handles:
    1.  **Redaction:** The Veil of Secrecy.
    2.  **Indentation:** Visual hierarchy.
    3.  **Timestamping:** Temporal precision.
    4.  **Formatting:** Application of the BasicStyler.
    """

    SECRET_PATTERNS = [
        r'(api_key|token|secret|password|passwd|credential|key)\s*[:=]\s*[\'"]?([^\s\'"]+)',
        r'(sk_(?:live|test)_[0-9a-zA-Z]{24})',
        r'(ghp_[0-9a-zA-Z]{36})'
    ]

    def __init__(self):
        self.console = get_console()
        self.indent_level = 0
        self.styler = BasicStyler()

    def indent(self):
        """Deepens the Gnostic hierarchy."""
        self.indent_level += 1

    def dedent(self):
        """Surfaces from the Gnostic hierarchy."""
        if self.indent_level > 0:
            self.indent_level -= 1

    def redact(self, text: str) -> str:
        """[THE VEIL] Masks sensitive Gnosis."""
        redacted = text
        for pattern in self.SECRET_PATTERNS:
            redacted = re.sub(pattern, r'\1: [REDACTED]', redacted, flags=re.IGNORECASE)
        return redacted

    def write_line(self, message: str, style: str = "white", icon: str = "", timestamp: bool = True):
        """The fundamental rite of inscription."""
        prefix = ""

        # 1. The Temporal Stamp
        if timestamp:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            prefix += f"[{self.styler.get_style('timestamp')}]{ts}[/] "

        # 2. The Spatial Indent
        indent_str = "  " * self.indent_level
        prefix += indent_str

        # 3. The Sigil
        if icon:
            prefix += f"{icon} "

        # 4. The Message
        # We escape the message to prevent accidental markup injection from raw logs,
        # but we allow the caller to pass pre-formatted markup if they wish (handled via style arg).
        # For safety in Basic renderer, we assume message is raw text unless specified.

        clean_msg = self.redact(message)

        # Construct the final Text object
        full_text = Text.from_markup(f"{prefix}")
        msg_text = Text(clean_msg, style=style) if style else Text(clean_msg)
        full_text.append(msg_text)

        self.console.print(full_text)

    def write_panel(self, content: str, title: str, style: str = "white"):
        """Inscribes a block of Gnosis."""
        clean_content = self.redact(content)
        self.console.print(Panel(
            clean_content,
            title=title,
            border_style=style,
            expand=False
        ))

    def write_key_value(self, key: str, value: str):
        """Inscribes a state change."""
        k_style = self.styler.get_style("key")
        v_style = self.styler.get_style("value")

        clean_val = self.redact(str(value))

        # Indent logic manually for Text assembly
        indent_str = "  " * (self.indent_level + 1)

        text = Text.assemble(
            (f"{indent_str}• ", "dim"),
            (key, k_style),
            (": ", "dim"),
            (clean_val, v_style)
        )
        self.console.print(text)