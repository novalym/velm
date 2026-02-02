# scaffold/core/simulation/conductor/reality_forge.py

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, List

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
    == THE REALITY FORGE (V-Ω-STATE-AWARE)                                         ==
    =================================================================================
    Constructs ephemeral realities and chronicles their initial state.
    """

    def __init__(self, real_root: Path, sim_root: Path):
        self.real_root = real_root
        self.sim_root = sim_root
        self.ignore_spec = self._forge_ignore_spec()
        self.manifest_path = self.sim_root / ".scaffold" / "sim_manifest.json"

    def materialize_void(self):
        """Forges a clean, empty universe."""
        self._prepare_sanctum()
        self._record_manifest([])  # Void state
        Logger.debug(f"Void materialized at {self.sim_root.name}")

    def materialize_mirror(self):
        """Forges a perfect reflection and records the manifest."""
        self._prepare_sanctum()
        Logger.debug(f"Mirroring reality to {self.sim_root.name}...")

        mirrored_files = []

        # Strategy A: The Git Bridge
        if (self.real_root / ".git").exists() and shutil.which("git"):
            try:
                res = subprocess.run(
                    ["git", "ls-files", "-c", "-o", "--exclude-standard"],
                    cwd=self.real_root, capture_output=True, text=True, timeout=10
                )
                if res.returncode == 0:
                    paths = [Path(p) for p in res.stdout.splitlines() if p.strip()]
                    if paths:
                        for rel in paths:
                            if self._copy_file(rel):
                                mirrored_files.append(str(rel.as_posix()))

                        self._ensure_internal_structures()
                        self._record_manifest(mirrored_files)
                        self._check_lockfile()
                        return
            except Exception as e:
                Logger.warn(f"Git Bridge faltered ({e}). Falling back to manual copy.")

        # Strategy B: The Manual Walk
        files_to_copy = self._scan_reality(self.real_root)
        for src in files_to_copy:
            try:
                rel = src.relative_to(self.real_root)
                if self._copy_file(rel):
                    mirrored_files.append(str(rel.as_posix()))
            except Exception:
                pass

        self._ensure_internal_structures()
        self._record_manifest(mirrored_files)
        self._check_lockfile()

    def _copy_file(self, rel_path: Path) -> bool:
        """Atomic copy helper. Returns True if successful."""
        src = self.real_root / rel_path
        dst = self.sim_root / rel_path
        try:
            if src.exists() and src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                return True
        except Exception:
            pass
        return False

    def _record_manifest(self, files: List[str]):
        """
        [THE RITE OF RECORD]
        Writes the list of mirrored files to disk. This is the Absolute Truth
        of what exists in the simulation at T=0.
        """
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
        # We scan the SIMULATION to adopt what we actually copied
        sim_files = self._scan_reality(self.sim_root)
        for path in sim_files:
            write_dossier.append(GnosticWriteResult(
                success=True, path=path, action_taken=InscriptionAction.ADOPTED,
                bytes_written=path.stat().st_size, gnostic_fingerprint=hash_file(path), blueprint_origin=None
            ))
        update_chronicle(
            project_root=self.sim_root, blueprint_path=Path("ghost.scaffold"),
            rite_dossier={}, old_lock_data={}, write_dossier=write_dossier,
            final_vars={}, rite_name="Ghost Adoption"
        )

    # ... [Include _forge_ignore_spec, _is_ignored, _scan_reality from previous] ...
    def _forge_ignore_spec(self) -> Any:
        patterns = set()
        patterns.update(KnowledgeBase.ABYSS_DIRECTORIES)
        patterns.update(KnowledgeBase.ABYSS_GLOBS)
        patterns.add(".scaffold")
        patterns.add("simulation")
        gitignore = self.real_root / ".gitignore"
        if gitignore.exists():
            try:
                with open(gitignore, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.add(line)
            except Exception:
                pass
        if PATHSPEC_AVAILABLE:
            return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return patterns

    def _is_ignored(self, rel_path: str) -> bool:
        if PATHSPEC_AVAILABLE: return self.ignore_spec.match_file(rel_path)
        return False

    def _scan_reality(self, root: Path) -> List[Path]:
        valid_files = []
        for dirpath, dirnames, filenames in os.walk(root):
            for i in range(len(dirnames) - 1, -1, -1):
                d = dirnames[i]
                full_dir = Path(dirpath) / d
                try:
                    rel_dir = str(full_dir.relative_to(root)).replace("\\", "/")
                except:
                    continue
                if d == ".git" or d == ".scaffold" or self._is_ignored(rel_dir) or self._is_ignored(rel_dir + "/"):
                    del dirnames[i]
            for f in filenames:
                full_path = Path(dirpath) / f
                try:
                    rel_path = str(full_path.relative_to(root)).replace("\\", "/")
                except:
                    continue
                if not self._is_ignored(rel_path): valid_files.append(full_path)
        return valid_files