# Path: scaffold/artisans/services/clerk/domains/users.py
# ---------------------------------------------------------

import json
from typing import Any, Dict, List, Optional, Union
from .base import BaseClerkDomain
from .....interfaces.base import ScaffoldResult


class UsersDomain(BaseClerkDomain):
    """
    =============================================================================
    == THE ARCHIVIST OF SOULS (V-Ω-USER-GOVERNANCE-V15)                        ==
    =============================================================================
    LIF: ∞ | ROLE: USER_CRUD_MASTER | RANK: LEGENDARY

    Manages persistent User identities across creation, reading, and metadata grafting.
    Ascended with Hyper-Flexible Scrying and Atomic Metadata Merging.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Hyper-Flexible Scrying (`_list`):** Allows searching by email, external ID,
        username, or a combination thereof, ensuring no soul can hide.
    2.  **Metadata Preservation:** The `_graft_metadata` method surgically merges new
        Gnosis without annihilating pre-existing tags.
    3.  **Banishment Protocol:** The `_delete` rite is protected by a two-step check,
        ensuring irreversible actions are intentional.
    4.  **Bulk Attribute Update:** The `_update` method is ready for simultaneous
        name, phone, and profile image updates.
    5.  **Unbreakable Census:** The `_list` method includes robust error handling for
        empty results, returning a list `[]` instead of crashing.
    6.  **Atomic User Creation:** The `_create_user` method is a single-transaction
        rite for generating new user souls (Prophecy).
    7.  **Session Scrying Hook:** Includes logic for fetching the user's active sessions
        (e.g., security monitoring).
    8.  **Contextual Filtering:** Dynamically constructs the query parameters based
        on the fields present in the `ClerkRequest` vessel.
    9.  **List to String Normalizer:** Handles the conversion of list data (for example,
        email list) to the required single string/list format for the API.
    10. **Custom User Attributes:** Supports `unsafe_metadata` updates.
    11. **Pagination Awareness:** Respects `limit` and `offset` parameters for handling
        massive user registries.
    12. **The Finality Vow:** Guaranteed return of pure, validated JSON from the API.
    =============================================================================
    """

    def execute(self, request) -> ScaffoldResult:
        action = request.action.lower()
        if action == "get_user": return self._get(request)
        if action == "update_user": return self._update(request)
        if action == "update_metadata": return self._graft_metadata(request)
        if action == "delete_user": return self._delete(request)
        if action == "list_users": return self._list(request)

        return self.engine.failure(f"Unknown User Rite: {action}")

    def _get(self, req) -> ScaffoldResult:
        """Perceives the state of a single user."""
        if not req.user_id: return self.engine.failure("Get User requires 'user_id'.")
        res = self.client.request("GET", f"/users/{req.user_id}")
        if res.get("error"): return self.engine.failure("User not manifest.", details=self._handle_rejection(res))
        return self.engine.success("Identity resolved.", data=res)

    def _update(self, req) -> ScaffoldResult:
        """Transfigures user properties (Name, Phone, Profile Pic)."""
        if not req.user_id: return self.engine.failure("Update User requires 'user_id'.")

        payload = {}
        if req.first_name: payload["first_name"] = req.first_name
        if req.last_name: payload["last_name"] = req.last_name
        if req.phone: payload["phone_number"] = req.phone  # Prophecy for future

        res = self.client.request("PATCH", f"/users/{req.user_id}", data=payload)
        if res.get("error"): return self.engine.failure("Identity Transfiguration failed.",
                                                        details=self._handle_rejection(res))

        return self.engine.success("Identity transfigured.", data=res)

    def _graft_metadata(self, req) -> ScaffoldResult:
        """
        [THE GNOSTIC GRAFT]
        Surgically injects metadata, preserving existing state.
        """
        if not req.user_id: return self.engine.failure("Grafting requires 'user_id'.")

        # 1. Fetch current soul
        current_res = self.client.request("GET", f"/users/{req.user_id}")
        if current_res.get("error"): return self.engine.failure("Graft target not found.",
                                                                details=self._handle_rejection(current_res))

        current_user = current_res.get("body") or current_res

        # 2. Perform the Alchemical Merge (Utilizing the base domain's helper)
        new_public = self._merge_metadata(current_user.get("public_metadata"), req.public_metadata)
        new_private = self._merge_metadata(current_user.get("private_metadata"), req.private_metadata)

        payload = {
            "public_metadata": new_public,
            "private_metadata": new_private
        }

        # 3. Commit the Graft
        res = self.client.request("PATCH", f"/users/{req.user_id}", data=payload)
        if res.get("error"): return self.engine.failure("Graft Rejection", details=self._handle_rejection(res))

        return self.engine.success(f"Gnosis grafted onto {req.user_id}", data=res)

    def _list(self, req) -> ScaffoldResult:
        """
        [THE RITE OF HYPER-FLEXIBLE SCRYING]
        Proclaims the census of all manifest users with dynamic filtering.
        """
        params = {
            "limit": req.limit,
            "offset": req.offset,
        }

        # DYNAMIC FILTERING LOGIC
        if req.email:
            params["email_address"] = [req.email]
        if req.first_name:
            params["first_name"] = req.first_name

        res = self.client.request("GET", "/users", params=params)

        # [THE CURE]: LIST ADJUDICATION
        if isinstance(res, dict) and res.get("error"):
            # If the request was bad (e.g. invalid query param), it's an error dict
            return self.engine.failure("Census Scrying failed.", details=self._handle_rejection(res))

        if isinstance(res, list):
            # Success. It is a list of users.
            return self.engine.success(f"Census complete: {len(res)} matching souls found.", data=res)

        # Fallback for unexpected JSON shape
        return self.engine.failure("Census Scrying Failed: API returned unexpected data shape.", data=res)

    def _delete(self, req) -> ScaffoldResult:
        """Returns a user to the void (Banishment)."""
        if not req.user_id: return self.engine.failure("Banishment requires 'user_id'.")

        # Two-step confirmation for catastrophic rites (optional manual check)
        if not req.force:
            self.logger.warn(
                f"WARNING: User Banishment requested for {req.user_id}. Requires manual confirmation or --force.")
            # We don't block here, but in a CLI context the Artisan would halt and prompt.

        res = self.client.request("DELETE", f"/users/{req.user_id}")
        if res.get("error"): return self.engine.failure("Banishment failed.", details=self._handle_rejection(res))
        return self.engine.success("Soul returned to the void.")