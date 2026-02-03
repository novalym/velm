from typing import Any
from supabase import Client


class AuthGuard:
    """
    [THE IDENTITY GUARD]
    Administers the GoTrue User Management layer.
    """

    def __init__(self, client: Client):
        self.auth = client.auth.admin

    def execute(self, request) -> Any:
        action = request.auth_action

        if action == "list_users":
            return self.auth.list_users()

        elif action == "get_user":
            if not request.user_id: raise ValueError("user_id required")
            return self.auth.get_user_by_id(request.user_id)

        elif action == "create_user":
            # Admin creation (bypasses email confirm if config allows)
            return self.auth.create_user({
                "email": request.email,
                "password": request.password,
                "email_confirm": True,
                "user_metadata": request.data
            })

        elif action == "delete_user":
            if not request.user_id: raise ValueError("user_id required")
            return self.auth.delete_user(request.user_id)

        elif action == "invite":
            return self.auth.invite_user_by_email(request.email)

        raise ValueError(f"Unknown Auth Action: {action}")