# Path: scaffold/core/kernel/hologram.py

import os
import shutil
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, Optional, List

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy
from ...artisans.history.contracts import RiteGnosis

Logger = Scribe("HologramEngine")


class HolographicEngine:
    """
    =================================================================================
    == THE SPACETIME MANIPULATOR (V-Ω-LEGENDARY-APOTHEOSIS)                        ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The Gnostic heart of the Chronos Anomaly. It forges shadow realities from the
    Git database, performs the Rite of Gnostic Linking to make them manifest, and
    can materialize a past reality directly onto the filesystem. It is the one true
    engine of temporal interaction.
    =================================================================================
    """

    SHADOW_ROOT = ".scaffold/shadow"

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.shadow_path = self.root / self.SHADOW_ROOT
        self.active_links: Dict[Path, Path] = {}
        # Ascension 7: The Chronocache of Realities
        self._materialized_cache: Dict[str, Path] = {}

    def _get_rite_gnosis(self, rite_id: str) -> Optional[RiteGnosis]:
        """[FACULTY 11] The Forensic Dossier."""
        if rite_id.startswith("HEAD"):
            # For HEAD, we don't have a past rite, but we can get the commit
            try:
                commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True).strip()
                return RiteGnosis(
                    rite_id="HEAD",
                    rite_name="Current Reality",
                    timestamp=time.time(),
                    provenance={"git_commit": commit}
                )
            except Exception:
                return None

        # Gaze into the chronicles for the specific rite
        chronicle_path = self.root / ".scaffold" / "chronicles"
        for f in chronicle_path.glob(f"*_{rite_id[:8]}.lock"):
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                return RiteGnosis.from_dict(data, f.name)
            except Exception:
                continue
        return None

    def _get_file_manifest_for_commit(self, commit_hash: str) -> List[Path]:
        """[FACULTY 2] The Polyglot Git Gaze."""
        try:
            # ls-tree is the one true way to see the past.
            output = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit_hash], cwd=self.root,
                                             text=True)
            return [self.root / p for p in output.splitlines()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            Logger.warn(f"Could not divine file manifest for commit {commit_hash[:8]}. Falling back to current files.")
            return self.git_ls_files

    @property
    def git_ls_files(self) -> List[Path]:
        """Returns a list of all tracked files in the current HEAD."""
        try:
            output = subprocess.check_output(['git', 'ls-files'], cwd=self.root, text=True)
            return [self.root / p for p in output.splitlines()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []

    def materialize_to_path(self, rite_id: str, target_path: Path) -> int:
        """[ASCENSION 3] The Rite of Direct Materialization."""
        Logger.info(f"Performing direct materialization of rite {rite_id[:8]} to {target_path}...")
        rite_gnosis = self._get_rite_gnosis(rite_id)
        if not rite_gnosis or not rite_gnosis.provenance.git_commit:
            raise ArtisanHeresy(f"No Git commit Gnosis found for rite {rite_id}. Cannot materialize.")

        commit_hash = rite_gnosis.provenance.git_commit

        # 1. Clean the target directory (except .git)
        for item in target_path.iterdir():
            if item.name == '.git': continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # 2. Forge the reality directly into the target
        return self._forge_reality(commit_hash, target_path)

    def materialize(self, rite_id: str):
        """Materializes the shadow reality for a specific rite_id and links it."""
        Logger.info(f"Hologram requested for rite {rite_id[:8]}...")
        rite_gnosis = self._get_rite_gnosis(rite_id)
        if not rite_gnosis or not rite_gnosis.provenance.git_commit:
            Logger.warn(f"No Git commit Gnosis found for rite {rite_id}. Cannot materialize hologram.")
            self.dematerialize()
            return

        commit_hash = rite_gnosis.provenance.git_commit
        target_shadow = self.shadow_path / commit_hash

        # Ascension 3 & 7: Just-in-Time Materialization & Chronocache
        if commit_hash not in self._materialized_cache:
            self._forge_reality(commit_hash, target_shadow, rite_gnosis.manifest.keys())
            self._materialized_cache[commit_hash] = target_shadow

        self._link_shadow(target_shadow, rite_gnosis)

    def _forge_reality(self, commit_hash: str, target_dir: Path, manifest_filter: Optional[List[str]] = None) -> int:
        """
        [FACULTY 1, 4, 5] The Asynchronous Forge with Gnostic Triage & Unbreakable Ward.
        Reads files from git history and writes them to a target directory.
        Returns the number of files written.
        """
        Logger.verbose(f"Forging reality from commit {commit_hash[:8]} into {target_dir.name}...")
        target_dir.mkdir(parents=True, exist_ok=True)

        # Gaze upon the file manifest for this specific commit
        files_at_commit = self._get_file_manifest_for_commit(commit_hash)

        # If we have a lockfile manifest, use it as the absolute source of truth
        if manifest_filter:
            files_to_forge = [self.root / p for p in manifest_filter if self.root / p in files_at_commit]
        else:
            files_to_forge = files_at_commit

        count = 0

        # Ascension 5: The Asynchronous Forge
        with ThreadPoolExecutor() as executor:
            future_to_path = {
                executor.submit(self._forge_single_file, commit_hash, file_path, target_dir): file_path
                for file_path in files_to_forge
            }
            for future in as_completed(future_to_path):
                if future.result():
                    count += 1

        Logger.success(f"Reality forged. {count} scriptures materialized.")
        return count

    def _forge_single_file(self, commit_hash: str, file_path: Path, target_dir: Path) -> bool:
        """The atomic rite of forging a single file's soul."""
        try:
            rel_path = file_path.relative_to(self.root)
            # Use git show <rev>:<path> to read the object directly from the DB
            content = subprocess.check_output(['git', 'show', f'{commit_hash}:{rel_path.as_posix()}'], cwd=self.root)

            shadow_file = target_dir / rel_path
            shadow_file.parent.mkdir(parents=True, exist_ok=True)
            shadow_file.write_bytes(content)
            return True
        except subprocess.CalledProcessError:
            # Ascension 4: The Unbreakable Ward of the Void (e.g., file in LFS)
            Logger.warn(f"Could not read soul of '{rel_path}' at {commit_hash[:7]}. Forging a Gnostic void.")
            shadow_file = target_dir / rel_path
            shadow_file.parent.mkdir(parents=True, exist_ok=True)
            shadow_file.write_text(
                f"# GNOSTIC VOID: The soul of this scripture could not be resurrected from commit {commit_hash[:7]}.\n")
            return True
        except Exception as e:
            Logger.error(f"Error forging shadow for {file_path.relative_to(self.root)}: {e}")
            return False

    def _link_shadow(self, shadow_dir: Path, rite: RiteGnosis):
        """[FACULTY 6 & 8] The Sentinel of the .real World & The Rite of Selective Linking."""
        self.dematerialize()
        Logger.info(f"Performing Gnostic Linking to shadow reality {shadow_dir.name[:8]}...")

        # Ascension 8: Rite of Selective Linking
        # We only link the top-level directories that contain files from the rite's manifest
        dirs_to_link = set(Path(p).parts[0] for p in rite.manifest.keys() if Path(p).parts)

        for dir_name in sorted(list(dirs_to_link)):
            real_path = self.root / dir_name
            shadow_src = shadow_dir / dir_name
            real_backup_path = self.root / f"{dir_name}.real"

            # Ascension 6: Sentinel of the .real World
            if real_backup_path.exists():
                Logger.error(
                    f"Cannot link '{dir_name}': A profane '.real' backup already exists. Please resolve manually.")
                continue

            if real_path.exists() and shadow_src.exists():
                try:
                    real_path.rename(real_backup_path)
                    os.symlink(shadow_src, real_path, target_is_directory=True)
                    self.active_links[real_path] = real_backup_path
                    Logger.verbose(f"   -> Linked: {dir_name} -> shadow/{shadow_dir.name[:8]}/{dir_name}")
                except Exception as e:
                    Logger.error(f"Failed to link {dir_name}: {e}")
                    if real_backup_path.exists() and not real_path.exists():
                        real_backup_path.rename(real_path)

    def dematerialize(self):
        """Restores reality by removing links and renaming original dirs back."""
        if not self.active_links:
            return

        Logger.info("Dematerializing hologram and restoring present reality...")
        for link_path, backup_path in self.active_links.items():
            try:
                if link_path.is_symlink():
                    link_path.unlink()

                if backup_path.exists():
                    backup_path.rename(link_path)

                Logger.verbose(f"   -> Restored: {link_path.name}")
            except Exception as e:
                Logger.error(f"Failed to restore {link_path.name}: {e}")

        self.active_links.clear()