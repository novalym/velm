# Path: core/daemon/resolver/dna.py
# ---------------------------------
# LIF: INFINITY | ROLE: ENV_ASSEMBLER
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from .constants import (
    ENV_PYTHONPATH, ENV_PATH, ENV_SCAFFOLD_EXE,
    ENV_IO_ENCODING, ENV_UTF8_MODE, ENV_NO_BYTECODE,
    ENV_GNOSTIC_DEBUG, ENV_LOG_LEVEL, ENV_LD_LIBRARY_PATH
)
from .identity import SystemIdentity

class EnvironmentForge:
    """
    [THE ALCHEMIST]
    Mixes the Base OS Environment with Gnostic DNA to create
    the perfect atmosphere for child processes.
    """

    def __init__(self, identity: SystemIdentity, executable: Path, venv: Optional[Path], source_root: Path):
        self.identity = identity
        self.executable = executable
        self.venv = venv
        self.source_root = source_root

    def forge(self, extra_vars: Dict[str, str] = None) -> Dict[str, str]:
        """
        Creates the Environment Dictionary.
        """
        # 1. Clone Host DNA
        env = os.environ.copy()

        # 2. Enforce Encoding Law
        env[ENV_IO_ENCODING] = "utf-8"
        env[ENV_UTF8_MODE] = "1"

        # 3. Inject Executable into PATH
        # We prepend the executable's directory to PATH to ensure consistency
        bin_dir = self.executable.parent
        env[ENV_PATH] = f"{bin_dir.as_posix()}{os.pathsep}{env.get(ENV_PATH, '')}"
        env[ENV_SCAFFOLD_EXE] = self.executable.as_posix()

        # 4. Graft PYTHONPATH (If running from source)
        if not self.identity.is_frozen:
            current_pp = env.get(ENV_PYTHONPATH, "")
            # Prepend Source Root
            new_pp = f"{self.source_root.as_posix()}{os.pathsep}{current_pp}"
            env[ENV_PYTHONPATH] = new_pp

            # [ASCENSION 2]: Frozen Time Bridge (PyInstaller hybrid mode)
            if self.identity.meipass:
                env[ENV_PYTHONPATH] = f"{self.identity.meipass}{os.pathsep}{env[ENV_PYTHONPATH]}"

        # 5. Debug Propagation
        if self.identity.is_debug:
            env[ENV_GNOSTIC_DEBUG] = "1"
            env[ENV_LOG_LEVEL] = "DEBUG"
            env[ENV_NO_BYTECODE] = "1" # Prevent stale bytecode

        # 6. Library Path Healing (Linux)
        if self.identity.platform == "linux":
            ld_path = env.get(ENV_LD_LIBRARY_PATH, "")
            local_lib = self.source_root / "lib"
            if local_lib.exists():
                env[ENV_LD_LIBRARY_PATH] = f"{local_lib.as_posix()}{os.pathsep}{ld_path}"

        # 7. Merge Extra DNA
        if extra_vars:
            env.update(extra_vars)

        return env