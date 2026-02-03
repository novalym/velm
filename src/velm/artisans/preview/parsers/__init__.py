# Path: scaffold/artisans/preview/parsers/__init__.py
# =================================================================================
# == THE PARSER FACTORY (V-Ω-GATEWAY)                                            ==
# =================================================================================
# LIF: 10^32 | The Central Dispatch for UI Analysis
#
# [PURPOSE]: Unifies the specialized parsers (React, HTML) into a single
#            callable factory. Handles language normalization and fallback.

from .base import BaseUIParser
from .react import ReactParser
from .html import HTMLParser

# [ASCENSION]: The Universal Language Map
# Maps file extensions and language IDs to the correct Inquisitor.
_PARSER_MAP = {
    # React / TypeScript / JavaScript
    'typescript': ReactParser,
    'typescriptreact': ReactParser,
    'javascript': ReactParser,
    'javascriptreact': ReactParser,
    'tsx': ReactParser,
    'jsx': ReactParser,
    'ts': ReactParser,
    'js': ReactParser,

    # Web Standards
    'html': HTMLParser,
    'htm': HTMLParser,

    # [PROPHECY]: Future expansion slots
    'vue': None,  # Awaiting V2
    'svelte': None  # Awaiting V2
}


def get_parser(language: str) -> BaseUIParser:
    """
    The Rite of Parser Summoning.

    Args:
        language (str): The language ID or file extension (e.g. 'tsx', 'python').

    Returns:
        BaseUIParser: An instantiated parser capable of analyzing the scripture,
                      or None if the tongue is unknown to the Ocular Core.
    """
    if not language:
        return None

    normalized_lang = language.lower().strip().lstrip('.')

    parser_class = _PARSER_MAP.get(normalized_lang)

    if parser_class:
        return parser_class()

    return None


__all__ = ["get_parser", "BaseUIParser", "ReactParser", "HTMLParser"]