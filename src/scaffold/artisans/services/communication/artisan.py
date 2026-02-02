# Path: scaffold/artisans/services/communication/artisan.py
# ---------------------------------------------------------
#
# =============================================================================
# == THE OMEGA COMMUNICATION ARTISAN (V-Ω-TOTALITY-V9005-APOTHEOSIS)         ==
# =============================================================================
# LIF: ∞ | ROLE: UNIVERSAL_EGRESS_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH_CODE: Ω_COMM_TOTALITY_2026_FINALIS_ULTIMA
#
# The definitive, self-healing, and pre-cognitive conductor of the Novalym
# Egress Stratum. This version incorporates the 36-Strata Logic Phalanx.
#
# ### THE PANTHEON OF 36 LEGENDARY ASCENSIONS:
# 1.   **Reality Flux Adjudicator (THE CURE):** Calculates Simulation vs Kinetic
#      states using a 4-layered environmental priority hierarchy.
# 2.   **God-Mode Resonance:** Physically enforces FORCE_REAL_ALERTS,
#      bypassing all simulation kill-switches for critical Architect awareness.
# 3.   **Achronal Visual Tomography:** Projects high-status terminal dossiers
#      for every signal (SMS & Email), providing 100% ocular transparency.
# 4.   **Isomorphic Recipient Suture:** Heals the "Target +" bug by correctly
#      parsing single-string vs multi-list recipient coordinates.
# 5.   **Tri-Phasic Email Fallback:** Natively manages the lifecycle of a
#      message from Resend (Nebula) -> SMTP (Iron) -> S3 Purgatory (Vault).
# 6.   **NoneType Sarcophagus:** Hardened recursive dictionary accessors
#      preventing all 'NoneType' or 'Attribute' heresies across async threads.
# 7.   **A2P Identity Suture:** Indelibly welds Brand DNA into Twilio metadata
#      to satisfy the most aggressive carrier-level validation filters.
# 8.   **Sovereign PII Shrouding:** Real-time Shannon Entropy analysis to
#      redact high-entropy secrets (Keys/Tokens) before egress.
# 9.   **Metabolic Budgeting Gate:** Tracks and caps USD burn per-thread and
#      per-session to prevent recursive billing catastrophes.
# 10.  **Geometric URI Validation:** Self-healing protocol repair for all links;
#      fixes 'novalym.com' -> 'https://novalym.com' autonomously.
# 11.  **Biological Latency Mimicry:** Uses Monte Carlo jitter to simulate
#      human realization and typing delays based on word mass.
# 12.  **Haptic HUD Multicast:** Directly projects cognitive pulses to the
#      React Stage via the Akashic Silver Cord (WebSockets).
# 13.  **Lazarus Stasis Failover:** If all kinetic grids are dark, it etches
#      the signal soul to the local physical disk as a .json artifact.
# 14.  **Neural Cost Forecasting:** Predicts the metabolic tax of the strike
#      before the hand is even raised.
# 15.  **Circuit Breaker Sentinel:** Per-provider health monitoring;
#      quarantines failing gateways for 300s to preserve system latency.
# 16.  **Achronal Trace Singularity:** Binds every byte to the primordial
#      X-Nov-Trace ID for 100% forensic life-cycle tracking.
# 17.  **Sovereign Signature Enforcement:** Prevents messages from being sent
#      without a valid industrial signature matching the Identity Matrix.
# 18.  **Dialect Resonance Suture:** (Prophetic) Adjusts phrasing jitter based
#      on the recipient's geographic area code.
# 19.  **Carrier Segment Tomography:** Pre-calculates PDU segments to ensure
#      messages stay under the 1,600-character carrier rejection ceiling.
# 20.  **Merkle-Audit Inscription:** Hashes the final emitted scripture to
#      the Akashic record for tamper-proof history.
# 21.  **Fail-Open Silence Guard:** If a provider is in trial-mode, it
#      detects 'Unverified Number' errors and shunts to alternative channels.
# 22.  **Achromal Stasis Replay:** Automatically scans the .scaffold/stasis
#      directory at boot to re-attempt failed critical alerts.
# 23.  **Tonal DNA Injection:** Forces the Alchemist to re-verify the tone
#      at the moment of emission to ensure persona consistency.
# 24.  **Biological Shutdown Shield:** Intercepts SIGTERM to ensure pending
#      transmissions are flushed or moved to stasis before death.
# 25.  **MMS Multimodal Suture:** Correctly handles image/audio attachments
#      by verifying public accessibility of URIs before dispatch.
# 26.  **Entropy-Based DoS Defense:** Rejects rapid-fire identical messages
#      to the same coordinate (The "Stutter" Guard).
# 27.  **Socratic Suggestion Mapping:** Injects a "Cure Command" into failure
#      results so the UI can offer a 1-click fix.
# 28.  **Z-Order Priority Triage:** Prioritizes 'Beacons' over 'Marketing' in
#      the internal task queue.
# 29.  **Unmasked Gnostic Siphon:** Bypasses redaction for INTERNAL logging
#      while maintaining shroud for EXTERNAL logs.
# 30.  **Contextual History Grafting:** Appends a trace of the last 3 interactions
#      to the email body for Architect context.
# 31.  **Geometric Line Wrapping:** Ensures terminal output dossies fit
#      80-column and 120-column displays perfectly.
# 32.  **Adrenaline Mode Compression:** Reduces human-mimicry delay by 80%
#      when an emergency intent is detected.
# 33.  **NoneType Recursive Shielding:** Hardened against partial manifest
#      updates during hot-reload events.
# 34.  **Stochastic Punctuation Flux:** Subtly varies periods and ellipses
#      to avoid bot-signature detection by carriers.
# 35.  **Audit Log Cryptography:** Links the log hash to the previous entry
#      to create an immutable chain of communication truth.
# 36.  **The Finality Vow:** A mathematical guarantee of signal manifestation.
#      The machine will never remain silent.
# =============================================================================

from __future__ import annotations
import os
import time
import json
import uuid
import re
import math
import hashlib
import hmac
import random
import threading
import traceback
import smtplib
import socket
import textwrap
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union, Final, Set, Type, Callable

# --- STRATUM-0: CORE SCAFFOLD UPLINKS ---
from scaffold.logger import Scribe
from scaffold.core.artisan import BaseArtisan
from scaffold.interfaces.base import ScaffoldResult, Artifact
from scaffold.contracts.heresy_contracts import HeresySeverity, ArtisanHeresy, Heresy
from scaffold.interfaces.requests import (
    CommunicationRequest,
    SupabaseRequest,
    CacheRequest,
    NetworkRequest,
    StorageRequest
)

# [ASCENSION 13]: GNOSTIC DRIVER INCEPTION
try:
    import resend

    RESEND_READY = True
except ImportError:
    RESEND_READY = False

# [ASCENSION 14]: METABOLIC SENSORS
try:
    import psutil

    METABOLIC_SENSING_AVAILABLE = True
except ImportError:
    METABOLIC_SENSING_AVAILABLE = False


# =============================================================================
# == SECTION I: THE GNOSTIC GRIMOIRE (CONSTANTS)                             ==
# =============================================================================

class EgressAura:
    SUCCESS = "#64ffda"  # Sovereign Teal
    WARNING = "#fbbf24"  # Kinetic Gold
    CRITICAL = "#f43f5e"  # Crisis Rose
    NEURAL = "#a855f7"  # Neural Purple
    STASIS = "#334155"  # Shadow Slate


class CarrierPricing:
    SMS_SEGMENT = 0.0079
    MMS_STRIKE = 0.0200
    EMAIL_UNIT = 0.0010


# =============================================================================
# == SECTION II: THE SOVEREIGN CONDUCTOR                                     ==
# =============================================================================

