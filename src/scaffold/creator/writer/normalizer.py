# Path: scaffold/creator/writer/normalizer.py
# -------------------------------------------
import os
import re
from pathlib import Path


class ContentNormalizer:
    """
    =============================================================================
    == THE ALCHEMIST OF FORM (V-Ω-TEXT-NORMALIZER)                             ==
    =============================================================================
    Ensures consistent line endings and enforces Makefile tab discipline.
    """

    def __init__(self, is_windows: bool):
        self.is_windows = is_windows

    def sanctify(self, path: Path, content: str) -> str:
        # 1. Normalize EOL
        clean = content.replace('\r\n', '\n')

        # 2. Makefile Tab Enforcement
        if path.name.lower() == "makefile" or path.suffix.lower() == ".mk":
            clean = self._enforce_tabs(clean)

        # 3. OS Adaptation
        if self.is_windows:
            clean = clean.replace('\n', '\r\n')

        return clean

    def _enforce_tabs(self, content: str) -> str:
        lines = content.splitlines()
        out = []
        # Matches 2-8 spaces at start of line
        indent_regex = re.compile(r"^( {2,8})")

        for line in lines:
            if not line.strip():
                out.append(line)
                continue
            # If it looks like a recipe (indented), force tab
            if indent_regex.match(line):
                out.append("\t" + line.lstrip(' '))
            else:
                out.append(line)
        return "\n".join(out)