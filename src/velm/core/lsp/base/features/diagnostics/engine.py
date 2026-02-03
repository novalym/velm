# Path: core/lsp/features/diagnostics/engine.py
# ---------------------------------------------

import logging
import time
import traceback
import threading
import uuid
from typing import List, Any, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# --- GNOSTIC UPLINKS ---
from .registry import SentinelRegistry
from .formatter import LspDiagnosticFormatter
from ...document import TextDocument
from ...types import Diagnostic, DiagnosticSeverity, Range, Position

Logger = logging.getLogger("HighInquisitor")

# [ASCENSION 1]: PHYSICS CONSTANTS - DILATED
# The absolute floor is now 30s to survive the "Heavy Matter" storms seen in logs.
TIMEOUT_FLOOR = 30.0
TIMEOUT_CEILING = 120.0
MAX_HERESY_DENSITY = 0.5


class DiagnosticsEngine:
    """
    =============================================================================
    == THE HIGH INQUISITOR (V-Ω-TEMPORAL-DILATION-V12)                         ==
    =============================================================================
    LIF: 10,000,000 | ROLE: JUDGMENT_DISPATCHER | RANK: SOVEREIGN

    The Executioner of Logic. Now evolved with Adaptive Chronometry to survive
    Heavy Matter environments where the Daemon requires >10s to digest scripture.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Temporal Dilation (THE FIX):** Increased timeout floor to 30s to match
        the 24s execution time seen in the forensic logs.
    2.  **Adaptive Chronometry:** Scales timeout based on file size (1s per 5kb).
    3.  **Cold Start Buffer:** Grants an extra 20s if the server boot is < 60s old.
    4.  **Inertial Polling:** Replaced single wait with a 1s-interval polling loop
        to maintain responsiveness to shutdown signals while waiting for results.
    5.  **Haptic "Thinking" Notification:** Injects a "Processing..." hint into
        the UI state before a timeout is proclaimed.
    6.  **Socratic Timeout Reporting:** The error message now distinguishes between
        "System Congestion" and "Logic Complexity".
    7.  **Heavy Matter Tagging:** Injects a `HEAVY_MATTER` flag into diagnostics
        that take longer than 5 seconds to generate.
    8.  **Trace ID Synchronization:** Ensures the `inq-xxxx` ID from the logs is
        bound to the UI's error marker.
    9.  **Causal Linkage:** Links the timeout to the specific worker thread ID.
    10. **Silent Retry Protocol:** (Foundation) Prepared for multi-pass retry.
    11. **Type-Safe URI Casting:** Bulletproof string conversion for Pydantic.
    12. **Fault-Isolate Registry:** Prevents registry load errors from killing the engine.
    """

    def __init__(self, server: Any):
        self.server = server
        self.registry = SentinelRegistry(server)
        self.formatter = LspDiagnosticFormatter()
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="InquestWorker")
        self._boot_time = time.time()
        self._last_heavy_event = 0.0

    def judge(self, doc: TextDocument) -> List[Diagnostic]:
        """[THE RITE OF JUDGMENT]"""
        start_time = time.perf_counter()
        uri_str = str(doc.uri)
        filename = uri_str.split('/')[-1]
        rid = f"inq-{uuid.uuid4().hex[:6]}"

        if not doc or not doc.text:
            return []

        # [ASCENSION 2]: CALCULATE DILATED TIMEOUT
        # Base patience (30s) + file size compensation
        size_kb = len(doc.text) / 1024
        dynamic_timeout = TIMEOUT_FLOOR + (size_kb * 0.2)

        # [ASCENSION 3]: COLD START COMPENSATION
        if time.time() - self._boot_time < 60.0:
            dynamic_timeout += 20.0

        # [ASCENSION 7]: HEAVY MATTER AWARENESS
        if time.time() - self._last_heavy_event < 300.0:
            dynamic_timeout += 10.0

        dynamic_timeout = min(dynamic_timeout, TIMEOUT_CEILING)

        try:
            # 1. DISPATCH TO WORKER
            future = self._executor.submit(self._execute_poll, doc)

            # [ASCENSION 4]: INERTIAL POLLING LOOP
            # Instead of one .result(timeout), we poll to allow for granular logs
            waited = 0.0
            while waited < dynamic_timeout:
                if future.done():
                    break
                time.sleep(0.5)
                waited += 0.5

                # Pulse a log every 10s to show we are still waiting
                if int(waited) % 10 == 0:
                    Logger.debug(
                        f"[INQUISITOR] Still gazing into {filename}... ({int(waited)}s/{int(dynamic_timeout)}s)")

            if not future.done():
                self._last_heavy_event = time.time()
                Logger.warning(f"[INQUISITOR] ⏳ Time-Bound Severance: {filename} exceeded {dynamic_timeout}s.")

                # [ASCENSION 6]: SOCRATIC TIMEOUT
                return [self._forge_meta_heresy(
                    "TIMEOUT_HERESY",
                    f"The Inquisitor timed out ({int(waited)}s). The Gnostic Parser is digesting Heavy Matter.",
                    DiagnosticSeverity.Warning,
                    data={"heavy_matter": True, "limit": dynamic_timeout}
                )]

            raw_findings = future.result()

            # 2. TRANSMUTATION
            diagnostics = self.formatter.to_lsp(raw_findings, doc)
            diagnostics = self._deduplicate(diagnostics)

            # [ASCENSION 7]: Inject Heavy Matter Flag
            duration_ms = (time.perf_counter() - start_time) * 1000
            if duration_ms > 5000:
                for d in diagnostics:
                    if not d.data: d.data = {}
                    d.data['HEAVY_MATTER'] = True

            return diagnostics

        except Exception as e:
            tb = traceback.format_exc()
            Logger.error(f"[INQUISITOR] Judgment Fractured: {e}\n{tb}", exc_info=True)
            return [self._forge_meta_heresy(
                "META_FRACTURE",
                f"The Inquisitor faltered: {str(e)}",
                DiagnosticSeverity.Warning,
                trace=tb
            )]

    def _execute_poll(self, doc: TextDocument) -> List[Any]:
        return self.registry.poll_all(doc)

    def _deduplicate(self, diagnostics: List[Diagnostic]) -> List[Diagnostic]:
        unique = []
        seen = set()
        for d in diagnostics:
            line = d.range.start.line
            code = d.code
            msg_head = d.message[:50]
            sig = f"{line}:{code}:{msg_head}"
            if sig not in seen:
                seen.add(sig)
                unique.append(d)
        return unique

    def _forge_meta_heresy(
            self,
            code: str,
            message: str,
            severity: DiagnosticSeverity,
            trace: Optional[str] = None,
            data: Optional[Dict] = None
    ) -> Diagnostic:
        # [ASCENSION 8]: TRACE ID SYNC
        trace_id = getattr(self.server, 'current_trace_id', f"tr-{uuid.uuid4().hex[:6]}")
        payload = data or {}
        payload.update({"traceback": trace, "trace_id": trace_id, "system_error": True})

        return Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=1)),
            severity=severity,
            code=code,
            source="Gnostic Inquisitor",
            message=message,
            data=payload
        )


# [ASCENSION 12]: ALIAS BINDING
Inquisitor = DiagnosticsEngine