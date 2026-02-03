# Path: core/lsp/base/governor.py
# ------------------------------
import sys
import time
import logging
from typing import Any, Dict, List, Optional, Union
from .state import ServerState
from .telemetry import forensic_log
from .types import (
    InitializeParams, InitializeResult, ServerCapabilities,
    ServerInfo, TextDocumentSyncKind
)


class LifecycleGovernor:
    """
    =============================================================================
    == THE LIFECYCLE GOVERNOR (V-Ω-TEMPORAL-ANCHOR)                            ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: REALITY_NEGOTIATOR | RANK: SOVEREIGN

    Orchestrates the birth, constitutional negotiation, and dissolution of the
    Language Server process.
    """

    def __init__(self, server: Any):
        self.server = server
        self._is_draining = False

    def initialize(self, params: Dict[str, Any]) -> InitializeResult:
        """[RITE]: MATERIALIZATION - Negotiates the laws of communion."""
        with self.server._state_lock:
            if self.server.state != ServerState.DORMANT:
                forensic_log("Initialization ignored: Oracle already manifest.", "WARN", "GOVERNOR")
                return self._forge_result()

            self.server.state = ServerState.AWAKENING

            # 1. PARSE INGRESS PARAMS
            p = InitializeParams.model_validate(params)

            # 2. ANCHOR ROOTS
            if p.root_uri:
                from .utils.uri import UriUtils
                self.server.project_root = UriUtils.to_fs_path(p.root_uri)

            # 3. MAP WORKSPACE
            if p.workspace_folders:
                self.server.documents.initialize_workspace(p.workspace_folders)

            # 4. STORE CLIENT SOUL
            self.server.client_capabilities = p.capabilities
            if p.client_info:
                forensic_log(f"Linked to {p.client_info.name} v{p.client_info.version}", "INFO", "GOVERNOR")

            # 5. DIVINE CAPABILITIES
            return self._forge_result()

    def initialized(self):
        """[RITE]: ACTIVATION - The mind becomes hot."""
        with self.server._state_lock:
            self.server.state = ServerState.ACTIVE

        forensic_log("Neural Lattice Synchronized. Mind is ACTIVE.", "SUCCESS", "GOVERNOR")

        # Proclaim vitality to the Ocular UI
        self.server.endpoint.send_notification("gnostic/vitality", {
            "status": "ONLINE",
            "timestamp": time.time()
        })

    def shutdown(self):
        """[RITE]: DRAINING - Prepares for oblivion."""
        with self.server._state_lock:
            if self._is_draining: return
            self._is_draining = True
            self.server.state = ServerState.DRAINING

            forensic_log("Shutdown willed. Draining Kinetic Foundry...", "RITE", "GOVERNOR")

            # Cancel all background causality
            self.server.foundry.shutdown(wait=True)

        return None

    def exit(self):
        """[RITE]: OBLIVION - Final process dissolution."""
        self.server.state = ServerState.VOID
        # Protocol Law: 0 if willed shutdown, else 1
        sys.exit(0 if self._is_draining else 1)

    def _forge_result(self) -> InitializeResult:
        """Synthesizes the Constitutional Proclamation."""
        return InitializeResult(
            capabilities=self.server.get_capabilities(),
            serverInfo=ServerInfo(
                name="Gnostic Base Framework",
                version="1.0.0-OMEGA"
            )
        )