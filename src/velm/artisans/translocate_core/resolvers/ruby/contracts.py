# // scaffold/artisans/translocate_core/resolvers/ruby/contracts.py
# -----------------------------------------------------------------

from dataclasses import dataclass

@dataclass
class RubyDetectedRequire:
    """
    A raw require statement perceived by the Inquisitor.
    """
    line_num: int
    path: str
    kind: str          # 'relative' (require_relative) or 'absolute' (require)
    start_byte: int    # Offset of the string content (excluding quotes)
    end_byte: int      # End offset
    quote_style: str   # ' or "

@dataclass
class RubyHealingEdict:
    """
    An instruction to transfigure a require statement.
    """
    line_num: int
    original_path: str
    new_path: str
    start_byte: int
    end_byte: int
    quote_style: str