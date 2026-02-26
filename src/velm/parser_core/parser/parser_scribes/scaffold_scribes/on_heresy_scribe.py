# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/on_heresy_scribe.py
# -------------------------------------------------------------------------------------

import re
import json
import sys
import traceback
from textwrap import dedent
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any, TYPE_CHECKING, Final

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....utils.core_utils import calculate_visual_indent

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser


class OnHeresyScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF REDEMPTION (V-Ω-DIAGNOSTIC-ANCHOR-HEALED)                     ==
    =================================================================================
    LIF: ∞ | ROLE: REDEMPTION_ANCHOR_AND_VALIDATOR | RANK: OMEGA_GUARDIAN

    Acts as a Topological Anchor for `%% on-heresy`.

    [THE CURE]:
    Now safely injects lists (`target_heresies`) and integers (`parent_line_num`)
    into the `semantic_selector` without Pydantic rebellion.
    """

    PARAMETER_REGEX: Final[re.Pattern] = re.compile(r'^\s*%%\s*on-heresy\s*(?:\((?P<params>.*?)\))?\s*:?\s*$')

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "OnHeresyScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        line_num = vessel.line_num
        raw_header = vessel.raw_scripture.rstrip()
        self.Logger.verbose(f"L{line_num:03d}: The Scribe of Redemption awakens for '{raw_header}'.")

        try:
            # --- MOVEMENT I: PARAMETER ALCHEMY ---
            match = self.PARAMETER_REGEX.match(raw_header)
            target_heresies = []
            if match and match.group('params'):
                raw_params = match.group('params')
                target_heresies = [p.strip() for p in raw_params.split(',') if p.strip()]

            # --- MOVEMENT II: THE ACHRONAL ORPHAN DIVINATION ---
            is_orphan, parent_item, diagnosis, suggestion = self._divine_ancestry()

            if is_orphan:
                self.parser._proclaim_heresy(
                    "ORPHANED_REDEMPTION_HERESY",
                    vessel,
                    details=f"Forensic Diagnosis: {diagnosis}",
                    suggestion=suggestion,
                    severity=HeresySeverity.CRITICAL,
                    ui_hints={"vfx": "shake", "color": "#ef4444"}
                )
                # Quarantine
                parent_indent = self.parser._calculate_original_indent(lines[i])
                content_lines, end_index = self.parser._consume_indented_block_with_context(
                    lines, i + 1, parent_indent
                )
                return end_index

            # --- MOVEMENT III: THE AST SUTURE ---
            semantic_payload = {
                "target_heresies": target_heresies if target_heresies else ["ALL"],
                "parent_line_num": parent_item.line_num if parent_item else 0
            }

            # [THE CURE]: semantic_selector now accepts Any type
            anchor_item = ScaffoldItem(
                path=Path(f"BLOCK_HEADER:{vessel.line_type.name}:{line_num}"),
                is_dir=True,
                content=json.dumps(semantic_payload, default=str),
                line_num=line_num,
                raw_scripture=vessel.raw_scripture,
                original_indent=vessel.original_indent,
                line_type=vessel.line_type,
                semantic_selector=semantic_payload
            )
            self.parser.raw_items.append(anchor_item)
            self.Logger.success(f"   -> Redemption Anchor forged.")

            return i + 1

        except Exception as e:
            sys.stderr.write(f"\n[ON_HERESY:CRASH] Exception at L{line_num}: {e}\n")
            traceback.print_exc(file=sys.stderr)
            self.parser._proclaim_heresy("ON_HERESY_SCRIBE_FRACTURE", vessel, details=str(e),
                                         severity=HeresySeverity.CRITICAL)
            return i + 1

    def _divine_ancestry(self) -> Tuple[bool, Optional[ScaffoldItem], str, str]:
        if not self.parser.raw_items:
            return True, None, "Floating in primordial void.", "Ensure this follows a Kinetic Rite."

        valid_ancestor = None
        for item in reversed(self.parser.raw_items):
            if item.line_type not in (GnosticLineType.COMMENT, GnosticLineType.VOID):
                valid_ancestor = item
                break

        if not valid_ancestor:
            return True, None, "Only ethereal matter precedes block.", "Move after Kinetic Rite."

        if valid_ancestor.line_type in (GnosticLineType.POST_RUN, GnosticLineType.VOW, GnosticLineType.LOGIC,
                                        GnosticLineType.ON_UNDO):
            return False, valid_ancestor, "Valid Ancestry", ""

        diagnosis = f"It follows a {valid_ancestor.line_type.name} definition."
        return True, valid_ancestor, diagnosis, "Redemption Rites must follow Actions."

    def __repr__(self) -> str:
        return f"<Ω_ON_HERESY_SCRIBE status=DIAGNOSTIC>"