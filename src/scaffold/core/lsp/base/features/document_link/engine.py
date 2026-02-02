# Path: core/lsp/base/features/document_link/engine.py
# ----------------------------------------------------
import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import DocumentLinkProvider
from .models import DocumentLink, DocumentLinkParams

Logger = logging.getLogger("DocumentLinkEngine")


class DocumentLinkEngine:
    """
    =============================================================================
    == THE HYPERTEXT CONDUCTOR (V-Ω-OPTICAL-CORE)                              ==
    =============================================================================
    LIF: 10,000,000 | ROLE: LINK_DISPATCHER

    Coordinates the Council of Weavers to detect and resolve links.
    Supports parallel scanning and lazy resolution.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[DocumentLinkProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="LinkWeaver"
        )

    def register(self, provider: DocumentLinkProvider):
        self.providers.append(provider)
        Logger.debug(f"Link Weaver Registered: {provider.name}")

    def compute(self, params: DocumentLinkParams) -> List[DocumentLink]:
        """[THE RITE OF DISCOVERY]"""
        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return []

        all_links = []

        # Parallel Execution
        futures = {self._executor.submit(p.provide_links, doc): p for p in self.providers}

        # 500ms timeout for link detection (needs to be fast)
        done, not_done = concurrent.futures.wait(futures, timeout=0.5)

        for future in done:
            try:
                links = future.result()
                if links: all_links.extend(links)
            except Exception as e:
                Logger.error(f"Weaver fractured: {e}")

        return all_links

    def resolve(self, link: DocumentLink) -> DocumentLink:
        """[THE RITE OF RESOLUTION]"""
        # In V1, we assume the data payload contains the provider name if we need specific resolution
        # For now, we return as is or implement specific provider lookup
        return link