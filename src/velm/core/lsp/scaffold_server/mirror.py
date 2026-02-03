# Path: core/lsp/scaffold_server/mirror.py
# ----------------------------------------
# LIF: INFINITY | ROLE: VISUAL_CORTEX | RANK: SOVEREIGN
# =================================================================================
# == THE MIRROR PROJECTOR (V-Ω-TOTALITY-V306-TRANSCENDENT)                       ==
# =================================================================================

import time
import uuid
import logging
import threading
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..base import (
    forensic_log,
    UriUtils,
    ServerState
)

Logger = logging.getLogger("MirrorProjector")


class MirrorProjector:
    """
    [THE VISUAL CORTEX]
    Orchestrates the projection of structural Gnosis to the Ocular UI.
    Ensures the Mirror (Tree View) is a liquid-smooth reflection of the Architect's will.
    """

    def __init__(self, server: Any):
        self.server = server

        # --- [INTERNAL MEMORY STRATA] ---
        # Map[URI, Version] - Temporal Guard
        self._last_projected_version: Dict[str, int] = {}
        # Map[URI, Hash] - Redundancy Filter
        self._last_projected_hash: Dict[str, str] = {}

        self._lock = threading.RLock()

    def project(self, uri: str, structure: List[Dict[str, Any]], ascii_tree: str = "", version: int = 0):
        """
        [THE RITE OF PROJECTION]
        Transmits the structural hologram to the Ocular UI across the Silver Cord.
        """
        # [ASCENSION 2]: GENERATIONAL FLUX FILTER
        with self._lock:
            if version < self._last_projected_version.get(uri, -1) and version != 0:
                # Discard stale reality
                return
            self._last_projected_version[uri] = version

        try:
            # 1. [ASCENSION 1]: ISOMORPHIC URI SYNCHRONIZATION
            # Force absolute parity with the client's internal coordinate system.
            norm_uri = UriUtils.normalize_uri(uri)
            fs_path = UriUtils.to_fs_path(norm_uri)

            # 2. [ASCENSION 3]: RECURSIVE NODE ALCHEMISTRY
            # Purify the tree matter and ensure no null-pointer heresies reach the React layer.
            sanitized_structure = self._sanitize_tree(structure)

            # 3. [ASCENSION 9]: LUMINOUS TRACE CORRELATION
            # Link this projection to the current request context for forensic auditing.
            trace_id = getattr(self.server._ctx, 'trace_id', f"mir-{uuid.uuid4().hex[:6].upper()}")

            # 4. [ASCENSION 7]: ATOMIC MULTICAST BURST
            # Combine all perceived facets of the scripture into a single protocol packet.
            projection_packet = {
                "uri": norm_uri,
                "structure": sanitized_structure,
                "ascii_tree": ascii_tree,
                "version": version,
                "meta": {
                    "timestamp": time.time(),
                    "trace_id": trace_id,
                    "latency_ms": self._calculate_latency(),  # [ASCENSION 10]
                    "is_shadow": norm_uri.startswith("scaffold-shadow:")  # [ASCENSION 8]
                }
            }

            # 5. THE PROCLAMATION
            # Send the Gnostic notification to the Ocular UI.
            self.server.endpoint.send_notification("scaffold/previewStructure", projection_packet)

            # self.server.logger.debug(f"Mirror Reflected: {fs_path.name} (v{version})", trace_id=trace_id)

        except Exception as fracture:
            # [ASCENSION 12]: FAULT TOLERANCE
            forensic_log(f"Mirror Projection Fracture for {uri}: {fracture}", "ERROR", "MIRROR")

    # =============================================================================
    # == INTERNAL ALCHEMISTRY                                                    ==
    # =============================================================================

    def _sanitize_tree(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [ASCENSION 3]: THE NODE ALCHEMIST
        Recursively ensures every node is valid, named, and iconographically aligned.
        """
        if not nodes:
            return []

        # [ASCENSION 12]: CAUSAL ANCHORING
        # Promote important files to the top of the collection.
        def _sort_key(n):
            name = n.get('name', '').lower()
            if 'scaffold.scaffold' in name: return 0
            if 'index.' in name: return 1
            if n.get('is_dir'): return 2
            return 3

        sorted_nodes = sorted(nodes, key=_sort_key)

        for node in sorted_nodes:
            # 1. DIVINE IDENTITY
            if 'name' not in node or not node['name']:
                path = node.get('path', 'unknown_node')
                node['name'] = str(path).split('/')[-1] if path else "AnonymousNode"

            # 2. [ASCENSION 4]: SEMANTIC ICONOGRAPHY
            # Assign kind codes (1=File, 13=Var, 12=Func, 19=Folder)
            if 'kind' not in node:
                if node.get('is_dir'):
                    node['kind'] = 19
                elif node['name'].startswith('$$'):
                    node['kind'] = 13
                elif node['name'].startswith('@'):
                    node['kind'] = 12
                else:
                    node['kind'] = 1

            # 3. [ASCENSION 6]: ADAPTIVE DETAIL SPLICING
            # Extract variable values for immediate visibility
            if 'value' in node and not node.get('detail'):
                node['detail'] = f"= {node['value']}"

            # 4. [ASCENSION 8]: VOID GUARD
            # Ensure children is always a manifest list, never a null heresy.
            if 'children' in node and node['children']:
                node['children'] = self._sanitize_tree(node['children'])
            else:
                node['children'] = []

        return sorted_nodes

    def _calculate_latency(self) -> float:
        """[ASCENSION 10]: CHRONOMETRIC TELEMETRY."""
        # Calculate how long since the current request (keystroke) arrived.
        start = getattr(self.server._ctx, 'start_time', time.perf_counter())
        return (time.perf_counter() - start) * 1000

    def clear(self, uri: str):
        """[THE RITE OF ABSOLUTION] Clears the temporal memory for a specific file."""
        norm_uri = UriUtils.normalize_uri(uri)
        with self._lock:
            self._last_projected_version.pop(norm_uri, None)
            self._last_projected_hash.pop(norm_uri, None)

# === SCRIPTURE SEALED: THE MIRROR IS PURE ===