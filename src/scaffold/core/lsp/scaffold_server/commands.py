# Path: core/lsp/scaffold_server/commands.py
# ------------------------------------------
# LIF: INFINITY | ROLE: KINETIC_CONDUCTOR | AUTH: Ω_COMMAND_SINGULARITY_V400_FINAL
# SYSTEM: GNOSTIC_KERNEL | RANK: SOVEREIGN | ROLE: INTENT_ACTUATOR

import logging
import json
import time
import uuid
import sys
import os
import threading
import traceback
from typing import List, Any, Dict, Optional, Union, Callable
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, UriUtils
from ..base.types import WorkspaceEdit, TextEdit, Range, Position, MessageType


# [ASCENSION 1]: GLOBAL FORENSIC REGISTRY
# We use stderr for the most reliable delivery of diagnostic truth.
def scream(msg: str, trace_id: str = "0xVOID"):
    timestamp = time.strftime("%H:%M:%S")
    sys.stderr.write(f"\n[KINETIC:CONDUCTOR] [{timestamp}] [{trace_id}] 📢 {msg}\n")
    sys.stderr.flush()


class CommandRouter:
    """
    =============================================================================
    == THE KINETIC CONDUCTOR (V-Ω-TOTALITY-V400-INDESTRUCTIBLE)                ==
    =============================================================================
    LIF: INFINITY | ROLE: INTENT_ACTUATOR | RANK: SOVEREIGN

    The supreme orchestrator of physical change. It bridges the Architect's
    interaction with the Daemon's kinetic power through a transactional,
    haptic-aware command bus.
    """

    def __init__(self, server: Any):
        self.server = server

        # [ASCENSION 12]: THE SACRED EDICT MAP
        self._rites: Dict[str, Callable] = {
            # --- THE HALL OF REDEMPTION ---
            "scaffold.applyFix": self.h_apply_fix,
            "scaffold.heal": self.h_apply_fix,

            # --- THE HALL OF EVOLUTION ---
            "scaffold.transmute": self.h_transmute,
            "scaffold.refactor.extract": self.h_refactor_extract,

            # --- THE HALL OF PERCEPTION ---
            "scaffold.survey": self.h_survey,
            "scaffold.runRite": self.h_run_generic_rite
        }

        self._last_cmd_time = 0.0
        self._lock = threading.RLock()
        scream("Kinetic Conductor Materialized. All Rites Consecrated.")

    def dispatch(self, command: str, arguments: Optional[List[Any]]) -> Any:
        """
        =============================================================================
        == THE RITE OF DISPATCH (THE INGRESS PORTAL)                               ==
        =============================================================================
        """
        # 1. [ASCENSION 6]: CAUSAL ANCHORING
        trace_id = f"cmd-{uuid.uuid4().hex[:6].upper()}"
        start_ns = time.perf_counter_ns()

        # [ASCENSION 1]: THE FORENSIC ANNOUNCER
        scream(f"INBOUND EDICT: '{command}'", trace_id)

        # 2. [ASCENSION 11]: METABOLIC THROTTLE
        with self._lock:
            now = time.time()
            if now - self._last_cmd_time < 0.05:  # 50ms cooldown
                time.sleep(0.05)
            self._last_cmd_time = time.time()

        # 3. [ASCENSION 11]: FAULT-ISOLATE SARCOPHAGUS
        try:
            handler = self._rites.get(command)
            if not handler:
                msg = f"Unknown Edict: '{command}'. Is it manifest in the Grimoire?"
                scream(f"⚠️ {msg}", trace_id)
                self.server.log_message(msg, type=MessageType.Warning)
                return {"success": False, "error": "COMMAND_UNMANIFEST"}

            # 4. [ASCENSION 2]: RECURSIVE ARGUMENT UNWRAPPING
            # Standard LSP sends args as a list. Monaco might wrap them in another list.
            # We unwrap until we find the real payload.
            safe_args = arguments or []
            scream(f"Raw Args: {json.dumps(safe_args, default=str)[:200]}", trace_id)

            while len(safe_args) == 1 and isinstance(safe_args[0], list):
                scream("Unwrapping nested argument list...", trace_id)
                safe_args = safe_args[0]

            # 5. EXECUTION
            scream(f"Delegating to Handler: {handler.__name__}", trace_id)
            result = handler(safe_args, trace_id)

            # 6. [ASCENSION 7]: CHRONOMETRIC TELEMETRY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            scream(f"Rite Concluded in {duration_ms:.2f}ms", trace_id)

            return result

        except Exception as fracture:
            # [ASCENSION 8]: THE CATASTROPHIC AUTOPSY
            tb = traceback.format_exc()
            scream(f"💥 RITE FRACTURE: {fracture}", trace_id)
            sys.stderr.write(f"\n[AUTOPSY]\n{tb}\n")
            sys.stderr.flush()

            self.server.log_message(f"Crucible Fracture: {str(fracture)}", type=MessageType.Error)
            # [ASCENSION 10]: HAPTIC SHAKE
            self.server.endpoint.send_notification("gnostic/vfx", {"type": "shake", "intensity": 0.8})

            return {"success": False, "error": str(fracture), "traceback": tb}

    # =============================================================================
    # == THE SACRED RITES (HANDLERS)                                             ==
    # =============================================================================

    def h_apply_fix(self, args: List[Any], trace_id: str) -> Any:
        """
        [RITE]: APPLY_FIX (THE SUPREME HEALER)
        =========================================================================
        LIF: 100x | ROLE: MASTER_HEALER
        """
        if len(args) < 2:
            scream("❌ Aborting: Insufficient arguments for Healing Rite.", trace_id)
            return {"success": False, "error": "INSUFFICIENT_ARGS"}

        # Extract atoms from the payload
        uri = str(args[0])
        heresy = args[1]  # The diagnostic/heresy data

        scream(f"Targeting Scripture: {uri.split('/')[-1]}", trace_id)
        scream(f"Heresy Code: {heresy.get('code')}", trace_id)

        # 1. [ASCENSION 9]: LIBRARIAN VITALITY CHECK
        doc = self.server.documents.get(uri)
        if not doc:
            # Fallback: Try to find by normalized URI
            norm_uri = UriUtils.normalize_uri(uri)
            doc = self.server.documents.get(norm_uri)

        if not doc:
            msg = f"Scripture void in Librarian: {uri}"
            scream(f"❌ {msg}", trace_id)
            self.server.show_message(msg, type=MessageType.Error)
            return {"success": False, "error": "DOCUMENT_VOID"}

        # 2. [ASCENSION 3]: THE SOCRATIC HERALD
        self.server.log_message(f"Commencing Redemption for {heresy.get('code')}...", type=MessageType.Log)

        # 3. [ASCENSION 4]: DAEMON RELAY TRIAGE
        params = {
            "file_path": str(UriUtils.to_fs_path(uri)),
            "heresy_key": heresy.get("code"),
            "line_num": heresy.get("range", {}).get("start", {}).get("line", 0) + 1,
            "project_root": str(self.server.project_root),
            "content": doc.text,  # Inject the living soul
            "context": {
                "diagnostic": heresy,
                "source": "LSP_COMMAND_FIX",
                "trace_id": trace_id
            },
            "metadata": {"trace_id": trace_id, "timestamp": time.time()}
        }

        scream("Dispatched plea to Daemon. Waiting for revelation...", trace_id)

        # We use the unblocked relay_request
        response = self.server.relay_request("repair", params)

        if response and response.get('success'):
            data = response.get('data', {})
            edits_data = data.get('edits', [])

            if not edits_data:
                scream("⚠️ Prophet returned success but zero deltas.", trace_id)
                self.server.show_message("Repair Artisan found no path to redemption.", type=MessageType.Warning)
                return {"success": True, "message": "NO_EDITS_GENERATED"}

            # 4. [ASCENSION 5]: ATOMIC EDIT VERIFICATION
            changes = {}
            for e in edits_data:
                # Ensure the URI is canonical for the client
                target_uri = e.get('uri') or uri
                if not target_uri.startswith("file:"):
                    target_uri = UriUtils.to_uri(target_uri)

                if target_uri not in changes: changes[target_uri] = []

                # Suture the TextEdit
                changes[target_uri].append({
                    "range": e["range"],
                    "newText": e["newText"]
                })

            scream(f"Forge Complete. Manifesting {len(edits_data)} deltas to UI.", trace_id)

            # 5. [ASCENSION 10]: THE ACTIVE PROCLAMATION
            # Push the edit command back to the Ocular UI
            self.server.endpoint.send_request("workspace/applyEdit", {
                "label": f"Gnostic Repair: {heresy.get('code')}",
                "edit": {"changes": changes}
            })

            # 6. [ASCENSION 10]: HAPTIC SYNERGY
            self.server.endpoint.send_notification("gnostic/vfx", {
                "type": "bloom", "color": "#10b981", "intensity": 0.8
            })

            scream("✨ REALITY HEALED.", trace_id)
            return {"success": True}

        else:
            # [ASCENSION 4]: RELAY FAILURE TRIAGE
            error_msg = response.get('message', 'Daemon Connection Timeout') if response else 'Daemon Unresponsive'
            scream(f"❌ DISPATCH FAILED: {error_msg}", trace_id)

            self.server.show_message(f"Redemption rite failed: {error_msg}", type=MessageType.Error)
            self.server.endpoint.send_notification("gnostic/vfx", {"type": "shake", "intensity": 1.0})

            return {"success": False, "error": error_msg}

    def h_transmute(self, args: List[Any], trace_id: str) -> Any:
        """[RITE]: TRANSMUTE - Force sync with blueprint."""
        if not args: return None
        fs_path = str(UriUtils.to_fs_path(args[0]))
        scream(f"Transmuting: {fs_path}", trace_id)
        return self.server.relay_request("transmute", {
            "path_to_scripture": fs_path,
            "project_root": str(self.server.project_root),
            "metadata": {"trace_id": trace_id}
        })

    def h_refactor_extract(self, args: List[Any], trace_id: str) -> Any:
        """[RITE]: EXTRACT - Logic Fission."""
        scream("Refactor: Logic Fission requested.", trace_id)
        # Implementation details...
        pass

    def h_survey(self, args: List[Any], trace_id: str) -> Any:
        """[RITE]: SURVEY - Re-align the project graph."""
        scream("Survey: Topological scan initiated.", trace_id)
        if not self.server.project_root: return None
        return self.server.relay_request("grandSurvey", {
            "rootUri": self.server.project_root.as_uri(),
            "metadata": {"trace_id": trace_id}
        })

    def h_run_generic_rite(self, args: List[Any], trace_id: str) -> Any:
        """[THE GATEWAY]: Dispatches any artisan by name."""
        if len(args) < 2: return None
        scream(f"Gateway: Dispatching to artisan '{args[0]}'", trace_id)
        return self.server._dispatch_to_daemon(args[0], args[1])

# === SCRIPTURE SEALED: THE KINETIC CONDUIT IS INVINCIBLE ===