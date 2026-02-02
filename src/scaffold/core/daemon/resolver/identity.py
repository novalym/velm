# Path: core/daemon/resolver/identity.py
# --------------------------------------
# LIF: INFINITY | ROLE: SYSTEM_FINGERPRINT
import sys
import platform
import os
from typing import Dict


class SystemIdentity:
    """
    [THE FINGERPRINT]
    Captures the static truth of the Host Machine.
    """

    def __init__(self):
        # 1. OS & Arch
        self.platform = sys.platform
        self.arch = platform.machine()
        self.node = platform.node()
        self.release = platform.release()

        # 2. Python Reality
        self.python_version = platform.python_version()
        self.implementation = platform.python_implementation()

        # 3. Execution Mode (Frozen vs Source)
        # _MEIPASS is the hallmark of PyInstaller
        self.is_frozen = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
        self.meipass = getattr(sys, '_MEIPASS', None)

        # 4. Debug State
        # Detects explicit env var OR Python optimization flag (-O)
        self.is_debug = bool(os.environ.get('GNOSTIC_DEBUG', False) or __debug__)

    def get_matrix(self) -> Dict[str, str]:
        """Returns the Identity Matrix for Telemetry."""
        return {
            "platform": self.platform,
            "arch": self.arch,
            "node": self.node,
            "os_release": self.release,
            "python_version": self.python_version,
            "python_impl": self.implementation,
            "execution_mode": "FROZEN" if self.is_frozen else "SOURCE",
            "debug_mode": str(self.is_debug),
            "pid": str(os.getpid())
        }