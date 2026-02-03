# Path: packages/scaffold/src/scaffold/artisans/services/communication/channels/sms_twilio.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: KINETIC_SIGNAL_EMITTER | RANK: SOVEREIGN
# SYSTEM: SCAFFOLD_CORE | PROTOCOL: Ω_KINETIC_EMISSION_V38
# =========================================================================================

from __future__ import annotations
import os
import time
import logging
import math
import threading
import json
import re
import traceback
from typing import Any, Optional, Dict, Tuple, List
from pathlib import Path

# --- CORE SCAFFOLD UPLINKS ---
from .base import BaseCourier
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult
from .....contracts.heresy_contracts import Heresy, HeresySeverity

# [PHYSICS CONSTANTS]
GSM_CHARSET = "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1b\f^{}\\[~]|€ !\"#%&'()*+,-./0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SEGMENT_SIZE_GSM = 160
SEGMENT_SIZE_GSM_MULTI = 153
SEGMENT_SIZE_UCS2 = 70
SEGMENT_SIZE_UCS2_MULTI = 67

Logger = logging.getLogger("Courier:Twilio")


class TwilioCourier(BaseCourier):
    """
    =============================================================================
    == THE OMEGA TELEPHONIC COURIER (V-Ω-TOTALITY-V42-FINAL)                   ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_SIGNAL_EMITTER | RANK: SOVEREIGN

    The definitive interface for the Global Carrier Grid.
    Hardened for multi-environment execution and forensic auditability.
    """

    # [ASCENSION 4]: THE ORACLE OF ERRORS
    # Maps Twilio Error Codes to Socratic Heresies and Redemption Paths
    ERROR_GRIMOIRE = {
        20003: ("Capital Exhaustion", "The Treasury is empty. Twilio balance is insufficient."),
        21211: ("Coordinate Invalid", "The recipient's phone number is malformed or invalid."),
        21408: ("Geographic Restriction", "Target region is blocked by your account permissions."),
        21610: ("Blacklist Block", "The recipient has willed silence (Opted-out via STOP)."),
        21612: ("Service Inactive", "The Messaging Service is currently dormant or suspended."),
        21614: ("Incompatible Node", "Target is a Landline and cannot receive phonic matter."),
        30001: ("Queue Overflow", "Twilio account rate limits exceeded."),
        30003: ("Unreachable Destination", "The handset is offline or out of carrier range."),
        30004: ("Message Blocked", "The carrier has blocked this message."),
        30005: ("Carrier Unknown", "The destination carrier is unmapped or experiencing a blackout."),
        30006: ("Landline Block", "The destination carrier blocked the strike (Landline detected)."),
        30007: ("Content Filtered", "Carrier violation: Content resembles SPAM or robotic pattern."),
        30008: ("Unknown Failure", "A generic fracture occurred in the carrier handover."),
        63018: ("Rate Limit Exceeded", "Twilio API concurrency threshold breached.")
    }

    _client_lock = threading.Lock()

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._client: Optional[Any] = None

    @property
    def client(self) -> Any:
        """[THE RITE OF CONNECTION] Thread-safe singleton materialization."""
        if not self._client:
            with self._client_lock:
                if not self._client:
                    # Lazy Import to prevent boot-latency for non-sms projects
                    from twilio.rest import Client as TwilioClient

                    sid = os.environ.get("TWILIO_ACCOUNT_SID")
                    token = os.environ.get("TWILIO_AUTH_TOKEN")

                    if not (sid and token):
                        return None  # Dispatcher will handle simulation fallback

                    self._client = TwilioClient(sid, token)
        return self._client

    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        """
        [THE RITE OF DISPATCH]
        Transmutes the MessageEnvelope into a physical kinetic signal.
        """
        start_time = time.perf_counter()
        trace_id = envelope.metadata.get("trace_id", "0xVOID")

        # 1. RESOLVE IDENTITY ORIGIN
        # Priorities: Metadata -> Environment
        from_number = envelope.metadata.get("from_number") or os.environ.get("TWILIO_FROM_NUMBER")
        mg_sid = envelope.metadata.get("messaging_service_sid") or os.environ.get("TWILIO_MESSAGING_SERVICE_SID")

        if not from_number and not mg_sid:
            return self.engine.failure("Signal Aborted: No provisioned sender identity manifest.")

        # 2. THE CURE: CELESTIAL ATTACHMENT SUTURE
        # [ASCENSION 1]: Extract URLs from attachments for Twilio media_url
        media_urls = []
        for attr in envelope.attachments:
            attr_str = str(attr)
            if attr_str.startswith(('http://', 'https://')):
                media_urls.append(attr_str)

        # 3. PHYSICS AUDIT (Segment Analysis)
        segments, encoding = self._calculate_physics(envelope.body_text)
        recipient = envelope.to[0]

        # 4. STATUS CALLBACK COORDINATION
        # [ASCENSION 10]: Standardize based on the Gateway URL
        gateway = os.environ.get("GATEWAY_URL") or "http://localhost:8000"
        status_url = f"{gateway.rstrip('/')}/v1/ingress/twilio/status"

        # 5. FORGE PAYLOAD
        # Twilio creates an MMS if media_url is present, otherwise SMS.
        params = {
            "to": recipient,
            "body": envelope.body_text,
            "status_callback": status_url
        }

        if mg_sid:
            params["messaging_service_sid"] = mg_sid
        else:
            params["from_"] = from_number

        if media_urls:
            params["media_url"] = media_urls

        # 6. [ASCENSION 12]: THE KINETIC SARCOPHAGUS
        try:
            # 1. Verify Client Vitality
            if not self.client:
                return self.engine.failure("Twilio Client void. Identity required for kinetic strike.")

            # 2. THE MOMENT OF IMPACT
            # [ASCENSION 14]: Atomic Emission
            message = self.client.messages.create(**params)

            # 3. CAPTURE METABOLIC METRICS
            duration_ms = (time.perf_counter() - start_time) * 1000

            # [ASCENSION 3]: ECONOMIC TOMOGRAPHY
            # Note: price is usually None on immediate return; we estimate for vitals
            price_est = len(media_urls) * 0.02 + segments * 0.0079

            # 4. OCULAR HUD BROADCAST
            if self.engine.akashic:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "STRIKE_CONFIRMED",
                        "label": f"SID:{message.sid[:8]}",
                        "color": "#fbbf24",
                        "trace": trace_id
                    }
                })

            # 5. FORGE THE TRIUMPHANT RESULT
            result = self.engine.success(
                message=f"Signal successfully projected to {self._mask(recipient)}",
                data={
                    "sid": message.sid,
                    "status": message.status,
                    "segments": getattr(message, 'num_segments', segments),
                    "encoding": encoding,
                    "price": message.price or f"{price_est:.4f}",
                    "unit": message.price_unit or "USD",
                    "latency_ms": duration_ms
                }
            )

            # [THE FIX]: Explicitly populate the vitals slot
            result.vitals = {
                "metabolic_cost_usd": price_est,
                "latency_ms": duration_ms,
                "trace_id": trace_id,
                "segments": segments
            }

            return result

        except Exception as fracture:
            # 7. [ASCENSION 4]: THE ORACLE OF REDEMPTION
            return self._transmute_fracture(fracture, trace_id, segments)

    def _calculate_physics(self, body: str) -> Tuple[int, str]:
        """Calculates segments and encoding mass."""
        if not body: return 0, "GSM7"

        # Check if characters fall outside the GSM7 spectrum
        is_gsm = all(c in GSM_CHARSET for c in body)
        encoding = "GSM7" if is_gsm else "UCS2"

        # Selection of segment boundaries
        if is_gsm:
            limit = SEGMENT_SIZE_GSM
            per_page = SEGMENT_SIZE_GSM_MULTI
        else:
            limit = SEGMENT_SIZE_UCS2
            per_page = SEGMENT_SIZE_UCS2_MULTI

        length = len(body)
        if length <= limit: return 1, encoding
        return math.ceil(length / per_page), encoding

    def _mask(self, phone: str) -> str:
        """[ASCENSION 9]: Privacy Shroud."""
        if len(phone) > 7: return f"{phone[:3]}***{phone[-4:]}"
        return "***-****"

    def _transmute_fracture(self, e: Exception, trace: str, segments: int) -> ScaffoldResult:
        """
        [THE GNOSTIC REDEMPTION]
        Translates raw carrier exceptions into Socratic Heresies.
        """
        msg = str(e)
        code = 0
        diag = "UNKNOWN_CARRIER_PARADOX"
        sugg = "Verify API key resonance and Twilio balance."
        severity = HeresySeverity.CRITICAL

        # Attempt to parse Twilio-specific metadata
        if hasattr(e, 'code'):
            code = e.code
            g_entry = self.ERROR_GRIMOIRE.get(code)
            if g_entry:
                diag, sugg = g_entry
            else:
                diag = f"Unmapped Carrier Error: {code}"

            # [ASCENSION 5]: 500-Series logic
            if hasattr(e, 'status') and e.status >= 500:
                diag = "CARRIER_INTERNAL_COLLAPSE"
                sugg = "The Twilio Grid is unstable. Wait for auto-resurrection."

        # [ASCENSION 13]: BROADCAST FRACTURE TO HUD
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "STRIKE_FRACTURED",
                    "label": diag,
                    "color": "#ef4444",
                    "trace": trace
                }
            })

        return self.engine.failure(
            message=f"Telephonic Fracture: {diag}",
            severity=severity,
            suggestion=sugg,
            details=f"TwilioCode: {code} | Trace: {trace} | Segments: {segments} | Raw: {msg}",
            # Pass metrics even in failure for forensic auditing
            vitals={
                "metabolic_cost_usd": 0.0,
                "error_code": code,
                "latency_ms": 0.0
            }
        )

# == SCRIPTURE SEALED: THE KINETIC HAND IS IMMUTABLE ==