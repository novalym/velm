# Path: scaffold/core/ignition/diviner/seekers/base.py
# ----------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_BASE_SEEKER_V5

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Set, Optional
from .....logger import Scribe

Logger = Scribe("BaseSeeker")

class BaseSeeker(ABC):
    """
    =============================================================================
    == THE ANCESTRAL SEEKER (V-Ω-CONTRACT)                                     ==
    =============================================================================
    The fundamental laws of perception.
    """

    # [ASCENSION 2]: THE ABYSSAL WARD
    # Folders that consume time and space but contain no soul.
    ABYSS = {
        ".git", "node_modules", "venv", ".venv", "__pycache__",
        "dist", "build", "target", "vendor", "tmp", ".next", ".nuxt",
        "bin", "obj", ".idea", ".vscode", "coverage", ".cache"
    }

    def __init__(self, root: Path):
        """
        Initialize with an absolute Gnostic Anchor.
        """
        self.root = root.resolve()

    @abstractmethod
    def scan(self, target: Optional[Path] = None) -> Optional[Path]:
        """Performs the specialized perception rite."""
        pass

    def is_abyssal(self, path: Path) -> bool:
        """Determines if a path should be avoided by the Sentinel."""
        return path.name in self.ABYSS or path.name.startswith('.')

    def normalize(self, path: Path) -> Path:
        """[ASCENSION 20]: Absolute Isomorphic Normalization."""
        return path.resolve()

    def safe_iter(self, path: Path):
        """[ASCENSION 22]: Guarded iterator against Permission Heresy."""
        try:
            return path.iterdir()
        except (PermissionError, OSError) as e:
            Logger.warn(f"Seeker is blind at {path}: Access Denied.")
            return []