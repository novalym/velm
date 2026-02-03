# Path: scaffold/artisans/hover/hover_mentor/warden.py
# ---------------------------------------------------

import re
from typing import List

class SecurityWarden:
    """
    =============================================================================
    == THE SECURITY WARDEN (V-Ω-CITADEL-SENTINEL)                              ==
    =============================================================================
    The final barrier. It gazes specifically for vectors of corruption,
    secret exposure, and system instability.
    """

    def __init__(self, token: str, lines: List[str], line_idx: int):
        self.token = token
        self.lines = lines
        self.idx = line_idx
        self.current_line = lines[line_idx].strip() if line_idx < len(lines) else ""

    def judge(self) -> List[str]:
        """Adjudicates the line for high-threat heresies."""
        warnings = []

        # 1. THE EXPOSED VEIN (Raw Secrets)
        # Gaze for assignments to sensitive keys that contain literal strings instead of Jinja
        if any(k in self.current_line.lower() for k in ["key", "secret", "password", "token"]):
            if '"' in self.current_line or "'" in self.current_line:
                if "{{" not in self.current_line and "@vault" not in self.current_line:
                    warnings.append("**💀 CRITICAL SECURITY ALERT:** A plaintext secret was perceived! Banish it to the `.env` and use `${{...}}`.")

        # 2. THE INJECTION VECTOR (Unshielded Will)
        if self.token == "%%":
            # Check for variables inside shell edicts without the 'shell_escape' filter
            if "{{" in self.current_line and "shell_escape" not in self.current_line:
                warnings.append("**🚨 DANGER:** Variable injected into shell without a `| shell_escape` ward. This is an active vector for command injection.")

        # 3. THE PATH TRAVERSAL (Root Escape)
        if "../" in self.current_line or "..\\" in self.current_line:
            warnings.append("**Guardian's Warning:** Path traversal (`..`) detected. The God-Engine forbids escaping the consecrated Project Root.")

        # 4. THE RITE OF SUDO (Privilege Escalation)
        if "sudo " in self.current_line.lower():
            warnings.append("**Security Note:** `sudo` usage detected. Rites requiring escalation should be handled by the host environment, not the blueprint.")

        # 5. THE UNSTABLE TAG (Docker latest)
        if ":latest" in self.current_line and "docker" in self.current_line.lower():
            warnings.append("**Stability Warning:** Usage of the `:latest` tag is a heresy against reproducibility. Use a specific version pin.")

        return warnings