# Path: scaffold/core/ignition/diviner/sentinel/scanner.py
# --------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: SENTINEL_SCANNER_V1

import os
import shutil
from pathlib import Path
from typing import Optional, List
from .grimoire import TOOL_GRIMOIRE
from ....logger import Scribe

Logger = Scribe("OcularScanner")


class ArtisanScanner:
    """
    =============================================================================
    == THE OCULAR SCANNER (V-Ω-PATH-TRIAGE)                                    ==
    =============================================================================
    [ASCENSION 1]: Performs an aggressive, multi-vector search for binaries.
    """

    @classmethod
    def find_binary(cls, name: str) -> Optional[Path]:
        # 1. Standard PATH scry
        path = shutil.which(name)
        if path:
            return Path(path).resolve()

        # 2. Alternative scry (for Windows .cmd/.exe)
        config = TOOL_GRIMOIRE.get(name, {})
        for alt in config.get("binary_alternatives", []):
            path = shutil.which(alt)
            if path:
                return Path(path).resolve()

        # 3. [ASCENSION 27]: Windows AppData/Programs Scry
        if os.name == 'nt':
            path = cls._scry_windows_depths(name)
            if path: return path

        # 4. [ASCENSION 28]: MacOS Bundle Inception
        if os.uname().sysname == 'Darwin':
            # Future: logic for /Applications/.../Contents/MacOS
            pass

        return None

    @classmethod
    def _scry_windows_depths(cls, name: str) -> Optional[Path]:
        local_appdata = os.environ.get('LOCALAPPDATA', '')
        prog_files = os.environ.get('ProgramFiles', '')

        candidates = [
            Path(local_appdata) / "Microsoft/WindowsApps" / f"{name}.exe",
            Path(prog_files) / "nodejs" / f"{name}.exe",
            # Add more specific known paths here
        ]

        for cand in candidates:
            if cand.exists():
                return cand.resolve()
        return None

