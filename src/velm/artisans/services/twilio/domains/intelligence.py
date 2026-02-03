# Path: scaffold/artisans/services/twilio/domains/intelligence.py
# ---------------------------------------------------------------

from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class IntelligenceDomain(BaseTwilioDomain):
    """[THE ORACLE] Lookups & Validation."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        target = self.alchemist.normalize_e164(request.phone_number)
        if not target: return self.engine.failure("Lookup requires valid phone_number.")

        try:
            fields = "line_type_intelligence"
            if request.include_name: fields += ",caller_name"
            if request.include_carrier: fields += ",sim_swap"  # Advanced Fraud Check

            lookup = self.client.lookups.v2.phone_numbers(target).fetch(fields=fields)

            data = {
                "number": lookup.phone_number,
                "valid": lookup.valid,
                "type": lookup.line_type_intelligence.get("type", "unknown"),
                "carrier": lookup.line_type_intelligence.get("carrier_name"),
                "mobile_country_code": lookup.line_type_intelligence.get("mobile_country_code"),
                "mobile_network_code": lookup.line_type_intelligence.get("mobile_network_code")
            }

            if request.include_name and lookup.caller_name:
                data["caller_name"] = lookup.caller_name.get("caller_name")
                data["caller_type"] = lookup.caller_name.get("caller_type")

            return self.engine.success(f"Revelation for {target}: {data['type']}", data=data)

        except TwilioRestException as e:
            if e.code == 404: return self.engine.failure("Number does not exist.")
            return self.engine.failure(self.alchemist.transmute_error(e, "Lookup"))