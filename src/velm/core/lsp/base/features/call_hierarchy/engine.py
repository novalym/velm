# Path: core/lsp/base/features/call_hierarchy/engine.py
# -----------------------------------------------------
import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import CallHierarchyProvider
from .models import (
    CallHierarchyItem, CallHierarchyIncomingCall, CallHierarchyOutgoingCall,
    CallHierarchyPrepareParams, CallHierarchyIncomingCallsParams, CallHierarchyOutgoingCallsParams
)

Logger = logging.getLogger("CallHierarchyEngine")


class CallHierarchyEngine:
    """
    =============================================================================
    == THE GRAPH CONDUCTOR (V-Ω-TOPOLOGICAL-CORE)                              ==
    =============================================================================
    LIF: 10,000,000 | ROLE: HIERARCHY_DISPATCHER

    Coordinates the Council of Tracers.
    Handles the three-stage handshake of the Hierarchy Protocol.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[CallHierarchyProvider] =[]

    def register(self, provider: CallHierarchyProvider):
        self.providers.append(provider)
        Logger.debug(f"Hierarchy Tracer Registered: {provider.name}")

    def prepare(self, params: CallHierarchyPrepareParams) -> List[CallHierarchyItem]:
        """STAGE 1: Resolve the root node."""
        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return[]

        import concurrent.futures
        futures = {self.server.foundry.submit(f"call-prep-{p.name}", p.prepare, doc, params.position): p for p in self.providers}

        items =[]
        done, _ = concurrent.futures.wait(futures, timeout=1.0)

        for future in done:
            try:
                res = future.result()
                if res: items.extend(res)
            except Exception as e:
                Logger.error(f"Prepare fractured: {e}")

        return items

    def incoming_calls(self, params: CallHierarchyIncomingCallsParams) -> List[CallHierarchyIncomingCall]:
        """STAGE 2: Upstream Traversal."""
        results =[]
        import concurrent.futures
        futures = {self.server.foundry.submit(f"call-in-{p.name}", p.incoming_calls, params.item): p for p in self.providers}

        done, _ = concurrent.futures.wait(futures, timeout=2.0)
        for future in done:
            try:
                res = future.result()
                if res: results.extend(res)
            except Exception as e:
                Logger.error(f"Incoming fractured: {e}")
        return results

    def outgoing_calls(self, params: CallHierarchyOutgoingCallsParams) -> List[CallHierarchyOutgoingCall]:
        """STAGE 3: Downstream Traversal."""
        results =[]
        import concurrent.futures
        futures = {self.server.foundry.submit(f"call-out-{p.name}", p.outgoing_calls, params.item): p for p in self.providers}

        done, _ = concurrent.futures.wait(futures, timeout=2.0)
        for future in done:
            try:
                res = future.result()
                if res: results.extend(res)
            except Exception as e:
                Logger.error(f"Outgoing fractured: {e}")
        return results