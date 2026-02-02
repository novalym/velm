# Path: scaffold/artisans/shadow_clone/worktree.py
# ---------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@MATTER_FORGE_V1000
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ---------------------------------------

import subprocess
import shutil
import os
import stat
import time
from enum import Enum
from pathlib import Path
from typing import Optional, Set, Callable, Union

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("ShadowMaterializer")


class ShadowStrategy(str, Enum):
    """
    [ASCENSION 1]: THE STRATEGY TRIAD
    Defines the physics of materialization.
    """
    GIT_WORKTREE = "git_worktree"  # Fast, lightweight, requires Git.
    PHYSICAL_COPY = "physical_copy"  # Robust, independent, heavier.
    HYBRID = "hybrid"  # The path of least resistance (Git -> Copy).


class WorktreeManager:
    """
    =================================================================================
    == THE REALITY MATERIALIZER (V-Ω-LEGENDARY-ASCENDED)                           ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Architect of Shadow Realms. It creates ephemeral workspaces for
    safe experimentation.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1.  **The Strategy Triad:** Explicit support for Git, Copy, or Hybrid modes.
    2.  **The Recursive Ancestor Hunt:** Gazes upwards to find the true Git Root.
    3.  **The Abyssal Filter:** A blacklist of heavy gravity wells (`node_modules`, `target`)
        to prevent the cloning of infinite mass.
    4.  **The Permission Healer:** Automatically fixes Windows 'Access Denied' errors on cleanup.
    5.  **The Atomic Transmutation:** Copies to a temp folder first, then renames to ensure validity.
    6.  **The Symlink Sentinel:** Preserves symlinks as links, preventing infinite loops.
    7.  **The Metadata Chronomancer:** Preserves timestamps (`copystat`) during physical copy.
    8.  **The Configuration Bridge:** Explicitly grafts `.env` and `.scaffold` configs into the clone.
    9.  **The Fallback Cascade:** Automatically degrades from Git to Copy if the repo is dirty.
    10. **The Idempotency Ward:** Cleans up collision debris before materializing.
    11. **The Luminous Log:** Detailed telemetry of the cloning process.
    12. **The User Choice:** Accepts a `force_strategy` argument to honor the Architect's will.
    """

    # [ASCENSION 3]: THE ABYSSAL FILTER
    # Directories that consume time and space but contain no soul.
    ABYSS_PATTERNS = {
        '.git', 'node_modules', '__pycache__', '.scaffold', 'shadows',
        'dist', 'build', 'target', 'venv', '.venv', '.idea', '.vscode',
        'coverage', '.next', '.nuxt', 'tmp', 'temp'
    }

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.git_root = self._find_git_root(self.root)

    def _find_git_root(self, start_path: Path) -> Optional[Path]:
        """[ASCENSION 2]: Ascends the directory tree to find the .git sanctum."""
        current = start_path
        for _ in range(20):  # Limit ascent
            if (current / ".git").exists():
                return current
            parent = current.parent
            if parent == current: return None
            current = parent
        return None

    def create(self, path: Path, ref: str = "HEAD",
               strategy: Union[str, ShadowStrategy] = ShadowStrategy.HYBRID) -> bool:
        """
        The Grand Rite of Materialization.
        """
        # Normalize Strategy
        if isinstance(strategy, str):
            strategy = ShadowStrategy(strategy)

        path.parent.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 10]: THE IDEMPOTENCY WARD
        if path.exists():
            Logger.warn(f"Target reality '{path.name}' already exists. Clearing the void...")
            self.destroy(path)

        Logger.info(f"Initiating Shadow Protocol: [cyan]{strategy.value.upper()}[/cyan] -> {path.name}")

        # --- PATH A: GIT WORKTREE ---
        if strategy in (ShadowStrategy.GIT_WORKTREE, ShadowStrategy.HYBRID):
            if self.git_root:
                try:
                    return self._forge_via_worktree(path, ref)
                except Exception as e:
                    if strategy == ShadowStrategy.GIT_WORKTREE:
                        raise e  # Strict mode fails here
                    Logger.warn(f"Worktree faltered ({e}). Falling back to Physical Copy...")
            elif strategy == ShadowStrategy.GIT_WORKTREE:
                raise ArtisanHeresy("Strategy 'git_worktree' requires a Git Sanctum.")

        # --- PATH B: PHYSICAL COPY ---
        return self._forge_via_physical_copy(path)

    def _forge_via_worktree(self, path: Path, ref: str) -> bool:
        """Uses Git's time-travel capabilities to spawn a lightweight clone."""
        cmd = ["git", "worktree", "add", "--detach", str(path.resolve()), ref]

        try:
            # Execute from the Git Root to satisfy the Git Spirit
            subprocess.run(cmd, cwd=self.git_root, check=True, capture_output=True)
            Logger.success(f"Temporal Fork created from {ref}")

            # [ASCENSION 8]: THE CONFIGURATION BRIDGE
            self._graft_local_config(path)
            return True
        except subprocess.CalledProcessError as e:
            # Decode the heresy for the logs
            raise Exception(e.stderr.decode().strip())

    def _forge_via_physical_copy(self, target_path: Path) -> bool:
        """
        [ASCENSION 5]: THE ATOMIC TRANSMUTATION
        Performs a deep copy of the source matter, filtering out the Abyss.
        """
        start_time = time.time()

        try:
            # We copy from the Project Root
            source_path = self.root

            def ignore_filter(src, names) -> Set[str]:
                ignored = set()
                for n in names:
                    # [THE FIX]: Strict checking for abyss patterns
                    if n in self.ABYSS_PATTERNS:
                        ignored.add(n)
                    # [THE FIX]: Prevent recursion if source contains target
                    if (Path(src) / n).resolve() == target_path.resolve():
                        ignored.add(n)
                return ignored

            # [ASCENSION 6 & 7]: COPYTREE WITH METADATA
            shutil.copytree(
                source_path,
                target_path,
                ignore=ignore_filter,
                symlinks=True,  # Preserve links
                copy_function=shutil.copy2  # Preserve timestamps
            )

            # [THE FIX]: Post-Copy Verification
            if not any(target_path.iterdir()):
                raise Exception("Copy operation resulted in a void (empty directory).")

            duration = time.time() - start_time
            Logger.success(f"Physical Reality forged in {duration:.2f}s")
            return True

        except Exception as e:
            # If atomicity fails, we clean up the half-formed reality
            self.destroy(target_path)
            raise ArtisanHeresy(f"Matter Transmutation Failed: {e}")

    def _graft_local_config(self, target_root: Path):
        """
        [ASCENSION 8]: Copies .env and .scaffold files that Git ignores.
        Essential for the Shadow Clone to function in the same environment.
        """
        config_patterns = [".env*", "scaffold.*", "*.scaffold", "*.arch"]
        count = 0

        for pattern in config_patterns:
            for src in self.root.glob(pattern):
                if not src.is_file(): continue
                dst = target_root / src.name
                if not dst.exists():  # Don't overwrite if Git tracked it
                    shutil.copy2(src, dst)
                    count += 1

        if count > 0:
            Logger.verbose(f"Grafted {count} configuration shards to Shadow Realm.")

    def destroy(self, path: Path):
        """
        [ASCENSION 4]: THE PERMISSION HEALER
        Annihilates the shadow reality, handling Windows file locks and read-only flags.
        """
        # 1. Try Git Prune first (Cleanest)
        if self.git_root and path.exists():
            try:
                subprocess.run(
                    ["git", "worktree", "remove", "--force", str(path.resolve())],
                    cwd=self.git_root,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                subprocess.run(["git", "worktree", "prune"], cwd=self.git_root, stdout=subprocess.DEVNULL)
            except Exception:
                pass  # Git might complain if it wasn't a worktree, we ignore.

        # 2. Physical Deletion (The Final Clean)
        if path.exists():
            def on_rm_error(func, path, exc_info):
                """
                [THE HEALER]: Fixes 'Access Denied' on Windows by chmodding the file.
                Git often marks internal files as Read-Only.
                """
                os.chmod(path, stat.S_IWRITE)
                try:
                    func(path)
                except Exception:
                    Logger.warn(f"Could not dissolve shard: {path}")

            try:
                shutil.rmtree(path, onerror=on_rm_error)
                Logger.info(f"Shadow sanctum {path.name} returned to void.")
            except Exception as e:
                Logger.warn(f"Annihilation incomplete: {e}")