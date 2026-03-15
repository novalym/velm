# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/operator_merge.py
# ------------------------------------------------------------------------------------------

import copy
from typing import Any
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class KineticOperator:
    """
    =============================================================================
    == THE KINETIC OPERATOR (V-Ω-POLYMORPHIC-MERGE)                            ==
    =============================================================================
    LIF: 1,000,000x | ROLE: STATE_MUTATOR[ASCENSION 3 & 4]: The Absolute Transmutator for Stateful Operators.
    Handles deep-dict merging, list accumulation, and numeric summation with
    Titanium-grade type coercion and NoneType immunity.
    """

    @classmethod
    def apply(cls, var_name: str, current: Any, new_value: Any, operator: str, line_num: int) -> Any:
        """Executes the assignment operator (=, +=, |=)."""

        if operator == "=":
            return new_value

        # =========================================================================
        # == THE CURE: NONETYPE AMNESTY                                          ==
        # =========================================================================
        # If the variable is unmanifest, we pretend it is the identity element
        # of the incoming type to prevent a hard crash on the first append.
        if current is None:
            if isinstance(new_value, list) and operator == "+=":
                current = []
            elif isinstance(new_value, dict) and operator == "|=":
                current = {}
            elif isinstance(new_value, (int, float)) and operator == "+=":
                current = 0
            elif isinstance(new_value, str) and operator == "+=":
                current = ""
            elif isinstance(new_value, set) and operator in ("+=", "|="):
                current = set()
            else:
                raise ArtisanHeresy(
                    f"OPERATOR_VOID_HERESY: Cannot apply '{operator}' on unmanifest soul '{var_name}'.",
                    severity=HeresySeverity.CRITICAL, line_num=line_num
                )

        # =========================================================================
        # == MOVEMENT I: THE ADDITIVE OPERATOR (+=)                              ==
        # =========================================================================
        if operator == "+=":
            if isinstance(current, list):
                new_list = list(current)
                if isinstance(new_value, list):
                    new_list.extend(new_value)
                elif isinstance(new_value, (set, tuple)):
                    new_list.extend(list(new_value))
                else:
                    new_list.append(new_value)
                return new_list

            elif isinstance(current, str):
                return current + str(new_value)

            elif isinstance(current, (int, float)):
                try:
                    return current + type(current)(new_value)
                except (ValueError, TypeError):
                    raise ArtisanHeresy(f"MATH_HERESY: Cannot numerically add '{new_value}' to '{var_name}'.",
                                        line_num=line_num)

            elif isinstance(current, set):
                new_set = set(current)
                if isinstance(new_value, (list, set, tuple)):
                    new_set.update(new_value)
                else:
                    new_set.add(new_value)
                return new_set

            else:
                raise ArtisanHeresy(
                    f"TYPE_SCHISM_HERESY: Cannot apply '+=' between {type(current).__name__} and {type(new_value).__name__}.",
                    severity=HeresySeverity.CRITICAL, line_num=line_num)

        # =========================================================================
        # == MOVEMENT II: THE MERGE OPERATOR (|=)                                ==
        # =========================================================================
        elif operator == "|=":
            if isinstance(current, dict) and isinstance(new_value, dict):
                return cls._deep_merge(current, new_value)

            elif isinstance(current, set) and isinstance(new_value, (set, list, tuple)):
                return current.union(set(new_value))

            else:
                raise ArtisanHeresy(
                    f"TYPE_SCHISM_HERESY: Cannot apply '|=' (Deep Merge) between {type(current).__name__} and {type(new_value).__name__}. Both must be dictionaries.",
                    severity=HeresySeverity.CRITICAL, line_num=line_num)

        return new_value

    @classmethod
    def _deep_merge(cls, d1: dict, d2: dict) -> dict:
        """Recursive Dictionary Fusion."""
        res = copy.deepcopy(d1)
        for k, v in d2.items():
            if k in res and isinstance(res[k], dict) and isinstance(v, dict):
                res[k] = cls._deep_merge(res[k], v)
            else:
                res[k] = copy.deepcopy(v)
        return res