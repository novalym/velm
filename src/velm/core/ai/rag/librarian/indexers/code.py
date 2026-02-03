# Path: core/ai/rag/librarian/indexers/code.py
# --------------------------------------------

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base import BaseIndexer
from ..contracts import RAGChunk
from ......inquisitor import get_treesitter_gnosis
from ......logger import Scribe

Logger = Scribe("CodeAnatomist")


class CodeIndexer(BaseIndexer):
    """
    =============================================================================
    == THE AST SURGEON (V-Ω-STRUCTURAL-SEMANTIC-ULTIMA)                        ==
    =============================================================================
    LIF: 100,000,000,000

    Extracts code atoms with high-fidelity context.
    It understands Nesting, Complexity, and Signatures.
    """

    def chunk(self, path: Path, content: str) -> List[RAGChunk]:
        chunks = []
        rel_path = str(path.relative_to(self.root)).replace('\\', '/')
        lang = self._normalize_lang(path.suffix)

        # 1. The Gnostic Inquest
        dossier = get_treesitter_gnosis(path, content)

        if "error" in dossier:
            return self._fallback_indentation_chunk(path, content, rel_path, lang)

        # 2. Map Hierarchy (Line containment)
        # Class ranges for parentage inference
        class_ranges = []
        for cls in dossier.get("classes", []):
            start = cls['start_point'][0]
            end = cls['end_point'][0] + cls['line_count']
            class_ranges.append((start, end, cls['name']))

        # 3. Process Classes
        for cls in dossier.get("classes", []):
            chunks.extend(self._process_symbol(cls, content, rel_path, "class", lang))

        # 4. Process Functions
        for func in dossier.get("functions", []):
            # Divine Parent
            start_line = func['start_point'][0]
            parent_name = None
            for c_start, c_end, c_name in class_ranges:
                if c_start <= start_line <= c_end:
                    parent_name = c_name
                    break

            fqn = f"{parent_name}.{func['name']}" if parent_name else func['name']

            # Enrich object
            func['fqn'] = fqn
            func['parent'] = parent_name

            chunks.extend(self._process_symbol(func, content, rel_path, "function", lang))

        return chunks

    def _process_symbol(self, node: Dict, full_content: str, path: str, type_: str, lang: str) -> List[RAGChunk]:
        """
        Transmutes an AST Node into one or more RAG Chunks.
        Handles massive bodies by splitting them.
        """
        chunks = []
        start_line = node['start_point'][0]
        line_count = node['line_count']
        end_line = start_line + line_count

        lines = full_content.splitlines()

        # [ASCENSION 6] Comment Binding
        # Look backwards for comments
        scan_idx = start_line - 1
        comments = []
        while scan_idx >= 0:
            line = lines[scan_idx].strip()
            if line.startswith(('#', '//', '///')):
                comments.insert(0, lines[scan_idx])
                scan_idx -= 1
            elif not line:
                scan_idx -= 1  # Skip blanks
            else:
                break

        # Determine content
        symbol_content = "\n".join(comments + lines[start_line:end_line])

        # [ASCENSION 8] Secret Scanning
        if "password" in symbol_content.lower() or "secret" in symbol_content.lower():
            # Simple heuristic redaction
            symbol_content = re.sub(r'([\'"])(.*?)([\'"])', r'\1[REDACTED]\3', symbol_content)

        # [ASCENSION 2 & 3] Metadata Extraction
        meta = {
            "name": node.get('fqn', node['name']),
            "type": type_,
            "complexity": int(node.get('cyclomatic_complexity', 0)),
            "docstring": node.get('docstring', '').strip(),
            "args": ", ".join(node.get('args', [])),  # [ASCENSION 4] Flattened
            "decorators": ", ".join(node.get('decorators', []))  # [ASCENSION 4] Flattened
        }

        # [ASCENSION 5] The Body Guard
        # If > 100 lines, split into Signature and Body parts
        if line_count > 100:
            # 1. Signature Chunk (First 20 lines approx)
            sig_content = "\n".join(lines[start_line: start_line + 20])
            sig_content += "\n... [Body Truncated] ..."

            chunks.append(self._create_chunk(
                f"{path}:{meta['name']}:sig", sig_content, path, start_line + 1, type_, lang, meta
            ))

            # 2. Body Chunks
            chunk_size = 50
            body_start = start_line + 20
            while body_start < end_line:
                body_end = min(body_start + chunk_size, end_line)
                body_content = f"# Context: {meta['name']} (continued)\n" + "\n".join(lines[body_start:body_end])

                chunks.append(self._create_chunk(
                    f"{path}:{meta['name']}:body_{body_start}",
                    body_content,
                    path,
                    body_start + 1,
                    "code_body",
                    lang,
                    {"parent_symbol": meta['name']}
                ))
                body_start = body_end
        else:
            # Standard Chunk
            chunks.append(self._create_chunk(
                f"{path}:{meta['name']}", symbol_content, path, start_line + 1, type_, lang, meta
            ))

        return chunks

    def _create_chunk(self, id_: str, content: str, path: str, line: int, type_: str, lang: str,
                      meta: Dict) -> RAGChunk:
        return RAGChunk(
            id=id_,
            content=content,
            file_path=path,
            start_line=line,
            end_line=line + content.count('\n'),
            type=type_,
            language=lang,
            metadata=meta
        )

    def _fallback_indentation_chunk(self, path: Path, content: str, rel_path: str, lang: str) -> List[RAGChunk]:
        """
        [ASCENSION 10] Smart Indentation Chunking.
        Splits by top-level blocks instead of arbitrary lines.
        """
        chunks = []
        lines = content.splitlines()
        current_block = []
        current_start = 1

        for i, line in enumerate(lines):
            # If line is top-level (no indent) and not empty/comment, it might be a break point
            if line.strip() and not line.startswith((' ', '\t', '#', '//')) and i > current_start + 10:
                # Flush
                chunks.append(self._create_chunk(
                    f"{rel_path}:{current_start}", "\n".join(current_block), rel_path, current_start, "text_block",
                    lang, {}
                ))
                current_block = []
                current_start = i + 1

            current_block.append(line)

        if current_block:
            chunks.append(self._create_chunk(
                f"{rel_path}:{current_start}", "\n".join(current_block), rel_path, current_start, "text_block", lang, {}
            ))

        return chunks

    def _normalize_lang(self, suffix: str) -> str:
        s = suffix.lower()
        mapping = {
            '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript', '.go': 'go',
            '.rs': 'rust', '.java': 'java', '.cpp': 'cpp', '.c': 'c'
        }
        return mapping.get(s, 'text')