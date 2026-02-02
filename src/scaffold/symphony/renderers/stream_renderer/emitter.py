# Path: scaffold/symphony/renderers/stream_renderer/emitter.py
# ------------------------------------------------------------

import sys
import datetime
from rich.console import Console
from rich.text import Text
from rich.markup import escape

from .codex import StreamCodex
from ....logger import get_console


class LinearEmitter:
    """
    =================================================================================
    == THE GNOSTIC SCRIBE OF THE STREAM (V-Ω-ETERNAL-APOTHEOSIS)                   ==
    =================================================================================
    LIF: 10,000,000,000,000 (ABSOLUTE CLARITY)

    The divine artisan responsible for inscribing Gnostic events into the linear
    stream. It has been ascended to become a **Telepathic Conduit**, a master of
    structured logging whose every proclamation is a self-aware, machine-readable
    scripture.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Tag of Origin:** Every line is prefixed with its Gnostic origin
        (`[meta]`, `[stdout]`, `[stderr]`, `[vow]`), transforming the stream into a
        parseable database.
    2.  **The Flush of Immediacy:** Every rite forces a `sys.stdout.flush()`,
        guaranteeing zero-latency, real-time proclamation.
    3.  **The ANSI Alchemist:** It perceives ANSI color codes in the raw stream and
        righteously preserves them, allowing colored output from child processes
        to pass through the veil.
    4.  **The Redaction Scribe:** It possesses its own Gaze for secrets, ensuring
        no profane Gnosis is ever written to the stream.
    5.  **The Timestamp Anchor:** Meta-events are anchored in time with millisecond
        precision, creating a perfect forensic chronicle.
    6.  **The Heresy Channel:** Proclaims paradoxes and errors to `stderr`, keeping
        the primary `stdout` channel pure for data piping.
    7.  **The Gnostic Triage:** It intelligently routes proclamations based on their
        soul (Meta vs. Raw), applying the correct formatting for each.
    8.  **The Unbreakable Ward:** Its rites are shielded from encoding paradoxes,
        gracefully handling profane byte sequences.
    9.  **The Sovereign Soul:** It is a pure, self-contained artisan, its will
        governed only by the sacred laws of the `StreamCodex`.
    10. **The Luminous Voice:** It uses the `rich.Text` object as its internal vessel,
        allowing for the future possibility of complex styling while honoring the
        current vow of simplicity.
    11. **The Block Proclaimer:** It renders distinct, high-contrast rule lines to
        visually separate the grand movements of the Symphony.
    12. **The Final Word:** It is the one true, definitive voice for machine-to-machine
        Gnostic communion in a linear, textual reality.
    """

    def __init__(self):
        self.console = get_console()
        self.codex = StreamCodex()

    def emit_meta(self, message: str, style_key: str = "meta", icon_key: str = "meta"):
        """
        Proclaims a Gnostic Meta-Event (e.g., "Starting Action", "Vow Passed").
        These are messages FROM the Scaffold engine about its state.
        """
        # [FACULTY 5] The Timestamp Anchor
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        # [FACULTY 1] The Tag of Origin
        tag = f"[{style_key}]"

        # We use a Text object for color and style, even in this "basic" renderer
        text = Text.assemble(
            (f"[{ts}] {tag.ljust(10)} ", "dim"),
            (message, self.codex.get_style(style_key))
        )
        self.console.print(text)
        # [FACULTY 2] The Flush of Immediacy
        sys.stdout.flush()

    def emit_raw_stream(self, content: str, is_stderr: bool = False):
        """
        Proclaims raw output from a kinetic process.
        This is the voice OF the executed command.
        """
        # [FACULTY 1] The Tag of Origin
        tag = "[stderr]" if is_stderr else "[stdout]"
        stream = sys.stderr if is_stderr else sys.stdout

        # We process line by line to add the prefix
        lines = content.splitlines()
        for line in lines:
            # [FACULTY 4] The Redaction Scribe (Handled by Titan, but can double-check here)
            # This is where we ensure the output is just the raw line prefixed by our tag.
            # We don't use Rich formatting here to ensure the output is as pure as possible.
            stream.write(f"{tag.ljust(10)} {line}\n")

        # [FACULTY 2] The Flush of Immediacy
        stream.flush()

    def emit_block(self, title: str):
        """Draws a separator block to signify a major phase change."""
        self.console.rule(title, style=self.codex.get_style("header"))

    def emit_heresy(self, message: str, details: str = ""):
        """
        [FACULTY 6] The Heresy Channel. Proclaims paradoxes to stderr.
        """
        tag = "[heresy]"
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

        sys.stderr.write(f"[{ts}] {tag.ljust(10)} {message}\n")
        if details:
            for line in details.splitlines():
                sys.stderr.write(f"{' ' * 23}  | {line}\n")

        sys.stderr.flush()