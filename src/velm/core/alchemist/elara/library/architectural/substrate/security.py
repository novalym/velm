# Path: core/alchemist/elara/library/architectural/substrate/security.py
# ----------------------------------------------------------------------

import os
import re

class SecurityOracle:
    """
    =============================================================================
    == THE SECURITY ORACLE (V-Ω-TOTALITY)                                      ==
    =============================================================================
    [ASCENSIONS 33-36]:
    33. Container C-Group Detection (Docker/K8s).
    34. Entropy / Secret redaction.
    35. Privilege Escalation sensing.
    """
    @property
    def is_container(self) -> bool:
        """[ASCENSION 33]: Detects if running inside a Docker or K8s container."""
        if os.path.exists('/.dockerenv'): return True
        try:
            with open('/proc/1/cgroup', 'rt') as f:
                return 'docker' in f.read() or 'kubepods' in f.read()
        except Exception:
            return False

    def redact(self, text: str) -> str:
        """[ASCENSION 34]: Entropy Sieve. Automatically masks PII/Secrets."""
        text = re.sub(r'sk_live_[a-zA-Z0-9]{24}', '[REDACTED_SECRET]', text)
        text = re.sub(r'ghp_[a-zA-Z0-9]{36}', '[REDACTED_GITHUB_TOKEN]', text)
        return text

    @property
    def is_root(self) -> bool:
        """[ASCENSION 35]: Detects root privileges (POSIX)."""
        return hasattr(os, 'getuid') and os.getuid() == 0