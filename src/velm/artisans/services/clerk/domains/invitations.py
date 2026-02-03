# Path: scaffold/artisans/services/clerk/domains/invitations.py
# ---------------------------------------------------------------

from .base import BaseClerkDomain
from .....interfaces.base import ScaffoldResult


class InvitationsDomain(BaseClerkDomain):
    """
    =============================================================================
    == THE HERALD OF ENTRY (V-Ω-INVITATION-STRATUM)                           ==
    =============================================================================
    Manages the manifestation of new souls into the authenticated cosmos.
    """

    def execute(self, request) -> ScaffoldResult:
        action = request.action.lower()
        if action == "invite":
            return self._create_invite(request)
        elif action == "list_invites":
            return self._list_invites(request)
        elif action == "revoke_invite":
            return self._revoke_invite(request)

        return self.engine.failure(f"Unknown Invitation Rite: {action}")

    def _create_invite(self, req) -> ScaffoldResult:
        """Forges a formal invitation with embedded metadata."""
        # [ASCENSION 1]: Metadata Pre-Grafting
        # Injects the Novalym ID and Tier into the invite itself
        payload = {
            "email_address": req.email,
            "redirect_url": req.redirect_url,
            "public_metadata": req.public_metadata or {},
            "ignore_existing": True  # The Vow of Continuity
        }

        res = self.client.request("POST", "/invitations", data=payload)

        if res.get("error"):
            return self.engine.failure(
                message=f"Invitation Refused: {req.email}",
                details=self._handle_rejection(res)
            )

        return self.engine.success(
            f"Invitation dispatched to {req.email}",
            data={
                "id": res.get("id"),
                "status": res.get("status"),
                "ts": res.get("created_at")
            }
        )

    def _list_invites(self, req) -> ScaffoldResult:
        """Retrieves the census of pending souls."""
        params = {"limit": req.limit, "offset": req.offset, "status": "pending"}
        res = self.client.request("GET", "/invitations", params=params)
        return self.engine.success("Invitation census complete.", data=res)

    def _revoke_invite(self, req) -> ScaffoldResult:
        """Returns an unaccepted invitation to the void."""
        if not req.invitation_id:
            return self.engine.failure("Revocation requires invitation_id.")

        res = self.client.request("POST", f"/invitations/{req.invitation_id}/revoke")
        if res.get("error"):
            return self.engine.failure("Revocation failed.", details=self._handle_rejection(res))

        return self.engine.success(f"Invitation {req.invitation_id} revoked.")