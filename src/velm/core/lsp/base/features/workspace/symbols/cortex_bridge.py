# Path: core/lsp/features/workspace/symbols/cortex_bridge.py
# -----------------------------------------------------------
import logging
from typing import List
from .models import WorkspaceSymbol


class DaemonCortexBridge:
    """[THE SILVER BRIDGE] Communes with the Daemon's global index."""

    def __init__(self, server):
        self.server = server

    def query(self, query: str) -> List[WorkspaceSymbol]:
        # [ASCENSION 1]: KINETIC REQUISITION
        if not hasattr(self.server, 'relay_request'): return []

        params = {
            "query": query,
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_SYMBOL_SCRY"}
        }

        try:
            # Synchronous plea across the portal
            response = self.server.relay_request("workspace/symbol", params)
            if response and response.get('success'):
                # Transmute into our models
                raw_data = response.get('data', [])
                return [WorkspaceSymbol.model_validate(s) for s in raw_data]
        except Exception:
            pass

        return []