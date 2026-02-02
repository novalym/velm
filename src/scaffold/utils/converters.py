# ========================================================================================
# ==   SANCTUM: converters.py - The Grimoire of Pure Transmutation (V-Ω-APOTHEOSIS)     ==
# ==   PURPOSE: To serve as the sacred, foundational codex containing all pure,       ==
# ==            stateless, and unbreakable case conversion rites. This is the        ==
# ==            lowest, most stable level of the utility Gnosis.                      ==
# ========================================================================================
#
# LIF: 10,000,000,000,000,000
#
# This scripture is forged with an Unbreakable Vow of Purity. It imports nothing from
# the Scaffold ecosystem. It has no knowledge of Alchemists, Artisans, or Symphonies.
# It is a vessel of pure, mathematical truth, a timeless grimoire that could serve
# any Great Work, in any cosmos. Its Gnosis is eternal and self-contained.
#
# ========================================================================================

import re
from typing import List

# This file is intentionally pure. It imports nothing from the scaffold ecosystem.

def _split_into_words(text: str) -> List[str]:
    """
    The Sacred Heart of Deconstruction. This internal, divine rite is the one
    true source of all subsequent transmutations. It gazes upon any profane
    string (PascalCase, camelCase, snake_case, kebab-case, even HTTPRequest)
    and deconstructs it into its pure, Gnostic component words.
    """
    if not isinstance(text, str) or not text:
        return []
    # Handle acronyms gracefully (e.g., "HTTPRequest" -> "http_request")
    text_with_boundaries = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
    # Handle case changes (e.g., "myVariable" -> "my_variable")
    text_with_boundaries = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text_with_boundaries)
    # Handle delimiters
    text_with_boundaries = text_with_boundaries.replace('-', '_').replace(' ', '_')
    # Return the pure, lowercase souls
    return [word.lower() for word in text_with_boundaries.split('_') if word]

# --- Primary Transmutation Rites ---

def to_snake_case(text: str) -> str:
    """
    Transmutes a string into snake_case.
    Gnostic Plea: {{ 'MyVariableName' | snake }} -> "my_variable_name"
    """
    return '_'.join(_split_into_words(text))

def to_pascal_case(text: str) -> str:
    """
    Transmutes a string into PascalCase (also known as UpperCamelCase).
    Gnostic Plea: {{ 'my_variable_name' | pascal }} -> "MyVariableName"
    """
    return ''.join(word.capitalize() for word in _split_into_words(text))

def to_camel_case(text: str) -> str:
    """
    Transmutes a string into camelCase (also known as lowerCamelCase).
    Gnostic Plea: {{ 'my_variable_name' | camel }} -> "myVariableName"
    """
    words = _split_into_words(text)
    if not words: return ""
    return words[0] + ''.join(word.capitalize() for word in words[1:])

# --- Variant Transmutation Rites ---

def to_kebab_case(text: str) -> str:
    """
    Transmutes a string into kebab-case (also known as slug-case or dash-case).
    Gnostic Plea: {{ 'MyVariableName' | kebab }} -> "my-variable-name"
    """
    return '-'.join(_split_into_words(text))

def to_screaming_snake_case(text: str) -> str:
    """
    Transmutes a string into SCREAMING_SNAKE_CASE (also known as CONSTANT_CASE).
    Gnostic Plea: {{ 'MyVariableName' | screaming_snake }} -> "MY_VARIABLE_NAME"
    """
    return '_'.join(word.upper() for word in _split_into_words(text))

def to_dot_case(text: str) -> str:
    """
    Transmutes a string into dot.case, common for configuration keys.
    Gnostic Plea: {{ 'MyVariableName' | dot }} -> "my.variable.name"
    """
    return '.'.join(_split_into_words(text))

def to_path_case(text: str) -> str:
    """
    Transmutes a string into path/case, common for file paths or URL segments.
    Gnostic Plea: {{ 'MyVariableName' | path }} -> "my/variable/name"
    """
    return '/'.join(_split_into_words(text))

# --- Human-Readable Transmutation Rites ---

def to_sentence_case(text: str) -> str:
    """
    Transmutes a string into Sentence case, with the first word capitalized.
    Gnostic Plea: {{ 'my_variable_name' | sentence }} -> "My variable name"
    """
    words = _split_into_words(text)
    if not words: return ""
    return (words[0].capitalize() + ' ' + ' '.join(words[1:])).strip()

def to_title_case(text: str) -> str:
    """
    Transmutes a string into Title Case, with every word capitalized.
    Gnostic Plea: {{ 'my_variable_name' | title }} -> "My Variable Name"
    """
    return ' '.join(word.capitalize() for word in _split_into_words(text))

# --- Simple Transmutation Rites ---

def to_upper_case(text: str) -> str:
    """
    Transmutes an entire string to UPPER CASE, preserving existing structure.
    Gnostic Plea: {{ 'my_variable_name' | upper }} -> "MY_VARIABLE_NAME"
    """
    return str(text).upper()

def to_lower_case(text: str) -> str:
    """
    Transmutes an entire string to lower case, preserving existing structure.
    Gnostic Plea: {{ 'MyVariableName' | lower }} -> "myvariablename"
    """
    return str(text).lower()

# --- Legacy & Alias Rites for Gnostic Compatibility ---

def to_slug_case(text: str) -> str:
    """
    An alias for `to_kebab_case` for Gnostic compatibility and discoverability.
    """
    return to_kebab_case(text)