# Path: core/alchemist/elara/resolver/evaluator/visitor/engine.py
# ---------------------------------------------------------------

import ast
import traceback
from typing import Any, TYPE_CHECKING

# [THE MASTER CURE]: ACHRONAL TYPE SHIELDING
# Move the LexicalScope import to the shadow realm to prevent boot-deadlock.
if TYPE_CHECKING:
    from ...context import LexicalScope

from .state import VisitorState
from .identity import IdentityEvaluator
from .primitives import PrimitivesEvaluator
from .operators import OperatorsEvaluator
from .collections import CollectionsEvaluator
from .calls import CallsEvaluator

from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy, SecurityHeresy, MetabolicFeverHeresy
from .......logger import Scribe

Logger = Scribe("SafeEvaluator")


class SafeEvaluator(ast.NodeVisitor):
    """
    =================================================================================
    == THE SAFE EVALUATOR ENGINE (V-Ω-TOTALITY-VMAX-ZERO-STICTION)                 ==
    =================================================================================
    LIF: ∞^∞ | ROLE: AST_EXECUTION_ROUTER | RANK: OMEGA_SOVEREIGN_PRIME[THE MASTER CURE]: The `time.sleep(0)` context switch has been mathematically
    exorcised from the AST walk. The Evaluator now executes Python expressions
    at the raw speed of the C-Interpreter.
    """

    __slots__ = ('v_state', 'identity', 'primitives', 'operators', 'collections', 'calls')

    def __init__(self, scope: 'LexicalScope', strict_mode: bool = True):
        self.v_state = VisitorState(scope, strict_mode)

        # Initialize Sub-Organs
        self.identity = IdentityEvaluator(self.v_state, self)
        self.primitives = PrimitivesEvaluator(self.v_state, self)
        self.operators = OperatorsEvaluator(self.v_state, self)
        self.collections = CollectionsEvaluator(self.v_state, self)
        self.calls = CallsEvaluator(self.v_state, self)

    def evaluate(self, tree: ast.Expression) -> Any:
        """The Absolute Point of Ignition."""
        try:
            return self.visit(tree.body)

        except (UndefinedGnosisHeresy, SecurityHeresy, MetabolicFeverHeresy, AmnestyGrantedHeresy):
            raise
        except Exception as catastrophic_paradox:
            if self.v_state.strict_mode:
                tb_str = traceback.format_exc()
                raise UndefinedGnosisHeresy(
                    symbol="KERNEL_PANIC",
                    message=f"Logic Fracture in SGF Evaluator: {str(catastrophic_paradox)}",
                    details=f"Internal Traceback:\n{tb_str}",
                    trace_id=self.v_state.trace_id
                )
            # Use Sentinel Return rather than throwing exceptions to save performance
            return None

    # --- THE DELEGATION RITES (Direct Passthrough) ---

    def visit_Constant(self, node: ast.Constant) -> Any:
        return self.primitives.visit_Constant(node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> str:
        return self.primitives.visit_JoinedStr(node)

    def visit_FormattedValue(self, node: ast.FormattedValue) -> Any:
        return self.primitives.visit_FormattedValue(node)

    def visit_IfExp(self, node: ast.IfExp) -> Any:
        return self.primitives.visit_IfExp(node)

    def visit_Name(self, node: ast.Name) -> Any:
        return self.identity.visit_Name(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        return self.identity.visit_Attribute(node)

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        return self.identity.visit_Subscript(node)

    def visit_Index(self, node: ast.Index) -> Any:
        return self.identity.visit_Index(node)

    def visit_Slice(self, node: ast.Slice) -> Any:
        return self.identity.visit_Slice(node)

    def visit_ExtSlice(self, node: ast.ExtSlice) -> Any:
        return self.identity.visit_ExtSlice(node)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        return self.operators.visit_BinOp(node)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        return self.operators.visit_UnaryOp(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> bool:
        return self.operators.visit_BoolOp(node)

    def visit_Compare(self, node: ast.Compare) -> bool:
        return self.operators.visit_Compare(node)

    def visit_List(self, node: ast.List) -> list:
        return self.collections.visit_List(node)

    def visit_Tuple(self, node: ast.Tuple) -> tuple:
        return self.collections.visit_Tuple(node)

    def visit_Set(self, node: ast.Set) -> set:
        return self.collections.visit_Set(node)

    def visit_Dict(self, node: ast.Dict) -> dict:
        return self.collections.visit_Dict(node)

    def visit_ListComp(self, node: ast.ListComp) -> list:
        return self.collections.visit_ListComp(node)

    def visit_DictComp(self, node: ast.DictComp) -> dict:
        return self.collections.visit_DictComp(node)

    def visit_SetComp(self, node: ast.SetComp) -> set:
        return self.collections.visit_SetComp(node)

    def visit_Call(self, node: ast.Call) -> Any:
        return self.calls.visit_Call(node)

    def generic_visit(self, node: ast.AST) -> Any:
        if self.v_state.strict_mode:
            raise SecurityHeresy(target=type(node).__name__, line_num=getattr(node, 'lineno', 0),
                                 col_num=getattr(node, 'col_offset', 0))
        return f"<UNSUPPORTED_NODE:{type(node).__name__}>"