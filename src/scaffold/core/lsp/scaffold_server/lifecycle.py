# Path: core/lsp/scaffold_server/lifecycle.py
# -------------------------------------------
# LIF: INFINITY | ROLE: REALITY_CONSECRATOR | RANK: SOVEREIGN
# auth_code: Ω_LIFECYCLE_TOTALITY_V306_UNSTOPPABLE

import os
import gc
import sys
import uuid
import time
import re
import threading
import traceback
from pathlib import Path
from typing import Any, Dict, Optional

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, ServerState
from ..base.utils.uri import UriUtils
from ..base.types import (
    InitializeParams,
    InitializeResult,
    ServerCapabilities,
    ServerInfo,
    MessageType,
    TextDocumentSyncKind
)

# [ASCENSION 7]: TOKEN PURIFIER
TOKEN_CLEANSE_RE = re.compile(r'[\s\x00-\x1f\x7f-\xff]')


class OracleLifecycle:
    """
    =============================================================================
    == THE ORACLE LIFECYCLE (V-Ω-TOTALITY-V306-UNSTOPPABLE)                    ==
    =============================================================================
    The High Priest of Inception. Responsible for the materialization of the
    Oracle, the negotiation of immutable laws, and the confirmation of Life.
    =============================================================================
    """

    def __init__(self, server: Any):
        self.server = server
        self.logger = server.logger
        self._boot_time_ns = time.perf_counter_ns()
        self._initialized_flag = False

    # =========================================================================
    # == RITE 1: THE MATERIALIZATION (REQUEST)                               ==
    # =========================================================================

    def initialize(self, params: Any) -> Dict[str, Any]:
        """
        Negotiates the laws of reality with the Ocular UI.
        """
        # [ASCENSION 1]: THERMAL RE-ENTRY GUARD
        with self.server._state_lock:
            if self.server.state != ServerState.DORMANT:
                self.logger.warn("Initialization Plea ignored: Essence already manifest.")
                return self._generate_consecrated_response()

            self.server.state = ServerState.AWAKENING

        # [ASCENSION 2]: AURA TRACE GENESIS
        trace_id = f"init-{uuid.uuid4().hex[:8].upper()}"
        forensic_log(f"Oracle Awakening Initiated. Trace: {trace_id}", "RITE", "LIFE", trace_id=trace_id)

        try:
            # 1. PARSE HANDSHAKE DNA
            # Transmute raw JSON-RPC dict into a validated Pydantic model
            # [ASCENSION 3]: MODEL SOVEREIGNTY
            p = InitializeParams.model_validate(params) if isinstance(params, dict) else params

            # 2. [ASCENSION 4]: ISOMORPHIC ANCHOR PURIFICATION
            root_uri = getattr(p, 'root_uri', None) or getattr(p, 'rootUri', None)
            opts = getattr(p, 'initialization_options', {}) or getattr(p, 'initializationOptions', {}) or {}

            # Triage: Prefer rootUri, fallback to projectRoot from options, final fallback CWD
            uri_to_resolve = root_uri.root if hasattr(root_uri, 'root') else (root_uri or opts.get('projectRoot'))

            if uri_to_resolve:
                # [THE CURE]: ABSOLUTE PATH RESOLUTION
                self.server.project_root = UriUtils.to_fs_path(uri_to_resolve)

                # [ASCENSION 6]: ENVIRONMENTAL GRAFTING
                os.environ["SCAFFOLD_PROJECT_ROOT"] = str(self.server.project_root)
                if self.server.engine:
                    self.server.engine.project_root = str(self.server.project_root)

                forensic_log(f"Reality Anchored to Sanctum: {self.server.project_root}", "SUCCESS", "LIFE",
                             trace_id=trace_id)
            else:
                self.server.project_root = Path.cwd().resolve()
                self.logger.warn("Handshake missing Root URI. Defaulting anchor to CWD.")

            # 3. [ASCENSION 5]: SILVER CORD PRE-WARMING
            if isinstance(opts, dict):
                self.server._daemon_port = int(opts.get('daemonPort', 5555))

                # [ASCENSION 7]: AGGRESSIVE TOKEN EXORCISM
                raw_token = str(opts.get('token', 'VOID'))
                clean_token = TOKEN_CLEANSE_RE.sub('', raw_token)
                self.server._daemon_token = clean_token

                if self.server._daemon_token != 'VOID' and self.server._daemon_token != '':
                    # [ASCENSION 8]: LAZY SKILL AWAKENING
                    # Fire-and-forget relay ignition
                    threading.Thread(
                        target=self.server.relay.ignite,
                        args=(self.server._daemon_port, self.server._daemon_token),
                        name="RelayIgniter",
                        daemon=True
                    ).start()
                else:
                    forensic_log("No Daemon token found. Operating in Standalone (Local) Mode.", "INFO", "LIFE",
                                 trace_id=trace_id)

            # 4. STORE CLIENT SOUL
            self.server.client_capabilities = getattr(p, 'capabilities', None)

            # [ASCENSION 9]: FORENSIC PID INSCRIPTION
            if self.server.project_root and self.server.project_root.exists():
                # [THE GUARD]: Don't pollute the App Root if something went wrong
                if self.server.project_root == Path.cwd():
                    # Unless the project is ACTUALLY the app root (rare)
                    pass

                try:
                    debug_dir = self.server.project_root / ".scaffold" / "debug"
                    # [SAFETY]: Only create if parent exists to avoid deep nesting of errors
                    if not debug_dir.exists():
                        debug_dir.mkdir(parents=True, exist_ok=True)

                    (debug_dir / "lsp.pid").write_text(str(os.getpid()))
                except Exception as e:
                    self.logger.warn(f"PID Inscription failed: {e}")

            # 5. [ASCENSION 10]: METABOLIC PURGE
            gc.collect()

            # 6. [ASCENSION 11]: CONSTITUTIONAL PROCLAMATION
            return self._generate_consecrated_response()

        except Exception as e:
            # [ASCENSION 12]: CATASTROPHIC AUTOPSY
            self.logger.critical(f"Inception Fracture: {str(e)}")
            forensic_log("Catastrophic Inception failure.", "CRIT", "LIFE", exc=e, trace_id=trace_id)
            return self._generate_fallback_response()

    # =========================================================================
    # == RITE 2: THE ACTIVATION (NOTIFICATION)                               ==
    # =========================================================================

    def initialized(self, params: Any = None):
        """
        [THE MISSING LINK: RESTORED]
        Confirming the connection and opening the eyes of the Oracle.
        """
        with self.server._state_lock:
            if self._initialized_flag: return
            self.server.state = ServerState.ACTIVE
            self._initialized_flag = True

        # [ASCENSION 3]: CHRONOMETRY
        total_boot_ms = (time.perf_counter_ns() - self._boot_time_ns) / 1_000_000

        # [ASCENSION 9]: VITALITY BROADCAST
        self.server.endpoint.send_notification("gnostic/vitality", {
            "status": "ONLINE",
            "mode": "FULL_DUPLEX" if self.server._relay_active else "STANDALONE",
            "boot_ms": round(total_boot_ms, 2),
            "timestamp": time.time(),
            "session_id": self.server._session_id
        })

        # [ASCENSION 10]: INCEPTION SWEEP
        # Now that we are initialized, force the Inquisitor to gaze at all open files.
        #if self.server.project_root:
            #self.server.inquest.inception_sweep()

        forensic_log(f"Singularity active in {total_boot_ms:.2f}ms. Initiating Inception Sweep.", "SUCCESS", "LIFE")

    # =========================================================================
    # == INTERNAL GNOSIS                                                     ==
    # =========================================================================

    def _generate_consecrated_response(self) -> Dict[str, Any]:
        """Forges the high-fidelity constitutional response."""
        caps = self.server.get_capabilities()
        result = InitializeResult(
            capabilities=caps,
            serverInfo=ServerInfo(
                name="Scaffold Gnostic Oracle",
                version="3.2.0-SINGULARITY"
            )
        )
        return result.model_dump(mode='json', by_alias=True, exclude_none=True)

    def _generate_fallback_response(self) -> Dict[str, Any]:
        """Provides a safe-mode manifest when reality collapses."""
        return {
            "capabilities": {
                "textDocumentSync": 1,
                "hoverProvider": False,
                "completionProvider": {"triggerCharacters": ["$"]}
            },
            "serverInfo": {
                "name": "Scaffold Oracle [RECOVERY_MODE]",
                "version": "3.2.0-FRACTURED"
            }
        }

# === SCRIPTURE SEALED: THE LIFECYCLE IS COMPLETE ===