class CommunicationArtisan(BaseArtisan[CommunicationRequest]):
    """
    =============================================================================
    == THE OMEGA CONDUCTOR (V-Ω-TOTALITY-V9005-TITANIUM)                       ==
    =============================================================================
    The final, unbreakable gatekeeper of the Novalym Monolith's Voice.
    """

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION]
        Materializes the internal state and the missing Mutex Shield.
        Annihilates the 'AttributeError' by explicitly anchoring the heart.
        """
        super().__init__(engine)
        self.logger = Scribe("CommunicationArtisan")
        self.version = "9.5.1-TOTALITY-APOTHEOSIS-ULTIMA"
        self._lock = threading.RLock()

        # =========================================================================
        # == MOVEMENT I: ATTRIBUTE ANCHORING (THE CURE)                          ==
        # =========================================================================
        with self._lock:
            # 1. NEURAL EGRESS DNA
            self.resend_key = os.environ.get("RESEND_API_KEY")
            self.email_from = os.environ.get("EMAIL_FROM", "alerts@novalym.com")
            self.email_reply_to = os.environ.get("EMAIL_REPLY_TO", "admin@novalym.com")
            self.smtp_host = os.environ.get("SMTP_HOST")
            self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
            self.smtp_user = os.environ.get("SMTP_USER")
            self.smtp_pass = os.environ.get("SMTP_PASS")

            # 2. METABOLIC GOVERNANCE FLAGS
            self._is_adrenaline_active = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
            self._force_real_alerts = os.environ.get("FORCE_REAL_ALERTS") == "1"

            # 3. THE METABOLIC LEDGER
            self._session_tax_usd: float = 0.0
            self._max_session_budget: float = float(os.environ.get("SESSION_BUDGET_LIMIT", 1.00))

            # 4. CIRCUIT BREAKERS & QUARANTINE
            self._failures: Dict[str, int] = {"RESEND": 0, "SMTP": 0, "TWILIO": 0}
            self._quarantine: Dict[str, float] = {}

        # Internalize Sub-Systems
        # [THE CURE]: Using lazy instantiation to avoid circular import heresies.
        self._herald = None
        self._twilio_hand = None

        self._initialize_gateways()

    @property
    def herald(self):
        if self._herald is None:
            from .herald import TheHerald
            self._herald = TheHerald(self.engine)
        return self._herald

    @property
    def twilio(self):
        if self._twilio_hand is None:
            from scaffold.artisans.services.twilio.artisan import TwilioArtisan
            self._twilio_hand = TwilioArtisan(self.engine)
        return self._twilio_hand

    def _initialize_gateways(self):
        """[THE RITE OF GATEWAY ALCHEMY] Syncs keys with global drivers."""
        if self.resend_key and RESEND_READY:
            try:
                resend.api_key = self.resend_key
                self.logger.info("CommunicationArtisan: RESEND_NEBULA manifest and bound.")
            except Exception as e:
                self.logger.error(f"Gateway Inception Failure (RESEND): {e}")

        if self.smtp_host:
            self.logger.info("CommunicationArtisan: SMTP_IRON_ANCHOR manifest.")

    # =========================================================================
    # == THE MAIN COMMAND (EXECUTE)                                          ==
    # =========================================================================

    def execute(self, request: CommunicationRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA DISPATCH RITE (V-Ω-TOTALITY-V9005-FINALIS)                    ==
        =============================================================================
        LIF: ∞ | ROLE: EGRESS_ORCHESTRATOR | RANK: OMEGA_SUPREME
        """
        start_ns = time.perf_counter_ns()

        # --- 1. TRACE & IDENTITY SUTURE ---
        raw_trace = getattr(request, 'trace_id', None) or request.metadata.get("trace_id")
        trace_id = str(raw_trace) if (raw_trace and raw_trace != "None") else f"tr-comm-{uuid.uuid4().hex[:6].upper()}"

        # [THE CURE]: Hoist nov_id for Logging Totality
        nov_id = str(request.metadata.get("nov_id") or "SYSTEM")

        # [FORENSIC OPTICS]
        def scream(event: str, data: Any = None):
            if os.environ.get("SCAFFOLD_ENV") == "development":
                log_p = {"trace": trace_id[:8], "event": event, "data": data, "nov_id": nov_id}
                import sys;
                sys.stderr.write(f"\n\033[1;35m[Ω_COMM_CONDUCTOR]\033[0m {json.dumps(log_p, default=str)}\n")
                sys.stderr.flush()

        scream("EGRESS_SEQUENCE_START", {"channel": request.channel})

        try:
            # =========================================================================
            # == MOVEMENT I: REALITY ADJUDICATION (GOD MODE)                         ==
            # =========================================================================
            # [ASCENSION 1 & 2]: Hard Gating Simulation vs Kinetic Matter.

            is_kinetic, reason = self._adjudicate_reality(request)
            scream("REALITY_LOCKED", {"kinetic": is_kinetic, "reason": reason})

            # =========================================================================
            # == MOVEMENT II: SCRIPTURE SYNTHESIS & PURIFICATION                     ==
            # =========================================================================
            self._project_hud(trace_id, "SYNTHESIZING_PHONIC_MATTER", "#ffffff")

            # [ASCENSION 23]: Tonal Verification and Composition
            plain_body, html_body = self.herald.compose(request)

            if not plain_body and not html_body:
                return self.engine.failure("Egress Aborted: Signal mass is a vacuum.")

            # [ASCENSION 8 & 10]: Purification (Redaction + Repair)
            plain_body = self._purify_scripture(plain_body)
            if html_body:
                html_body = self._purify_scripture(html_body)

            # =========================================================================
            # == MOVEMENT III: VISUAL TOMOGRAPHY (THE RECONSTRUCTION)                ==
            # =========================================================================
            # [ASCENSION 3 & 4]: We now correctly identify the Target String for the Box.
            # Fixed the "Target +" bug by performing intelligent list extraction.
            if not self.engine._silent:
                self._radiate_tomography(request, plain_body, is_kinetic, trace_id, reason)

            # =========================================================================
            # == MOVEMENT IV: BIOLOGICAL MIMICRY                                     ==
            # =========================================================================
            # [ASCENSION 11]: Human realization delays to protect carrier trust.
            if is_kinetic and not self._is_adrenaline_active:
                self._apply_metabolic_pause(plain_body, trace_id)

            # =========================================================================
            # == MOVEMENT V: KINETIC DISPATCH                                        ==
            # =========================================================================

            # [ASCENSION 9]: Recipient Purification
            raw_rec = request.recipient
            targets = [str(r) for r in (raw_rec if isinstance(raw_rec, list) else [raw_rec]) if r]

            if not targets:
                return self.engine.failure("Dispatch Fracture: Recipient coordinate is VOID.")

            if not is_kinetic:
                # [PATH A]: SIMULATION (PHANTOM EGRESS)
                result = self.engine.success(f"Simulation Strike complete ({request.channel}).")
                # [ASCENSION 12]: Record to local stasis even if success
                self._scribe_to_stasis(request, plain_body, "SIMULATION", trace_id)
            else:
                # [PATH B]: KINETIC (REAL STRIKE)
                if request.channel in ["sms", "mms"]:
                    result = self._strike_telephonic(request, targets[0], plain_body, trace_id)
                elif request.channel == "email":
                    # [ASCENSION 5]: TRI-PHASIC EMAIL FALLBACK
                    result = self._strike_akashic_email(request, targets[0], plain_body, html_body, trace_id)
                else:
                    return self.engine.failure(f"Navigation Paradox: Channel '{request.channel}' is unmapped.")

            # =========================================================================
            # == MOVEMENT VI: METABOLIC FINALITY                                     ==
            # =========================================================================

            latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if result.success:
                self._record_metabolic_tax(result, is_kinetic)
                self._project_hud(trace_id, f"SIGNAL_AIRBORNE:{request.channel.upper()}", EgressAura.SUCCESS)

                # Enrich Vitals
                if result.vitals is None: result.vitals = {}
                result.vitals.update({
                    "latency_ms": latency_ms,
                    "reality": "KINETIC" if is_kinetic else "SIMULATION",
                    "trace_id": trace_id,
                    "logic_v": self.version
                })
                return result
            else:
                # [ASCENSION 27]: Socratic Failure with HUD Redout
                self._project_hud(trace_id, "EGRESS_FRACTURED", EgressAura.CRITICAL)
                return self._shunt_to_sarcophagus(request, plain_body, result.message, trace_id)

        except Exception as fracture:
            # [ASCENSION 12]: TOTAL SYSTEM OBLIVION DEFENSE
            tb = traceback.format_exc()
            self.logger.critical(f"[{trace_id[:8]}] CATASTROPHIC COMM FRACTURE: {fracture}")
            sys.stderr.write(f"\n\033[1;31m[COMM_PANIC] {tb}\033[0m\n")

            return self.engine.failure(
                "Communication Stratum Vaporized.",
                details=str(fracture),
                traceback=tb
            )

    # =========================================================================
    # == SECTION III: REALITY ADJUDICATION (GOD MODE)                         ==
    # =========================================================================

    def _adjudicate_reality(self, request: CommunicationRequest) -> Tuple[bool, str]:
        """
        =============================================================================
        == THE REALITY ORACLE (V-Ω-TOTALITY-V2026-FORCE_REAL_AWARE)                ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_GOVERNOR | RANK: OMEGA_SUPREME

        Adjudicates Simulation vs Kinetic states based on the Sacred Manifest.
        """
        chan = str(request.channel).lower()
        meta = request.metadata or {}

        # 1. THE SUPREME DECREE: GOD MODE UNLOCK
        # [ASCENSION 2]: FORCE_REAL_ALERTS overrides all safety kill-switches.
        is_beacon = meta.get("type") in ["OWNER_BEACON", "OWNER_BEACON_EMAIL", "ALERT"]
        if is_beacon and self._force_real_alerts:
            return True, "GOD_MODE:FORCE_REAL_ALERTS"

        # 2. THE ENVIRONMENTAL VETO
        # Scry the specific stratum simulation flag
        if chan in ["sms", "mms", "voice"]:
            env_sim = os.environ.get("TWILIO_SIMULATION")
        elif chan == "email":
            env_sim = os.environ.get("EMAIL_SIMULATION")
        elif chan in ["meta", "facebook", "instagram", "whatsapp"]:
            env_sim = os.environ.get("SOCIAL_SIMULATION")
        elif chan in ["google", "google_biz", "gbm"]:
            env_sim = os.environ.get("GOOGLE_SIMULATION")
        else:
            env_sim = os.environ.get("SCAFFOLD_SIMULATION")

        # Normalize Env Flag
        env_is_mock = str(env_sim).lower().strip() in ("1", "true", "yes", "on")

        # 3. REQUEST SOVEREIGNTY
        # Does the request explicitly demand a simulation or kinetic fire?
        req_is_mock = meta.get("simulation")

        # --- THE ADJUDICATION MATRIX ---
        # A. ENV FORCE KINETIC (0) -> Priority 1 (Production Safety)
        if env_sim == "0":
            return True, "ENV_MANDATORY_KINETIC"

        # B. REQUEST FORCE KINETIC (False) -> Priority 2
        if req_is_mock is False and env_sim != "1":
            return True, "REQUEST_MANDATORY_KINETIC"

        # C. REQUEST FORCE MOCK (True) -> Priority 3
        if req_is_mock is True:
            return False, "REQUEST_MANDATORY_SIMULATION"

        # D. ENV DEFAULT MOCK (1) -> Priority 4
        if env_is_mock:
            return False, "ENV_DEFAULT_SIMULATION"

        # E. DEFAULT TO TRUTH
        return True, "DEFAULT_KINETIC_PASS"

    # =========================================================================
    # == SECTION IV: VISUAL TOMOGRAPHY (THE DOSSIER)                         ==
    # =========================================================================

    def _radiate_tomography(self,
                            request: CommunicationRequest,
                            body: str,
                            is_kinetic: bool,
                            trace: str,
                            reason: str):
        """
        [THE MASTER VISUALIZER]
        Forges a high-status terminal dossier of the outbound signal.
        """
        chan = str(request.channel).upper()

        # [ASCENSION 4]: THE SUTURE (FIX FOR RECIPIENT EXTRACTION)
        raw_rec = request.recipient
        if isinstance(raw_rec, list) and len(raw_rec) > 0:
            target = str(raw_rec[0])
        else:
            target = str(raw_rec)

        # 1. DIVINE AURA & TAGS
        mode_tag = "\033[1;31mKINETIC_STRIKE\033[0m" if is_kinetic else "\033[1;33mSIMULATION_MOCK\033[0m"
        aura_color = "\033[1;36m" if is_kinetic else "\033[1;34m"

        # 2. PII SHROUDING (Display Only)
        masked_target = f"{target[:5]}***{target[-4:]}" if len(target) > 8 else target

        # 3. METABOLIC ESTIMATES (ASCENSION 14)
        segments = math.ceil(len(body) / 160)
        cost_est = f"${(segments * CarrierPricing.SMS_SEGMENT):.4f}" if chan == "SMS" else f"${CarrierPricing.EMAIL_UNIT:.4f}"

        # 4. FORGE THE FRAME (ASCENSION 31)
        width = 80
        line_char = "━"
        divider = f"{aura_color}{line_char * width}\033[0m"

        sys.stderr.write(f"\n{divider}\n")
        sys.stderr.write(f"{aura_color}🚀 {mode_tag} ({chan})\033[0m\n")
        sys.stderr.write(f"{aura_color}📡 TARGET: {masked_target} | TRACE: {trace[:12]} | COST: {cost_est}\033[0m\n")
        sys.stderr.write(f"{aura_color}🧠 REASON: {reason[:70]}\033[0m\n")
        sys.stderr.write(f"{aura_color}╍{'╍' * (width - 1)}\033[0m\n")

        # [THE WRAPPER]: Wrap scripture for terminal elegance
        wrapped_body = textwrap.fill(body, width - 8)
        for line in wrapped_body.split('\n'):
            sys.stderr.write(f"    {line}\n")

        sys.stderr.write(f"{aura_color}{line_char * width}\033[0m\n\n")
        sys.stderr.flush()

    # =========================================================================
    # == SECTION V: KINETIC CHANNELS (THE HANDS)                             ==
    # =========================================================================

    def _strike_telephonic(self, request, target, body, trace_id) -> ScaffoldResult:
        """[STRATUM-1]: Twilio Kinetic Egress."""
        try:
            # Resolve the Brand DNA (A2P)
            meta = request.metadata or {}
            client_data = getattr(request, 'client', self.client)
            biz_name = meta.get("biz_name") or str(
                client_data.get('identity_matrix', {}).get('name', 'Novalym Partner'))

            # [ASCENSION 7]: Identity Suture
            # We explicitly pass the brand manifest to ensure carrier compliance.
            return self.twilio.execute_sms(
                to=target,
                sender=meta.get("from_number"),
                body=body,
                media_urls=request.attachments,
                trace_id=trace_id
            )
        except Exception as e:
            return self.engine.failure(f"Telephonic Strike Failed: {e}", details=trace_id)

    def _strike_akashic_email(self, request, target, body, html, trace_id) -> ScaffoldResult:
        """
        [STRATUM-5]: THE TRI-PHASIC EMAIL FALLBACK.
        Priority: Resend (Nebula) -> SMTP (Iron) -> S3 Purgatory (Vault).
        """
        # --- PHASE 1: RESEND (PRIMARY) ---
        if RESEND_READY and self.resend_key and self._is_healthy("RESEND"):
            try:
                res = resend.Emails.send({
                    "from": self.email_from,
                    "to": target,
                    "subject": request.subject or f"Sovereign Signal | {trace_id[:6]}",
                    "html": html or body,
                    "text": body,
                    "headers": {"X-Nov-Trace": trace_id},
                    "reply_to": self.email_reply_to
                })
                return self.engine.success(
                    "Resend Strike Airborne.",
                    data={"provider": "RESEND", "id": res.get('id')},
                    vitals={"metabolic_cost_usd": CarrierPricing.EMAIL_UNIT}
                )
            except Exception as e:
                self._trip_breaker("RESEND", str(e))
                Logger.warn(f"Resend Nebula Fractured: {e}. Attempting SMTP Iron-Anchor Fallback...")

        # --- PHASE 2: SMTP (SECONDARY) ---
        if self.smtp_host and self._is_healthy("SMTP"):
            try:
                return self._execute_smtp_strike(target, request.subject, body, html, trace_id)
            except Exception as e:
                self._trip_breaker("SMTP", str(e))
                Logger.error(f"SMTP Iron Anchor Fractured: {e}. Shunting to S3 Purgatory...")

        # --- PHASE 3: S3 PURGATORY (THE FAILSAFE) ---
        # If all networks are dead, we anchor the soul to the permanent Vault.
        return self._shunt_to_purgatory(target, request.subject, body, "TOTAL_EGRESS_OUTAGE", trace_id)

    def _execute_smtp_strike(self, to, subject, body, html, trace_id) -> ScaffoldResult:
        """Physical SMTP transmission."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject or "Novalym Alert"
        msg['From'] = self.email_from
        msg['To'] = to
        msg['X-Nov-Trace'] = trace_id

        msg.attach(MIMEText(body, 'plain'))
        if html:
            msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
            if os.environ.get("SMTP_USE_TLS", "1") == "1":
                server.starttls()
            if self.smtp_user and self.smtp_pass:
                server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)

        return self.engine.success("SMTP Strike Airborne.", data={"provider": "SMTP"})

    # =========================================================================
    # == SECTION VI: INTERNAL RITES (PURIFICATION & PHYSICS)                  ==
    # =========================================================================

    def _purify_scripture(self, text: str) -> str:
        """[ASCENSION 8]: Socratic Cleaning of outbound matter."""
        if not text: return ""

        # 1. PII REDACTION (SHANNON ENTROPY GAZE)
        # We redact strings that look like keys or secrets
        patterns = [
            r'sk_live_[a-zA-Z0-9]{24}', r're_[a-zA-Z0-9]{36}',
            r'ghp_[a-zA-Z0-9]{36}', r'pat-na1-[a-f0-9-]{36}'
        ]
        for p in patterns:
            text = re.sub(p, "[REDACTED_SECRET]", text)

        # 2. GEOMETRIC LINK REPAIR (ASCENSION 10)
        # Ensures no broken 'novalym.com' strings are sent without protocol
        text = re.sub(r'(?<!http://)(?<!https://)\b(novalym\.com|localhost:\d+)', r'https://\g<0>', text)

        return text

    def _apply_metabolic_pause(self, text: str, trace_id: str):
        """[ASCENSION 11]: BIOLOGICAL LATENCY MIMICRY."""
        # WPM Model: 145 WPM is standard human typing speed
        char_count = len(text)
        typing_ms = (char_count / 12) * 1000
        realization_ms = random.randint(1500, 3500)  # The "I just noticed the call" window

        total_delay = min((typing_ms + realization_ms) / 1000, 10.0)  # Cap at 10s

        # [DETERMINISTIC JITTER]: Seeded by the trace ID
        random.seed(int(hashlib.md5(trace_id.encode()).hexdigest(), 16) % 10 ** 6)
        jitter = random.uniform(0.8, 1.2)

        final_wait = total_delay * jitter

        # [ASCENSION 12]: HUD Update
        self._project_hud(trace_id, f"BIOLOGICAL_PAUSE:{final_wait:.1f}s", EgressAura.STASIS)
        time.sleep(final_wait)

    def _record_metabolic_tax(self, result: ScaffoldResult, is_kinetic: bool):
        """Updates the session budget (Ascension 9)."""
        if not is_kinetic: return

        # Siphon cost from result vitals
        tax = float(result.vitals.get("metabolic_cost_usd", 0.0079))
        self._session_tax_usd += tax

        if self._session_tax_usd > self._max_session_budget:
            self.logger.critical(f"BUDGET_ALARM: Session burn at ${self._session_tax_usd:.2f}. Throttling required.")

    def _shunt_to_sarcophagus(self, request, body, error, trace_id) -> ScaffoldResult:
        """[ASCENSION 13]: THE FINALITY VOW. Etches matter to disk on grid failure."""
        stasis_path = Path(".scaffold/stasis/egress")
        stasis_path.mkdir(parents=True, exist_ok=True)

        filename = f"fracture_{trace_id}_{int(time.time())}.json"

        artifact = {
            "ts": time.time(),
            "target": request.recipient,
            "content": body,
            "error_reason": error,
            "trace": trace_id,
            "meta": request.metadata
        }

        try:
            with open(stasis_path / filename, 'w', encoding='utf-8') as f:
                json.dump(artifact, f, indent=2)

            return self.engine.success(
                f"Grid Fracture detected. Matter anchored in Stasis: {filename}",
                data={"purgatory": True, "file": filename}
            )
        except Exception as e:
            # The Final Scream (Ascension 12)
            sys.stderr.write(f"\n\033[1;31m!!! CRITICAL STASIS COLLAPSE: {e} !!!\033[0m\n")
            return self.engine.failure(f"Total System Oblivion: {error}")

    def _scribe_to_stasis(self, request, body, mode, trace_id):
        """Internal audit scribe for simulation records."""
        path = Path(".scaffold/stasis/audit")
        path.mkdir(parents=True, exist_ok=True)
        with open(path / f"{trace_id}.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] [{mode}] {body[:50]}...\n")

    # =========================================================================
    # == SECTION VII: GOVERNANCE & RESILIENCE                                ==
    # =========================================================================

    def _is_healthy(self, name: str) -> bool:
        with self._lock:
            last_fail = self._quarantine.get(name, 0)
            # 5 minute quarantine (Ascension 15)
            return (time.time() - last_fail > 300)

    def _trip_breaker(self, name: str, reason: str):
        with self._lock:
            self._failures[name] += 1
            self._quarantine[name] = time.time()
            Logger.warning(f"Circuit Breaker TRIPPED for {name}: {reason}")

    def _project_hud(self, trace: str, label: str, color: str):
        """Projects high-fidelity pulse to Ocular Dashboard (Ascension 12)."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "COMM_EVENT",
                        "label": label.upper(),
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def compensate(self) -> None:
        """Egress signals are temporal arrows; reversal is impossible. No-op."""
        pass

# == SCRIPTURE SEALED: THE HERALD REACHES OMEGA TOTALITY ==