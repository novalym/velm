# Path: core/lsp/base/features/type_hierarchy/engine.py
# -----------------------------------------------------
import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import TypeHierarchyProvider
from .models import (
    TypeHierarchyItem,
    TypeHierarchyPrepareParams,
    TypeHierarchySupertypesParams,
    TypeHierarchySubtypesParams
)

Logger = logging.getLogger("TypeHierarchyEngine")


class TypeHierarchyEngine:
    """
    =============================================================================
    == THE GENETIC CONDUCTOR (V-Ω-EVOLUTIONARY-CORE)                           ==
    =============================================================================
    LIF: 10,000,000 | ROLE: INHERITANCE_DISPATCHER

    Coordinates the Council of Geneticists.
    Handles the three-stage handshake of the Type Hierarchy Protocol.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[TypeHierarchyProvider] =[]

    def register(self, provider: TypeHierarchyProvider):
        self.providers.append(provider)
        Logger.debug(f"Genetic Tracer Registered: {provider.name}")

    def prepare(self, params: TypeHierarchyPrepareParams) -> List[TypeHierarchyItem]:
        """STAGE 1: Resolve the root type node."""
        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return[]

        import concurrent.futures
        futures = {self.server.foundry.submit(f"type-prep-{p.name}", p.prepare, doc, params.position): p for p in self.providers}

        items =[]
        done, _ = concurrent.futures.wait(futures, timeout=1.0)

        for future in done:
            try:
                res = future.result()
                if res: items.extend(res)
            except Exception as e:
                Logger.error(f"Prepare fractured: {e}")

        return items

    def supertypes(self, params: TypeHierarchySupertypesParams) -> List[TypeHierarchyItem]:
        """STAGE 2: Upstream Traversal (Parents)."""
        results =[]
        import concurrent.futures
        futures = {self.server.foundry.submit(f"type-super-{p.name}", p.supertypes, params.item): p for p in self.providers}

        done, _ = concurrent.futures.wait(futures, timeout=2.0)
        for future in done:
            try:
                res = future.result()
                if res: results.extend(res)
            except Exception as e:
                Logger.error(f"Supertypes fractured: {e}")
        return results

    def subtypes(self, params: TypeHierarchySubtypesParams) -> List[TypeHierarchyItem]:
        """STAGE 3: Downstream Traversal (Children)."""
        results =[]
        import concurrent.futures
        futures = {self.server.foundry.submit(f"type-sub-{p.name}", p.subtypes, params.item): p for p in self.providers}

        done, _ = concurrent.futures.wait(futures, timeout=2.0)
        for future in done:
            try:
                res = future.result()
                if res: results.extend(res)
            except Exception as e:
                Logger.error(f"Subtypes fractured: {e}")
        return results
