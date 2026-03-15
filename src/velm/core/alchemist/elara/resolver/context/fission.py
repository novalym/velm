# Path: core/alchemist/elara/resolver/context/fission.py
# ------------------------------------------------------

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import LexicalScope


class DimensionalFission:
    """
    =============================================================================
    == DIMENSIONAL FISSION (V-Ω-BICAMERAL-SPAWNER)                             ==
    =============================================================================
    LIF: 10,000x | ROLE: SCOPE_ISOLATOR
    Handles the creation of child scopes for loops and macros, ensuring
    Ouroboros safety limits are enforced.
    """

    @classmethod
    def spawn_child(cls, scope: 'LexicalScope', name: str) -> 'LexicalScope':
        """[ASCENSION 156]: BICAMERAL FISSION."""
        if scope.depth > 100:
            raise RecursionError("Topological Overflow: Lexical depth exceeded.")

        from .engine import LexicalScope
        return LexicalScope(scope.global_ctx, parent=scope, name=name, is_shadow=scope._is_shadow)