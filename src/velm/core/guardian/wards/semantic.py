# Path: scaffold/core/guardian/wards/semantic.py
# ----------------------------------------------

import shlex
from typing import Optional, List

from ..contracts import SecurityViolation, ThreatLevel
from ..grimoire import PROFANE_COMMANDS


class SemanticWard:
    """
    =============================================================================
    == THE WARD OF MEANING (V-Ω-INTENT-ANALYZER)                               ==
    =============================================================================
    Judges the verb and its arguments for inherent danger.
    """

    def adjudicate(self, command_string: str, line_num: int) -> Optional[SecurityViolation]:
        try:
            tokens = shlex.split(command_string)
        except:
            return None  # SyntaxWard handles parse errors

        if not tokens:
            return None

        verb = tokens[0].lower()

        # 1. The Grimoire Lookup
        if verb in PROFANE_COMMANDS:
            severity = PROFANE_COMMANDS[verb]

            # Contextual leniency can go here.
            # E.g., 'rm' is Critical, but maybe 'rm *.tmp' is only Medium?
            # For now, we enforce the Grimoire's will.

            return SecurityViolation(
                ward="Semantic",
                reason=f"Profane Command: '{verb}' is restricted.",
                threat_level=severity,
                context=f"Line {line_num}"
            )

        return None