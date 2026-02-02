import stripe
from typing import Any, Dict, List


class RevenueEngine:
    """[THE REVENUE ENGINE] Orchestrates the flow of recurring capital."""

    def execute(self, action: str, req_id: str, payload: Dict, expand: List[str], limit: int) -> Any:
        if action == "create":
            # Payload should contain 'customer' and 'items'=[{'price': '...'}]
            return stripe.Subscription.create(**payload, expand=expand)

        elif action == "retrieve":
            return stripe.Subscription.retrieve(req_id, expand=expand)

        elif action == "update":
            # Handles upgrades, downgrades, and quantity changes
            return stripe.Subscription.modify(req_id, **payload, expand=expand)

        elif action == "cancel":
            return stripe.Subscription.cancel(req_id)

        elif action == "list":
            return stripe.Subscription.list(limit=limit, expand=expand, **payload)

        elif action == "usage":
            # Report usage for metered billing
            # Payload: {'quantity': 1, 'timestamp': ...}
            # ID here refers to the Subscription Item ID, not Subscription ID
            return stripe.SubscriptionItem.create_usage_record(req_id, **payload)

        raise ValueError(f"Unknown Subscription Action: {action}")