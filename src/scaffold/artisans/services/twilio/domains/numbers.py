# Path: scaffold/artisans/services/twilio/domains/numbers.py
# ----------------------------------------------------------

import os
from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class NumbersDomain(BaseTwilioDomain):
    """[THE ARCHITECT OF NODES] Handles Search, Buy, Configure, Release."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        if request.action == "search":
            return self._search(request)
        elif request.action == "buy":
            return self._buy(request)
        elif request.action == "configure":
            return self._configure(request)
        elif request.action == "release":
            return self._release(request)
        return self.engine.failure(f"Unknown Number Rite: {request.action}")

    def _search(self, request: TwilioRequest) -> ScaffoldResult:
        country = request.country_code or "US"
        area = request.area_code

        try:
            # Flexible Search: If Area Code fails, maybe we can search Region?
            # For now, strict Area Code or National.
            params = {
                "limit": request.limit or 10,
                "sms_enabled": True,
                "voice_enabled": True
            }
            if area: params["area_code"] = area

            numbers = self.client.available_phone_numbers(country).local.list(**params)

            data = [{"phone_number": n.phone_number, "friendly": n.friendly_name, "lata": n.lata} for n in numbers]
            return self.engine.success(f"Scrying complete. {len(data)} nodes found.", data=data)

        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Search"))

    def _buy(self, request: TwilioRequest) -> ScaffoldResult:
        if not request.phone_number: return self.engine.failure("Buy requires 'phone_number'.")

        gateway = os.environ.get("GATEWAY_URL", "http://localhost:8000")

        try:
            purchased = self.client.incoming_phone_numbers.create(
                phone_number=request.phone_number,
                friendly_name=request.friendly_name or f"NOV-NODE | {request.phone_number}",
                voice_url=request.voice_url or f"{gateway}/v1/ingress/twilio/voice",
                sms_url=request.sms_url or f"{gateway}/v1/ingress/twilio/message"
            )
            return self.engine.success(f"Asset Secured: {purchased.sid}",
                                       data={"sid": purchased.sid, "number": purchased.phone_number})
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Acquisition"))

    def _configure(self, request: TwilioRequest) -> ScaffoldResult:
        # Resolve SID
        sid = request.sid
        if not sid and request.phone_number:
            # Lookup SID by number
            existing = self.client.incoming_phone_numbers.list(phone_number=request.phone_number, limit=1)
            if existing: sid = existing[0].sid

        if not sid: return self.engine.failure("Configure requires 'sid' or 'phone_number'.")

        try:
            updates = {}
            if request.friendly_name: updates["friendly_name"] = request.friendly_name
            if request.voice_url: updates["voice_url"] = request.voice_url
            if request.sms_url: updates["sms_url"] = request.sms_url

            self.client.incoming_phone_numbers(sid).update(**updates)
            return self.engine.success(f"Node {sid} re-tuned.")
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Configuration"))

    def _release(self, request: TwilioRequest) -> ScaffoldResult:
        # Resolve SID logic similar to configure...
        sid = request.sid
        # ... (simplified for brevity)
        if not sid: return self.engine.failure("Release requires SID.")

        try:
            self.client.incoming_phone_numbers(sid).delete()
            return self.engine.success(f"Asset {sid} released.")
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Release"))