# Path: core/ai/rag/librarian/indexers/text.py
# --------------------------------------------

import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base import BaseIndexer
from ..contracts import RAGChunk
from ......logger import Scribe

Logger = Scribe("TextAnatomist")


class TextIndexer(BaseIndexer):
    """
    =============================================================================
    == THE MARKDOWN ANATOMIST (V-Ω-STATE-AWARE-ULTIMA)                         ==
    =============================================================================
    LIF: 100,000,000,000

    A context-aware parser that dissects Documentation into semantic organs.
    It understands Hierarchy (Headers), Metadata (Frontmatter), and Examples (Code Blocks).
    """

    # Regex for finding links [Label](URL)
    LINK_REGEX = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

    def chunk(self, path: Path, content: str) -> List[RAGChunk]:
        chunks: List[RAGChunk] = []
        rel_path = str(path.relative_to(self.root)).replace('\\', '/')

        # 1. Frontmatter Extraction
        metadata_global = {}
        processed_content = content
        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    if isinstance(frontmatter, dict):
                        # Flatten immediately
                        for k, v in frontmatter.items():
                            metadata_global[f"fm_{k}"] = str(v)
                    processed_content = parts[2]
            except Exception as e:
                Logger.warn(f"Frontmatter parsing failed for '{rel_path}': {e}")

        # 2. State Machine Parsing
        lines = processed_content.splitlines()
        header_stack = ["Root"]
        current_block = []
        current_start_line = 1
        in_code_block = False
        code_lang = "text"

        def flush_chunk(end_line_idx: int, is_code: bool = False):
            if not current_block: return
            text = "\n".join(current_block).strip()
            if not text: return

            # Metadata enrichment
            meta = metadata_global.copy()

            # [ASCENSION 8] Flatten Hierarchy
            hierarchy = " > ".join(header_stack)
            meta["headers"] = hierarchy

            # [ASCENSION 5] Link Harvesting
            links = self.LINK_REGEX.findall(text)
            if links:
                # Store top 3 links to avoid metadata bloat
                meta["references"] = ", ".join([url for _, url in links[:3]])

            # [ASCENSION 6] Admonition Detection
            if text.startswith(("!!!", "> **", "> [!")):
                meta["is_admonition"] = "true"

            chunk_type = "code_snippet" if is_code else "documentation"

            chunks.append(RAGChunk(
                id=f"{rel_path}:{hierarchy}:{current_start_line}",
                content=f"# {hierarchy}\n\n{text}",
                file_path=rel_path,
                start_line=current_start_line,
                end_line=end_line_idx + 1,
                type=chunk_type,
                language=code_lang if is_code else "markdown",
                metadata=meta
            ))

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # [ASCENSION 1] Code Fence Detection
            if line_stripped.startswith("```"):
                if in_code_block:
                    # Closing the block
                    current_block.append(line)
                    flush_chunk(i, is_code=True)
                    current_block = []
                    in_code_block = False
                    current_start_line = i + 1
                    code_lang = "text"
                else:
                    # Starting a block - flush previous text first
                    flush_chunk(i - 1)
                    current_block = [line]
                    in_code_block = True
                    current_start_line = i
                    # Extract lang
                    code_lang = line_stripped.lstrip("`").strip() or "text"
                continue

            if in_code_block:
                current_block.append(line)
                continue

            # [ASCENSION 3] Header Detection (Only outside code blocks)
            if line_stripped.startswith("#"):
                # Determine level
                level = len(line_stripped.split()[0])
                title = line_stripped.lstrip("#").strip()

                if level <= 6 and title:
                    # Flush previous content
                    flush_chunk(i - 1)
                    current_block = []
                    current_start_line = i

                    # Update Stack
                    # Pop until we are at the right parent level
                    # Stack: [Root (0), H1 (1), H2 (2)]
                    # If new level is 2, we pop until len is 2 (Root, H1), then append new H2
                    while len(header_stack) > level:
                        header_stack.pop()
                    # If we jumped down (H1 -> H3), we just append
                    header_stack.append(title)

                    # We treat the header line as part of the next block
                    current_block.append(line)
                    continue

            current_block.append(line)

        # Final Flush
        flush_chunk(len(lines))

        return chunks