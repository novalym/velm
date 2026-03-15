# Path: core/alchemist/elara/resolver/evaluator/visitor/identity.py
# -----------------------------------------------------------------

import ast
import builtins
from typing import Any
from .state import VisitorState
from ..void import VOID, GnosticVoid
from ..constants import EvaluationConstants
from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy, SecurityHeresy
from .......logger import Scribe

Logger = Scribe("IdentityEvaluator")


class IdentityEvaluator:
    """
    =============================================================================
    == THE IDENTITY EVALUATOR (V-Ω-TOTALITY-VMAX-O(1)-SUTURE)                  ==
    =============================================================================
    LIF: ∞^∞ | ROLE: AST_IDENTITY_RESOLVER | RANK: OMEGA_SOVEREIGN

    [THE MASTER CURE]
    The era of "Difflib Freezes" is mathematically annihilated. This Evaluator
    has been stripped of all O(N) fuzzy-searching and Alphanumeric Normalization.
    It now relies EXCLUSIVELY on O(1) Hash-Map lookups and the Apophatic Void
    Registry. Missing variables resolve in nanoseconds.
    =============================================================================
    """

    def __init__(self, v_state: VisitorState, engine: Any):
        self.v_state = v_state
        self.engine = engine

    def visit_Name(self, node: ast.Name) -> Any:
        """The O(1) Core Identity Resolver."""
        self.v_state.check_metabolism(node)
        raw_id = node.id

        # 1. SYSTEM WHITELIST (O(1) Check)
        if raw_id in EvaluationConstants.SYSTEM_WHITELIST:
            val = self.v_state.scope.get(raw_id)
            if val is not None: return val
            return getattr(builtins, raw_id, None)

        # =========================================================================
        # == [THE MASTER CURE]: THE NEGATIVE ENTROPY CACHE (O(1) FAST-FAIL)      ==
        # =========================================================================
        # If we have already proven this identity is unmanifest in the timeline,
        # we instantly return VOID to prevent recursive deep-scrying.
        if not hasattr(self.v_state.scope.global_ctx, '_void_registry'):
            self.v_state.scope.global_ctx._void_registry = set()

        if raw_id in self.v_state.scope.global_ctx._void_registry:
            return None if self.v_state.in_default_filter else VOID

        # 2. O(1) LATTICE RETRIEVAL
        # Scope.get() natively traverses Local -> Parent -> Global -> Registry
        val = self.v_state.scope.get(raw_id)

        # 3. TRUTH THAWING
        if val is not None:
            if self.v_state.in_default_filter:
                if hasattr(val, '_shadow_map') and not val: return None
            if isinstance(val, str):
                v_low = val.lower().strip()
                if v_low in ("true", "yes", "resonant", "on"): return True
                if v_low in ("false", "no", "fractured", "off"): return False
            return val

        # =========================================================================
        # == [THE CURE]: VOID ENSHRINEMENT (PERMANENT O(N) ANNIHILATION)         ==
        # =========================================================================
        # The variable is a true void. We permanently enshrine it in the Negative
        # Cache for this transaction, ensuring future loops skip it instantly.
        self.v_state.scope.global_ctx._void_registry.add(raw_id)

        if self.v_state.in_default_filter:
            return None

        if self.v_state.strict_mode:
            raise UndefinedGnosisHeresy(
                symbol=raw_id,
                trace_id=self.v_state.trace_id,
                line_num=node.lineno,
                col_num=node.col_offset
            )

        # Fallback string for Amnesty Mode
        return f"{{{{ {raw_id} }}}}"

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """The O(1) Attribute Resolver."""
        self.v_state.check_metabolism(node)

        # Subversion Ward
        if node.attr.startswith('__') and not self.v_state.scope.get("_is_shadow"):
            raise SecurityHeresy(target=node.attr, line_num=node.lineno)

        # Resolve Parent Object
        try:
            obj = self.engine.visit(node.value)
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return None
            raise e

        if obj is None or isinstance(obj, GnosticVoid):
            if self.v_state.strict_mode and not self.v_state.in_default_filter:
                raise UndefinedGnosisHeresy(symbol=f"?.{node.attr}", trace_id=self.v_state.trace_id,
                                            line_num=node.lineno)
            return None

        # =========================================================================
        # == [THE CURE]: O(1) PROPERTY SCRYING                                   ==
        # =========================================================================
        res = None
        if isinstance(obj, dict):
            res = obj.get(node.attr)
        else:
            try:
                res = getattr(obj, node.attr)
            except AttributeError:
                if hasattr(obj, 'get'):
                    res = obj.get(node.attr)

        if self.v_state.in_default_filter:
            if hasattr(res, '_shadow_map') and not res: return None

        if res is not None: return res

        # If we reach here, the attribute is truly void. No fuzzy matching allowed.
        if self.v_state.strict_mode and not self.v_state.in_default_filter:
            raise UndefinedGnosisHeresy(
                symbol=f"{type(obj).__name__}.{node.attr}",
                trace_id=self.v_state.trace_id,
                line_num=node.lineno
            )

        return None

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        """The O(1) Array/Index Resolver."""
        self.v_state.check_metabolism(node)
        try:
            obj = self.engine.visit(node.value)
            slice_val = self.engine.visit(node.slice)
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return None
            raise e

        if obj is None or isinstance(obj, GnosticVoid):
            if self.v_state.strict_mode and not self.v_state.in_default_filter:
                raise UndefinedGnosisHeresy(symbol="?[_]", trace_id=self.v_state.trace_id, line_num=node.lineno)
            return None

        try:
            return obj[slice_val]
        except (KeyError, IndexError, TypeError):
            if self.v_state.strict_mode and not self.v_state.in_default_filter:
                raise UndefinedGnosisHeresy(symbol=f"_[{slice_val}]", trace_id=self.v_state.trace_id,
                                            line_num=node.lineno)
            return None

    def visit_Index(self, node: ast.Index) -> Any:
        return self.engine.visit(node.value)

    def visit_Slice(self, node: ast.Slice) -> Any:
        start = self.engine.visit(node.lower) if node.lower else None
        stop = self.engine.visit(node.upper) if node.upper else None
        step = self.engine.visit(node.step) if node.step else None
        return slice(start, stop, step)

    def visit_ExtSlice(self, node: ast.ExtSlice) -> Any:
        return tuple(self.engine.visit(dim) for dim in node.dims)