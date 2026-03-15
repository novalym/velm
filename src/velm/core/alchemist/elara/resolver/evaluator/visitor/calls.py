# Path: core/alchemist/elara/resolver/evaluator/visitor/calls.py
# --------------------------------------------------------------

import ast
from typing import Any
from .state import VisitorState
from ..void import VOID, GnosticVoid
from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy


class CallsEvaluator:
    """
    =============================================================================
    == THE CALLS EVALUATOR (V-Ω-TOTALITY)                                      ==
    =============================================================================
    Handles dynamic function invocations, parameter passing, and MRO checking.
    """

    def __init__(self, v_state: VisitorState, engine: Any):
        self.v_state = v_state
        self.engine = engine

    def _resolve_callable_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name): return node.id
        if isinstance(node, ast.Attribute): return node.attr
        return "anonymous_soul"

    def visit_Call(self, node: ast.Call) -> Any:
        """[ASCENSION 7]: Safe Call Arity Oracle integrated via execution wrap."""
        self.v_state.check_metabolism(node)

        try:
            func = self.engine.visit(node.func)
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return VOID
            raise e

        symbol_name = self._resolve_callable_name(node.func)

        if func is None or isinstance(func, GnosticVoid):
            if self.v_state.in_default_filter: return VOID
            raise UndefinedGnosisHeresy(
                symbol=symbol_name,
                message=f"Void Call: The rite of '{symbol_name}' is unmanifest in this timeline.",
                line_num=node.lineno,
                trace_id=self.v_state.trace_id
            )

        try:
            args = [self.engine.visit(a) for a in node.args]
            kwargs = {kw.arg: self.engine.visit(kw.value) for kw in node.keywords if kw.arg}
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            # Call Argument Shielding
            if self.v_state.in_default_filter: return VOID
            raise e

        if not callable(func):
            if self.v_state.in_default_filter: return VOID
            raise UndefinedGnosisHeresy(
                symbol=symbol_name,
                message=f"Profane Invocation: '{symbol_name}' ({type(func).__name__}) cannot be waked as a function.",
                line_num=node.lineno,
                trace_id=self.v_state.trace_id
            )

        try:
            # [ASCENSION 22]: Type-Cast Fast Path
            # Automatically coerce Python primitive casting if identified
            if symbol_name in ('int', 'float', 'str', 'bool') and func.__module__ == 'builtins':
                if not args: return func()
                return func(args[0])

            result = func(*args, **kwargs)
            return result if result is not None else VOID

        except Exception as catastrophic_paradox:
            if self.v_state.in_default_filter: return VOID
            if self.v_state.strict_mode:
                import traceback
                tb_str = traceback.format_exc()
                raise UndefinedGnosisHeresy(
                    symbol=f"RITE_FRACTURE:{symbol_name}",
                    message=f"Artisan Fracture: '{symbol_name}' shattered during strike: {catastrophic_paradox}",
                    details=f"Internal Traceback:\n{tb_str}",
                    line_num=node.lineno,
                    trace_id=self.v_state.trace_id
                )
            return VOID