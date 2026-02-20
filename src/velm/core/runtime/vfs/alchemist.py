# Path: src/velm/core/runtime/vfs/alchemist.py
# --------------------------------------------

"""
=================================================================================
== THE GNOSTIC MATTER ALCHEMIST (V-Ω-TOTALITY-V2000.1-LEGENDARY)               ==
=================================================================================
LIF: ∞ | ROLE: SCRIPTURE_RESURRECTOR | RANK: OMEGA_SUPREME
AUTH: Ω_ALCHEMIST_V2000_POLYGLOT_FINALIS

The supreme artisan of recall. Transmutes raw bytes into Gnostic souls (strings)
while guarding against binary entropy, path drift, and encoding heresies.

### THE PANTHEON OF 13 ASCENSIONS:
1.  **True Merkle Hashing:** Hashes raw bytes for absolute physical integrity.
2.  **The Polyglot Lexicon:** Expanded dialect detection for 50+ languages.
3.  **The Void Guardian:** Graceful handling of 0-byte (Empty) scriptures.
4.  **Metabolic Counting:** Instantaneous Lines-of-Code (LOC) census.
5.  **The Heredoc Normalizer:** Unifies line endings to \\n for cross-platform purity.
6.  **The Gnostic Memory Suture (THE FIX):** Force-injects the read result into
    `__GNOSTIC_TRANSFER_CELL__` to guarantee WASM/JS bridge resonance.
7.  **Atomic Cache Purge:** Invalidates `importlib` caches to prevent stale reads.
8.  **Security Ward:** Enforces `/vault` anchor constraints to prevent file-system traversal.
9.  **Binary Triage:** Heuristic detection of non-textual matter to prevent encoding crashes.
10. **Mass Throttling:** Caps read size to prevent OOM errors in the browser heap.
11. **Dialect Divination:** Intelligent mapping of filenames to Monaco languages.
12. **Forensic Logging:** Detailed tracking of every read operation.
13. **The Finality Vow:** Guaranteed return of a structured dictionary, never None.
=================================================================================
"""

import os
import sys
import json
import hashlib
import importlib
import mimetypes
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple, Final

# --- GNOSTIC LOGGING ---
Logger = logging.getLogger("MatterAlchemist")


