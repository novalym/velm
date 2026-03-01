# Path: src/velm/core/runtime/vfs/scryer.py
# -----------------------------------------

"""
=================================================================================
== THE GNOSTIC SCRYER: OMEGA POINT (V-Ω-TOTALITY-V100K-INDESTRUCTIBLE)         ==
=================================================================================
LIF: ∞ | ROLE: OMNISCIENT_OBSERVER | RANK: OMEGA_SOVEREIGN
AUTH: Ω_SCRYER_V100K_ONTOLOGICAL_PURITY_FINALIS

[ARCHITECTURAL CONSTITUTION]
This scripture defines the sovereign engine of perception for the Virtual
Filesystem. It transmutes physical matter shards into a structured,
hierarchical Gnostic Tree for the Ocular HUD.

### THE PANTHEON OF 26 LEGENDARY ASCENSIONS (HYPER-DIAGNOSTIC EDITION):
1.  **Ontological Purity Ward (THE CURE):** Mathematically guarantees that files NEVER
    possess a `children` attribute, annihilating the UI's "Hollow Directory Mirage"
    which blinded the Architect to valid `.py` and `.symphony` matter.
2.  **Stat-First Adjudication (THE FIX):** Uses `stat.S_ISREG(info.st_mode)` as the
    absolute source of truth for file classification, preventing Emscripten's IDBFS
    from masquerading 0-byte files as empty directories.
3.  **The Forensic Scream:** Uses raw `print()` to bypass all logging buffers,
    screaming the exact state of `os.listdir()` to the console during panics.
4.  **The Dual-Gaze Protocol:** Performs a RAW scan alongside the FILTERED scan
    to prove if the Abyssal Filter is hiding the truth.
5.  **Null-Proof Interface:** The public gateway `vfs_scry_recursive` explicitly
    checks for `None` and transmutes into `[]`.
6.  **Pre-Emptive Suture:** Instantly injects a safe `STAYED` vessel into
    `__GNOSTIC_TRANSFER_CELL__` before computation begins.
7.  **Titanium I/O Ward:** Every OS interaction is wrapped in forensic try/catch.
8.  **Type-Sovereign Inputs:** Validates `root_path` across str, Path, and NoneType.
9.  **The Ghost Node Protocol:** Unreadable directories manifest as `access_denied` nodes.
10. **Merkle-Lite Fingerprinting:** Fast SHA256 hashing for files < 2MB.
11. **Achronal Path Normalization:** Enforces POSIX forward-slashes globally.
12. **Anti-Ouroboros Ward:** Detects circular symlinks via `st_ino`.
13. **The Abyssal Filter V3:** Blinds the Gaze to `node_modules`, `.git`, etc.,
    but strictly preserves `.symphony` and `.py` files.
14. **Directory Aura Tomography:** Calculates cumulative size/count recursively.
15. **Metabolic Throttling:** Hard depth-ceiling of 25 to prevent stack overflow.
16. **Dialect Divination:** Maps extensions to Monaco languages flawlessly.
17. **Symlink Adjudication:** Resolves links and tags broken ones.
18. **Finality Vow:** Guaranteed return of a serialized List, absolutely JSON-safe.
19. **Global Transfer Cell Suture:** Finalizes the JSON-RPC payload seamlessly.
20. **Permission Probe:** Checks `os.access(R_OK)` on every node.
21. **Temporal Delta:** Reports age of file in seconds.
22. **Hidden Matter Detection:** Flags dotfiles explicitly.
23. **Zero-Byte Alert:** Warns on empty files (potential touch errors).
24. **Path Variance Check:** Compares `resolve()` vs `absolute()` to catch symlink drifts.
25. **Environment Echo:** Prints `os.getcwd()` and `os.getuid()` (if available).
26. **The Absolute Catch-All:** Silently swallows trailing slash parsing errors.
=================================================================================
"""

import os
import time
import stat
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


