# Path: core/lsp/features/semantic_tokens/legend.py
# -------------------------------------------------

from enum import IntEnum
from typing import List, Dict
from pydantic import BaseModel

class TokenType(IntEnum):
    """Canonical LSP Token Types."""
    NAMESPACE = 0; TYPE = 1; CLASS = 2; ENUM = 3; INTERFACE = 4; STRUCT = 5;
    TYPEPARAMETER = 6; PARAMETER = 7; VARIABLE = 8; PROPERTY = 9; ENUMMEMBER = 10;
    EVENT = 11; FUNCTION = 12; METHOD = 13; MACRO = 14; KEYWORD = 15; MODIFIER = 16;
    COMMENT = 17; STRING = 18; NUMBER = 19; REGEXP = 20; OPERATOR = 21; DECORATOR = 22

class TokenModifier(IntEnum):
    """Canonical LSP Token Modifiers (Bitflags)."""
    DECLARATION = 0b1
    DEFINITION = 0b10
    READONLY = 0b100
    STATIC = 0b1000
    DEPRECATED = 0b10000
    ABSTRACT = 0b100000
    ASYNC = 0b1000000
    MODIFICATION = 0b10000000
    DOCUMENTATION = 0b100000000
    DEFAULT_LIBRARY = 0b1000000000

class TokenLegend(BaseModel):
    """The map that tells Monaco how to interpret our integers."""
    token_types: List[str]
    token_modifiers: List[str]

def get_default_legend() -> TokenLegend:
    return TokenLegend(
        token_types=[t.name.lower() for t in TokenType],
        token_modifiers=[m.name.lower() for m in TokenModifier]
    )