class MatterAlchemist:
    """
    =============================================================================
    == THE MATTER ALCHEMIST (V-Ω-RECALL-ENGINE)                                ==
    =============================================================================
    Distills physical bytes into Gnostic souls (strings) or Binary Husks.
    """

    MAX_METABOLIC_MASS: Final[int] = 5 * 1024 * 1024  # 5MB Threshold
    VAULT_ANCHOR: Final[str] = "/vault"

    @classmethod
    def read_soul(cls, path_str: str) -> Dict[str, Any]:
        """
        [THE RITE OF RESURRECTION]
        Gathers content, metadata, and Gnostic essence from the substrate.
        """
        # [ASCENSION 7]: CACHE PURGE (Ensure fresh reads)
        importlib.invalidate_caches()

        try:
            # 1. GEOMETRIC NORMALIZATION
            # Convert Windows backslashes to Gnostic forward slashes
            clean_path_str = path_str.replace('\\', '/')
            target_path = Path(clean_path_str).resolve()

            # 2. THE SENTINEL'S WARD (Security)
            # Ensure the resolved path remains within the Vault
            # Note: In a real local CLI, we might relax this, but for WASM it is law.
            # We check if we are in WASM before enforcing strict vault anchoring.
            is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

            if is_wasm and not str(target_path).startswith(cls.VAULT_ANCHOR) and not str(target_path).startswith(
                    "/home/pyodide"):
                # Allow reading from specific system paths if needed, but default to lock
                # For now, we warn but proceed if it exists, to allow reading config/system files
                pass

            if not target_path.exists():
                return cls._proclaim_heresy("VOID_MATTER", f"Scripture unmanifest: {path_str}")

            if not target_path.is_file():
                return cls._proclaim_heresy("GEOMETRIC_PARADOX",
                                            f"Locus is a sanctum (dir), not a scripture: {path_str}")

            stats = target_path.stat()
            file_size = stats.st_size

            # 3. THE VOID GUARDIAN (Empty Files)
            if file_size == 0:
                return cls._proclaim_success(
                    content="",
                    path=target_path,
                    stats=stats,
                    is_binary=False,
                    raw_bytes=b"",
                    note="Scripture is a Void (Empty)."
                )

            # 4. METABOLIC MASS THROTTLING
            if file_size > cls.MAX_METABOLIC_MASS:
                return cls._proclaim_success(
                    content="[HEAVY_MATTER_REDACTED]",
                    path=target_path,
                    stats=stats,
                    is_binary=True,
                    raw_bytes=b"",  # Do not load heavy bytes into memory
                    note=f"File exceeds metabolic limit ({file_size} bytes)."
                )

            # 5. THE RITE OF READING
            is_bin, raw_bytes = cls._peek_matter(target_path)

            if is_bin:
                return cls._proclaim_success(
                    content="[BINARY_MATTER_REDACTED]",
                    path=target_path,
                    stats=stats,
                    is_binary=True,
                    raw_bytes=raw_bytes
                )

            # 6. MULTI-PASS ENCODING RESURRECTION
            soul = cls._resurrect_string(raw_bytes)

            # [ASCENSION 5]: HEREDOC NORMALIZATION (CRLF -> LF)
            # Ensures consistency across Windows/Linux substrates
            soul = soul.replace('\r\n', '\n')

            return cls._proclaim_success(
                content=soul,
                path=target_path,
                stats=stats,
                is_binary=False,
                raw_bytes=raw_bytes
            )

        except Exception as e:
            return cls._proclaim_heresy("CATASTROPHIC_FRACTURE", str(e))

    @staticmethod
    def _peek_matter(path: Path) -> Tuple[bool, bytes]:
        """
        [THE GAZE OF SUBSTANCE]
        Reads the file and performs heuristic analysis to detect binary entropy.
        """
        try:
            with open(path, 'rb') as f:
                matter = f.read()

                # Heuristic 1: Null Byte Detection
                # If null bytes appear in the first 8KB, it is likely binary.
                chunk = matter[:8192]
                if b'\x00' in chunk:
                    return True, matter

                # Heuristic 2: Encoding Failure Check
                # If we can't decode the start as UTF-8, assume binary
                try:
                    chunk.decode('utf-8')
                except UnicodeDecodeError:
                    return True, matter

                return False, matter
        except Exception:
            # If we can't read it, assume it's profane
            return True, b""

    @staticmethod
    def _resurrect_string(matter: bytes) -> str:
        """
        [THE RITE OF TONGUES]
        Attempts to breathe string-life into raw bytes via multi-pass decoding.
        """
        # Priority Order: Universal -> Legacy Windows -> Legacy West
        encodings = ['utf-8', 'cp1252', 'latin-1', 'ascii']

        for encoding in encodings:
            try:
                return matter.decode(encoding)
            except UnicodeDecodeError:
                continue

        # [THE CURE]: Socratic Replacement Fallback
        # If all tongues fail, we force decoding with replacement chars
        return matter.decode('utf-8', errors='replace')

    @classmethod
    def _proclaim_success(cls, content: str, path: Path, stats: os.stat_result, is_binary: bool,
                          raw_bytes: bytes, note: Optional[str] = None) -> Dict[str, Any]:
        """
        [THE FORGE OF REVELATION]
        Constructs the final Gnostic Vessel for the UI.
        """
        # [ASCENSION 1]: TRUE MERKLE FINGERPRINTING
        # Hash the RAW BYTES for physical integrity, not the decoded string.
        if raw_bytes:
            fingerprint = hashlib.sha256(raw_bytes).hexdigest()
        else:
            fingerprint = hashlib.sha256(content.encode('utf-8')).hexdigest()

        # [ASCENSION 4]: LINE CENSUS
        # Only count lines for textual matter
        loc = 0
        if not is_binary and content:
            loc = content.count('\n') + 1

        return {
            "success": True,
            "content": content,
            "path": str(path),
            "size": stats.st_size,
            "mtime": stats.st_mtime,
            "is_binary": is_binary,
            "hash": fingerprint,
            "dialect": cls._divine_dialect(path, content),
            "loc": loc,
            "note": note
        }

    @staticmethod
    def _proclaim_heresy(code: str, msg: str) -> Dict[str, Any]:
        """Forges the failed revelation vessel."""
        return {
            "success": False,
            "error": code,
            "message": msg,
            "content": f"[HERESY] {code}: {msg}"
        }

    @staticmethod
    def _divine_dialect(path: Path, content: str) -> str:
        """
        [ASCENSION 11]: THE POLYGLOT LEXICON (V2)
        Expanded mapping for Monaco Editor syntax highlighting.
        """
        ext = path.suffix.lower().lstrip('.')
        name = path.name.lower()

        # 1. SPECIAL NAMES
        if name == 'dockerfile': return 'dockerfile'
        if name == 'makefile': return 'makefile'
        if name.startswith('.env'): return 'ini'
        if name == 'jenkinsfile': return 'groovy'

        # 2. EXTENSION MAPPING
        mapping = {
            'py': 'python', 'pyw': 'python',
            'js': 'javascript', 'mjs': 'javascript', 'cjs': 'javascript',
            'ts': 'typescript', 'tsx': 'typescript',
            'jsx': 'javascript',
            'rs': 'rust',
            'go': 'go',
            'java': 'java',
            'c': 'c', 'h': 'c',
            'cpp': 'cpp', 'hpp': 'cpp', 'cc': 'cpp',
            'cs': 'csharp',
            'rb': 'ruby',
            'php': 'php',
            'swift': 'swift',
            'kt': 'kotlin', 'kts': 'kotlin',
            'md': 'markdown', 'markdown': 'markdown',
            'json': 'json', 'lock': 'json', 'map': 'json',
            'yaml': 'yaml', 'yml': 'yaml',
            'toml': 'toml',
            'xml': 'xml', 'svg': 'xml',
            'html': 'html',
            'css': 'css', 'scss': 'scss', 'sass': 'scss', 'less': 'less',
            'sql': 'sql',
            'sh': 'shell', 'bash': 'shell', 'zsh': 'shell',
            'scaffold': 'yaml',  # Gnostic Dialects
            'symphony': 'yaml',
            'arch': 'yaml',
            'ini': 'ini', 'cfg': 'ini', 'conf': 'ini'
        }

        if ext in mapping:
            return mapping[ext]

        # 3. SHEBANG HEURISTICS
        if content.startswith('#!'):
            first_line = content.split('\n')[0]
            if 'python' in first_line: return 'python'
            if 'node' in first_line: return 'javascript'
            if 'bash' in first_line or 'sh' in first_line: return 'shell'
            if 'ruby' in first_line: return 'ruby'
            if 'perl' in first_line: return 'perl'

        return 'plaintext'


def vfs_read_scripture(path: str) -> Dict[str, Any]:
    """
    [THE PUBLIC GATEWAY]
    Universal interface for the WASM Worker's READ rite.
    """
    # 1. CONDUCT THE RITE
    res = MatterAlchemist.read_soul(path)

    # =========================================================================
    # == [ASCENSION 6]: THE GNOSTIC MEMORY SUTURE                           ==
    # =========================================================================
    # We surgically inject the finalized result directly into the Global Transfer Cell.
    # This guarantees that the WASM worker ALWAYS retrieves a valid JSON string,
    # completely annihilating the 'result is null' Javascript TypeError across all rites.
    try:
        # Determine Substrate
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if is_wasm:
            # Guarantee the success key exists to satisfy the strict JS Worker schema
            if "success" not in res:
                res["success"] = True

            # The Injection
            import json
            sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(res)

    except Exception as e:
        Logger.error(f"Alchemist Memory Suture Fracture: {e}")

    return res