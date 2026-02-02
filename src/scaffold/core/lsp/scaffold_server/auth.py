# Path: core/lsp/scaffold_server/auth.py
# --------------------------------------
# LIF: INFINITY | ROLE: SENTINEL_GUARD | RANK: SOVEREIGN
# auth_code: Ω_AUTH_INVINCIBLE_TOTALITY_V24_SINGULARITY

import time
import secrets
import os
import re
import threading
import uuid
from typing import Any, Dict, Optional, Tuple, Set, Union
from ..base import forensic_log, JsonRpcError, ErrorCodes

# =================================================================================
# == THE LAWS OF THE CITADEL (CONSTANTS)                                         ==
# =================================================================================
MAX_AUTH_FAILURES = 10
THROTTLE_DURATION = 30.0
AUTH_RECOVERY_TIME = 60.0
MIN_ENTROPY_LENGTH = 16

# [ASCENSION 3]: THE PURIFIER MATRIX
# Strips all whitespace, control chars, and non-ASCII entropy
TOKEN_PURIFIER = re.compile(r'[\s\x00-\x1f\x7f-\xff]')


class SentinelGuard:
    """
    =================================================================================
    == THE SENTINEL GUARD (V-Ω-TOTALITY-V24-INVINCIBLE)                            ==
    =================================================================================
    The Supreme Immune System. Adjudicates the trust relationship between the
    Ocular Mind and the Kinetic Hand with absolute forensic precision.
    =================================================================================
    """

    def __init__(self, server: Any):
        self.server = server
        self._lock = threading.RLock()

        # Vitality State
        self._failed_attempts = 0
        self._last_attempt_ts = 0.0
        self._consecrated_visas: Set[str] = set()

        # Telemetry
        self.total_consecrations = 0
        self.total_rejections = 0
        self._session_id = f"auth-core-{uuid.uuid4().hex[:6]}"

    def handle_relay_auth(self, params: Any) -> Dict[str, Any]:
        """
        [THE RITE OF CONSECRATION]
        The primary gateway for the Silver Cord authentication.
        """
        now = time.time()
        trace_id = params.get("trace_id") or f"tr-auth-{uuid.uuid4().hex[:4]}"

        # --- MOVEMENT I: METABOLIC CIRCUIT BREAKER ---
        # [ASCENSION 4 & 16]: Throttling and Self-Healing
        with self._lock:
            if now - self._last_attempt_ts > AUTH_RECOVERY_TIME:
                self._failed_attempts = 0  # Decay failures

            if self._failed_attempts >= MAX_AUTH_FAILURES:
                wait_time = int(THROTTLE_DURATION - (now - self._last_attempt_ts))
                if wait_time > 0:
                    forensic_log(f"Auth Blocked: Circuit Breaker active for {wait_time}s", "CRIT", "AUTH",
                                 trace_id=trace_id)
                    return {
                        "success": False,
                        "status": "THROTTLED",
                        "message": "Protocol Violation: High frequency auth failure.",
                        "retry_after": wait_time
                    }

        # --- MOVEMENT II: ATOMIC PURIFICATION ---
        # [ASCENSION 3 & 21]: Null-safe and Purified
        raw_token = str(params.get("token", "") or params.get("auth_token", ""))
        incoming = TOKEN_PURIFIER.sub('', raw_token)

        # [ASCENSION 12]: JIT Master Scrying
        # We ensure the master token is current and purified
        master_raw = str(getattr(self.server, '_daemon_token', 'VOID'))
        master = TOKEN_PURIFIER.sub('', master_raw)

        identity = params.get("identity", "UNKNOWN_ENTITY")
        forensic_log(f"Auth Challenge from {identity} [{self._session_id}]", "RITE", "AUTH", trace_id=trace_id)

        # --- MOVEMENT III: THE ADJUDICATION ---
        # [ASCENSION 1 & 7]: Constant-time and Entropy Check
        if not self._is_entropy_sufficient(incoming):
            return self._reject_plea(identity, trace_id, now, "INSUFFICIENT_ENTROPY")

        # [ASCENSION 1]: CONSTANT-TIME ADJUDICATION
        if secrets.compare_digest(incoming, master):
            return self._consecrate_link(identity, trace_id)
        else:
            return self._reject_plea(identity, trace_id, now, "TOKEN_MISMATCH", incoming, master)

    def _is_entropy_sufficient(self, token: str) -> bool:
        """[ASCENSION 7]: Guard against 'VOID' or blank token scenarios."""
        if not token or token == "VOID": return False
        return len(token) >= MIN_ENTROPY_LENGTH

    def _consecrate_link(self, identity: str, trace_id: str) -> Dict[str, Any]:
        """[RITE]: CONSECRATION_SUCCESS"""
        with self._lock:
            self._failed_attempts = 0
            self.total_consecrations += 1

            # [ASCENSION 9]: Establish Full-Duplex Authority
            self.server._relay_active = True

            # [ASCENSION 6]: Forge Session Visa
            visa = secrets.token_hex(32)
            self._consecrated_visas.add(visa)

        forensic_log(f"Lattice Consecrated. Neural Relay established for {identity}.", "SUCCESS", "AUTH",
                     trace_id=trace_id)

        # [ASCENSION 8]: HAPTIC UI FEEDBACK (BLOOM)
        self.server.endpoint.send_notification("gnostic/vfx", {
            "type": "bloom",
            "color": "#10b981",
            "intensity": 0.8
        })

        # [ASCENSION 5]: RELEASE THE ADRENALINE
        # Trigger the conducter to release the backlog across the Silver Cord.
        if hasattr(self.server, 'adrenaline') and self.server.adrenaline:
            # Dispatch flush in a dedicated kinetic thread
            threading.Thread(
                target=self.server.adrenaline.flush_backlog,
                name="AdrenalineFlush-Task",
                daemon=True
            ).start()

        return {
            "success": True,
            "status": "CONSECRATED",
            "session_id": self.server._session_id,
            "visa": visa,
            "trace_id": trace_id
        }

    def _reject_plea(self, identity: str, trace_id: str, ts: float, reason: str,
                     incoming: str = "", master: str = "") -> Dict[str, Any]:
        """[RITE]: CONSECRATION_FAILURE"""
        with self._lock:
            self._failed_attempts += 1
            self._last_attempt_ts = ts
            self.total_rejections += 1

        # [ASCENSION 2]: HEX-SPECTRAL FORENSICS
        # This is the "Smoking Gun" for the invisible character heresy.
        inc_hex = incoming.encode('utf-8').hex() if incoming else "VOID"
        mas_hex = master.encode('utf-8').hex() if master else "VOID"

        forensic_log(f"Auth Fracture [{reason}]: {identity}", "ERROR", "AUTH", trace_id=trace_id)
        forensic_log(f"Forensic Hex -> Incoming: {inc_hex}", "DEBUG", "AUTH", trace_id=trace_id)
        forensic_log(f"Forensic Hex -> Master:   {mas_hex}", "DEBUG", "AUTH", trace_id=trace_id)

        # [ASCENSION 8]: HAPTIC UI FEEDBACK (SHAKE)
        self.server.endpoint.send_notification("gnostic/vfx", {
            "type": "shake",
            "intensity": 0.6
        })

        return {
            "success": False,
            "status": "REJECTED",
            "message": f"Consecration Failed: {reason}",
            "code": f"AUTH_FRACTURE_{reason}",
            "trace_id": trace_id
        }

    def verify_visa(self, visa: str) -> bool:
        """[ASCENSION 6]: Validates ephemeral access tokens."""
        return visa in self._consecrated_visas

# === SCRIPTURE SEALED: THE SENTINEL IS INVINCIBLE ===