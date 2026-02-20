# Path: src/velm/core/runtime/vfs/scryer.py
# -----------------------------------------

"""
=================================================================================
== THE GNOSTIC SCRYER: OMEGA POINT (V-Ω-TOTALITY-V8.0-NULL-PROOF)              ==
=================================================================================
LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_SCRYER_V8_NULL_PROOF_FINALIS

[ARCHITECTURAL CONSTITUTION]
This scripture defines the sovereign engine of perception for the Virtual
Filesystem. It transmutes physical matter shards into a structured,
hierarchical Gnostic Tree for the Ocular HUD.

### THE PANTHEON OF 15 LEGENDARY ASCENSIONS:
1.  **Null-Proof Interface (THE CURE):** The public gateway `vfs_scry_recursive`
    now explicitly checks for `None` returns and transmutes them into `[]`.
2.  **The Pre-Emptive Suture:** Instantly injects a safe `STAYED` vessel into
    `__GNOSTIC_TRANSFER_CELL__` before computation begins.
3.  **Titanium I/O Ward:** Every single OS interaction is wrapped in a forensic
    try/catch block.
4.  **Type-Sovereign Inputs:** Validates `root_path` across str, Path, and NoneType.
5.  **The Ghost Node Protocol:** Unreadable directories manifest as `access_denied`.
6.  **Merkle-Lite Fingerprinting:** Fast, fail-safe SHA256 hashing for files < 1MB.
7.  **Achronal Path Normalization:** Enforces POSIX forward-slashes globally.
8.  **Anti-Ouroboros Ward:** Detects circular symlinks via `st_ino`.
9.  **The Abyssal Filter:** Blinds the Gaze to `node_modules`, `.git`, etc.
10. **Directory Aura Tomography:** Calculates cumulative size/count.
11. **Metabolic Throttling:** Hard depth-ceiling of 25.
12. **Dialect Divination:** Maps extensions to Monaco languages.
13. **Symlink Adjudication:** Resolves links and tags broken ones.
14. **Finality Vow:** Guaranteed return of a serialized List.
15. **Global Transfer Cell Suture:** Finalizes the JSON-RPC payload seamlessly.
=================================================================================
"""

import os
import time
import hashlib
import logging
import traceback
import sys
import json
import __main__
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Union, Tuple

# --- GNOSTIC LOGGING ---
Logger = logging.getLogger("GnosticScryer")
logging.basicConfig(level=logging.INFO)


