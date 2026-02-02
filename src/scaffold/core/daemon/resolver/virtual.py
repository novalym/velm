# Path: core/daemon/resolver/virtual.py
# -------------------------------------
# LIF: INFINITY | ROLE: ENV_SCANNER
import sys
import os
from pathlib import Path
from typing import Optional
from .constants import ENV_CONDA_PREFIX, ENV_VIRTUAL_ENV


class VenvScanner:
    """
    [THE X-RAY]
    Penetrates the veil to find the Virtual Environment root.
    """

    @staticmethod
    def scan() -> Optional[Path]:
        # 1. Standard Venv / Virtualenv
        # Check if we are running inside one
        if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
            return Path(sys.prefix).resolve()

        # 2. Conda
        if ENV_CONDA_PREFIX in os.environ:
            return Path(os.environ[ENV_CONDA_PREFIX]).resolve()

        # 3. Poetry / Generic Env Var
        if ENV_VIRTUAL_ENV in os.environ:
            return Path(os.environ[ENV_VIRTUAL_ENV]).resolve()

        # 4. Proximity Scan (The Heuristic)
        # Look for .venv/ or venv/ in parent directories
        current = Path.cwd()
        for _ in range(4):  # Limit recursion to 4 levels
            for name in [".venv", "venv", "env"]:
                probe = current / name
                if probe.exists() and probe.is_dir():
                    # Validate it has a scripts/bin dir
                    if (probe / "bin").exists() or (probe / "Scripts").exists():
                        return probe.resolve()

            if current.parent == current: break
            current = current.parent

        return None

