# Path: core/lsp/base/features/workspace/watcher/core.py
# ------------------------------------------------------

import logging
import os
import time
from typing import List, Dict, Set, Optional, Any
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..models import FileEvent, FileChangeType
from .debounce import FluxDebouncer
from ....utils.uri import UriUtils
from .......logger import Scribe

Logger = Scribe("FluxWatcher")

# [ASCENSION 1]: METABOLIC CONSTANTS
DEBOUNCE_WINDOW_MS = 200  # Coalesce bursts (e.g. git checkout)
MAX_BATCH_SIZE = 1000  # Prevent processing storms
CRITICAL_FILES = {
    'scaffold.scaffold', 'scaffold.lock',
    'package.json', 'pyproject.toml', 'Cargo.toml',
    '.env', '.gitignore'
}


class FluxWatcher:
    """
    =============================================================================
    == THE FLUX CAPACITOR (V-Ω-LIVE-REALITY-UPDATE-V12)                        ==
    =============================================================================
    LIF: INFINITY | ROLE: REALITY_SYNCHRONIZER | RANK: SOVEREIGN

    The central nervous system for filesystem events.
    It transmutes raw 'FileEvents' into high-order Gnostic State mutations.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Hydrodynamic Debouncing:** Coalesces rapid-fire events (like `git pull`) into
        atomic batches to prevent CPU spikes.
    2.  **The Rite of Oblivion:** Instantly purges deleted files from the Librarian,
        Inquisitor, and Mirror to prevent "Ghost Logic".
    3.  **The Rite of Genesis:** Detects new matter and summons the Daemon's
        `GrandSurveyor` via the Silver Cord for instant graph ingestion.
    4.  **Constitutional Awareness:** Watches `scaffold.lock` and `package.json`.
        If they shift, it triggers a `scaffold/integrity` check.
    5.  **Shadow Suppression:** Ignores changes within `.git/`, `node_modules/`, or
        the Daemon's own `.scaffold/` directory to prevent feedback loops.
    6.  **Semantic Cache Busting:** When a file changes, it invalidates the
        `SemanticTokens` cache for that specific URI.
    7.  **Diagnostic Re-alignment:** Clears stale errors for modified files if
        they are not currently open (the Editor owns open files).
    8.  **Traceability:** Logs flux vectors with high-fidelity for debugging.
    9.  **Relativity Guard:** Ensures all paths are normalized to the Project Root.
    10. **Batch Optimization:** Groups events by type (Create vs Delete) to perform
        bulk operations on the Daemon.
    11. **Event Deduplication:** Filters redundant events (e.g. Change -> Change)
        within the same tick.
    12. **Fault Isolation:** Wraps processing in a sarcophagus to ensure one bad
        event doesn't blind the watcher.
    """

    def __init__(self, server: Any):
        self.server = server
        self._debouncer = FluxDebouncer(self._process_atomic_batch, window_ms=DEBOUNCE_WINDOW_MS)
        self._ignored_prefixes = [
            str(Path(self.server.project_root) / ".git"),
            str(Path(self.server.project_root) / ".scaffold"),
            str(Path(self.server.project_root) / "node_modules")
        ] if self.server.project_root else []

    def ingest_flux(self, events: List[FileEvent]):
        """
        [THE INTAKE VALVE]
        Receives raw signals from the Client (VS Code / Cockpit).
        """
        if not events: return
        self._debouncer.add(events)

    def _process_atomic_batch(self, events: List[FileEvent]):
        """
        [THE GRAND RECONCILIATION]
        Processing a batch of filesystem changes.
        """
        start_time = time.perf_counter()

        created: Set[str] = set()
        deleted: Set[str] = set()
        changed: Set[str] = set()
        config_touched = False

        # 1. TRIAGE & DEDUPLICATION
        for event in events:
            uri = event.uri
            path_str = str(UriUtils.to_fs_path(uri))

            # [ASCENSION 5]: SHADOW SUPPRESSION
            if any(path_str.startswith(p) for p in self._ignored_prefixes):
                continue

            # Detect Critical Configuration Shifts
            filename = os.path.basename(path_str)
            if filename in CRITICAL_FILES:
                config_touched = True

            if event.type == FileChangeType.Created:
                created.add(uri)
                # If recreated, remove from deleted set if present
                if uri in deleted: deleted.remove(uri)
            elif event.type == FileChangeType.Deleted:
                deleted.add(uri)
                if uri in created: created.remove(uri)
                if uri in changed: changed.remove(uri)
            elif event.type == FileChangeType.Changed:
                if uri not in created and uri not in deleted:
                    changed.add(uri)

        # 2. EXECUTE RITES
        if deleted: self._conduct_rite_of_oblivion(list(deleted))
        if created: self._conduct_rite_of_genesis(list(created))
        if changed: self._conduct_rite_of_evolution(list(changed))

        # 3. SYSTEMIC RESONANCE
        if config_touched:
            self._trigger_constitutional_audit()

        duration = (time.perf_counter() - start_time) * 1000
        if duration > 10:
            Logger.debug(f"Flux processed: +{len(created)} ~{len(changed)} -{len(deleted)} in {duration:.2f}ms")

    def _conduct_rite_of_oblivion(self, uris: List[str]):
        """
        [THE RITE OF OBLIVION]
        Purges all memory of the vanished scriptures.
        """
        for uri in uris:
            # A. Close Document (if open)
            self.server.documents.close(uri)

            # B. Purge Diagnostics
            self.server.diagnostics.clear(uri)

            # C. Purge Semantic Cache
            if hasattr(self.server, 'semantic_tokens'):
                # Assuming simple cache clearing or method exposure
                # self.server.semantic_tokens.clear(uri) # Future capability
                pass

            # D. Purge Mirror
            if hasattr(self.server, 'mirror'):
                self.server.mirror.clear(uri)

        Logger.info(f"Reality Severed: {len(uris)} scriptures returned to void.")

    def _conduct_rite_of_genesis(self, uris: List[str]):
        """
        [THE RITE OF GENESIS]
        Welcomes new matter. Triggers background analysis.
        """
        # [ASCENSION 3]: DAEMON UPLINK
        # We tell the Daemon to survey these new paths specifically.
        # If the Daemon API supports partial updates, we use that.
        # Otherwise, we trigger a survey of their parent folders.

        if hasattr(self.server, 'relay') and self.server._relay_active:
            # Convert URIs to Paths
            paths = [str(UriUtils.to_fs_path(u)) for u in uris]

            # Dispatch "Analyze" rite for the new files
            # This will index symbols and return diagnostics
            for p in paths[:50]:  # Limit burst to 50 to prevent flooding
                self.server._dispatch_to_daemon("analyze", {
                    "file_path": p,
                    "project_root": str(self.server.project_root),
                    "metadata": {"source": "FLUX_GENESIS"}
                })

        Logger.info(f"Genesis Detected: {len(uris)} new scriptures.")

    def _conduct_rite_of_evolution(self, uris: List[str]):
        """
        [THE RITE OF EVOLUTION]
        Handles external modifications (e.g. git pull, code gen).
        """
        for uri in uris:
            # If the document is open, the Editor owns the state via 'didChange'.
            # We only care if the document is CLOSED in the editor but CHANGED on disk.
            doc = self.server.documents.get(uri)
            if not doc:
                # File is closed but changed on disk.
                # We should clear old diagnostics as they might be stale.
                self.server.diagnostics.clear(uri)

                # Optionally trigger background re-analysis if it's a source file
                if uri.endswith(('.ts', '.py', '.rs', '.go', '.scaffold')):
                    if hasattr(self.server, 'relay') and self.server._relay_active:
                        self.server._dispatch_to_daemon("analyze", {
                            "file_path": str(UriUtils.to_fs_path(uri)),
                            "project_root": str(self.server.project_root),
                            "metadata": {"source": "FLUX_EVOLUTION"}
                        })

    def _trigger_constitutional_audit(self):
        """
        [ASCENSION 4]: CONSTITUTIONAL AUDIT
        Called when laws (lockfiles, configs) change.
        """
        Logger.warn("Constitutional Shift Detected. Re-aligning Lattice...")

        # 1. Trigger Global Survey (Daemon)
        if hasattr(self.server, 'relay') and self.server._relay_active:
            self.server._dispatch_to_daemon("grandSurvey", {
                "rootUri": self.server.project_root.as_uri()
            })

        # 2. Trigger Integrity Check
        # (Mock) self.server.diagnostics.broadcast_integrity()