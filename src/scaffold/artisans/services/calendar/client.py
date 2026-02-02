# Path: src/scaffold/artisans/services/calendar/client.py
# -------------------------------------------------------
# LIF: INFINITY | ROLE: CALCOM_API_PROXY | RANK: SOVEREIGN
# AUTH: Ω_CALENDAR_CLIENT_V3_ASCENDED
# =========================================================================================

import httpx
import os
import logging
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta, timezone

# [ASCENSION 1]: CORE SCAFFOLD UPLINKS
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....interfaces.requests import SupabaseRequest, SupabaseDomain

Logger = logging.getLogger("CalComClient")


class CalDotComClient:
    """
    =============================================================================
    == THE OMEGA CELESTIAL PROXY (V-Ω-TOTALITY-V3.0)                           ==
    =============================================================================
    LIF: ∞ | ROLE: THE_TIME_LORD | RANK: IMMORTAL
    """

    BASE_URL = "https://api.cal.com/v1"

    def get_availability(self, api_key: str, username: str, event_slug: str, context: Dict = None) -> List[Dict]:
        """
        [THE RITE OF THE SIGHT - V3.0]
        Surgically resolves between PHANTOM (Supabase RPC) and KINETIC (Cal.com API) reality.
        """
        context = context or {}
        is_simulation = context.get('simulation', False)
        engine = context.get('engine')  # Injected by the Artisan

        # --- MOVEMENT I: PHANTOM TEMPORAL GATEWAY (BYPASS) ---
        if is_simulation and engine:
            try:
                Logger.info(
                    f"[{context.get('trace_id', 'TEST')[:6]}] Executing PHANTOM Temporal Scry via Supabase RPC...")

                # [ASCENSION 1]: Call the Supabase RPC Phantom Gateway
                res = engine.dispatch(SupabaseRequest(
                    domain=SupabaseDomain.DATABASE,
                    method="rpc",
                    func_name="mock_cal_slots"  # The sovereign function we defined
                ))

                if res.success and res.data and res.data[0].get('slots'):
                    # The RPC returns a list containing the desired JSON object: [{slots: [...]}]
                    return res.data[0]['slots']

                Logger.warning(f"[{context.get('trace_id', 'TEST')[:6]}] Phantom RPC returned a void result.")
                return []

            except Exception as e:
                Logger.critical(f"[{context.get('trace_id', 'TEST')[:6]}] Phantom Temporal Gateway Fracture: {e}")
                # We fail through to the kinetic logic as a desperate measure.

        # --- MOVEMENT II: KINETIC REALITY (EXTERNAL API) ---
        start_date = datetime.now(timezone.utc).isoformat()
        end_date = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        params = {
            "apiKey": api_key,
            "username": username,
            "eventTypeId": event_slug,
            "startTime": start_date,
            "endTime": end_date
        }

        try:
            with httpx.Client() as client:
                response = client.get(
                    f"{self.BASE_URL}/availability",
                    params=params,
                    timeout=10.0
                )

                if response.status_code != 200:
                    Logger.error(
                        f"[{context.get('trace_id', 'VOID')[:6]}] Cal.com Scry Failed: HTTP {response.status_code} - {response.text[:100]}")
                    raise ArtisanHeresy(f"Cal.com Scry Rejected: Status {response.status_code}", details=response.text)

                data = response.json()
                all_slots = []
                slots_dict = data.get("slots", {})
                for date_key in slots_dict:
                    for slot in slots_dict[date_key]:
                        all_slots.append({"start": slot["time"]})

                return all_slots

        except Exception as e:
            Logger.critical(f"[{context.get('trace_id', 'VOID')[:6]}] Temporal Grid Severed: {e}")
            return []

    def create_booking(self, api_key: str, event_id: Union[int, str], start_time: str, lead_data: Dict,
                       metadata: Dict) -> Dict:
        """
        [THE RITE OF THE ANCHOR - V3.0]
        Physically anchors the meeting in the physical world.
        """
        # [ASCENSION 5]: Multitenant & Trace Suture
        nov_id = metadata.get("novalym_id", "NOV-VOID")
        trace_id = metadata.get("trace_id", "tr-void")

        # [ASCENSION 8]: Fallback Email for Booking
        lead_email_fallback = f"{lead_data.get('phone', 'unlisted')}@novalym.voice"

        payload = {
            "eventTypeId": event_id,
            "start": start_time,
            "responses": {
                "name": lead_data.get("name", "Valued Client"),
                "email": lead_data.get("email", lead_email_fallback),
                "location": "Phone Call - Novalym System",
                "phone": lead_data.get("phone")  # Explicitly pass phone to the booking system
            },
            "metadata": {
                "source": "NOVALYM_KINETIC_KERNEL",
                "lead_phone": lead_data.get("phone"),
                "novalym_id": nov_id,
                "trace_id": trace_id
            },
            "timeZone": lead_data.get("timezone", "UTC")
        }

        try:
            with httpx.Client() as client:
                # [ASCENSION 9]: Correct URL & API Key Suture
                response = client.post(
                    f"{self.BASE_URL}/bookings?apiKey={api_key}",
                    json=payload,
                    timeout=15.0
                )

                if response.status_code >= 400:
                    Logger.error(f"[{trace_id}] Booking Fracture: HTTP {response.status_code} - {response.text[:100]}")
                    # [ASCENSION 4]: Error Transmutation
                    raise ArtisanHeresy(f"Temporal Collision: Status {response.status_code} on booking.",
                                        details=response.text)

                return response.json()
        except Exception as e:
            Logger.error(f"[{trace_id}] Booking Fracture: {e}")
            raise e