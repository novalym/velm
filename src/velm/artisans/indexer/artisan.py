# Path: artisans/indexer/artisan.py
# ---------------------------------

import time
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import IndexRequest
from .core.engine import IndexingEngine
from .languages.factory import LanguageFactory


class IndexerArtisan(BaseArtisan[IndexRequest]):
    """
    =============================================================================
    == THE INDEXER ARTISAN (V-Ω-POLYGLOT-SWARM-V2)                             ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: KNOWLEDGE_INGESTOR
    """

    def execute(self, request: IndexRequest) -> ScaffoldResult:
        start_time = time.monotonic()

        # 1. Acquire Targets
        if not self.engine.cortex:
            return self.failure("Cortex not manifest.")

        memory = self.engine.cortex.perceive()

        # Filter for unindexed files that we support
        files_to_index = [
            f for f in memory.inventory
            if (request.force or not self.engine.cortex.is_indexed(f))
               and LanguageFactory.get_parser(f) is not None
        ]

        if not files_to_index:
            return self.success("Index Up-to-Date.")

        self.logger.info(f"Igniting Polyglot Swarm: {len(files_to_index)} scriptures identified.")

        # 2. Ignite Swarm
        engine = IndexingEngine(self.engine.cortex)
        stats = engine.run_swarm(files_to_index)

        stats.duration_ms = (time.monotonic() - start_time) * 1000

        return self.success(
            f"Indexing Complete. {stats.total_symbols} symbols found.",
            data=stats.__dict__
        )