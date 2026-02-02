# Path: scaffold/parser_core/logic_weaver/state.py
# ------------------------------------------------

from typing import Dict, Any, Set, List
from pathlib import Path
from ...logger import Scribe
from ...utils import find_project_root

Logger = Scribe("LogicState")


class GnosticContext:
    """
    The Keeper of Truth.
    Manages variables, project root, and the Virtual Manifest of creation.
    """

    def __init__(self, raw_context: Dict[str, Any]):
        self._context = raw_context.copy()

        # 1. The Rite of Contextual Anchoring
        if 'project_root' not in self._context:
            found_root, _ = find_project_root(Path.cwd())
            self._context['project_root'] = found_root or Path.cwd()

        if isinstance(self._context['project_root'], str):
            self._context['project_root'] = Path(self._context['project_root'])

        # 2. The Virtual Reality Engine
        # Tracks files we intend to create to satisfy "file_exists" checks immediately
        self.virtual_manifest: Set[str] = set()

        # Bind virtual manifest to context for the Adjudicator
        self._context['generated_manifest'] = self.virtual_manifest

        # 3. The Boolean Purifier
        self._purify_booleans()

    def _purify_booleans(self):
        """Transmutes string truths into boolean souls."""
        for k, v in self._context.items():
            if isinstance(v, str):
                lower_v = v.lower()
                if lower_v in ('true', 'yes', '1', 'on'):
                    self._context[k] = True
                elif lower_v in ('false', 'no', '0', 'off'):
                    self._context[k] = False

    def register_virtual_file(self, path: Path):
        """Inscribes a path into the Virtual Reality."""
        clean_path = str(path).replace('\\', '/')
        self.virtual_manifest.add(clean_path)
        # Update the list reference for the Adjudicator
        self._context['generated_manifest'] = list(self.virtual_manifest)

    @property
    def raw(self) -> Dict[str, Any]:
        """Access the raw dictionary for Alchemical transmutation."""
        return self._context