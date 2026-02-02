import hmac
import hashlib
import json
import httpx
from typing import Any
from ...client import GlobalConnectionPool
from .....contracts.heresy_contracts import ArtisanHeresy


class WebhookEmitter:
    """
    [THE SIGNAL EMITTER]
    Sends cryptographically signed payloads to external systems.
    Essential for secure server-to-server notifications.
    """

    def execute(self, request) -> Any:
        client = GlobalConnectionPool.get_client()
        payload = request.json_body or {}

        headers = request.headers.copy()

        # The Rite of Signing
        if request.secret:
            signature = self._sign_payload(payload, request.secret)
            headers[request.signature_header] = signature

        try:
            response = client.post(
                url=request.url,
                headers=headers,
                json=payload,
                timeout=request.timeout
            )

            return {
                "success": not response.is_error,
                "status": response.status_code,
                "response": response.text
            }
        except Exception as e:
            raise ArtisanHeresy(f"Webhook Emission Failed: {e}")

    def _sign_payload(self, payload: Dict, secret: str) -> str:
        """Forges an HMAC-SHA256 signature of the payload."""
        payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        secret_bytes = secret.encode('utf-8')

        signature = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
        return f"sha256={signature}"