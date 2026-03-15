# Path: src/velm/codex/core/std_iter.py
# -------------------------------------

"""
=================================================================================
== THE ITERABLE COMPOSER (V-Ω-ITER-DOMAIN)                                     ==
=================================================================================
Provides functional programming tools (flatten, unique, chunk) natively to the
Jinja context, allowing Architects to build complex loops without writing Python.
=================================================================================
"""
from typing import Dict, Any, List

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain


@domain("iter")
class IterDomain(BaseDirectiveDomain):
    """The Master of the Manifold."""

    @property
    def namespace(self) -> str:
        return "iter"

    def help(self) -> str:
        return "Functional manipulation of Lists and Arrays (unique, flatten, chunk)."

    def _directive_unique(self, context: Dict[str, Any], items: list, *args, **kwargs) -> list:
        """@iter/unique(items=[1,1,2,3]) ->[1,2,3]"""
        if not isinstance(items, list): return items
        # Preserve order while deduplicating (Python 3.7+ dict maintains insertion order)
        return list(dict.fromkeys(items))

    def _directive_flatten(self, context: Dict[str, Any], items: list, *args, **kwargs) -> list:
        """@iter/flatten(items=[[1,2], [3,4]]) ->[1,2,3,4]"""
        if not isinstance(items, list): return items

        flat_list = []
        for i in items:
            if isinstance(i, list):
                flat_list.extend(self._directive_flatten(context, i))
            else:
                flat_list.append(i)
        return flat_list

    def _directive_chunk(self, context: Dict[str, Any], items: list, size: int = 2, *args, **kwargs) -> list:
        """@iter/chunk(items=[1,2,3,4,5], size=2) -> [[1,2], [3,4],[5]]"""
        if not isinstance(items, list): return items
        if size <= 0: raise CodexHeresy("Chunk size must be greater than zero.")
        return [items[i:i + size] for i in range(0, len(items), size)]

    def _directive_keys(self, context: Dict[str, Any], dictionary: dict, *args, **kwargs) -> list:
        """@iter/keys(dictionary={"a": 1, "b": 2}) -> ["a", "b"]"""
        if not isinstance(dictionary, dict): raise CodexHeresy("Argument must be a dictionary.")
        return list(dictionary.keys())