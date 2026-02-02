# Path: core/lsp/scaffold_server/sync.py
# --------------------------------------
# LIF: INFINITY | ROLE: ISOMORPHIC_SYNCHRONIZER | RANK: SOVEREIGN
# auth_code: Ω_SYNC_TOTALITY_V26_SUTURED_SINGULARITY

import threading
import time
import uuid
import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List, Union

# --- IRON CORE UPLINKS ---
from ..base import (
    forensic_log,
    UriUtils,
    ServerState
)
from ..base.types import (
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    DidSaveTextDocumentParams,
    DidCloseTextDocumentParams,
    MessageType
)
from ....artisans.analyze.reporting.privacy import PrivacySentinel

# --- PHYSICS CONSTANTS ---
BACKPRESSURE_THRESHOLD = 50
MUNDANE_FLUX_SIZE = 10  # Ignore changes < 10 chars if hash matches


class ScriptureSiphon:
    """
    =================================================================================
    == THE ISOMORPHIC SYNCHRONIZER (V-Ω-TOTALITY-V26-SUTURED)                      ==
    =================================================================================
    The circulatory system of the Oracle. Hardened to ensure every scripture is
    anchored to absolute reality before perception begins.
    =================================================================================
    """
    # [ASCENSION 12]: ZERO-OVERHEAD REGISTRY
    __slots__ = ['server', '_last_merkle_seal', '_sync_lock', '_version_map', '_path_registry']

    def __init__(self, server: Any):
        self.server = server
        self._last_merkle_seal: Dict[str, str] = {}
        self._version_map: Dict[str, int] = {}
        self._path_registry: Dict[str, Path] = {}
        self._sync_lock = threading.RLock()

    # =============================================================================
    # == RITE 1: THE GENESIS (DID OPEN)                                          ==
    # =============================================================================

    def did_open(self, params: Any):
        """
        Materializes a new scripture within the Oracle's mind.
        [ASCENSION 1]: Absolute Coordinate Adjudication.
        """
        # 1. TRANSMUTE & UNWRAP
        if isinstance(params, dict):
            params = DidOpenTextDocumentParams.model_validate(params)

        uri = str(params.text_document.uri)
        text = params.text_document.text
        version = params.text_document.version

        with self._sync_lock:
            # 2. [THE CURE]: ABSOLUTE PATH DETERMINISM
            # Dissolve schemes and force absolute physical anchoring
            fs_path = UriUtils.to_fs_path(uri)

            if not fs_path.is_absolute():
                if self.server.project_root:
                    fs_path = (self.server.project_root / fs_path).resolve()
                else:
                    fs_path = fs_path.resolve()

            # Record the absolute path for all future mutations of this URI
            norm_uri = UriUtils.normalize_uri(uri)
            self._path_registry[norm_uri] = fs_path
            self._version_map[norm_uri] = version

            # 3. [ASCENSION 3]: MERKLE SEAL
            content_hash = hashlib.md5(text.encode('utf-8', errors='ignore')).hexdigest()
            self._last_merkle_seal[norm_uri] = content_hash

            # 4. INSCRIBE IN THE LIBRARIAN
            # This populates the Iron Core's document store
            self.server.documents.open(params.text_document)

            # 5. [ASCENSION 11]: FORENSIC PROCLAMATION
            trace_id = f"gen-{uuid.uuid4().hex[:6].upper()}"
            forensic_log(f"Genesis: {fs_path.name} (v{version})", "SUCCESS", "SYNC", trace_id=trace_id)

            # 6. [ASCENSION 8]: DISPATCH INQUEST (PRIORITY ALPHA)
            # [THE CURE]: WE ONLY CALL THE INQUEST.
            # The Inquest engine handles the decision to delegate to Adrenaline or process locally.
            # Calling Adrenaline here creates a duplicate event loop (The Echo).
            self.server.foundry.submit(
                f"inq-open-{trace_id}",
                self.server.inquest.conduct, uri, text, version
            )

            # 7. [ASCENSION 5]: HAPTIC BLOOM
            self.server.endpoint.send_notification("gnostic/vfx", {
                "type": "bloom", "uri": uri, "intensity": 0.4
            })

    # =============================================================================
    # == RITE 2: THE MUTATION (DID CHANGE)                                       ==
    # =============================================================================

    def did_change(self, params: Any):
        """
        Surgically applies flux to the document buffer.
        """
        # Unwrap params if they are Pydantic models
        if hasattr(params, 'text_document'):
            uri = str(params.text_document.uri)
            version = params.text_document.version
            changes = params.content_changes
        else:
            # Dictionary fallback
            uri = params.get('textDocument', {}).get('uri')
            version = params.get('textDocument', {}).get('version')
            changes = params.get('contentChanges', [])

        norm_uri = UriUtils.normalize_uri(uri)

        with self._sync_lock:
            # [THE SURGICAL FIX]: AUTO-RESURRECTION
            # If the document is missing from memory, try to load it from disk JIT.
            if not self.server.documents.get(norm_uri):
                try:
                    fs_path = UriUtils.to_fs_path(uri)
                    if fs_path.exists():
                        content = fs_path.read_text(encoding='utf-8', errors='ignore')
                        # Force open the document so we can apply the change
                        self.server.documents.open({
                            "uri": uri,
                            "languageId": "scaffold",  # Default assumption
                            "version": version - 1,  # Assume we missed the previous state
                            "text": content
                        })
                except Exception:
                    # If we can't resurrect it, we can't patch it.
                    return

            # Proceed with standard update logic...
            self.server.documents.change(params)

            # Trigger analysis (The Inquest)
            doc = self.server.documents.get(norm_uri)
            if doc:
                self.server.foundry.submit(
                    f"inq-change-{version}",
                    self.server.inquest.conduct, uri, doc.text, version
                )

    # =============================================================================
    # == RITE 3: THE PERSISTENCE (DID SAVE)                                      ==
    # =============================================================================

    def did_save(self, params: Any):
        """Collapses the memory buffer into physical matter."""
        if isinstance(params, dict):
            params = DidSaveTextDocumentParams.model_validate(params)

        uri = str(params.text_document.uri)
        norm_uri = UriUtils.normalize_uri(uri)
        fs_path = self._path_registry.get(norm_uri)

        # [ASCENSION 1]: ANCHOR RECOVERY
        if not fs_path:
            fs_path = UriUtils.to_fs_path(uri).resolve()

        # [ASCENSION 9]: REALITY CONVERGENCE VOW
        # Force a hard Daemon analysis on save to ensure the Project Graph is absolute.
        if self.server._relay_active:
            self.server.foundry.submit(
                f"save-convergence-{uuid.uuid4().hex[:4]}",
                self.server._dispatch_to_daemon, "analyze", {
                    "file_path": str(fs_path),
                    "metadata": {"source": "LSP_SAVE_CONVERGENCE"}
                }
            )

        forensic_log(f"Persistence Sealed: {fs_path.name}", "SUCCESS", "SYNC")

    # =============================================================================
    # == RITE 4: THE OBLIVION (DID CLOSE)                                        ==
    # =============================================================================

    def did_close(self, params: Any):
        """Returns the scripture to the void."""
        if isinstance(params, dict):
            params = DidCloseTextDocumentParams.model_validate(params)

        uri = str(params.text_document.uri)
        norm_uri = UriUtils.normalize_uri(uri)

        with self._sync_lock:
            # [ASCENSION 12]: ATOMIC PURGE
            self.server.documents.close(uri)
            self.server.inquest.clear_file(uri)
            self._last_merkle_seal.pop(norm_uri, None)
            self._version_map.pop(norm_uri, None)
            self._path_registry.pop(norm_uri, None)

        # Banish markers from the UI
        self.server.diagnostics.clear(uri)
        forensic_log(f"Oblivion: {norm_uri.split('/')[-1]} dissolved.", "INFO", "SYNC")

    def clear(self):
        """Total purification of the synchronizer."""
        with self._sync_lock:
            self._last_merkle_seal.clear()
            self._version_map.clear()
            self._path_registry.clear()

# === SCRIPTURE SEALED: THE SYNCHRONIZER IS SOVEREIGN ===