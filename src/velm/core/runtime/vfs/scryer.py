# Path: src/velm/core/runtime/vfs/scryer.py
# ----------------------------------------
"""
=================================================================================
== THE GNOSTIC SCRYER: TOTALITY (V-Ω-TOTALITY-V200.1-RESILIENT)                ==
=================================================================================
LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SUPREME
AUTH: Ω_SCRYER_V200_RECTIFIED_2026_FINALIS

[ARCHITECTURAL CONSTITUTION]
This scripture defines the sovereign engine of perception. It transmutes physical
matter shards into a structured, hierarchical Gnostic Tree for the Ocular HUD.
=================================================================================
"""

import os
import time
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Union

# --- GNOSTIC LOGGING ---
Logger = logging.getLogger("GnosticScryer")


class GnosticScryer:
    """
    The Sovereign Engine of Perception.
    Performs deep-tissue biopsy of the virtual filesystem.
    """

    # [ASCENSION 4]: THE ABYSSAL FILTER
    # Matter that must be veiled from the Ocular Membrane to maintain purity.
    ABYSS = {
        '.git', '.scaffold', '__pycache__', 'node_modules',
        '.venv', 'venv', 'dist', 'build', '.next', '.pyc',
        '.DS_Store', 'scaffold.lock', '.pyo', '.pyd'
    }

    def __init__(self, root_path: Union[str, Path]):
        self.root = Path(root_path).resolve()
        # [ASCENSION 5]: INODE VIGIL
        self.seen_inodes: Set[int] = set()

    @classmethod
    def conduct_inquest(cls, target_path: str) -> List[Dict[str, Any]]:
        """
        The primary entry point for the WASM Dispatcher.
        Conducts a full topographic biopsy of the target locus.
        """
        scryer = cls(target_path)
        return scryer.scry()

    def scry(self) -> List[Dict[str, Any]]:
        """Initiates the recursive Gaze."""
        if not self.root.exists():
            Logger.warning(f"Scryer Fracture: Target locus '{self.root}' is a void.")
            return []

        # [ASCENSION 1]: Begin recursive materialization
        return self._scry_recursive(self.root, depth=0)

    def _scry_recursive(self, current_path: Path, depth: int = 0) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE RECURSIVE GAZE (V-Ω-TOTALITY-RECTIFIED)                            ==
        =============================================================================
        [ASCENSION 10]: Metabolic Throttling. Prevents depth-charge crashes.
        """
        if depth > 20:
            return []

        nodes: List[Dict[str, Any]] = []

        try:
            # [ASCENSION 2]: os.scandir provides maximum I/O throughput in WASM
            with os.scandir(current_path) as entries:
                for entry in entries:
                    # 1. THE ABYSSAL CHECK
                    if entry.name in self.ABYSS:
                        continue

                    # 2. INODE VIGIL (Prevent circular Ouroboros loops)
                    try:
                        info = entry.stat(follow_symlinks=False)
                        if info.st_ino in self.seen_inodes:
                            continue
                        self.seen_inodes.add(info.st_ino)
                    except (OSError, FileNotFoundError):
                        continue

                    # 3. METADATA TOMOGRAPHY
                    is_dir = entry.is_dir(follow_symlinks=False)
                    is_symlink = entry.is_symlink()

                    # [ASCENSION 7]: Normalize all paths to POSIX standards
                    clean_path = entry.path.replace('\\', '/')

                    node = {
                        "name": entry.name,
                        "path": clean_path,
                        "type": "directory" if is_dir else "file",
                        "size": info.st_size,
                        "mtime": info.st_mtime,
                        "inode": info.st_ino
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
                        # Continue the walk into the sub-sanctum
                        node["children"] = self._scry_recursive(Path(entry.path), depth + 1)
                    else:
                        # [ASCENSION 3]: MERKLE-HASH INCEPTION
                        # Only hash small scriptures during scry to preserve CPU energy.
                        if info.st_size < 1024 * 50:  # 50KB Threshold
                            node["hash"] = self._forge_merkle_leaf(Path(entry.path))

                    nodes.append(node)

        except (PermissionError, OSError) as e:
            # [ASCENSION 8]: Fault-tolerant capture of I/O paradoxes
            Logger.debug(f"Perception hindered at {current_path}: {e}")
            pass

        return nodes

    def _forge_merkle_leaf(self, file_path: Path) -> str:
        """Forges a SHA-256 fingerprint of a matter shard."""
        try:
            content = file_path.read_bytes()
            return hashlib.sha256(content).hexdigest()
        except Exception:
            return "0xVOID"


def vfs_scry_recursive(path: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE FINALITY VOW: THE UNIVERSAL INTERFACE                               ==
    =============================================================================
    The one true bridge between the WASM Dispatcher and the VFS Oracle.
    """
    return GnosticScryer.conduct_inquest(path)

# == SCRIPTURE SEALED: THE TOPOGRAPHICAL INQUISITOR IS NOW UNBREAKABLE ==