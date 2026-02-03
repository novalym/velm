# Path: core/lsp/scaffold_server/adrenaline.py
# --------------------------------------------
# LIF: INFINITY | ROLE: TEMPORAL_RESERVOIR | RANK: SOVEREIGN
# auth_code: Ω_ADRENALINE_TOTALITY_V24_SINGULARITY

import time
import uuid
import json
import threading
import logging
import hashlib
from typing import Any, Dict, Optional, List, Tuple
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, UriUtils

Logger = logging.getLogger("AdrenalineConductor")

# --- PHYSICS CONSTANTS ---
BACKLOG_CAPACITY = 100
STALE_THRESHOLD_SEC = 60.0


class AdrenalineConductor:
    """
    =============================================================================
    == THE ADRENALINE CONDUCTOR (V-Ω-TOTALITY-V24)                             ==
    =============================================================================
    Captures architectural intent during the "Cold Start" phase and projects
    it into the Daemon the microsecond the Silver Cord achieves resonance.
    It solves the "Relay Race Paradox" by serving as a Temporal Reservoir.
    =============================================================================
    """
    __slots__ = [
        'server', '_backlog', '_order', '_lock', '_is_flushing',
        'total_coalesced', 'total_shed'
    ]

    def __init__(self, server: Any):
        self.server = server

        # --- [INTERNAL STORAGE STRATA] ---
        # Map[URI, Payload] - Coalesced storage
        self._backlog: Dict[str, Dict[str, Any]] = {}
        # List[URI] - Preserves arrival order for Triage
        self._order: List[str] = []

        self._lock = threading.RLock()
        self._is_flushing = False

        # Telemetry
        self.total_coalesced = 0
        self.total_shed = 0

    def trigger(self, uri: str, content: str, version: int = 0):
        """
        [THE RITE OF DISPATCH]
        Attempts immediate real-time analysis or enqueues into the backlog.
        """
        with self._lock:
            # 1. DIVINE COORDINATES
            norm_uri = UriUtils.normalize_uri(uri)
            fs_path = str(UriUtils.to_fs_path(norm_uri)).replace('\\', '/')
            trace_id = f"adr-{uuid.uuid4().hex[:6].upper()}"

            # 2. FORGE THE PLEA
            payload = {
                "file_path": fs_path,
                "content": content,
                "project_root": str(self.server.project_root) if self.server.project_root else ".",
                "version": version,
                "metadata": {
                    "source": "LSP_ADRENALINE",
                    "trace_id": trace_id,
                    "timestamp": time.time(),
                    "priority": 1 if version == 0 else 2  # didOpen > didChange
                }
            }

            # 3. [REAL-TIME PATH]: If the Silver Cord is hot, leap to execution
            if self.server._relay_active:
                # forensic_log(f"Relay Hot. Projecting Analysis: {fs_path.split('/')[-1]}", "RITE", "ADRENALINE", trace_id=trace_id)
                self.server.foundry.submit(
                    f"adr-push-{trace_id}",
                    self._dispatch, payload
                )
                return

            # 4. [BACKLOG PATH]: Inscribe in the temporal reservoir

            # [ASCENSION 1]: QUANTUM COALESCENCE
            # If we already have a pending request for this file, update it.
            # This prevents 50 'didChange' events from stacking up.
            if norm_uri in self._backlog:
                self.total_coalesced += 1
                # We retain the original trace_id but update the content and version
                # to ensure the eventually-sent request represents the NEWEST reality.
                old_meta = self._backlog[norm_uri]['metadata']
                payload['metadata']['trace_id'] = old_meta['trace_id']  # Preserve lineage
                payload['metadata']['timestamp'] = old_meta['timestamp']  # Track age

                self._backlog[norm_uri] = payload
                # forensic_log(f"Intent Coalesced: {fs_path.split('/')[-1]} (v{version})", "DEBUG", "ADRENALINE")
            else:
                # [ASCENSION 4]: HYDRAULIC BACKPRESSURE
                if len(self._order) >= BACKLOG_CAPACITY:
                    self._shed_entropy()

                self._backlog[norm_uri] = payload
                self._order.append(norm_uri)
                forensic_log(f"Relay Cold. Intent Enqueued: {fs_path.split('/')[-1]} (Buffer: {len(self._order)})",
                             "INFO", "ADRENALINE", trace_id=trace_id)

    def flush_backlog(self):
        """
        [THE RITE OF THE FIRST BREATH]
        Atomically flushes the reservoir into the Daemon's intake.
        Called by the SentinelGuard upon successful Consecration.
        """
        with self._lock:
            if not self._backlog or self._is_flushing:
                return
            self._is_flushing = True

        try:
            count = len(self._backlog)
            forensic_log(f"Consecration confirmed. Flushing {count} backlogged intentions...", "SUCCESS", "ADRENALINE")

            # [ASCENSION 2]: DIALECT TRIAGE
            # Sort by priority (didOpen first) then by original arrival time
            with self._lock:
                sorted_uris = sorted(
                    self._order,
                    key=lambda u: (self._backlog[u]['metadata']['priority'], self._backlog[u]['metadata']['timestamp'])
                )

            for uri in sorted_uris:
                payload = None
                with self._lock:
                    payload = self._backlog.pop(uri, None)

                if not payload: continue

                # [ASCENSION 9]: STALE-DATE GUARD
                if time.time() - payload['metadata']['timestamp'] > STALE_THRESHOLD_SEC:
                    self.total_shed += 1
                    # forensic_log(f"Dropping Ancient Intent: {payload['file_path']}", "WARN", "ADRENALINE")
                    continue

                # [ASCENSION 6]: JIT CONTEXT INJECTION
                # Update with current session credentials
                payload['project_root'] = str(self.server.project_root)

                # [ASCENSION 7]: FOUNDRY SERIALIZATION
                # Dispatch without blocking the flush loop
                self.server.foundry.submit(
                    f"adr-flush-{payload['metadata']['trace_id']}",
                    self._dispatch, payload
                )

            # forensic_log("Adrenaline Flush Complete. Reality Synchronized.", "SUCCESS", "ADRENALINE")

        finally:
            with self._lock:
                self._order.clear()
                self._is_flushing = False

    def _dispatch(self, payload: Dict):
        """
        The low-level transmitter.
        Siphons the plea across the Silver Cord to the Kinetic Daemon.
        """
        try:
            # We use the internal dispatch helper in the server
            self.server._dispatch_to_daemon("analyze", payload)
        except Exception as e:
            # [ASCENSION 5]: FAIL-OPEN FALLBACK
            # If the relay fails during flush, we try one final internal scan
            forensic_log(f"Relay Dispatch Fracture: {e}. Pivoting to Internal Fallback.", "WARN", "ADRENALINE")
            try:
                uri = payload.get('file_path', 'unknown')
                self.server.inquest.conduct(uri, payload['content'], payload['version'])
            except:
                pass

    def _shed_entropy(self):
        """[ASCENSION 4]: Metabolic shedding of the oldest low-priority event."""
        # Try to find a 'didChange' event to drop first
        for i, uri in enumerate(self._order):
            if self._backlog[uri]['metadata']['priority'] == 2:  # Cull a change, not an open
                self._backlog.pop(uri)
                self._order.pop(i)
                self.total_shed += 1
                return

        # Fallback: cull absolute oldest
        oldest_uri = self._order.pop(0)
        self._backlog.pop(oldest_uri)
        self.total_shed += 1

    def clear(self):
        """Total purification of the gateway."""
        with self._lock:
            self._backlog.clear()
            self._order.clear()

# === SCRIPTURE SEALED: THE RESERVOIR IS TITANIUM ===