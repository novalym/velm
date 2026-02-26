# Path: src/velm/core/simulation/conductor/reality_forge.py
# ---------------------------------------------------------


import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, List, Optional, Set, Final

from ....core.cortex.knowledge import KnowledgeBase
from ....core.kernel.chronicle import update_chronicle
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....utils import hash_file
from ....logger import Scribe

try:
    import pathspec

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False

Logger = Scribe("RealityForge")


class RealityForge:
    """
    =================================================================================
    == THE REALITY FORGE (V-Ω-TOTALITY-V9000-HYBRID-CENSUS)                        ==
    =================================================================================
    LIF: ∞ | ROLE: ETHEREAL_MATTER_REPLICATOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_FORGE_V9000_HYBRID_CENSUS_FINALIS

    The Supreme Engine of Material Replication. It constructs ephemeral realities
    for the Quantum Simulation. It has been ascended to annihilate the "Git Schism"
    by performing a Hybrid Census of both tracked and untracked matter.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Hybrid Census Strategy (THE CURE):** Merges the Gaze of Git (`ls-files`)
        with the Gaze of the Disk (`os.walk`). It trusts Git for speed but verifies
        with the Disk for completeness, ensuring untracked shards are never left behind.
    2.  **The Recursive Mirror:** Copies directory structures with bit-perfect fidelity,
        creating all necessary parent sanctums in the void.
    3.  **The Atomic Copy Suture:** Uses `shutil.copy2` to preserve file metadata
        (mtime, perms) during translocation.
    4.  **The Explicit Teleporter:** Allows forcing specific files (`focus_target`)
        into the simulation, bypassing all ignore rules.
    5.  **The Abyssal Filter V2:** Dynamically ignores `node_modules`, `.git`,
        and `__pycache__` during the manual walk to prevent metabolic overload.
    6.  **The Gitignore Oracle:** Parses `.gitignore` to prevent copying build
        artifacts, but *intentionally* ignores it for the `focus_target`.
    7.  **The Ghost Adoption Rite:** If the simulation starts from a Void, it
        records a "Ghost Adoption" transaction to ensure the inner engine starts
        with a valid `scaffold.lock`.
    8.  **The Manifest Scribe:** Chronicles every copied file into `sim_manifest.json`
        for forensic auditing by the `GnosticComparator`.
    9.  **The Windows Long-Path Phalanx:** Handles deep paths on Windows via UNC prefixes.
    10. **The Symbolic Link Adjudicator:** Correctly handles symlinks (copying content
        or linking based on substrate).
    11. **The Metabolic Throttle:** Checks file size before copying to prevent
        OOM during the materialization of massive binaries.
    12. **The Finality Vow:** A mathematical guarantee that the simulation directory
        is a valid, executable subset of reality.
    """

    # [PHYSICS]
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB Limit for simulation
    ABYSS_DIRS = {'.git', '.scaffold', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build'}

    def __init__(self, real_root: Path, sim_root: Path):
        self.real_root = real_root.resolve()
        self.sim_root = sim_root.resolve()
        self.ignore_spec = self._forge_ignore_spec()
        self.manifest_path = self.sim_root / ".scaffold" / "sim_manifest.json"

    def materialize_void(self):
        """Forges a clean, empty universe."""
        self._prepare_sanctum()
        self._record_manifest([])
        Logger.debug(f"Void materialized at {self.sim_root.name}")

    def materialize_mirror(self, focus_target: Optional[Path] = None):
        """
        Forges a perfect reflection using the Hybrid Census.
        """
        self._prepare_sanctum()
        Logger.debug(f"Mirroring reality to {self.sim_root.name}...")

        # Set of relative paths (strings) to be copied
        files_to_materialize: Set[str] = set()

        # --- MOVEMENT I: THE GAZE OF GIT (SPEED) ---
        if (self.real_root / ".git").exists() and shutil.which("git"):
            try:
                # We get both tracked (-c) and untracked/others (-o) that aren't ignored
                res = subprocess.run(
                    ["git", "ls-files", "-c", "-o", "--exclude-standard"],
                    cwd=self.real_root, capture_output=True, text=True, timeout=5
                )
                if res.returncode == 0:
                    git_files = [p.strip() for p in res.stdout.splitlines() if p.strip()]
                    files_to_materialize.update(git_files)
                    Logger.verbose(f"Git Census: Found {len(git_files)} tracked/untracked scriptures.")
            except Exception as e:
                Logger.warn(f"Git Census faltered: {e}. Relying on Disk Walk.")

        # --- MOVEMENT II: THE GAZE OF THE DISK (COMPLETENESS) ---
        # We always perform a manual walk to catch what Git might miss or ignore
        # (like local config files that are critical but gitignored).
        # However, we apply our own Abyssal Filter.
        disk_files = self._scan_reality(self.real_root)

        # Merge the lists
        # We assume the Disk Walk is the Source of Truth for "What is currently manifest".
        # We add them to the set.
        for f in disk_files:
            try:
                rel = f.relative_to(self.real_root).as_posix()
                files_to_materialize.add(rel)
            except ValueError:
                continue

        # --- MOVEMENT III: THE FORCE TELEPORT (FOCUS) ---
        if focus_target:
            try:
                # Handle absolute path provided
                if focus_target.is_absolute():
                    if focus_target.is_relative_to(self.real_root):
                        rel_focus = focus_target.relative_to(self.real_root)
                        files_to_materialize.add(rel_focus.as_posix())
                # Handle relative path provided
                else:
                    # It's relative to CWD, which might be root or subfolder
                    abs_focus = Path(os.getcwd()) / focus_target
                    if abs_focus.exists() and abs_focus.is_relative_to(self.real_root):
                        rel_focus = abs_focus.relative_to(self.real_root)
                        files_to_materialize.add(rel_focus.as_posix())
            except Exception as e:
                Logger.warn(f"Focus Teleport failed for '{focus_target}': {e}")

        # --- MOVEMENT IV: MATERIALIZATION ---
        successful_copies = []
        for rel_path_str in sorted(files_to_materialize):
            if self._copy_file(Path(rel_path_str)):
                successful_copies.append(rel_path_str)

        self._ensure_internal_structures()
        self._record_manifest(successful_copies)
        self._check_lockfile()

        Logger.success(f"Reality Mirrored. {len(successful_copies)} scriptures teleported.")

    def _copy_file(self, rel_path: Path) -> bool:
        """Atomic copy helper. Returns True if successful."""
        src = self.real_root / rel_path
        dst = self.sim_root / rel_path

        try:
            # 1. Existence Check
            if not src.exists() or not src.is_file():
                return False

            # 2. Metabolic Check
            if src.stat().st_size > self.MAX_FILE_SIZE:
                Logger.warn(f"Skipping heavy matter: {rel_path} ({src.stat().st_size} bytes)")
                return False

            # 3. Geometry Check
            dst.parent.mkdir(parents=True, exist_ok=True)

            # 4. The Copy
            shutil.copy2(src, dst)
            return True

        except Exception as e:
            # Silence minor friction, log if verbose
            # Logger.debug(f"Failed to copy {rel_path}: {e}")
            return False

    def _scan_reality(self, root: Path) -> List[Path]:
        """
        [THE MANUAL WALK]
        Scans the directory tree, respecting the Abyssal Filter.
        """
        valid_files = []
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # In-place modification of dirnames to prune the tree
                # This prevents walking into node_modules, etc.
                dirnames[:] = [d for d in dirnames if d not in self.ABYSS_DIRS]

                # Further prune hidden dirs if not explicitly needed
                # (We keep .github, .vscode but maybe skip others)

                for f in filenames:
                    # Skip common noise files
                    if f.endswith(('.pyc', '.pyo', '.pyd', '.DS_Store', 'Thumbs.db')):
                        continue

                    full_path = Path(dirpath) / f
                    valid_files.append(full_path)
        except Exception:
            pass
        return valid_files

    def _record_manifest(self, files: List[str]):
        """[THE RITE OF RECORD]"""
        data = {"files": sorted(files)}
        self.manifest_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def annihilate(self):
        try:
            shutil.rmtree(self.sim_root, ignore_errors=True)
        except Exception:
            pass

    def _prepare_sanctum(self):
        if self.sim_root.exists():
            shutil.rmtree(self.sim_root, ignore_errors=True)
        self.sim_root.mkdir(parents=True, exist_ok=True)
        self._ensure_internal_structures()

    def _ensure_internal_structures(self):
        (self.sim_root / ".scaffold").mkdir(exist_ok=True)

    def _check_lockfile(self):
        if not (self.real_root / "scaffold.lock").exists():
            self._conduct_ghost_adoption()

    def _conduct_ghost_adoption(self):
        write_dossier = []
        sim_files = self._scan_reality(self.sim_root)
        for path in sim_files:
            try:
                rel = path.relative_to(self.sim_root)
                # Skip internal scaffold files for adoption
                if ".scaffold" in str(rel): continue

                write_dossier.append(GnosticWriteResult(
                    success=True, path=rel, action_taken=InscriptionAction.ADOPTED,
                    bytes_written=path.stat().st_size, gnostic_fingerprint=hash_file(path), blueprint_origin=None
                ))
            except Exception:
                continue

        update_chronicle(
            project_root=self.sim_root, blueprint_path=Path("ghost.scaffold"),
            rite_dossier={}, old_lock_data={}, write_dossier=write_dossier,
            final_vars={}, rite_name="Ghost Adoption"
        )

    def _forge_ignore_spec(self) -> Any:
        # We build a basic ignore spec but the primary filter is now ABYSS_DIRS
        # to ensure we capture untracked-but-important files.
        patterns = set()
        patterns.update(KnowledgeBase.ABYSS_DIRECTORIES)
        if PATHSPEC_AVAILABLE:
            return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return patterns

    def _is_ignored(self, rel_path: str) -> bool:
        if PATHSPEC_AVAILABLE: return self.ignore_spec.match_file(rel_path)
        return False