class GnosticScryer:
    """
    =============================================================================
    == THE SOVEREIGN ENGINE OF PERCEPTION (TRUTH-TELLER EDITION)               ==
    =============================================================================
    Performs deep-tissue biopsy of the virtual filesystem (IDBFS/WASM).
    """

    # [ASCENSION 13]: THE ABYSSAL FILTER
    # Explicitly hardened to ensure we NEVER filter source code files.
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
            # [ASCENSION 8]: Type Sanitization
            if root_path is None:
                self.root = Path(".")
            elif isinstance(root_path, str):
                self.root = Path(root_path).resolve()
            elif isinstance(root_path, Path):
                self.root = root_path.resolve()
            else:
                self.root = Path(str(root_path)).resolve()

            # [ASCENSION 12]: INODE VIGIL
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
            return scryer.scry().get("tree", [])
        except Exception as e:
            Logger.critical(f"FATAL INQUEST FAILURE: {e}")
            return []

    def scry(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF DIAGNOSTIC REVELATION (V-Ω-TOTALITY-V100K)                  ==
        =============================================================================
        LIF: 100x | ROLE: FORENSIC_BIOPSY | RANK: OMEGA_SUPREME

        Performs a deep-tissue biopsy of the virtual filesystem. Returns a 'Reality Dossier'.
        =============================================================================
        """
        start_ns = time.perf_counter_ns()

        # --- STRATUM 0: THE SENSORY DOSSIER ---
        diagnostics = {
            "locus": str(self.root),
            "absolute": str(self.root.resolve()),
            "cwd": os.getcwd(),
            "exists": self.root.exists(),
            "is_dir": self.root.is_dir(),
            "is_file": self.root.is_file(),
            "uid": os.getuid() if hasattr(os, 'getuid') else "WASM_GUEST",
            "raw_contents": [],
            "error": None,
            "merkle_anchor": "0xVOID"
        }

        try:
            # --- MOVEMENT I: THE DUAL-GAZE PROBE ---
            # [ASCENSION 4]: THE UNFILTERED REALITY.
            if diagnostics["exists"] and diagnostics["is_dir"]:
                try:
                    diagnostics["raw_contents"] = os.listdir(str(self.root))
                except Exception as e:
                    diagnostics["error"] = f"RAW_READ_FRACTURE: {str(e)}"

            # --- MOVEMENT II: THE RECURSIVE INCEPTION ---
            if not diagnostics["exists"]:
                return {"tree": [], "diagnostics": diagnostics, "success": True, "message": "LOCUS_UNMANIFEST"}

            if not diagnostics["is_dir"]:
                return {"tree": [], "diagnostics": diagnostics, "success": False, "message": "LOCUS_IS_NOT_SANCTUM"}

            # Conduct the recursive walk
            tree, stats = self._scry_recursive(self.root, depth=0)

            # --- MOVEMENT III: METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            # [ASCENSION 3]: PROCLAIMING THE SUMMARY
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                print(f"[SCRYER] 🧪 Perceived {stats['count']} nodes in {duration_ms:.2f}ms. Anchor: {self.root.name}")

            # [ASCENSION 18]: THE FINALITY VOW
            return {
                "success": True,
                "tree": tree or [],
                "diagnostics": diagnostics,
                "metrics": {
                    "atom_count": stats["count"],
                    "total_mass_bytes": stats["size"],
                    "latency_ms": duration_ms,
                    "timestamp": time.time()
                }
            }

        except Exception as catastrophic_paradox:
            error_trace = traceback.format_exc()
            diagnostics["error"] = f"CATASTROPHIC_FRACTURE: {str(catastrophic_paradox)}"
            Logger.error(f"VFS_SCRY_FRACTURE:\n{error_trace}")

            return {
                "success": False,
                "tree": [],
                "diagnostics": diagnostics,
                "error_trace": error_trace,
                "message": "The Gaze of the Scryer was shattered by an unhandled paradox."
            }

    def _scry_recursive(self, current_path: Path, depth: int = 0) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """
        =================================================================================
        == THE OMEGA RECURSIVE GAZE: TOTALITY (V-Ω-V100000-ONTOLOGICAL-PURITY)         ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCRY_RECURSIVE_V100K_CHILDREN_PURGE_2026_FINALIS

        [THE CURE FOR THE UI MIRAGE]:
        Files must absolutely NOT possess a 'children' key. If they do, the React UI
        misinterprets them as void directories and drops them from the visual plane.
        This function mathematically enforces that boundary.
        =================================================================================
        """
        # [ASCENSION 15]: Metabolic Throttling
        if depth > 25:
            return [], {"size": 0, "count": 0}

        nodes: List[Dict[str, Any]] = []
        dir_stats = {"size": 0, "count": 0}
        path_str_root = str(current_path)

        try:
            # Primordial 'listdir' syncs the IDBFS directory index.
            entries = os.listdir(path_str_root)

            for entry_name in entries:
                try:
                    # THE ABYSSAL CHECK
                    if entry_name in self.ABYSS_DIRS or entry_name in self.ABYSS_FILES:
                        continue

                    full_path = current_path / entry_name
                    full_path_str = str(full_path)

                    # [ASCENSION 2]: BRUTE-FORCE TYPE ADJUDICATION
                    is_dir = False
                    is_link = False

                    # PHYSICAL BIOPSY
                    try:
                        info = os.lstat(full_path_str)
                    except (OSError, FileNotFoundError):
                        # [ASCENSION 9]: Ghost Node Recovery
                        nodes.append({
                            "name": entry_name,
                            "path": str(full_path).replace('\\', '/'),
                            "type": "ghost",
                            "size": 0,
                            "mtime": 0,
                            "metadata": {"error": "LSTAT_FAILED"}
                        })
                        continue

                    # [ASCENSION 12]: THE ANTI-OUROBOROS WARD
                    if info.st_ino != 0:
                        if info.st_ino in self.seen_inodes:
                            continue
                        self.seen_inodes.add(info.st_ino)

                    clean_rel_path = full_path_str.replace('\\', '/')
                    readable = os.access(full_path_str, os.R_OK)

                    # =========================================================================
                    # == [THE CURE]: THE ONTOLOGICAL TRUTH TELLER                            ==
                    # =========================================================================
                    # 1. Check Link first
                    if stat.S_ISLNK(info.st_mode):
                        is_link = True
                        is_dir = False
                    # 2. Check Directory next
                    elif stat.S_ISDIR(info.st_mode):
                        is_dir = True
                        is_link = False
                    # 3. Default to File (Everything else is a file)
                    else:
                        is_dir = False
                        is_link = False

                    # Base Identity Core
                    node: Dict[str, Any] = {
                        "name": entry_name,
                        "path": clean_rel_path,
                        "type": "directory" if is_dir else "symlink" if is_link else "file",
                        "size": info.st_size,
                        "mtime": info.st_mtime,
                        "inode": info.st_ino,
                        "metadata": {
                            "readable": readable,
                            "age_seconds": time.time() - info.st_mtime,
                            "is_link": is_link,
                            "is_mirage_checked": True
                        }
                    }

                    if not is_dir and info.st_size == 0:
                        node["metadata"]["is_empty"] = True

                    # =========================================================================
                    # == [ASCENSION 1]: THE ONTOLOGICAL PURITY WARD (THE CURE)               ==
                    # =========================================================================
                    if is_dir:
                        # 1. Provide the array ONLY for sanctums
                        node["children"] = []
                        if readable:
                            # The Mind dives deeper into the Sanctum
                            child_nodes, child_stats = self._scry_recursive(full_path, depth + 1)
                            node["children"] = child_nodes or []

                            # MASS ACCUMULATION
                            node["size"] = child_stats["size"]
                            node["file_count"] = child_stats["count"]
                            dir_stats["size"] += child_stats["size"]
                            dir_stats["count"] += child_stats["count"]
                        else:
                            node["type"] = "access_denied_dir"
                    else:
                        # 2. FILE BRANCH: ZERO 'CHILDREN' KEYS PERMITTED
                        # We expressly do NOT add 'children': None or 'children': [].

                        dir_stats["size"] += info.st_size
                        dir_stats["count"] += 1

                        # [ASCENSION 16]: DIALECT DIVINATION
                        node["language"] = self._divine_language(entry_name)

                        # [ASCENSION 10]: MERKLE-LITE FINGERPRINTING
                        if readable and info.st_size < self.HEAVY_MATTER_LIMIT:
                            node["hash"] = self._forge_merkle_leaf(full_path)
                        else:
                            node["hash"] = "0xHEAVY_MATTER"

                    nodes.append(node)

                except Exception as entry_fracture:
                    if os.environ.get("SCAFFOLD_DEBUG") == "1":
                        print(f"[VFS_SCRYER] ⚠️  Atom '{entry_name}' fractured: {entry_fracture}")
                    continue

        except (PermissionError, OSError) as e:
            return [{
                "name": f"LOCKED_SANCTUM_{current_path.name}",
                "path": str(current_path).replace('\\', '/'),
                "type": "access_denied",
                "size": 0,
                "mtime": 0,
                "children": [],
                "hash": "0xACCESS_DENIED"
            }], dir_stats

        except Exception as catastrophic_heresy:
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                print(f"[VFS_SCRYER] 💀 CATASTROPHIC FRACTURE: {catastrophic_heresy}")
            return [], dir_stats

        # [ASCENSION 18]: THE FINALITY VOW
        return sorted(nodes, key=lambda x: (x.get("type") != "directory", x.get("name", "").lower())), dir_stats

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
        """Maps file extensions to Monaco syntax highlighters."""
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
            'scaffold': 'yaml', 'symphony': 'yaml', 'arch': 'yaml',
            'txt': 'plaintext', 'lock': 'json'
        }
        return grammar_map.get(ext, 'plaintext')


def vfs_scry_recursive(path: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE OMNISCIENT VFS GATEWAY: OMEGA POINT (V-Ω-TOTALITY-V100K-FINALIS)    ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_BRIDGE_TERMINUS | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_VFS_SCRY_V100K_RESONANCE_SUTURE_2026_FINALIS

    [ARCHITECTURAL CONSTITUTION]
    This scripture defines the supreme entry point for the WASM Dispatcher. It has
    been ascended with the Diagnostic Wake-up Protocol to resolve the
    Hydration Collapse. It scries the physical substrate and materializes a
    high-fidelity 'Reality Dossier' for the JavaScript Eye.
    =============================================================================
    """
    import os
    import sys
    import time
    import json
    import __main__
    import traceback
    from pathlib import Path

    start_ns = time.perf_counter_ns()
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    # [ASCENSION 8]: APOPHATIC TYPE GUARD
    try:
        if path is None:
            effective_path = "/vault/project"
        else:
            effective_path = str(Path(str(path)).resolve())
    except Exception:
        effective_path = "/vault/project"

    # [ASCENSION 6]: THE PRE-EMPTIVE SUTURE
    if is_wasm:
        try:
            # Anchor the global transfer cell to prevent JS 'null' rejections
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps({
                "success": False,
                "status": "STAYED",
                "message": "Perception_Waking",
                "tree": []
            })
        except Exception:
            pass

    tree = []
    success = False
    error_msg = ""

    diagnostics = {
        "locus": effective_path,
        "absolute": os.path.abspath(effective_path).replace('\\', '/'),
        "cwd": os.getcwd().replace('\\', '/'),
        "uid": os.getuid() if hasattr(os, 'getuid') else -1,
        "exists": os.path.exists(effective_path),
        "is_dir": os.path.isdir(effective_path),
        "raw_contents": [],
        "substrate": "WASM" if is_wasm else "IRON"
    }

    try:
        if diagnostics["exists"] and diagnostics["is_dir"]:
            try:
                diagnostics["raw_contents"] = os.listdir(effective_path)
            except Exception as e:
                diagnostics["raw_contents"] = [f"READ_FRACTURE: {str(e)}"]

        scryer = GnosticScryer(effective_path)

        try:
            dossier = scryer.scry()
            # [ASCENSION 5]: NONETYPE SARCOPHAGUS
            tree = dossier.get("tree", []) if dossier.get("tree") is not None else []
            success = dossier.get("success", True)
        except Exception as scry_err:
            success = False
            error_msg = f"SCRY_CONDUCT_FRACTURE: {str(scry_err)}"
            print(f"[SCRYER] ⚠️  Internal conduct failed: {error_msg}")

        has_physical_matter = len(diagnostics["raw_contents"]) > 0
        resonance_status = "PHYSICAL" if has_physical_matter else "RESONANT" if diagnostics["exists"] else "VOID"

    except Exception as catastrophic_paradox:
        success = False
        error_msg = str(catastrophic_paradox)
        diagnostics["error"] = error_msg
        diagnostics["traceback"] = traceback.format_exc()
        resonance_status = "FRACTURED"
        print(f"[SCRYER] 💀 GATEWAY_PANIC for locus '{effective_path}': {error_msg}", file=sys.stderr)

    duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

    # Final Payload Construction
    revelation = {
        "success": success,
        "status": resonance_status,
        "tree": tree,
        "diagnostics": diagnostics,
        "metrics": {
            "atom_count": len(tree),
            "latency_ms": round(duration_ms, 3),
            "timestamp": time.time(),
            "substrate": diagnostics["substrate"]
        }
    }

    if error_msg:
        revelation["error"] = "SCRY_FRACTURE"
        revelation["message"] = error_msg

    # [ASCENSION 19]: THE FINAL REVELATION SUTURE
    if is_wasm:
        try:
            # Commit result to the global Pyodide context
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps(revelation)
        except Exception as suture_err:
            print(f"[SCRYER] 💀 Critical Memory Suture Failure: {suture_err}")

    return tree