
from pathlib import Path
from typing import List, Dict, Any, Tuple

from .contracts import MutationEdict, MutationOp
from ...contracts.data_contracts import GnosticLineType
from ...parser_core.parser import ApotheosisParser


class PatchParser:
    """
    [FACULTY 6] The Enhanced Gnostic Parser.
    Detects operators, vows, and semantic modifiers.
    """

    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables
        self.parser = ApotheosisParser(grammar_key='scaffold')

    def parse(self, content: str, context_path: Path) -> Tuple[List[MutationEdict], Dict[str, Any]]:
        _, items, _, _, variables, _ = self.parser.parse_string(
            content,
            file_path_context=context_path,
            pre_resolved_vars=self.variables
        )

        edicts = []
        last_edict = None

        for item in items:
            # --- Vow Attachment ---
            if item.line_type == GnosticLineType.VOW:
                if last_edict:
                    last_edict.vows.append(item.content)
                continue

            # Only process FORM items as mutations
            if item.line_type != GnosticLineType.FORM:
                continue

            raw = item.raw_scripture.strip()
            op = MutationOp.DEFINE  # Default

            if item.mutation_op == "+=":
                op = MutationOp.APPEND
            elif item.mutation_op == "^=":
                op = MutationOp.PREPEND
            elif item.mutation_op == "-=":
                op = MutationOp.SUBTRACT
            elif item.mutation_op == "~=":
                op = MutationOp.TRANSFIGURE
            # item.mutation_op might be None for defines

            # Anchor Hash (Legacy check, can be upgraded to Vow later)
            anchor_hash = None
            if "@hash:" in str(item.path):
                import re
                hash_match = re.search(r'@hash:([a-fA-F0-9]+)', str(item.path))
                if hash_match:
                    anchor_hash = hash_match.group(1)
                    clean_path_str = str(item.path).split('@hash:')[0].strip()
                    item.path = Path(clean_path_str)

            edict = MutationEdict(**item.model_dump())
            edict.mutation_op = op
            edict.anchor_hash = anchor_hash

            # Transfer Semantic Gnosis
            edict.semantic_selector = item.semantic_selector

            edicts.append(edict)
            last_edict = edict

        return edicts, variables