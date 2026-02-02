# Path: scaffold/core/runtime/middleware/policy.py
# ------------------------------------------------

import json
from pathlib import Path
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, RunRequest, CreateRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class PolicyMiddleware(Middleware):
    """
    =============================================================================
    == THE GRAND INQUISITOR OF COMPLIANCE (V-Ω-ENTERPRISE-GOVERNANCE)          ==
    =============================================================================
    LIF: 10,000,000,000

    Enforces strict architectural laws defined in `.scaffold-policy.json`.
    Useful for teams enforcing "No Shell Scripts" or "Python Only".
    """

    POLICY_FILE = ".scaffold-policy.json"

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        root = request.project_root or Path.cwd()
        policy_path = root / self.POLICY_FILE

        if policy_path.exists():
            try:
                policy = json.loads(policy_path.read_text(encoding='utf-8'))
                self._adjudicate_policy(request, policy)
            except json.JSONDecodeError:
                self.logger.warn("Policy file is profane (Invalid JSON). Skipping compliance check.")

        return next_handler(request)

    def _adjudicate_policy(self, request: BaseRequest, policy: dict):
        """Checks the request against the Laws."""

        # 1. Forbidden Rites (Commands)
        forbidden_rites = policy.get("forbidden_rites", [])
        request_type = type(request).__name__.replace("Request", "").lower()
        if request_type in forbidden_rites:
            raise ArtisanHeresy(
                f"Policy Violation: The '{request_type}' rite is forbidden in this sanctum.",
                severity=HeresySeverity.CRITICAL
            )

        # 2. Allowed Languages (for Run/Create)
        allowed_langs = policy.get("allowed_languages", [])
        if allowed_langs:
            target = None
            if isinstance(request, RunRequest):
                target = str(request.target)
            elif isinstance(request, CreateRequest):
                # Heuristic check on extensions
                pass

            if target:
                # Simple check: if target is a known lang key (python, node)
                if target in ['python', 'node', 'go', 'rust'] and target not in allowed_langs:
                    raise ArtisanHeresy(
                        f"Policy Violation: The '{target}' tongue is forbidden. Allowed: {allowed_langs}",
                        severity=HeresySeverity.CRITICAL
                    )