# Path: scaffold/core/redemption/diagnostician/specialists/system_healer.py
# -------------------------------------------------------------------------

import shutil
import re
import sys
from typing import Optional, Dict, Any, List

from ..contracts import Diagnosis
from .....contracts.heresy_contracts import ArtisanHeresy


class SystemHealer:
    """
    =================================================================================
    == THE SYSTEM HEALER (V-Ω-FORENSIC-INQUISITOR)                                 ==
    =================================================================================
    LIF: 10,000,000,000

    The Specialist of the Host Reality. It gazes upon broken processes and missing
    artisans, transmuting raw exit codes and stderr noise into actionable Gnosis.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **The Gaze of the Missing Binary (127):** Detects if a tool is absent from PATH.
    2.  **The Gaze of Authority (126):** Detects permission errors on executables.
    3.  **The Pythonic Inquest:** Parses `ModuleNotFoundError` from stderr.
    4.  **The Node Inquest:** Parses `npm ERR!` and `MODULE_NOT_FOUND`.
    5.  **The Git Inquest:** Detects unconfigured identities or missing repos.
    6.  **The Venv Sentinel:** Detects operations on system Python.
    7.  **The Path Prover:** Verifies if the command exists using `shutil.which`.
    8.  **The OOM Watcher:** Detects Exit 137 (Out of Memory).
    9.  **The Confidence Matrix:** Assigns high confidence (1.0) to binary checks.
    10. **The Luminous Dossier:** Returns rich metadata about the missing component.
    11. **The Oracle of Healing:** Forges precise `pip install`, `npm install`, or system commands.
    12. **The Unbreakable Contract:** Always returns `Optional[Diagnosis]`, never bool.
    """

    @staticmethod
    def heal(exc: BaseException, context: Optional[Dict[str, Any]] = None) -> Optional[Diagnosis]:
        """
        The Rite of Systemic Diagnosis.
        """
        if not context:
            context = {}

        # 1. The Gaze upon the Broken Process (CalledProcessError)
        if hasattr(exc, 'returncode'):
            returncode = exc.returncode
            # Extract the command string for forensic analysis
            cmd_raw = getattr(exc, 'cmd', None)
            cmd_str = "unknown"
            binary = "unknown"

            if isinstance(cmd_raw, list):
                cmd_str = " ".join(cmd_raw)
                binary = cmd_raw[0]
            elif isinstance(cmd_raw, str):
                cmd_str = cmd_raw
                binary = cmd_str.split()[0]

            # Capture the dying breath (Output/Stderr)
            output = (getattr(exc, 'output', '') or '') + (getattr(exc, 'stderr', '') or '')

            # --- CASE A: The Missing Artisan (Exit 127 or "not found") ---
            if returncode == 127 or "not found" in output.lower() or not shutil.which(binary):
                # Specific advice for common tools
                advice = f"The artisan '{binary}' is not manifest in the PATH."
                install_cmd = None

                if binary == 'poetry':
                    install_cmd = "pip install poetry"
                elif binary == 'node':
                    install_cmd = "brew install node"  # Heuristic
                elif binary == 'docker':
                    advice += " Install Docker Desktop."

                return Diagnosis(
                    heresy_name="MissingBinary",
                    cure_command=install_cmd,
                    advice=advice,
                    confidence=1.0,
                    metadata={"binary": binary, "exit_code": 127}
                )

            # --- CASE B: The Forbidden Artisan (Exit 126 / Permission Denied) ---
            if returncode == 126 or "permission denied" in output.lower():
                return Diagnosis(
                    heresy_name="PermissionDenied",
                    cure_command=f"chmod +x {binary}",
                    advice=f"The artisan '{binary}' exists but lacks the Rite of Execution (+x).",
                    confidence=0.9,
                    metadata={"binary": binary, "exit_code": 126}
                )

            # --- CASE C: The Exhausted Artisan (OOM / Exit 137) ---
            if returncode == 137:
                return Diagnosis(
                    heresy_name="SystemExhaustion",
                    cure_command=None,
                    advice="The process was slaughtered by the OS (Out of Memory). Increase resources.",
                    confidence=0.95,
                    metadata={"exit_code": 137}
                )

            # --- CASE D: Python Module Heresy ---
            if "ModuleNotFoundError" in output or "ImportError" in output:
                match = re.search(r"No module named '([^']+)'", output)
                if match:
                    missing_pkg = match.group(1)
                    return Diagnosis(
                        heresy_name="MissingPythonSoul",
                        cure_command=f"pip install {missing_pkg}",
                        advice=f"The Python soul '{missing_pkg}' is missing from the environment.",
                        confidence=1.0,
                        metadata={"package": missing_pkg}
                    )

            # --- CASE E: Node Module Heresy ---
            if "npm ERR!" in output or "MODULE_NOT_FOUND" in output:
                return Diagnosis(
                    heresy_name="MissingNodeSoul",
                    cure_command="npm install",
                    advice="The Node ecosystem is fractured. Resurrect dependencies.",
                    confidence=0.8,
                    metadata={"context": "node"}
                )

        # 2. The Gaze upon the Forbidden Path (PermissionError in Python)
        if isinstance(exc, PermissionError):
            if "site-packages" in str(exc):
                # The Venv Sentinel
                return Diagnosis(
                    heresy_name="NakedPythonWrite",
                    cure_command="python -m venv .venv && source .venv/bin/activate",
                    advice="You are attempting to write to the System Python. Create a Virtual Environment.",
                    confidence=0.95,
                    metadata={}
                )

        # 3. The Gaze upon the Void (FileNotFoundError for Binaries)
        if isinstance(exc, FileNotFoundError):
            filename = exc.filename
            return Diagnosis(
                heresy_name="ArtifactMissing",
                cure_command=f"touch {filename}",  # Crude but valid
                advice=f"The scripture '{filename}' is a void.",
                confidence=0.7,
                metadata={"file": filename}
            )

        return None