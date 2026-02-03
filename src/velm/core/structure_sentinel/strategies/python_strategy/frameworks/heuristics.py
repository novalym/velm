# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/heuristics.py
# ------------------------------------------------------------------------------------------------------------------------

from pathlib import Path
from typing import List, Optional, Any


class EntrypointDiviner:
    """
    [THE ENTRYPOINT BLOODHOUND]
    Scores files to find the application root.
    """

    def __init__(self, reader_func):
        self.read = reader_func

    def find_best_match(self, root: Path, markers: List[str], tx: Any) -> Optional[Path]:
        candidates = []
        # Search common locations
        search_paths = [root, root / "src", root / "app"]
        for base in search_paths:
            if base.exists():
                candidates.extend(base.glob("*.py"))

        best_candidate = None
        best_score = 0

        for cand in candidates:
            if cand.name.startswith("test_") or cand.name == "conftest.py":
                continue

            score = 0
            # Filename Weight
            if cand.name == "main.py":
                score += 20
            elif cand.name == "app.py":
                score += 15
            elif cand.name == "wsgi.py":
                score += 10
            elif cand.name == "asgi.py":
                score += 10
            elif cand.name == "settings.py":
                score += 5  # Low score, usually config

            # Content Weight
            try:
                content = self.read(cand, root, tx)
                for marker in markers:
                    if marker in content:
                        score += 50

                # Boost if it instantiates the class
                if " = " in content and "(" in content:
                    score += 5
            except:
                pass

            if score > best_score:
                best_score = score
                best_candidate = cand

        return best_candidate if best_score > 0 else None

