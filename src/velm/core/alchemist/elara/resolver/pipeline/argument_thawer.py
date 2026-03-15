# Path: core/alchemist/elara/resolver/pipeline/argument_thawer.py
# --------------------------------------------------------------

import ast
from typing import List, Dict, Tuple, Any

from ..context import LexicalScope
from ..evaluator import SafeEvaluator, AmnestyGrantedHeresy, UndefinedGnosisHeresy

class ArgumentThawer:
    """
    =============================================================================
    == THE ARGUMENT THAWING MATRIX (V-Ω-TOTALITY)                              ==
    =============================================================================
    LIF: ∞ | ROLE: ARGUMENT_RESOLVER | RANK: MASTER[ASCENSION 134 & 146]: A sovereign class dedicated purely to transmuting
    the raw string arguments of a filter into fully evaluated Python objects
    via the AST Virtual Call Sieve.
    """

    @classmethod
    def thaw(
        cls,
        args_body: str,
        rite_name: str,
        scope: LexicalScope,
        is_mercy: bool
    ) -> Tuple[List[Any], Dict[str, Any]]:
        """
        Transmutes `arg1, key=val` into evaluated Python objects.
        """
        if not args_body:
            return [], {}

        args =[]
        kwargs = {}

        try:
            # [ASCENSION 127]: The Virtual Call Sieve
            virtual_code = f"virtual_call({args_body})"
            tree = ast.parse(virtual_code, mode='eval')

            if isinstance(tree.body, ast.Call):
                call_node = tree.body
                visitor = SafeEvaluator(scope)

                # =====================================================================
                # ==[ASCENSION 133]: THE LAMINAR SUTURE (THE MASTER CURE)           ==
                # =====================================================================
                # We project the "Amnesty Sarcophagus" down into the argument evaluator.
                # This mathematically annihilates the Nested Default Paradox.
                if is_mercy:
                    visitor._in_default_filter = True

                args =[visitor.visit(arg) for arg in call_node.args]
                kwargs = {kw.arg: visitor.visit(kw.value) for kw in call_node.keywords if kw.arg}
            else:
                raise AmnestyGrantedHeresy(f"Structural Argument Heresy in '{rite_name}'.")

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy, Exception) as argument_fracture:
            # [ASCENSION 126]: The Cascading Default Suture
            if is_mercy:
                # We return None for the first argument to let the fallback logic ignite.
                args =[None]
                kwargs = {}
            else:
                raise AmnestyGrantedHeresy(f"Argument fracture in '{rite_name}': {argument_fracture}")

        return args, kwargs