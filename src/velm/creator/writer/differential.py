# Path: scaffold/creator/writer/differential.py
# ---------------------------------------------
import hashlib
import difflib
from typing import Tuple, Optional


class DifferentialEngine:
    """
    =============================================================================
    == THE ORACLE OF DIFFERENCE (V-Ω-HASH-COMPARATOR)                          ==
    =============================================================================
    Calculates cryptographic hashes and textual diffs.
    """

    @staticmethod
    def compute_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def compute_diff(old_text: str, new_text: str, filename: str) -> Optional[str]:
        if old_text == new_text: return None

        diff_gen = difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
        )
        return "".join(diff_gen)