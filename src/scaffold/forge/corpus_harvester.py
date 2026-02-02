# scaffold/forge/corpus_harvester.py

import os
from pathlib import Path
from typing import List, Dict, Any
from ..core.cortex.file_discoverer import FileDiscoverer
from ..core.cortex.tokenomics import TokenEconomist
from ..logger import Scribe

Logger = Scribe("GnosticHarvester")


class CorpusHarvester:
    """
    =============================================================================
    == THE HARVESTER OF SOULS (V-Ω-DATA-MINER)                               ==
    =============================================================================
    Walks the sanctum, collecting scriptures (code) and preparing them for the
    Instruction Forger.
    """

    def __init__(self, root: Path):
        self.root = root
        self.economist = TokenEconomist()

    def harvest(self, extensions: List[str] = None) -> List[Dict[str, str]]:
        """
        Gathers raw text from the project.
        Returns: List[{path: str, content: str, type: str}]
        """
        extensions = extensions or ['.py', '.ts', '.tsx', '.js', '.rs', '.go', '.scaffold', '.symphony', '.md']

        discoverer = FileDiscoverer(self.root, include_patterns=[f"*{ext}" for ext in extensions])
        files = discoverer.discover()

        corpus = []
        Logger.info(f"Harvesting Gnosis from {len(files)} scriptures...")

        for path in files:
            try:
                content = path.read_text(encoding='utf-8')
                if not content.strip(): continue

                # Basic sanity check: Don't train on massive minified files
                if len(content) > 100_000:
                    continue

                corpus.append({
                    "path": str(path.relative_to(self.root)),
                    "content": content,
                    "type": "code" if path.suffix != ".md" else "documentation"
                })
            except Exception:
                pass

        Logger.success(f"Harvested {len(corpus)} units of raw Gnosis.")
        return corpus