# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/facade.py
# -------------------------------------------------------------------------------

from pathlib import Path
from typing import Optional, TYPE_CHECKING, List
from ...logger import Scribe
from .strategies import STRATEGY_REGISTRY
from .contracts import StructureStrategy

if TYPE_CHECKING:
    from ..kernel.transaction import GnosticTransaction

Logger = Scribe("StructureSentinel")


class StructureSentinel:
    """
    =================================================================================
    == THE SENTINEL OF STRUCTURE (V-Ω-CONTEXT-AWARE-LOGGING)                       ==
    =================================================================================
    The divine Guardian of Architectural Integrity.
    Now capable of perceiving the soul of a directory to choose the correct law.
    """

    def __init__(self, project_root: Path, transaction: Optional["GnosticTransaction"] = None):
        self.project_root = project_root
        self.transaction = transaction
        self.strategies = STRATEGY_REGISTRY
        Logger.verbose(f"Structure Sentinel initialized. Strategies: {list(self.strategies.keys())}")

    def ensure_structure(self, path: Path):
        """
        The Rite of Consecration.
        """
        Logger.info(f"Sentinel gazing upon: [cyan]{path.name}[/cyan]")

        strategies_to_invoke = []

        if path.is_dir():
            # [THE FIX] Directory Inference
            # We peek inside to see what language this sanctum speaks.
            strategies_to_invoke = self._divine_strategies_from_dir(path)
            if not strategies_to_invoke:
                Logger.verbose(f"   -> No known language signatures found in directory '{path.name}'.")
        else:
            # File Inference (Extension)
            ext = path.suffix.lower()
            if ext in self.strategies:
                strategies_to_invoke.append(self.strategies[ext])
            else:
                Logger.verbose(f"   -> No strategy found for extension '{ext}'.")

        if not strategies_to_invoke:
            return

        for strategy in strategies_to_invoke:
            try:
                Logger.info(f"   -> Invoking {strategy.__class__.__name__}...")
                strategy.consecrate(path, self.project_root, self.transaction)
            except Exception as e:
                Logger.warn(f"Structural Consecration failed for '{path}': {e}")

    def _divine_strategies_from_dir(self, directory: Path) -> List[StructureStrategy]:
        """Scans a directory to determine which strategies apply."""
        found_strategies = []
        # Heuristic: Check files inside to guess language
        try:
            # We look for common markers
            has_py = any(f.suffix == '.py' for f in directory.iterdir())
            has_rs = any(f.suffix == '.rs' for f in directory.iterdir())
            has_js = any(f.suffix in ('.js', '.ts', '.tsx', '.jsx') for f in directory.iterdir())

            if has_py and '.py' in self.strategies:
                found_strategies.append(self.strategies['.py'])
            if has_rs and '.rs' in self.strategies:
                found_strategies.append(self.strategies['.rs'])
            if has_js:
                # Add JS strategy if needed (currently mapped to boundary checks)
                pass

        except Exception as e:
            Logger.warn(f"Could not gaze into directory '{directory.name}': {e}")

        return found_strategies