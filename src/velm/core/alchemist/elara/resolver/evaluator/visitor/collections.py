# Path: core/alchemist/elara/resolver/evaluator/visitor/collections.py
# --------------------------------------------------------------------

import ast
from typing import Any, List, Dict
from .state import VisitorState
from ..heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy


class CollectionsEvaluator:
    """
    =============================================================================
    == THE COLLECTIONS EVALUATOR (V-Ω-TOTALITY)                                ==
    =============================================================================
    Handles Arrays, Objects, Spreads, and Comprehensions.
    """

    def __init__(self, v_state: VisitorState, engine: Any):
        self.v_state = v_state
        self.engine = engine

    # --- STANDARD COLLECTIONS & SPREADS ---

    def visit_List(self, node: ast.List) -> list:
        self.v_state.check_metabolism(node)
        try:
            res = []
            for elt in node.elts:
                # [ASCENSION 12]: List Spread Operator (*args)
                if isinstance(elt, ast.Starred):
                    res.extend(self.engine.visit(elt.value))
                else:
                    res.append(self.engine.visit(elt))
            return res
        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as e:
            if self.v_state.in_default_filter: return []
            raise e

    def visit_Tuple(self, node: ast.Tuple) -> tuple:
        self.v_state.check_metabolism(node)
        try:
            res = []
            for elt in node.elts:
                if isinstance(elt, ast.Starred):
                    res.extend(self.engine.visit(elt.value))
                else:
                    res.append(self.engine.visit(elt))
            return tuple(res)
        except:
            return tuple()

    def visit_Set(self, node: ast.Set) -> set:
        self.v_state.check_metabolism(node)
        try:
            res = set()
            for elt in node.elts:
                if isinstance(elt, ast.Starred):
                    res.update(self.engine.visit(elt.value))
                else:
                    res.add(self.engine.visit(elt))
            return res
        except:
            return set()

    def visit_Dict(self, node: ast.Dict) -> dict:
        self.v_state.check_metabolism(node)
        try:
            res = {}
            for k, v in zip(node.keys, node.values):
                # [ASCENSION 11]: Dictionary Spread Operator (**kwargs)
                if k is None:  # This means it's a **kwargs spread in AST
                    spread_dict = self.engine.visit(v)
                    if isinstance(spread_dict, dict):
                        res.update(spread_dict)
                else:
                    res[self.engine.visit(k)] = self.engine.visit(v)
            return res
        except:
            return {}

    # --- HOLOGRAPHIC COMPREHENSION UNROLLING [ASCENSION 2] ---

    def _assign_target(self, target: ast.AST, value: Any, target_scope: Any):
        """[ASCENSION 6]: Deep-Tuple Unpacking for comprehensions."""
        if isinstance(target, ast.Name):
            target_scope.set_local(target.id, value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            import collections
            if not isinstance(value, (list, tuple, collections.abc.Sequence)):
                raise UndefinedGnosisHeresy(symbol="UNPACKING_FRACTURE",
                                            message=f"Iteration Heresy: Cannot unpack non-iterable.")
            for i, elt in enumerate(target.elts):
                if i < len(value): self._assign_target(elt, value[i], target_scope)

    def visit_ListComp(self, node: ast.ListComp) -> List[Any]:
        self.v_state.check_metabolism(node)
        result = []

        def _recursive_generate(gen_idx: int, current_scope: Any):
            if gen_idx >= len(node.generators):
                sub_evaluator = self.engine.__class__(current_scope, self.v_state.strict_mode)
                sub_evaluator.v_state.in_default_filter = self.v_state.in_default_filter
                result.append(sub_evaluator.visit(node.elt))
                return

            gen = node.generators[gen_idx]
            iterable_evaluator = self.engine.__class__(current_scope, self.v_state.strict_mode)
            iterable_evaluator.v_state.in_default_filter = self.v_state.in_default_filter
            iterable = iterable_evaluator.visit(gen.iter)
            if iterable is None: return

            for item in iterable:
                iteration_scope = current_scope.spawn_child(f"list_comp_l{gen_idx}")
                self._assign_target(gen.target, item, iteration_scope)

                cond_eval = self.engine.__class__(iteration_scope, self.v_state.strict_mode)
                cond_eval.v_state.in_default_filter = self.v_state.in_default_filter

                if all(cond_eval.visit(if_clause) for if_clause in gen.ifs):
                    _recursive_generate(gen_idx + 1, iteration_scope)

        _recursive_generate(0, self.v_state.scope)
        return result

    def visit_DictComp(self, node: ast.DictComp) -> Dict[Any, Any]:
        self.v_state.check_metabolism(node)
        result = {}

        def _recursive_generate(gen_idx: int, current_scope: Any):
            if gen_idx >= len(node.generators):
                sub_evaluator = self.engine.__class__(current_scope, self.v_state.strict_mode)
                sub_evaluator.v_state.in_default_filter = self.v_state.in_default_filter
                key = sub_evaluator.visit(node.key)
                val = sub_evaluator.visit(node.value)
                result[key] = val
                return

            gen = node.generators[gen_idx]
            iterable_eval = self.engine.__class__(current_scope, self.v_state.strict_mode)
            iterable_eval.v_state.in_default_filter = self.v_state.in_default_filter
            iterable = iterable_eval.visit(gen.iter)
            if iterable is None: return

            for item in iterable:
                iteration_scope = current_scope.spawn_child(f"dict_comp_l{gen_idx}")
                self._assign_target(gen.target, item, iteration_scope)
                cond_eval = self.engine.__class__(iteration_scope, self.v_state.strict_mode)
                cond_eval.v_state.in_default_filter = self.v_state.in_default_filter
                if all(cond_eval.visit(if_clause) for if_clause in gen.ifs):
                    _recursive_generate(gen_idx + 1, iteration_scope)

        _recursive_generate(0, self.v_state.scope)
        return result

    def visit_SetComp(self, node: ast.SetComp) -> set:
        return set(self.visit_ListComp(node))