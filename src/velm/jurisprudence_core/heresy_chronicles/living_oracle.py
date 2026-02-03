# Path: jurisprudence_core/heresy_chronicles/living_oracle.py
# -----------------------------------------------------------

from typing import Dict, Any

# --- THE DIVINE SUMMONS ---
# The profane summons of the Sentinel's artisans are ANNIEHILATED.
# from .structural_arbiter import StructuralArbiter
# from .heuristic_counselor import HeuristicCounselor
from ...contracts.heresy_contracts import SyntaxHeresy
from ...logger import Scribe


class LivingOracle:
    """
    =================================================================================
    == THE HUMBLE SEER OF HERESY (V-Ω-PURIFIED-SOUL)                               ==
    =================================================================================
    LIF: 100,000,000

    This is the Living Oracle in its new, purified form. Its Gaze is no longer
    profaned by attempting to replicate the deep, causal analysis of the Sentinel.
    Its one true purpose is now to perform a humble, local Gaze upon a `SyntaxHeresy`
    vessel and extract the immediate, essential Gnosis required by the `HeresyChronicler`.

    It is a pure, focused, and unbreakable artisan that honors the sacred boundary
    between Scaffold's domain-specific wisdom and the Sentinel's universal Gaze.

    ### THE PANTHEON OF 6 PURIFIED FACULTIES:
    1.  **The Unbreakable Contract:** Its `__init__` accepts the `SyntaxHeresy`.
    2.  **The Annihilation of Profane Summons:** It no longer imports or instantiates
        `StructuralArbiter` or `HeuristicCounselor`.
    3.  **The Gaze of the Ancestors (Simplified):** It performs a humble, safe traversal
        of the `node_proxy` to find the names of parent nodes, providing essential
        structural context without complex logic.
    4.  **The Gaze of the Siblings (Simplified):** It safely inspects the immediate
        siblings of the profane node for local context.
    5.  **The Luminous Dossier:** Its `divine()` rite returns a pure, simple dictionary
        of its findings.
    6.  **The Unbreakable Ward of Grace:** Its every Gaze is shielded from paradox,
        ensuring it can never shatter the `HeresyChronicler` that summons it.
    =================================================================================
    """

    def __init__(self, heresy: SyntaxHeresy):
        """
        The Rite of Inception. The Seer is born with the complete soul of the heresy.
        """
        self.heresy = heresy
        self.scribe = Scribe("LivingOracle")

    def divine(self) -> Dict[str, Any]:
        """
        The Grand Symphony of Humble Divination.
        Performs a safe, local Gaze for immediate structural context.
        """
        dossier: Dict[str, Any] = {
            "ancestors": [],
            "siblings": [],
            "counsel": "Consult the Gnostic Law proclaimed by the Sentinel."  # The new default
        }

        # The Unbreakable Ward
        node = getattr(self.heresy, 'node_proxy', None)
        if not self.heresy or not node:
            return dossier

        # --- MOVEMENT I: THE HUMBLE GAZE OF THE ANCESTORS ---
        # We perform a safe, bounded walk up the tree.
        try:
            ancestors = []
            current = node.parent
            for _ in range(10):  # A ward against infinite loops
                if not current: break
                ancestors.append(current.type)
                current = current.parent
            # The closest ancestor is last, so we reverse for a top-down view.
            dossier["ancestors"] = list(reversed(ancestors))
        except Exception as e:
            self.scribe.warn(f"The Gaze of the Ancestors was clouded by a paradox: {e}")

        # --- MOVEMENT II: THE HUMBLE GAZE OF THE SIBLINGS ---
        # We look at the immediate neighbors of the profane node.
        try:
            siblings = []
            if node.parent:
                siblings = [child.type for child in node.parent.children]
            dossier["siblings"] = siblings
        except Exception as e:
            self.scribe.warn(f"The Gaze of the Siblings was clouded by a paradox: {e}")

        # The Heuristic Counselor's Gaze is no longer performed here.
        # Its wisdom is now fully contained within the Sentinel's own proclamation.

        return dossier