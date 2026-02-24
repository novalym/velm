# Path: artisans/dream/archetype_indexer/extractor.py
# ---------------------------------------------------

import re
from pathlib import Path
from typing import Set, List

from .contracts import ArchetypeSoul
from ....logger import Scribe

Logger = Scribe("Indexer:Biopsy")


class SoulExtractor:
    """
    =============================================================================
    == THE BIOPSY SURGEON (V-Ω-REGEX-PHALANX)                                  ==
    =============================================================================
    Performs deep extraction of Gnosis from raw text.
    """

    # --- THE GRIMOIRE OF REGEX ---

    # Matches: # @gnosis:key value
    META_REGEX = re.compile(r'^[#|//]*\s*@(?:gnosis:)?(\w+)\s*[:=]?\s*(.*)', re.IGNORECASE)

    # Matches: $$ var_name = "default"
    VAR_REGEX = re.compile(r'^\s*\$\$\s*([a-zA-Z0-9_]+)\s*=')

    # Matches: path/to/file :: "content"  (To infer tech stack)
    FILE_SIG_REGEX = re.compile(r'^\s*([a-zA-Z0-9_\-\./]+)\s*(?:::|<<)')

    # --- THE DNA MAP (Structure -> Tag) ---
    DNA_MARKERS = {
        "Dockerfile": "docker",
        "docker-compose.yml": "docker",
        "Cargo.toml": ["rust", "cargo"],
        "go.mod": ["go", "golang"],
        "package.json": ["node", "javascript", "npm"],
        "tsconfig.json": "typescript",
        "pyproject.toml": ["python", "poetry"],
        "requirements.txt": ["python", "pip"],
        "mix.exs": "elixir",
        "Makefile": "make",
        "vite.config": "vite",
        "next.config": "nextjs"
    }

    def extract(self, path: Path, rel_id: str) -> ArchetypeSoul:
        """
        Conducts the Biopsy.
        """
        soul = ArchetypeSoul(id=rel_id, path=path)

        # We weigh the ID heavily in the corpus
        corpus_parts = [rel_id.replace('/', ' ').replace('-', ' '), rel_id]

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()

            # --- PHASE 1: HEADER SCRYING ---
            # We scan the first 100 lines for metadata headers
            for line in lines[:100]:
                line = line.strip()
                if not line: continue

                meta_match = self.META_REGEX.match(line)
                if meta_match:
                    key, val = meta_match.groups()
                    key = key.lower()
                    val = val.strip()

                    if key in ('title', 'name'):
                        soul.title = val
                        corpus_parts.extend([val] * 5)  # 5x Gravity
                    elif key in ('summary', 'description', 'desc'):
                        soul.summary = val
                        corpus_parts.extend([val] * 3)  # 3x Gravity
                    elif key == 'tags':
                        tags = {t.strip().lower() for t in val.split(',')}
                        soul.tags.update(tags)
                        corpus_parts.extend(list(tags) * 4)  # 4x Gravity
                    elif key == 'author':
                        soul.author = val

            # --- PHASE 2: STRUCTURAL BIOPSY ---
            # We scan the whole file for Variable Definitions and File Signatures
            for line in lines:
                # Scry Variables
                if var_match := self.VAR_REGEX.match(line):
                    soul.required_vars.append(var_match.group(1))

                # Scry File Signatures (for DNA inference)
                if file_match := self.FILE_SIG_REGEX.match(line):
                    filename = Path(file_match.group(1)).name
                    self._analyze_dna(filename, soul)

            # --- PHASE 3: CORPUS FUSION ---
            # Merge inferred tags into corpus
            corpus_parts.extend(list(soul.inferred_tags) * 2)
            soul.lexical_corpus = " ".join(corpus_parts).lower()

        except Exception as e:
            Logger.warn(f"Biopsy failed for {path.name}: {e}. Soul incomplete.")
            # Return partial soul rather than failing
            soul.lexical_corpus = rel_id  # Minimum viable searchability

        return soul

    def _analyze_dna(self, filename: str, soul: ArchetypeSoul):
        """
        Maps a filename to implied technologies.
        """
        for marker, tags in self.DNA_MARKERS.items():
            if marker in filename:
                if isinstance(tags, list):
                    soul.inferred_tags.update(tags)
                else:
                    soul.inferred_tags.add(tags)