# Path: core/lsp/scaffold_features/semantic_tokens/legend.py
# ------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_SEMANTIC_LEGEND_TOTALITY_V100
# SYSTEM: SPECTRAL_SCRIPTORIUM | ROLE: THEMATIC_MAPPING

from enum import IntEnum, IntFlag
from typing import List, Dict, Any
from pydantic import Field, ConfigDict
from ...base.types.base import LspModel


# =================================================================================
# == I. THE SPECTRAL TYPES (WHAT THE ATOM IS)                                    ==
# =================================================================================

class TokenType(IntEnum):
    """
    [THE IDENTITY MATRIX]
    Maps semantic categories to integer indices for the LSP stream.
    """
    NAMESPACE = 0
    TYPE = 1
    CLASS = 2
    ENUM = 3
    INTERFACE = 4
    STRUCT = 5
    TYPE_PARAMETER = 6
    PARAMETER = 7
    VARIABLE = 8
    PROPERTY = 9
    ENUM_MEMBER = 10
    EVENT = 11
    FUNCTION = 12
    METHOD = 13
    MACRO = 14
    KEYWORD = 15
    MODIFIER = 16
    COMMENT = 17
    STRING = 18
    NUMBER = 19
    REGEXP = 20
    OPERATOR = 21
    DECORATOR = 22  # @directives

    # --- GNOSTIC EXTENSIONS ---
    SIGIL = 23  # $$ :: << ->
    EDICT = 24  # >> ?? !! %%
    SANCTUM = 25  # Directories/Paths
    SOUL = 26  # Inline content within ::


# =================================================================================
# == II. THE SPECTRAL MODIFIERS (WHAT THE ATOM IS DOING)                         ==
# =================================================================================

class TokenModifier(IntFlag):
    """
    [THE STATE MATRIX]
    Bit-flags representing the ontological status of a token.
    """
    NONE = 0
    DECLARATION = 1 << 0
    DEFINITION = 1 << 1
    READONLY = 1 << 2
    STATIC = 1 << 3
    DEPRECATED = 1 << 4
    ABSTRACT = 1 << 5
    ASYNC = 1 << 6
    MODIFICATION = 1 << 7
    DOCUMENTATION = 1 << 8
    DEFAULT_LIBRARY = 1 << 9  # Built-ins like now() or env()


# =================================================================================
# == III. THE LEGEND VESSEL (THE ROSSETTA STONE)                                 ==
# =================================================================================

class TokenLegend(LspModel):
    """
    [THE LEGEND]
    The definitive map transmitted to the Client during the Handshake.
    It tells the Eye how to interpret the stream of integers.
    """
    model_config = ConfigDict(populate_by_name=True)

    token_types: List[str] = Field(
        ...,
        alias="tokenTypes",
        description="The list of token types the server may emit."
    )

    token_modifiers: List[str] = Field(
        ...,
        alias="tokenModifiers",
        description="The list of token modifiers the server may emit."
    )


# =================================================================================
# == IV. THE CONSECRATION FACTORY                                                ==
# =================================================================================

def get_default_legend() -> TokenLegend:
    """
    [RITE]: GET_DEFAULT_LEGEND
    Materializes the standard Gnostic Legend for the Singularity.
    """
    # [ASCENSION 8]: Automatic Index Generation
    # We strip the Enums to produce the ordered string list required by LSP.
    types = [t.name.lower() for t in TokenType]

    # For modifiers, we iterate the flags in bit-order
    modifiers = [
        "declaration", "definition", "readonly", "static",
        "deprecated", "abstract", "async", "modification",
        "documentation", "defaultLibrary"
    ]

    return TokenLegend(
        tokenTypes=types,
        tokenModifiers=modifiers
    )

# === SCRIPTURE SEALED: THE LEGEND IS IMMUTABLE ===