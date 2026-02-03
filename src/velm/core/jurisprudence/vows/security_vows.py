import os
import re
import stat
import math
from collections import Counter
from typing import Tuple
from .base import BaseVowHandler


class SecurityVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE GUARDIAN OF PURITY (SECURITY & ENTROPY)                             ==
    =============================================================================
    Judges files for security vulnerabilities, secrets, and permission heresies.
    """

    SECRET_PATTERNS = [
        r'sk_(live|test)_[0-9a-zA-Z]{24}',  # Stripe
        r'ghp_[0-9a-zA-Z]{36}',  # GitHub
        r'xox[baprs]-([0-9a-zA-Z]{10,48})',  # Slack
        r'-----BEGIN PRIVATE KEY-----',  # RSA/PEM
    ]

    def _calculate_entropy(self, data: str) -> float:
        """Calculates Shannon entropy."""
        if not data: return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def _vow_file_has_no_secrets(self, path: str) -> Tuple[bool, str]:
        """Asserts a file does not contain known secret patterns."""
        target = self._resolve(path)
        if not target.is_file(): return False, "Void path."

        try:
            content = target.read_text(encoding='utf-8', errors='ignore')
            for pattern in self.SECRET_PATTERNS:
                if re.search(pattern, content):
                    return False, f"Heresy: Secret pattern found in '{path}'."
            return True, f"'{path}' appears free of known secrets."
        except Exception as e:
            return False, f"Read error: {e}"

    def _vow_file_entropy_lt(self, path: str, limit: str) -> Tuple[bool, str]:
        """
        Asserts file entropy is below a threshold.
        High entropy (>6.0) often indicates secrets, binaries, or encrypted data.
        """
        target = self._resolve(path)
        if not target.is_file(): return False, "Void path."

        try:
            content = target.read_text(encoding='utf-8', errors='ignore')
            entropy = self._calculate_entropy(content)
            limit_float = float(limit)
            return entropy < limit_float, f"Entropy {entropy:.2f} < {limit_float}."
        except Exception:
            return False, "Could not calculate entropy."

    def _vow_permissions_max(self, path: str, max_octal: str) -> Tuple[bool, str]:
        """
        Asserts permissions are NOT looser than X.
        Useful for checking private keys (should be 600).
        """
        target = self._resolve(path)
        if not target.exists(): return False, "Void path."

        # Convert octal strings to int
        current_mode = target.stat().st_mode & 0o777
        max_mode = int(max_octal, 8)

        # We want to ensure current_mode has NO bits set that are not in max_mode
        # Logic: (current | max) == max
        # Example: current=600, max=644. (600 | 644) = 644. OK.
        # Example: current=644, max=600. (644 | 600) = 644 != 600. FAIL.

        is_safe = (current_mode | max_mode) == max_mode
        return is_safe, f"Mode {oct(current_mode)[-3:]} <= {max_octal}."

    def _vow_owner_is_current_user(self, path: str) -> Tuple[bool, str]:
        """Asserts the file is owned by the running user (POSIX only)."""
        if os.name == 'nt': return True, "Windows has no owners."
        target = self._resolve(path)
        if not target.exists(): return False, "Void path."

        return target.stat().st_uid == os.getuid(), "File owned by current user."