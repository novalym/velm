# Path: core/alchemist/elara/resolver/evaluator/facade.py
# -------------------------------------------------------

import ast
import hashlib
import threading
import traceback
from typing import Any, Dict, Union, TYPE_CHECKING

from .visitor import SafeEvaluator
from .heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy, SecurityHeresy, MetabolicFeverHeresy
if TYPE_CHECKING:
    from ..context import LexicalScope

class GnosticASTEvaluator:
    """
    =================================================================================
    == THE OMNISCIENT EVALUATOR (V-Ω-TOTALITY-VMAX-CACHED-RESONANCE)               ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ADJUDICATOR_OF_WILL | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_EVALUATOR_VMAX_CACHED_SUTURE_2026_FINALIS
    """

    # [ASCENSION 25]: THE GLOBAL CHRONO-REGISTRY
    _AST_CACHE: Dict[str, ast.Expression] = {}
    _CACHE_LOCK = threading.RLock()

    @classmethod
    def evaluate(
            cls,
            expression: str,
            context: Union['LexicalScope', Dict[str, Any]],
            strict_mode: bool = True
    ) -> Any:
        """
        =============================================================================
        == THE RITE OF ADJUDICATION (V-Ω-TOTALITY-VMAX-HEALED)                     ==
        =============================================================================
        [THE MASTER CURE]: The supreme terminal for logic-to-truth conversion.
        """
        expr_clean = str(expression).strip()
        if not expr_clean:
            return None

        # [ASCENSION 27]: Null-Byte Exorcism
        expr_clean = expr_clean.replace('\x00', '')

        # Contextual Synchronization
        if isinstance(context, dict):
            from ..context import ForgeContext
            forge_ctx = ForgeContext(
                variables=context,
                strict_mode=strict_mode,
                trace_id=context.get('trace_id', 'tr-facade')
            )
            scope = LexicalScope(forge_ctx)
        else:
            scope = context

        # O(1) AST Memoization
        with cls._CACHE_LOCK:
            tree = cls._AST_CACHE.get(expr_clean)

        if tree is None:
            try:
                tree = ast.parse(expr_clean, mode='eval')
                with cls._CACHE_LOCK:
                    if len(cls._AST_CACHE) > 5000:
                        cls._AST_CACHE.clear()
                    cls._AST_CACHE[expr_clean] = tree
            except (SyntaxError, ValueError, TypeError) as syntax_paradox:
                if strict_mode:
                    raise UndefinedGnosisHeresy(
                        symbol="SYNTAX_FRACTURE",
                        message=f"Syntax Heresy in ELARA Expression '{expr_clean}': {syntax_paradox}"
                    )
                raise AmnestyGrantedHeresy(alien_syntax=f"{{{{ {expr_clean} }}}}")

        # The Kinetic Strike
        try:
            visitor = SafeEvaluator(scope, strict_mode)
            return visitor.evaluate(tree)

        except (AmnestyGrantedHeresy, UndefinedGnosisHeresy, SecurityHeresy, MetabolicFeverHeresy):
            raise
        except Exception as catastrophic_fracture:
            # Fault-Isolated Redemption
            if strict_mode:
                tb_str = traceback.format_exc()
                raise UndefinedGnosisHeresy(
                    symbol="KERNEL_PANIC",
                    message=f"Logic Fracture in SGF Evaluator: {catastrophic_fracture}",
                    details=f"Internal Traceback:\n{tb_str}"
                )
            raise AmnestyGrantedHeresy(alien_syntax=f"{{{{ {expr_clean} }}}}")