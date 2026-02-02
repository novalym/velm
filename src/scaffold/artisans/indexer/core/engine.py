# Path: artisans/indexer/core/engine.py
# -------------------------------------

import concurrent.futures
from pathlib import Path
from typing import List, Any
from .contracts import IndexingStats
from ..languages.factory import LanguageFactory


class IndexingEngine:
    """
    =============================================================================
    == THE SWARM ENGINE (V-Ω-PARALLEL-PROCESSOR)                               ==
    =============================================================================
    Manages the thread pool and dispatches files to their respective parsers.
    """

    def __init__(self, cortex):
        self.cortex = cortex

    def run_swarm(self, files: List[Path]) -> IndexingStats:
        stats = IndexingStats(total_files=len(files))

        # Max 8 workers to balance GIL vs IO
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_path = {
                executor.submit(self._process_file, f): f
                for f in files
            }

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    symbols = future.result()
                    if symbols:
                        self.cortex.memorize_symbols(path, symbols)
                        stats.total_symbols += len(symbols)
                except Exception:
                    stats.errors += 1

        return stats

    def _process_file(self, path: Path):
        try:
            parser = LanguageFactory.get_parser(path)
            if not parser: return []
            content = path.read_text(encoding='utf-8', errors='ignore')
            return parser.parse(content, path)
        except Exception:
            return []