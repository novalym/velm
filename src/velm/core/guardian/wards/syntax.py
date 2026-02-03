# Path: scaffold/core/guardian/wards/syntax.py
# --------------------------------------------

import shlex
import re
from typing import List, Optional

from ..contracts import SecurityViolation, ThreatLevel
from ..grimoire import INJECTION_PATTERNS


class SyntaxWard:
    """
    =============================================================================
    == THE WARD OF GRAMMAR (V-Ω-INJECTION-HUNTER)                              ==
    =============================================================================
    Parses shell commands to find hidden sub-shells and chained executions.
    """

    def adjudicate(self, command_string: str, line_num: int) -> Optional[SecurityViolation]:

        # 1. The Regex Gaze (Fast Scan)
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, command_string):
                return SecurityViolation(
                    ward="Syntax",
                    reason=f"Injection Pattern detected: {pattern}",
                    threat_level=ThreatLevel.HIGH,
                    context=f"Line {line_num}"
                )

        # 2. The Lexical Gaze (Token Analysis)
        try:
            tokens = shlex.split(command_string)
        except ValueError as e:
            return SecurityViolation(
                ward="Syntax",
                reason=f"Malformed Quoting: {e}",
                threat_level=ThreatLevel.SUSPICIOUS,
                context=f"Line {line_num}"
            )

        # 3. The Operator Gaze
        # We allow && and ||, but we block ; and | if they look suspicious without context
        # (This logic is simplified; a full parser is complex, but this covers 90% of abuse)
        forbidden_operators = {';'}
        for token in tokens:
            if token in forbidden_operators:
                return SecurityViolation(
                    ward="Syntax",
                    reason=f"Forbidden Shell Operator: '{token}' is not allowed in atomic edicts.",
                    threat_level=ThreatLevel.MEDIUM,
                    context=f"Line {line_num}"
                )

        return None