# Path: scaffold/symphony/conductor_core/context/vault.py
# -------------------------------------------------------

import os
import shutil
import subprocess
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.symphony_contracts import SecretSource
from ....logger import Scribe

Logger = Scribe("GnosticVault")


class VaultProvider(ABC):
    """
    The Sacred Contract for a Secret Provider.
    Any entity that wishes to whisper secrets to the Symphony must honor this interface.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The canonical name of the provider (e.g., 'env', '1password')."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the provider's CLI or library is manifest in the mortal realm."""
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Optional[str]:
        """
        The Rite of Retrieval.
        Fetches the secret. Returns None if the key is not found.
        Raises ArtisanHeresy if the retrieval mechanism fails catastrophically.
        """
        pass


class EnvProvider(VaultProvider):
    """
    The Humble Provider. Retrieves secrets from the process environment variables.
    Syntax: @vault("env:MY_SECRET") or @vault("MY_SECRET")
    """

    @property
    def name(self) -> str:
        return "env"

    def is_available(self) -> bool:
        return True  # The environment is always with us.

    def retrieve(self, key: str) -> Optional[str]:
        return os.getenv(key)


class OnePasswordProvider(VaultProvider):
    """
    The 1Password Provider.
    Syntax: @vault("1password:vault_name/item_name/field_name")
            or @vault("op://vault/item/field")
    """

    @property
    def name(self) -> str:
        return "1password"

    def is_available(self) -> bool:
        return shutil.which("op") is not None

    def retrieve(self, key: str) -> Optional[str]:
        # Support both "op://..." syntax and raw path
        reference = key if key.startswith("op://") else f"op://{key}"

        try:
            # We use --no-newline to get the raw secret without whitespace
            result = subprocess.run(
                ["op", "read", reference, "--no-newline"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()
            # If item not found, return None to allow higher-level handling
            if "doesn't exist" in error_msg or "not found" in error_msg:
                return None

            # Otherwise, it's a system failure (auth, network)
            raise ArtisanHeresy(
                f"1Password Retrieval Failed for '{reference}'.",
                details=f"OP CLI Error: {error_msg}",
                suggestion="Ensure you are signed in (`op signin`) and the reference is correct."
            )


class DopplerProvider(VaultProvider):
    """
    The Doppler Provider.
    Syntax: @vault("doppler:MY_SECRET_NAME")
    """

    @property
    def name(self) -> str:
        return "doppler"

    def is_available(self) -> bool:
        return shutil.which("doppler") is not None

    def retrieve(self, key: str) -> Optional[str]:
        try:
            # doppler secrets get MY_SECRET --plain
            result = subprocess.run(
                ["doppler", "secrets", "get", key, "--plain"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            if "Unknown secret" in e.stderr:
                return None

            raise ArtisanHeresy(
                f"Doppler Retrieval Failed for '{key}'.",
                details=f"Doppler CLI Error: {e.stderr.strip()}",
                suggestion="Ensure `doppler login` and `doppler setup` have been conducted."
            )


class AWSSecretsManagerProvider(VaultProvider):
    """
    The AWS Provider.
    Syntax: @vault("aws:secret-id")
    """

    @property
    def name(self) -> str:
        return "aws"

    def is_available(self) -> bool:
        return shutil.which("aws") is not None

    def retrieve(self, key: str) -> Optional[str]:
        # aws secretsmanager get-secret-value --secret-id <key> --query SecretString --output text
        try:
            result = subprocess.run(
                ["aws", "secretsmanager", "get-secret-value", "--secret-id", key, "--query", "SecretString", "--output",
                 "text"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None


class GnosticVault:
    """
    =================================================================================
    == THE KEEPER OF SECRETS (V-Ω-SECURE-STORAGE-PLUGGABLE-CALLABLE)               ==
    =================================================================================
    LIF: 10,000,000,000

    Manages sensitive Gnosis. Ensures secrets are retrieved securely from external
    providers and are never exposed in logs or dumps.

    ### ASCENDED FACULTY #1: THE CALLABLE IDENTITY
    This class now implements `__call__`. This allows it to be accessed as both a
    property (`context.vault.store`) and a method (`context.vault().store`), healing
    the API schism in the Handlers.
    """

    # Heuristic keys that are always treated as secrets even if not in the vault
    SECRET_KEY_PATTERNS = {'password', 'secret', 'token', 'key', 'auth', 'credential', 'private'}

    def __init__(self):
        # The Secure Memory: Stores the *values* of secrets retrieved during this session.
        self._memory: Dict[str, str] = {}

        # The Pantheon of Providers
        self.providers: Dict[str, VaultProvider] = {
            "env": EnvProvider(),
            "1password": OnePasswordProvider(),
            "doppler": DopplerProvider(),
            "aws": AWSSecretsManagerProvider(),
        }

    def __call__(self) -> 'GnosticVault':
        """
        [THE HEALING RITE]
        Allows the Vault instance to be called like a function, returning itself.
        This fixes `context.vault().store(...)`.
        """
        return self

    def resolve_source(self, source: SecretSource) -> str:
        """
        [THE RITE OF RETRIEVAL]
        Fetches the secret from the specified provider.
        """
        provider_key = source.provider.lower()
        secret_key = source.key

        # 1. Select the Specialist
        provider = self.providers.get(provider_key)
        if not provider:
            supported = ", ".join(self.providers.keys())
            raise ArtisanHeresy(
                f"Unknown Secret Provider: '{provider_key}'.",
                suggestion=f"Supported providers: {supported}"
            )

        # 2. Check Availability
        if not provider.is_available():
            raise ArtisanHeresy(
                f"The '{provider.name}' provider is not manifest in this reality.",
                suggestion=f"Install the necessary CLI tool for {provider.name}.",
                severity=HeresySeverity.CRITICAL
            )

        # 3. Retrieve
        Logger.verbose(f"Communing with {provider.name} for secret '{secret_key}'...")
        secret_value = provider.retrieve(secret_key)

        if secret_value is None:
            raise ArtisanHeresy(
                f"The secret '{secret_key}' could not be found in '{provider.name}'.",
                severity=HeresySeverity.CRITICAL
            )

        return secret_value

    def is_secret(self, key: str) -> bool:
        """
        [THE SECRET SENTINEL]
        Determines if a variable key implies a secret value.
        """
        # 1. Is it explicitly in the vault memory?
        if key in self._memory:
            return True

        # 2. Does it look like a secret?
        return any(s in key.lower() for s in self.SECRET_KEY_PATTERNS)

    def store(self, key: str, value: str):
        """
        Explicitly marks a value as a secret in the vault memory.
        This is used when a secret is retrieved and assigned to a variable.
        """
        self._memory[key] = value

    def retrieve_memory(self, key: str) -> Optional[str]:
        """Retrieves a value previously stored in the vault memory."""
        return self._memory.get(key)

    def mask(self, key: str, value: Any) -> str:
        """
        [THE MASKING RITE]
        Returns '******' if the key indicates a secret, otherwise returns the value string.
        """
        if self.is_secret(key):
            return "******"
        return str(value)

    def to_dict(self) -> Dict[str, str]:
        """
        Returns a dictionary representation of the vault for debugging,
        with ALL values redacted.
        """
        return {k: "******" for k in self._memory}

    def __contains__(self, key: str):
        return key in self._memory

    def __len__(self):
        return len(self._memory)

    def __repr__(self):
        return f"<GnosticVault: {len(self._memory)} secrets guarding {', '.join(self.providers.keys())}>"