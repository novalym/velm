# Path: scaffold/artisans/create/safety.py
# ----------------------------------------
import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple

from rich.prompt import Confirm

from ...contracts.data_contracts import ScaffoldItem
from ...core.cortex.dependency_oracle import DependencyOracle
from ...logger import Scribe

Logger = Scribe("CreationGuardian")

class CreationGuardian:
    """
    =================================================================================
    == THE GUARDIAN OF MATERIALIZATION (V-Ω-SAFETY-WARD)                           ==
    =================================================================================
    Responsible for pre-flight checks, collision detection, and environment health.
    """

    def __init__(self, project_root: Path, console):
        self.project_root = project_root
        self.console = console

    def detect_collisions(self, items: List[ScaffoldItem]) -> List[Path]:
        """Returns a list of files that already exist on disk."""
        collisions = []
        for item in items:
            if item.is_dir: continue
            target = (self.project_root / item.path).resolve()
            if target.exists():
                collisions.append(target)
        return collisions

    def resolve_conflicts(self, items: List[ScaffoldItem]) -> List[ScaffoldItem]:
        """Interactively resolves overwrites."""
        pure_items = []
        for item in items:
            target = (self.project_root / item.path).resolve()
            if target.exists() and not item.is_dir:
                if not Confirm.ask(f"Scripture '[yellow]{item.path}[/yellow]' exists. Overwrite?", default=False):
                    Logger.info(f"Preserved: {item.path}")
                    continue
            pure_items.append(item)
        return pure_items

    def adjudicate_dependencies(self, needs: List[str], auto_install: bool = False):
        """[FACULTY 6] Summons the DependencyOracle to verify tools/libs."""
        Logger.info(f"Adjudicating dependencies: {needs}")
        oracle = DependencyOracle(self.project_root)
        try:
            success = oracle.adjudicate(needs, auto_install=auto_install)
            if not success:
                Logger.warn("Dependency resolution incomplete. The created scriptures may falter.")
        except Exception as e:
            Logger.error(f"Dependency Oracle encountered a paradox: {e}")

    def summon_editor(self, files: List[Path]):
        """[FACULTY 11] Opens the created files in the default editor."""
        editor = os.getenv('EDITOR') or os.getenv('VISUAL') or 'code'
        try:
            cmd = [editor] + [str(f) for f in files]
            Logger.info(f"Summoning editor: {' '.join(cmd)}")
            subprocess.run(cmd, check=False)
        except Exception as e:
            Logger.warn(f"Could not summon editor '{editor}': {e}")