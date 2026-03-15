# Path: core/alchemist/elara/resolver/evaluator/visitor/primitives.py
# -------------------------------------------------------------------

import ast
from typing import Any
from .state import VisitorState
from ..void import VOID
from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy


class PrimitivesEvaluator:
    """
    =============================================================================
    == THE PRIMITIVES EVALUATOR (V-Ω-TOTALITY)                                 ==
    =============================================================================
    Handles raw constants, formatting, and ternary operators.
    """

    def __init__(self, v_state: VisitorState, engine: Any):
        self.v_state = v_state
        self.engine = engine

    def visit_Constant(self, node: ast.Constant) -> Any:
        self.v_state.check_metabolism(node)
        # [ASCENSION 9]: The Null-Byte Sarcophagus V8
        if isinstance(node.value, str) and '\x00' in node.value:
            return node.value.replace('\x00', '')
        return node.value

    def visit_JoinedStr(self, node: ast.JoinedStr) -> str:
        """[ASCENSION 4]: Substrate-Aware F-String Forge."""
        self.v_state.check_metabolism(node)
        try:
            return "".join(str(self.engine.visit(v)) for v in node.values)
        except Exception:
            return ""

    def visit_FormattedValue(self, node: ast.FormattedValue) -> Any:
        self.v_state.check_metabolism(node)
        try:
            return self.engine.visit(node.value)
        except Exception:
            return ""

    def visit_IfExp(self, node: ast.IfExp) -> Any:
        """
        [ASCENSION 5]: TERNARY AMNESTY SHIELD.
        Lazy evaluation: The unchosen branch is NEVER evaluated, protecting
        it from UndefinedGnosisHeresy.
        """
        self.v_state.check_metabolism(node)
        try:
            # Evaluate Condition
            condition_truth = self.engine.visit(node.test)

            # Short-Circuit to the chosen path
            if condition_truth:
                return self.engine.visit(node.body)
            else:
                return self.engine.visit(node.orelse)

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as gnostic_fracture:
            if self.v_state.in_default_filter:
                return None
            raise gnostic_fracture