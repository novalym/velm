# Path: scaffold/core/ignition/diviner/sentinel/vitality.py
# ---------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: SENTINEL_VITALITY_V1

import os
import subprocess
import re
from pathlib import Path
from typing import Tuple, Optional
from ....logger import Scribe

Logger = Scribe("VitalityProbe")


class VitalityProbe:
    """
    =============================================================================
    == THE VITALITY PROBE (V-Ω-THE-PULSE)                                      ==
    =============================================================================
    [ASCENSION 5]: isolated, timeout-guarded execution for health checks.
    """

    @classmethod
    def check_health(cls, path: Path, custom_args: Optional[list] = None) -> Tuple[bool, str]:
        """
        Executes the binary to ensure it breathes. Returns (is_healthy, version_str).
        """
        if not os.access(path, os.X_OK):
            # [ASCENSION 4]: PERMISSION SUTURE
            if os.name != 'nt':
                try:
                    os.chmod(path, 0o755)
                    Logger.info(f"Sutured permissions for: [cyan]{path.name}[/cyan]")
                except:
                    pass

            if not os.access(path, os.X_OK):
                return False, "E_NO_EXEC_PERMISSION"

        # [ASCENSION 3]: VERSION SCRAPER
        cmd = custom_args if custom_args else [str(path), "--version"]

        try:
            # [ASCENSION 5]: THE WARDEN (Isolated Timeout)
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1.5,  # Aggressive timeout
                check=False
            )

            output = (proc.stdout + proc.stderr).strip()

            if proc.returncode != 0 and not output:
                return False, f"E_EXIT_CODE_{proc.returncode}"

            # Extract version signature
            version = cls._extract_version(output)
            return True, version

        except subprocess.TimeoutExpired:
            return False, "E_TIMEOUT"
        except Exception as e:
            return False, f"E_FRACTURE_{str(e)}"

    @staticmethod
    def _extract_version(text: str) -> str:
        """[ASCENSION 3]: Regex-based version scraping."""
        match = re.search(r'(\d+\.\d+\.\d+)', text)
        return match.group(1) if match else "v?.?.?"

