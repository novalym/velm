# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/inclusion.py
# ----------------------------------------------------------------------------

import re
from typing import List, TYPE_CHECKING
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ....pipeline import FilterPipeline
from ........logger import Scribe

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("InclusionHandlers")


class InclusionHandlers:
    """Handles dynamic include and extends logic."""

    @staticmethod
    def handle_include(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        """[GAP 7 & 12]: Dynamic Include with Arrays and Ignore Missing."""
        expression = node.metadata.get("expression", "")
        ignore_missing = "ignore missing" in expression.lower()
        if ignore_missing:
            expression = re.sub(r'(?i)\bignore\s+missing\b', '', expression).strip()

        try:
            evaluated_path = FilterPipeline.execute(expression, scope)
            paths_to_try = evaluated_path if isinstance(evaluated_path, list) else [evaluated_path]

            included_matter = ""
            for p in paths_to_try:
                try:
                    included_matter = resolver.inclusion.conduct_include(str(p), scope, ignore_missing=False)
                    break
                except FileNotFoundError:
                    continue

            if not included_matter and not ignore_missing:
                raise FileNotFoundError(f"None of the include paths resolved: {paths_to_try}")

            output.append(GnosticToken(
                type=TokenType.LITERAL, content=included_matter, raw_text=included_matter,
                line_num=node.token.line_num, column_index=node.token.column_index,
                metadata={**node.token.metadata, "is_resolved_variable": True}
            ))
        except Exception as e:
            Logger.error(f"L{node.token.line_num}: Inclusion Fracture: {e}")

    @staticmethod
    def handle_extends(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        """[GAP 13]: Dynamic Extends Trap. Resolved by InheritanceOracle prior to walk."""
        pass