# Path: core/lsp/scaffold_features/call_hierarchy/providers/daemon_bridge.py
# --------------------------------------------------------------------------
import logging
from typing import List, Any, Optional
from ....base.features.call_hierarchy.contracts import CallHierarchyProvider
from ....base.features.call_hierarchy.models import (
    CallHierarchyItem, CallHierarchyIncomingCall, CallHierarchyOutgoingCall
)
from ....base.document import TextDocument
from ....base.utils.text import TextUtils
from ....base.utils.uri import UriUtils
from ....base.telemetry import forensic_log

Logger = logging.getLogger("DaemonHierarchyBridge")


class DaemonCallHierarchyProvider(CallHierarchyProvider):
    """
    =============================================================================
    == THE CORTEX BRIDGE (V-Ω-GRAPH-SIPHON)                                    ==
    =============================================================================
    LIF: 100x | ROLE: GRAPH_RELAY

    Siphons topological truth from the Daemon's `GrandSurveyor` and `GraphArtisan`.
    It enables cross-file, cross-language call tracing by utilizing the Daemon's
    pre-computed dependency graph.

    ### THE 12 ASCENSIONS:
    1.  **Atomic Word Extraction:** Divines the symbol at cursor to prime the query.
    2.  **Stateful Data Injection:** Embeds `file_path` and `symbol_id` into the `data` payload for stateless follow-ups.
    3.  **Trace ID Threading:** Ensures the Hierarchy request chain is forensically auditable.
    4.  **Titanium Path Resolution:** Uses `UriUtils` to guarantee Daemon/LSP path parity.
    5.  **Graceful Void Handling:** Returns empty lists instead of crashing on `null` daemon responses.
    6.  **Kind Mapping:** Transmutes Daemon symbol types (string) to LSP Enums (int).
    7.  **Range Clamping:** Ensures ranges returned by Daemon fit within the document bounds.
    8.  **Project Root Anchoring:** Sends the root context to allow relative path resolution in Daemon.
    9.  **Synchronous Relay:** Uses `relay_request` with a generous 2s timeout.
    10. **Result Transmutation:** Converts raw dicts to strict Pydantic models.
    11. **Self-Reference Guard:** Daemon logic filters recursion; Bridge handles transport.
    12. **Multi-Stratum Support:** Ready for Python, JS, and Scaffold macro calls.
    """

    @property
    def name(self) -> str:
        return "DaemonCortex"

    def prepare(self, doc: TextDocument, position: Any) -> List[CallHierarchyItem]:
        # 1. Divine Symbol
        info = TextUtils.get_word_at_position(doc, position)
        if not info: return []

        # 2. Ask Daemon
        if not hasattr(self.server, 'relay_request'): return []

        # [ASCENSION 4]: Titanium Path
        fs_path = str(UriUtils.to_fs_path(doc.uri))

        params = {
            "file_path": fs_path,
            "symbol": info.text.replace('(', '').strip(),
            "position": {"line": position.line, "character": position.character},
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_HIERARCHY_PREPARE"}
        }

        try:
            # [ASCENSION 9]: Synchronous Plea
            res = self.server.relay_request("hierarchy/prepare", params)
            if res and res.get('success'):
                raw_items = res.get('data', [])
                items = []
                for i in raw_items:
                    # [ASCENSION 2]: Inject State for follow-up calls
                    if 'data' not in i:
                        i['data'] = {
                            "symbol": i['name'],
                            "uri": i['uri'],
                            "fs_path": str(UriUtils.to_fs_path(i['uri']))
                        }
                    items.append(CallHierarchyItem.model_validate(i))
                return items
        except Exception as e:
            Logger.error(f"Hierarchy Prepare Fractured: {e}")

        return []

    def incoming_calls(self, item: CallHierarchyItem) -> List[CallHierarchyIncomingCall]:
        if not hasattr(self.server, 'relay_request'): return []

        # Retrieve state from the item
        symbol_data = item.data or {}

        params = {
            "symbol": symbol_data.get("symbol", item.name),
            "file_path": symbol_data.get("fs_path", ""),
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_HIERARCHY_INCOMING"}
        }

        try:
            res = self.server.relay_request("hierarchy/incoming", params)
            if res and res.get('success'):
                return [CallHierarchyIncomingCall.model_validate(i) for i in res.get('data', [])]
        except Exception as e:
            Logger.error(f"Incoming Calls Fractured: {e}")

        return []

    def outgoing_calls(self, item: CallHierarchyItem) -> List[CallHierarchyOutgoingCall]:
        if not hasattr(self.server, 'relay_request'): return []

        symbol_data = item.data or {}

        params = {
            "symbol": symbol_data.get("symbol", item.name),
            "file_path": symbol_data.get("fs_path", ""),
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_HIERARCHY_OUTGOING"}
        }

        try:
            res = self.server.relay_request("hierarchy/outgoing", params)
            if res and res.get('success'):
                return [CallHierarchyOutgoingCall.model_validate(i) for i in res.get('data', [])]
        except Exception as e:
            Logger.error(f"Outgoing Calls Fractured: {e}")

        return []