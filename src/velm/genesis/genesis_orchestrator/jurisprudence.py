# Path: scaffold/genesis/genesis_orchestrator/jurisprudence.py
# ------------------------------------------------------------

from typing import List, Dict, TYPE_CHECKING

from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...logger import Scribe
from ...jurisprudence_core.genesis_jurisprudence import GENESIS_CODEX

if TYPE_CHECKING:
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GenesisJurisprudence")


class JurisprudenceMixin:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC JURISPRUDENCE (V-Ω-LEGENDARY++. THE PURE JUDGE)   ==
    =================================================================================
    This divine artisan is a **Pure Judge**. Its one true purpose is to summon
    the sacred `GENESIS_CODEX`, walk its verses, and for each law, summon the
    `adjudicator` to gaze upon the Architect's will.

    It differs from the Type System; it judges *Wisdom*, not just *Syntax*.
    """

    def _adjudicate_gnostic_purity(self: 'GenesisDialogueOrchestrator', gnosis: Dict) -> List[Heresy]:
        """
        The Rite of Architectural Judgment.
        Scans the entire project configuration for logical contradictions or bad practices.
        """
        Logger.verbose("God-Engine of Gnostic Jurisprudence awakens to adjudicate the Architect's will...")
        heresies: List[Heresy] = []

        for law in GENESIS_CODEX:
            # The Gaze of the Void (Null-Safety Ward)
            # We only judge if the context key exists in the Gnosis (or if logic implies it)
            gnosis_value = gnosis.get(law.context_key)

            try:
                if law.validator(gnosis):
                    # Resolve dynamic message if callable
                    message = law.message(gnosis) if callable(law.message) else law.message

                    heresies.append(Heresy(
                        message=message,
                        line_num=0,  # This is a holistic, not line-specific, heresy
                        line_content=f"{law.context_key}: {gnosis_value}",
                        severity=HeresySeverity.WARNING,  # Mentorship is a warning
                        suggestion=law.suggestion
                    ))
            except Exception as e:
                Logger.warn(f"Jurisprudence Paradox on law '{law.key}': {e}")

        if heresies:
            Logger.info(f"Gnostic Inquisitor has perceived {len(heresies)} potential heresies in the Architect's will.")

        return heresies