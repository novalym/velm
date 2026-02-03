import stripe
from typing import Any, Dict


class KineticPay:
    """[THE KINETIC PAY] Generates instant payment URLs."""

    def execute(self, action: str, req_id: str, payload: Dict) -> Any:
        if action == "create":
            return stripe.PaymentLink.create(**payload)

        elif action == "retrieve":
            return stripe.PaymentLink.retrieve(req_id)

        elif action == "update":
            return stripe.PaymentLink.modify(req_id, **payload)

        raise ValueError(f"Unknown Link Action: {action}")