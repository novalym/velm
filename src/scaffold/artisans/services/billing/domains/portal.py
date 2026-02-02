import stripe
from typing import Any, Dict


class PortalGateway:
    """[THE SELF-SERVE GATEWAY] Generates magic links for customer management."""

    def execute(self, action: str, payload: Dict) -> Any:
        if action == "create":
            # Payload: {'customer': 'cus_...', 'return_url': '...'}
            return stripe.billing_portal.Session.create(**payload)

        raise ValueError(f"Unknown Portal Action: {action}")