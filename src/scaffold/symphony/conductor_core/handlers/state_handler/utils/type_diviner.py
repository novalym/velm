# Path: scaffold/symphony/conductor_core/handlers/state_handler/utils/type_diviner.py
# -----------------------------------------------------------------------------------
import json
from typing import Any
from ......logger import Scribe

Logger = Scribe("TypeDiviner")


class TypeDiviner:
    """
    =============================================================================
    == THE TYPE DIVINER (V-Ω-STRICT-INFERENCE)                                 ==
    =============================================================================
    Transmutes raw strings into their true Gnostic forms (int, bool, dict, list).
    """

    @staticmethod
    def divine(value: str) -> Any:
        """Infers types from strings with paranoid precision."""
        if not isinstance(value, str):
            return value

        cleaned = value.strip()
        lower = cleaned.lower()

        # 1. Booleans
        if lower == 'true': return True
        if lower == 'false': return False

        # 2. Nulls
        if lower in ('null', 'none', 'nil'): return None

        # 3. Integers
        if cleaned.lstrip('-').isdigit():
            return int(cleaned)

        # 4. Floats (Simple check)
        try:
            if '.' in cleaned:
                return float(cleaned)
        except ValueError:
            pass

        # 5. Structured Data (JSON)
        # Only attempt if it looks like a structure to avoid performance hits
        if (cleaned.startswith('{') and cleaned.endswith('}')) or \
                (cleaned.startswith('[') and cleaned.endswith(']')):
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass  # It was just a string with braces

        # 6. Fallback: String
        return value