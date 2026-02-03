# scaffold/semantic_injection/directives/crypto_domain.py

"""
=================================================================================
== THE ALCHEMIST OF ENTROPY (V-Ω-CRYPTO-DOMAIN)                                ==
=================================================================================
LIF: 1,000,000,000

This artisan implements the `@crypto` namespace. It generates cryptographically
secure strings for secrets, passwords, and unique identifiers.

Usage:
    secrets.env :: JWT_SECRET=@crypto/random(64)
    config.json :: "id": "@crypto/uuid"
    admin_creds :: @crypto/password(24)
=================================================================================
"""
import secrets
import string
import uuid
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("crypto")
class CryptoDomain(BaseDirectiveDomain):
    """
    The Forge of Unique & Secure Things.
    """

    @property
    def namespace(self) -> str:
        return "crypto"

    def help(self) -> str:
        return "Generates secure secrets (random hex, uuid, base64, complex passwords)."

    # =========================================================================
    # == THE RITES OF CHAOS                                                  ==
    # =========================================================================

    def _directive_random(self, context: Dict[str, Any], length: int = 32, *args, **kwargs) -> str:
        """
        @crypto/random(length=32)
        Forges a random hexadecimal string of *byte* length (actual char length is 2x).
        Great for API keys and simple tokens.
        """
        try:
            l = int(length)
        except ValueError:
            l = 32
        return secrets.token_hex(l)

    def _directive_hex(self, context: Dict[str, Any], length: int = 32, *args, **kwargs) -> str:
        """
        @crypto/hex(length=32)
        Alias for @crypto/random.
        """
        return self._directive_random(context, length)

    def _directive_uuid(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @crypto/uuid
        Forges a standard UUID v4.
        """
        return str(uuid.uuid4())

    def _directive_base64(self, context: Dict[str, Any], length: int = 32, *args, **kwargs) -> str:
        """
        @crypto/base64(length=32)
        Forges a URL-safe base64 string.
        Great for web tokens where hex is too verbose.
        """
        try:
            l = int(length)
        except ValueError:
            l = 32
        return secrets.token_urlsafe(l)

    def _directive_password(self, context: Dict[str, Any], length: int = 24, special: bool = True, *args,
                            **kwargs) -> str:
        """
        @crypto/password(length=24, special=true)
        Forges a complex password containing uppercase, lowercase, digits, and symbols.
        """
        try:
            l = int(length)
        except ValueError:
            l = 24

        # Define the chaos pool
        alphabet = string.ascii_letters + string.digits
        if str(special).lower() in ('true', '1', 'yes'):
            alphabet += "!@#$%^&*()-_=+"

        # The Rite of Assembly: Ensure at least one of each if special is on
        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(l))
            if str(special).lower() not in ('true', '1', 'yes'):
                return password

            # Validation for complex passwords
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(c.isdigit() for c in password)
                    and any(c in "!@#$%^&*()-_=+" for c in password)):
                return password