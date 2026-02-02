import stripe
from typing import Any, Dict, List


class DebtCollector:
    """[THE DEBT COLLECTOR] Manages specific bills of record."""

    def execute(self, action: str, req_id: str, payload: Dict, expand: List[str], limit: int) -> Any:
        if action == "create":
            return stripe.Invoice.create(**payload, expand=expand)

        elif action == "retrieve":
            return stripe.Invoice.retrieve(req_id, expand=expand)

        elif action == "finalize":
            return stripe.Invoice.finalize_invoice(req_id, expand=expand)

        elif action == "pay":
            return stripe.Invoice.pay(req_id, expand=expand)

        elif action == "void":
            return stripe.Invoice.void_invoice(req_id, expand=expand)

        elif action == "list":
            return stripe.Invoice.list(limit=limit, expand=expand, **payload)

        raise ValueError(f"Unknown Invoice Action: {action}")