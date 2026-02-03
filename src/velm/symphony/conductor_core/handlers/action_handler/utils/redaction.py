# Path: scaffold/symphony/conductor_core/handlers/action_handler/utils/redaction.py
# ---------------------------------------------------------------------------------
import re

class SecretRedactor:
    """
    =============================================================================
    == THE VEIL OF SECRECY (V-Ω-REGEX-SENTINEL)                                ==
    =============================================================================
    Protects the logs from the heresy of leaked credentials.
    """
    PATTERNS = [
        r'(api_key|token|secret|password|key)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?',
        r'(sk_(?:live|test)_[0-9a-zA-Z]{24})',
        r'(ghp_[0-9a-zA-Z]{36})'
    ]

    @staticmethod
    def redact(text: str) -> str:
        if not text: return ""
        redacted = text
        for pattern in SecretRedactor.PATTERNS:
            redacted = re.sub(pattern, r'\1: [REDACTED]', redacted, flags=re.IGNORECASE)
        return redacted