# Path: core/lsp/base/manager.py
# ------------------------------

import logging
import threading
from typing import Dict, Optional, List, Any
from .document import TextDocument
from .utils.uri import UriUtils
from .telemetry import forensic_log

# [ASCENSION 13]: LAZY IMPORT FOR TYPE RESURRECTION
try:
    from .types import TextDocumentContentChangeEvent
except ImportError:
    pass


class DocumentLibrarian:
    """
    =============================================================================
    == THE DOCUMENT LIBRARIAN (V-Ω-MULTIDIMENSIONAL-MEMORY-FIXED)              ==
    =============================================================================
    LIF: 100,000,000 | ROLE: MEMORY_ORCHESTRATOR

    [THE FIX]: Implements the 'Unwrap' Rite to handle Pydantic V2 models safely.
    Annihilates the 'no attribute get' heresy.
    """

    def __init__(self, server: Any):
        self.server = server
        self._documents: Dict[str, TextDocument] = {}
        self._lock = threading.RLock()
        self._total_mass = 0  # Track total byte size

    def _unwrap(self, item: Any) -> Dict[str, Any]:
        """
        [THE RITE OF UNWRAPPING]
        Transmutes Pydantic Models into Dictionaries for legacy access patterns.
        """
        if isinstance(item, dict): return item
        if hasattr(item, 'model_dump'): return item.model_dump(mode='json', by_alias=True)
        if hasattr(item, 'dict'): return item.dict(by_alias=True)
        return {}

    def open(self, item: Any):
        """[RITE]: OPENING - Ingests a new scripture."""
        # [THE FIX]: Unwrap the vessel before dissection
        data = self._unwrap(item)

        uri = data.get('uri')
        canon_uri = UriUtils.normalize_uri(uri)

        with self._lock:
            doc = TextDocument(
                uri=canon_uri,
                language_id=data.get('languageId', 'unknown'),
                version=data.get('version', 0),
                text=data.get('text', '')
            )

            # Check mass
            mass = len(doc.text)
            if canon_uri in self._documents:
                self._total_mass -= len(self._documents[canon_uri].text)

            self._documents[canon_uri] = doc
            self._total_mass += mass

            if self._total_mass > 100 * 1024 * 1024:
                forensic_log(f"Metabolic Stress: Library at {self._total_mass / 1024 / 1024:.1f}MB", "WARN",
                             "LIBRARIAN")

    def change(self, params: Any):
        """[RITE]: MUTATION - Applies deltas to a document."""
        # [THE FIX]: Unwrap the params container
        data = self._unwrap(params)

        text_doc = data.get('textDocument', {})
        uri = text_doc.get('uri')
        version = text_doc.get('version')

        canon_uri = UriUtils.normalize_uri(uri)

        with self._lock:
            doc = self._documents.get(canon_uri)
            if not doc:
                forensic_log(f"Phantom Edit: {canon_uri} is not manifest.", "ERROR", "LIBRARIAN")
                return

            # Apply all content changes in order
            for change_item in data.get('contentChanges', []):
                # Ensure change item is handled as a proper object
                # If we unwrapped everything to dicts, we can re-validate or just pass dicts
                # if TextDocument.apply_change supports it.
                # For safety, we re-inflate to the Contract.

                try:
                    # Lazy load inside method to avoid circular imports at top level
                    from .types import TextDocumentContentChangeEvent
                    change = TextDocumentContentChangeEvent.model_validate(change_item)
                except Exception:
                    # Fallback for manual dict construction if Pydantic fails or missing
                    # This handles the case where 'change_item' is already a dict
                    pass

                    # Actually, TextDocument.apply_change expects an object with .range and .text
                # If we have a dict, we can wrap it in a SimpleNamespace or just re-validate.
                # Re-validating is safest.
                from .types import TextDocumentContentChangeEvent
                change_obj = TextDocumentContentChangeEvent.model_validate(change_item)

                old_len = len(doc.text)
                doc.apply_change(change_obj, version)
                self._total_mass = self._total_mass - old_len + len(doc.text)

    def close(self, uri: Any):
        """[RITE]: OBLIVION - Returns a scripture to the void."""
        # Handle if uri passes as object or string
        uri_str = uri.uri if hasattr(uri, 'uri') else str(uri)

        canon_uri = UriUtils.normalize_uri(uri_str)
        with self._lock:
            if canon_uri in self._documents:
                doc = self._documents.pop(canon_uri)
                self._total_mass -= len(doc.text)

    def get(self, uri: str) -> Optional[TextDocument]:
        """Retrieves a document safely."""
        canon_uri = UriUtils.normalize_uri(uri)
        with self._lock:
            return self._documents.get(canon_uri)

    def get_version(self, uri: str) -> int:
        canon_uri = UriUtils.normalize_uri(uri)
        with self._lock:
            doc = self._documents.get(canon_uri)
            return doc.version if doc else -1

    @property
    def open_uris(self) -> List[str]:
        with self._lock:
            return list(self._documents.keys())

    def clear(self):
        """Total memory purification."""
        with self._lock:
            self._documents.clear()
            self._total_mass = 0