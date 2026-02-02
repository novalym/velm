# Path: scaffold/core/runtime/middleware/compliance.py
# ----------------------------------------------------

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, GenesisRequest, WeaveRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("ComplianceSentinel")


class ComplianceMiddleware(Middleware):
    """
    =============================================================================
    == THE LEGAL FIREWALL (V-Ω-ENTERPRISE-GOVERNANCE)                          ==
    =============================================================================
    LIF: 10,000,000,000

    Enforces corporate law upon the creative process.
    Prevents the materialization of IP liabilities (Viral Licenses, Missing Headers).
    """

    POLICY_FILE = ".scaffold-compliance.json"
    GLOBAL_POLICY_FILE = Path.home() / ".scaffold" / "enterprise-policy.json"

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. The Gaze of Exemption (Bypass)
        # Enterprise admins can bypass checks with a specific ENV var + Flag
        if request.variables.get("skip_compliance") and os.getenv("SCAFFOLD_ADMIN_OVERRIDE"):
            Logger.warn("Compliance checks bypassed by Admin Decree.")
            return next_handler(request)

        # 2. Load the Codex of Law
        policy = self._load_policy(request.project_root)

        if not policy:
            return next_handler(request)

        # 3. The Inquisition
        self._adjudicate_licenses(request, policy)
        self._adjudicate_forbidden_patterns(request, policy)
        self._adjudicate_headers(request, policy)

        return next_handler(request)

    def _load_policy(self, project_root: Optional[Path]) -> Dict[str, Any]:
        """Merges Global and Project policies (Project is stricter)."""
        policy = {
            "forbidden_licenses": ["GPL", "AGPL", "CC-BY-SA"],
            "forbidden_patterns": ["internal_only", "confidential", "do_not_distribute"],
            "require_copyright": True,
            "copyright_holder": "Acme Corp"
        }

        # Load Global Overrides
        if self.GLOBAL_POLICY_FILE.exists():
            try:
                policy.update(json.loads(self.GLOBAL_POLICY_FILE.read_text()))
            except:
                pass

        # Load Project Overrides
        if project_root:
            local_policy = project_root / self.POLICY_FILE
            if local_policy.exists():
                try:
                    policy.update(json.loads(local_policy.read_text()))
                except:
                    pass

        return policy

    def _adjudicate_licenses(self, request: BaseRequest, policy: Dict):
        """Prevents the infection of viral licenses."""
        forbidden = set(l.lower() for l in policy.get("forbidden_licenses", []))

        # Check variables
        req_license = str(request.variables.get("license", "")).lower()

        if any(bad in req_license for bad in forbidden):
            raise ArtisanHeresy(
                f"Compliance Violation: Viral License Detected ('{request.variables.get('license')}').",
                severity=HeresySeverity.CRITICAL,
                suggestion="Select a permissive license (MIT, Apache-2.0) or request Legal exemption."
            )

    def _adjudicate_forbidden_patterns(self, request: BaseRequest, policy: Dict):
        """Scans input variables for banned terminology."""
        patterns = policy.get("forbidden_patterns", [])
        if not patterns: return

        for key, value in request.variables.items():
            val_str = str(value).lower()
            for pattern in patterns:
                if re.search(pattern, val_str, re.IGNORECASE):
                    raise ArtisanHeresy(
                        f"Compliance Violation: Forbidden terminology '{pattern}' detected in variable '{key}'.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Remove sensitive internal codenames or restricted terms from the blueprint."
                    )

    def _adjudicate_headers(self, request: BaseRequest, policy: Dict):
        """Ensures the Copyright Vow is present."""
        if not policy.get("require_copyright"): return

        # If creating a new project, we ensure the author/owner is set correctly
        if isinstance(request, (GenesisRequest, WeaveRequest)):
            holder = policy.get("copyright_holder")
            author = request.variables.get("author")

            # If policy mandates a specific holder, enforce it or ensure author matches
            if holder and (not author or holder.lower() not in author.lower()):
                Logger.warn(f"Compliance Notice: Project author '{author}' does not match corporate owner '{holder}'.")
                # We might inject it automatically here
                request.variables["copyright_holder"] = holder