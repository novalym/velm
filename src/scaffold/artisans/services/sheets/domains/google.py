import os
import json
from typing import Any, Dict, List
from .....contracts.heresy_contracts import ArtisanHeresy


class GoogleSheetEngine:
    """[THE G_SUITE WEAVER]"""

    def execute(self, request) -> Any:
        try:
            import gspread
        except ImportError:
            raise ArtisanHeresy("gspread not found. Run `pip install gspread`.")

        creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not creds_json:
            raise ArtisanHeresy("GOOGLE_SERVICE_ACCOUNT_JSON missing.")

        try:
            creds_dict = json.loads(creds_json)
            gc = gspread.service_account_from_dict(creds_dict)

            # Open Sheet
            sh = gc.open_by_key(request.base_id)
            worksheet = sh.worksheet(request.table_name)

            if request.action == "read":
                if request.range:
                    return worksheet.get(request.range)
                return worksheet.get_all_records()

            elif request.action == "append":
                # Flatten dicts to lists if needed, or assume caller provides list of lists for 'rows'
                # But Request model says List[Dict]. We must map headers.

                # Simple append (list of lists)
                # We convert dicts to values based on header row if possible,
                # but for V1 we just assume the user sends row-aligned values OR we append raw.

                # Smart Append:
                values = [list(r.values()) for r in request.rows]
                return worksheet.append_rows(values, value_input_option=request.value_input_option)

            elif request.action == "clear":
                return worksheet.clear()

        except Exception as e:
            raise ArtisanHeresy(f"Google Sheet Fracture: {e}")