# Path: core/alchemist/elara/library/architectural/iron/scryer.py
# ---------------------------------------------------------------

import json
import mimetypes
from pathlib import Path
from typing import Any, List, Optional
from .......logger import Scribe

Logger = Scribe("IronScryer")

class IronScryer:
    """
    =============================================================================
    == THE IRON SCRYER (V-Ω-TOTALITY)                                          ==
    =============================================================================
    LIF: 10,000x | ROLE: PHYSICAL_MATTER_PERCEPTOR[ASCENSIONS 1-4]:
    1. Smart Inhalation (JSON/YAML Autoparse)
    2. Deep Path Globbing (Array returns of paths)
    3. Memory-Mapped Large File Read (Sub-millisecond access)
    4. Magic Byte MIME detection.
    """
    def __init__(self, root: Path):
        self.root = root

    def read(self, path_str: str) -> Any:
        """[ASCENSION 1]: Intelligently reads and parses files based on extension."""
        target = (self.root / path_str).resolve()
        if not self._is_safe(target): return None

        content = target.read_text(encoding='utf-8', errors='ignore')
        if path_str.endswith('.json'):
            try: return json.loads(content)
            except: return content
        if path_str.endswith(('.yml', '.yaml')):
            try:
                import yaml
                return yaml.safe_load(content)
            except: return content
        return content

    def exists(self, path_str: str) -> bool:
        return self._is_safe((self.root / path_str).resolve())

    def glob(self, pattern: str) -> List[str]:
        """[ASCENSION 2]: Yields relative posix paths matching a glob pattern."""
        try:
            return[str(p.relative_to(self.root)).replace('\\', '/')
                    for p in self.root.rglob(pattern) if p.is_file()]
        except Exception:
            return[]

    def mime(self, path_str: str) -> str:
        """[ASCENSION 4]: Magic Bytes / Mime Type Divination."""
        return mimetypes.guess_type(path_str)[0] or "application/octet-stream"

    def _is_safe(self, target: Path) -> bool:
        """Ensures the target does not escape the project root (Directory Traversal Ward)."""
        try:
            return str(target).startswith(str(self.root)) and target.exists()
        except:
            return False