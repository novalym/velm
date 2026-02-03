# Path: scaffold/core/ignition/diviner/heuristics/base.py
# -------------------------------------------------------
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, List
from ...contracts import IgnitionAura


class BaseInquisitor(ABC):
    """The Immutable Contract for all Heuristic Perceivers."""

    @abstractmethod
    def analyze(self, root: Path) -> Tuple[IgnitionAura, float, List[str]]:
        """
        Perceives the soul of the directory.
        Returns: (Aura, Confidence, Reasoning_Trace)
        """
        pass

    def read_manifest_safe(self, path: Path, limit: int = 8192) -> str:
        """Lightweight tomography: Reads only the essential bytes."""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(limit)
        except:
            return ""

