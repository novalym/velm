import httpx
import time
from typing import Any, Dict
from ...client import GlobalConnectionPool
from .....contracts.heresy_contracts import ArtisanHeresy


class RestEngine:
    """[THE REST WEAVER] Handles standard HTTP interactions."""

    def execute(self, request) -> Any:
        client = GlobalConnectionPool.get_client()

        # 1. Prepare Headers & Auth
        headers = request.headers.copy()
        if request.auth:
            self._inject_auth(headers, request.auth)

        # 2. The Rite of Transmission (With Retries)
        attempts = 0
        max_attempts = max(1, request.retries + 1)
        last_error = None

        while attempts < max_attempts:
            try:
                response = client.request(
                    method=request.method,
                    url=request.url,
                    headers=headers,
                    params=request.params,
                    json=request.json_body,
                    data=request.data,
                    timeout=request.timeout
                )

                # Success Logic
                if not response.is_error:
                    try:
                        return response.json()
                    except:
                        return response.text

                # Server Error -> Retry
                if response.status_code >= 500:
                    raise httpx.HTTPStatusError("Server Error", request=response.request, response=response)

                # Client Error -> Fail Immediately
                return {
                    "error": True,
                    "status": response.status_code,
                    "body": response.text
                }

            except httpx.RequestError as e:
                last_error = e
            except httpx.HTTPStatusError as e:
                last_error = e

            attempts += 1
            if attempts < max_attempts:
                time.sleep(0.5 * (2 ** (attempts - 1)))  # Exponential Backoff

        raise ArtisanHeresy(f"Network Rite Failed after {attempts} attempts: {last_error}")

    def _inject_auth(self, headers: Dict[str, str], auth: Dict[str, str]):
        auth_type = auth.get('type', '').lower()
        if auth_type == 'bearer':
            headers['Authorization'] = f"Bearer {auth.get('token')}"
        elif auth_type == 'api_key':
            key_name = auth.get('key', 'X-API-Key')
            headers[key_name] = auth.get('value')
        elif auth_type == 'basic':
            # httpx handles basic auth better via the 'auth' arg, but we can do headers manually
            import base64
            creds = f"{auth.get('user')}:{auth.get('pass')}"
            b64_creds = base64.b64encode(creds.encode()).decode()
            headers['Authorization'] = f"Basic {b64_creds}"

