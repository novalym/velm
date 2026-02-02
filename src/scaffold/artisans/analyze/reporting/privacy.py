# Path: artisans/analyze/reporting/privacy.py
# -------------------------------------------

import re
from typing import List, Tuple


class PrivacySentinel:
    """
    =============================================================================
    == THE PRIVACY SENTINEL (V-Ω-REGEX-SAFEGUARD-ULTIMA)                       ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: DATA_MASKING_ENGINE

    Scans text for high-entropy secrets and redacts them using specific rules.
    Prevents "Group Reference" fractures by mapping specific patterns to
    specific replacement strings.
    """

    # [ASCENSION 1]: THE RULE REGISTRY
    # Format: (Regex_Pattern, Replacement_String)
    # \g<1> refers to Capture Group 1.
    REDACTION_RULES: List[Tuple[str, str]] = [
        # 1. Key-Value Pairs (Keep Key, Redact Value)
        # Matches: api_key = "xyz", token: "abc"
        (
            r'(api_key|token|secret|password|auth)\s*[:=]\s*["\']?([^\s"\'}]+)["\']?',
            r'\g<1>: [REDACTED]'
        ),

        # 2. Stripe Keys (sk_live_...)
        (
            r'sk_live_[a-zA-Z0-9]{24}',
            r'[REDACTED_STRIPE_KEY]'
        ),

        # 3. GitHub Tokens (ghp_...)
        (
            r'ghp_[a-zA-Z0-9]{36}',
            r'[REDACTED_GITHUB_TOKEN]'
        ),

        # 4. RSA Private Keys (Block)
        (
            r'-----BEGIN RSA PRIVATE KEY-----[\s\S]*?-----END RSA PRIVATE KEY-----',
            r'[REDACTED_PRIVATE_KEY_BLOCK]'
        ),

        # 5. RSA Header (Fallback if block fails)
        (
            r'-----BEGIN RSA PRIVATE KEY-----',
            r'[REDACTED_KEY_HEADER]'
        ),

        # 6. AWS Access Keys (AKIA...)
        (
            r'(AKIA[0-9A-Z]{16})',
            r'[REDACTED_AWS_KEY]'
        )
    ]

    @staticmethod
    def redact(content: str) -> str:
        """
        [THE RITE OF MASKING]
        Iterates through the Rule Registry and sanitizes the input.
        Safe against 'invalid group reference' errors.
        """
        if not content:
            return ""

        sanitized = content

        for pattern, replacement in PrivacySentinel.REDACTION_RULES:
            try:
                sanitized = re.sub(
                    pattern,
                    replacement,
                    sanitized,
                    flags=re.IGNORECASE | re.MULTILINE
                )
            except Exception:
                # [SILENCE WARD]: Never let a regex error crash the pipeline.
                pass

        return sanitized