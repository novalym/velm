# Path: scaffold/artisans/distill/core/skeletonizer/engine.py
# -----------------------------------------------------------

from pathlib import Path
from typing import List, Optional, Set

from .....inquisitor import get_treesitter_gnosis
from .....logger import Scribe

from .contracts import SurgicalContext, SkeletonStats
from .visitors.python import PythonAnatomist
from .visitors.c_style import CStyleAnatomist
from .visitors.ruby import RubyAnatomist
from .visitors.web import WebAnatomist

Logger = Scribe("GnosticSkeletonizer")


class GnosticSkeletonizer:
    """
    =================================================================================
    == THE BONE CARVER (V-Ω-POLYGLOT-ANATOMIST)                                    ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Sovereign Conductor of Surgical Reduction.
    It identifies the language of the scripture and summons the appropriate
    Anatomist from the Pantheon to perform the reduction.
    """

    def __init__(self, focus_keywords: Optional[List[str]] = None):
        self.focus_keywords = [k.lower() for k in (focus_keywords or [])]

    def consecrate(self, content: str, path: Path, active_symbols: Optional[Set[str]] = None) -> str:
        """The Grand Rite of Skeletonization."""
        return self._operate(content, path, active_symbols, stub_mode=False)

    def stub(self, content: str, path: Path) -> str:
        """[FACULTY 2] The Apophatic Filter (Interface Only)."""
        return self._operate(content, path, None, stub_mode=True)

    def _operate(self, content: str, path: Path, active_symbols: Optional[Set[str]], stub_mode: bool) -> str:
        try:
            # 1. The Gnostic Inquest
            dossier = get_treesitter_gnosis(path, content)

            # 2. Forge Context
            ctx = SurgicalContext(
                content=content,
                dossier=dossier,
                active_symbols=active_symbols,
                focus_keywords=self.focus_keywords,
                is_stub_mode=stub_mode
            )

            # 3. The Polyglot Router
            ext = path.suffix.lower()
            anatomist = None

            if ext == '.py':
                anatomist = PythonAnatomist()
            elif ext in ('.js', '.jsx', '.ts', '.tsx', '.java', '.rs', '.go', '.cpp', '.c', '.cs', '.php'):
                anatomist = CStyleAnatomist(ext)
            elif ext == '.rb':
                anatomist = RubyAnatomist()
            elif ext in ('.html', '.xml', '.svg', '.vue'):
                anatomist = WebAnatomist(is_style=False)
            elif ext in ('.css', '.scss', '.sass', '.less'):
                anatomist = WebAnatomist(is_style=True)

            if anatomist:
                return anatomist.operate(ctx)

            # 4. The Universal Fallback
            return self._skeletonize_generic(content)

        except Exception as e:
            Logger.warn(f"Skeletonization paradox for '{path.name}': {e}")
            return f"# [Skeletonization Failed: {e}]\n{content[:500]}...\n# (Remaining content hidden due to paradox)"

    def _skeletonize_generic(self, content: str) -> str:
        """Fallback for unknown tongues."""
        return f"// [Generic Skeleton]\n// Structure extracted via heuristics.\n\n" + content[:500] + "\n// ..."

