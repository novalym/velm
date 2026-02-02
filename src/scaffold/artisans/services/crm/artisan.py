import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import CRMRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

from .factory import CRMFactory

Logger = logging.getLogger("CRMArtisan")


class CRMArtisan(BaseArtisan[CRMRequest]):
    """
    =============================================================================
    == THE HIGH DIPLOMAT (V-Ω-RELATIONSHIP-ENGINE)                             ==
    =============================================================================
    LIF: ∞ | ROLE: CRM_ORCHESTRATOR

    Manages the web of souls across external CRMs.
    Handles Upserts, Associations, and CRUD with normalized Gnosis.
    """

    def execute(self, request: CRMRequest) -> ScaffoldResult:
        try:
            # 1. Summon the Diplomat
            provider = CRMFactory.get_provider(request.provider, self.engine)
            result = None

            # 2. Execute the Core Rite
            if request.action == "create":
                result = provider.create(request.entity, request.data)

            elif request.action == "update":
                if not request.id: return self.engine.failure("Update requires ID.")
                result = provider.update(request.entity, request.id, request.data)

            elif request.action == "get":
                if not request.id: return self.engine.failure("Get requires ID.")
                result = provider.get(request.entity, request.id, request.properties)

            elif request.action == "search":
                if not request.match_value: return self.engine.failure("Search requires match_value.")
                result = provider.search(request.entity, request.match_key, request.match_value, request.properties)

            elif request.action == "upsert":
                # The Intelligent Rite
                if not request.match_value:
                    # If match_value not explicit, try to find it in data using match_key
                    request.match_value = request.data.get(request.match_key)

                if not request.match_value:
                    return self.engine.failure(f"Upsert requires '{request.match_key}' in data or match_value.")

                result = provider.upsert(request.entity, request.match_key, request.match_value, request.data)

            elif request.action == "associate":
                # Explicit association command
                # Requires 'to_entity' and 'to_id' in data or params?
                # Let's assume associations list in request is for POST-CREATE linking,
                # but 'associate' action is for dedicated linking.
                # We interpret request.data['to_entity'] etc.
                pass  # Implementation specific to direct call

            else:
                return self.engine.failure(f"Unknown CRM Action: {request.action}")

            # 3. The Rite of Association (Post-Op)
            # If we created/upserted a record, and associations were requested, forge the links now.
            if result and request.associations and (request.action in ["create", "upsert"]):

                # Extract the ID of the primary entity
                # HubSpot returns 'id', others might vary. We assume standardized 'id'.
                primary_id = result.get('id')

                if primary_id:
                    link_results = []
                    for assoc in request.associations:
                        to_ent = assoc.get("to_entity")
                        to_id = assoc.get("to_id")
                        if to_ent and to_id:
                            link_res = provider.associate(request.entity, primary_id, to_ent, to_id)
                            link_results.append(link_res)

                    # Attach link info to result metadata
                    if isinstance(result, dict):
                        result["_associations"] = link_results

            return self.engine.success(
                f"CRM Rite ({request.action} {request.entity}) Completed.",
                data=result
            )

        except Exception as e:
            Logger.error(f"CRM Fracture: {e}", exc_info=True)
            return self.engine.failure(f"CRM Protocol Failed: {str(e)}")