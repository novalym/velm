import json
import urllib.request
import urllib.error
from typing import Tuple
from .base import BaseVowHandler


class HttpVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF THE WEB (HTTP/API)                                        ==
    =============================================================================
    Judges the responsiveness and content of remote or local HTTP services.
    Essential for validating `docker-compose` startups or API deployment.
    """

    def _make_request(self, url: str, method: str = "GET") -> Tuple[int, str, dict]:
        """Internal helper."""
        req = urllib.request.Request(url, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                body = response.read().decode('utf-8')
                return response.status, body, response.headers
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8'), e.headers
        except Exception as e:
            return 0, str(e), {}

    def _vow_http_status_is(self, url: str, status_code: str) -> Tuple[bool, str]:
        """Asserts an endpoint returns a specific status code (e.g., 200)."""
        code, _, _ = self._make_request(url)
        target = int(status_code)
        return code == target, f"URL returned {code} (Expected {target})."

    def _vow_http_body_contains(self, url: str, text: str) -> Tuple[bool, str]:
        """Asserts the response body contains a string."""
        code, body, _ = self._make_request(url)
        if code == 0: return False, f"Connection failed: {body}"
        return text in body, f"Response {'contains' if text in body else 'lacks'} '{text}'."

    def _vow_http_is_json(self, url: str) -> Tuple[bool, str]:
        """Asserts the response is valid JSON."""
        code, body, _ = self._make_request(url)
        if code == 0: return False, "Connection failed."
        try:
            json.loads(body)
            return True, "Response is valid JSON."
        except:
            return False, "Response is not JSON."

    def _vow_http_header_equals(self, url: str, header: str, value: str) -> Tuple[bool, str]:
        """Asserts a specific header matches."""
        code, _, headers = self._make_request(url)
        if code == 0: return False, "Connection failed."

        actual = headers.get(header, "")
        return actual == value, f"Header '{header}' is '{actual}'."

    def _vow_http_is_https(self, url: str) -> Tuple[bool, str]:
        """Asserts the URL uses a secure transport."""
        return url.startswith("https://"), f"URL scheme is {'https' if url.startswith('https') else 'insecure'}."
