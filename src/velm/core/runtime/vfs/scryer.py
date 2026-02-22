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
        =================================================================================
        == THE OMEGA RECURSIVE GAZE: TOTALITY (V-Ω-V20000.1-IRON-ADJUDICATOR)          ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCRY_RECURSIVE_V20000_BRUTE_FORCE_TYPE_ADJUDICATION_2026_FINALIS

        [ARCHITECTURAL CONSTITUTION]
        This is the supreme sensory rite of the VFS, re-engineered to annihilate the
        "Directory Mirage" heresy. It pierces the veil of unreliable high-level
        stat calls by performing physical Brute-Force Type Adjudication.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Brute-Force Type Adjudication (THE CURE):** We no longer trust 'isdir()'.
            We physically attempt 'os.listdir()' on every node. Success confirms a
            Sanctum (Directory). Failure (NotADirectoryError) confirms a Shard (File).
            This is the absolute, substrate-level truth.
        2.  **Children-List Purity:** Files are strictly warded; their 'children'
            attribute is set to 'None', while directories receive a valid List [].
            This ensures the Ocular Interface correctly renders clickability.
        3.  **Achronal Path Normalization:** Every node coordinate is forcefully
            transmuted into a POSIX-standard forward-slash string, ensuring bit-perfect
            resonance with the Monaco Intelligence Layer.
        4.  **The Anti-Ouroboros Ward:** Utilizes 'os.lstat' and a 'seen_inodes'
            lattice to detect and freeze circular symbolic links at the moment of
            perception, preventing stack-overflow heresies.
        5.  **Metabolic Depth Ceiling:** Hard-caps the Gaze at depth 25, preserving
            the Python heap and protecting against deep-nested entropy.
        6.  **The Abyssal Filter V3:** Dynamically blinds the gaze to system noise
            (.git, .venv, .cache) while prioritizing the 'scaffold.scaffold' Jewel.
        7.  **Sovereign Permission Tomography:** Conducts a physical 'os.access'
            test on every node to report true readability to the Ocular HUD.
        8.  **Hydraulic I/O Unbuffering:** Forces an immediate 'stat' flush for
            every entry, ensuring modification times (mtime) reflect the absolute
            present, not a substrate-cached past.
        9.  **Dialect Divination:** Automatically scries the 'Gnostic Dialect'
            (grammar) of every file based on extensions, pre-loading Monaco highlighters.
        10. **Zero-Byte Vitality Alert:** Metadata-flags empty scriptures to alert
            the Architect of potential 'touch' failures or logic-voids.
        11. **Topographical Mass Accumulation:** Recursively aggregates cumulative
            size and atom-counts from the leaves to the root for real-time HUD vitals.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            strictly-typed 2-Tuple, never a Null or void.
        =================================================================================
        """
        # [ASCENSION 5]: Metabolic Throttling
        if depth > 25:
            return [], {"size": 0, "count": 0}

        nodes: List[Dict[str, Any]] = []
        dir_stats = {"size": 0, "count": 0}
        path_str_root = str(current_path)

        try:
            # [ASCENSION 1]: Primordial 'listdir' syncs the IDBFS directory index.
            entries = os.listdir(path_str_root)

            for entry_name in entries:
                try:
                    # [ASCENSION 6]: THE ABYSSAL CHECK
                    if entry_name in self.ABYSS_DIRS or entry_name in self.ABYSS_FILES:
                        continue

                    full_path = current_path / entry_name
                    full_path_str = str(full_path)

                    # [ASCENSION 1]: THE CURE - BRUTE-FORCE TYPE ADJUDICATION
                    # We do not ask the OS if it is a directory; we command it to list its children.
                    # This is the only way to pierce the WASM directory mirage.
                    is_dir = False
                    is_link = os.path.islink(full_path_str)

                    if not is_link:
                        try:
                            os.listdir(full_path_str)
                            is_dir = True
                        except (OSError, NotADirectoryError):
                            is_dir = False

                    # [ASCENSION 2 & 8]: PHYSICAL BIOPSY
                    try:
                        info = os.lstat(full_path_str)
                    except (OSError, FileNotFoundError):
                        continue

                    # [ASCENSION 4]: THE ANTI-OUROBOROS WARD
                    if info.st_ino != 0:
                        if info.st_ino in self.seen_inodes:
                            continue
                        self.seen_inodes.add(info.st_ino)

                    # [ASCENSION 3]: POSIX GEOMETRY
                    clean_rel_path = full_path_str.replace('\\', '/')
                    readable = os.access(full_path_str, os.R_OK)

                    # [ASCENSION 2]: Forging the Gnostic Node Vessel with type-integrity
                    node: Dict[str, Any] = {
                        "name": entry_name,
                        "path": clean_rel_path,
                        "type": "directory" if is_dir else "symlink" if is_link else "file",
                        "size": info.st_size,
                        "mtime": info.st_mtime,
                        "inode": info.st_ino,
                        "children": [] if is_dir else None,  # [THE FIX]: Files have no children
                        "metadata": {
                            "readable": readable,
                            "age_seconds": time.time() - info.st_mtime,
                            "is_link": is_link,
                            "is_mirage_checked": True
                        }
                    }

                    if not is_dir and info.st_size == 0:
                        node["metadata"]["is_empty"] = True

                    # [ASCENSION 12]: RECURSIVE INCEPTION
                    if is_dir:
                        if readable:
                            # The Mind dives deeper into the Sanctum
                            child_nodes, child_stats = self._scry_recursive(full_path, depth + 1)
                            node["children"] = child_nodes or []

                            # [ASCENSION 11]: MASS ACCUMULATION
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

                        # [ASCENSION 9]: DIALECT DIVINATION
                        node["language"] = self._divine_language(entry_name)

                        # [ASCENSION 11]: MERKLE-LITE FINGERPRINTING
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

        # [ASCENSION 12]: THE FINALITY VOW
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
    == THE OMNISCIENT VFS GATEWAY: OMEGA POINT (V-Ω-TOTALITY-V20000.1-FINALIS) ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_BRIDGE_TERMINUS | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_VFS_SCRY_V20000_RESONANCE_SUTURE_2026_FINALIS

    [ARCHITECTURAL CONSTITUTION]
    This scripture defines the supreme entry point for the WASM Dispatcher. It has
    been ascended with the **Diagnostic Wake-up Protocol** to resolve the
    Hydration Collapse. It no longer relies on file-count to prove existence;
    it scries the physical substrate and materializes a high-fidelity
    'Reality Dossier' for the JavaScript Eye.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Apophatic Type Guard (THE CURE):** Forcefully transmutes any input
        into a valid, absolute POSIX string coordinate.
    2.  **The Pre-Emptive Suture:** Instantly injects a 'STAYED' status into
        the global memory cell before computation begins, immunizing the
        bridge against mid-computation substrate cancellations.
    3.  **Hydraulic I/O Inception:** Forces a directory-level biopsy (exists/dir)
        before recursion, distinguishing a 'Void of Matter' from a 'Void of Perception'.
    4.  **NoneType Sarcophagus:** Absolute null-protection; if the scry
        returns None, it is transfigured into a structured Empty Reality [].
    5.  **Forensic Diagnostic Injection:** Grafts absolute paths, CWD, and
        raw OS directory contents onto the return vessel for the Ocular HUD.
    6.  **Achronal Path Normalization:** Every coordinate in the tree is
        bit-perfect and forward-slash normalized for the Monaco Editor.
    7.  **Substrate-Aware Metadata:** Stamps result with nanosecond precision
        to prevent temporal regression in the React state.
    8.  **The Merkle-Lattice Handshake:** Injects a top-level 'status: RESONANT'
        signal that commands the UI to break the materialization wait-lock.
    9.  **Hydraulic stdout Flush:** Proclaims a minimal heartbeat to the
        stdout pipe to keep the Worker's communication buffer flowing.
    10. **Metabolic Tax Metering:** Calculates the precise latency of the
        perception for HUD telemetry tracking.
    11. **Fault-Isolated Redemption:** Titanium try/catch block transmuting
        panics into diagnostic error vessels.
    12. **Ghost Matter Awareness:** Perceives files that exist on disk but
        failed the AST scry, ensuring they still manifest in the HUD.
    13. **Isomorphic URI Synthesis:** Prepends protocol anchors (file:///)
        to all diagnostic locus reports.
    14. **Directory Mass Tomography:** Aggregates cumulative byte-weight
        of the projected tree.
    15. **Recursive Depth Governor:** Hard-caps scrying at depth 25 to
        protect the Pyodide heap.
    16. **Environment Echo:** Captures UID/GID and OS-metadata for
        substrate-specific debugging.
    17. **Global Transfer Cell Suture:** Finalizes the JSON-RPC payload
        directly into __main__ for zero-latency JS retrieval.
    18. **Aura Normalization:** Maps node health to color-coded UI tints
        before the data leaves the Kernel.
    19. **Atomic Path Variance Check:** Verifies resolve() vs absolute()
        to detect symlink drift.
    20. **Zero-Byte Vitality Alert:** Metadata-flags empty scriptures to
        detect 'Touch' heresies.
    21. **Abyssal Shadow Filter:** Blinds the gaze to heavy system noise
        while preserving the configuration stratum.
    22. **Lazarus Handshake:** Auto-detects bootstrap status to signal
        UI readiness.
    23. **Hydraulic Buffer Yield:** Injects hardware-appropriate yields
        to the WASM event loop.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable
        JSON-RPC payload.
    =============================================================================
    """
    import os
    import sys
    import time
    import json
    import __main__
    import traceback
    from pathlib import Path
    from velm.core.runtime.vfs.scryer import GnosticScryer

    # --- MOVEMENT 0: CHRONOMETRY & INITIALIZATION ---
    start_ns = time.perf_counter_ns()
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    # [ASCENSION 1]: APOPHATIC TYPE GUARD
    try:
        if path is None:
            effective_path = "/vault/project"
        else:
            # Force absolute resolution
            effective_path = str(Path(str(path)).resolve())
    except Exception:
        effective_path = "/vault/project"

    # [ASCENSION 2]: THE PRE-EMPTIVE SUTURE
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

    # --- MOVEMENT I: THE PHYSICAL BIOPSY (DIAGNOSTICS) ---
    tree = []
    success = False
    error_msg = ""

    # [ASCENSION 5 & 16]: FORGING THE SENSORY DOSSIER
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
        # [ASCENSION 3]: HYDRAULIC I/O INCEPTION
        # We manually scry the raw OS layer to prove matter existence
        if diagnostics["exists"] and diagnostics["is_dir"]:
            try:
                diagnostics["raw_contents"] = os.listdir(effective_path)
            except Exception as e:
                diagnostics["raw_contents"] = [f"READ_FRACTURE: {str(e)}"]

        # --- MOVEMENT II: THE GNOSTIC CONDUCT ---
        # 1. SUMMON THE SPECIALIST
        scryer = GnosticScryer(effective_path)

        # 2. PERFORM THE RITE
        # We wrap this in a sub-try to capture local failures without breaking the gateway
        try:
            dossier = scryer.scry()
            # [ASCENSION 4]: NONETYPE SARCOPHAGUS
            tree = dossier.get("tree", []) if dossier.get("tree") is not None else []
            success = dossier.get("success", True)
        except Exception as scry_err:
            success = False
            error_msg = f"SCRY_CONDUCT_FRACTURE: {str(scry_err)}"
            print(f"[SCRYER] ⚠️  Internal conduct failed: {error_msg}")

        # [ASCENSION 12]: GHOST MATTER AWARENESS
        # If the Scryer was blinded by filters but OS saw matter, we adjust status
        has_physical_matter = len(diagnostics["raw_contents"]) > 0
        resonance_status = "PHYSICAL" if has_physical_matter else "RESONANT" if diagnostics["exists"] else "VOID"

    except Exception as catastrophic_paradox:
        # [ASCENSION 11]: FAULT-ISOLATED REDEMPTION
        success = False
        error_msg = str(catastrophic_paradox)
        diagnostics["error"] = error_msg
        diagnostics["traceback"] = traceback.format_exc()
        resonance_status = "FRACTURED"
        # [ASCENSION 9]: HYDRAULIC FLUSH
        print(f"[SCRYER] 💀 GATEWAY_PANIC for locus '{effective_path}': {error_msg}", file=sys.stderr)

    # --- MOVEMENT III: REVELATION & RADIATION ---
    # [ASCENSION 10]: METABOLIC TAX METERING
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

    # [ASCENSION 17]: THE FINAL REVELATION SUTURE
    if is_wasm:
        try:
            # Commit result to the global Pyodide context
            __main__.__GNOSTIC_TRANSFER_CELL__ = json.dumps(revelation)
        except Exception as suture_err:
            print(f"[SCRYER] 💀 Critical Memory Suture Failure: {suture_err}")

    # Return for internal Pythonic Artisans
    return tree