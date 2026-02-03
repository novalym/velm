# Path: scaffold/artisans/services/twilio/domains/management.py
# -------------------------------------------------------------

from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class ManagementDomain(BaseTwilioDomain):
    """[THE NODE TUNER] Config & Release."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        if request.action == "configure": return self._configure(request)
        if request.action == "release": return self._release(request)
        return self.engine.failure(f"Unknown Management Rite: {request.action}")

    def _resolve_sid(self, request: TwilioRequest) -> str:
        if request.sid: return request.sid
        if request.phone_number:
            existing = self.client.incoming_phone_numbers.list(phone_number=request.phone_number, limit=1)
            if existing: return existing[0].sid
        return None

    def _configure(self, request: TwilioRequest) -> ScaffoldResult:
        sid = self._resolve_sid(request)
        if not sid: return self.engine.failure("Configuration requires SID or Number.")

        try:
            updates = {}
            if request.friendly_name: updates["friendly_name"] = request.friendly_name
            if request.voice_url: updates["voice_url"] = request.voice_url
            if request.sms_url: updates["sms_url"] = request.sms_url
            if request.status_callback: updates["status_callback"] = request.status_callback

            self.client.incoming_phone_numbers(sid).update(**updates)
            return self.engine.success(f"Node {sid} re-tuned.")
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Configuration"))

    def _release(self, request: TwilioRequest) -> ScaffoldResult:
        sid = self._resolve_sid(request)
        if not sid: return self.engine.success("Node already dissolved (Not found).")

        try:
            self.client.incoming_phone_numbers(sid).delete()
            return self.engine.success(f"Asset {sid} returned to the void.")
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Release"))