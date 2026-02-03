# Path: scaffold/artisans/daemon_artisan/conductor.py
# --------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_DAEMON_CONDUCTOR_V1B
# SYSTEM: DAEMON_ARTISAN | ROLE: HOLLOW_ORCHESTRATOR
# =================================================================================
# [ASCENSION LOG]:
# 1. HOLLOW NAMESPACE: Zero top-level imports of sub-managers.
# 2. JIT FACULTY AWAKENING: Sub-managers are materialized as lazy properties.
# 3. NANO-LATENCY DISPATCH: Command routing occurs before the heavy lift.
# 4. DIMENSIONAL DECOUPLING: Separates CLI intent from Server logic.
# 5. ATOMIC REGISTRATION: Injects 'self' into JIT-born artisans.
# 6. CIRCUIT BREAKER ROUTING: Unknown rites are terminated before loading logic.
# =================================================================================

from pathlib import Path
from typing import Optional, Dict, Any, List, Union, TYPE_CHECKING

# --- THE LIGHTWEIGHT ANCHORS (SAFE) ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import DaemonRequest

# [ASCENSION]: We use TYPE_CHECKING to preserve IDE gnosis without the import tax.
if TYPE_CHECKING:
    from .lifecycle import LifecycleManager
    from .telemetry import TelemetryProvider
    from .governance import GovernanceHandler


class DaemonArtisan(BaseArtisan[DaemonRequest]):
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR (V-Ω-HOLLOW-ORCHESTRATOR-ULTIMA)                    ==
    =================================================================================
    LIF: ∞ | HANDLER_BOOT: <1ms

    The High Priest of the Daemon.
    It no longer carries the weight of the Pantheon in its soul. It is a
    pure, ephemeral conduit that summons the specialist artisans from the void
    only at the exact moment of invocation.
    =================================================================================
    """

    def __init__(self, engine):
        super().__init__(engine)
        # Containers for lazy-loaded faculties
        self._lifecycle = None
        self._telemetry = None
        self._governance = None

    # =========================================================================
    # == THE PANTHEON OF LAZY PROPERTIES (JIT MATERIALIZATION)               ==
    # =========================================================================

    @property
    def lifecycle(self) -> 'LifecycleManager':
        """Materializes the Lifecycle Artisan only when start/stop is spoken."""
        if self._lifecycle is None:
            from .lifecycle import LifecycleManager
            self._lifecycle = LifecycleManager(self)
        return self._lifecycle

    @property
    def telemetry(self) -> 'TelemetryProvider':
        """Materializes the Telemetry Artisan only for status/log probes."""
        if self._telemetry is None:
            from .telemetry import TelemetryProvider
            self._telemetry = TelemetryProvider(self)
        return self._telemetry

    @property
    def governance(self) -> 'GovernanceHandler':
        """Materializes the Governance Artisan only for config reloads."""
        if self._governance is None:
            from .governance import GovernanceHandler
            self._governance = GovernanceHandler(self)
        return self._governance

    # =========================================================================
    # == THE GRAND SYMPHONY (ZERO-LATENCY DISPATCH)                          ==
    # =========================================================================

    def execute(self, request: DaemonRequest) -> ScaffoldResult:
        """
        [THE RITE OF GNOSTIC TRIAGE]
        Routes the plea to the appropriate faculty. The 12-second import tax
        is only paid IF the logic is actually needed.
        """
        command = request.command

        # 1. Nano-Triage: Exit early for unknown pleas before loading any logic
        valid_rites = {
            "start", "vigil", "stop", "status",
            "logs", "reload", "rotate_keys"
        }
        if command not in valid_rites:
            return self.failure(f"Unknown daemon rite: '{command}'.")

        # 2. [THE APOTHEOSIS]: Sequential JIT Delegation
        # We access the property only for the specific command path.
        if command == "start":
            return self.lifecycle.start(request, is_vigil=False)

        elif command == "vigil":
            return self.lifecycle.start(request, is_vigil=True)

        elif command == "stop":
            return self.lifecycle.stop(request)

        elif command == "status":
            return self.telemetry.proclaim_status(request)

        elif command == "logs":
            return self.telemetry.stream_logs(request)

        elif command == "reload":
            return self.governance.reload(request)

        elif command == "rotate_keys":
            return self.governance.rotate_keys(request)

        return self.failure(f"Heresy: Triage paradox encountered for '{command}'.")