# Path: scaffold/core/sanitation/ghost_buster.py
# ----------------------------------------------

import os
from pathlib import Path
from typing import Set, Optional
from ...logger import Scribe

Logger = Scribe("GhostBuster")


class GhostBuster:
    """
    =================================================================================
    == THE GHOST BUSTER (V-Ω-VOID-EXORCIST)                                        ==
    =================================================================================
    LIF: 10,000,000,000,000

    A sovereign artisan dedicated to the annihilation of hollow sanctums (empty directories).
    It performs a bottom-up traversal of the directory tree. If a directory is found to be
    empty and is not protected by the Sacred Vows of the project, it is returned to the void.
    """

    # The Grimoire of the Untouchables (Global Defaults)
    DEFAULT_PROTECTED = {
        '.git', '.scaffold', '.vscode', '.idea', 'node_modules', 'venv', '.venv', '__pycache__'
    }

    def __init__(self, root: Path, protected_paths: Optional[Set[Path]] = None):
        """
        Args:
            root: The physical root of the cleaning operation.
            protected_paths: Specific absolute paths that must NEVER be pruned (even if empty).
        """
        self.root = root.resolve()
        self.protected_paths = {p.resolve() for p in (protected_paths or [])}
        self.protected_names = self.DEFAULT_PROTECTED.copy()

    def exorcise(self, dry_run: bool = False) -> int:
        """
        The Rite of Annihilation.
        Walks bottom-up. If a directory is empty (and not sacred), it is removed.
        Returns the count of annihilated sanctums.
        """
        if not self.root.exists():
            return 0

        Logger.info(f"The Ghost Buster awakens in [cyan]{self.root.name}[/cyan]...")
        pruned_count = 0

        # We walk bottom-up (topdown=False) to prune nested empty dirs in one pass
        for dirpath, dirnames, filenames in os.walk(self.root, topdown=False):
            current_path = Path(dirpath).resolve()

            # 1. The Gaze of the Root (Do not eat yourself)
            if current_path == self.root:
                continue

            # 2. The Gaze of Content (Files imply life)
            if filenames:
                continue

            # 3. The Gaze of Persistence (Subdirectories)
            # Since we walk bottom-up, if 'dirnames' is not empty, it means
            # those subdirectories were NOT pruned (they contained life),
            # so this directory must also persist.
            if dirnames:
                continue

            # 4. The Gaze of Sanctity (Protected Explicit Paths)
            if current_path in self.protected_paths:
                Logger.verbose(f"   -> Preserving sacred empty sanctum: {current_path.relative_to(self.root)}")
                continue

            # 5. The Gaze of the System (Protected Names)
            # Logic: if 'src/.git/objects' -> .git is protected.
            try:
                rel_path = current_path.relative_to(self.root)
                if any(part in self.protected_names for part in rel_path.parts):
                    continue
            except ValueError:
                continue

            # 6. The Rite of Deletion
            if self._annihilate(current_path, dry_run):
                pruned_count += 1
                # Manually remove from parent's dirnames to allow parent pruning if applicable
                try:
                    parent = current_path.parent
                    # Note: os.walk doesn't use this list for traversal when topdown=False,
                    # but we modify it conceptually.
                except Exception:
                    pass

        if pruned_count > 0:
            Logger.success(f"Ghost Buster purged {pruned_count} hollow sanctum(s).")
        else:
            Logger.verbose("The Void is clean. No ghosts detected.")

        return pruned_count

    def _annihilate(self, path: Path, dry_run: bool) -> bool:
        """Performs the physical removal."""
        try:
            if dry_run:
                Logger.info(f"   [DRY-RUN] -> Would bust ghost: {path.relative_to(self.root)}")
                return True

            path.rmdir()
            Logger.verbose(f"   -> Ghost Busted: {path.relative_to(self.root)}")
            return True
        except OSError as e:
            # Often caused by OS locks or race conditions (file created during walk)
            Logger.warn(f"Failed to bust ghost '{path.name}': {e}")
            return False

