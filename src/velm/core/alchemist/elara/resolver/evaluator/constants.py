# Path: core/alchemist/elara/resolver/evaluator/constants.py
# ----------------------------------------------------------

import ast
import operator
import os
import sys
from typing import Dict, Callable, Set, Final

# [ASCENSION 18]: Substrate DNA Identification
IS_WASM: Final[bool] = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

class EvaluationConstants:
    """The Immutable Laws of the SGF Evaluator."""

    #[ASCENSION 8]: Hardware pacing limits
    MAX_NODE_COUNT: Final[int] = 5000
    MAX_EVAL_TIME_NS: Final[int] = 500_000_000  # 500ms

    # Operators map for high-speed dispatch
    OPERATORS: Final[Dict[type, Callable]] = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod, ast.Pow: operator.pow,
        ast.Eq: operator.eq, ast.NotEq: operator.ne,
        ast.Lt: operator.lt, ast.LtE: operator.le,
        ast.Gt: operator.gt, ast.GtE: operator.ge,
        ast.Is: operator.is_, ast.IsNot: operator.is_not,
        ast.In: lambda a, b: operator.contains(b, a),
        ast.NotIn: lambda a, b: not operator.contains(b, a),
        ast.Not: operator.not_, ast.USub: operator.neg, ast.UAdd: operator.pos,
        ast.Invert: operator.invert,
        ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b
    }

    # Common aliases to ignore in variable lookups
    SYSTEM_WHITELIST: Final[Set[str]] = {
        'True', 'False', 'None', 'range', 'len', 'int', 'str', 'float', 'bool',
        'list', 'dict', 'set', 'enumerate', 'zip', 'any', 'all', 'max', 'min',
        'sum', 'abs', 'round', 'math', 'os', 'path', 'time', 'json'
    }