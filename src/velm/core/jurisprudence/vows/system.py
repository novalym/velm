import shutil
import sys
import platform
import os
from typing import Tuple
from .base import BaseVowHandler


class SystemVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF THE MACHINE (ENVIRONMENT)                                 ==
    =============================================================================
    Judges the Host environment, Tools, and Variables.
    """

    def _vow_command_available(self, command: str) -> Tuple[bool, str]:
        return shutil.which(command) is not None, f"Artisan '{command}' is manifest."

    def _vow_on_platform(self, target_os: str) -> Tuple[bool, str]:
        current = platform.system().lower()
        return current == target_os.lower(), f"Platform is {current}."

    def _vow_env_var_set(self, var_name: str) -> Tuple[bool, str]:
        return var_name in os.environ, f"Env '{var_name}' is present."

    def _vow_env_var_equals(self, var_name: str, value: str) -> Tuple[bool, str]:
        actual = os.environ.get(var_name)
        return actual == value, f"Env '{var_name}' is '{actual}'."

    def _vow_python_version_min(self, version: str) -> Tuple[bool, str]:
        try:
            target = tuple(map(int, version.split('.')))
            current = sys.version_info[:2]
            return current >= target, f"Python is {current[0]}.{current[1]}."
        except ValueError:
            return False, f"Invalid version format: {version}"