# Path: core/daemon/akashic/envelope.py
# -------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ENVELOPE_SINGULARITY_V12_FIXED
# SYSTEM: GNOSTIC_AKASHIC | ROLE: PROTOCOL_TRANSMUTER
# =================================================================================

import time
import os
import uuid
import hashlib
import json
import re
from typing import Dict, Any, Optional

from .constants import TAG_HERESY, TAG_KINETIC, TAG_INTERNAL

# [ASCENSION 2]: ANSI PURIFICATION ENGINE
# Pre-compiled regex for stripping terminal escape codes.
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class EnvelopeForge:
    """
    =============================================================================
    == THE ENVELOPE FORGE (V-Ω-PROTOCOL-TRANSMUTER-ULTIMA)                     ==
    =============================================================================
    LIF: INFINITY | ROLE: PACKET_ARCHITECT

    Transmutes raw thought-forms (Dictionaries) into formal JSON-RPC Notifications.
    It acts as the Gatekeeper of Protocol, deciding whether a message is a
    Log, a Signal, or a Structural Update.
    """

    # [ASCENSION 1]: THE PASSTHROUGH GATE (WHITELIST)
    # These methods are structural signals. They must NOT be wrapped in 'window/logMessage'.
    # They are sent raw to trigger logic in the Client (LSP/Cockpit).
    PASSTHROUGH_METHODS = {
        'textDocument/publishDiagnostics',  # The Inquisitor's findings
        'scaffold/jobComplete',  # The Kinetic Result
        'scaffold/progress',  # The Progress Pulse
        'scaffold/previewStructure',  # The Tree View Update
        'scaffold/neuralLink',  # The AI Stream
        '$/heartbeat',  # The Vitality Check
        'gnostic/config',  # The Late-Binding Credential Update
        'window/showMessage',  # Standard LSP Toast
        'window/workDoneProgress/create',  # LSP Progress
        '$/progress'  # LSP Progress
    }

    @staticmethod
    def wrap(packet: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Wraps a log entry or data packet in the sacred JSON-RPC vestments.
        """
        # [ASCENSION 9]: THE VOID WARD
        if not packet:
            return None

        current_time = time.time()

        # [ASCENSION 4]: TRACE INJECTION
        # Attempt to inherit the trace_id from the kinetic environment
        trace_id = packet.get("trace_id") or os.environ.get("GNOSTIC_REQUEST_ID") or f"tr-{uuid.uuid4().hex[:8]}"

        # Determine Method
        raw_method = packet.get("method")

        # =========================================================================
        # == PATH A: THE PASSTHROUGH (STRUCTURAL SIGNALS)                        ==
        # =========================================================================
        # If the packet is already formatted as JSON-RPC, or matches the whitelist.

        is_preformatted = "jsonrpc" in packet
        is_whitelisted = raw_method in EnvelopeForge.PASSTHROUGH_METHODS

        if is_preformatted or is_whitelisted:
            # [ASCENSION 7]: METADATA GRAFTING
            # Even raw packets get the Gnostic Metadata for debugging.
            meta = packet.get("_meta", {})
            if not meta:
                meta = {"timestamp": current_time, "trace_id": trace_id}

            if is_preformatted:
                # Inject meta if missing
                if "_meta" not in packet:
                    packet["_meta"] = meta
                return packet

            # Construct Raw Notification
            return {
                "jsonrpc": "2.0",
                "method": raw_method,
                "params": packet.get("params", {}),
                "_meta": meta
            }

        # =========================================================================
        # == PATH B: DIAGNOSTIC ELEVATION (IMPLICIT DETECTION)                   ==
        # =========================================================================
        # If we see a packet that *looks* like a diagnostic payload but lacks a method.
        if "diagnostics" in packet and "uri" in packet:
            return {
                "jsonrpc": "2.0",
                "method": "textDocument/publishDiagnostics",
                "params": {
                    "uri": packet["uri"],
                    "diagnostics": packet["diagnostics"]
                },
                "_meta": {"timestamp": current_time, "trace_id": trace_id}
            }

        # =========================================================================
        # == PATH C: THE LOG WRAPPER (DEFAULT)                                   ==
        # =========================================================================
        # Everything else is treated as a Log Message and wrapped.

        # [ASCENSION 8]: SEMANTIC ROUTING
        tags = packet.get("tags", [])
        level = packet.get("level", "INFO").upper()

        if "NEURAL_LINK" in tags:
            method = "scaffold/neuralLink"
        elif TAG_HERESY in tags or level in ["CRITICAL", "FATAL"]:
            method = "scaffold/heresy"
        elif "PROGRESS" in tags:
            method = "scaffold/progress"
        elif TAG_KINETIC in tags:
            method = "scaffold/kinetic"
        else:
            # Default: Standard LSP Log Message
            method = "window/logMessage"

        # [ASCENSION 6]: SEVERITY ALIGNMENT
        # Map string levels to LSP Integers (1=Error, 2=Warn, 3=Info, 4=Log)
        if level in ["CRITICAL", "ERROR", "FATAL"]:
            ui_type = 1
        elif level in ["WARNING", "WARN"]:
            ui_type = 2
        elif level in ["INFO", "SYSTEM", "SUCCESS"]:
            ui_type = 3
        else:
            ui_type = 4  # Debug / Kinetic / Trace

        # [ASCENSION 12]: TYPE SAFETY CASTING
        message_text = str(packet.get("message", ""))

        # [ASCENSION 2]: ANSI PURIFICATION
        # Only strip ANSI for standard log messages meant for the UI console.
        # Custom methods might want rich text.
        if method == "window/logMessage":
            message_text = ANSI_ESCAPE.sub('', message_text)

        # Forge Params based on Method
        if method == "window/logMessage":
            module = packet.get("module", "KERNEL")
            params = {
                "type": ui_type,
                "message": f"[{module}] {message_text}"
            }
        else:
            # Custom Gnostic Params (Rich Structure)
            params = {
                "type": ui_type,
                "message": message_text,
                "level": level,
                "module": packet.get("module", "KERNEL"),
                "timestamp": packet.get("timestamp", current_time),
                "data": packet.get("data"),
                "trace_id": trace_id,
                "tags": tags
            }

        # [ASCENSION 3]: ENTROPY FINGERPRINTING
        # Generate a hash for deduplication in the UI (The "Echo Filter")
        try:
            content_str = json.dumps(params, default=str)
            fingerprint = hashlib.md5(content_str.encode()).hexdigest()
            params["_hash"] = fingerprint
        except:
            pass

        # [ASCENSION 10]: RPC COMPLIANCE ENFORCER
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }