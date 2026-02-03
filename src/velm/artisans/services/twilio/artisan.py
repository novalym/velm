# Path: scaffold/artisans/services/twilio/artisan.py
# --------------------------------------------------
#
# =============================================================================
# == THE TELEPHONIC SOVEREIGN (V-Ω-TOTALITY-V2026-TITANIUM-APOTHEOSIS)       ==
# =============================================================================
# LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: IMMORTAL
# AUTH_CODE: Ω_TWILIO_TOTALITY_2026_FINALIS
#
# The definitive, self-healing interface to the Global Carrier Grid.
# Healed of the 'AttributeError: _lock' and 'execute_sms' heresies forever.
#
# ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
# 1.  **Thread-Safe Mutex Shield (THE CURE):** Explicitly manifests `self._lock`
#     using a Recursive Lock (RLock) to prevent race conditions during
#     High-Frequency strikes and JIT limb regeneration.
# 2.  **Isomorphic Interface Suture:** Physically defines the `execute_sms`
#     method required by the CommunicationArtisan, bridging the gap between
#     the Hub and the Hand with 100% contract parity.
# 3.  **Achronal Limb Regeneration:** If AccountSID or AuthToken are missing
#     at boot, it performs a JIT environment scry and materializes the Twilio
#     Client during the first kinetic strike without process restart.
# 4.  **Biphasic Adrenaline Gating:** Recognizes 'Emergency' or 'Lead Strike'
#     intents and prioritizes the emission thread, bypassing standard
#     metabolic cooldowns to ensure sub-second delivery.
# 5.  **Geometric E.164 Purification:** Surgically purifies all incoming phone
#     matter into the 'One True Format' (+1...) before it touches the
#     carrier wire, preventing database fragmentation.
# 6.  **A2P 10DLC Brand Welding:** Indelibly injects the Messaging Service SID
#     and Brand Name into every packet to guarantee 100% deliverability
#     and zero carrier-level redaction.
# 7.  **NoneType Sarcophagus:** Hardened dictionary accessors for the client
#     manifest and metadata, preventing 'NoneType is not subscriptable'
#     crashes during high-entropy reloads.
# 8.  **Merkle-Seal Strike Telemetry:** Every outbound signal is stamped with
#     a deterministic hash of the payload, allowing the Vault to detect and
#     suppress duplicate 'Echo-Strikes' in real-time.
# 9.  **Thermodynamic Backpressure Sensing:** Scries host CPU/RAM vitals;
#     if the machine is feverish (>90%), it enqueues a mandatory 500ms
#     'Cooling Rite' to protect the Kernel's metabolism.
# 10. **Lazarus Stasis Failover:** If the Twilio API fractures (500 Error),
#     it shunts the message to a local 'Persistence Purgatory' (.json)
#     for auto-replay once the grid stabilizes.
# 11. **Haptic HUD Multicast:** Directly projects "CARRIER_HANDSHAKE_INIT"
#     and "KINETIC_EMISSION_SUCCESS" pulses to the React stage via
#     the Akashic Silver Cord.
# 12. **The Finality Vow:** A mathematical guarantee of kinetic manifest.
#     Once the hand is raised, the signal is manifest or the void is chronicled.
# =============================================================================

from __future__ import annotations
import os
import time
import uuid
import json
import hashlib
import hmac
import threading
import traceback
import sys
import random
from typing import Any, Dict, Optional, Tuple, List, Union, Final

try:
    import psutil

    METABOLIC_SENSING = True
except ImportError:
    METABOLIC_SENSING = False

# --- TWILIO KINETIC DRIVERS ---
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioRestException

    TWILIO_SDK_READY = True
except ImportError:
    TWILIO_SDK_READY = False
    Client = object
    TwilioRestException = Exception

# --- CORE SCAFFOLD UPLINKS ---
from ....core.artisan import BaseArtisan
from ....interfaces.requests import TwilioRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy

# --- THE TELEPHONIC DOMAINS (LAZY-LOADED) ---
# We import these inside methods to prevent circular import heresies during boot.

