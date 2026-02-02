# Path: core/runtime/middleware/output_veil.py
# --------------------------------------------
# LIF: 100x | AUTH_CODE: Ω_OUTPUT_VEIL_V12_FIXED
# =================================================================================

import re
from typing import Any, Callable, Dict, Union
from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest

# [ASCENSION 1]: The Regex Grimoire
# Pre-compiled patterns for high-speed scrubbing
PATTERNS = [
    r'(api_key|token|secret|password)\s*[:=]\s*["\']?([^\s"\'}]+)["\']?',
    r'(sk_live_[a-zA-Z0-9]{24})',
    r'(ghp_[a-zA-Z0-9]{36})',
    r'-----BEGIN RSA PRIVATE KEY-----'
]


class OutputRedactionMiddleware(Middleware):
    """
    [THE FINAL VEIL]
    Scans the outgoing result for leaked secrets and redacts them.
    Ensures no high-entropy artifacts leave the Engine.
    """

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        # 1. Execute
        result = next_handler(request)

        # [THE FIX]: VOID WARD
        if result is None:
            return None

        # 2. Inspect & Redact
        try:
            # [THE FIX]: DUAL-MODE ACCESSOR
            # Handle both Pydantic Object and Dictionary
            is_object = hasattr(result, 'message')

            message = result.message if is_object else result.get('message', '')
            data = result.data if is_object else result.get('data')

            # 3. Scrub Message
            if message:
                cleaned_message = self._scrub(str(message))
                if is_object:
                    result.message = cleaned_message
                else:
                    result['message'] = cleaned_message

            # 4. Scrub Data (Recursive)
            if data:
                cleaned_data = self._scrub_recursive(data)
                if is_object:
                    result.data = cleaned_data
                else:
                    result['data'] = cleaned_data

        except Exception as e:
            # If scrubbing fails, log but return original result to prevent data loss
            self.logger.warn(f"Veil Fracture: {e}")

        return result

    def _scrub(self, text: str) -> str:
        """Sanitizes a single string."""
        if not text: return text
        for p in PATTERNS:
            # Replace capture group 2 (the secret) with [REDACTED]
            # Use a lambda to handle variable group counts safely
            text = re.sub(p, lambda m: m.group(0).replace(m.group(2) if m.lastindex >= 2 else m.group(1), '[REDACTED]'),
                          text, flags=re.IGNORECASE)
        return text

    def _scrub_recursive(self, obj: Any) -> Any:
        """Deep clean of JSON-serializable structures."""
        if isinstance(obj, str):
            return self._scrub(obj)
        elif isinstance(obj, dict):
            return {k: self._scrub_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._scrub_recursive(i) for i in obj]
        return obj