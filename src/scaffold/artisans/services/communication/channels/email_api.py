import os
import httpx
from .base import BaseCourier
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult


class APICourier(BaseCourier):
    """
    [THE CELESTIAL GATE]
    High-speed HTTP dispatch for modern providers (Resend, SendGrid).
    """

    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        provider = envelope.metadata.get("provider", "resend")

        if provider == "resend":
            return self._dispatch_resend(envelope)
        elif provider == "sendgrid":
            return self._dispatch_sendgrid(envelope)
        else:
            return self.engine.failure(f"Unknown API Provider: {provider}")

    def _dispatch_resend(self, envelope: MessageEnvelope) -> ScaffoldResult:
        key = os.getenv("RESEND_API_KEY")
        if not key: return self.engine.failure("Resend API Key missing.")

        payload = {
            "from": os.getenv("EMAIL_FROM", "onboarding@resend.dev"),
            "to": envelope.to,
            "subject": envelope.subject,
            "html": envelope.body_html,
            "text": envelope.body_text
        }
        if envelope.cc: payload["cc"] = envelope.cc
        if envelope.bcc: payload["bcc"] = envelope.bcc

        try:
            r = httpx.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {key}"},
                json=payload
            )
            r.raise_for_status()
            return self.engine.success("Resend Dispatch Complete", data=r.json())
        except Exception as e:
            return self.engine.failure(f"Resend Fracture: {e}")

    def _dispatch_sendgrid(self, envelope: MessageEnvelope) -> ScaffoldResult:
        # Implementation for SendGrid...
        return self.engine.failure("SendGrid Implementation Pending")