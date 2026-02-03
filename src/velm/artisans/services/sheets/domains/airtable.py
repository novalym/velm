import os
from typing import Any
from .....contracts.heresy_contracts import ArtisanHeresy


class AirtableEngine:
    """[THE AIR WEAVER]"""

    def execute(self, request) -> Any:
        try:
            from pyairtable import Api
        except ImportError:
            raise ArtisanHeresy("pyairtable not found. Run `pip install pyairtable`.")

        token = os.environ.get("AIRTABLE_API_KEY")
        if not token: raise ArtisanHeresy("AIRTABLE_API_KEY missing.")

        api = Api(token)
        table = api.table(request.base_id, request.table_name)

        if request.action == "read":
            # Returns list of records with 'id' and 'fields'
            return table.all()

        elif request.action == "append":
            # Batch create
            return table.batch_create(request.rows)

        elif request.action == "update":
            if not request.row_id:
                raise ArtisanHeresy("Airtable update requires row_id.")
            # Single update for simplicity, batch update requires mapping
            # Assuming rows[0] is the data
            return table.update(request.row_id, request.rows[0])

        elif request.action == "delete":
            if not request.row_id:
                raise ArtisanHeresy("Airtable delete requires row_id.")
            return table.delete(request.row_id)

        raise ValueError(f"Unknown Airtable Action: {request.action}")