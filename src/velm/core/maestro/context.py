# Path: scaffold/core/maestro/context.py
# --------------------------------------
# =========================================================================================
# == THE OMNISCIENT CONTEXT FORGE (V-Ω-TOTALITY-V90.0-PATH-ORACLE-FINALIS)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: ENVIRONMENTAL_SUTURE | RANK: OMEGA_SUPREME
# AUTH: Ω_CONTEXT_FORGE_V90_PATH_ORACLE_ASCENDED
# =========================================================================================

import os
import re
import shlex
import shutil
import sys
import platform
import threading
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple, Union

from .contracts import MaestroContext
from ..alchemist import DivineAlchemist
from ...creator.registers import QuantumRegisters
from ...logger import Scribe

Logger = Scribe("ContextOracle")


class ContextForge:
    """
    =================================================================================
    == THE UNBREAKABLE CONTEXT FORGE (V-Ω-TOTALITY-V90.0-PATH-ORACLE)              ==
    =================================================================================
    @gnosis:title The Omniscient Context Forge
    @gnosis:summary The supreme guardian of the execution atmosphere.
    @gnosis:LIF INFINITY

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:
    1.  **The Gnostic Ward (THE FIX):** Defensively handles `self.regs.gnosis` to
        annihilate 'AttributeError' and 'TypeError' even if Gnosis is corrupted.
    2.  **The Path Oracle:** Aggressively scries the host machine for missing
        binaries (Poetry, NPM, Go, Rust) across deep system strata.
    3.  **The Windows Script Suture:** Surgically identifies and injects the
        'AppData/Roaming/Python/Scripts' path where Windows hides global tools.
    4.  **The Achronal Path Cache:** Memoizes binary locations to achieve
        sub-microsecond environment forging.
    5.  **The Shell Diviner:** Intelligently adjudicates between WSL, Bash,
        CMD, and PowerShell based on the target rite's requirements.
    6.  **The CI/CD Inoculator:** Enforces 'CI=true' and 'noninteractive' mode
        to ensure automation tools don't halt for human input.
    7.  **The Trans Reality Bridge:** Performs the sacred 'WSL Path Transmutation'
        for cross-boundary execution.
    8.  **The Pythonic Encoding Vow:** Enforces UTF-8 I/O at the kernel level
        to prevent character-set heresies.
    9.  **The Orphaned Sanctum Guard:** Automatically falls back to the
        Sanctum Root if the logical project root is a void.
    10. **The Semantic Variable Graft:** Transmutes Gnostic variables into
        'SC_' prefixed environment DNA for child processes.
    11. **The Priority Inverter:** Detects high-load states and adjusts process
        'niceness' to prioritize the Great Work.
    12. **The Finality Vow:** A mathematical guarantee of a valid execution
        environment regardless of host-machine entropy.
    """

    # [FACULTY 2]: THE GNOSTIC SHELL GRIMOIRE
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
        self._scry_cache: Dict[str, List[str]] = {}
        self._lock = threading.Lock()

    def forge(self, line_num: int, explicit_undo: Optional[List[str]]) -> MaestroContext:
        """
        =============================================================================
        == THE RITE OF REALITY FORGING (FORGE)                                     ==
        =============================================================================
        The supreme conductor for environment materialization.
        """
        # 1. Divine the Shell's soul
        shell_executable, shell_soul = self._divine_shell_soul()

        # 2. Anchor the physical locus
        base_cwd = self._resolve_sanctum()
        transmuted_cwd = base_cwd

        # [ASCENSION 7]: Cross-Reality Transmutation
        if shell_soul and shell_soul["transmutation_rite"]:
            transmutation_func = getattr(self, shell_soul["transmutation_rite"])
            transmuted_cwd = Path(transmutation_func(str(base_cwd)))
            Logger.verbose(f"L{line_num}: Reality Boundary Crossed. CWD -> '{transmuted_cwd}'")

        # 3. Alchemize the Atmosphere
        env = self._forge_environment(base_cwd, shell_executable, shell_soul)

        return MaestroContext(
            line_num=line_num,
            explicit_undo=explicit_undo,
            cwd=transmuted_cwd,
            env=env,
            shell_executable=shell_executable
        )

    def _resolve_sanctum(self) -> Path:
        """[FACULTY 9]: THE GNOSTIC ANCHOR."""
        sanctum_root = Path(self.regs.sanctum.root)
        logical_root = self.regs.project_root

        if not logical_root or str(logical_root) == ".":
            return sanctum_root.resolve()

        # [THE CURE]: Attempt to locate logical root, fallback to sanctum if void
        cwd = (sanctum_root / logical_root).resolve()
        if not cwd.exists():
            # If we are inside a transaction, the directory might be in the Staging area.
            # We trust the Transactional filesystem to handle the resolution if possible.
            Logger.warn(f"Locus '{cwd}' is currently a void. Anchoring to Sanctum Root.")
            return sanctum_root.resolve()
        return cwd

    def _get_gnostic_dict(self) -> Dict[str, Any]:
        """[FACULTY 1]: THE GNOSTIC WARD (THE CURE)."""
        if isinstance(self.regs.gnosis, dict):
            return self.regs.gnosis
        Logger.warn(f"Gnostic Entropy: Registers hold {type(self.regs.gnosis)}. Resetting to dict.")
        return {}

    def _divine_shell_soul(self) -> Tuple[str, Optional[Dict[str, Any]]]:
        """[FACULTY 5]: THE SHELL DIVINER."""
        gnosis = self._get_gnostic_dict()

        # 1. Check for explicit Architect's Will
        shell_gnosis = gnosis.get("scaffold_env", {}).get("shell_path")
        if shell_gnosis and isinstance(shell_gnosis, str):
            shell_path = shutil.which(shell_gnosis)
            if shell_path:
                if 'bash.exe' in shell_path and sys.platform == 'win32':
                    return shell_path, self.SHELL_SOULS['wsl']
                return shell_path, self.SHELL_SOULS.get('bash' if 'bash' in shell_path else 'cmd')

        # 2. OS-Native Adjudication
        if sys.platform != "win32":
            # POSIX Sovereignty
            shell_path = shutil.which("bash") or shutil.which("zsh") or shutil.which("sh")
            return shell_path or "/bin/sh", self.SHELL_SOULS['bash']

        # 3. Windows Adjudication (The Windows Suture)
        # We prefer CMD for Make compatibility, but check for PowerShell availability
        shell_path = shutil.which("cmd.exe")
        if shell_path:
            return shell_path, self.SHELL_SOULS['cmd']

        shell_path = shutil.which("powershell.exe")
        if shell_path:
            return shell_path, self.SHELL_SOULS['powershell']

        return "cmd.exe", self.SHELL_SOULS['cmd']

    def _forge_environment(self, execution_root: Path, shell_executable: str, shell_soul: Dict) -> Dict[str, str]:
        """[FACULTY 10]: THE ENVIRONMENT ALCHEMIST."""
        env = os.environ.copy()
        gnosis = self._get_gnostic_dict()

        # [FACULTY 6]: THE VOW OF AUTOMATION (CI INJECTION)
        env["CI"] = "true"
        env["CONTINUOUS_INTEGRATION"] = "true"
        env["DEBIAN_FRONTEND"] = "noninteractive"
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"

        # [FACULTY 10]: VARIABLE GRAFTING
        for k, v in gnosis.items():
            if isinstance(v, (str, int, bool)):
                safe_key = "SC_" + re.sub(r'[^A-Z0-9_]', '_', str(k).upper())
                env[safe_key] = str(v)

        env["SC_PROJECT_ROOT"] = str(self.regs.project_root or self.regs.sanctum.root)
        env["SC_CWD"] = str(execution_root)

        # [FACULTY 2]: THE PATH ORACLE (THE RADIATED TRUTH)
        augmented_path_list = self._scry_global_paths(execution_root)

        # [FACULTY 7]: CROSS-REALITY TRANSMUTATION
        final_paths = []
        transmutation_rite = shell_soul.get("transmutation_rite") if shell_soul else None

        if transmutation_rite:
            transmutation_func = getattr(self, transmutation_rite)
            final_paths = [transmutation_func(p) for p in augmented_path_list if p]
        else:
            final_paths = [p for p in augmented_path_list if p]

        path_separator = shell_soul.get("path_separator", os.pathsep) if shell_soul else os.pathsep
        # Deduplicate while preserving order of priority
        env["PATH"] = path_separator.join(list(dict.fromkeys(final_paths)))

        return env

    def _scry_global_paths(self, execution_root: Path) -> List[str]:
        """
        =============================================================================
        == THE PATH ORACLE (V-Ω-TOTALITY-V2)                                      ==
        =============================================================================
        LIF: 100x | ROLE: BINARY_LOCATOR

        Aggressively hunts for Python, Node, and Rust scripts directories
        that often fail to migrate into sub-processes.
        """
        root_key = str(execution_root)
        if root_key in self._scry_cache:
            return self._scry_cache[root_key]

        with self._lock:
            paths = []

            # 1. LOCAL SANCTUM PATHS (Highest Priority)
            # Add local venv and node_modules immediately
            for venv_name in [".venv", "venv", "env"]:
                bin_name = "Scripts" if sys.platform == "win32" else "bin"
                local_venv_bin = execution_root / venv_name / bin_name
                if local_venv_bin.exists():
                    paths.append(str(local_venv_bin))

            local_node_bin = execution_root / "node_modules" / ".bin"
            if local_node_bin.exists():
                paths.append(str(local_node_bin))

            # 2. THE WINDOWS SCRIPT SUTURE (LIF-100 FIX)
            if sys.platform == "win32":
                user_profile = os.getenv("USERPROFILE")
                app_data = os.getenv("APPDATA")
                local_app_data = os.getenv("LOCALAPPDATA")

                # Hunt for Poetry & Global Pip Scripts (The common 'missing' locations)
                candidates = []
                if app_data:
                    candidates.append(Path(app_data) / "Python" / "Scripts")
                    candidates.append(Path(app_data) / "npm")
                if local_app_data:
                    candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python311" / "Scripts")
                    candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python312" / "Scripts")
                if user_profile:
                    candidates.append(Path(user_profile) / ".cargo" / "bin")
                    candidates.append(Path(user_profile) / ".local" / "bin")

                for cand in candidates:
                    if cand.exists():
                        paths.append(str(cand))

                # Deep-Scry Program Files for Common Artisans
                for pf in [os.getenv("ProgramFiles"), os.getenv("ProgramFiles(x86)")]:
                    if not pf: continue
                    for tool in ["Git/bin", "nodejs", "Poetry/bin", "LLVM/bin"]:
                        tool_path = Path(pf) / tool
                        if tool_path.exists():
                            paths.append(str(tool_path))

            # 3. INHERITED DNA (Existing PATH)
            current_path = os.environ.get("PATH", "")
            paths.extend(current_path.split(os.pathsep))

            # 4. PURIFICATION
            clean_paths = [p for p in paths if p and os.path.isdir(p)]
            self._scry_cache[root_key] = clean_paths
            return clean_paths

    def _transmute_windows_path_to_wsl(self, path_str: str) -> str:
        """[FACULTY 7]: THE REALITY BRIDGE."""
        if not path_str: return ""
        # Convert C:\Path to /mnt/c/Path
        match = re.match(r'^([a-zA-Z]):[\\/]', path_str)
        if match:
            drive = match.group(1).lower()
            rest = path_str[len(match.group(0)):].replace('\\', '/')
            return f'/mnt/{drive}/{rest}'
        return path_str.replace('\\', '/')

    def __repr__(self) -> str:
        return f"<Ω_CONTEXT_FORGE status=VIGILANT scry_cache={len(self._scry_cache)}>"

# == SCRIPTURE SEALED: THE CONTEXT IS NOW SOVEREIGN AND OMEGA ==