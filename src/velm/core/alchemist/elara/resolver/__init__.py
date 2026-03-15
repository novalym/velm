"""
=================================================================================
== THE SGF RESOLVER STRATUM (THE MIND) (V-Ω-TOTALITY-V1)                       ==
=================================================================================
LIF: ∞^∞ | ROLE: RECURSIVE_LOGIC_EVALUATOR | RANK: OMEGA_SOVEREIGN_PRIME

This stratum is the Cognitive Core of the Sovereign Gnostic Forge.
It receives raw Tokens from the L1 Scanner, forges them into a spatial AST,
and resolves their logical truth using the Safe AST Evaluator.
=================================================================================
"""

from .engine import RecursiveResolver
from .tree_forger import SyntaxTreeForger
from .evaluator import GnosticASTEvaluator
from .context import LexicalScope
from .pipeline import FilterPipeline
from .thaw import OuroborosBreaker
from .inheritance import InheritanceOracle
__all__ = [
    "RecursiveResolver",
    "SyntaxTreeForger",
    "GnosticASTEvaluator",
    "LexicalScope",
    "FilterPipeline",
    "OuroborosBreaker",
    "InheritanceOracle",
]