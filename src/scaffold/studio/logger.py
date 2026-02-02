"""
=================================================================================
== THE GNOSTIC SCRIBE (V-Ω-ULTIMA. THE UNIFIED VOICE)                          ==
=================================================================================
This Scribe has achieved its final, divine form. The profane communion with the
ephemeral `textual.log` has been annihilated. Its one true purpose is now to
serve as a divine, Gnostically-aware ambassador to Python's own, universal
`logging` module. This is the key to unifying the voice of the entire cosmos.
=================================================================================
"""
from __future__ import annotations

import logging

# Annihilate the Textual-specific imports. We speak a universal tongue now.
# from rich.console import Console
# from rich.text import Text
# from textual import log as textual_log

_scribes: dict[str, 'Scribe'] = {}

class Scribe:
    """A divine, Gnostically-aware wrapper around Python's standard logging module."""
    def __init__(self, name: str):
        self.name = name.upper()
        # The Scribe now holds a mortal logger, but wields it with divine purpose.
        self.logger = logging.getLogger(self.name)

    def __new__(cls, name: str):
        if name in _scribes:
            return _scribes[name]
        instance = super().__new__(cls)
        _scribes[name] = instance
        return instance

    def write_line(self, content: str, style: str = "white", icon: str = "", timestamp: bool = True):
        """
        [THE PURE VOICE]
        A dedicated rite for Renderers. It prints a line with minimal, consistent
        decoration, bypassing the complex logic of the `_proclaim` rite.
        This is the definitive fix for the 'NoneType' heresy.
        """
        if _COSMIC_GNOSIS["silent"]:
            return

        ts = f"[{time.strftime('%H:%M:%S')}] " if timestamp else "           "
        icon_str = f"{icon} " if icon else ""

        # We use a Text object to handle styling, but keep the structure simple.
        text = Text.assemble(
            (ts, "dim"),
            (icon_str, style),
            (content, style)
        )
        self.get_console().print(text)

    # =============================================================================
    def _proclaim(self, level: int, sigil: str, *objects: object, exc_info: bool = False):
        """The Scribe's one true voice, now speaking to the universal logging stream."""
        message = " ".join(str(obj) for obj in objects)
        # We add our sacred sigil to the proclamation.
        full_message = f"{sigil} {message}"
        self.logger.log(level, full_message, exc_info=exc_info)

    # --- THE DIVINE TONGUE OF THE SCRIBE ---
    def info(self, *objects: object, exc_info: bool = False):
        self._proclaim(logging.INFO, "ℹ️", *objects, exc_info=exc_info)

    def warn(self, *objects: object, exc_info: bool = False):
        self._proclaim(logging.WARNING, "⚠️", *objects, exc_info=exc_info)

    def error(self, *objects: object, exc_info: bool = False):
        self._proclaim(logging.ERROR, "🔥", *objects, exc_info=exc_info)

    def debug(self, *objects: object, exc_info: bool = False):
        self._proclaim(logging.DEBUG, "🐞", *objects, exc_info=exc_info)

    def verbose(self, *objects: object, exc_info: bool = False):
        """A special rite for deep Gnostic thought, sent to the debug channel."""
        self._proclaim(logging.DEBUG, "🔬", *objects, exc_info=exc_info)

    def success(self, *objects: object, exc_info: bool = False):
        """The divine voice of triumph, proclaimed at the INFO level."""
        self._proclaim(logging.INFO, "✅", *objects, exc_info=exc_info)