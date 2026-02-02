# Path: scaffold/artisans/services/twilio/domains/lookups.py
# ----------------------------------------------------------

from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class LookupDomain(BaseTwilioDomain):
    """[THE ORACLE OF IDENTITY] HLR and Caller Name lookups."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        target = self.alchemist.normalize_e164(request.phone_number)
        if not target: return self.engine.failure("Lookup requires phone_number.")

        try:
            # We use V2 lookups for better data
            # Fields: line_type_intelligence gives us mobile/landline distinction
            fields = "line_type_intelligence"
            if request.include_name: fields += ",caller_name"

            lookup = self.client.lookups.v2.phone_numbers(target).fetch(fields=fields)

            data = {
                "number": lookup.phone_number,
                "valid": lookup.valid,
                "type": lookup.line_type_intelligence.get("type", "unknown"),
                "carrier": lookup.line_type_intelligence.get("carrier_name"),
                "caller_name": lookup.caller_name.get("caller_name") if lookup.caller_name else None
            }

            return self.engine.success(f"Revelation for {target}: {data['type']}", data=data)

        except TwilioRestException as e:
            if e.code == 404:
                return self.engine.failure("Number does not exist.")
            return self.engine.failure(self.alchemist.transmute_error(e, "Lookup"))