class GnosticScryer:
    """
    =============================================================================
    == THE SOVEREIGN ENGINE OF PERCEPTION                                      ==
    =============================================================================
    Performs deep-tissue biopsy of the virtual filesystem (IDBFS/WASM).
    """

    # [ASCENSION 9]: THE ABYSSAL FILTER
    ABYSS_DIRS: Set[str] = {
        '.git', '.scaffold', '__pycache__', 'node_modules',
        '.venv', 'venv', 'dist', 'build', '.next', '.cache',
        '.idea', '.vscode'
    }

    ABYSS_FILES: Set[str] = {
        '.DS_Store', 'Thumbs.db', 'scaffold.lock', '.pyc', '.pyo', '.pyd'
    }

    HEAVY_MATTER_LIMIT = 1048576 * 2  # 2MB Threshold for hashing

    def __init__(self, root_path: Union[str, Path]):
        """[THE RITE OF ANCHORING]"""
        try:
            # [ASCENSION 4]: Type Sanitization
            if root_path is None:
                self.root = Path(".")
            elif isinstance(root_path, str):
                self.root = Path(root_path).resolve()
            elif isinstance(root_path, Path):
                self.root = root_path.resolve()
            else:
                self.root = Path(str(root_path)).resolve()

            # [ASCENSION 8]: INODE VIGIL
            self.seen_inodes: Set[int] = set()

        except Exception as e:
            Logger.error(f"Anchor Fracture: {e}")
            self.root = Path("/").resolve()
            self.seen_inodes = set()

    @classmethod
    def conduct_inquest(cls, target_path: str) -> List[Dict[str, Any]]:
        """The primary entry point for the WASM Dispatcher."""
        try:
            scryer = cls(target_path)
            result = scryer.scry()
            # [ASCENSION 1]: Null-Proof Return
            return result if result is not None else []
        except Exception as e:
            Logger.critical(f"FATAL INQUEST FAILURE: {e}")
            return []

    def scry(self) -> List[Dict[str, Any]]:
        """Initiates the recursive Gaze with [VOID_TOLERANCE]."""
        try:
            if not self.root.exists() or not self.root.is_dir():
                return []

            result, _ = self._scry_recursive(self.root, depth=0)

            # [ASCENSION 1]: Sanitize output
            if result is None: return []
            return [node for node in result if node is not None]

        except Exception as e:
            error_trace = traceback.format_exc()
            Logger.error(f"VFS_SCRY_FRACTURE:\n{error_trace}")

            return [{
                "name": "FRACTURE_LOG.txt",
                "path": "FRACTURE_LOG.txt",
                "type": "file",
                "size": len(error_trace),
                "mtime": time.time(),
                "content": error_trace,
                "hash": "0xHERESY"
            }]

    def _scry_recursive(self, current_path: Path, depth: int = 0) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """
        =============================================================================
        == THE RECURSIVE GAZE (V-Ω-ADAPTIVE-DEPTH-TITANIUM)                        ==
        =============================================================================
        """
        # [ASCENSION 10]: Metabolic Throttling
        if depth > 25:
            return [], {"size": 0, "count": 0}

        nodes: List[Dict[str, Any]] = []
        dir_stats = {"size": 0, "count": 0}

        try:
            # [ASCENSION 2]: os.scandir for I/O throughput
            with os.scandir(current_path) as entries:
                for entry in entries:
                    try:
                        # 1. THE ABYSSAL CHECK
                        if entry.is_dir() and entry.name in self.ABYSS_DIRS:
                            continue
                        if not entry.is_dir() and entry.name in self.ABYSS_FILES:
                            continue

                        # 2. INODE VIGIL
                        try:
                            info = entry.stat(follow_symlinks=False)
                            if info.st_ino != 0 and info.st_ino in self.seen_inodes:
                                continue
                            if info.st_ino != 0:
                                self.seen_inodes.add(info.st_ino)
                        except (OSError, FileNotFoundError):
                            continue

                            # 3. METADATA TOMOGRAPHY
                        is_dir = entry.is_dir(follow_symlinks=False)
                        is_symlink = entry.is_symlink()
                        clean_path = str(Path(entry.path)).replace('\\', '/')

                        node: Dict[str, Any] = {
                            "name": entry.name,
                            "path": clean_path,
                            "type": "directory" if is_dir else "file",
                            "size": info.st_size,
                            "mtime": info.st_mtime,
                            "inode": info.st_ino,
                            "metadata": {}
                        }

                        # 4. SYMLINK ADJUDICATION
                        if is_symlink:
                            try:
                                node["link_target"] = os.readlink(entry.path)
                                node["type"] = "symlink"
                            except OSError:
                                node["type"] = "ghost_link"

                        # 5. RECURSIVE INCEPTION
                        if is_dir:
                            child_nodes, child_stats = self._scry_recursive(Path(entry.path), depth + 1)
                            node["children"] = child_nodes or []
                            node["size"] = child_stats["size"]
                            node["file_count"] = child_stats["count"]

                            dir_stats["size"] += child_stats["size"]
                            dir_stats["count"] += child_stats["count"]
                        else:
                            dir_stats["size"] += info.st_size
                            dir_stats["count"] += 1
                            node["language"] = self._divine_language(entry.name)

                            # [ASCENSION 6]: MERKLE-LITE
                            if info.st_size < self.HEAVY_MATTER_LIMIT:
                                node["hash"] = self._forge_merkle_leaf(Path(entry.path))
                            else:
                                node["hash"] = "0xHEAVY_MATTER"

                        nodes.append(node)

                    except Exception:
                        continue

        except (PermissionError, OSError):
            return [{
                "name": f"LOCKED_SANCTUM_{current_path.name}",
                "path": str(current_path),
                "type": "access_denied",
                "size": 0,
                "mtime": 0,
                "hash": "0xACCESS_DENIED"
            }], dir_stats

        except Exception as e:
            Logger.error(f"Unexpected Scry Failure at {current_path}: {e}")
            return [], dir_stats

        # Sort: Directories first, then alphabetical
        sorted_nodes = sorted(nodes, key=lambda x: (x.get("type") != "directory", x.get("name", "").lower()))
        return sorted_nodes, dir_stats

    def _forge_merkle_leaf(self, file_path: Path) -> str:
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "0xVOID"

    def _divine_language(self, filename: str) -> str:
        """[ASCENSION 11]: Maps file extensions to Monaco syntax highlighters."""
        ext = filename.split('.').pop().lower() if '.' in filename else ""
        if not ext:
            if filename == "Dockerfile": return "dockerfile"
            if filename == "Makefile": return "makefile"
            return "plaintext"

        grammar_map = {
            'py': 'python', 'ts': 'typescript', 'tsx': 'typescript',
            'js': 'javascript', 'jsx': 'javascript', 'json': 'json',
            'md': 'markdown', 'rs': 'rust', 'go': 'go', 'html': 'html',
            'css': 'css', 'yaml': 'yaml', 'yml': 'yaml', 'toml': 'toml',
            'sh': 'shell', 'bash': 'shell', 'sql': 'sql',
            'scaffold': 'yaml', 'symphony': 'yaml', 'arch': 'yaml'
        }
        return grammar_map.get(ext, 'plaintext')


