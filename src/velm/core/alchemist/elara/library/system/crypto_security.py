# Path: core/alchemist/elara/library/system_rites/crypto_security.py
# ------------------------------------------------------------------

import hashlib
import math
import re
import os
import json
from typing import Any, List
from pathlib import Path
from ..registry import register_rite


@register_rite("hash_file")
def hash_physical_matter(value: Any, algo: str = "sha256") -> str:
    """[ASCENSION 80]: Memory Mapped File Suture."""
    p = Path(str(value).strip().strip('"\''))
    if not p.exists() or not p.is_file(): return "0xVOID"

    h = hashlib.new(algo)
    file_size = p.stat().st_size

    # Use mmap for massive files > 100MB
    if file_size > 100 * 1024 * 1024:
        import mmap
        with open(p, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                h.update(mm)
    else:
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()


@register_rite("fingerprint")
def merkle_context_seal(value: Any = None, keys: List[str] = None, **kwargs) -> str:
    ctx = kwargs.get('context', {})
    if not ctx: return "0xVOID"
    target_data = {k: ctx.get(k) for k in keys if k in ctx} if keys else {k: v for k, v in ctx.items() if
                                                                          not k.startswith('__')}
    canonical = json.dumps(target_data, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16].upper()


@register_rite("entropy")
def get_shannon_entropy(value: Any) -> float:
    s = str(value)
    if not s: return 0.0
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])


@register_rite("redact")
def secure_redaction_sieve(value: Any, threshold: float = 4.0) -> str:
    s = str(value)
    if get_shannon_entropy(s) > threshold and len(s) > 16 and " " not in s:
        return f"{s[:4]}...[REDACTED_BY_SOVEREIGN_SIEVE]...{s[-4:]}"
    return s