# Path: scaffold/parser_core/parser/parser_scribes/symphony_scribes/symphony_logic_scribe.py
# ------------------------------------------------------------------------------------------

"""
=================================================================================
== THE ORACLE OF GNOSTIC LOGIC (V-Ω-LEGENDARY. THE BRANCHING MIND)             ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000

This artisan handles the perception of Control Flow: `if:`, `elif:`, and `else:` blocks.
It uses **Recursive Parsing** to treat the indented body as a mini-symphony,
nesting the resulting Edicts within a parent Conditional Edict.

It enforces strict grammar on conditions and ensures that no block is a void.
=================================================================================
"""
from typing import List, TYPE_CHECKING, Tuple

from .symphony_block_scribe import SymphonyBlockScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import Edict, EdictType, ConditionalType
from pathlib import Path

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyLogicScribe(SymphonyBlockScribe):
    """
    The God-Engine of Gnostic Composition for logic blocks.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser)

    def _resolve_conditional_type(self, header: str) -> ConditionalType:
        """
        [ELEVATION 6: THE TYPE DIVINER]
        Returns the canonical Enum for the conditional type based on the raw header.
        """
        header = header.strip()
        if header.startswith(('if', '@if')): return ConditionalType.IF
        if header.startswith(('elif', '@elif')): return ConditionalType.ELIF
        if header.startswith(('else', '@else')): return ConditionalType.ELSE

        # Fallback should not be reached due to parser triage
        return ConditionalType.IF

    def _extract_condition(self, raw_header: str, directive: str) -> Tuple[str, str]:
        """
        [ELEVATION 1: CONDITION EXTRACTOR & CLEANSER]
        Surgically removes the keyword and colon.
        Returns (clean_condition_for_storage, raw_condition_for_logging)
        """
        if raw_header.startswith('@'):
            remainder = raw_header[len(directive) + 1:].strip()
        else:
            remainder = raw_header[len(directive):].strip()

        raw_condition = remainder.rstrip(':').strip()

        clean_condition = raw_condition
        if clean_condition.startswith('{{') and clean_condition.endswith('}}'):
            clean_condition = clean_condition[2:-2].strip()

        return clean_condition, raw_condition

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Conducts the Rite of Logical Branching (V-Ω-TUPLE-CORRECTED).

        *** APOTHEOSIS COMPLETE ***
        It now proclaims `ScaffoldItems` for logic blocks, making them visible to the AST.
        """
        line_num = vessel.line_num
        raw_header = vessel.raw_scripture.strip()
        directive = vessel.directive_type

        clean_condition_for_storage, raw_condition_for_logging = self._extract_condition(raw_header, directive)
        cond_type = self._resolve_conditional_type(raw_header)

        if directive == 'else' and raw_condition_for_logging:
            self.parser.heresies.append(ArtisanHeresy(
                f"ELSE_CONDITION_HERESY: 'else' blocks cannot have conditions. Did you mean 'elif'?",
                line_num=line_num
            ))
            return i + 1

        if directive in ('if', 'elif') and not raw_condition_for_logging:
            raise ArtisanHeresy("LOGIC_HERESY: Conditional block requires a non-empty expression.", line_num=line_num)

        # --- THE DIVINE HEALING: PROCLAIM THE GNOSTIC ANCHOR FOR LOGIC ---
        logic_anchor_item = ScaffoldItem(
            path=Path(f"LOGIC:{cond_type.name}:{line_num}"),
            is_dir=False,
            content=clean_condition_for_storage,
            line_num=line_num,
            raw_scripture=raw_header,
            original_indent=self.parser._calculate_original_indent(lines[i]),
            line_type=GnosticLineType.LOGIC,
            condition_type=cond_type,
            condition=clean_condition_for_storage
        )
        self.parser.raw_items.append(logic_anchor_item)
        # --- THE APOTHEOSIS IS COMPLETE ---

        block_content, end_index = self._consume_block(lines, i)

        if not block_content.strip():
            self.parser.heresies.append(ArtisanHeresy(
                f"EMPTY_LOGIC_HERESY: The '{raw_header}' block is a void. It serves no purpose.",
                line_num=line_num,
                severity=HeresySeverity.WARNING
            ))

        sub_parser = self.parser.__class__(grammar_key='symphony')
        sub_parser.variables = self.parser.variables.copy()

        _, _, _, sub_edicts, _, _ = sub_parser.parse_string(
            block_content,
            self.parser.file_path,
            line_offset=line_num
        )

        full_raw_scripture = f"{vessel.raw_scripture}\n{block_content}"

        edict = Edict(
            type=EdictType.CONDITIONAL,
            raw_scripture=full_raw_scripture,
            line_num=line_num,
            command=clean_condition_for_storage,
            conditional_type=cond_type,
            body=sub_edicts
        )

        self.parser.edicts.append(edict)

        # --- THE DIVINE HEALING PART 2: PROCLAIM THE CLOSING ANCHOR ---
        closing_anchor_item = ScaffoldItem(
            path=Path(f"LOGIC:ENDIF:{end_index}"),
            is_dir=False,
            line_num=end_index,
            raw_scripture="@endif",
            original_indent=self.parser._calculate_original_indent(lines[i]),
            line_type=GnosticLineType.LOGIC,
            condition_type=ConditionalType.ENDIF
        )
        self.parser.raw_items.append(closing_anchor_item)
        # --- THE APOTHEOSIS IS COMPLETE ---

        return end_index