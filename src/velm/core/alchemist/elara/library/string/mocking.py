# Path: core/alchemist/elara/library/string_rites/mocking.py
# ----------------------------------------------------------

import random
import hashlib
import time
import uuid
from typing import Any
from ..registry import register_rite


@register_rite("lorem")
def lorem_rite(value: Any, words: int = 10) -> str:
    """[ASCENSION 18]: Deterministic Lorem Ipsum Generator."""
    lorem_pool = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
        "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
        "et", "dolore", "magna", "aliqua", "ut", "enim", "ad", "minim", "veniam"
    ]
    seed = sum(ord(c) for c in str(value))
    rng = random.Random(seed)

    result = [rng.choice(lorem_pool) for _ in range(int(words))]
    if result: result[0] = result[0].capitalize()
    return " ".join(result) + "."


@register_rite("avatar_url")
def avatar_url_rite(value: Any, provider: str = "gravatar", size: int = 200) -> str:
    """[ASCENSION 19]: The Avatar Forger."""
    email = str(value).strip().lower()
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()

    if provider.lower() == "dicebear":
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={email_hash}&size={size}"
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"


@register_rite("mock_date")
def mock_date_rite(value: Any, tense: str = "past") -> str:
    """[ASCENSION 20]: The Temporal Mocker."""
    seed = sum(ord(c) for c in str(value))
    rng = random.Random(seed)

    now = int(time.time())
    one_year = 31536000

    if tense == "past":
        offset = rng.randint(0, one_year)
        ts = now - offset
    elif tense == "future":
        offset = rng.randint(0, one_year)
        ts = now + offset
    else:
        ts = now

    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


@register_rite("mock")
def mock_rite(value: Any) -> str:
    desc = str(value).lower()
    seed = sum(ord(c) for c in desc)
    rng = random.Random(seed)

    if "uuid" in desc or "id" in desc:
        return str(uuid.UUID(int=rng.getrandbits(128), version=4))
    if "color" in desc or "hex" in desc:
        return f"#{rng.randint(0, 0xFFFFFF):06x}"
    if "name" in desc:
        return rng.choice(["Aria", "Kael", "Lyra", "Orion", "Nova", "Zephyr"])
    if "email" in desc:
        return f"user_{rng.randint(100, 999)}@novalym.systems"

    return "lorem_ipsum_mock_data"