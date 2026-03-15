# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/flow.py
# -----------------------------------------------------------------------

import re
from typing import List, TYPE_CHECKING
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from .....constants import SGFControlFlow
from ....context import LexicalScope
from ....pipeline import FilterPipeline

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver


class FlowHandlers:
    """Handles if, elif, else, for, match, and case statements."""

    @staticmethod
    def handle_if_elif(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        try:
            is_true = bool(FilterPipeline.execute(expression, scope))
        except Exception:
            is_true = False

        if is_true:
            for child in node.children:
                if child.token.type == TokenType.LOGIC_BLOCK and child.metadata.get("gate") in (SGFControlFlow.ELIF,
                                                                                                SGFControlFlow.ELSE):
                    continue
                resolver._walk(child, scope, output, spooler)
        else:
            for child in node.children:
                if child.token.type == TokenType.LOGIC_BLOCK:
                    c_gate = child.metadata.get("gate")
                    if c_gate in (SGFControlFlow.ELIF, SGFControlFlow.ELSE):
                        resolver._walk(child, scope, output, spooler)
                        break

    @staticmethod
    def handle_match(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        try:
            match_val = str(FilterPipeline.execute(expression, scope)).lower()
        except Exception:
            match_val = "void_intent"

        case_matched = False
        match_scope = scope.spawn_child(name=f"match_{match_val[:8]}")

        for child in node.children:
            if child.token.type == TokenType.LOGIC_BLOCK:
                c_gate = child.metadata.get("gate")
                if c_gate == SGFControlFlow.CASE:
                    if case_matched: continue
                    case_expr = child.metadata.get("expression", "")
                    try:
                        case_val = str(FilterPipeline.execute(case_expr, match_scope)).lower()
                        if case_val == match_val:
                            case_matched = True
                            resolver._walk(child, match_scope, output, spooler)
                    except Exception:
                        pass
                elif c_gate == SGFControlFlow.DEFAULT:
                    if not case_matched:
                        resolver._walk(child, match_scope, output, spooler)
                        case_matched = True

    @staticmethod
    def handle_for(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        match = re.match(r'^\s*([\w\s,]+)\s+in\s+(.+)$', expression)
        if not match: return

        loop_vars_str, iterable_expr = match.groups()
        loop_var_names = [v.strip() for v in loop_vars_str.split(',')]

        try:
            iterable = FilterPipeline.execute(iterable_expr.strip(), scope)
        except Exception:
            return

        if not iterable: return

        iterable_list = list(iterable) if not isinstance(iterable, list) else iterable
        length = len(iterable_list)

        for index, item in enumerate(iterable_list):
            if index > 5000: break  # Event Horizon protection

            loop_scope = scope.spawn_child(name=f"for_{index}")

            # [ASCENSION]: The Ultimate Jinja2 Loop Context
            class LoopTracker:
                def __init__(self, idx, length, data):
                    self.index = idx + 1
                    self.index0 = idx
                    self.revindex = length - idx
                    self.revindex0 = length - idx - 1
                    self.first = (idx == 0)
                    self.last = (idx == length - 1)
                    self.length = length
                    self.depth = scope.depth
                    self.depth0 = scope.depth - 1
                    self._data = data
                    self._idx = idx

                @property
                def previtem(self): return self._data[self._idx - 1] if self._idx > 0 else None

                @property
                def nextitem(self): return self._data[self._idx + 1] if self._idx < self.length - 1 else None

                def cycle(self, *args):
                    if not args: return ""
                    return args[self.index0 % len(args)]

            loop_scope.set("loop", LoopTracker(index, length, iterable_list))

            if len(loop_var_names) == 1:
                loop_scope.set(loop_var_names[0], item)
            elif len(loop_var_names) == 2 and isinstance(item, (tuple, list, dict)) and len(item) == 2:
                loop_scope.set(loop_var_names[0], item[0])
                loop_scope.set(loop_var_names[1], item[1])

            for child in node.children:
                resolver._walk(child, loop_scope, output, spooler)