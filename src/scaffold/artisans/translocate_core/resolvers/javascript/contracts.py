# // scaffold/artisans/translocate_core/resolvers/javascript/contracts.py
# -----------------------------------------------------------------------

from dataclasses import dataclass
from typing import Tuple

@dataclass
class JSDetectedImport:
    """
    A raw import statement perceived by the Inquisitor.
    """
    line_num: int
    quote_style: str           # ' or "
    specifier: str             # e.g., "./utils", "react", "@/components/Button"
    start_byte: int            # Precise byte offset of the specifier string
    end_byte: int              # Precise end offset
    is_dynamic: bool           # import() or require() vs static import

@dataclass
class JSHealingEdict:
    """
    An instruction to perform surgical byte-replacement on a JS file.
    """
    line_num: int
    original_specifier: str
    new_specifier: str
    start_byte: int
    end_byte: int
    quote_style: str