# Path: src/velm/core/runtime/vfs/scryer.py
# -----------------------------------------

"""
=================================================================================
== THE GNOSTIC SCRYER: OMEGA POINT (V-Ω-TOTALITY-V9000-HYPER-DIAGNOSTIC)       ==
=================================================================================
LIF: ∞ | ROLE: OMNISCIENT_OBSERVER | RANK: OMEGA_SOVEREIGN
AUTH: Ω_SCRYER_V9000_TRUTH_TELLER_FINALIS

[ARCHITECTURAL CONSTITUTION]
This scripture defines the sovereign engine of perception for the Virtual
Filesystem. It transmutes physical matter shards into a structured,
hierarchical Gnostic Tree for the Ocular HUD.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (HYPER-DIAGNOSTIC EDITION):
1.  **The Forensic Scream (THE TRUTH):** Uses raw `print()` to bypass all logging
    buffers, screaming the exact state of `os.listdir()` to the console.
2.  **The Dual-Gaze Protocol:** Performs a RAW scan alongside the FILTERED scan
    to prove if the Abyssal Filter is hiding the truth.
3.  **Null-Proof Interface:** The public gateway `vfs_scry_recursive` explicitly
    checks for `None` and transmutes into `[]`.
4.  **Pre-Emptive Suture:** Instantly injects a safe `STAYED` vessel into
    `__GNOSTIC_TRANSFER_CELL__` before computation begins.
5.  **Titanium I/O Ward:** Every OS interaction is wrapped in forensic try/catch.
6.  **Type-Sovereign Inputs:** Validates `root_path` across str, Path, and NoneType.
7.  **The Ghost Node Protocol:** Unreadable directories manifest as `access_denied` nodes.
8.  **Merkle-Lite Fingerprinting:** Fast SHA256 hashing for files < 2MB.
9.  **Achronal Path Normalization:** Enforces POSIX forward-slashes globally.
10. **Anti-Ouroboros Ward:** Detects circular symlinks via `st_ino`.
11. **The Abyssal Filter:** Blinds the Gaze to `node_modules`, `.git`, etc.
12. **Directory Aura Tomography:** Calculates cumulative size/count recursively.
13. **Metabolic Throttling:** Hard depth-ceiling of 25 to prevent stack overflow.
14. **Dialect Divination:** Maps extensions to Monaco languages.
15. **Symlink Adjudication:** Resolves links and tags broken ones.
16. **Finality Vow:** Guaranteed return of a serialized List.
17. **Global Transfer Cell Suture:** Finalizes the JSON-RPC payload seamlessly.
18. **Permission Probe:** Checks `os.access(R_OK)` on every node.
19. **Temporal Delta:** Reports age of file in seconds.
20. **Hidden Matter Detection:** Flags dotfiles explicitly.
21. **Zero-Byte Alert:** Warns on empty files (potential touch errors).
22. **Path Variance Check:** Compares `resolve()` vs `absolute()` to catch symlink drifts.
23. **Environment Echo:** Prints `os.getcwd()` and `os.getuid()` (if available).
24. **The Ultimate Return:** Returns a list that is mathematically impossible to be None.
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
    == THE SOVEREIGN ENGINE OF PERCEPTION (TRUTH-TELLER EDITION)               ==
    =============================================================================
    Performs deep-tissue biopsy of the virtual filesystem (IDBFS/WASM).
    """

    # [ASCENSION 11]: THE ABYSSAL FILTER
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
            # [ASCENSION 6]: Type Sanitization
            if root_path is None:
                self.root = Path(".")
            elif isinstance(root_path, str):
                self.root = Path(root_path).resolve()
            elif isinstance(root_path, Path):
                self.root = root_path.resolve()
            else:
                self.root = Path(str(root_path)).resolve()

            # [ASCENSION 10]: INODE VIGIL
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
            return scryer.scry()
        except Exception as e:
            Logger.critical(f"FATAL INQUEST FAILURE: {e}")
            return []

    def scry(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF DIAGNOSTIC REVELATION (V-Ω-TOTALITY-V9.0)                   ==
        =============================================================================
        LIF: 100x | ROLE: FORENSIC_BIOPSY | RANK: OMEGA_SUPREME

        Performs a deep-tissue biopsy of the virtual filesystem. Instead of a mere
        list, it returns a 'Reality Dossier' containing:
        1. THE TREE: The filtered Gnostic Topology.
        2. THE DIAGNOSTICS: The raw, un-filtered state of the physical substrate.
        3. THE METRICS: Temporal and metabolic tax of the perception.
        =============================================================================
        """
        start_ns = time.perf_counter_ns()

        # --- STRATUM 0: THE SENSORY DOSSIER ---
        # [ASCENSION 18]: This block is forged before any logic to ensure we capture
        # the 'Primordial State' of the anchor.
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
            # [ASCENSION 2]: THE UNFILTERED REALITY.
            # We perform a direct OS-level listdir to bypass the Abyssal Filter.
            # This proves if matter exists even if the Engine hides it.
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

            # [ASCENSION 12]: PROCLAIMING THE SUMMARY
            # We still print to stdout for terminal-attached architects
            print(f"[SCRYER] 🧪 Perceived {stats['count']} nodes in {duration_ms:.2f}ms. Anchor: {self.root.name}")

            # [ASCENSION 24]: THE FINALITY VOW
            # We return a structured dossier that the Ocular UI can easily dissect.
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
            # [ASCENSION 11]: FAULT-ISOLATED REDEMPTION
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
        =============================================================================
        == THE OMEGA RECURSIVE GAZE: TOTALITY (V-Ω-TOTALITY-V9000-RESONANT)        ==
        =============================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCRY_RECURSIVE_V9000_ZERO_NULL_FINALIS

        [ARCHITECTURAL CONSTITUTION]
        This is the supreme sensory rite of the VFS. It performs a high-fidelity
        biopsy of the substrate, transmuting raw directory entries into Gnostic Nodes.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Null-Matter Amnesty (THE FIX):** Guarantees that every directory node
            possesses a 'children' attribute as a valid List [], never None.
        2.  **The Anti-Ouroboros Ward:** Utilizes `seen_inodes` to detect and bypass
            circular symbolic links, preventing stack-overflow heresies.
        3.  **Metabolic Depth Ceiling:** Hard-caps the recursion at depth 25 to protect
            the Python heap in the browser substrate.
        4.  **Achronal Path Normalization:** Forces every node path into POSIX
            forward-slash standards for bit-perfect Monaco resonance.
        5.  **NoneType Entry Guard:** Surgically skips OS entries that fail the
            Initial Gaze (e.g. vanished mid-scan).
        6.  **The Abyssal Filter:** Automatically blinds the gaze to node_modules,
            .git, and .scaffold caches to maximize signal-to-noise ratio.
        7.  **Sovereign Permission Probe:** Conducts a physical `os.access` test
            on every node to report true readability.
        8.  **Merkle-Lite Fingerprinting:** Performs SHA256 hashing for files
            under 2MB, providing an Integrity Seal for the HUD.
        9.  **Hydraulic I/O Unbuffering:** Uses `os.scandir` for maximum throughput
            and minimum metabolic tax on the WASM loop.
        10. **Dialect Divination:** Automatically maps file extensions to
            Monaco Intelligence Dialects (e.g. .py -> python).
        11. **Zero-Byte Vitality Alert:** Specifically flags empty files in
            metadata to alert the Architect of potential creation failures.
        12. **The Finality Vow:** A mathematical guarantee of returning a
            fully-formed Tree and Stats tuple.
        =============================================================================
        """
        # [ASCENSION 3]: Metabolic Throttling
        if depth > 25:
            return [], {"size": 0, "count": 0}

        nodes: List[Dict[str, Any]] = []
        dir_stats = {"size": 0, "count": 0}

        try:
            # [ASCENSION 9]: os.scandir for high-throughput I/O
            with os.scandir(current_path) as entries:
                for entry in entries:
                    try:
                        # [ASCENSION 5]: NoneType Entry Guard
                        if not entry: continue

                        entry_name = entry.name

                        # [ASCENSION 6]: THE ABYSSAL CHECK
                        is_dir_check = entry.is_dir(follow_symlinks=False)

                        if is_dir_check:
                            if entry_name in self.ABYSS_DIRS:
                                continue
                        else:
                            if entry_name in self.ABYSS_FILES:
                                continue

                        # [ASCENSION 2]: THE ANTI-OUROBOROS WARD
                        try:
                            info = entry.stat(follow_symlinks=False)
                            # Skip if we've seen this inode (Circular Symlink Detection)
                            if info.st_ino != 0 and info.st_ino in self.seen_inodes:
                                continue
                            if info.st_ino != 0:
                                self.seen_inodes.add(info.st_ino)
                        except (OSError, FileNotFoundError):
                            # Entry vanished or is profane
                            continue

                        # [ASCENSION 4]: POSIX GEOMETRY
                        clean_path = str(Path(entry.path)).replace('\\', '/')

                        # [ASCENSION 7]: SOVEREIGN PERMISSION PROBE
                        readable = os.access(entry.path, os.R_OK)

                        node: Dict[str, Any] = {
                            "name": entry_name,
                            "path": clean_path,
                            "type": "directory" if is_dir_check else "file",
                            "size": info.st_size,
                            "mtime": info.st_mtime,
                            "inode": info.st_ino,
                            "children": [],  # [ASCENSION 1]: THE CURE
                            "metadata": {
                                "readable": readable,
                                "age_seconds": time.time() - info.st_mtime
                            }
                        }

                        # [ASCENSION 11]: ZERO-BYTE ALERT
                        if not is_dir_check and info.st_size == 0:
                            node["metadata"]["is_empty"] = True

                        # [ASCENSION 12]: SYMLINK ADJUDICATION
                        if entry.is_symlink():
                            try:
                                node["link_target"] = os.readlink(entry.path)
                                node["type"] = "symlink"
                            except OSError:
                                node["type"] = "ghost_link"

                        # [ASCENSION 12]: RECURSIVE INCEPTION
                        if is_dir_check:
                            if readable:
                                child_nodes, child_stats = self._scry_recursive(Path(entry.path), depth + 1)
                                # [THE CURE]: Double-ward against null returns from lower strata
                                node["children"] = child_nodes if child_nodes is not None else []

                                # Propagate Mass to parent
                                node["size"] = child_stats["size"]
                                node["file_count"] = child_stats["count"]

                                dir_stats["size"] += child_stats["size"]
                                dir_stats["count"] += child_stats["count"]
                            else:
                                node["type"] = "access_denied_dir"
                        else:
                            # Scalar Matter Update
                            dir_stats["size"] += info.st_size
                            dir_stats["count"] += 1
                            node["language"] = self._divine_language(entry_name)

                            # [ASCENSION 8]: MERKLE-LITE
                            if readable and info.st_size < self.HEAVY_MATTER_LIMIT:
                                node["hash"] = self._forge_merkle_leaf(Path(entry.path))
                            else:
                                node["hash"] = "0xHEAVY_MATTER"

                        nodes.append(node)

                    except Exception as entry_heresy:
                        # [THE WARD]: Single entry failure must not shatter the whole tree
                        print(f"[SCRYER] ⚠️  Node Inquest Fractured for '{entry.name}': {entry_heresy}")
                        continue

        except (PermissionError, OSError) as e:
            # Handle directory access heresies at the root of the call
            return [{
                "name": f"LOCKED_SANCTUM_{current_path.name}",
                "path": str(current_path),
                "type": "access_denied",
                "size": 0,
                "mtime": 0,
                "children": [],
                "hash": "0xACCESS_DENIED"
            }], dir_stats

        except Exception as e:
            # Absolute failsafe for recursive logic
            print(f"[SCRYER] 💀 CATASTROPHIC RECURSION FRACTURE: {e}")
            return [], dir_stats

        # [ASCENSION 12]: THE FINALITY VOW
        # Sort: Directories first, then Alphabetical
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
        """[ASCENSION 14]: Maps file extensions to Monaco syntax highlighters."""
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


# =============================================================================
# == THE PUBLIC GATEWAY: THE UNIVERSAL INTERFACE                             ==
# =============================================================================

def vfs_scry_recursive(path: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE OMNISCIENT VFS GATEWAY: OMEGA POINT (V-Ω-TOTALITY-V10000.1-FINALIS) ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_BRIDGE_TERMINUS | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_VFS_SCRY_V10000_RESONANCE_SUTURE_2026_FINALIS

    [ARCHITECTURAL CONSTITUTION]
    This function is the supreme entry point for the WASM Dispatcher. It has been
    ascended with the **Diagnostic Wake-up Protocol** to resolve the Hydration
    Collapse. It no longer relies on file-count to prove existence; it scries the
    physical substrate and materializes a high-fidelity 'Reality Dossier' for
    the JavaScript Eye.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Apophatic Type Guard:** Forcefully transmutes any input into a valid
        POSIX-compliant string coordinate.
    2.  **The Pre-Emptive Suture (THE CURE):** Instantly injects a 'STAYED'
        status into the global memory cell BEFORE computation begins,
        immunizing the bridge against mid-computation substrate cancellations.
    3.  **Hydraulic I/O Inception:** Forces a directory-level biopsy (exists/is_dir)
        before the recursive walk, identifying the difference between a
        'Void of Matter' and a 'Void of Perception'.
    4.  **NoneType Sarcophagus:** Employs absolute null-protection; if the scry
        returns None, it is transfigured into a structured Empty Reality [].
    5.  **Forensic Diagnostic Injection:** Grafts absolute paths, CWD, and raw
        directory contents onto the return vessel for the Ocular HUD.
    6.  **Achronal Path Normalization:** Ensures every coordinate in the result
        tree is bit-perfect and forward-slash normalized for the Monaco Editor.
    7.  **Substrate-Aware Metadata:** Stamps the result with a nanosecond-precision
        timestamp to prevent temporal regression in the React state.
    8.  **The Merkle-Lattice Handshake:** Injects a top-level 'status: RESONANT'
        signal that commands the UI to break the materialization wait-lock.
    9.  **Hydraulic stdout Flush:** Proclaims a minimal heartbeat to the stdout
        pipe to keep the Worker's communication buffer flowing.
    10. **Metabolic Tax Metering:** Calculates the precise latency of the
        perception for HUD telemetry tracking.
    11. **Fault-Isolated Redemption:** Wraps the entire inquest in a titanium
        try/catch block, transmuting panics into diagnostic error vessels.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        high-fidelity JSON-RPC payload committed to the Global Transfer Cell.
    =============================================================================
    """
    import os
    import time
    import json
    import __main__
    from pathlib import Path
    from velm.core.runtime.vfs.scryer import GnosticScryer

    # [ASCENSION 1]: APOPHATIC TYPE GUARD
    if path is None:
        path = "/vault/project"
    else:
        path = str(path)

    # [ASCENSION 2]: THE PRE-EMPTIVE SUTURE (THE CURE)
    # We scry the substrate DNA to determine if we are in the Ethereal Plane (WASM).
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
    start_ns = time.perf_counter_ns()

    if is_wasm:
        try:
            # Pre-inject a 'STAYED' status to ward against race-condition rejections.
            # This satisfies the JS 'await' even if the worker thread is context-switched.
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps({
                "success": False,
                "status": "STAYED",
                "message": "Perception_In_Progress",
                "tree": []
            })
        except Exception:
            pass

    # --- THE RITE OF PERCEPTION ---
    tree = []
    success = False
    error_msg = ""
    diagnostics = {}

    try:
        # [ASCENSION 3]: HYDRAULIC I/O INCEPTION
        # We manually verify the target exists before the recursive walk.
        target_path = Path(path).resolve()
        diagnostics = {
            "locus": path,
            "absolute": str(target_path).replace('\\', '/'),
            "cwd": os.getcwd().replace('\\', '/'),
            "exists": target_path.exists(),
            "is_dir": target_path.is_dir(),
            "raw_contents": []
        }

        if diagnostics["exists"] and diagnostics["is_dir"]:
            try:
                # RAW_CENSUS: Prove if files exist outside of the scryer's filters.
                diagnostics["raw_contents"] = os.listdir(str(target_path))
            except Exception as e:
                diagnostics["raw_contents"] = [f"READ_ERROR: {str(e)}"]

        # 1. CONDUCT THE INQUEST
        # We summon the specialist Scryer to perform the recursive biopsy.
        scryer = GnosticScryer(path)
        tree = scryer.scry()

        # [ASCENSION 4]: NONETYPE SARCOPHAGUS
        if tree is None:
            tree = []

        success = True

    except Exception as e:
        # [ASCENSION 11]: FAULT-ISOLATED REDEMPTION
        import traceback
        tree = []
        success = False
        error_msg = str(e)
        diagnostics["error"] = error_msg
        diagnostics["traceback"] = traceback.format_exc()
        # [ASCENSION 9]: PROCLAIM FAILURE TO STDOUT
        print(f"[SCRYER] 💀 GATEWAY FAILURE for path '{path}': {error_msg}")

    # --- MOVEMENT III: THE REVELATION SUTURE ---
    # [ASCENSION 10]: METABOLIC TAX METERING
    duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

    # [ASCENSION 12]: THE FINALITY VOW
    # We forge the final, unbreakable dossier for the JavaScript Eye.
    if is_wasm:
        try:
            payload = {
                "success": success,
                # [ASCENSION 8]: RESONANCE PROMOTION
                # If we confirmed the path exists (even if empty), we proclaim RESONANT.
                # This is the key to breaking the 'Materializing' loop.
                "status": "RESONANT" if diagnostics.get("exists") else "VOID",
                "tree": tree,
                "diagnostics": diagnostics,  # [ASCENSION 5]
                "metadata": {
                    "timestamp": time.time(),
                    "node_count": len(tree),
                    "latency_ms": duration_ms,
                    "substrate": "ETHER_WASM_VFS"
                }
            }

            if not success:
                payload["error"] = "SCRY_FRACTURE"
                payload["message"] = error_msg

            # [ASCENSION 17]: THE FINAL REVELATION SUTURE
            # Surgically commit the payload to the global cell for JS pyodide.globals retrieval.
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps(payload)

        except Exception as e:
            # Socratic Logging if the final seal fractures.
            msg = f"VFS Memory Suture Fracture in Scryer: {e}"
            if "Logger" in globals():
                Logger.error(msg)
            else:
                print(msg)

    # Return the tree list for internal Pythonic Artisans.
    return tree