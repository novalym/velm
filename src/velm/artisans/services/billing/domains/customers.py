import stripe
from typing import Any, Dict, List


class CustomerLedger:
    """[THE IDENTITY LEDGER] Manages the payers of tribute."""

    def execute(self, action: str, req_id: str, payload: Dict, expand: List[str], limit: int) -> Any:
        if action == "create":
            return stripe.Customer.create(**payload, expand=expand)

        elif action == "retrieve":
            if not req_id: raise ValueError("Customer ID required for retrieval.")
            return stripe.Customer.retrieve(req_id, expand=expand)

        elif action == "update":
            if not req_id: raise ValueError("Customer ID required for update.")
            return stripe.Customer.modify(req_id, **payload, expand=expand)

        elif action == "delete":
            if not req_id: raise ValueError("Customer ID required for deletion.")
            return stripe.Customer.delete(req_id)

        elif action == "list":
            return stripe.Customer.list(limit=limit, expand=expand, **payload)

        elif action == "search":
            # Payload must contain 'query' key: "name:'John' AND metadata['id']:'123'"
            query = payload.get("query", "")
            return stripe.Customer.search(query=query, limit=limit, expand=expand)

        raise ValueError(f"Unknown Customer Action: {action}")