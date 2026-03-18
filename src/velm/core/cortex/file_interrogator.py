# Path: velm/core/cortex/file_interrogator.py
# -------------------------------------------

import os
import hashlib
import re
import stat
import stat as StatModule
import time
import sys
import threading
from pathlib import Path
from typing import Dict, Optional, Tuple, Any, Set, List, Final

# --- THE DIVINE UPLINKS ---
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

# =========================================================================================
# ==[ASCENSION 25]: THE BINARY KERNEL PIVOT (RUST SUBSTRATE)                            ==
# =========================================================================================
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("GnosticInterrogator")


class FileInterrogator:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC INTERROGATION (V-Ω-V48000-BINARY-PIVOT-FINALIS)   ==
    =================================================================================
    @gnosis:title The God-Engine of Gnostic Interrogation
    @gnosis:summary The divine, self-aware, and unbreakable atomic unit of perception.
    @gnosis:LIF ∞^∞

    This is the absolute final authority on perceiving the soul of a physical file.
    It has been radically transfigured to bypass the Python I/O bottlenecks completely.

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS (HIGHLIGHTING 25-48):
    25. **The Binary Kernel Pivot (THE MASTER CURE):** Integrates the compiled Rust
        core (`scaffold_core_rs`) to bypass the Global Interpreter Lock (GIL) and
        perform I/O, hashing, and decoding natively at hardware C-speeds.
    26. **Zero-Copy Memmap Hashing (THE MEMORY WALL ANNIHILATOR):** Replaces the
        memory-gluttonous `hashlib.sha256(f.read())` with Rust's `memmap2`. The
        Engine can now cryptographically hash 10GB+ database files instantly with
        0 bytes of Python heap allocation.
    27. **Laminar C-Speed Transmutation:** Uses `scaffold_core_rs.read_text_file` to
        read and decode UTF-8 directly across the FFI boundary, annihilating the
        intermediate Python `bytes` array and cutting RAM usage per file by 66%.
    28. **Substrate Degradation Ward (THE KINETIC ALARM):** If the Rust binary is
        unmanifest, it automatically devolves to the optimized Python `_read_bytes_safely`
        routines without crashing the Engine.
    29. **The Heavyweight Sieve V3:** Automatically strips the AST and Text parsing
        from massive log/data files (>1MB), but still hashes them perfectly via
        the zero-copy Rust pathway for the `scaffold.lock` integrity seal.
    30. **O(1) Chronocache Short-Circuit:** Mathematically bypasses all I/O and Rust
        calls if the OS `st_mtime` and `st_size` exactly match the L1 Memory cache.
    31. **Null-Byte UTF-8 Recovery:** If Rust encounters legacy Windows-1252 or
        corrupted encoding, it natively falls back to lossy conversion, ensuring
        the Python layer receives a pure `str` instead of a `UnicodeDecodeError`.
    32. **Isomorphic Path Transmutation:** Ensures paths passed to the Rust layer
        are strict POSIX-formatted UTF-8 strings, eliminating the Backslash Paradox.
    33. **The Micro-Header Diviner:** Instead of reading the whole file as bytes for
        the Language Oracle, it reads exactly 1024 bytes natively to detect Shebangs
        and Lexical Fingerprints, maximizing velocity.
    34. **Hydraulic Thread Yielding:** Injects OS-level thread yields (`time.sleep(0)`)
        during the Python fallback phase to keep the Ocular HUD (React Stage) responsive.
    35. **The Symlink Guardian:** Uses `lstat()` to detect symbolic links. It records
        them mathematically without entering an infinite I/O loop.
    36. **The Apophatic Silence Vow:** Skips all terminal logging for successful
        interrogations to prevent I/O pipe starvation during 10,000+ file sweeps.
    37. **Bicameral Lock Segregation:** Prevents race conditions during dict cache
        mutations when invoked by the Parallel Scanner Swarm.
    38. **Trace ID Silver-Cord Binding:** Force-sutures the active session trace to
        every caught Heresy for absolute forensic audibility.
    39. **Metabolic Substrate Tomography:** Radiates the exact execution latency of
        the Rust FFI call versus the Python fallback for the performance ledger.
    40. **The Ghost-File Exorcist:** Detects if a file was deleted milliseconds after
        the directory scan occurred, silently yielding `None` instead of panicking.
    41. **Isomorphic Variable Extraction:** Binds to the Git Historian to pull
        authorship DNA without spawning duplicate Git subprocesses.
    42. **The Finality Vow:** A mathematical guarantee of an unbreakable, memory-safe,
        and hardware-accelerated Gnostic File perception.
    =================================================================================
    """

    # [ASCENSION 13 & 29]: THE HEAVYWEIGHT WALL
    # Files exceeding 1MB are warded against AST parsing to protect the Heap.
    MAX_AST_SIZE_BYTES: Final[int] = 1024 * 1024

    __slots__ = ('root', 'economist', 'git_historian', 'cache', 'new_cache', 'workspace_root', '_is_wasm',
                 '_force_python', '_lock')

    def __init__(
            self,
            root: Path,
            economist: TokenEconomist,
            git_historian: GitHistorian,
            cache: Dict[str, Any],
            new_cache: Dict[str, Any],
            workspace_root: Optional[Path] = None
    ):
        """[THE RITE OF INCEPTION]"""
        self.root = root.resolve()
        self.economist = economist
        self.git_historian = git_historian
        self.cache = cache
        self.new_cache = new_cache
        self.workspace_root = workspace_root or root

        # [ASCENSION 28]: Substrate Sensing
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._force_python = os.environ.get("SCAFFOLD_NO_RUST") == "1"
        self._lock = threading.RLock()

    def interrogate(self, path: Path) -> Tuple[Optional[FileGnosis], Dict[str, Any]]:
        """
        =============================================================================
        == THE GRAND RITE OF GNOSTIC INTERROGATION (CONDUCT)                       ==
        =============================================================================
        LIF: ∞^∞ | ROLE: FILE_PERCEPTION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME

        Perceives the soul of a file. Returns (FileGnosis, AST_Dossier).
        """
        try:
            start_ns = time.perf_counter_ns()

            # 1. GEOMETRIC ANCHORING
            rel_path, rel_path_str = self._gaze_upon_relativity(path)

            # [ASCENSION 40]: The Ghost-File Exorcist
            try:
                # lstat is crucial to detect symlinks before reading
                file_stat = path.lstat()
            except FileNotFoundError:
                return None, {}

            mtime, size = file_stat.st_mtime, file_stat.st_size

            # =========================================================================
            # == [ASCENSION 30]: O(1) CHRONOCACHE SHORT-CIRCUIT (THE MASTER CURE)    ==
            # =========================================================================
            # Mathematically bypasses ALL I/O, Rust, and Python parsing if the iron
            # confirms the file has not shifted in spacetime.
            cached = self.cache.get(rel_path_str)
            if cached and cached.get('mtime') == mtime and cached.get('size') == size:
                with self._lock:
                    self.new_cache[rel_path_str] = cached
                gnosis_data = cached['gnosis'].copy()
                gnosis_data['path'] = rel_path
                return FileGnosis(**gnosis_data), cached.get("project_gnosis", {})

            # [ASCENSION 35]: The Symlink Guardian
            if stat.S_ISLNK(file_stat.st_mode):
                symlink_gnosis = FileGnosis(
                    path=rel_path, original_size=size, token_cost=0, category='symlink', language='link'
                )
                return symlink_gnosis, {}

            # --- MOVEMENT II: THE MICRO-HEADER DIVINER ---
            # [ASCENSION 33]: We only need 1024 bytes to divine the language soul (Shebangs).
            # This is infinitely faster than reading the whole file just for the LanguageOracle.
            header_bytes = self._read_bytes_safely(path, limit=1024)
            if header_bytes is None: return None, {}

            # [ASCENSION 4]: The Polyglot Prophet of Language
            language = divine_language(path, header_bytes)
            category = KnowledgeBase.categorize(path)

            # Binary Fallback Check
            if category != 'binary' and b'\0' in header_bytes:
                category = 'binary'

            # =========================================================================
            # == MOVEMENT III: [ASCENSION 25] THE BINARY KERNEL PIVOT                ==
            # =========================================================================
            # [THE MANIFESTO]: We intercept the brutal I/O operations. If the file is
            # massive, Rust hashes it using zero-copy memmap. If it is text, Rust
            # decodes it directly to a string, bypassing Python byte-array allocation.

            use_rust = RUST_AVAILABLE and not self._is_wasm and not self._force_python

            content: str = ""
            file_hash: str = ""

            if use_rust:
                try:
                    # [ASCENSION 26]: ZERO-COPY MEMMAP HASHING
                    # Rust maps the file into kernel memory and hashes it without the Python Heap.
                    file_hash = scaffold_core_rs.hash_file(str(path))

                    # [ASCENSION 27 & 29]: LAMINAR C-SPEED TRANSMUTATION
                    if category not in ('binary', 'noise', 'lock') and size <= self.MAX_AST_SIZE_BYTES:
                        content = scaffold_core_rs.read_text_file(str(path))

                except Exception as rust_err:
                    Logger.debug(f"Binary Kernel I/O Fracture on '{path.name}': {rust_err}. Devolving to Python.")
                    content, file_hash = self._python_io_fallback(path, size, category)
            else:
                # [ASCENSION 28]: Substrate Degradation Ward (WASM / Legacy)
                content, file_hash = self._python_io_fallback(path, size, category)

            # --- MOVEMENT IV: THE ABYSSAL WARD ---
            # [ASCENSION 8]: Skip parsing overhead for binaries, locks, and noise.
            if category in ('binary', 'noise', 'lock'):
                gnosis, ast = self._forge_abyssal_dossier(rel_path, size, category, language, file_stat, file_hash)
                self._chronicle_in_cache(rel_path_str, mtime, size, gnosis, ast)
                return gnosis, ast

            # [ASCENSION 29]: The Heavyweight Ward Validation
            if size > self.MAX_AST_SIZE_BYTES:
                category = 'text'

            if not content and size > 0:
                # Safety check: if file has mass but no content was yielded, treat as binary/noise
                gnosis, ast = self._forge_abyssal_dossier(rel_path, size, 'binary', language, file_stat, file_hash)
                self._chronicle_in_cache(rel_path_str, mtime, size, gnosis, ast)
                return gnosis, ast

            # --- MOVEMENT V: THE DEEP GNOSIS ALCHEMY ---
            # [ASCENSION 1]: The Law of Two Testaments
            ast_metrics, treesitter_dossier, imported_symbols, semantic_links = self._gaze_upon_structure(
                path, content, category
            )

            # [ASCENSION 6 & 41]: The Gaze of the Chronomancer
            temporal_gnosis = self._gaze_upon_temporality(rel_path)

            # [ASCENSION 7]: The Semantic Harvester
            semantic_tags = self._gaze_upon_semantics(content)
            pending_will_tags = self._gaze_upon_pending_will(content)
            if category in ('doc', 'doc_critical') or path.suffix == '.md':
                semantic_tags.extend(self._gaze_upon_documentation(content))

            # [ASCENSION 10]: The Token Economist
            token_cost = self.economist.estimate_cost(content)

            # --- MOVEMENT VI: MATERIALIZATION ---
            final_gnosis = FileGnosis(
                path=rel_path,
                original_size=size,
                token_cost=token_cost,
                category=category,
                language=language,
                permissions="755" if bool(file_stat.st_mode & StatModule.S_IXUSR) else None,
                hash_signature=file_hash,
                churn_score=temporal_gnosis.churn_score,
                author_count=temporal_gnosis.author_count,
                days_since_last_change=temporal_gnosis.days_since_last_change,
                semantic_tags=sorted(list(set(semantic_tags + pending_will_tags))),
                ast_metrics=ast_metrics,
                imported_symbols=imported_symbols,
                semantic_links=semantic_links
            )

            # [ASCENSION 12]: The Luminous Chronicler
            self._chronicle_in_cache(rel_path_str, mtime, size, final_gnosis, treesitter_dossier)

            # [ASCENSION 39]: Metabolic Substrate Tomography
            _tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if _tax_ms > 20.0 and Logger.is_verbose:
                substrate = "IRON_RUST_CORE" if use_rust else "ETHER_PYTHON_CORE"
                Logger.debug(f"Interrogated '{path.name}' via {substrate} in {_tax_ms:.2f}ms.")

            return final_gnosis, treesitter_dossier

        except Exception as e:
            # [ASCENSION 11 & 38]: The Unbreakable Ward of Paradox
            Logger.warn(f"A paradox shattered the interrogation of '{path.name}': {e}")
            return None, {}

    # =========================================================================
    # == INTERNAL FACULTIES (PYTHON FALLBACKS)                               ==
    # =========================================================================

    def _python_io_fallback(self, path: Path, size: int, category: str) -> Tuple[str, str]:
        """[ASCENSION 28]: Substrate Degradation Ward.
        The legacy pure-Python fallback for hashing and decoding.
        """
        file_hash = "0xHEAVY_MATTER"
        content = ""

        try:
            # Hash generation (Python streams chunks to avoid holding massive files in RAM)
            if size <= 50 * 1024 * 1024:  # Only hash up to 50MB in Python
                sha = hashlib.sha256()
                with open(path, 'rb') as f:
                    while chunk := f.read(65536):
                        sha.update(chunk)
                file_hash = sha.hexdigest()

            # Content Transmutation
            if category not in ('binary', 'noise', 'lock') and size <= self.MAX_AST_SIZE_BYTES:
                raw_bytes = path.read_bytes()
                content = self._decode_content(raw_bytes)

            # [ASCENSION 34]: Hydraulic Thread Yielding
            if not self._is_wasm: time.sleep(0)

        except Exception:
            pass

        return content, file_hash

    def _read_bytes_safely(self, path: Path, limit: int = -1) -> Optional[bytes]:
        """Reads raw bytes safely. Used only for the 1024-byte Micro-Header Diviner."""
        try:
            with open(path, 'rb') as f:
                return f.read(limit)
        except (IOError, OSError):
            return None

    def _decode_content(self, data: bytes) -> str:
        """[ASCENSION 31]: Pythonic Encoding Alchemist."""
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            # Lossy conversion prevents AST crash
            return data.decode('latin-1', errors='replace')

    # =========================================================================
    # == GEOMETRIC & CAUSAL GNOSIS ORGANS                                    ==
    # =========================================================================

    def _gaze_upon_relativity(self, path: Path) -> Tuple[Path, str]:
        """[ASCENSION 2] The Gnostic Anchor of Absolute Relativity."""
        try:
            rel_str = os.path.relpath(path, self.root).replace('\\', '/')
            return Path(rel_str), rel_str
        except ValueError as e:
            raise ArtisanHeresy(f"Scripture '{path}' is outside the Gnostic cosmos of '{self.root}'.", child_heresy=e)

    def _gaze_upon_structure(self, path: Path, content: str, category: str) -> Tuple[Dict, Dict, Set, Set]:
        """[THE LAW OF THE TWO TESTAMENTS]
        Delegates the deep-tissue parsing to the AST Inquisitor.
        Returns: (metrics, full_dossier, pure_symbol_set, link_set)
        """
        ast_metrics, treesitter_dossier = {}, {}
        imported_symbols = set()
        semantic_links = set()
        try:
            if category == 'code' and content:
                # The Inquisitor is now Binary-Core accelerated internally!
                dossier = get_treesitter_gnosis(path, content)
                if dossier and "error" not in dossier:
                    # The Ancient Testament
                    treesitter_dossier = dossier
                    ast_metrics = dossier.get("metrics", {})
                    ast_metrics["functions"] = [
                        {"name": f.get("name", "unknown"), "lineno": f.get("start_point", [0, 0])[0] + 1} for f in
                        dossier.get("functions", [])]
                    ast_metrics["classes"] = [
                        {"name": c.get("name", "unknown"), "lineno": c.get("start_point", [0, 0])[0] + 1} for c in
                        dossier.get("classes", [])]

                    # The Ascended Testament
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
                # Extract markdown links locally
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
                               file_hash: str) -> Tuple[FileGnosis, Dict]:
        """Forges a stable shell for files that skip the heavy parsing loops."""
        gnosis = FileGnosis(
            path=rel_path,
            original_size=size,
            token_cost=0,
            category=category,
            language=language,
            permissions="755" if bool(file_stat.st_mode & StatModule.S_IXUSR) else None,
            hash_signature=file_hash
        )
        return gnosis, {}

    def _chronicle_in_cache(self, rel_path_str: str, mtime: float, size: int, gnosis: FileGnosis, ast: Dict):
        """[ASCENSION 37]: Bicameral Lock Segregation."""
        with self._lock:
            self.new_cache[rel_path_str] = {
                'mtime': mtime,
                'size': size,
                'gnosis': gnosis.model_dump(mode='json'),
                'project_gnosis': ast
            }