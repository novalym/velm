# Path: scaffold/artisans/services/twilio/domains/provisioning.py
# ---------------------------------------------------------------

import os
from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class ProvisioningDomain(BaseTwilioDomain):
    """[THE ASSET HUNTER] Search & Acquisition."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        if request.action == "search": return self._search(request)
        if request.action == "buy": return self._buy(request)
        return self.engine.failure(f"Unknown Provisioning Rite: {request.action}")

    def _search(self, request: TwilioRequest) -> ScaffoldResult:
        country = request.country_code or "US"

        # Build Filter
        params = {
            "limit": request.limit or 20,
            "sms_enabled": request.sms_enabled,
            "voice_enabled": request.voice_enabled,
            "mms_enabled": request.mms_enabled
        }

        if request.area_code: params["area_code"] = request.area_code
        if request.contains: params["contains"] = request.contains  # Vanity Search

        try:
            # Polymorphic Search (Local vs TollFree vs Mobile)
            # Defaulting to Local for now, could expand based on request.type
            numbers = self.client.available_phone_numbers(country).local.list(**params)

            data = [{
                "phone_number": n.phone_number,
                "friendly": n.friendly_name,
                "lata": n.lata,
                "locality": n.locality,
                "region": n.region,
                "postal_code": n.postal_code
            } for n in numbers]

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
            return self.engine.success(
                f"Asset Secured: {purchased.sid}",
                data={
                    "sid": purchased.sid,
                    "number": purchased.phone_number,
                    "capabilities": purchased.capabilities
                }
            )
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Acquisition"))