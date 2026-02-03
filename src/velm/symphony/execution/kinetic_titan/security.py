# Path: scaffold/symphony/execution/kinetic_titan/security.py
# -----------------------------------------------------------

import re


class StreamSentinel:
    """
    =============================================================================
    == THE STREAM SENTINEL (V-Ω-REALTIME-REDACTION)                            ==
    =============================================================================
    Scans the kinetic output stream for secrets before they are proclaimed.
    """

    SECRET_PATTERNS = [
        r'(api_key|token|secret|password|passwd|credential|key)\s*[:=]\s*[\'"]?([^\s\'"]+)',
        r'(sk_(?:live|test)_[0-9a-zA-Z]{24})',
        r'(ghp_[0-9a-zA-Z]{36})',
        r'(Bearer\s+)([a-zA-Z0-9\-\._~\+\/]+)',
    ]

    _COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in SECRET_PATTERNS]

    @classmethod
    def redact(cls, content: str) -> str:
        """Applies the Veil of Secrecy."""
        if not content: return ""
        for pattern in cls._COMPILED_PATTERNS:
            content = pattern.sub(r'\1: [REDACTED]', content)
        return content

    @classmethod
    def strip_ansi(cls, text: str) -> str:
        """Removes existing ANSI codes for pure log storage."""
        # Simple heuristic, usually handled by rich.AnsiDecoder but good for raw logs
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)