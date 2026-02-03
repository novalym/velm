# Path: scaffold/core/maestro/context.py
# --------------------------------------

import os
import re
import shlex
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple, Union

from .contracts import MaestroContext
from ..alchemist import DivineAlchemist
from ...creator.registers import QuantumRegisters
from ...logger import Scribe

Logger = Scribe("MaestroContextForge")


class ContextForge:
    """
    =================================================================================
    == THE UNBREAKABLE CONTEXT FORGE (V-Ω-CI-AWARE-HEALED-DEFENSIVE)               ==
    =================================================================================
    @gnosis:title The Unbreakable Context Forge
    @gnosis:summary Forges the execution environment. Now injects 'CI=true' to
                    prevent interactive tool crashes on Windows.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **The Gnostic Ward (THE FIX):** Safely handles `self.regs.gnosis` even if it
        has been corrupted into a non-dictionary form, preventing `AttributeError`.
    2.  **The Shell Diviner:** Intelligently selects the correct shell (bash, cmd, wsl)
        based on the environment and configuration.
    3.  **The Path Augmenter:** Automatically injects `node_modules/.bin` and `venv/bin`
        into the PATH for the child process.
    4.  **The CI Injector:** Sets `CI=true` and `DEBIAN_FRONTEND=noninteractive` to
        ensure automation tools behave correctly.
    """

    # FACULTY 2: The Gnostic Shell Grimoire
    SHELL_SOULS: Dict[str, Dict[str, Any]] = {
        "wsl": {
            "family": "posix",
            "path_separator": ":",
            "transmutation_rite": "_transmute_windows_path_to_wsl",
        },
        "bash": {
            "family": "posix",
            "path_separator": ":",
            "transmutation_rite": None,
        },
        "cmd": {
            "family": "windows",
            "path_separator": ";",
            "transmutation_rite": None,
        },
        "powershell": {
            "family": "windows",
            "path_separator": ";",
            "transmutation_rite": None,
        }
    }

    def __init__(self, registers: QuantumRegisters, alchemist: DivineAlchemist):
        self.regs = registers
        self.alchemist = alchemist

    def forge(self, line_num: int, explicit_undo: Optional[List[str]]) -> MaestroContext:
        """The Grand Rite of Reality Forging."""
        shell_executable, shell_soul = self._divine_shell_soul()

        base_cwd = self._resolve_sanctum()
        transmuted_cwd = base_cwd
        if shell_soul and shell_soul["transmutation_rite"]:
            transmutation_func = getattr(self, shell_soul["transmutation_rite"])
            transmuted_cwd = Path(transmutation_func(str(base_cwd)))
            Logger.verbose(f"Cross-Reality CWD Transmuted: '{base_cwd}' -> '{transmuted_cwd}'")

        env = self._forge_environment(base_cwd, shell_executable, shell_soul)

        return MaestroContext(
            line_num=line_num,
            explicit_undo=explicit_undo,
            cwd=transmuted_cwd,
            env=env,
            shell_executable=shell_executable
        )

    def _resolve_sanctum(self) -> Path:
        sanctum_root = Path(self.regs.sanctum.root)
        logical_root = self.regs.project_root

        if not logical_root or str(logical_root) == ".":
            return sanctum_root.resolve()

        cwd = (sanctum_root / logical_root).resolve()
        if not cwd.exists():
            Logger.warn(f"Maestro cannot conduct in void '{cwd}'. Falling back to Sanctum Root.")
            return sanctum_root.resolve()
        return cwd

    def _get_gnostic_dict(self) -> Dict[str, Any]:
        """
        [THE GNOSTIC WARD]
        Ensures we always get a dictionary, even if the registers hold a profane string.
        """
        if isinstance(self.regs.gnosis, dict):
            return self.regs.gnosis

        # If corrupted, return empty dict to prevent crash
        Logger.warn(
            f"Gnostic Corruption Detected: Registers hold {type(self.regs.gnosis)} instead of Dict. Assuming empty.")
        return {}

    def _divine_shell_soul(self) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        [THE RITE OF DIVINATION - FORTIFIED]
        Perceives the true shell soul to be summoned, protected against malformed Gnosis.
        """
        gnosis = self._get_gnostic_dict()
        shell_gnosis = None

        # [THE DEFENSIVE GAZE]
        # We access 'scaffold_env' safely. Even if gnosis is a dict, 'scaffold_env'
        # might have been overwritten by a string variable during alchemy.
        try:
            scaffold_env = gnosis.get("scaffold_env")
            if isinstance(scaffold_env, dict):
                shell_gnosis = scaffold_env.get("shell_path")
            elif scaffold_env is not None:
                # If it exists but is not a dict, it is heresy. We ignore it.
                Logger.debug(f"Ignored malformed 'scaffold_env': Expected dict, got {type(scaffold_env).__name__}")
        except Exception as e:
            Logger.warn(f"Paradox reading shell configuration: {e}")

        # If explicit shell path found in Gnosis
        if shell_gnosis and isinstance(shell_gnosis, str):
            shell_path = shutil.which(shell_gnosis)
            if shell_path:
                if 'bash.exe' in shell_path and sys.platform == 'win32':
                    return shell_path, self.SHELL_SOULS['wsl']
                if 'bash' in shell_path:
                    return shell_path, self.SHELL_SOULS['bash']

        # Fallback Logic
        if sys.platform != "win32":
            shell_path = shutil.which("bash") or shutil.which("sh")
            if shell_path:
                return shell_path, self.SHELL_SOULS['bash']

        shell_path = shutil.which("cmd.exe")
        if shell_path:
            return shell_path, self.SHELL_SOULS['cmd']

        return "/bin/sh", self.SHELL_SOULS['bash']

    # Alias for internal consistency
    _get_gnosis_dict = _get_gnostic_dict

    def _forge_environment(self, execution_root: Path, shell_executable: str, shell_soul: Dict) -> Dict[str, str]:
        """
        [THE ENVIRONMENT ALCHEMIST]
        Injects system variables and the Critical 'CI=true' flag.
        """
        env = os.environ.copy()
        gnosis = self._get_gnostic_dict()

        # [THE FIX] The Vow of Automation
        # This tells npm, git, and others: "Do not wait for a human. Do not prompt."
        env["CI"] = "true"
        env["CONTINUOUS_INTEGRATION"] = "true"
        env["DEBIAN_FRONTEND"] = "noninteractive"  # For Linux apt-get

        for k, v in gnosis.items():
            if isinstance(v, (str, int, bool)):
                safe_key = "SC_" + re.sub(r'[^A-Z0-9_]', '_', str(k).upper())
                env[safe_key] = str(v)

        env["SC_PROJECT_ROOT"] = str(self.regs.project_root or self.regs.sanctum)
        env["SC_CWD"] = str(execution_root)

        augmented_path_list = self._augment_path(execution_root, env)

        final_paths = []
        transmutation_rite_name = shell_soul.get("transmutation_rite") if shell_soul else None

        if transmutation_rite_name:
            transmutation_func = getattr(self, transmutation_rite_name)
            for p in augmented_path_list:
                final_paths.append(transmutation_func(p))
        else:
            final_paths = [p for p in augmented_path_list if p]

        if final_paths:
            path_separator = shell_soul.get("path_separator", os.pathsep) if shell_soul else os.pathsep
            unique_paths = list(dict.fromkeys(final_paths))
            env["PATH"] = path_separator.join(unique_paths)

        env["PYTHONIOENCODING"] = "utf-8"
        return env

    def _augment_path(self, execution_root: Path, current_env: Dict) -> List[str]:
        paths_to_add = []
        node_bin = execution_root / "node_modules" / ".bin"
        if node_bin.exists(): paths_to_add.append(str(node_bin))

        venv_bin_name = "Scripts" if sys.platform == "win32" else "bin"
        # Check potential venv locations
        for venv_parent in [execution_root, self.regs.project_root]:
            if not venv_parent: continue
            for venv_name in ["venv", ".venv", "env"]:
                venv_bin = venv_parent / venv_name / venv_bin_name
                if venv_bin.exists():
                    paths_to_add.append(str(venv_bin))

        current_path_str = current_env.get("PATH", "")
        return paths_to_add + current_path_str.split(os.pathsep)

    def _transmute_windows_path_to_wsl(self, path_str: str) -> str:
        if not path_str: return ""
        match = re.match(r'^([a-zA-Z]):[\\/]', path_str)
        if match:
            drive = match.group(1).lower()
            rest = path_str[len(match.group(0)):].replace('\\', '/')
            wsl_path = f'/mnt/{drive}/{rest}'
            return wsl_path
        return path_str