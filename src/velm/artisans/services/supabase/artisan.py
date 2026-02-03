import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import SupabaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

# --- DOMAINS ---
from .client import SupabaseConnection
from .domains.database import DatabaseWeaver
from .domains.auth import AuthGuard
from .domains.storage import StorageKeeper

Logger = logging.getLogger("SupabaseArtisan")


class SupabaseArtisan(BaseArtisan[SupabaseRequest]):
    """
    =============================================================================
    == THE SUPABASE SOVEREIGN (V-Ω-MODULAR-TITANIUM)                           ==
    =============================================================================
    The unified gateway to the Supabase infrastructure.
    It routes the plea to the correct Domain Weaver based on the request.domain.
    """

    def execute(self, request: SupabaseRequest) -> ScaffoldResult:
        try:
            # 1. Establish the Silver Cord
            client = SupabaseConnection.get_client()

            result_data = None

            # 2. Route to Domain
            if request.domain == "database":
                weaver = DatabaseWeaver(client)
                response = weaver.execute(request)
                # Supabase-py response object handling
                result_data = response.data if hasattr(response, 'data') else response

            elif request.domain == "auth":
                guard = AuthGuard(client)
                result_data = guard.execute(request)

            elif request.domain == "storage":
                keeper = StorageKeeper(client)
                result_data = keeper.execute(request)

            elif request.domain == "function":
                # Edge Function Invocation
                result_data = client.functions.invoke(request.table, invoke_options=request.data)

            else:
                return self.engine.failure(f"Unknown Supabase Domain: {request.domain}")

            return self.engine.success(
                f"Supabase Rite ({request.domain}) Completed.",
                data=result_data
            )

        except Exception as e:
            Logger.error(f"Supabase Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Supabase Interaction Failed: {str(e)}")