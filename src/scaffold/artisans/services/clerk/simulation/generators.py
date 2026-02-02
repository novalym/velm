# Path: scaffold/artisans/services/clerk/simulation/generators.py
# ----------------------------------------------------------------

import uuid
import random
import time
from typing import Dict, Any

class SoulForger:
    """
    [THE DREAM WEAVER]
    Generates deterministic, high-fidelity hallucinations of Clerk objects.
    """

    @staticmethod
    def user_id() -> str:
        return f"user_{uuid.uuid4().hex[:24]}"

    @staticmethod
    def org_id() -> str:
        return f"org_{uuid.uuid4().hex[:24]}"

    @staticmethod
    def invite_id() -> str:
        return f"inv_{uuid.uuid4().hex[:24]}"

    @staticmethod
    def session_id() -> str:
        return f"sess_{uuid.uuid4().hex[:24]}"

    @classmethod
    def forge_user_object(cls, email: str, public_meta: Dict = None, private_meta: Dict = None) -> Dict[str, Any]:
        """Materializes a complete User soul in Limbo."""
        uid = cls.user_id()
        now = int(time.time() * 1000)
        return {
            "id": uid,
            "object": "user",
            "primary_email_address_id": f"email_{uuid.uuid4().hex[:12]}",
            "email_addresses": [{
                "id": f"email_{uuid.uuid4().hex[:12]}",
                "object": "email_address",
                "email_address": email,
                "verification": {"status": "verified", "strategy": "from_invitation"}
            }],
            "first_name": "Phantom",
            "last_name": "Architect",
            "public_metadata": public_meta or {},
            "private_metadata": private_meta or {},
            "created_at": now,
            "updated_at": now,
            "last_sign_in_at": None
        }