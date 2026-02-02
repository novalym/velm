# Path: scaffold/core/runtime/middleware/veil.py
# ----------------------------------------------

import re
from typing import Dict, Any

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe


class SecretScrubberMiddleware(Middleware):
    """
    =============================================================================
    == THE VEIL OF SILENCE (V-Ω-DATA-LEAK-PREVENTION)                          ==
    =============================================================================
    LIF: 10,000,000,000

    Scans input variables for high-entropy strings or key-names resembling secrets.
    Moves them to the `request.secrets` vault and redacts the public record.
    """

    # The Grimoire of Secret Names
    SECRET_KEYS = {
        'api_key', 'secret', 'password', 'token', 'credential', 'private_key',
        'auth', 'jwt', 'access_key'
    }

    # The Gaze of Entropy (Regex for keys looking like secrets)
    ENTROPY_PATTERNS = [
        r'sk-[a-zA-Z0-9]{32,}',  # OpenAI / Stripe
        r'ghp_[a-zA-Z0-9]{30,}',  # GitHub
        r'xox[baprs]-([0-9a-zA-Z]{10,48})',  # Slack
    ]

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        if not request.variables:
            return next_handler(request)

        scrubbed_vars = {}
        found_secrets = 0

        for key, value in request.variables.items():
            is_secret = False
            val_str = str(value)

            # 1. Check Key Name
            if any(s in key.lower() for s in self.SECRET_KEYS):
                is_secret = True

            # 2. Check Value Entropy
            if not is_secret:
                for pattern in self.ENTROPY_PATTERNS:
                    if re.search(pattern, val_str):
                        is_secret = True
                        break

            if is_secret:
                # Move to Vault
                request.secrets[key] = val_str
                # Redact Public Record
                # [FIX] We use brackets instead of braces to prevent Jinja recursion
                scrubbed_vars[key] = "[REDACTED_BY_VEIL]"
                found_secrets += 1
            else:
                scrubbed_vars[key] = value

        if found_secrets > 0:
            request.variables = scrubbed_vars
            # We log this audit event but keep the values hidden
            self.logger.audit(f"The Veil has secured {found_secrets} secret(s) from the input stream.")

        return next_handler(request)