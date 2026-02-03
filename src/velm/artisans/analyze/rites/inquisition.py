# Path: artisans/analyze/rites/inquisition.py
# ------------------------------------------

from typing import List, Dict, Any
from ..static_inquisitor.inquisitor import StaticInquisitor


class RiteOfInquisition:
    """
    =============================================================================
    == THE RITE OF INQUISITION (V-Ω-STATIC-ANALYSIS)                           ==
    =============================================================================
    Preserves `_rite_of_inquisition`.
    Summons the StaticInquisitor to audit the parsed AST.
    """

    @staticmethod
    def conduct(
            grammar: str,
            content: str,
            variables: Dict,
            items: List,
            edicts: List,
            dossier: Any
    ) -> List[Dict[str, Any]]:
        # The StaticInquisitor is configured by the grammar key
        inquisitor = StaticInquisitor(grammar, alchemist=None)

        return inquisitor.audit(
            content=content,
            variables=variables,
            items=items,
            edicts=edicts,
            dossier=dossier
        )