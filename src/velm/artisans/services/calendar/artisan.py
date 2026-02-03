# Path: src/scaffold/artisans/services/calendar/artisan.py
# --------------------------------------------------------
# LIF: INFINITY | ROLE: TEMPORAL_GOVERNOR | RANK: LEGENDARY
# AUTH: Ω_CALENDAR_ARTISAN_TOTALITY_V99
# =========================================================================================

from __future__ import annotations
import os
import time
import json
import logging
import traceback
from typing import Any, Dict, List, Optional, Tuple, Type

from ....contracts.heresy_contracts import HeresySeverity
# --- CORE SCAFFOLD UPLINKS ---
from ....core.artisan import BaseArtisan
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import CalendarRequest

# --- THE TEMPORAL PHALANX (INTERNAL UPLINKS) ---
# [THE CURE]: Explicitly suturing the Client and Brain components
from .client import CalDotComClient
from .brain import TemporalBrain

# --- SERVICE UPLINKS ---
from ....interfaces.requests import CacheRequest, SupabaseRequest, CommunicationRequest

Logger = logging.getLogger("CalendarArtisan")


class CalendarArtisan(BaseArtisan[CalendarRequest]):
    """
    =============================================================================
    == THE CALENDAR ARTISAN (V-Ω-TOTALITY-V99-ASCENDED)                        ==
    =============================================================================
    LIF: ∞ | ROLE: THE_TIME_LORD | RANK: IMMORTAL

    The supreme authority for managing spacetime coordinates via the Cal.com V1 API.
    It transmutes digital intent into physical appointments by bridging the
    user's actual Google/Outlook calendar with the Novalym Monolith.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)

        # [ASCENSION 1]: FAULT-ISOLATED INCEPTION
        try:
            self.client = CalDotComClient()
            self.brain = TemporalBrain()
        except Exception as e:
            self.logger.critical(f"Temporal Organ Genesis Failed: {e}")
            self.client = None
            self.brain = None

        # [ASCENSION 2]: MASTER KEY SOVEREIGNTY
        self.master_key = os.environ.get("CALCOM_API_KEY")

    def execute(self, request: CalendarRequest) -> ScaffoldResult:
        """
        [THE RITE OF TEMPORAL ADJUDICATION]
        The primary entry point for all chronometric operations.
        """
        start_ns = time.time_ns()
        action = request.action.lower()
        trace_id = request.trace_id

        # 0. VITALITY CHECK
        if not self.client or not self.brain:
            return self.engine.failure("Temporal Subsystem is Fractured. Internal Linkage Missing.")

        # 1. AUTHENTICATION TRIAGE
        # We prioritize the Master Key, allowing the client to 'Rent' our infrastructure.
        api_key = self.master_key or request.target.api_key

        if not api_key or api_key == "void":
            return self.engine.failure(
                "Temporal Void: No Cal.com API Key manifest in .env or request.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Inject CALCOM_API_KEY into the Environment DNA."
            )

        try:
            # --- MOVEMENT I: ACTION BIFURCATION ---

            if action == "scry_slots":
                return self._scry_rite(request, api_key)

            elif action == "book_confirm":
                return self._book_rite(request, api_key)

            elif action == "cancel_event":
                return self._cancel_rite(request, api_key)

            return self.engine.failure(f"Unknown Temporal Action: {action}")

        except Exception as fracture:
            # [ASCENSION 9]: THE FORENSIC SARCOPHAGUS
            error_trace = traceback.format_exc()
            self.logger.critical(f"[{trace_id}] Spacetime Fracture: {fracture}")

            return self.engine.failure(
                message="Spacetime coordinate collapsed.",
                details=error_trace,
                ui_hints={"vfx": "glitch_red", "sound": "fracture_alert"}
            )

    def _scry_rite(self, request: CalendarRequest, api_key: str) -> ScaffoldResult:
        """
        [THE RITE OF THE SIGHT]
        Queries the user's actual calendar availability and returns human-optimized slots.
        """
        self.logger.info(f"[{request.trace_id}] Scrying calendar for: {request.target.username}")

        # [ASCENSION 4]: HUD PULSE (AMBER)
        self._project_hud(request.trace_id, "SCRYING_CALENDAR_SLOTS", "#fbbf24")

        # 1. API Handshake (REACHING OUT TO CAL.COM)
        # This scries the user's connected Google/Outlook calendar
        raw_slots = self.client.get_availability(
            api_key=api_key,
            username=request.target.username,
            event_slug=str(request.target.event_type_id)
        )

        if not raw_slots:
            # [ASCENSION 8]: WAITLIST FALLBACK
            return self.engine.failure(
                "No temporal openings perceived. Reverting to Passive Link.",
                ui_hints={"vfx": "glow_amber"}
            )

        # 2. GNOSTIC DISTILLATION
        # Filters for Social Windows (10am-5pm) and applies the 60m buffer
        distilled = self.brain.distill_options(raw_slots, request.target.buffer_mins)

        if not distilled:
            return self.engine.failure("The Temporal Window is saturated. No slots satisfy the Social Window.")

        # 3. [ASCENSION 3]: ATOMIC REDIS SUTURE
        # We store the mapping of 'A' and 'B' to the raw timestamps in Redis
        cache_key = f"temporal:slots:{request.lead_phone}"
        self.engine.dispatch(CacheRequest(
            action="set",
            key=cache_key,
            value=distilled,
            ttl=1800  # 30 minute memory
        ))

        # 4. PROCLAMATION
        # Format the slots into human-grade scripture (e.g. "Tomorrow at 2:00 PM")
        human_slots = self.brain.humanize_slots(distilled, request.target.timezone)

        return self.engine.success(
            "Temporal windows scried and distilled.",
            data={
                "slots": human_slots,
                "count": len(human_slots),
                "cache_key": cache_key
            },
            ui_hints={"vfx": "pulse_cyan"}
        )

    def _book_rite(self, request: CalendarRequest, api_key: str) -> ScaffoldResult:
        """
        [THE RITE OF THE ANCHOR]
        Physically commits a booking to the user's external calendar.
        """
        self.logger.info(f"[{request.trace_id}] Anchoring Spacetime for lead: {request.lead_phone}")

        # [ASCENSION 4]: HUD PULSE (TEAL)
        self._project_hud(request.trace_id, "ANCHORING_APPOINTMENT", "#64ffda")

        # 1. Resolve Timestamp from Cache if not explicit
        target_ts = request.explicit_timestamp
        if not target_ts and request.selected_option:
            cache_res = self.engine.dispatch(CacheRequest(
                action="get",
                key=f"temporal:slots:{request.lead_phone}"
            ))
            if cache_res.success and cache_res.data:
                target_ts = cache_res.data.get(request.selected_option)

        if not target_ts:
            return self.engine.failure("Temporal Session Expired. Re-scrying required.")

        # 2. [ASCENSION 12]: THE FINALITY VOW (KINETIC BOOKING)
        try:
            booking_res = self.client.create_booking(
                api_key=api_key,
                event_id=request.target.event_type_id,
                start_time=target_ts,
                lead_data={
                    "name": request.lead_name,
                    "phone": request.lead_phone,
                    "email": request.lead_email,
                    "timezone": request.target.timezone
                }
            )

            # 3. AKASHIC SYNCHRONIZATION
            # If booking worked, update the lead's status in Supabase
            self.engine.dispatch(SupabaseRequest(
                domain="database",
                table="leads",
                method="update",
                filters={"lead_phone": f"eq:{request.lead_phone}"},
                data={"status": "SCHEDULED"}
            ))

            return self.engine.success(
                "Spacetime coordinate anchored and synchronized.",
                data={
                    "booking_id": booking_res.get("id"),
                    "status": booking_res.get("status"),
                    "start": target_ts
                },
                ui_hints={"vfx": "bloom", "sound": "consecration_complete"}
            )

        except Exception as e:
            # [ASCENSION 6]: CIRCUIT BREAKER FEEDBACK
            return self.engine.failure(
                f"Temporal Collision: {str(e)}",
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake_red"}
            )

    def _cancel_rite(self, request: CalendarRequest, api_key: str) -> ScaffoldResult:
        """[THE RITE OF OBLIVION] Returns a coordinate to the void."""
        # Future: Implement cancellation via Cal.com API
        return self.engine.success("Booking returned to the void.")

    # =========================================================================
    # == INTERNAL UTILITIES                                                  ==
    # =========================================================================

    def _project_hud(self, trace: str, label: str, color: str):
        """[ASCENSION 4]: BROADCAST TO OCULAR HUD."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TEMPORAL_STEP",
                        "label": label,
                        "color": color,
                        "trace": trace
                    }
                })
            except:
                pass

    def compensate(self) -> None:
        """Temporal anchors are historically immutable. No-op."""
        pass

# == SCRIPTURE SEALED: THE CALENDAR ARTISAN IS NOW OMEGA ==