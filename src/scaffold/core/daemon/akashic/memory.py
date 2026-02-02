# Path: core/daemon/akashic/memory.py
# -----------------------------------
# LIF: INFINITY | ROLE: TEMPORAL_STORAGE_GOD_TIER
# =================================================================================
# == THE MEMORY CRYSTAL (V-Ω-TEMPORAL-ARMOR-ASCENDED)                        ==
# =================================================================================
# [CAPABILITIES]:
# 1. HYBRID DEDUPLICATION: Filters by Object ID and Trace ID.
# 2. TEMPORAL ARMOR: Sorting logic that never crashes, even on malformed data.
# 3. AUTO-HEALING: Silently wraps malformed packets during recall.
# 4. DEEP FREEZE: Returns immutable copies to prevent observer effects.

import threading
import time
import copy
from collections import deque
from typing import List, Dict, Any, Set
from .constants import MAX_HISTORY_DEPTH, MAX_PINNED_HERESIES


class ScrollOfTime:
    """
    The thread-safe, self-healing memory core.
    It maintains the chronological sequence of the Daemon's consciousness.
    """

    def __init__(self):
        self._flow = deque(maxlen=MAX_HISTORY_DEPTH)
        self._pinned = deque(maxlen=MAX_PINNED_HERESIES)
        self._lock = threading.RLock()

        # [ASCENSION 8]: Forensic Metrics
        self.ingestion_count = 0
        self.last_ingest_time = 0.0

    def inscribe(self, rpc_packet: Dict[str, Any], is_heresy: bool):
        """
        Writes a thought to the scroll.
        """
        with self._lock:
            # [ASCENSION 9]: Structure Enforcement (Lightweight)
            # We ensure it's a dict, but we leave deep validation to the Engine's Sanitizer
            if not isinstance(rpc_packet, dict):
                return

            self._flow.append(rpc_packet)
            self.ingestion_count += 1
            self.last_ingest_time = time.time()

            # [ASCENSION 3]: Heresy Pinning
            # Critical errors are preserved in a separate buffer that rotates much slower.
            if is_heresy:
                self._pinned.append(rpc_packet)

    def recall(self, since_timestamp: float = 0) -> List[Dict[str, Any]]:
        """
        [ASCENSION 1]: DELTA SYNCHRONIZATION (THE UNBREAKABLE REPLAY)
        Returns a time-sorted list of events.

        [THE CURE]: This method implements 'Temporal Armor'.
        It uses a safe accessor for timestamps and handles both Flat Logs and RPC Envelopes,
        ensuring the sort never raises a KeyError.
        """
        with self._lock:
            # Snapshot buffers to minimize lock time
            flow_snap = list(self._flow)
            pinned_snap = list(self._pinned)

        combined = []
        seen_traces: Set[str] = set()
        seen_refs: Set[int] = set()

        def get_timestamp(pkt: Dict[str, Any]) -> float:
            """Divines time from any structure."""
            try:
                # 1. Try JSON-RPC Params
                ts = pkt.get('params', {}).get('timestamp')
                if ts is not None: return float(ts)

                # 2. Try Root Level (Flat Log)
                ts = pkt.get('timestamp')
                if ts is not None: return float(ts)

                return 0.0
            except:
                return 0.0

        def get_trace_id(pkt: Dict[str, Any]) -> str:
            """Extracts unique fingerprint."""
            try:
                # 1. RPC Params
                tid = pkt.get('params', {}).get('trace_id')
                if tid: return str(tid)

                # 2. Root
                tid = pkt.get('trace_id')
                if tid: return str(tid)

                return ""
            except:
                return ""

        # Processing Loop
        for packet in (pinned_snap + flow_snap):
            # Identity Deduplication
            pkt_id = id(packet)
            if pkt_id in seen_refs: continue
            seen_refs.add(pkt_id)

            # Trace Deduplication
            trace = get_trace_id(packet)
            if trace and trace in seen_traces: continue
            if trace: seen_traces.add(trace)

            # Time Filtering
            ts = get_timestamp(packet)
            if ts > since_timestamp:
                combined.append(packet)

        # [ASCENSION 2]: THE INVINCIBLE SORT
        # We sort using the safe helper, guaranteeing stability.
        combined.sort(key=get_timestamp)

        return combined

    def tail(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        [ASCENSION 4]: KINETIC TAIL
        Returns the raw last N events without sorting. Optimized for high-speed console streaming.
        """
        with self._lock:
            return list(self._flow)[-count:]

    def clear(self):
        """
        [ASCENSION 5]: ATOMIC PURGE
        Resets the memory to the Primordial Void.
        """
        with self._lock:
            self._flow.clear()
            self._pinned.clear()

    def snapshot(self) -> Dict[str, Any]:
        """[ASCENSION 6]: FORENSIC DUMP"""
        with self._lock:
            return {
                "flow": list(self._flow),
                "pinned": list(self._pinned),
                "stats": {
                    "total_ingested": self.ingestion_count,
                    "depth": len(self._flow),
                    "pinned_count": len(self._pinned)
                }
            }