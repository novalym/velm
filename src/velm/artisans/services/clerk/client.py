# Path: scaffold/artisans/services/clerk/client.py
# -------------------------------------------------

import os
import httpx
from typing import Dict, Any, Optional
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .constants import BASE_URL


class ClerkClient:
    """[THE CELESTIAL PROXY] Synchronous wrapper for the Clerk API."""

    def __init__(self):
        self.api_key = os.environ.get("CLERK_SECRET_KEY")
        if not self.api_key:
            raise ArtisanHeresy("Clerk API Key is VOID in .env", severity=HeresySeverity.CRITICAL)

    def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Clerk-API-Version": "2021-02-05"  # Lock the timeline
        }

        with httpx.Client(base_url=BASE_URL, headers=headers, timeout=10.0) as client:
            res = client.request(method, endpoint, params=params, json=data)

            if res.status_code >= 400:
                return {"error": True, "status": res.status_code, "body": res.json()}

            return res.json()