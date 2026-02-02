# Path: scaffold/artisans/services/clerk/domains/organizations.py
# ----------------------------------------------------------------

from .base import BaseClerkDomain
from .....interfaces.base import ScaffoldResult


class OrganizationsDomain(BaseClerkDomain):
    """
    =============================================================================
    == THE CITADEL BUILDER (V-Ω-B2B-ORCHESTRATION)                            ==
    =============================================================================
    Manages the multi-user structures (Organizations) for enterprise sovereignty.
    """

    def execute(self, request) -> ScaffoldResult:
        action = request.action.lower()
        if action == "create_org": return self._create(request)
        if action == "add_member": return self._add_member(request)
        if action == "get_org": return self._get(request)

        return self.engine.failure(f"Unknown Organization Rite: {action}")

    def _create(self, req) -> ScaffoldResult:
        """Forges a new organizational citadel."""
        payload = {
            "name": req.legal_name,
            "public_metadata": req.public_metadata or {},
            "created_by": req.user_id  # The founder
        }
        res = self.client.request("POST", "/organizations", data=payload)
        return self.engine.success(f"Citadel '{req.legal_name}' forged.", data=res)

    def _add_member(self, req) -> ScaffoldResult:
        """Binds a user soul to an organization."""
        payload = {"user_id": req.user_id, "role": req.role}
        res = self.client.request("POST", f"/organizations/{req.org_id}/memberships", data=payload)
        return self.engine.success(f"User {req.user_id} joined Citadel {req.org_id}.")

    def _get(self, req) -> ScaffoldResult:
        res = self.client.request("GET", f"/organizations/{req.org_id}")
        return self.engine.success("Citadel perceived.", data=res)