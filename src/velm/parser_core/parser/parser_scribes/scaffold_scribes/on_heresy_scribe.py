# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/on_heresy_scribe.py
# -------------------------------------------------------------------------------------

import re
from textwrap import dedent
from typing import List, Optional, Tuple

# --- THE DIVINE IMPORTS ---
from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....utils.core_utils import calculate_visual_indent


class OnHeresyScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF REDEMPTION (V-Ω-ORPHAN-SENTINEL-ULTIMA)                       ==
    =================================================================================
    LIF: 10,000,000,000 | ROLE: REDEMPTION_VALIDATOR | RANK: OMEGA_GUARDIAN

    This divine artisan is the specific handler for the `%% on-heresy` sigil when it
    is perceived by the Master Inquisitor.

    **GNOSTIC ARCHITECTURAL NOTE:**
    In the pure Gnostic Topology, an `on-heresy` block is causally bound to the
    preceding `post-run` block via the `PostRunScribe`'s prophetic lookahead (peeking).

    Therefore, if *this* Scribe is summoned by the main parsing loop, it signifies a
    **Metaphysical Fracture**: The Redemption Rite has been found wandering alone in
    the void, detached from the Action it was meant to save.

    This Scribe's purpose is to:
    1.  **Consume the Block** (to prevent syntax cascading errors).
    2.  **Analyze the Fracture** (Forensic Gaze).
    3.  **Proclaim the Heresy** (Orphaned Block Detection).
    """

    def __init__(self, parser):
        super().__init__(parser, "OnHeresyScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Rite of Orphan Adjudication.
        """
        line_num = vessel.line_num
        raw_header = vessel.raw_scripture.rstrip()

        self.Logger.verbose(f"L{line_num:03d}: The Scribe of Redemption awakens for '{raw_header}'.")

        # --- MOVEMENT I: THE RITE OF CONSUMPTION ---
        # We must consume the block even if it is an orphan, otherwise the parser
        # will try to interpret the commands inside as file paths or garbage.

        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Use the Parser's central block consumer to respect all Gnostic spacing laws
        content_lines, end_index = self.parser._consume_indented_block_with_context(
            lines, i + 1, parent_indent
        )

        block_size = len(content_lines)
        self.Logger.verbose(f"   -> Consumed {block_size} line(s) of orphaned redemption logic.")

        # --- MOVEMENT II: THE FORENSIC GAZE (WHY IS IT ORPHANED?) ---
        # We analyze the *previous* item in the parser's timeline to generate a
        # helpful, Socratic suggestion.

        last_item = self.parser.raw_items[-1] if self.parser.raw_items else None

        diagnosis = "The block is floating in the void with no antecedent."
        suggestion = "Ensure this block immediately follows a `%% post-run` or `%% on-undo` block."

        if last_item:
            if last_item.line_type == GnosticLineType.POST_RUN:
                # If the last item WAS a post-run, but we are here, it implies a separation.
                # Perhaps a blank line with whitespace, or a comment that broke the peeking chain.
                diagnosis = (
                    f"It follows a 'POST_RUN' block (L{last_item.line_num}), but the "
                    f"Causal Link was severed."
                )
                suggestion = (
                    "Remove any blank lines or interrupting comments between the "
                    "`%% post-run` block and the `%% on-heresy` block."
                )
            elif last_item.line_type == GnosticLineType.VARIABLE:
                diagnosis = f"It follows a Variable Definition ($$ {last_item.path})."
                suggestion = "Redemption Rites cannot redeem Variables. Move this block after a Kinetic Rite."
            elif last_item.line_type == GnosticLineType.FORM:
                diagnosis = f"It follows a Form Definition ({last_item.path})."
                suggestion = "Redemption Rites cannot redeem Files. Move this block after a Kinetic Rite."

        # --- MOVEMENT III: THE PROCLAMATION OF HERESY ---
        heresy_details = (
            f"An `%% on-heresy` block was found at line {line_num}, but it is not attached "
            f"to a valid parent rite.\n\n"
            f"[bold]Forensic Diagnosis:[/bold] {diagnosis}"
        )

        self.parser._proclaim_heresy(
            "ORPHANED_REDEMPTION_HERESY",
            vessel,
            details=heresy_details,
            suggestion=suggestion,
            severity=HeresySeverity.CRITICAL
        )

        # We return the end index so the parser can continue scanning for valid matter
        return end_index

    def __repr__(self) -> str:
        return f"<Ω_ON_HERESY_SCRIBE status=VIGILANT>"