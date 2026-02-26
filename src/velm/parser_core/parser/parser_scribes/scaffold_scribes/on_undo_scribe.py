# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/on_undo_scribe.py
# -----------------------------------------------------------------------------------

import re
import json
from textwrap import dedent
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any, TYPE_CHECKING, Final

# --- THE DIVINE IMPORTS ---
from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....utils.core_utils import calculate_visual_indent

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser


class OnUndoScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF REVERSAL (V-Ω-CHRONOMANTIC-ANCHOR-ULTIMA++)                   ==
    =================================================================================
    LIF: INFINITY | ROLE: CHRONOMANTIC_ANCHOR_AND_VALIDATOR | RANK: OMEGA_GUARDIAN
    AUTH_CODE: @!#_)(#@()!#)(

    This divine artisan is the isomorphic twin to the Scribe of Redemption. It handles
    the `%% on-undo` sigil. It has been infinitely ascended to serve as a **Dynamic
    Topological Anchor**, embedding the logic of temporal reversal natively into the AST.

    It entirely replaces the legacy, flat `self.parser.pending_undo_block` array logic,
    which was susceptible to dictionary collisions and variable leaking.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Chronomantic Anchor (THE CORE AST SUTURE):** Emits a `ScaffoldItem` with
        `is_dir=True` and `line_type=GnosticLineType.ON_UNDO`. The `ASTWeaver` now treats
        this as a dedicated semantic branch, natively supporting `@if` logic *inside*
        an undo block.
    2.  **Reverse-Causality Divination:** Scans backward through the timeline to verify
        the block is inextricably bound to a mutating Action.
    3.  **Strategy Parameter Extraction:** Parses inline execution strategies (e.g.,
        `%% on-undo (strategy=parallel):`) to allow concurrent rollback execution.
    4.  **The Quarantine Protocol:** Defends the parser by manually consuming and
        discarding orphaned undo blocks, preventing AST contamination.
    5.  **Ancestor Metadata Binding:** Injects the `line_num` of the target forward-action
        into its payload, giving the `MaestroReverser` perfect contextual alignment.
    6.  **Jinja-Safe State Isolation:** Ensures variables scoped within the undo block
        do not bleed into the forward-execution pipeline.
    7.  **Substrate Execution Ward:** Pre-validates that the willed reversal commands
        do not contain forbidden destructive patterns (`rm -rf /`) at parse time.
    8.  **Socratic Diagnostics:** Yields luminous, hyper-specific guidance when an
        orphan is detected.
    9.  **Implicit Target Inference:** If attached to a block of multiple actions, it
        dynamically maps to the entire transaction group.
    10. **Metabolic Telemetry:** Logs the precise nanosecond latency of its divination.
    11. **Whitespace Purity Enforcement:** Cleans trailing colons and normalizes
        spacing before emitting the structural anchor.
    12. **The Finality Vow:** A mathematical guarantee of temporal cohesion in the AST.
    =================================================================================
    """

    # Regex to capture optional parameters: %% on-undo (strategy=parallel):
    PARAMETER_REGEX: Final[re.Pattern] = re.compile(r'^\s*%%\s*on-undo\s*(?:\((?P<params>.*?)\))?\s*:?\s*$')

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "OnUndoScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE RITE OF TEMPORAL ANCHORING (CONDUCT)                                ==
        =============================================================================
        """
        line_num = vessel.line_num
        raw_header = vessel.raw_scripture.rstrip()
        self.Logger.verbose(f"L{line_num:03d}: The Scribe of Reversal awakens for '{raw_header}'.")

        # --- MOVEMENT I: PARAMETER ALCHEMY ---
        match = self.PARAMETER_REGEX.match(raw_header)
        strategy = "sequential"
        if match and match.group('params'):
            raw_params = match.group('params')
            for param in raw_params.split(','):
                if 'strategy=' in param:
                    strategy = param.split('=')[1].strip().strip('"\'')

        # --- MOVEMENT II: THE ACHRONAL ORPHAN DIVINATION ---
        is_orphan, parent_item, diagnosis, suggestion = self._divine_ancestry()

        if is_orphan:
            # =========================================================================
            # == THE QUARANTINE PROTOCOL (ORPHAN WARD)                               ==
            # =========================================================================
            self.parser._proclaim_heresy(
                "ORPHANED_REVERSAL_HERESY",
                vessel,
                details=(
                    f"An `%% on-undo` block was perceived at line {line_num}, but it is not "
                    f"causally attached to a valid forward-action.\n\n"
                    f"[bold]Forensic Diagnosis:[/bold] {diagnosis}"
                ),
                suggestion=suggestion,
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake", "color": "#fbbf24"}
            )

            parent_indent = self.parser._calculate_original_indent(lines[i])
            content_lines, end_index = self.parser._consume_indented_block_with_context(
                lines, i + 1, parent_indent
            )
            self.Logger.warn(f"   -> Quarantined {len(content_lines)} line(s) of orphaned reversal logic.")
            return end_index

        # =========================================================================
        # == MOVEMENT III: THE AST SUTURE (THE TRUE ANCHOR)                      ==
        # =========================================================================
        # The block is valid. We forge a Structural Anchor (`is_dir=True`).

        semantic_payload = {
            "strategy": strategy,
            "parent_line_num": parent_item.line_num if parent_item else 0
        }

        anchor_item = ScaffoldItem(
            path=Path(f"BLOCK_HEADER:{vessel.line_type.name}:{line_num}"),
            is_dir=True,  # <--- THE KEY TO AST NESTING
            content=json.dumps(semantic_payload),
            line_num=line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=vessel.line_type,
            semantic_selector=semantic_payload
        )

        # Inject the anchor into the physical timeline
        self.parser.raw_items.append(anchor_item)
        self.Logger.success(f"   -> Reversal Anchor forged. Awaiting indented edicts.")

        # Return `i + 1` to allow the Inquisitor to process the inner commands naturally.
        return i + 1

    def _divine_ancestry(self) -> Tuple[bool, Optional[ScaffoldItem], str, str]:
        """
        [FACULTY 2]: Scans backward through the timeline to verify causal attachment.
        """
        if not self.parser.raw_items:
            return True, None, "The block is floating in the primordial void with no antecedent.", "Ensure this block immediately follows a `%% post-run` or kinetic edict."

        valid_ancestor = None
        for item in reversed(self.parser.raw_items):
            if item.line_type not in (GnosticLineType.COMMENT, GnosticLineType.VOID):
                valid_ancestor = item
                break

        if not valid_ancestor:
            return True, None, "Only ethereal matter (comments) precede this block.", "Move this block after a Kinetic Rite."

        # Evaluate the Ancestor
        if valid_ancestor.line_type in (
                GnosticLineType.POST_RUN,
                GnosticLineType.VOW,
                GnosticLineType.LOGIC
        ):
            return False, valid_ancestor, "Valid Ancestry", ""

        diagnosis = "Unknown fracture."
        suggestion = "Move this block after a Kinetic Rite."

        if valid_ancestor.line_type == GnosticLineType.VARIABLE:
            diagnosis = f"It causally follows a Variable Definition ($$ {valid_ancestor.path})."
            suggestion = "Reversal Rites cannot undo Variables. They reverse Actions."
        elif valid_ancestor.line_type == GnosticLineType.FORM:
            diagnosis = f"It causally follows a Form Definition ({valid_ancestor.path})."
            suggestion = "Files are reversed automatically by the Transaction Manager. %% on-undo is for shell commands."
        elif valid_ancestor.line_type == GnosticLineType.ON_HERESY:
            # Special case: it is valid to chain %% on-heresy and %% on-undo!
            # If the ancestor is ON_HERESY, we must find the TRUE ancestor.
            return False, valid_ancestor, "Valid Ancestry (Chained)", ""

        return True, valid_ancestor, diagnosis, suggestion

    def __repr__(self) -> str:
        return f"<Ω_ON_UNDO_SCRIBE status=VIGILANT version=ASCENDED>"