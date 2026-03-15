# Path: src/velm/codex/atoms/guide_knowledge/project_memory.py
# -----------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, Optional


class ProjectMemory:
    """The persistent archive of Project-Specific Gnosis."""

    @staticmethod
    def recall(label: str) -> Optional[str]:
        """Scries the local cache for taught wisdom."""
        path = Path(".scaffold/cache/guide_memory.json")
        if not path.exists(): return None

        try:
            data = json.loads(path.read_text())
            return data.get(label.lower())
        except:
            return None

    @staticmethod
    def census() -> list:
        """Proclaims the names of all adopted logic shards."""
        path = Path(".scaffold/cache/guide_memory.json")
        if not path.exists(): return []
        try:
            return list(json.loads(path.read_text()).keys())
        except:
            return []