# Path: core/alchemist/elara/scanner/scryer/amnesty.py
# ----------------------------------------------------

import re
from typing import Final
from ...constants import SGFTokens
from ..patterns.alien import AMNESTY_VETO_REGEX, GNOSTIC_PREFIX

class AmnestyAdjudicator:
    """
    =========================================================================
    == THE AMNESTY ADJUDICATOR: V8 (V-Ω-TOTALITY-VMAX)                     ==
    =========================================================================
    Performs high-fidelity semantic scrying to distinguish between
    Gnostic Intent and Foreign Matter.
    """
    RE_GNOSTIC_FORCE: Final[re.Pattern] = re.compile(rf"^{GNOSTIC_PREFIX}")
    VALID_INTENT_REGEX: Final[re.Pattern] = re.compile(
        r'^\s*[a-zA-Z_][a-zA-Z0-9_.\-\[\]{}\'"| (),\s:=*+/%<>!]*\s*$',
        re.DOTALL
    )

    @classmethod
    def adjudicate(cls, content: str, start_sigil: str) -> bool:
        if start_sigil == SGFTokens.COMMENT_START:
            return True

        clean = content.strip()
        if not clean:
            return True

        if cls.RE_GNOSTIC_FORCE.search(clean):
            return True

        if clean.startswith('{') and clean.endswith('}'):
            if "=>" in clean: return False
            return True

        if AMNESTY_VETO_REGEX.search(clean):
            return False

        if "../" in clean or "..\\" in clean:
            return False

        if not cls.VALID_INTENT_REGEX.match(clean):
            return False

        return True