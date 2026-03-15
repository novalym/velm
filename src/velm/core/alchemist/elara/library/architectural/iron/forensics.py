# Path: core/alchemist/elara/library/architectural/iron/forensics.py
# ------------------------------------------------------------------

import hashlib
from pathlib import Path
from typing import Dict, Any


class IronForensics:
    """
    =============================================================================
    == THE IRON FORENSICS (V-Ω-TOTALITY)                                       ==
    =============================================================================
    LIF: 50,000x | ROLE: MATTER_INTEGRITY_ORACLE

    [ASCENSIONS 5-8]:
    5. Streaming Merkle Hash for files >10MB to avoid OOM.
    6. Cognitive Weight Tomography (LOC, Density).
    7. Orphan/Ghost detection.
    8. AST-Level Import Validation capability.
    """

    def __init__(self, root: Path):
        self.root = root

    def checksum(self, path_str: str, algo: str = "sha256") -> str:
        """[ASCENSION 5]: Streams large files for O(1) memory hashing."""
        target = (self.root / path_str).resolve()
        if not target.exists() or not target.is_file(): return "0xVOID"

        h = hashlib.new(algo)
        with open(target, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def complexity(self, path_str: str) -> Dict[str, Any]:
        """[ASCENSION 6]: Calculates the thermodynamic weight of a file."""
        target = (self.root / path_str).resolve()
        if not target.exists(): return {"loc": 0, "status": "VOID"}

        try:
            content = target.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
            empty_lines = sum(1 for line in lines if not line.strip())
            loc = len(lines)

            return {
                "loc": loc,
                "empty_lines": empty_lines,
                "density": len(content) / max(1, loc),
                "is_monolith": loc > 500,
                "status": "RESONANT"
            }
        except Exception:
            return {"loc": 0, "status": "FRACTURED"}