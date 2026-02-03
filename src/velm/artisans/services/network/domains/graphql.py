from typing import Any
from ...client import GlobalConnectionPool
from .....contracts.heresy_contracts import ArtisanHeresy


class GraphEngine:
    """[THE QUERY WEAVER] Speaks the tongue of Graphs."""

    def execute(self, request) -> Any:
        if not request.query:
            raise ArtisanHeresy("GraphQL Rite requires a 'query' payload.")

        client = GlobalConnectionPool.get_client()

        # Prepare Payload
        gql_payload = {"query": request.query}
        if request.variables:
            gql_payload["variables"] = request.variables

        try:
            response = client.post(
                url=request.url,
                headers=request.headers,
                json=gql_payload,
                timeout=request.timeout
            )

            if response.is_error:
                return {
                    "error": True,
                    "status": response.status_code,
                    "body": response.text
                }

            result = response.json()

            # Check for GraphQL-level errors
            if "errors" in result:
                return {
                    "error": True,
                    "gql_errors": result["errors"],
                    "data": result.get("data")
                }

            return result.get("data")

        except Exception as e:
            raise ArtisanHeresy(f"GraphQL Rite Fractured: {e}")