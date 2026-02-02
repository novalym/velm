import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import BillingRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

# --- DOMAINS ---
from .client import StripeMint
from .domains.customers import CustomerLedger
from .domains.subscriptions import RevenueEngine
from .domains.portal import PortalGateway
from .domains.products import CatalogManager
from .domains.invoices import DebtCollector
from .domains.links import KineticPay

Logger = logging.getLogger("BillingArtisan")


class BillingArtisan(BaseArtisan[BillingRequest]):
    """
    =============================================================================
    == THE HIGH TREASURER (V-Ω-MODULAR-FINANCE)                                ==
    =============================================================================
    LIF: ∞ | ROLE: CAPITAL_ORCHESTRATOR

    The unified gateway to the Stripe Sovereign Lattice.
    Routes fiscal intent to the specialized Domain Engines.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        # Ensure the Mint is open
        StripeMint.get_client()

        # Instantiate Domains
        self.customers = CustomerLedger()
        self.subscriptions = RevenueEngine()
        self.portal = PortalGateway()
        self.catalog = CatalogManager()
        self.invoices = DebtCollector()
        self.links = KineticPay()

    def execute(self, request: BillingRequest) -> ScaffoldResult:
        try:
            result = None
            req_id = request.id
            payload = request.payload
            expand = request.expand
            limit = request.limit
            action = request.action

            # --- ROUTING MATRIX ---

            if request.entity == "customer":
                result = self.customers.execute(action, req_id, payload, expand, limit)

            elif request.entity == "subscription":
                result = self.subscriptions.execute(action, req_id, payload, expand, limit)

            elif request.entity == "portal":
                result = self.portal.execute(action, payload)

            elif request.entity in ["product", "price"]:
                result = self.catalog.execute(request.entity, action, req_id, payload, limit)

            elif request.entity == "invoice":
                result = self.invoices.execute(action, req_id, payload, expand, limit)

            elif request.entity == "payment_link":
                result = self.links.execute(action, req_id, payload)

            else:
                return self.engine.failure(f"Unknown Fiscal Entity: {request.entity}")

            return self.engine.success(
                f"Treasury Rite ({request.entity} -> {action}) Completed.",
                data=result
            )

        except Exception as e:
            Logger.error(f"Treasury Fracture: {e}", exc_info=True)
            # Stripe errors usually have a user_message or error.message
            msg = str(e)
            if hasattr(e, 'user_message'): msg = e.user_message

            return self.engine.failure(
                f"Billing Protocol Failed: {msg}",
                data={"full_error": str(e)}
            )