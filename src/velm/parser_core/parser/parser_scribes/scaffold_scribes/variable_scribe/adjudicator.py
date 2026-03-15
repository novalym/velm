# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/adjudicator.py
# ---------------------------------------------------------------------------------------

import re
from typing import Any, Set
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......jurisprudence_core.gnostic_type_system import GnosticTypeParser
from ......utils import to_snake_case
from ......logger import Scribe

Logger = Scribe("VariableScribe:Adjudicator")

class VariableAdjudicator:
    """
    =============================================================================
    == THE VARIABLE ADJUDICATOR (V-Ω-JURISPRUDENCE)                            ==
    =============================================================================
    ROLE: TYPE_AND_STYLE_WARDEN

    Enforces the Laws of Form (Types), Immutability (Constants), and Style.
    """

    @staticmethod
    def adjudicate_style(var_name: str, is_const: bool, parser_instance: Any, line_num: int):
        """[ASCENSION 22]: The Stylistic Mentor."""
        # Note: We bypass Heresy logging here and let the Engine handle it directly
        # to decouple the Adjudicator from the specific Parser implementation.
        pass

    @staticmethod
    def check_immutability(var_name: str, constants_set: Set[str], line_num: int):
        """[ASCENSION 6]: The Immutable Lock."""
        if var_name in constants_set:
            raise ArtisanHeresy(
                f"IMMUTABILITY_HERESY: Cannot redefine Constant '{var_name}'.",
                severity=HeresySeverity.CRITICAL,
                line_num=line_num
            )

    @staticmethod
    def enforce_type_contract(var_name: str, value: Any, type_hint: str, parser_contracts: dict, line_num: int) -> Any:
        """
        [ASCENSION 21]: Type Contract Enforcement.
        If the value is a multiline string from a shell command $(...) and the
        type hint is 'list', it autonomicly coerces the string into a list.
        """
        if isinstance(value, str) and "{{" in value:
            Logger.verbose(f"   -> Deferred type check for dynamic value '{var_name}'.")
            return value

        # [ASCENSION 2]: The Shell Array Expander
        if type_hint.strip().lower() in ('list', '[]') and isinstance(value, str):
            if '\n' in value:
                value =[x.strip() for x in value.splitlines() if x.strip()]

        try:
            gnostic_type = GnosticTypeParser.parse(type_hint)
            gnostic_type.validate(value, f"$$ {var_name}", parser_contracts)
            return value
        except ValueError as e:
            raise ArtisanHeresy(
                "CONTRACT_VIOLATION",
                details=f"Variable '{var_name}' ({value}) violates contract '{type_hint}': {e}",
                severity=HeresySeverity.CRITICAL,
                line_num=line_num
            )