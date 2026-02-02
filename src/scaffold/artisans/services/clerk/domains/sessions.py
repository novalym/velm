# Path: scaffold/artisans/services/clerk/domains/sessions.py
# ------------------------------------------------------------

from .base import BaseClerkDomain
from .....interfaces.base import ScaffoldResult


class SessionsDomain(BaseClerkDomain):
    """
    =============================================================================
    == THE VIGILANT WATCHMAN (V-Ω-SESSION-SCRYING)                            ==
    =============================================================================
    Monitors and governs the active connections of users to the Monolith.
    """

    def execute(self, request) -> ScaffoldResult:
        action = request.action.lower()
        if action == "get_sessions": return self._list(request)
        if action == "kick_session": return self._revoke(request)

        return self.engine.failure(f"Unknown Session Rite: {action}")

    def _list(self, req) -> ScaffoldResult:
        """Scries for all active connections for a specific user."""
        res = self.client.request("GET", "/sessions", params={"user_id": req.user_id, "status": "active"})
        return self.engine.success(f"Vigil complete: {len(res)} sessions manifest.", data=res)

    def _revoke(self, req) -> ScaffoldResult:
        """Irrevocably severs a connection."""
        res = self.client.request("POST", f"/sessions/{req.session_id}/revoke")
        return self.engine.success(f"Connection {req.session_id} severed.")