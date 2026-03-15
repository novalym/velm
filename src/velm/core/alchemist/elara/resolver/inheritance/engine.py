# Path: core/alchemist/elara/resolver/inheritance/engine.py
# -----------------------------------------------------------

import time
from typing import Any, Dict, Optional, TYPE_CHECKING

from ...contracts.atoms import ASTNode
from .scryer import AncestryScryer
from .harvester import BlockHarvester
from .grafter import TreeGrafter
from .forensics import LineageTomographer


class InheritanceOracle:
    """
    =============================================================================
    == THE INHERITANCE ORACLE: OMEGA FACADE (V-Ω-TOTALITY-VMAX)                ==
    =============================================================================
    LIF: ∞^∞ | ROLE: LINEAGE_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME

    [THE MANIFESTO]
    The monolithic era is over. The Oracle is now a hyper-intelligent facade
    orchestrating the specialized organs of the Inheritance Sanctum to achieve
    Topological Morphogenesis.
    """

    def __init__(self, engine_ref: Any):
        """[THE RITE OF INCEPTION]"""
        self.engine = engine_ref

    # =========================================================================
    # == THE STATELESS PROXY GATES                                           ==
    # =========================================================================

    def resolve_hierarchy(self, child_ast: ASTNode, scope: Any) -> ASTNode:
        """
        =========================================================================
        == THE RITE OF HIERARCHICAL CONVERGENCE                                ==
        =========================================================================
        [THE MASTER CURE]: Transmutes the relationship between Child and Parent.
        """
        start_ns = time.perf_counter_ns()

        # 1. MOVEMENT I: ANCESTRAL SCRYING
        parent_path = AncestryScryer.find_parent_path(child_ast)
        if not parent_path:
            return child_ast  # No lineage to resolve

        # 2. MOVEMENT II: ANCESTRAL SUMMONING
        parent_scripture = AncestryScryer.summon_parent_scripture(parent_path, scope)

        # 3. MOVEMENT III: ANCESTRAL FORGING
        # [RECURSIVE STRIKE]: We trigger the full pipeline to get parent AST
        from ...scanner.engine import GnosticScanner
        from ..tree_forger.engine import SyntaxTreeForger

        scanner = GnosticScanner()
        parent_tokens = scanner.scan(parent_scripture)
        parent_ast = SyntaxTreeForger.forge(parent_tokens)

        # 4. MOVEMENT IV: BLOCK HARVESTING
        child_blocks = BlockHarvester.harvest(child_ast)

        # 5. MOVEMENT V: THE SURGICAL GRAFT
        # [STRIKE]: Suture child blocks into parent topography
        final_ast = TreeGrafter.suture(parent_ast, child_blocks, scope)

        # --- METABOLIC FINALITY ---
        tax = LineageTomographer.record_tax(start_ns)
        LineageTomographer.log_lineage(
            getattr(child_ast.token, 'source_file', 'Child'),
            parent_path,
            tax
        )

        return final_ast

    def __repr__(self) -> str:
        return "<Ω_INHERITANCE_ORACLE status=RESONANT mode=MORPHOGENESIS>"