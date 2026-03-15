# Path: parser_core/parser/ast_weaver/stack_manager/adjudicator.py
# ----------------------------------------------------------------

import re
from typing import Optional

from .....contracts.data_contracts import _GnosticNode, GnosticLineType, ScaffoldItem


class SiblingAdjudicator:
    """
    =============================================================================
    == THE LOGIC-MATRIX DECOUPLER (V-Ω-SEMANTIC-TRUTH-ORACLE)                  ==
    =============================================================================
    [ASCENSION 5]: Isolates the complex, regex-heavy logic of determining if
    one AST node is the semantic closure of another.
    """

    @classmethod
    def is_closing_tag_for(cls, incoming_item: ScaffoldItem, stack_node: _GnosticNode) -> bool:
        """
        [THE SIBLING ADJUDICATOR]
        Determines if the incoming `item` (e.g., @else) structurally replaces
        the `stack_node` (e.g., @if) at the exact same indentation level.
        """
        # If the active stack node has no physical item, it cannot be closed
        if not stack_node.item:
            return False

        valid_types = (GnosticLineType.LOGIC, GnosticLineType.SGF_CONSTRUCT)

        # Fast fail if either item is not a logic gate
        if stack_node.item.line_type not in valid_types: return False
        if incoming_item.line_type not in valid_types: return False

        start_type = cls._extract_logic_type(stack_node.item)
        end_type = cls._extract_logic_type(incoming_item)

        if not start_type or not end_type:
            return False

        # --- THE LOGIC MATRIX ---
        # [ASCENSION 9]: SGF-Aware Boundary Detection

        # IF is closed by ELIF, ELSE, ENDIF
        if start_type in ("IF", "ELIF") and end_type in ("ELIF", "ELSE", "ENDIF"):
            return True

        # ELSE is closed by ENDIF
        if start_type == "ELSE" and end_type == "ENDIF":
            return True

        # FOR is closed by ENDFOR
        if start_type == "FOR" and end_type == "ENDFOR":
            return True

        # TRY is closed by CATCH, FINALLY, ENDTRY
        if start_type in ("TRY", "CATCH") and end_type in ("CATCH", "FINALLY", "ENDTRY"):
            return True

        if start_type == "FINALLY" and end_type == "ENDTRY":
            return True

        return False

    @classmethod
    def _extract_logic_type(cls, item: ScaffoldItem) -> str:
        """
        [ASCENSION 6]: Apophatic Type Extraction.
        Extracts the canonical logic keyword (IF, ELSE, FOR) using fast attributes
        before falling back to Regex.
        """
        # 1. Try explicit condition type first (Fastest)
        if item.condition_type:
            s = str(item.condition_type).upper()
            if 'CONDITIONALTYPE.' in s:
                return s.split('.')[-1]
            return s

        # 2. Try Regex on Jinja expression (Fallback)
        if item.sgf_expression:
            match = re.search(r'{%[-]?\s*(\w+)', item.sgf_expression)
            if match:
                return match.group(1).upper()

        return ""