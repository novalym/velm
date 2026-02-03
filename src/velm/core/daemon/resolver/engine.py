# Path: core/daemon/resolver/engine.py
# ------------------------------------
# LIF: INFINITY | ROLE: RESOLVER_ORCHESTRATOR | AUTH_CODE: Ω_RESOLVER_ENGINE_V100
from pathlib import Path
from typing import Dict, Optional

from .identity import SystemIdentity
from .executable import BinaryDiviner
from .virtual import VenvScanner
from .dna import EnvironmentForge


class GnosticRuntimeResolver:
    """
    =================================================================================
    == THE GNOSTIC RUNTIME RESOLVER (V-Ω-TOTALITY)                                 ==
    =================================================================================
    The Sovereign Controller of the Resolver Subsystem.
    It orchestrates Identity, Discovery, and Environmental Forging.
    """

    def __init__(self):
        # 1. Divine Identity
        self.identity = SystemIdentity()

        # 2. Locate Source Root (Relative to this file)
        # .../core/daemon/resolver/engine.py -> up 4 levels -> root
        self.source_root = Path(__file__).parent.parent.parent.parent.resolve()

        # 3. Divine Executable
        self.executable_path = BinaryDiviner.divine(
            self.identity.is_frozen,
            self.identity.platform
        )

        # 4. Scan Virtual Environment
        self.venv_root = VenvScanner.scan()

        # 5. Initialize Forge
        self.forge_master = EnvironmentForge(
            self.identity,
            self.executable_path,
            self.venv_root,
            self.source_root
        )

    def forge_environment(self, extra_vars: Dict[str, str] = None) -> Dict[str, str]:
        """
        [THE RITE OF FORGING]
        Returns a complete, optimized environment dictionary for child processes.
        """
        return self.forge_master.forge(extra_vars)

    def get_identity_matrix(self) -> Dict[str, str]:
        """
        [THE RITE OF RECOGNITION]
        Returns system telemetry for the Handshake.
        """
        matrix = self.identity.get_matrix()
        matrix.update({
            "venv_active": str(bool(self.venv_root)),
            "venv_path": self.venv_root.as_posix() if self.venv_root else "",
            "executable": self.executable_path.as_posix()
        })
        return matrix