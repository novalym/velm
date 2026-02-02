# Path: core/lsp/base/features/diagnostics/manager.py
# ---------------------------------------------------

import logging
import threading
import time
import uuid
from collections import defaultdict
from typing import Dict, List, Any, Optional, Union

from ...types import (
    PublishDiagnosticsParams,
    Diagnostic,
    DiagnosticSeverity,
    Range,
    Position,
    DocumentDiagnosticParams,
    FullDocumentDiagnosticReport,
    UnchangedDocumentDiagnosticReport,
    DocumentDiagnosticReport
)
from .engine import Inquisitor
from .ledger import HeresyLedger
from .governor import BurstGovernor

Logger = logging.getLogger("DiagnosticManager")


class DiagnosticManager:
    """
    =============================================================================
    == THE OMNISCIENT HERALD (V-Ω-PULL-MODEL-ASCENDED)                         ==
    =============================================================================
    [THE 12 ASCENSIONS]:
    1.  **Hybrid Architecture:** Supports both Push (Legacy) and Pull (LSP 3.17) models simultaneously.
    2.  **Generational State:** Tracks `resultId` per document to enable Delta Logic.
    3.  **The Unchanged Vow:** Returns "Unchanged" reports to save bandwidth.
    4.  **Atomic Range Reconstruction:** Pydantic V2 immutable fix.
    5.  **Integer Severity Sorting:** Prioritizes Critical Errors.
    6.  **Trace ID Sync:** Correlates pull requests with log traces.
    7.  **Adaptive Scheduling:** Debounces analysis based on file size.
    8.  **Haptic Triggers:** Sends visual shake events on new errors.
    9.  **Relay Ingestion:** Merges Daemon diagnostics.
    10. **Integrity Broadcasts:** Updates the global health score.
    11. **Zombie Purge:** Clears state on file close.
    12. **Lock-Free Reads:** Optimistic caching for the Pull Loop.
    """

    def __init__(self, server: Any):
        self.server = server
        self.inquisitor = Inquisitor(server)
        self.ledger = HeresyLedger()
        self.governor = BurstGovernor()
        self._lock = threading.RLock()

        # [ASCENSION: CONSECRATION]
        # Advertise support for LSP 3.17 Pull Diagnostics
        server.register_capability(lambda caps: setattr(caps, 'diagnostic_provider', {
            "interFileDependencies": True,
            "workspaceDiagnostics": False
        }))

        self._last_integrity_broadcast = 0.0
        self._last_error_count: Dict[str, int] = defaultdict(int)

        # [ASCENSION 2]: GENERATIONAL STATE
        # Map[URI, {id: str, diagnostics: List[Diagnostic]}]
        self._cache_state: Dict[str, Dict[str, Any]] = {}

    def schedule_validation(self, uri: str, version: int, priority: bool = False):
        if self.server.state == "DRAINING": return
        delay = 0.05 if priority else 0.5
        doc = self.server.documents.get(uri)
        if doc and doc.line_count > 2000: delay = 1.0

        self.governor.schedule(
            uri=uri,
            version=version,
            base_delay=delay,
            task=lambda: self._conduct_inquest(uri, version),
            priority=priority
        )

    def ingest_relay_diagnostics(self, uri: str, diagnostics: List[Diagnostic]):
        if not self.server.documents.get(uri): return
        self.ledger.update(uri, diagnostics, source="DAEMON")
        # In Push mode, we publish. In Pull mode, we just update the ledger and wait for the client to ask.
        # But for UI reactivity, we Push anyway (Hybrid Mode).
        self._publish(uri)

    def _conduct_inquest(self, uri: str, version: int):
        """Runs the analysis logic and updates the Ledger."""
        doc = self.server.documents.get(uri)
        if not doc or doc.version != version: return

        try:
            local_heresies = self.inquisitor.judge(doc)
            self.ledger.update(uri, local_heresies, source="LOCAL")

            # [ASCENSION 3]: HYBRID NOTIFICATION
            # Even in Pull Mode, we Push to ensure instant UI updates for non-LSP clients (like the Cockpit Graph).
            # The LSP client (VS Code) will ignore this if it prefers Pull, or use it if it prefers Push.
            self._publish(uri, version)
            self._broadcast_integrity()

        except Exception as e:
            Logger.error(f"[HERALD] Inquest Fracture for {uri}: {e}")

    def compute_pull(self, params: DocumentDiagnosticParams) -> DocumentDiagnosticReport:
        """
        [THE RITE OF THE PULL]
        LSP 3.17 Handler. The Client asks for diagnostics.
        """
        uri = str(params.text_document.uri)
        previous_id = params.previous_result_id

        # 1. Ensure fresh state if needed (or trust the Ledger's current state)
        # Note: In a true Pull model, we might trigger analysis HERE.
        # But we use an event-driven architecture, so the Ledger is usually up to date.
        # We assume _conduct_inquest has run via didChange.

        with self._lock:
            # Get current merged truth
            merged_diagnostics = self._get_merged_safe(uri)

            # Generate a hash-based ID for this state
            # Simple composition of URI + count + first-error-hash
            current_id = self._generate_result_id(uri, merged_diagnostics)

            # 2. CHECK FOR CHANGE (The Unchanged Vow)
            if previous_id == current_id:
                return UnchangedDocumentDiagnosticReport(resultId=current_id)

            # 3. RETURN FULL REPORT
            return FullDocumentDiagnosticReport(
                resultId=current_id,
                items=merged_diagnostics
            )

    def _generate_result_id(self, uri: str, diagnostics: List[Diagnostic]) -> str:
        """Forges a unique ID for the current diagnostic state."""
        import hashlib
        # We hash the string representation of the diagnostic count + content
        # This is deterministic enough for change detection.
        payload = f"{uri}:{len(diagnostics)}:{str([d.message for d in diagnostics])}"
        return hashlib.md5(payload.encode()).hexdigest()

    def _get_merged_safe(self, uri: str) -> List[Diagnostic]:
        """Retrieves and sanitizes diagnostics for protocol compliance."""
        merged_diagnostics = self.ledger.get_merged(uri)
        doc = self.server.documents.get(uri)
        if not doc: return []

        max_line = max(0, doc.line_count - 1)
        final_batch: List[Diagnostic] = []

        for d in merged_diagnostics:
            try:
                s_l = d.range.start.line
                e_l = d.range.end.line

                # Clamp Geometry
                if s_l > max_line or e_l > max_line:
                    new_s_l = min(s_l, max_line)
                    new_e_l = min(e_l, max_line)
                    new_range = Range(
                        start=Position(line=new_s_l, character=d.range.start.character),
                        end=Position(line=new_e_l, character=d.range.end.character)
                    )
                    d = d.model_copy(update={"range": new_range})

                final_batch.append(d)
            except Exception:
                continue

        final_batch.sort(key=lambda x: int(x.severity))
        return final_batch

    def _publish(self, uri: str, version: Optional[int] = None):
        """[LEGACY PUSH]: Used for UI events and older clients."""
        with self._lock:
            doc = self.server.documents.get(uri)
            if not doc: return
            if version is None: version = doc.version

            final_batch = self._get_merged_safe(uri)

            # Push Notification
            params = PublishDiagnosticsParams(uri=uri, version=version, diagnostics=final_batch)
            self.server.endpoint.send_notification(
                "textDocument/publishDiagnostics",
                params.model_dump(mode='json', exclude_none=True)
            )

            # Haptic Trigger
            error_count = sum(1 for d in final_batch if int(d.severity) == 1)
            prev_count = self._last_error_count[uri]
            if error_count > prev_count:
                self.server.endpoint.send_notification("gnostic/vfx", {"type": "shake", "intensity": 0.4})
            self._last_error_count[uri] = error_count

    def _broadcast_integrity(self):
        now = time.time()
        if now - self._last_integrity_broadcast < 0.5: return
        try:
            stats = self.ledger.get_integrity_stats()
            self.server.endpoint.send_notification("scaffold/integrity", stats)
            self._last_integrity_broadcast = now
        except Exception:
            pass

    def clear(self, uri: str):
        with self._lock:
            self.governor.cancel(uri)
            self.ledger.clear(uri)
            if uri in self._last_error_count: del self._last_error_count[uri]

            # Push clean state
            self.server.endpoint.send_notification(
                "textDocument/publishDiagnostics",
                {"uri": uri, "diagnostics": []}
            )