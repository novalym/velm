# Path: core/ai/akasha.py
# -----------------------

import os
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..cortex.vector import VectorCortex
from ..cortex.tokenomics import TokenEconomist
from ...logger import Scribe

Logger = Scribe("AkashicRecord")


class AkashicRecord:
    """
    =================================================================================
    == THE AKASHIC RECORD (V-Ω-GLOBAL-MEMORY-SINGULARITY)                          ==
    =================================================================================
    LIF: 100,000,000,000

    The Global Neural Memory of the Scaffold Cosmos. It transcends project boundaries,
    collecting every Rite, every success, and every performance metric into a
    universal Gnostic Pool located at `~/.scaffold/akasha`.
    """

    AKASHA_ROOT = Path.home() / ".scaffold" / "akasha"

    def __init__(self):
        self.AKASHA_ROOT.mkdir(parents=True, exist_ok=True)
        # We use a dedicated global collection.
        # Note: VectorCortex expects a project root, but here we treat AKASHA_ROOT as the project.
        self.vector_store = VectorCortex(self.AKASHA_ROOT)
        # Override internal DB path to be global
        self.vector_store.db_path = self.AKASHA_ROOT / "vector_store"

        self.economist = TokenEconomist()

    def enshrine(self,
                 rite_name: str,
                 content: str,
                 metrics: Dict[str, Any],
                 variables: Dict[str, Any],
                 source_path: str = "generated"):
        """
        Inscribes a successful rite into the global memory.
        Includes the 'Soul' (content) and the 'Vitality' (metrics).
        """
        # Forge a unique ID for this specific incarnation of the rite
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        incarnation_id = f"{rite_name}_{int(time.time())}_{content_hash}"

        # We sanitize variables to remove project-specific noise or secrets
        safe_vars = {k: v for k, v in variables.items()
                     if isinstance(v, (str, int, bool)) and "secret" not in k.lower() and "key" not in k.lower()}

        metadata = {
            "source": source_path,  # VectorCortex requires 'source' in metadata
            "rite": rite_name,
            "timestamp": time.time(),
            "project": variables.get("project_name", "unknown"),
            "duration_ms": metrics.get("duration_ms", 0),
            "tokens_total": metrics.get("tokens_total", 0),
            "context_json": json.dumps(safe_vars),  # Store context for retrieval
            "type": "akasha_memory"
        }

        Logger.verbose(f"Enshrining {rite_name} in the Akashic Record...")

        # We use the internal collection directly to bypass project-specific logic if needed,
        # but VectorCortex's _add_chunk logic is robust.
        # We manually construct the chunks to feed VectorCortex.
        self.vector_store._awaken()

        self.vector_store._collection.upsert(
            ids=[incarnation_id],
            documents=[content],
            metadatas=[metadata]
        )

    def recall_wisdom(self, query: str, limit: int = 3, filter_rite: str = None) -> List[Dict[str, Any]]:
        """
        Queries the global memory for similar past experiences.
        """
        filters = {"type": "akasha_memory"}
        if filter_rite:
            filters["rite"] = filter_rite

        Logger.verbose(f"Akasha: Searching for wisdom matching '{query[:40]}...'")
        return self.vector_store.search(query, limit=limit, filters=filters)

    def get_stats(self) -> Dict[str, Any]:
        """Returns the vitality of the global memory."""
        self.vector_store._awaken()
        count = self.vector_store._collection.count()
        size = sum(f.stat().st_size for f in self.AKASHA_ROOT.rglob('*') if f.is_file())
        return {
            "total_memories": count,
            "storage_size_bytes": size,
            "location": str(self.AKASHA_ROOT)
        }

    def purge(self):
        """Annihilates the global memory."""
        self.vector_store.clear()
        import shutil
        if self.AKASHA_ROOT.exists():
            shutil.rmtree(self.AKASHA_ROOT)
            self.AKASHA_ROOT.mkdir()