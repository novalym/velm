# Path: scaffold/artisans/services/clerk/simulation/state.py
# -----------------------------------------------------------

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


class LimboRegistry:
    """
    [THE SHADOW AKASHA]
    A persistent in-memory and on-disk registry for simulated users.
    Ensures that 'invite' -> 'get' causality is preserved in Dev.
    """

    def __init__(self, project_root: Path):
        self.cache_path = project_root / ".scaffold" / "cache" / "clerk_phantom_state.json"
        self.users: Dict[str, Dict] = {}
        self.invites: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if self.cache_path.exists():
            try:
                data = json.loads(self.cache_path.read_text())
                self.users = data.get("users", {})
                self.invites = data.get("invites", {})
            except:
                pass

    def save(self):
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "users": self.users,
                "invites": self.invites,
                "last_mutation": time.time()
            }
            self.cache_path.write_text(json.dumps(data, indent=2))
        except:
            pass

    def record_user(self, user_obj: Dict):
        self.users[user_obj["id"]] = user_obj
        self.save()

    def record_invite(self, invite_obj: Dict):
        self.invites[invite_obj["id"]] = invite_obj
        self.save()

    def find_user_by_email(self, email: str) -> Optional[Dict]:
        for user in self.users.values():
            if user["email_addresses"][0]["email_address"] == email:
                return user
        return None