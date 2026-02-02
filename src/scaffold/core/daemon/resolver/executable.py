# Path: core/daemon/resolver/executable.py
# ----------------------------------------
# LIF: INFINITY | ROLE: BINARY_SEEKER
import sys
import shutil
from pathlib import Path
from typing import Optional
from .constants import SHIM_WIN, SHIM_NIX


class BinaryDiviner:
    """
    [THE SEEKER]
    Locates the executable entry point for child processes.
    Crucial for spawning the CLI from the Daemon.
    """

    @staticmethod
    def divine(is_frozen: bool, platform: str) -> Path:
        """
        Determines the path to the 'scaffold' executable.
        """
        # STRATEGY A: WE ARE FROZEN (PyInstaller)
        # The executable is the process itself.
        if is_frozen:
            return Path(sys.executable).resolve()

        # STRATEGY B: VENV BINARY
        # Look adjacent to the python interpreter (Scripts/ or bin/)
        interpreter = Path(sys.executable).resolve()
        bin_dir = interpreter.parent

        candidates = [SHIM_WIN, SHIM_NIX, "scaffold.cmd"]

        for cand in candidates:
            target = bin_dir / cand
            if target.exists():
                return target

        # STRATEGY C: SYSTEM PATH SCAN
        # If running raw python, maybe 'scaffold' is in the global PATH
        which_scaffold = shutil.which("scaffold")
        if which_scaffold:
            return Path(which_scaffold).resolve()

        # STRATEGY D: FALLBACK
        # Just use the python interpreter itself.
        # The dispatcher will handle "python -m scaffold" logic if needed.
        return interpreter