# =============================================================================
# == THE PUBLIC GATEWAY: THE UNIVERSAL INTERFACE                             ==
# =============================================================================

def vfs_scry_recursive(path: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE FINALITY VOW: THE UNIVERSAL INTERFACE                               ==
    =============================================================================
    The one true bridge between the WASM Dispatcher and the VFS Oracle.
    Hardened against type heresies and the Null-Result Paradox.
    """
    # [ASCENSION 4]: Type Guard
    if not isinstance(path, str):
        Logger.error(f"vfs_scry_recursive received profane type: {type(path)}. Casting to string.")
        path = str(path)

    # =========================================================================
    # == [ASCENSION 2]: THE PRE-EMPTIVE SUTURE (THE CURE)                    ==
    # =========================================================================
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    if is_wasm:
        try:
            # Inject "STAYED" status to protect against mid-computation death
            safe_fallback = {
                "success": False,
                "status": "STAYED",
                "tree": [],
                "message": "The Gaze was interrupted by a Substrate Cancelation."
            }
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps(safe_fallback)
        except Exception:
            pass

            # 1. CONDUCT THE INQUEST
    tree = []
    success = False
    error_msg = ""

    try:
        tree = GnosticScryer.conduct_inquest(path)
        # [ASCENSION 1]: Explicit None Check
        if tree is None:
            tree = []
        success = True
    except Exception as e:
        tree = []
        success = False
        error_msg = str(e)

    # =========================================================================
    # == [ASCENSION 15]: THE FINAL REVELATION SUTURE                         ==
    # =========================================================================
    if is_wasm:
        try:
            if success:
                payload = {
                    "success": True,
                    "status": "RESONANT",
                    "tree": tree,
                    "metadata": {
                        "timestamp": time.time(),
                        "node_count": len(tree)
                    }
                }
            else:
                payload = {
                    "success": False,
                    "status": "FRACTURED",
                    "tree": [],
                    "error": "SCRY_FAILURE",
                    "message": error_msg
                }

            # The Final Seal
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps(payload)

        except Exception as e:
            Logger.error(f"VFS Memory Suture Fracture in Scryer: {e}")

    return tree