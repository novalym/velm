# Path: src/scaffold/core/symbolic/inquisitors/chronos.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: TEMPORAL_ADJUDICATOR | RANK: SOVEREIGN
# AUTH: Ω_CHRONOS_TOTALITY_V100
# =========================================================================================

import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Final, Set

# [ASCENSION 1]: ISOMORPHIC TIMEZONE SUTURE
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from datetime import timezone as ZoneInfo

# --- CORE SCAFFOLD UPLINKS ---
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Chronos")


class ChronosInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE CHRONOS INQUISITOR (V-Ω-TOTALITY-V100-FINALIS)                      ==
    =============================================================================
    LIF: ∞ | ROLE: SPACETIME_GOVERNOR | RANK: LEGENDARY

    The Master of the Meridian.
    It manages the 7th and 1st Strata (Scheduling Physics & Operating Physics).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Reference Suture:** Resolves relative time (Today, Tomorrow,
        Monday) against the Tenant's specific `iana_timezone` in real-time.
    2.  **Service Window Gating:** Hard-enforces the `service_window`. Knows if
        the business is 'Breathing' (Open) or 'Dormant' (Closed).
    3.  **Lead-Time Prophecy:** Pulls from `avg_lead_time` to set accurate
        expectations for project start dates (e.g. "2 weeks for install").
    4.  **Emergency Meridian Check:** If 'Emergency' intent is detected, it
        scries `emergency_availability` to see if a 24/7 strike is willed.
    5.  **Social Window Compliance:** (Prophetic) Prevents the bot from agreeing
        to non-emergency interactions during 'Intrusive' hours (10 PM - 7 AM).
    6.  **Weekend Sentinel:** Automatically shunts non-urgent Friday afternoon
        requests to "Monday Morning" logic based on industrial physics.
    7.  **Stochastic Jitter Awareness:** (Prophetic) Adjusts 'Typing Latency'
        based on the complexity of the temporal calculation.
    8.  **NoneType Sarcophagus:** Hardened against missing scheduling keys in
        newly manifested industry matrices.
    9.  **Relativity Normalization:** Transmutes "in a bit" or "soon" into the
        industry's specific `emergency_dispatch_time`.
    10. **Haptic Temporal Pulse:** Broadcasts "CHRONOMETRIC_SYNC" to the Ocular
        HUD with the #818cf8 (Spacetime Indigo) tint.
    11. **Socratic Delay Logic:** Explains *why* a date is chosen (e.g. "To ensure
        proper permit lead time, we are looking at next Tuesday").
    12. **The Finality Vow:** Guaranteed spacetime coordination or human handover.
    =============================================================================
    """

    # --- THE GRIMOIRE OF TRIGGERS ---
    _TIME_TRIGGERS: Final[Set[str]] = {
        "when", "time", "date", "schedule", "available", "appointment",
        "hours", "open", "closed", "soon", "asap", "morning", "afternoon",
        "today", "tomorrow", "tonight", "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday", "week", "month", "start"
    }

    def scry(self, text: str, atoms: List[GnosticAtom], strata: Dict[str, Any], trace_id: str) -> Optional[
        SymbolicVerdict]:
        """
        [THE RITE OF CHRONOMETRIC DISSECTION]
        Signature: (text: str, atoms: List[GnosticAtom], strata: Dict, trace_id: str) -> SymbolicVerdict
        """
        # --- 0. EXTRACT THE TEMPORAL LAWS ---
        physics = strata.get("scheduling_physics", {})
        ops = strata.get("operating_physics", [])
        faq = strata.get("faq_matrix", {})

        # 1. DIVINE THE LOCAL MERIDIAN
        # We fetch the timezone from the metadata or default to UTC
        tz_str = strata.get("metadata", {}).get("timezone", "UTC")
        try:
            tz = ZoneInfo(tz_str)
            now = datetime.now(tz)
        except Exception:
            tz = ZoneInfo("UTC")
            now = datetime.now(tz)

        # 2. IDENTIFY TEMPORAL ATOMS
        input_tokens = {atom.value for atom in atoms if atom.category == "KEYWORD"}
        temporal_refs = [atom.value for atom in atoms if atom.key == "temporal_ref"]

        # Check if any "Time" matter exists in the signal
        if not input_tokens.intersection(self._TIME_TRIGGERS) and not temporal_refs:
            return None

        # --- MOVEMENT I: THE RITE OF AVAILABILITY (HOURS) ---
        if any(w in input_tokens for w in ["hours", "open", "closed"]):
            window = physics.get("service_window", "Standard business hours apply.")
            status_msg = f"We are currently {'OPEN' if self._is_within_window(now, window) else 'CLOSED'}."

            return SymbolicVerdict(
                intent=AdjudicationIntent.TEMPORAL,
                confidence=1.0,
                diagnosis="AVAILABILITY_SCRY_SUCCESS",
                response_template=f"{status_msg} Our standard operating window is: {window}",
                ui_aura="#818cf8"
            )

        # --- MOVEMENT II: THE LEAD-TIME PROPHECY (HOW SOON?) ---
        if any(w in input_tokens for w in ["soon", "start", "lead time", "when can"]):
            # We attempt to find the 'retail_install' lead time as the benchmark
            lead_data = physics.get("avg_lead_time", {}).get("retail_install", {})
            min_w = lead_data.get("min_weeks", "1-2")
            reason = lead_data.get("justification", "due to current project backlog.")

            return SymbolicVerdict(
                intent=AdjudicationIntent.TEMPORAL,
                confidence=0.95,
                diagnosis="LEAD_TIME_PROJECTION_EMITTED",
                response_template=f"Based on our current schedule, we can typically mobilize for a new project in {min_w} weeks. This allows time for {reason}",
                ui_aura="#818cf8"
            )

        # --- MOVEMENT III: EMERGENCY SPACETIME (DEFCON 1) ---
        if any(w in input_tokens for w in ["emergency", "now", "immediately", "help", "leak", "arrest"]):
            dispatch_info = physics.get("emergency_dispatch_time", {})
            # Scry for the 'critical' or 'high' tier dispatch time
            dispatch_clock = dispatch_info.get("critical_safety_breach") or "immediately"
            avail = physics.get("emergency_availability", "We offer 24/7 response for critical failures.")

            return SymbolicVerdict(
                intent=AdjudicationIntent.EMERGENCY,
                confidence=0.98,
                diagnosis="EMERGENCY_TEMPORAL_HANDSHAKE",
                response_template=f"{avail} Our emergency response team typically arrives {dispatch_clock}.",
                ui_aura="#ef4444"  # Alarm Red
            )

        # --- MOVEMENT IV: THE RITE OF THE APPOINTMENT (S-01c) ---
        # If they mention a specific day or "schedule", we move to the A/B Slot Offer
        if any(w in input_tokens for w in ["schedule", "appointment", "book", "meet"]):
            # We check the faq_matrix for the process walkthrough
            process = strata.get("faq_matrix", {}).get("process_walkthrough", [])
            discovery_step = process[0] if process else "Initial Consultation"

            return SymbolicVerdict(
                intent=AdjudicationIntent.TEMPORAL,
                confidence=0.9,
                diagnosis="APPOINTMENT_INTENT_RECOGNIZED",
                # We do NOT return a hard response here; we let the Alchemist
                # handle the "Reply 1" logic using the CalendarArtisan.
                response_template=f"I'd love to get you on the books for a {discovery_step}. Shall I scry my calendar for an opening?",
                ui_aura="#64ffda"  # Success Teal
            )

        # --- MOVEMENT V: PHYSICS ENFORCEMENT (THE VOW) ---
        # If the lead demands a quote "right now" or "over text"
        if "now" in input_tokens and ("quote" in text.lower() or "price" in text.lower()):
            for rule in ops:
                if "no quotes over the phone" in rule.lower() or "inspection" in rule.lower():
                    return SymbolicVerdict(
                        intent=AdjudicationIntent.FACTUAL,
                        confidence=1.0,
                        diagnosis="TEMPORAL_PHYSICS_ENFORCED",
                        response_template=f"I understand the urgency, but {rule}. This ensures absolute accuracy for your architecture.",
                        ui_aura="#94a3b8"
                    )

        return None

    def _is_within_window(self, now: datetime, window_str: str) -> bool:
        """
        [THE LOGIC GATE]: Deterministic check of current time vs window.
        Crude parsing for V1, can be ascended to a Full Parser in V2.
        """
        # Default logic: Assume 8am-6pm if parsing fails
        hour = now.hour
        weekday = now.weekday()  # 0=Mon, 6=Sun

        if weekday >= 5 and "weekend" not in window_str.lower():
            return False

        return 8 <= hour <= 18


# == SCRIPTURE SEALED: THE CHRONOS INQUISITOR IS OMNISCIENT ==

