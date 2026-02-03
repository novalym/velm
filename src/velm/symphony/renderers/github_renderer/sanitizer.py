# Path: scaffold/symphony/renderers/github_renderer/sanitizer.py
# --------------------------------------------------------------

import json
from typing import Any


class GnosticSanitizer:
    """
    =================================================================================
    == THE DATA PURIFIER (V-Ω-ESCAPE-LOGIC)                                        ==
    =================================================================================
    LIF: 10,000,000,000

    Ensures that values passed to GitHub Actions commands do not break the
    runner's parser. It implements the sacred escaping laws of the Runner.
    """

    @staticmethod
    def escape_data(data: Any) -> str:
        """
        Escapes values for use in ::set-output or logging.
        % -> %25
        \r -> %0D
        \n -> %0A
        """
        s = str(data)
        return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")

    @staticmethod
    def escape_property(data: Any) -> str:
        """
        Escapes values for use in command properties (e.g. file=...).
        % -> %25
        \r -> %0D
        \n -> %0A
        : -> %3A
        , -> %2C
        """
        s = GnosticSanitizer.escape_data(data)
        return s.replace(":", "%3A").replace(",", "%2C")