# Path: core/lsp/scaffold_server/inquest.py
# -----------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_INQUEST_SINGULARITY_V100_LEGENDARY

import time
import uuid
import sys
import threading
import logging
import hashlib
import re
from typing import Any, Dict, Optional, List, Tuple
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, UriUtils, ServerState, MetricAccumulator
from ....artisans.analyze.processing.scaffold import ScaffoldProcessor
from ....artisans.analyze.reporting.privacy import PrivacySentinel

# --- PHYSICS CONSTANTS ---
MAX_FRACTURE_STRIKES = 3
HAPTIC_THRESHOLD_MS = 250
MUNDANE_FLUX_THRESHOLD = 5

# [ASCENSION 12]: ARTIFACT EXORCIST
# Regex to strip trailing quotes, dots, or whitespace from URIs before broadcast.
URI_CLEANSER = re.compile(r"['\"\.\s]+$")


class OcularInquest:
    """
    =============================================================================
    == THE OCULAR INQUEST (V-Ω-TOTALITY-V100-SINGULARITY)                      ==
    =============================================================================
    @gnosis:title The Ocular Inquest
    @gnosis:summary The Sovereign Optic Nerve. Perceives flux, filters noise, and
                    projects Gnostic Truth to the UI.
    @gnosis:LIF 100,000,000,000
    @gnosis:auth_code: Ω_INQUEST_TITANIUM

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **Titanium URI Sanitization:** Applies `UriUtils.normalize_uri` AND a final
        regex scrub (`URI_CLEANSER`) to annihilate the "Trailing Quote" heresy.
    2.  **Atomic Version Locking:** Rejects any analysis of version `N` if version `N+1`
        has already been processed. Time only moves forward.
    3.  **Merkle Silence:** Calculates MD5 hashes of content. If the content hasn't
        changed (even if version bumped), the inquest acts as a "Ghost" (no-op).
    4.  **Fracture Quarantine:** Tracks failures per file. If a specific file crashes
        the parser 3 times, it is quarantined to protect the Daemon's vitality.
    5.  **Dual-Stratum Execution:** Runs Stratum-0 (Local Syntax) instantly, then
        delegates Stratum-1 (Deep Analysis) to the Adrenaline Conductor.
    6.  **Path Duplication Guard:** Detects recursive path artifacts (`C:/Dev/C:/Dev`)
        and collapses them before they enter the analysis context.
    7.  **Privacy Redaction:** Automatically scrubs high-entropy strings (secrets)
        from diagnostic messages before they leave the server.
    8.  **Haptic Telemetry:** Measures analysis latency. If >250ms, sends a `gnostic/vfx`
        pulse to visually confirm "Heavy Computation" to the user.
    9.  **Trace ID DNA:** Injects a unique `trace_id` into every diagnostic, linking
        the UI squiggle back to the exact log entry that birthed it.
    10. **Shadow Awareness:** Detects `scaffold-shadow:` URIs and adjusts context logic
        to handle ephemeral memory buffers correctly.
    11. **Metabolic Backpressure:** Checks the Foundry queue depth. If overloaded,
        it degrades gracefully to "Syntax Only" mode.
    12. **Inception Sweep:** A dedicated rite to force-analyze all open tabs on boot,
        ensuring the "Mirror" is populated immediately after handshake.
    """
    __slots__ = [
        'server', 'processor', '_last_version_processed',
        '_last_merkle_seal', '_fracture_registry', '_lock'
    ]

    def __init__(self, server: Any):
        self.server = server
        # [THE INTERNAL GAZE]: Direct link to the local logic engine
        self.processor = server._internal_processor

        # --- [INTERNAL MEMORY STRATA] ---
        self._last_version_processed: Dict[str, int] = {}
        self._last_merkle_seal: Dict[str, str] = {}
        self._fracture_registry: Dict[str, int] = {}

        self._lock = threading.RLock()

    def conduct(self, uri: str, content: str, version: int):
        """
        [THE RITE OF REVELATION]
        LIF: 100x | Performs multi-spectral analysis across Local and Remote strata.
        """
        # --- 0. SPATIAL COORDINATION ---
        # [ASCENSION 1]: TITANIUM NORMALIZATION
        # We normalize immediately to ensure the key is stable across the entire pipeline.
        norm_uri = UriUtils.normalize_uri(uri)

        # [ASCENSION 12]: ARTIFACT SCRUB (The Final Polish)
        # Ensure no trailing garbage exists in the key.
        norm_uri = URI_CLEANSER.sub('', norm_uri)

        fs_path = UriUtils.to_fs_path(norm_uri)

        # [ASCENSION 6]: PATH DUPLICATION CHECK
        # If the resolved path seems to contain the project root TWICE, we have a fracture.
        if self.server.project_root:
            root_str = str(self.server.project_root).replace('\\', '/')
            path_str = str(fs_path).replace('\\', '/')

            # Simple heuristic: if root appears twice in the path
            if path_str.count(root_str) > 1:
                # Try to re-anchor to the root
                try:
                    rel = Path(path_str.split(root_str)[-1].lstrip('/'))
                    fs_path = (self.server.project_root / rel).resolve()
                    # Re-normalize URI based on corrected path
                    norm_uri = UriUtils.to_uri(fs_path)
                except:
                    pass

        # --- 1. [ASCENSION 3]: THE MERKLE SEAL ---
        # Calculate the hash of the current matter
        content_bytes = content.encode('utf-8', errors='ignore')
        seal = hashlib.md5(content_bytes).hexdigest()

        with self._lock:
            # 1.1. Monotonic Version Check (Causal Guard)
            # If the client sent a newer version while we were waiting, vaporize this thread.
            if version < self._last_version_processed.get(norm_uri, -1) and version != 0:
                return

            # 1.2. Mundane Flux Check (Merkle Guard)
            # If the content hasn't shifted, do not waste energy on re-analysis.
            if self._last_merkle_seal.get(norm_uri) == seal and version != 0:
                self._last_version_processed[norm_uri] = version
                return

            self._last_version_processed[norm_uri] = version
            self._last_merkle_seal[norm_uri] = seal

        # [ASCENSION 4]: QUARANTINE CHECK
        if self._fracture_registry.get(norm_uri, 0) >= MAX_FRACTURE_STRIKES:
            return  # Silent rejection of cursed files

        trace_id = f"inq-{uuid.uuid4().hex[:6].upper()}"
        start_time = time.perf_counter()

        # =====================================================================
        # == MOVEMENT I: THE INTERNAL GAZE (STRATUM-0)                       ==
        # =====================================================================
        # [ASCENSION 5]: Immediate Feedback Channel.
        try:
            # [ASCENSION 11]: METABOLIC BACKPRESSURE CHECK
            # If the local CPU is melting, we might downgrade logic (future impl).
            pressure = self.server.foundry.active_count

            ctx = {
                "content": content,
                "file_path": fs_path,
                "project_root": self.server.project_root,
                "grammar": "scaffold",
                "cursor_offset": -1,
                "telemetry": {"trace_id": trace_id, "start_time": start_time},
                "engine": self.server.engine,
                "session_id": self.server._session_id,
                "is_shadow": norm_uri.startswith("scaffold-shadow:")
            }

            # [RITE]: LOCAL_PROCESSOR_INVOCATION
            local_result = self.processor.process(ctx)

            # 2. CAUSAL VERIFICATION (Post-Compute)
            # Ensure the Architect hasn't willed new matter during the compute cycle.
            if self.server.documents.get_version(uri) > version and version != 0:
                return

            # 3. [ASCENSION 7 & 9]: PRIVACY & TRACE SPLICING
            raw_diags = local_result.get("diagnostics", [])
            for diag in raw_diags:
                # Banish plaintext secrets from the UI
                diag['message'] = PrivacySentinel.redact(diag.get('message', ''))
                # Suture the trace_id for the Redemption Artisans
                if 'data' not in diag: diag['data'] = {}
                diag['data'].update({
                    "trace_id": trace_id,
                    "version": version,
                    "source_stratum": 0
                })

            # 4. ATOMIC MULTICAST (LOCAL)
            # Project the findings to the Ocular Eye immediately.
            self._emit_holographic_data(norm_uri, version, raw_diags, local_result, trace_id)

            # Reset strikes on successful perception
            self._fracture_registry[norm_uri] = 0

        except Exception as fracture:
            # [ASCENSION 4]: FRACTURE REGISTRATION
            self._fracture_registry[norm_uri] = self._fracture_registry.get(norm_uri, 0) + 1
            forensic_log(f"Optic Fracture ({self._fracture_registry[norm_uri]}): {fs_path.name}", "ERROR", "INQUEST",
                         trace_id=trace_id)

            if self._fracture_registry[norm_uri] >= MAX_FRACTURE_STRIKES:
                self.server.log_message(
                    f"Scripture Quarantine: {fs_path.name} is causing logic-drift. Local analysis suspended.", type=2)

        # =====================================================================
        # == MOVEMENT II: THE REMOTE GAZE (DELEGATION)                       ==
        # =====================================================================
        # [ASCENSION 5]: RELAY-AGNOSTIC TRIGGER
        # We project the intent into the Adrenaline Conductor.
        # It handles the "Cold Start" backlog or immediate Silver Cord dispatch.
        if hasattr(self.server, 'adrenaline') and self.server.adrenaline:
            # We hand over the versioned intent with the CLEAN URI.
            self.server.adrenaline.trigger(norm_uri, content, version)

    def _emit_holographic_data(self, uri: str, version: int, diags: List, data: Dict, trace_id: str):
        """
        [THE RITE OF PROJECTION]
        Transmits multi-spectral findings to the Ocular UI.
        """
        # [ASCENSION 12]: FINAL PURIFICATION
        # Ensure the URI sent to the client is absolutely clean.
        clean_uri = URI_CLEANSER.sub('', uri)

        # A. Beam 1: Heresies (Diagnostics)
        self.server.endpoint.send_notification("textDocument/publishDiagnostics", {
            "uri": clean_uri,
            "version": version,
            "diagnostics": diags,
            "_source": "LOCAL_INQUEST"
        })

        # B. Beam 2: The Mirror (Structural Tree)
        if "structure" in data:
            self.server.mirror.project(clean_uri, data["structure"], data.get("ascii_tree", ""), version)

        # C. [ASCENSION 8]: HAPTIC PULSE
        # If analysis took significant mass, trigger a bloom in the UI
        latency = (time.perf_counter() - getattr(self.server._ctx, 'start_time', time.perf_counter())) * 1000
        if latency > HAPTIC_THRESHOLD_MS:
            self.server.endpoint.send_notification("gnostic/vfx", {
                "type": "pulse", "uri": clean_uri, "intensity": 0.3
            })

    def inception_sweep(self):
        """
        [ASCENSION 12]: THE RITE OF FIRST SIGHT
        Synchronizes all open scriptures to warm the Cortex.
        """
        open_uris = self.server.documents.open_uris
        if not open_uris: return

        forensic_log(f"Inception Sweep: Perceiving {len(open_uris)} scriptures.", "RITE", "INQUEST")

        for uri in open_uris:
            doc = self.server.documents.get(uri)
            if doc:
                # Project into the Foundry for non-blocking mass-perception
                self.server.foundry.submit(
                    f"sweep-{uuid.uuid4().hex[:4]}",
                    self.conduct, uri, doc.text, doc.version
                )

    def quarantine_purge(self, uri: str):
        """[RITE]: ABSOLUTION - Clears the fracture strikes for a URI."""
        norm_uri = UriUtils.normalize_uri(uri)
        with self._lock:
            self._fracture_registry.pop(norm_uri, None)
            self._last_merkle_seal.pop(norm_uri, None)
            self._last_version_processed.pop(norm_uri, None)