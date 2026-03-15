# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/jit_thawer.py
# --------------------------------------------------------------------------------------

from typing import Any, Dict
from ......logger import Scribe
from ......core.alchemist import DivineAlchemist

Logger = Scribe("VariableScribe:JitThawer")


class JitVariableThawer:
    """
    =============================================================================
    == THE JIT THAWER (V-Ω-TOPOLOGICAL-COLLAPSE-CURE)                          ==
    =============================================================================
    LIF: ∞ | ROLE: ACHRONAL_EVALUATOR

    [THE MASTER CURE]: Instantly evaluates templates assigned to variables
    against the CURRENT parser state. This mathematically annihilates the
    Topological Collapse paradox where `package_name = {{ package_name }}`
    overwrites pre-locked identities with raw braces.
    """

    @staticmethod
    def thaw(var_name: str, raw_value: str, alchemist: DivineAlchemist, current_mind: Dict[str, Any]) -> str:
        """
        Intercepts and evaluates ELARA sigils JIT.
        """
        if "{{" not in raw_value and "{%" not in raw_value:
            return raw_value

        try:
            # [ASCENSION 26]: Strict Mode Bypassing (Amnesty)
            # We mute strict mode temporarily. If the Architect references a variable
            # that is not yet defined, we want ELARA to grant Amnesty (leave it as a string)
            # rather than crashing the entire parse pass.
            original_strict = alchemist.sgf.strict_mode
            alchemist.sgf.strict_mode = False

            # [STRIKE]: The Achronal Evaluation
            thawed_value = alchemist.transmute(raw_value, current_mind)

            alchemist.sgf.strict_mode = original_strict
            return thawed_value

        except Exception as e:
            Logger.debug(f"JIT Thaw deferred for '{var_name}' (Logic in flux): {e}")
            return raw_value