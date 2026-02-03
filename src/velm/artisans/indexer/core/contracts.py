# Path: artisans/indexer/core/contracts.py
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from ....core.cortex.contracts import SymbolKind


@dataclass
class IndexingStats:
    total_files: int = 0
    total_symbols: int = 0
    duration_ms: float = 0.0
    errors: int = 0

