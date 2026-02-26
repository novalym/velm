# Path: parser_core/parser/ast_weaver/weaver/gatekeeper.py
# ----------------------------------------------------------

import re
from .....contracts.data_contracts import ScaffoldItem


class LogicGatekeeper:
    """
    =============================================================================
    == THE LOGIC GATEKEEPER (V-Ω-CLOSURE-DIVINER)                              ==
    =============================================================================
    Determines the semantic intent of logic tags. Specifically, it identifies
    if a tag's sole purpose is to close a preceding block (e.g., @endif).
    """

    @classmethod
    def is_pure_closer(cls, item: ScaffoldItem) -> bool:
        """
        [ASCENSION 7]: THE CLOSER DIVINER.
        Detects tags that ONLY close a block (endif, endfor, endtry).
        """
        if item.condition_type:
            ctype_str = str(item.condition_type).upper()
            if 'CONDITIONALTYPE.' in ctype_str:
                ctype_str = ctype_str.split('.')[-1]
            return ctype_str.startswith('END')

        elif item.jinja_expression:
            match = re.search(r'{%[-]?\s*(\w+)', item.jinja_expression)
            if match:
                return match.group(1).lower().startswith('end')

        return False