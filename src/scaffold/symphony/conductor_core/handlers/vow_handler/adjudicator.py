# Path: scaffold/symphony/conductor_core/handlers/vow_handler/adjudicator.py
# --------------------------------------------------------------------------

import csv
from io import StringIO
from typing import List, Dict, Callable

from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....core.jurisprudence.adjudicator import VowAdjudicator as CoreVowAdjudicator
from .....core.jurisprudence.contracts import AdjudicationContext
from .....core.alchemist import get_alchemist
from .....logger import Scribe

Logger = Scribe("VowAdjudicator")


class VowAdjudicator:
    """
    =============================================================================
    == THE TRUE JUDGE (V-Ω-ALCHEMICAL-HEART)                                   ==
    =============================================================================
    LIF: 10,000,000,000,000,000

    This artisan is the one true engine of Vow execution. It has been ascended with
    an Alchemical Heart, allowing it to transmute Gnostic variables within vow
    arguments before passing judgment.
    """

    def __init__(self, context_manager: 'GnosticContextManager'):
        self.context_manager = context_manager
        self.alchemist = get_alchemist()

    def _parse_args(self, args_str: str) -> List[str]:
        """Parses a comma-separated string into a list, respecting quotes."""
        if not args_str: return []
        try:
            reader = csv.reader(StringIO(args_str), skipinitialspace=True)
            for row in reader:
                return row
        except Exception:
            return [a.strip() for a in args_str.split(',')]
        return []

    def _transmute_args(self, args: List[str]) -> List[str]:
        """
        [FACULTY 1] The Alchemical Heart.
        Resolves Jinja expressions within the vow's arguments.
        """
        transmuted = []
        for arg in args:
            # We check for the Jinja sigil before invoking the alchemist for performance.
            if "{{" in arg:
                transmuted.append(self.alchemist.transmute(arg, self.context_manager.variables))
            else:
                transmuted.append(arg)
        return transmuted

    def adjudicate(self, vow_string: str, line_num: int):
        """
        The Grand Rite of Judgment.
        Raises ArtisanHeresy on failure.
        """
        clean_vow = vow_string.strip().lstrip("??").strip()

        if ":" in clean_vow:
            command, args_str = clean_vow.split(":", 1)
            command = command.strip()
            raw_args = self._parse_args(args_str)
        else:
            command = clean_vow
            raw_args = []

        # === THE DIVINE HEALING ===
        # The arguments are transmuted before they are judged.
        transmuted_args = self._transmute_args(raw_args)
        # ==========================

        # === THE GNOSTIC CONTEXT FORGE ===
        # We forge a complete AdjudicationContext, now including the last process result.
        context = AdjudicationContext(
            project_root=self.context_manager.project_root,
            variables=self.context_manager.variables,
            last_process_result=self.context_manager.last_process_result
        )
        # =================================

        # We summon the Core Adjudicator from the Jurisprudence sanctum
        core_adjudicator = CoreVowAdjudicator(context)

        # The Core Adjudicator performs the rite. It raises ArtisanHeresy on its own.
        # It now receives the *transmuted* arguments.
        core_adjudicator.adjudicate(
            command=command,
            args=transmuted_args,
            line_num=line_num
        )