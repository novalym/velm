# Path: scaffold/core/runtime/middleware/auth.py
# ----------------------------------------------

import os
import secrets
from typing import Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class AuthMiddleware(Middleware):
    """
    =============================================================================
    == THE GUARDIAN OF THE GATE (V-Ω-CRYPTOGRAPHIC-WARD)                       ==
    =============================================================================
    LIF: 10,000,000,000

    This middleware enforces cryptographic access control. It ensures that no
    profane entity can command the Daemon without the sacred Token.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. The Gaze of Necessity
        # If the engine is running in "Open Mode" (Local CLI without Daemon),
        # or if no master token is configured, the gate is open.
        master_token = os.getenv("SCAFFOLD_AUTH_TOKEN")
        if not master_token:
            # Warning: In a true server context, this is a risk.
            # But for local CLI, it's standard.
            return next_handler(request)

        # 2. The Extraction of the Key
        # We look for the token in the request secrets (injected by the Client/Daemon interface)
        client_token = request.secrets.get("auth_token")

        if not client_token:
            raise ArtisanHeresy(
                "Authentication Heresy: No token presented to the Gatekeeper.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Ensure your client is configured with the correct SCAFFOLD_AUTH_TOKEN."
            )

        # 3. The Constant-Time Adjudication
        # We use constant-time comparison to prevent timing attacks.
        if not secrets.compare_digest(client_token, master_token):
            raise ArtisanHeresy(
                "Authentication Heresy: The provided token is profane.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify your credentials."
            )

        # 4. The Granting of Passage
        return next_handler(request)