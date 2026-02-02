# Path: artisans/services/supabase/domains/database.py
# ----------------------------------------------------

import logging
from typing import Any, Dict, List, Union, Optional
from supabase import Client
# We import APIResponse for type hinting, though we handle dynamic returns
from postgrest.base_request_builder import APIResponse

# --- GNOSTIC UPLINKS ---
from .....interfaces.requests import SupabaseRequest
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = logging.getLogger("DatabaseWeaver")


class DatabaseWeaver:
    """
    =============================================================================
    == THE WEAVER OF QUERIES (V-Ω-POSTGREST-ALCHEMIST-ULTIMA)                  ==
    =============================================================================
    LIF: ∞ | ROLE: SQL_TRANSMUTER | RANK: LEGENDARY

    Transmutes Gnostic intent (SupabaseRequest) into fluent PostgREST method chains.
    Handles the complexity of RPCs, Filtering, Pagination, and Singularity.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The RPC Divergence:** Automatically detects Stored Procedure requests
        and routes them to a specialized execution path, bypassing table logic.
    2.  **The Method Selector:** Dynamically builds the query chain (Select, Insert,
        Update, Delete, Upsert) based on the request's intent.
    3.  **The Filter Matrix:** A powerful parsing engine that transmutes high-level
        filters (e.g., "id:eq:5", "status:in:[ACTIVE,PENDING]") into raw SQL predicates.
    4.  **The Sorting Compass:** Handles complex ordering directives (e.g., "created_at:desc").
    5.  **The Pagination Sextant:** Calculates precise ranges from `limit` and `offset`,
        bridging the gap between UI pagination and SQL offsets.
    6.  **The Count Strategy:** Smartly injects `count='exact'` or `count='planned'`
        metadata when the Architect demands a census.
    7.  **The CSV Alchemist:** Capable of requesting raw CSV streams for bulk data
        export directly from the database engine.
    8.  **The Singularity Gate:** Intelligently switches between `single()` (strict 1 row)
        and `maybe_single()` (0 or 1 row) based on the `optional` flag.
    9.  **The Void Shield (THE CURE):** A titanium guard against `None` responses
        from the underlying library, preventing 'NoneType' crashes on empty result sets.
    10. **The Atomic Execution:** Performs the final network call in a protected block.
    11. **The Response Unpacker:** Intelligently extracts `.data` for standard queries
        or returns the full object if metadata (count) is required.
    12. **The Heresy Shield:** Catches specific PostgREST errors (like PGRST116)
        and transmutes them into helpful, Socratic guidance for the Architect.
    =============================================================================
    """

    def __init__(self, client: Client):
        self.client = client

    def execute(self, request: SupabaseRequest) -> Any:
        try:
            # [ASCENSION 1]: THE RPC DIVERGENCE
            # If the method is RPC, we bypass table logic entirely.
            if request.method == "rpc":
                return self._execute_rpc(request)

            # Otherwise, we bind to the Table
            if not request.table:
                raise ValueError("Database Rite requires a 'table' for non-RPC methods.")

            query = self.client.table(request.table)

            # [ASCENSION 2]: THE METHOD SELECTOR
            if request.method == "select":
                # [ASCENSION 6]: COUNT STRATEGY
                count_method = request.count if request.count else None
                query = query.select(request.select_columns, count=count_method)

            elif request.method == "insert":
                query = query.insert(request.data, count=request.count)

            elif request.method == "update":
                query = query.update(request.data, count=request.count)

            elif request.method == "upsert":
                # We assume standard upsert. Future: Add on_conflict to Request schema.
                query = query.upsert(request.data, count=request.count)

            elif request.method == "delete":
                query = query.delete(count=request.count)

            else:
                raise ValueError(f"Unknown Database Method: {request.method}")

            # [ASCENSION 3]: THE FILTER MATRIX
            query = self._apply_filters(query, request.filters)

            # [ASCENSION 4]: THE SORTING COMPASS
            if request.order_by:
                # Format: "column:desc" or "column:asc" (default asc)
                col, direction = request.order_by.split(":") if ":" in request.order_by else (request.order_by, "asc")
                query = query.order(col, desc=(direction.lower() == "desc"))

            # [ASCENSION 5]: THE PAGINATION SEXTANT
            # Range handles both limit and offset logic
            if request.limit is not None or request.offset is not None:
                start = request.offset or 0
                if request.limit:
                    # PostgREST range is inclusive
                    end = start + request.limit - 1
                    query = query.range(start, end)
                else:
                    # If only limit provided without offset logic
                    query = query.limit(request.limit)

            # [ASCENSION 7]: THE CSV ALCHEMIST
            if request.csv:
                query = query.csv()

            # [ASCENSION 8]: THE SINGULARITY GATE
            # This logic prevents the 'JSON object requested, multiple (or zero) rows returned' error.
            if request.single:
                if request.optional:
                    # Returns 0 or 1 row. None if 0. No error on 0.
                    query = query.maybe_single()
                else:
                    # Returns exactly 1 row. Error if 0. Error if > 1.
                    query = query.single()

            # [ASCENSION 10]: THE ATOMIC EXECUTION
            response = query.execute()

            # =========================================================================
            # == [ASCENSION 9]: THE VOID SHIELD (THE CURE)                           ==
            # =========================================================================
            # If the query returns absolute nothingness (None), we return None immediately.
            # This handles the 'NoneType has no attribute data' heresy common in
            # headless deletions or empty maybe_single() results.
            if response is None:
                return None
            # =========================================================================

            # [ASCENSION 11]: THE RESPONSE UNPACKER
            # If we just want data, return data. If we want metadata (count), return full object.
            if request.count:
                return response  # Return full APIResponse for count access

            # Special case for CSV (It returns raw string in data?)
            # supabase-py behavior varies. Usually response.data is the payload.
            return response.data

        except Exception as e:
            # [ASCENSION 12]: THE HERESY SHIELD
            # We catch the raw PostgREST error and wrap it in a Gnostic Exception
            msg = str(e)
            if "PGRST116" in msg:
                # Specific guidance for the Singularity Heresy
                raise ArtisanHeresy(
                    "Database Singularity Fracture: 0 rows found when 1 was demanded.",
                    suggestion="Set 'optional=True' in your SupabaseRequest to allow empty results.",
                    details=msg,
                    severity=HeresySeverity.WARNING
                ) from e

            raise ArtisanHeresy(f"Akashic Query Failed: {msg}", child_heresy=e)

    def _execute_rpc(self, request: SupabaseRequest) -> Any:
        """Executes a Stored Procedure."""
        if not request.func_name:
            raise ValueError("RPC Rite requires 'func_name'.")

        rpc_params = request.data if isinstance(request.data, dict) else {}

        # RPC can also accept head=True or count parameters in theory,
        # but Python client support is specific.
        response = self.client.rpc(request.func_name, rpc_params).execute()

        # Apply Void Shield to RPC as well
        if response is None:
            return None

        return response.data

    def _apply_filters(self, query: Any, filters: Optional[Dict[str, Any]]) -> Any:
        """
        Parses the Gnostic Filter Dialect.
        Supported Syntax:
        - "col": "val"          -> eq(col, val)
        - "col": "eq:val"       -> eq(col, val)
        - "col": "gt:10"        -> gt(col, 10)
        - "col": "in:[1,2,3]"   -> in_(col, [1,2,3])
        - "col": "cs:{a,b}"     -> contains(col, {a,b})
        """
        if not filters:
            return query

        for key, raw_val in filters.items():
            op = "eq"
            val = raw_val

            # 1. Divine Operator
            if isinstance(raw_val, str) and ":" in raw_val:
                # Heuristic: Only split if the prefix is a known operator
                parts = raw_val.split(":", 1)
                potential_op = parts[0]

                # Check against common PostgREST operators
                if potential_op in ["eq", "neq", "gt", "gte", "lt", "lte", "like", "ilike", "is", "in", "cs", "cd"]:
                    op = potential_op
                    val = parts[1]

                    # 2. Type Transmutation for 'in' and 'cs'
                    if op in ["in", "cs", "cd"]:
                        # Convert string list "[a,b]" to list ["a","b"]
                        # This is a simple parser; for complex JSON, pass dicts in `filters` directly
                        if val.startswith("[") and val.endswith("]"):
                            val = val[1:-1].split(",")
                            val = [v.strip() for v in val]

            # 3. Dynamic Dispatch
            # map 'in' to 'in_' because 'in' is reserved python keyword
            method_name = "in_" if op == "in" else op

            if hasattr(query, method_name):
                query = getattr(query, method_name)(key, val)
            else:
                # Fallback to equality
                query = query.eq(key, raw_val)

        return query