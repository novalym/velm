# Path: scaffold/artisans/services/twilio/domains/messaging.py
# ------------------------------------------------------------

import os
from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest
from ..utils import TelephonicPhysics


class MessagingDomain(BaseTwilioDomain):
    """[THE KINETIC ARM] SMS/MMS/Scheduling."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        # 1. Purify
        to_number = self.alchemist.normalize_e164(request.to_number or request.recipient)
        if not to_number: return self.engine.failure("Messaging Void: 'to_number' required.")

        # 2. Origin Resolution
        from_number = request.from_number or os.environ.get("TWILIO_FROM_NUMBER")
        mg_sid = request.messaging_service_sid or os.environ.get("TWILIO_MESSAGING_SERVICE_SID")

        params = {"to": to_number, "body": request.body or request.content}

        if mg_sid:
            params["messaging_service_sid"] = mg_sid
        elif from_number:
            params["from_"] = from_number
        else:
            return self.engine.failure("Messaging Void: No Sender Identity defined.")

        # 3. Media
        if request.media_url:
            params["media_url"] = request.media_url if isinstance(request.media_url, list) else [request.media_url]

        # 4. Scheduling (The Chronomancer)
        if request.send_at:
            if not mg_sid: return self.engine.failure("Scheduling requires Messaging Service SID.")
            params["schedule_type"] = "fixed"
            params["send_at"] = request.send_at
            # Validity period logic for scheduled messages? Twilio defaults are usually fine.

        # 5. Status Callback
        gateway = os.environ.get("GATEWAY_URL", "http://localhost:8000")
        params["status_callback"] = f"{gateway}/v1/ingress/twilio/status"

        # 6. Physics Check (Cost Estimation)
        segs, encoding = TelephonicPhysics.calculate_segments(params.get("body", ""))

        try:
            msg = self.client.messages.create(**params)

            return self.engine.success(
                f"Signal Manifest: {msg.sid}",
                data={
                    "sid": msg.sid,
                    "status": msg.status,
                    "segments": msg.num_segments,
                    "estimated_segments": segs,
                    "encoding": encoding,
                    "price": msg.price,
                    "unit": msg.price_unit,
                    "scheduled": bool(request.send_at)
                }
            )
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Messaging"))