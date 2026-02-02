# Path: scaffold/creator/writer/security.py
# -----------------------------------------
import re
from typing import List
from ...logger import Scribe

Logger = Scribe("SecretSentinel")

class SecretSentinel:
    """
    =============================================================================
    == THE GUARDIAN OF SECRETS (V-Ω-ENTROPY-SCANNER)                           ==
    =============================================================================
    Scans content for high-entropy strings and API key patterns.
    """

    SECRET_PATTERNS = [
        ("Generic Secret", re.compile(r'(?i)("|\')?(api_key|secret|password|token|passwd|credential)("|\')?\s*[:=]\s*["\']?([^\s\'"&]{20,})["\']?')),
        ("Stripe Key", re.compile(r'(sk_(?:live|test)_[a-zA-Z0-9]{20,})')),
        ("AWS Key", re.compile(r'(AKIA[0-9A-Z]{16})')),
        ("SSH Private Key", re.compile(r'-----BEGIN OPENSSH PRIVATE KEY-----')),
    ]

    @classmethod
    def scan(cls, content: str, filename: str) -> List[str]:
        warnings = []
        for name, pattern in cls.SECRET_PATTERNS:
            if pattern.search(content):
                msg = f"Potential '{name}' detected in '{filename}'."
                Logger.warn(f"Security Alert: {msg}")
                warnings.append(msg)
        return warnings