import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import NetworkRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

# --- DOMAINS ---
from .domains.rest import RestEngine
from .domains.graphql import GraphEngine
from .domains.webhook import WebhookEmitter

Logger = logging.getLogger("NetworkArtisan")


class NetworkArtisan(BaseArtisan[NetworkRequest]):
    """
    =============================================================================
    == THE HIGH CONNECTOR (V-Ω-UNIVERSAL-NETWORK)                              ==
    =============================================================================
    LIF: ∞ | ROLE: IO_ORCHESTRATOR

    The unified gateway to the Digital Ether.
    Routes intent based on Protocol (HTTP, GraphQL, Webhook).
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.rest = RestEngine()
        self.graph = GraphEngine()
        self.webhook = WebhookEmitter()

    def execute(self, request: NetworkRequest) -> ScaffoldResult:
        try:
            result = None

            # --- ROUTING MATRIX ---
            if request.protocol == "http":
                result = self.rest.execute(request)

            elif request.protocol == "graphql":
                result = self.graph.execute(request)

            elif request.protocol == "webhook":
                result = self.webhook.execute(request)

            else:
                return self.engine.failure(f"Unknown Protocol: {request.protocol}")

            # Check for soft errors returned by engines
            if isinstance(result, dict) and result.get("error") is True:
                return self.engine.failure(
                    f"Network Error {result.get('status')}",
                    data=result
                )

            return self.engine.success(
                f"Network Rite ({request.protocol} -> {request.url}) Completed.",
                data=result
            )

        except Exception as e:
            Logger.error(f"Network Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Network Protocol Failed: {str(e)}")