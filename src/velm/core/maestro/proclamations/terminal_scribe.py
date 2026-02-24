# Path: src/velm/core/maestro/proclamations/terminal_scribe.py
# -----------------------------------------------------------

from rich.text import Text
from .base import ProclamationScribe


class TerminalScribe(ProclamationScribe):
    """The default, ultra-fast 'print' equivalent."""

    def proclaim(self, payload: str, metadata: dict):
        # [THE CURE]: Atomic Comma-Separation
        # If no payload but extra metadata exists, we treat it like print(a, b)
        if not payload and metadata:
            clean_msg = " ".join([str(v) for v in metadata.values()])
        else:
            clean_msg = self._purify(payload)

        # The Signature Chevron
        self.console.print(f"[bold cyan]»[/bold cyan] {clean_msg}")