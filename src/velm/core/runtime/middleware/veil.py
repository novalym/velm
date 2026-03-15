# Path: src/velm/core/runtime/middleware/veil.py
# ----------------------------------------------

import os
import re
import math
import time
import uuid
import json
import collections
from typing import Dict, Any, List, Set, Final, Pattern, Tuple, Union, Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("Security:Veil")


class SecretScrubberMiddleware(Middleware):
    """
    =================================================================================
    == THE VEIL OF SILENCE: OMEGA POINT (V-Ω-TOTALITY-V64000-INTENT-AWARE)         ==
    =================================================================================
    LIF: ∞ | ROLE: DATA_LEAK_PREVENTION_ORACLE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_VEIL_V64K_EXAMPLE_AMNESTY_FINALIS_2026
    """

    # --- I. THE CONSTITUTIONAL WHITELIST (AMNESTY) ---
    # These keys are public metadata and are NEVER redacted.
    PUBLIC_GNOSIS_WHITELIST: Final[Set[str]] = {
        'author', 'author_name', 'email', 'author_email', 'project_name',
        'project_slug', 'package_name', 'version', 'description', 'license',
        'project_type', 'clean_type_name', 'timestamp', 'date', 'year',
        'host', 'port', 'user', 'username', 'database', 'db_name',
        'region', 'zone', 'profile', 'trace_id', 'session_id', 'request_id',
        'client_id', 'machine_id', 'os', 'arch', 'python_version',
        'git_branch', 'git_commit', 'image', 'tag', 'repo_url', 'target_dir',
        '__current_dir__', '__current_file__', 'blueprint_path'
    }

    # --- II. THE GNOSTIC EXAMPLE AMNESTY (ASCENSION 25) ---
    # Patterns that mark a string as "Safe for Pedagogy".
    EXAMPLE_AMNESTY_PATTERNS: Final[List[Pattern]] = [
        re.compile(r'(?i)sk_test_[0-9a-zA-Z]{24,}'),  # Stripe Test Keys
        re.compile(r'(?i)pk_test_[0-9a-zA-Z]{24,}'),  # Stripe Public Test Keys
        re.compile(r'(?i).*placeholder.*'),  # Explicit placeholders
        re.compile(r'(?i).*example.*'),  # Explicit examples
        re.compile(r'(?i).*dummy.*'),  # Explicit dummies
        re.compile(r'(?i)your_.*_here'),  # "your_key_here"
        re.compile(r'^sk-[a-zA-Z0-9]{10}T[a-zA-Z0-9]{37}$'),  # Mocked OpenAI format
        re.compile(r'^0x[0]{10,}.*$'),  # Null addresses
    ]

    # --- III. THE PROFANE BLACKLIST (TARGETS) ---
    SECRET_KEY_ROOTS: Final[Set[str]] = {
        'api_key', 'secret', 'password', 'token', 'credential', 'private_key',
        'auth_token', 'jwt', 'access_key', 'pass', 'passwd', 'db_password',
        'client_secret', 'ssh_key', 'salt', 'nonce', 'cert', 'signature'
    }

    # --- IV. THE CLOUD SIGNATURE CODEX ---
    CLOUD_SIGNATURES: Final[List[Tuple[str, Pattern]]] = [
        ("AWS Access Key", re.compile(r'(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}')),
        ("Stripe Secret", re.compile(r'(sk_live_[0-9a-zA-Z]{24,})')),
        ("GitHub Token", re.compile(r'(gh[pousr]_[a-zA-Z0-9]{36,})')),
        ("Google API Key", re.compile(r'AIza[0-9A-Za-z\\-_]{35}')),
        ("Slack Token", re.compile(r'xox[baprs]-([0-9a-zA-Z]{10,48})')),
        ("OpenAI Key", re.compile(r'sk-[a-zA-Z0-9]{48}')),
        ("SSH Private Key", re.compile(r'-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----')),
        ("JWT", re.compile(r'eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+')),
    ]

    # --- V. PHYSICS CONSTANTS ---
    ENTROPY_THRESHOLD: Final[float] = 4.2
    STRICT_ENTROPY_THRESHOLD: Final[float] = 3.8
    MIN_SECRET_LENGTH: Final[int] = 12

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._strict_mode = os.environ.get("SCAFFOLD_ENV") == "production"
        self._entropy_cache: Dict[str, float] = collections.OrderedDict()
        self._cache_limit = 2000

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """The Rite of Perimeter Security."""

        # 1. Fast Path
        if not request.variables:
            return next_handler(request)

        # 2. Adrenaline Check: Mute GC for heavy scan if needed
        is_heavy = len(request.variables) > 50

        # 3. The Semantic Inquest
        scrubbed_vars, secrets_found = self._scrub_recursive(request.variables, path="root")

        # 4. The BICAMERAL VAULTING (Teleportation)
        if secrets_found:
            # We update the public variables with the redacted markers
            request.variables = scrubbed_vars

            # We move the truth to the secure vault
            for secret_path, secret_val in secrets_found.items():
                key = secret_path.split('.')[-1]
                request.secrets[key] = secret_val

            if not getattr(request, 'silent', False):
                Logger.info(f"🛡️  The Veil secured {len(secrets_found)} secret(s). [Gnostic Amnesty Applied]")

            # Forensic Trace Injection
            if not hasattr(request, 'metadata'): request.metadata = {}
            request.metadata['_veil_report'] = {
                "secured_count": len(secrets_found),
                "timestamp": time.time(),
                "trace": getattr(request, 'trace_id', 'void')
            }

        return next_handler(request)

    def _scrub_recursive(self, data: Any, path: str) -> Tuple[Any, Dict[str, str]]:
        """Deep-scans nested structures."""
        secrets_found = {}

        # --- CASE I: DICTIONARY (THE HUB) ---
        if isinstance(data, dict):
            clean_dict = {}
            for k, v in data.items():
                key_str = str(k).lower()
                key_path = f"{path}.{k}"

                # 1. [ASCENSION 22]: ENGINE INTERNAL WARD
                if k.startswith('__') and k.endswith('__'):
                    clean_dict[k] = v
                    continue

                # 2. [ASCENSION 26]: SOVEREIGN INTENT BYPASS
                # Keys starting with 'public_' or 'example_' get total amnesty.
                if k.startswith(('public_', 'example_', 'test_', 'dummy_')):
                    clean_dict[k] = v
                    continue

                # 3. [ASCENSION 1]: CONSTITUTIONAL WHITELIST
                if k in self.PUBLIC_GNOSIS_WHITELIST:
                    clean_dict[k] = v
                    continue

                # 4. RECURSE OR SCAN
                if isinstance(v, (dict, list)):
                    clean_val, sub_secrets = self._scrub_recursive(v, key_path)
                    clean_dict[k] = clean_val
                    secrets_found.update(sub_secrets)
                else:
                    # Leaf Node (Primitive)
                    is_blacklisted_key = self._is_blacklisted_key(key_str)

                    # [ASCENSION 25]: GNOSTIC EXAMPLE AMNESTY
                    # We check the value for example markers even if the key is blacklisted.
                    if is_blacklisted_key and not self._is_example_matter(v):
                        val_str = str(v)
                        if val_str and val_str not in ("None", "False", "0", ""):
                            secrets_found[key_path] = val_str
                            clean_dict[k] = "[REDACTED_BY_VEIL]"
                        else:
                            clean_dict[k] = v
                    else:
                        # Key is safe or value is an example, but conduct content scan for accidental leaks.
                        scrubbed_val, content_secret = self._scan_content_safety(v, key_path)
                        clean_dict[k] = scrubbed_val
                        if content_secret:
                            secrets_found[key_path] = content_secret

            return clean_dict, secrets_found

        # --- CASE II: LIST (THE MANIFOLD) ---
        elif isinstance(data, (list, tuple, set)):
            clean_list = []
            for idx, item in enumerate(data):
                clean_item, sub_secrets = self._scrub_recursive(item, f"{path}[{idx}]")
                clean_list.append(clean_item)
                secrets_found.update(sub_secrets)

            # Preserve original collection type
            if isinstance(data, tuple): return tuple(clean_list), secrets_found
            if isinstance(data, set): return set(clean_list), secrets_found
            return clean_list, secrets_found

        # --- CASE III: PYDANTIC OBJECTS (ASCENSION 26) ---
        elif hasattr(data, 'model_dump'):
            # Transmute to dict and scan, then we leave it as a dict to prevent Pydantic
            # validation errors on the '[REDACTED]' strings.
            return self._scrub_recursive(data.model_dump(), path)

        # --- CASE IV: PRIMITIVES ---
        else:
            return data, {}

    def _scan_content_safety(self, value: Any, path: str) -> Tuple[Any, Optional[str]]:
        """Scans primitive values for high-entropy secrets."""
        if not isinstance(value, str) or len(value) < self.MIN_SECRET_LENGTH:
            return value, None

        # [ASCENSION 33]: SGF IMMUNITY
        if "{{" in value or "{%" in value:
            return value, None

        # [ASCENSION 34]: UUID AMNESTY
        if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', value.lower()):
            return value, None

        # [ASCENSION 35]: PATH AMNESTY
        if value.startswith(('/', './', '../', 'C:\\')):
            return value, None

        # [ASCENSION 25]: EXAMPLE VALUE AMNESTY
        if self._is_example_matter(value):
            return value, None

        # 1. Cloud Signature Scan
        for sig_name, pattern in self.CLOUD_SIGNATURES:
            if pattern.search(value):
                return f"[REDACTED_{sig_name.upper().replace(' ', '_')}]", value

        # 2. Shannon Entropy Tomography
        if self._is_high_entropy(value):
            return "[REDACTED_HIGH_ENTROPY]", value

        # 3. Connection String Dissection
        if "://" in value and "@" in value:
            clean_url = self._dissect_url(value)
            if clean_url != value:
                return clean_url, value

        return value, None

    def _is_example_matter(self, value: Any) -> bool:
        """Determines if a string is a placeholder or common test artifact."""
        val_str = str(value)
        # Fast fail for short strings
        if len(val_str) < 5: return False
        return any(pattern.search(val_str) for pattern in self.EXAMPLE_AMNESTY_PATTERNS)

    def _is_blacklisted_key(self, key: str) -> bool:
        """Checks if a key name implies secret intent."""
        normalized = key.replace('_', '').replace('-', '').lower()
        return any(root in normalized for root in self.SECRET_KEY_ROOTS)

    def _is_high_entropy(self, text: str) -> bool:
        """[ASCENSION 4]: SHANNON ENTROPY TOMOGRAPHY."""
        # Secrets rarely have spaces or newlines.
        if ' ' in text or '\n' in text: return False

        # Check Cache
        if text in self._entropy_cache:
            entropy = self._entropy_cache[text]
        else:
            # MATH: Calculate Shannon Entropy
            # H(x) = -Sum(P(x) * log2(P(x)))
            prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
            entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

            # Cache rotation
            if len(self._entropy_cache) > self._cache_limit:
                self._entropy_cache.popitem()
            self._entropy_cache[text] = entropy

        threshold = self.STRICT_ENTROPY_THRESHOLD if self._strict_mode else self.ENTROPY_THRESHOLD
        return entropy > threshold

    def _dissect_url(self, url: str) -> str:
        """Surgically extracts passwords from connection URIs."""
        # group 1: protocol://user:
        # group 2: password
        # group 3: @host...
        pattern = r'([a-zA-Z0-9\+\-\.]+\:\/\/[^/:]+:)([^@]+)(@.+)'
        match = re.match(pattern, url)
        if match:
            return f"{match.group(1)}[REDACTED_BY_VAULT_SUTURE]{match.group(3)}"
        return url

    def __repr__(self) -> str:
        return f"<Ω_SECRET_VEIL status=VIGILANT mode={'STRICT' if self._strict_mode else 'RESONANT'}>"