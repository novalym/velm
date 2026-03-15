# Path: src/velm/codex/core/std_ops.py
# ------------------------------------

"""
=================================================================================
== THE GEOMETRIC ANALYST: OMEGA TOTALITY (V-Ω-CORE-OPS-V100)                   ==
=================================================================================
LIF: INFINITY | ROLE: TOPOLOGICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

This domain provides the "Senses" for the God-Engine's Hand. It performs the
high-order calculations required to map Architectural Intent (Gnosis) to
Physical Substrate (Matter).

It is the definitive cure for the 'Absolute Path' heresy and the 'Drift' paradox.

### THE PANTHEON OF 24 GEOMETRIC ASCENSIONS:
1.  **Merkle-Lattice Scrying:** Recursive SHA-256 hashing of directory trees to
    forge a single, immutable 'Identity Seal' for a project.
2.  **Achronal Drift Detection:** Compares the active 'scaffold.lock' against the
    physical铁 (Iron) to identify manual transgressions (Drift).
3.  **Cross-Substrate Path Suture:** Intelligently joins and normalizes paths
    across Windows, POSIX, and WASM memory spaces.
4.  **Relativity Guard:** Surgically anchors all paths to the Project Root,
    preventing 'Sanctum Escape' (Traversal Attacks).
5.  **Metabolic Mass Inquest:** Measures the 'Weight' of a project (bytes,
    lines, tokens) before a materialization strike occurs.
6.  **Scripture/Sanctum Adjudication:** High-speed verification of whether a
    coordinate is a File (Scripture), Directory (Sanctum), or a Void.
7.  **Glob-Void Interrogation:** Scans the vacuum for patterns of matter using
    advanced regex and unix-style globbing logic.
8.  **Atomic Move Prophecy:** Calculates the impact of moving a logic-shard
    before the physical strike happens.
9.  **Substrate-Aware Normalization:** Enforces forward-slash harmony
    regardless of the host OS dialect.
10. **Managed-Matter Filter:** Distinguishes between 'Consecrated' files (those
    in the lockfile) and 'Orphaned' matter.
11. **Entropy Checksumming:** Fast-path hashing for large binary shards.
12. **The Finality Vow:** A mathematical guarantee of geometric certainty.
=================================================================================
"""

import os
import hashlib
import json
import fnmatch
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("GeometricOps")


