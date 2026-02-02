# Path: scaffold/artisans/hover/hover_mentor/inquisitor.py
# ------------------------------------------------------

import re
from typing import List, Optional, Tuple, Set


class ContextualInquisitor:
    """
    =============================================================================
    == THE CONTEXTUAL INQUISITOR (V-Ω-AURA-PERCEPTION)                         ==
    =============================================================================
    Analyzes the "Aura" surrounding a token to divine structural heresies.
    """

    def __init__(self, token: str, lines: List[str], line_idx: int):
        self.token = token
        self.lines = lines
        self.idx = line_idx
        self.current_line = lines[line_idx].strip() if line_idx < len(lines) else ""

    def analyze(self) -> List[str]:
        """Performs a multi-pass gaze upon the surrounding scripture."""
        guidance = []

        # 1. THE VOWLESS ACTION (Kinetic Best Practice)
        if self.token == ">>":
            if not self._has_vow_protection():
                guidance.append(
                    "**Mentorship:** This action is currently 'Blind'. Follow it with a `?? succeeds` vow to ensure stability.")

        # 2. THE ANCESTRAL OVERRIDE (Variable Shadowing)
        if self.token == "$$":
            var_name = self._extract_var_name()
            if var_name and self._is_shadowing(var_name):
                guidance.append(
                    f"**Gnostic Warning:** Variable `{var_name}` shadows a system-reserved variable. Consider a unique name.")

        # 3. THE DEPTH CHARGE (Complexity Management)
        indent_level = len(self.lines[self.idx]) - len(self.lines[self.idx].lstrip())
        if indent_level > 12:
            guidance.append(
                "**Architectural Note:** Deep nesting perceived. Consider refactoring this block into a `@task` or a separate blueprint.")

        # 4. THE VOID PATH (Hidden Creation)
        if self.token in ("::", "<<") and "/." in self.current_line:
            guidance.append(
                "**Prudence Alert:** You are forging a hidden file (dotfile). Ensure this is willed and not a typo.")

        return guidance

    def _has_vow_protection(self) -> bool:
        """Checks if the next non-empty line is a Vow."""
        for i in range(self.idx + 1, min(self.idx + 4, len(self.lines))):
            line = self.lines[i].strip()
            if not line: continue
            if line.startswith("??"): return True
            if line.startswith(">>"): return False  # Another action starts
        return False

    def _extract_var_name(self) -> Optional[str]:
        match = re.search(r'\$\$\s*([a-zA-Z0-9_]+)', self.current_line)
        return match.group(1) if match else None

    def _is_shadowing(self, name: str) -> bool:
        # Sacred system variables that should not be shadowed
        SYSTEM_RESERVED = {'project_root', 'scaffold_version', 'timestamp', 'author_email'}
        return name.lower() in SYSTEM_RESERVED