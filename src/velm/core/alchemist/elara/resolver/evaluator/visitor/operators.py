# Path: core/alchemist/elara/resolver/evaluator/visitor/operators.py
# ------------------------------------------------------------------
import builtins
import ast
from typing import Any, Dict, List
from .state import VisitorState
from ..void import VOID, GnosticVoid
from ..constants import EvaluationConstants
from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy, SecurityHeresy
from ....library.tests import test_oracle
from ....library.registry import RITE_REGISTRY


class OperatorsEvaluator:
    """
    =============================================================================
    == THE KINETIC OPERATORS (V-Ω-TOTALITY)                                    ==
    =============================================================================
    Handles math, pipes (BitOr), Boolean short-circuiting, and Comparisons.
    """

    def __init__(self, v_state: VisitorState, engine: Any):
        self.v_state = v_state
        self.engine = engine

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """Handles standard Math and the Alchemical Pipe (|)."""
        self.v_state.check_metabolism(node)

        # --- THE ALCHEMICAL PIPE (|) ---
        if isinstance(node.op, ast.BitOr):
            filter_name = ""
            args = []
            kwargs = {}

            if isinstance(node.right, ast.Call):
                filter_name = self.engine.calls._resolve_callable_name(node.right.func)
            elif isinstance(node.right, ast.Name):
                filter_name = node.right.id
            else:
                try:
                    return self.engine.visit(node.left) | self.engine.visit(node.right)
                except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
                    if self.v_state.in_default_filter: return None
                    raise e

            is_mercy_filter = filter_name in ("default", "coalesce", "d")
            original_amnesty_state = self.v_state.in_default_filter
            self.v_state.in_default_filter = original_amnesty_state or is_mercy_filter

            try:
                try:
                    left_val = self.engine.visit(node.left)
                except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
                    if self.v_state.in_default_filter:
                        left_val = None
                    else:
                        raise e

                if isinstance(node.right, ast.Call):
                    try:
                        args = [self.engine.visit(a) for a in node.right.args]
                        kwargs = {kw.arg: self.engine.visit(kw.value) for kw in node.right.keywords if kw.arg}
                    except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
                        if self.v_state.in_default_filter:
                            args, kwargs = [None], {}
                        else:
                            raise e

                return self._conduct_pipe_alchemy(left_val, filter_name, args, kwargs, node.lineno)

            finally:
                self.v_state.in_default_filter = original_amnesty_state

        # --- STANDARD MATH ---
        try:
            left = self.engine.visit(node.left)
            right = self.engine.visit(node.right)
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return VOID
            raise e

        # [ASCENSION 20]: String Concatenation Sieve
        if isinstance(node.op, ast.Add) and isinstance(left, str) and isinstance(right, str):
            return "".join([left, right])

        if left is None or isinstance(left, GnosticVoid): left = 0
        if right is None or isinstance(right, GnosticVoid): right = 0

        op_handler = EvaluationConstants.OPERATORS.get(type(node.op))
        if not op_handler: return left

        try:
            return op_handler(left, right)
        except TypeError as te:
            try:
                return op_handler(float(left), float(right))
            except:
                if self.v_state.strict_mode: raise UndefinedGnosisHeresy(symbol="MATH_FRACTURE",
                                                                         message=f"Arithmetic Schism: {te}",
                                                                         line_num=node.lineno)
                return 0

    def _conduct_pipe_alchemy(self, value: Any, name: str, args: List, kwargs: Dict, line: int) -> Any:
        filter_func = self.v_state.filters.get(name)

        if not filter_func:
            rite_meta = RITE_REGISTRY.get_rite_metadata(name)
            if rite_meta:
                filter_func = rite_meta.handler
            else:
                filter_func = getattr(builtins, name, None)

        if not filter_func or not callable(filter_func):
            if self.v_state.strict_mode: raise UndefinedGnosisHeresy(symbol=f"filter:{name}",
                                                                     message=f"Void Filter: The rite of '{name}' is unmanifest.",
                                                                     line_num=line)
            return value

        if name in ('default', 'coalesce', 'd'):
            default_val = args[0] if args else ""
            if value is None or value == "" or isinstance(value, GnosticVoid): return default_val
            return value

        try:
            return filter_func(value, *args, **kwargs)
        except Exception as e:
            if self.v_state.strict_mode:
                if self.v_state.in_default_filter: return value
                raise UndefinedGnosisHeresy(symbol=f"filter_fracture:{name}",
                                            message=f"Filter '{name}' shattered: {str(e)}", line_num=line)
            return value

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        self.v_state.check_metabolism(node)
        try:
            operand = self.engine.visit(node.operand)
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return VOID
            raise e

        op_func = EvaluationConstants.OPERATORS.get(type(node.op))
        if not op_func: return operand
        try:
            return op_func(operand)
        except Exception:
            return operand

    def visit_BoolOp(self, node: ast.BoolOp) -> bool:
        """[ASCENSION 3]: Short-Circuit Boolean Evaluation Suture."""
        self.v_state.check_metabolism(node)
        try:
            if isinstance(node.op, ast.And):
                for value in node.values:
                    # If any false, short-circuit
                    if not self.engine.visit(value): return False
                return True
            if isinstance(node.op, ast.Or):
                for value in node.values:
                    # If any true, short-circuit
                    if self.engine.visit(value): return True
                return False
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return False
            raise e
        return False

    def visit_Compare(self, node: ast.Compare) -> bool:
        self.v_state.check_metabolism(node)
        try:
            left = self.engine.visit(node.left)
            for op, comparator in zip(node.ops, node.comparators):

                # ---[ASCENSION 19]: THE IS / IS NOT REDIRECTION ---
                if isinstance(op, (ast.Is, ast.IsNot)):
                    test_name = ""
                    test_args = []

                    if isinstance(comparator, ast.Name):
                        test_name = comparator.id
                    elif isinstance(comparator, ast.Call):
                        test_name = self.engine.calls._resolve_callable_name(comparator.func)
                        test_args = [self.engine.visit(a) for a in comparator.args]
                    else:
                        right = self.engine.visit(comparator)
                        op_func = EvaluationConstants.OPERATORS.get(type(op))
                        if not op_func(left, right): return False
                        left = right
                        continue

                    # Direct bridge to the Test Oracle
                    result = test_oracle.evaluate(left, test_name, *test_args)
                    if isinstance(op, ast.IsNot): result = not result
                    if not result: return False
                    continue

                # --- [ASCENSION 17]: C-Optimized Set Membership ---
                right = self.engine.visit(comparator)
                if isinstance(op, ast.In) and isinstance(right, list):
                    # Cast list to set in memory for O(1) lookup
                    right = set(right)

                op_func = EvaluationConstants.OPERATORS.get(type(op))
                if not op_func: return False
                if not op_func(left, right): return False
                left = right

            return True
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return False
            raise e