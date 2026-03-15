# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/validation.py
# -----------------------------------------------------------------------------

from typing import List, TYPE_CHECKING
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ...projector import MermaidAstProjector
from ...anticipator import TopologicalAnticipator
from ........contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

class ValidationHandlers:
    """Handles contracts, shards, and visualization."""

    @staticmethod
    def handle_visualize(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        title = expression.strip('"\'') or "Current Flow"
        mermaid_str = MermaidAstProjector.project(node.parent or node, title)

        output.append(GnosticToken(
            type=TokenType.LITERAL, content=f"```mermaid\n{mermaid_str}\n```", raw_text=mermaid_str,
            line_num=node.token.line_num, column_index=node.token.column_index,
            metadata={"is_resolved_variable": True}
        ))

    @staticmethod
    def handle_require(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        shard_id = node.metadata.get("expression", "").strip('"\'')
        engine_ref = resolver.engine_ref

        success = TopologicalAnticipator.fetch_dependency(shard_id, engine_ref)
        if not success and scope.global_ctx.strict_mode:
            raise ArtisanHeresy(f"Anticipation Fracture: Mandatory shard '{shard_id}' could not be fetched.",
                                severity=HeresySeverity.CRITICAL)

    @staticmethod
    def handle_contract(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        if ':' in expression:
            var_name, var_type = [x.strip() for x in expression.split(':', 1)]
            scope.register_contract(var_name, {"type": var_type, "line": node.token.line_num})