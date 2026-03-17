# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/flow.py
# -----------------------------------------------------------------------

import re
from typing import List, TYPE_CHECKING
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from .....constants import SGFControlFlow
from ....context import LexicalScope
from ....pipeline import FilterPipeline
from ........logger import Scribe

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("FlowHandlers")


class FlowHandlers:
    """
    =================================================================================
    == THE OMEGA FLOW HANDLERS: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS-FINALIS) ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_LOGIC_ROUTER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Bicameral Chain Tracking (THE MASTER CURE):** Tracks branch resolution
        using `parent_id`. This mathematically links `@if`, `@elif`, and `@else`
        siblings across the AST plane. Nested `if` blocks are immune to clobbering.
    2.  **Apophatic Truth Thawing (THE MASTER CURE):** Bypasses brittle python `bool()`
        casting. Natively invokes `LaminarTypeRegistry.thaw_truth`.
    =================================================================================
    """

    @staticmethod
    def handle_if_elif(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        gate = str(node.metadata.get("gate", "if")).lower()

        # [ASCENSION 1]: BICAMERAL CHAIN TRACKING
        parent_id = str(id(node.parent)) if getattr(node, 'parent', None) else "ROOT_STRATUM"
        chain_key = f"__chain_pending_{parent_id}__"

        if gate == "if":
            scope.set_local(chain_key, True)

        is_pending = scope.get(chain_key, True)

        if not is_pending:
            Logger.verbose(f"L{node.token.line_num}: Gate '@{gate}' bypassed. Sibling branch already consecrated.")
            return

        is_true = False

        if gate in ("if", "elif"):
            expression = node.metadata.get("expression", "")
            try:
                # [ASCENSION 2]: APOPHATIC TRUTH THAWING
                from ........core.alchemist.elara.resolver.evaluator import GnosticASTEvaluator
                from ........core.alchemist.elara.resolver.evaluator.void import LaminarTypeRegistry

                res = GnosticASTEvaluator.evaluate(expression, scope, strict_mode=False)
                is_true = LaminarTypeRegistry.thaw_truth(res)
            except Exception as e:
                is_true = False
        else:
            is_true = True

        if is_true:
            Logger.success(f"L{node.token.line_num}: Gate '@{gate}' unlocked. Flowing into branch reality.")

            # Seal the chain. Subsequent ELIF/ELSE siblings will be blinded.
            scope.set_local(chain_key, False)

            for child in node.children:
                resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_match(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        parent_id = str(id(node))
        match_key = f"__match_val_{parent_id}__"
        matched_key = f"__case_matched_{parent_id}__"

        try:
            from ........core.alchemist.elara.resolver.evaluator import GnosticASTEvaluator
            res = GnosticASTEvaluator.evaluate(expression, scope, strict_mode=False)
            match_val = str(res).lower()
        except Exception:
            match_val = "void_intent"

        match_scope = scope.spawn_child(name=f"match_{match_val[:8]}")
        match_scope.set_local(match_key, match_val)
        match_scope.set_local(matched_key, False)

        for child in node.children:
            resolver._walk(child, match_scope, output, spooler)

    @staticmethod
    def handle_case(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                    spooler: 'LaminarStreamSpooler'):
        parent_id = str(id(node.parent)) if getattr(node, 'parent', None) else "ROOT"
        matched_key = f"__case_matched_{parent_id}__"
        match_key = f"__match_val_{parent_id}__"

        is_matched = scope.get(matched_key, False)
        if is_matched: return

        case_expr = node.metadata.get("expression", "")
        match_val = scope.get(match_key, "void")

        try:
            from ........core.alchemist.elara.resolver.evaluator import GnosticASTEvaluator
            res = GnosticASTEvaluator.evaluate(case_expr, scope, strict_mode=False)
            case_val = str(res).lower()

            if case_val == match_val:
                scope.set_local(matched_key, True)
                for child in node.children:
                    resolver._walk(child, scope, output, spooler)
        except Exception:
            pass

    @staticmethod
    def handle_default(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        parent_id = str(id(node.parent)) if getattr(node, 'parent', None) else "ROOT"
        matched_key = f"__case_matched_{parent_id}__"

        is_matched = scope.get(matched_key, False)
        if not is_matched:
            scope.set_local(matched_key, True)
            for child in node.children:
                resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_for(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        match = re.match(r'^\s*([\w\s,]+)\s+in\s+(.+)$', expression)
        if not match: return

        loop_vars_str, iterable_expr = match.groups()
        loop_var_names = [v.strip() for v in loop_vars_str.split(',')]

        try:
            from ........core.alchemist.elara.resolver.evaluator import GnosticASTEvaluator
            iterable = GnosticASTEvaluator.evaluate(iterable_expr.strip(), scope, strict_mode=False)
        except Exception:
            return

        if not iterable: return

        iterable_list = list(iterable) if not isinstance(iterable, (list, tuple, dict)) else iterable
        if isinstance(iterable_list, dict): iterable_list = list(iterable_list.items())

        length = len(iterable_list)

        for index, item in enumerate(iterable_list):
            if index > 5000: break

            loop_scope = scope.spawn_child(name=f"for_{index}")

            class LoopTracker:
                def __init__(self, idx, length, data):
                    self.index = idx + 1
                    self.index0 = idx
                    self.revindex = length - idx
                    self.revindex0 = length - idx - 1
                    self.first = (idx == 0)
                    self.last = (idx == length - 1)
                    self.length = length
                    self._data = data
                    self._idx = idx

                @property
                def previtem(self): return self._data[self._idx - 1] if self._idx > 0 else None

                @property
                def nextitem(self): return self._data[self._idx + 1] if self._idx < self.length - 1 else None

            loop_scope.set_local("loop", LoopTracker(index, length, iterable_list))

            if len(loop_var_names) == 1:
                loop_scope.set_local(loop_var_names[0], item)
            elif len(loop_var_names) >= 2 and isinstance(item, (tuple, list)):
                for i, v_name in enumerate(loop_var_names):
                    if i < len(item):
                        loop_scope.set_local(v_name, item[i])

            for child in node.children:
                resolver._walk(child, loop_scope, output, spooler)