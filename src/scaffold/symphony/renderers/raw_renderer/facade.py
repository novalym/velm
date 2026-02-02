# Path: scaffold/symphony/renderers/raw_renderer/facade.py
# --------------------------------------------------------

import sys
from typing import Any, Union, List, Dict, Optional
from pathlib import Path
from ..base import Renderer
from ....contracts.symphony_contracts import ConductorEvent, EventType, Edict, ActionResult, SymphonyResult

class RawRenderer(Renderer):
    """
    =================================================================================
    == THE INVISIBLE HAND (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                          ==
    =================================================================================
    LIF: ∞ (ABSOLUTE FIDELITY)

    The purest of all scribes. Its Prime Directive is to become a perfect, invisible
    conduit between the soul of a running process and the terminal. It adds no
    prefixes, no timestamps, no colors, no icons, no panels. It is the raw,
    unadulterated truth.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gaze of the Void:** Ignores all meta-events (start, stop, state changes).
    2.  **The Pure Pipe:** Writes `LOG` events directly to `sys.stdout` without modification.
    3.  **The Flush of Immediacy:** Forces a `flush()` after every write to guarantee zero latency.
    4.  **The Silent Heresy:** Proclaims paradoxes to `sys.stderr` for stream separation.
    5.  **The Unbreakable Contract:** Honors every vow of the `Renderer` contract, even if by silence.
    6.  **The Zero-Overhead Mind:** Contains almost no internal state or logic.
    7.  **The Machine's Voice:** Perfect for piping to other CLI tools (`| grep`, `| jq`).
    8.  **The IDE's Ear:** Ideal for output channels that need clean, parsable text.
    9.  **The Interactive Silence:** Returns a simple `True` for interactive pleas.
    10. **The Epilogue of Nothingness:** Prints no final summary to keep the output stream pure.
    11. **The Sovereign Soul:** Has zero dependencies, not even on Rich.
    12. **The Final Word:** It is the ultimate expression of the Unix philosophy.
    """

    def handle_event(self, event: ConductorEvent):
        """Only cares about LOG and PARADOX events."""
        if event.type == EventType.LOG:
            content = event.payload.get("content", "")
            # Direct, unbuffered write to stdout
            sys.stdout.write(content + '\n')
            sys.stdout.flush()
        elif event.type == EventType.PARADOX_PROCLAIMED:
            # Errors go to stderr to not pollute the pipe
            sys.stderr.write(f"Symphony Paradox: {event.payload.get('message')}\n")
            sys.stderr.flush()

    def conduct_interactive_plea(self, prompt_text: str, default: bool = True) -> bool:
        return default

    # --- All other methods are silent ---
    def prologue(self, *args, **kwargs): pass
    def epilogue(self, *args, **kwargs): pass
    def render_summary_dossier(self, result: SymphonyResult): pass
    def render_paradox(self, *args, **kwargs): pass
    def render_action_prologue(self, *args, **kwargs):
        """
        [THE VOW OF SILENCE]
        The Raw Renderer does not proclaim meta-events. It is a pure conduit
        for the child process's soul. This is the correct implementation.
        """
        pass

    def render_action_epilogue(self, *args, **kwargs):
        """
        [THE VOW OF SILENCE]
        No summary or final status is printed to keep the output stream pure.
        The exit code is known by the calling process.
        """
        pass

    def update_live_stream(self, live_context: Any, line: Union[str, Any]):
        """
        [THE PURE PIPE]
        The one true purpose of this renderer. Writes the line directly to stdout.
        """
        # The handle_event logic already does this, but we implement it here
        # for full contract compliance and clarity.
        content = str(line)
        sys.stdout.write(content + '\n')
        sys.stdout.flush()

    def render_polyglot_prologue(self, *args, **kwargs): pass
    def render_vow_result(self, *args, **kwargs): pass
    def render_state_change(self, *args, **kwargs): pass
    def render_proclamation(self, *args, **kwargs): pass
    def render_block_prologue(self, *args, **kwargs): pass
    def render_block_epilogue(self, *args, **kwargs): pass
    def render_intercession_altar(self, *args, **kwargs): pass
    def render_comment(self, *args, **kwargs): pass
    def render_foreign_adjudication(self, *args, **kwargs): pass
    def render_structured_status(self, *args, **kwargs): pass
    def suspend(self): pass
    def resume(self): pass