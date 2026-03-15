# Path: core/alchemist/elara/resolver/inheritance/scryer.py
# -----------------------------------------------------------

import re
from typing import Optional, Any, TYPE_CHECKING
from ...contracts.atoms import ASTNode, TokenType

if TYPE_CHECKING:
    from .engine import InheritanceOracle


class AncestryScryer:
    """
    =============================================================================
    == THE ANCESTRY SCRYER (V-Ω-TOTALITY)                                      ==
    =============================================================================
    LIF: 50,000x | ROLE: LINEAGE_LOCATOR
    Surgically identifies the 'extends' anchor and summons the parent scripture.
    """

    @classmethod
    def find_parent_path(cls, node: ASTNode) -> Optional[str]:
        """[ASCENSION 1]: High-speed directive scryer."""
        for child in node.children:
            if child.token.type == TokenType.LOGIC_BLOCK:
                if child.metadata.get("gate") == "extends":
                    # Extract path from: {% extends "path/to/parent" %}
                    return child.token.content.replace("extends", "").strip().strip('"\'')
        return None

    @classmethod
    def summon_parent_scripture(cls, path_str: str, scope: Any) -> str:
        """[ASCENSION 13]: Physical Iron Inhalation."""
        iron = scope.get("iron")
        if not iron:
            raise ValueError("Substrate Fracture: Iron Proxy unmanifested.")

        scripture = iron.read(path_str)
        if not scripture:
            raise ValueError(f"Inheritance Fracture: Ancestor '{path_str}' is unmanifest.")

        return scripture