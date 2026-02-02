# Path: scaffold/artisans/distill/core/assembler/content/artisans/sanitizer.py

import re
from typing import List, Tuple
from .......core.cortex.contracts import DistillationProfile


class Sanitizer:
    """The artisan of purification. Redacts secrets and strips comments."""

    SECRET_DEFINITIONS: List[Tuple[str, str]] = [
        (r'(?i)(api_key|secret|token|password|credential|private_key)(\s*[:=]\s*)["\'][a-zA-Z0-9_\-.*]+["\']',
         r'\1\2"{{ SECRET_REDACTED }}"'),
        (r'sk_(live|test)_[a-zA-Z0-9]{24,}', r'"{{ SECRET_REDACTED }}"'),
        (r'ghp_[a-zA-Z0-9]{36}', r'"{{ SECRET_REDACTED }}"'),
        (r'xox[baprs]-([0-9a-zA-Z]{10,48})', r'"{{ SECRET_REDACTED }}"'),
        (r'ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*', r'"{{ JWT_REDACTED }}"')
    ]

    def clean(self, content: str, profile: DistillationProfile) -> str:
        """Performs the Rite of Sanitization."""
        clean = content

        if profile.strip_comments:
            # The Gaze is now more intelligent, preserving pragmas and tasks.
            clean = re.sub(r'(?m)^\s*#(?!\s*@|!|TODO|FIXME).*$', '', clean)
            clean = re.sub(r'(?m)^\s*//(?!\s*@|!|TODO|FIXME).*$', '', clean)
            # Collapse license headers (heuristic: block comments at start of file)
            clean = re.sub(r'^\s*/\*.*?\*/', '', clean, flags=re.DOTALL)

        if profile.redact_secrets:
            for pattern, replacement in self.SECRET_DEFINITIONS:
                # The redaction level is now honored with Gnostic clarity.
                if profile.redaction_level == 'mask':
                    clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
                else:  # 'strip'
                    clean = re.sub(pattern, '', clean, flags=re.IGNORECASE)

        return clean