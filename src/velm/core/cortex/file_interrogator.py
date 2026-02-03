# Path: core/cortex/file_interrogator.py
# --------------------------------------

import os
import hashlib
import re
import stat as StatModule
import time
from pathlib import Path
from typing import Dict, Optional, Tuple, Any, Set, List

# --- THE DIVINE SUMMONS ---
from .contracts import FileGnosis, DISTILLATION_CHUNK_SIZE
from .entropy_oracle import calculate_shannon_entropy
from .git_historian import GitHistorian, TemporalGnosis
from .knowledge import KnowledgeBase
from .language_oracle import divine_language
from .tag_extractor import extract_semantic_tags
from .tokenomics import TokenEconomist
from ...inquisitor import get_treesitter_gnosis
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("GnosticInterrogator")


class FileInterrogator:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC INTERROGATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)     ==
    =================================================================================
    @gnosis:title The God-Engine of Gnostic Interrogation
    @gnosis:summary The divine, self-aware, and unbreakable atomic unit of perception.
    @gnosis:LIF 100,000,000,000,000

    [ASCENSION]: Now includes the 'Heavyweight Ward' to banish massive files from
    the AST Inquisitor, preventing the Infinite Freeze.
    """

    # [ASCENSION 13]: THE HEAVYWEIGHT LIMIT (1MB)
    MAX_AST_SIZE_BYTES = 1024 * 1024

    def __init__(
            self,
            root: Path,
            economist: TokenEconomist,
            git_historian: GitHistorian,
            cache: Dict[str, Any],
            new_cache: Dict[str, Any],
            workspace_root: Optional[Path] = None
    ):
        self.root = root
        self.economist = economist
        self.git_historian = git_historian
        self.cache = cache
        self.new_cache = new_cache
        self.workspace_root = workspace_root or root

    def interrogate(self, path: Path) -> Tuple[Optional[FileGnosis], Dict[str, Any]]:
        """
        [THE GRAND RITE OF GNOSTIC INTERROGATION]
        Perceives the soul of a file. Returns (FileGnosis, AST_Dossier).
        """
        try:
            rel_path, rel_path_str = self._gaze_upon_relativity(path)
            try:
                file_stat = path.stat()
            except FileNotFoundError:
                return None, {}
            mtime, size = file_stat.st_mtime, file_stat.st_size

            # [ASCENSION 3] The Cryptographic Chronocache
            cached = self.cache.get(rel_path_str)
            if cached and cached.get('mtime') == mtime and cached.get('size') == size:
                self.new_cache[rel_path_str] = cached
                gnosis_data = cached['gnosis'].copy()
                gnosis_data['path'] = rel_path
                return FileGnosis(**gnosis_data), cached.get("project_gnosis", {})

            # [ASCENSION 9] The Symlink Guardian
            if path.is_symlink():
                return FileGnosis(path=rel_path, original_size=size, token_cost=0, category='symlink',
                                  language='link'), {}

            header_bytes = self._read_bytes_safely(path, DISTILLATION_CHUNK_SIZE)
            if header_bytes is None: return None, {}

            # [ASCENSION 4] The Polyglot Prophet of Language
            language = divine_language(path, header_bytes)
            category = KnowledgeBase.categorize(path)
            if category != 'binary' and b'\0' in header_bytes:
                category = 'binary'

            # [ASCENSION 8] The Abyssal Sentinel (Skip Binary/Noise/Locks)
            if category in ('binary', 'noise', 'lock'):
                gnosis, ast = self._forge_abyssal_dossier(rel_path, size, category, language, file_stat, header_bytes)
                self._chronicle_in_cache(rel_path_str, mtime, size, gnosis, ast)
                return gnosis, ast

            # [ASCENSION 13]: THE HEAVYWEIGHT WARD
            # If the file is massive, we treat it as text/noise to avoid crashing the AST parser.
            if size > self.MAX_AST_SIZE_BYTES:
                # Logger.verbose(f"Skipping AST for heavyweight scripture: {rel_path.name} ({size} bytes)")
                category = 'text'  # Downgrade from 'code'

            content_bytes = self._read_bytes_safely(path)
            if content_bytes is None: return None, {}

            # [ASCENSION 5] The Encoding Alchemist
            content = self._decode_content(content_bytes)

            # [ASCENSION 1] The Law of Two Testaments
            # Only perform AST Gaze if it's code and under the size limit
            ast_metrics, treesitter_dossier, imported_symbols, semantic_links = self._gaze_upon_structure(
                path, content, category
            )

            # [ASCENSION 6] The Gaze of the Chronomancer
            temporal_gnosis = self._gaze_upon_temporality(rel_path)

            # [ASCENSION 7] The Semantic Harvester
            semantic_tags = self._gaze_upon_semantics(content)
            pending_will_tags = self._gaze_upon_pending_will(content)
            if category in ('doc', 'doc_critical') or path.suffix == '.md':
                semantic_tags.extend(self._gaze_upon_documentation(content))

            # [ASCENSION 10] The Token Economist
            token_cost = self.economist.estimate_cost(content)

            final_gnosis = FileGnosis(
                path=rel_path, original_size=size, token_cost=token_cost, category=category, language=language,
                permissions="755" if bool(file_stat.st_mode & StatModule.S_IXUSR) else None,
                hash_signature=hashlib.sha256(content_bytes).hexdigest() if size < 10 * 1024 * 1024 else "",
                churn_score=temporal_gnosis.churn_score, author_count=temporal_gnosis.author_count,
                days_since_last_change=temporal_gnosis.days_since_last_change,
                semantic_tags=sorted(list(set(semantic_tags + pending_will_tags))),
                ast_metrics=ast_metrics, imported_symbols=imported_symbols, semantic_links=semantic_links
            )

            # [ASCENSION 12] The Luminous Chronicler
            self._chronicle_in_cache(rel_path_str, mtime, size, final_gnosis, treesitter_dossier)
            return final_gnosis, treesitter_dossier

        except Exception as e:
            # [ASCENSION 11] The Unbreakable Ward of Paradox
            Logger.warn(f"A paradox shattered the interrogation of '{path.name}': {e}")
            return None, {}

    def _gaze_upon_relativity(self, path: Path) -> Tuple[Path, str]:
        """[ASCENSION 2] The Gnostic Anchor of Absolute Relativity."""
        try:
            rel_str = os.path.relpath(path, self.root).replace('\\', '/')
            return Path(rel_str), rel_str
        except ValueError as e:
            raise ArtisanHeresy(f"Scripture '{path}' is outside the Gnostic cosmos of '{self.root}'.", child_heresy=e)

    def _gaze_upon_structure(self, path: Path, content: str, category: str) -> Tuple[Dict, Dict, Set, Set]:
        """
        [THE LAW OF THE TWO TESTAMENTS]
        Returns: (metrics, full_dossier, pure_symbol_set, link_set)
        """
        ast_metrics, treesitter_dossier = {}, {}
        imported_symbols = set()
        semantic_links = set()
        try:
            if category == 'code' and content:
                # AST Parsing is expensive. Only do it for code.
                dossier = get_treesitter_gnosis(path, content)
                if dossier and "error" not in dossier:
                    # The Ancient Testament: The full, rich dictionary
                    treesitter_dossier = dossier
                    ast_metrics = dossier.get("metrics", {})
                    ast_metrics["functions"] = [
                        {"name": f.get("name", "unknown"), "lineno": f.get("start_point", [0, 0])[0] + 1} for f in
                        dossier.get("functions", [])]
                    ast_metrics["classes"] = [
                        {"name": c.get("name", "unknown"), "lineno": c.get("start_point", [0, 0])[0] + 1} for c in
                        dossier.get("classes", [])]

                    # The Ascended Testament: The pure set of strings
                    deps_block = dossier.get("dependencies", {})
                    if isinstance(deps_block, list):
                        imported_symbols.update(deps_block)
                    elif isinstance(deps_block, dict):
                        imported_symbols.update(deps_block.get("imported_symbols", []))
                        for imp in deps_block.get("imports", []):
                            if isinstance(imp, dict) and "path" in imp:
                                imported_symbols.add(imp["path"])
                            elif isinstance(imp, str):
                                imported_symbols.add(imp)
            elif category in ('doc', 'doc_critical') and content:
                path_regex = re.compile(r'[`\'"]((?:\./|src/|/)?[\w\./\-_]+?(\.py|\.ts|\.js|\.go|\.rs|\.md))[\'"`]')
                semantic_links = {match[0] for match in path_regex.findall(content)}
        except Exception as e:
            Logger.warn(f"Structural Gaze faltered for '{path.name}': {e}")
        return ast_metrics, treesitter_dossier, imported_symbols, semantic_links

    def _gaze_upon_documentation(self, content: str) -> List[str]:
        tags = []
        headers = re.findall(r'^#+\s+(.*)', content, re.MULTILINE)
        for h in headers:
            tags.extend([w.lower() for w in re.findall(r'\w+', h) if len(w) > 3])
        return tags

    def _gaze_upon_temporality(self, rel_path: Path) -> TemporalGnosis:
        try:
            return self.git_historian.inquire(rel_path)
        except Exception as e:
            Logger.warn(f"Temporal Gaze faltered for '{rel_path.name}': {e}")
            return TemporalGnosis()

    def _gaze_upon_semantics(self, content: str) -> List[str]:
        try:
            return extract_semantic_tags(content)
        except Exception:
            return []

    def _gaze_upon_pending_will(self, content: str) -> List[str]:
        try:
            return [f"TODO:{match[1].strip()}" for match in
                    re.findall(r'(TODO|FIXME)[:\s(]+(.*?)\)?$', content, re.IGNORECASE | re.MULTILINE)]
        except Exception:
            return []

    def _forge_abyssal_dossier(self, rel_path: Path, size: int, category: str, language: str, file_stat: os.stat_result,
                               content_bytes: bytes) -> Tuple[FileGnosis, Dict]:
        gnosis = FileGnosis(
            path=rel_path, original_size=size, token_cost=0, category=category, language=language,
            permissions="755" if bool(file_stat.st_mode & StatModule.S_IXUSR) else None,
            hash_signature=hashlib.sha256(content_bytes).hexdigest() if size < 10 * 1024 * 1024 else ""
        )
        return gnosis, {}

    def _chronicle_in_cache(self, rel_path_str: str, mtime: float, size: int, gnosis: FileGnosis, ast: Dict):
        self.new_cache[rel_path_str] = {
            'mtime': mtime, 'size': size,
            'gnosis': gnosis.model_dump(mode='json'),
            'project_gnosis': ast
        }

    def _read_bytes_safely(self, path: Path, limit: int = -1) -> Optional[bytes]:
        try:
            with open(path, 'rb') as f:
                return f.read(limit)
        except (IOError, OSError):
            return None

    def _decode_content(self, data: bytes) -> str:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return data.decode('latin-1', errors='replace')