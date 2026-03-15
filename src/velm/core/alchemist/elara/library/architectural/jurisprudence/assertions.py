# Path: core/alchemist/elara/library/architectural/jurisprudence/assertions.py
# ----------------------------------------------------------------------------

import uuid
import hashlib
from typing import Any
from ...registry import register_rite

class SchemaViolationHeresy(Exception): pass

@register_rite("uuid")
def validate_uuid(value: Any) -> str:
    """[ASCENSION 45]: Typological Proof. Proves a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return str(value)
    except Exception:
        raise SchemaViolationHeresy(f"Typology Fracture: '{value}' is not a UUID.")

@register_rite("enforce")
def enforce_law(value: Any, law_name: str) -> Any:
    """[ASCENSION 46]: Inline Jurisprudence. Validates against a named Law."""
    if law_name == "no_secrets" and "sk_live" in str(value):
        raise SchemaViolationHeresy("Jurisprudence Breach: Plaintext secret detected in matter.")
    return value

@register_rite("seal")
def finality_seal(value: Any) -> str:
    """[ASCENSION 47]: The Absolute Finality Seal. Merkle-hashes the final matter."""
    return hashlib.sha256(str(value).encode()).hexdigest()