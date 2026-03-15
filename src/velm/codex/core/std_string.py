# Path: src/velm/codex/core/std_string.py
# ---------------------------------------

"""
=================================================================================
== THE LINGUISTIC WEAVER (V-Ω-STRING-DOMAIN)                                   ==
=================================================================================
LIF: 100,000,000,000

The highest-impact domain for code generation. It allows the Architect to take
a raw string ("my user service") and transmute it into any required form
(PascalCase, snake_case, screaming_snake, kebab-case) safely and recursively.
=================================================================================
"""
import re
from typing import Dict, Any, List

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...utils import to_snake_case, to_pascal_case, to_kebab_case


@domain("str")
class StringDomain(BaseDirectiveDomain):
    """The Master of Lexical Form."""

    @property
    def namespace(self) -> str:
        return "str"

    def help(self) -> str:
        return "String transmutation (pascal, snake, kebab, split, replace, regex)."

    # --- 1. CASING ALCHEMY ---

    def _directive_pascal(self, context: Dict[str, Any], text: str, *args, **kwargs) -> str:
        """@str/pascal("my user service") -> MyUserService"""
        return to_pascal_case(str(text))

    def _directive_snake(self, context: Dict[str, Any], text: str, *args, **kwargs) -> str:
        """@str/snake("MyUserService") -> my_user_service"""
        return to_snake_case(str(text))

    def _directive_kebab(self, context: Dict[str, Any], text: str, *args, **kwargs) -> str:
        """@str/kebab("MyUserService") -> my-user-service"""
        return to_kebab_case(str(text))

    def _directive_screaming(self, context: Dict[str, Any], text: str, *args, **kwargs) -> str:
        """@str/screaming("my user service") -> MY_USER_SERVICE"""
        return to_snake_case(str(text)).upper()

    def _directive_pluralize(self, context: Dict[str, Any], text: str, *args, **kwargs) -> str:
        """@str/pluralize("user") -> "users" (Naive heuristic for rapid CRUD generation)"""
        t = str(text)
        if t.endswith('y') and not t.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
            return t[:-1] + 'ies'
        elif t.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return t + 'es'
        return t + 's'

    # --- 2. MANIPULATION ---

    def _directive_replace(self, context: Dict[str, Any], text: str, old: str, new: str, *args, **kwargs) -> str:
        """@str/replace(text="hello world", old="world", new="universe") -> "hello universe" """
        return str(text).replace(str(old), str(new))

    def _directive_regex_replace(self, context: Dict[str, Any], text: str, pattern: str, replacement: str, *args, **kwargs) -> str:
        """@str/regex_replace(text="v1.2.3", pattern=r"v\\d+", replacement="v2")"""
        try:
            return re.sub(str(pattern), str(replacement), str(text))
        except re.error as e:
            raise CodexHeresy(f"Profane Regex Pattern: {e}")

    def _directive_substring(self, context: Dict[str, Any], text: str, start: int = 0, end: int = None, *args, **kwargs) -> str:
        """@str/substring(text="hello", start=1, end=4) -> "ell" """
        t = str(text)
        if end is None: return t[start:]
        return t[start:end]

    def _directive_split(self, context: Dict[str, Any], text: str, delimiter: str = ",", *args, **kwargs) -> List[str]:
        """@str/split(text="a,b,c", delimiter=",") -> ["a", "b", "c"]"""
        return [s.strip() for s in str(text).split(str(delimiter))]

    def _directive_join(self, context: Dict[str, Any], items: list, delimiter: str = ", ", *args, **kwargs) -> str:
        """@str/join(items=["a", "b"], delimiter="-") -> "a-b" """
        return str(delimiter).join(str(i) for i in items)