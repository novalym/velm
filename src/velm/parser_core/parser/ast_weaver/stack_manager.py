import re
from pathlib import Path
from typing import List, Tuple

from .contracts import StackFrame
from ....contracts.data_contracts import _GnosticNode, GnosticLineType, ScaffoldItem
from ....logger import Scribe

Logger = Scribe("ASTStackManager")


class StackManager:
    """
    =============================================================================
    == THE SOVEREIGN OF THE STACK (V-Ω-STATE-MACHINE)                          ==
    =============================================================================
    Manages the indentation hierarchy. It decides when to PUSH (child),
    when to POP (dedent), and when to SWAP (sibling logic).
    """

    def __init__(self, root_node: _GnosticNode):
        # Initialize with the Eternal Root
        self.stack: List[StackFrame] = [
            StackFrame(node=root_node, indent=-1, physical_path=Path("."))
        ]

    @property
    def current_frame(self) -> StackFrame:
        return self.stack[-1]

    @property
    def current_node(self) -> _GnosticNode:
        return self.stack[-1].node

    @property
    def current_phys_path(self) -> Path:
        return self.stack[-1].physical_path

    def adjust_for_item(self, item: ScaffoldItem):
        """
        The Grand Rite of Alignment.
        Adjusts the stack depth to match the incoming item's indentation.
        Handles the 'Sibling Logic' edge case (if/else).
        """
        while True:
            top = self.current_frame

            # 1. Root Guard: Never pop the root
            if top.is_root:
                break

            # 2. Child Case: Item is deeper than current top -> We are inside it. Stop.
            if item.original_indent > top.indent:
                break

            # 3. Dedent Case: Item is shallower -> Pop stack to find parent.
            if item.original_indent < top.indent:
                self._pop(f"Dedent ({item.original_indent} < {top.indent})")
                continue

            # 4. Sibling Case: Same indentation.
            # LOGIC FIX: Check if this new item CLOSES the current item (e.g. else closes if)
            if self._is_closing_tag_for(item, top.node):
                self._pop(f"Sibling Logic Closure ({item.raw_scripture.strip()} closes {top.node.name})")
                continue

            # 5. Form Sibling: If current top is a file (FORM), it can't have children at same indent.
            if top.node.item and top.node.item.line_type == GnosticLineType.FORM:
                self._pop("Sibling Form Node")
                continue

            # If we are here, we are a sibling logic block that does NOT close the previous one
            # (unlikely with correct logic, but safe to break)
            break

    def push(self, node: _GnosticNode, indent: int, path_context: Path):
        """Pushes a new context onto the stack."""
        self.stack.append(StackFrame(node, indent, path_context))
        # Logger.verbose(f"   -> Pushed '{node.name}' (Indent: {indent})")

    def _pop(self, reason: str):
        node = self.stack.pop().node
        # Logger.verbose(f"   <- Popped '{node.name}' ({reason})")

    def _is_closing_tag_for(self, item: ScaffoldItem, stack_node: _GnosticNode) -> bool:
        """
        [THE SIBLING ADJUDICATOR]
        Determines if the incoming `item` (e.g., @else) structurally replaces
        the `stack_node` (e.g., @if) at the same indentation level.
        """
        if not stack_node.item: return False

        # We only judge Logic nodes
        valid_types = (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT)
        if stack_node.item.line_type not in valid_types: return False
        if item.line_type not in valid_types: return False

        start_type = self._extract_logic_type(stack_node.item)
        end_type = self._extract_logic_type(item)

        if not start_type or not end_type: return False

        # The Logic Matrix
        # IF is closed by ELIF, ELSE, ENDIF
        if start_type in ("IF", "ELIF") and end_type in ("ELIF", "ELSE", "ENDIF"): return True
        # ELSE is closed by ENDIF
        if start_type == "ELSE" and end_type == "ENDIF": return True
        # FOR is closed by ENDFOR
        if start_type == "FOR" and end_type == "ENDFOR": return True

        return False

    def _extract_logic_type(self, item: ScaffoldItem) -> str:
        """Extracts the canonical logic keyword (IF, ELSE, FOR)."""
        # Try explicit condition type first
        if item.condition_type:
            s = str(item.condition_type).upper()
            if 'CONDITIONALTYPE.' in s: return s.split('.')[-1]
            return s

        # Try Regex on Jinja expression
        if item.jinja_expression:
            match = re.search(r'{%[-]?\s*(\w+)', item.jinja_expression)
            if match: return match.group(1).upper()

        return ""