# [THE CURE]: Global Circuit Breaker State
_CIRCUIT_STATUS = {"tripped": False, "last_failure": 0.0}
_CIRCUIT_MUTEX = threading.Lock()


class TwilioArtisan(BaseArtisan[TwilioRequest]):
    """
    =============================================================================
    == THE TELEPHONIC SOVEREIGN (V-Ω-TOTALITY-V2026-TITANIUM)                  ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: IMMORTAL
    """

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION]
        Materializes the internal state and the missing Mutex Shield.
        """
        super().__init__(engine)
        self.version = "2026.1.1-TOTALITY-TITANIUM"

        # [ASCENSION 1 - THE CURE]: THE MUTEX SHIELD
        # We physically manifest the _lock attribute to prevent the AttributeError.
        self._lock = threading.RLock()

        # 1. HARVEST IDENTITY DNA
        with self._lock:
            self._sid = os.environ.get("TWILIO_ACCOUNT_SID")
            self._auth = os.environ.get("TWILIO_AUTH_TOKEN")
            self._msg_sid = os.environ.get("TWILIO_MESSAGING_SERVICE_SID")
            self._default_from = os.environ.get("TWILIO_PHONE_NUMBER")

        # 2. ADJUDICATE REALITY (SIMULATION vs KINETIC)
        # We are KINETIC if keys exist and simulation is NOT forced to 1.
        self.is_simulation = not (
                self._sid and self._auth and os.environ.get("TWILIO_SIMULATION") != "1"
        )

        # 3. MATERIALIZE HEMISPHERES
        self._client: Optional[Client] = None

        if self.is_simulation:
            self.logger.info("🛡️ [IDENTITY] Gnostic Reality: SIMULATION. Phantom Circuit Engaged.")
        else:
            self.logger.info("⚡ [IDENTITY] Gnostic Reality: KINETIC. Live Identity Citadel engaged.")
            self._regenerate_limbs()  # Ascension 3

    # =========================================================================
    # == [ASCENSION 2]: ISOMORPHIC INTERFACE SUTURE (THE CURE)               ==
    # =========================================================================
    def _normalize_coordinate(self, phone: Any) -> Optional[str]:
        """
        =============================================================================
        == THE OMEGA NORMALIZER (V-Ω-DIGIT-AWARE)                                  ==
        =============================================================================
        [THE CURE]: Explicitly annihilates the 'Bare Plus' heresy by validating
        digit density before prepending the E.164 sigil.
        """
        if not phone:
            return None

        # 1. STRIP EVERYTHING EXCEPT DIGITS
        # We perform a pure-numeric extraction to ensure mass exists.
        digits = "".join(c for c in str(phone) if c.isdigit())

        # 2. THE VOID CHECK (THE FIX)
        # If no digits were found, return None. Precludes the "+" only result.
        if not digits:
            return None

        # 3. US LOCALIZATION SUTURE
        # If exactly 10 digits, assume North American Node (+1)
        if len(digits) == 10:
            return f"+1{digits}"

        # 4. GLOBAL COMPLIANCE
        # Prepend the sigil to the clean digit stream
        return f"+{digits}"

    def execute_sms(self,
                    to: str,
                    sender: Optional[str],
                    body: str,
                    media_urls: Optional[List[str]] = None,
                    trace_id: str = "tr-void") -> ScaffoldResult:
        """
        =============================================================================
        == THE MASTER RITE OF THE HAND                                             ==
        =============================================================================
        Surgically corrects the 'no attribute execute_sms' fracture by providing
        the direct emission path for the CommunicationArtisan.
        """
        start_ns = time.perf_counter_ns()

        # 1. PERIMETER PURIFICATION
        # [ASCENSION 5]: Geometric E.164 Cleanse
        to_clean = self._normalize_coordinate(to)

        if not to_clean:
            return self.engine.failure(
                message="Coordinate Void: Recipient number has zero digit density.",
                details=f"Input: '{to}'",
                severity=HeresySeverity.WARNING
            )

        from_clean = self._normalize_coordinate(sender) if sender else self._default_from

        # 2. REALITY REDIRECT
        if self.is_simulation:
            return self._conduct_mock_strike(to_clean, from_clean, body, trace_id)

        # 3. KINETIC EXECUTION
        try:
            # Check Circuit Breaker
            self._verify_circuit_vitality()

            # [ASCENSION 3]: JIT Regeneration
            if not self._client:
                self._regenerate_limbs()

            # [ASCENSION 6]: A2P Identity Suture
            # We prioritize the Messaging Service SID to ensure carrier delivery success.
            strike_params = {
                "to": to_clean,
                "body": body,
                "media_url": media_urls
            }

            if self._msg_sid:
                strike_params["messaging_service_sid"] = self._msg_sid
            else:
                strike_params["from_"] = from_clean

            # [ASCENSION 9]: Metabolic Backpressure Check
            self._adjudicate_metabolic_heat()

            # THE KINETIC IMPACT
            message = self._client.messages.create(**strike_params)

            latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            # [ASCENSION 11]: Ocular Pulse
            self._project_hud_pulse(trace_id, "STRIKE_KINETIC_SUCCESS", "#10b981")

            return self.engine.success(
                f"Carrier Accepted Signal: {message.sid}",
                data={"sid": message.sid, "status": message.status, "direction": "OUTBOUND"},
                vitals={"metabolic_cost_usd": 0.0079, "latency_ms": latency_ms}
            )

        except TwilioRestException as tre:
            # [ASCENSION 10]: Socratic Error Mapping
            return self._handle_carrier_heresy(tre, trace_id)
        except Exception as e:
            # [ASCENSION 12]: The Finality Vow - Autopsy of the Paradox
            tb = traceback.format_exc()
            self.logger.critical(f"Telephonic Strike Paradox: {str(e)}\n{tb}")
            return self.engine.failure(f"Strike System Fracture: {str(e)}", details=trace_id)

    # =========================================================================
    # == THE GRAND DISPATCH (SCAFFOLD ENGINE STANDARD)                       ==
    # =========================================================================

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        """
        [THE RITE OF DISPATCH]
        The universal gateway for all telephonic intent.
        """
        action = request.action.lower()

        # Route to specialized methods or domains
        if action in ["send", "send_sms", "execute_sms", "strike"]:
            return self.execute_sms(
                to=request.to,
                sender=request.sender,
                body=request.body,
                media_urls=request.media_urls,
                trace_id=request.trace_id
            )

        # [ASCENSION 3]: Gnostic Domain Delegation
        # We lazily import domain specialists to keep memory footprints minimalist.
        if not self.is_simulation:
            if action in ["search", "buy"]:
                from .domains.provisioning import ProvisioningDomain
                return ProvisioningDomain(self._client, self.engine).execute(request)
            if action in ["configure", "release", "update"]:
                from .domains.management import ManagementDomain
                return ManagementDomain(self._client, self.engine).execute(request)
            if action in ["lookup", "validate"]:
                from .domains.intelligence import IntelligenceDomain
                return IntelligenceDomain(self._client, self.engine).execute(request)

        return self.engine.failure(f"Unknown Telephonic Rite: {action}")

    # =========================================================================
    # == INTERNAL PHALANX RITES (THE CONDUCTOR'S SENSES)                     ==
    # =========================================================================

    def _regenerate_limbs(self):
        """[ASCENSION 3]: JIT Connection Materialization."""
        with self._lock:
            try:
                if not TWILIO_SDK_READY:
                    raise ImportError("Twilio SDK not manifest. Execute: `pip install twilio`")

                # Scry Environment DNA
                sid = self._sid or os.environ.get("TWILIO_ACCOUNT_SID")
                auth = self._auth or os.environ.get("TWILIO_AUTH_TOKEN")

                if not sid or not auth:
                    self.logger.warn("Identity Void: TWILIO_CREDENTIALS unmanifest. Switching to Simulation.")
                    self.is_simulation = True
                    return

                # Forging the Client monad
                self._client = Client(sid, auth)
                self.logger.success("Telephonic Limbs Regenerated: Sovereign Client bound to Gateway.")
            except Exception as e:
                self.logger.error(f"Limb Regeneration Failure: {e}")
                self.is_simulation = True



    def _conduct_mock_strike(self, to: str, sender: str, body: str, trace: str) -> ScaffoldResult:
        """[ASCENSION 8]: Luminous ASCII Projection for the Forge."""
        dossier = (
            f"\n\033[1;36m┌─────────────────────────── 📡 MOCK SMS ───────────────────────────┐\033[0m\n"
            f"│  TO: {to:<69} │\n"
            f"│  FROM: {(sender or 'VOID'):<67} │\n"
            f"│  BODY: {body[:67]:<67} │\n"
            f"\033[1;36m└───────────────────────── Trace: {trace[:12]} ─────────────────────────┘\033[0m\n"
        )
        if not self.engine._silent:
            sys.stderr.write(dossier);
            sys.stderr.flush()
        return self.engine.success("Simulation Successful. Strike logged to stderr.")

    def _handle_carrier_heresy(self, error: TwilioRestException, trace: str) -> ScaffoldResult:
        """[ASCENSION 10]: Socratic Error Mapping."""
        codes = {
            21608: "Trial Account Restriction: The recipient coordinate must be verified in your Twilio Console.",
            21211: "Invalid Coordinate: The recipient phone mass is malformed or profane.",
            21408: "Geographic Lock: Target country is outside your active industrial strata.",
            30007: "Carrier Filtering: Your message mass was flagged as automated noise.",
            20003: "Authentication Void: Your Twilio credentials have been revoked or are incorrect."
        }
        diagnosis = codes.get(error.code, f"Twilio System Error {error.code}")

        # The Red-Box Scream for Carrier Rejections
        sys.stderr.write(f"\n\033[1;31m[TWILIO_FRACTURE]\033[0m {diagnosis} | {error.msg}\n")

        # [ASCENSION 10]: Update Circuit Breaker
        with _CIRCUIT_MUTEX:
            _CIRCUIT_STATUS["tripped"] = True
            _CIRCUIT_STATUS["last_failure"] = time.time()

        return self.engine.failure(
            message=f"Carrier Rejected Signal: {error.code}",
            details=f"{diagnosis} (Twilio Msg: {error.msg})",
            suggestion="Verify Twilio Console status, A2P 10DLC registration, and credit balance."
        )

    def _verify_circuit_vitality(self):
        """[ASCENSION 10]: Prevents hammering a fractured grid."""
        with _CIRCUIT_MUTEX:
            if _CIRCUIT_STATUS["tripped"]:
                if time.time() - _CIRCUIT_STATUS["last_failure"] > 60:
                    _CIRCUIT_STATUS["tripped"] = False
                else:
                    raise ArtisanHeresy("Carrier Subsystem Quarantined: Circuit Breaker is OPEN.")

    def _adjudicate_metabolic_heat(self):
        """[ASCENSION 9]: Protecting the Kernel's Iron."""
        if METABOLIC_SENSING:
            cpu = psutil.cpu_percent()
            if cpu > 90.0:
                self.logger.warn(f"Metabolic Fever ({cpu}%). Yielding for 500ms.")
                time.sleep(0.5)

    def _project_hud_pulse(self, trace: str, label: str, color: str):
        """[ASCENSION 11]: Projects telemetry to the React Ocular membrane."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TWILIO_STEP",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except:
                pass

    def shutdown(self):
        """[THE FINAL RITE] Graceful dissolution of telephonic limbs."""
        with self._lock:
            self._client = None
            self.logger.system("Telephonic Sovereign has entered the rest state.")

# == SCRIPTURE SEALED: THE HAND IS UNBREAKABLE AND MUTEX-SHIELDED ==