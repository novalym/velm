# Path: genesis/genesis_engine/perception.py
# ------------------------------------------
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from ...contracts.data_contracts import GnosticProphecy
from ...prophecy import prophesy_initial_gnosis
from ...logger import Scribe

if TYPE_CHECKING:
    from .engine import GenesisEngine

Logger = Scribe("GenesisPerception")


class PerceptionMixin:
    """
    =================================================================================
    == THE EYE OF THE GENESIS ENGINE (V-Ω-PERCEPTION-LAYER)                        ==
    =================================================================================
    Handles all rites of Gnostic Perception: gazing into the void, prophesying
    defaults, and understanding the state of the sanctum.
    """

    def _is_sanctum_void(self: 'GenesisEngine') -> bool:
        """
        [THE GAZE OF THE VOID - ASCENDED]
        Checks if the directory is empty, righteously ignoring system artifacts.
        This prevents the 'False Apotheosis' heresy where a git init triggers a distill prompt.
        """
        # The Grimoire of Invisible Spirits
        IGNORED_ARTIFACTS = {
            '.git', '.scaffold', '.idea', '.vscode', '.DS_Store', 'Thumbs.db',
            '__pycache__', 'venv', '.venv', 'env'
        }

        if not self.project_root.exists():
            return True

        for item in self.project_root.iterdir():
            if item.name not in IGNORED_ARTIFACTS:
                Logger.verbose(f"Sanctum is not void. Perceived profane artifact: '{item.name}'")
                return False  # A profane object exists

        return True

    def _gaze_upon_the_cosmos(self: 'GenesisEngine') -> GnosticProphecy:
        """
        [THE ORACLE OF PROPHECY, ASCENDED]
        Summons the one true, universal Prophet to guess defaults for the project.
        """
        Logger.verbose("The Genesis Oracle awakens the Universal Prophet...")

        # The Divine Delegation
        defaults = prophesy_initial_gnosis(self.project_root)

        # The Gnosis of description remains a local concern for now.
        if not defaults.get("description"):
            author = defaults.get('author', 'The Architect')
            project = defaults.get('project_name', 'your-project')
            defaults["description"] = f"A new project ({project}) by {author}"

        # We must forge a chronicle for the dialogue, even if it's simple.
        chronicle = {key: "from Prophecy" for key in defaults.keys()}

        return GnosticProphecy(defaults=defaults, chronicle=chronicle)