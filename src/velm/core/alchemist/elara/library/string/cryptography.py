# Path: core/alchemist/elara/library/string_rites/cryptography.py
# ---------------------------------------------------------------

import base64
import hashlib
import math
import re
from typing import Any, Optional
from ..registry import register_rite

RE_PII_EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


@register_rite("entropy")
def get_shannon_entropy(value: Any) -> float:
    s = str(value)
    if not s: return 0.0
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])


@register_rite("redact")
def redact_secrets(value: Any, pattern: Optional[str] = None) -> str:
    """[ASCENSION 9]: Custom Regex Redaction."""
    s = str(value)
    if not s: return ""

    if pattern:
        try:
            return re.sub(str(pattern), "[REDACTED]", s)
        except Exception:
            pass

    entropy = get_shannon_entropy(s)
    is_secret = (entropy > 4.5 and len(s) > 16 and " " not in s)
    if is_secret: return f"{s[:4]}...[REDACTED_BY_SCAFFOLD]...{s[-4:]}"
    return s


@register_rite("scrub")
def scrub_pii(value: Any) -> str:
    s = str(value)
    s = RE_PII_EMAIL.sub("[EMAIL_REDACTED]", s)
    s = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', "[PHONE_REDACTED]", s)
    return s


@register_rite("b64_encode")
def b64_encode(value: Any, url_safe: bool = False) -> str:
    s = value.encode('utf-8') if isinstance(value, str) else str(value).encode('utf-8')
    if url_safe: return base64.urlsafe_b64encode(s).decode('utf-8').rstrip('=')
    return base64.b64encode(s).decode('utf-8')


@register_rite("b64_decode")
def b64_decode(value: Any, url_safe: bool = False) -> str:
    try:
        s = str(value)
        if url_safe: return base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4)).decode('utf-8')
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return "[DECODE_FRACTURE]"


@register_rite("hash")
def hash_rite(value: Any, algo: str = "sha256") -> str:
    """[ASCENSION 10]: Multi-Algorithm Merkle Hashing."""
    try:
        data = str(value).encode('utf-8')
        return hashlib.new(algo.lower(), data).hexdigest()
    except ValueError:
        return hashlib.sha256(data).hexdigest()