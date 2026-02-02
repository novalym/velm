# Path: core/lsp/features/diagnostics/ledger.py
# ---------------------------------------------

import threading
import time
import statistics
from collections import defaultdict, deque
from typing import Dict, List, Any
from ...types import Diagnostic, DiagnosticSeverity


class HeresyLedger:
    """
    =============================================================================
    == THE HERESY LEDGER (V-Ω-MULTIVERSAL-STATE-VECTOR)                        ==
    =============================================================================
    The Immutable Memory of the Inquisitor.

    [CAPABILITIES]:
    1. **Source Isolation:** Stores Local vs Daemon errors separately.
    2. **Integrity Scoring:** Calculates a project health score (0-100).
    3. **Fixability Index:** Tracks how many errors have auto-fixes.
    4. **Atomic Merging:** Merges layers into a flat list for the client.
    """

    def __init__(self):
        # Map[URI, Map[Source, List[Diagnostic]]]
        self._store: Dict[str, Dict[str, List[Diagnostic]]] = defaultdict(dict)

        # Metadata: Map[URI, {integrity, fixable_count}]
        self._meta: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "integrity": 100.0,
            "fixable_count": 0,
            "history": deque(maxlen=10)
        })

        self._lock = threading.RLock()

    def update(self, uri: str, diagnostics: List[Diagnostic], source: str = "LOCAL"):
        """[THE RITE OF INSCRIPTION]"""
        with self._lock:
            # 1. Inscribe Data
            self._store[uri][source] = diagnostics

            # 2. Calculate Integrity
            merged = self._merge_sources(uri)
            meta = self._meta[uri]
            meta["integrity"] = self._calculate_score(merged)

            # 3. Count Fixables
            meta["fixable_count"] = sum(
                1 for d in merged if d.data and isinstance(d.data, dict) and d.data.get('fix_command')
            )

            # 4. Chronicle History
            meta["history"].append({
                "ts": time.time(),
                "source": source,
                "count": len(diagnostics),
                "score": meta["integrity"]
            })

    def get_merged(self, uri: str) -> List[Diagnostic]:
        """[THE RITE OF REVELATION]"""
        with self._lock:
            return self._merge_sources(uri)

    def _merge_sources(self, uri: str) -> List[Diagnostic]:
        if uri not in self._store: return []

        sources = self._store[uri]
        unique_map = {}

        # Priority: DAEMON > AI > LOCAL
        priority = ["LOCAL", "AI", "DAEMON"]
        sorted_keys = sorted(sources.keys(), key=lambda k: priority.index(k) if k in priority else -1)

        for src in sorted_keys:
            for diag in sources[src]:
                # Hash based on range + code + message snippet
                key = f"{diag.range.start.line}:{diag.code}:{diag.message[:20]}"
                unique_map[key] = diag

        return list(unique_map.values())

    def _calculate_score(self, diagnostics: List[Diagnostic]) -> float:
        if not diagnostics: return 100.0
        penalty = 0.0
        for d in diagnostics:
            if d.severity == DiagnosticSeverity.Error:
                penalty += 10.0
            elif d.severity == DiagnosticSeverity.Warning:
                penalty += 2.0
            else:
                penalty += 0.1
        return max(0.0, 100.0 - penalty)

    def get_integrity_stats(self) -> Dict[str, Any]:
        """[THE SYSTEM PULSE]"""
        with self._lock:
            total_heresies = 0
            total_critical = 0
            integrity_scores = []

            for uri in self._store.keys():
                merged = self._merge_sources(uri)
                total_heresies += len(merged)
                total_critical += sum(1 for d in merged if d.severity == DiagnosticSeverity.Error)
                integrity_scores.append(self._meta[uri]["integrity"])

            avg_integrity = statistics.mean(integrity_scores) if integrity_scores else 100.0

            return {
                "score": round(avg_integrity, 1),
                "total": total_heresies,
                "critical": total_critical,
                "timestamp": time.time()
            }

    def clear(self, uri: str):
        with self._lock:
            if uri in self._store: del self._store[uri]
            if uri in self._meta: del self._meta[uri]