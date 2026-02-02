import stripe
from typing import Any, Dict, List


class CatalogManager:
    """[THE CATALOG MANAGER] Defines the value of things."""

    def execute(self, entity: str, action: str, req_id: str, payload: Dict, limit: int) -> Any:
        # Handles both PRODUCT and PRICE entities

        if entity == "product":
            if action == "create": return stripe.Product.create(**payload)
            if action == "retrieve": return stripe.Product.retrieve(req_id)
            if action == "update": return stripe.Product.modify(req_id, **payload)
            if action == "list": return stripe.Product.list(limit=limit, **payload)

        elif entity == "price":
            if action == "create": return stripe.Price.create(**payload)
            if action == "retrieve": return stripe.Price.retrieve(req_id)
            if action == "update": return stripe.Price.modify(req_id, **payload)  # Usually only metadata
            if action == "list": return stripe.Price.list(limit=limit, **payload)

        raise ValueError(f"Unknown Catalog Action: {entity} {action}")