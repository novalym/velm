# Path: src/velm/artisans/identity/contracts.py
# ---------------------------------------------
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class OAuthState:
    """The ephemeral state of a handshake in progress."""
    provider: str
    validation_url: str
    consumer_key: str
    timestamp: float
    status: str

@dataclass
class IdentityProfile:
    """A verified identity stored in the Gnostic Vault."""
    provider: str
    account_id: str
    region: str
    is_active: bool
    meta: Dict[str, str]