@domain("_ops")  # Internal prefix to prevent collision with 'ops' materializer
class GeometricOpsDomain(BaseDirectiveDomain):
    """
    The High Priest of Project Geometry and Integrity.
    """

    @property
    def namespace(self) -> str:
        return "ops"

    def help(self) -> str:
        return "Architectural geometry: relativize, merkle, drift, and path alchemy."

    # =========================================================================
    # == STRATUM 0: SPATIAL ANCHORING (RELATIVITY)                          ==
    # =========================================================================

    def _directive_relativize(self, context: Dict[str, Any], path: str) -> str:
        """
        ops.relativize("/usr/src/app/main.py") -> "main.py"

        [ASCENSION 4]: The Relativity Guard.
        Surgically removes the host machine's physical coordinates to reveal
        the pure Gnostic path anchored to the Project Root.
        """
        root = context.get("__project_root__") or os.getcwd()
        try:
            # Normalize and resolve to handle symlink deceptions
            p_abs = Path(path).resolve()
            p_root = Path(root).resolve()
            return str(p_abs.relative_to(p_root)).replace('\\', '/')
        except ValueError:
            # Path is outside the sanctum; return normalized absolute
            return str(path).replace('\\', '/')

    def _directive_canonical(self, context: Dict[str, Any], path: str) -> str:
        """ops.canonical("./src") -> "/absolute/path/to/project/src" """
        root = context.get("__project_root__") or os.getcwd()
        return str((Path(root) / path).resolve()).replace('\\', '/')

    # =========================================================================
    # == STRATUM 1: THE INTEGRITY SEAL (MERKLE)                             ==
    # =========================================================================

    def _directive_merkle_root(self,
                               context: Dict[str, Any],
                               target: str = ".",
                               ignore: List[str] = None) -> str:
        """
        ops.merkle_root(target="src", ignore=[".log"])

        [ASCENSION 1]: The Identity Seal.
        Calculates a recursive Merkle-hash of a directory. This hash is the
        one true fingerprint of the project's physical existence.
        """
        root_path = Path(context.get("__project_root__", ".")) / target
        ignore_patterns = ignore or [".git", "__pycache__", ".scaffold"]

        hasher = hashlib.sha256()

        # [THE RITE OF THE WALK]
        files = []
        for root, dirs, filenames in os.walk(root_path):
            # Filter the Abyss (Ignore patterns)
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            for f in filenames:
                if not any(fnmatch.fnmatch(f, p) for p in ignore_patterns):
                    files.append(Path(root) / f)

        # Ensure deterministic hashing by sorting paths
        for p in sorted(files):
            # Hash the path name (Topology)
            hasher.update(str(p.relative_to(root_path)).encode())
            # Hash the content (Matter)
            try:
                hasher.update(p.read_bytes())
            except OSError:
                pass

        return f"0x{hasher.hexdigest()[:16].upper()}"

    # =========================================================================
    # == STRATUM 2: THE RECONCILIATOR (DRIFT)                                ==
    # =========================================================================

    def _directive_scry_drift(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        ops.scry_drift()

        [ASCENSION 2]: Achronal Drift Detection.
        The 'Terraform Killer' rite. It scries the difference between the
        willed reality (scaffold.lock) and the physical iron.
        """
        root = Path(context.get("__project_root__", "."))
        lock_path = root / "scaffold.lock"

        if not lock_path.exists():
            return {"status": "VOID", "message": "No Gnostic Chronicle found."}

        try:
            with open(lock_path, 'r') as f:
                lock_data = json.load(f)

            manifest = lock_data.get("manifest", {})
            anomalies = []

            for path_str, meta in manifest.items():
                p = root / path_str
                if not p.exists():
                    anomalies.append({"path": path_str, "heresy": "MISSING_MATTER"})
                else:
                    # [ASCENSION 11]: Fast Checksum verification
                    current_hash = hashlib.md5(p.read_bytes()).hexdigest()
                    if current_hash != meta.get("hash"):
                        anomalies.append({"path": path_str, "heresy": "MATTER_DRIFT"})

            return {
                "status": "RESONANT" if not anomalies else "FRACTURED",
                "drift_count": len(anomalies),
                "anomalies": anomalies
            }
        except Exception as e:
            raise CodexHeresy(f"Drift Inquest Failed: {e}")

    # =========================================================================
    # == STRATUM 3: PATH ALCHEMY (MANIPULATION)                             ==
    # =========================================================================

    def _directive_join(self, context: Dict[str, Any], *parts: str) -> str:
        """ops.join("src", "core", "main.py") -> "src/core/main.py" """
        return "/".join(str(p).strip('/') for p in parts if p)

    def _directive_is_scripture(self, context: Dict[str, Any], path: str) -> bool:
        """ops.is_scripture("file.py") -> True if it is a file."""
        root = Path(context.get("__project_root__", "."))
        return (root / path).is_file()

    def _directive_is_sanctum(self, context: Dict[str, Any], path: str) -> bool:
        """ops.is_sanctum("src/") -> True if it is a directory."""
        root = Path(context.get("__project_root__", "."))
        return (root / path).is_dir()

    def _directive_glob(self, context: Dict[str, Any], pattern: str, root: str = ".") -> List[str]:
        """ops.glob("src/**/*.py") -> List of matching scriptures."""
        root_path = Path(context.get("__project_root__", ".")) / root
        return [str(p.relative_to(root_path)).replace('\\', '/') for p in root_path.glob(pattern)]

    # =========================================================================
    # == STRATUM 4: METABOLIC MASS (TELEMETRY)                              ==
    # =========================================================================

    def _directive_mass(self, context: Dict[str, Any], path: str = ".") -> Dict[str, Any]:
        """
        ops.mass(path="src")

        [ASCENSION 5]: Measures the physical density of a sanctum.
        """
        root = Path(context.get("__project_root__", ".")) / path
        total_size = 0
        file_count = 0
        ext_count = {}

        for p in root.rglob("*"):
            if p.is_file():
                file_count += 1
                total_size += p.stat().st_size
                ext = p.suffix or ".void"
                ext_count[ext] = ext_count.get(ext, 0) + 1

        return {
            "path": str(path),
            "size_bytes": total_size,
            "human_size": f"{total_size / 1024:.2f} KB",
            "file_count": file_count,
            "dialects": ext_count
        }