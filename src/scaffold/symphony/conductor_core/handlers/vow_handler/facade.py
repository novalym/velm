# Path: scaffold/symphony/conductor_core/handlers/vow_handler/facade.py
# -----------------------------------------------------------------------

from typing import Any

# --- THE DIVINE SUMMONS OF THE ONE TRUE JUDGE ---
from ..base import BaseHandler
from .....contracts.symphony_contracts import Edict, EventType
from .....core.jurisprudence.adjudicator import VowAdjudicator
from .....core.jurisprudence.contracts import AdjudicationContext


class VowHandler(BaseHandler):
    """
    =================================================================================
    == THE GNOSTIC CONDUIT OF JUDGMENT (V-Ω-UNIFIED-MIND)                          ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The pure Conduit for all Vow Edicts. It forges the complete, living Gnostic
    Context of the Symphony and bestows it upon the one true High Adjudicator from
    the jurisprudence core.
    """

    def execute(self, edict: Edict):
        """
        The Grand Rite of Adjudication.
        """
        self.logger.verbose(f"Vow Handler awakened for: '{edict.raw_scripture.strip()}'")

        # 1. --- THE GNOSTIC CONTEXT FORGE ---
        # We forge a pure, complete AdjudicationContext with the living state
        # of the Symphony, including the critical `cwd`.
        adj_context = AdjudicationContext(
            project_root=self.context_manager.project_root,
            cwd=self.context_manager.cwd,
            variables=self.context_manager.variables,
            last_process_result=self.context_manager.last_process_result,
            generated_manifest=self.context_manager.get('generated_manifest', [])
        )

        # 2. --- THE SUMMONS OF THE HIGH ADJUDICATOR ---
        # The one true judge is summoned and consecrated with the living context.
        adjudicator = VowAdjudicator(context=adj_context)

        # 3. --- THE DIVINE PLEA ---
        # The High Adjudicator performs the rite. It will raise ArtisanHeresy on failure,
        # which is the correct behavior to be caught by the SymphonyEngine's rite_boundary.
        adjudicator.adjudicate(
            vow_string=edict.raw_scripture,
            line_num=edict.line_num
        )

        # 4. --- THE PROCLAMATION OF PURITY ---
        # If no heresy was raised, the vow is pure.
        self.engine._proclaim_event(
            EventType.VOW_RESULT,
            {
                "edict": edict,
                "is_pure": True,
                "reason": "Vow Upheld"  # The adjudicator provides details in verbose logs
            }
        )