# Path: scaffold/artisans/with_secrets.py
# ---------------------------------------

import os
import shlex
from typing import Dict, List

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import WithSecretsRequest
from ..help_registry import register_artisan
from ..contracts.heresy_contracts import ArtisanHeresy
from ..contracts.symphony_contracts import SecretSource
from ..symphony.execution import KineticTitan


@register_artisan("with")
class WithSecretsArtisan(BaseArtisan[WithSecretsRequest]):
    """
    =============================================================================
    == THE EPHEMERAL VAULT (V-Ω-SECURE-EXECUTION-CONTEXT)                      ==
    =============================================================================
    LIF: ∞ (ABSOLUTE SECURITY)

    Creates a temporary, in-memory sanctum of secrets, executes a command within
    that reality, and then annihilates all traces of the secrets.
    """

    def execute(self, request: WithSecretsRequest) -> ScaffoldResult:
        self.logger.info(f"The Ephemeral Vault opens. Summoning secrets from [cyan]{request.provider}[/cyan]...")

        # 1. Summon the Gnostic Vault
        # We must use the vault from the Symphony context as it is the most complete.
        from ..symphony.conductor_core.context.vault import GnosticVault
        vault = GnosticVault()

        # 2. Forge the Ephemeral Environment
        env_overrides: Dict[str, str] = {}

        with self.console.status("[bold magenta]Retrieving Gnostic secrets...[/bold magenta]"):
            for secret_ref in request.secrets:
                # The secret reference itself might contain the provider override
                # e.g., "op://vault/item" vs "doppler:API_KEY"
                provider, key = self._parse_secret_ref(secret_ref, request.provider)

                # Forge a SecretSource vessel to make the plea
                source = SecretSource(provider=provider, key=key)

                # Retrieve the secret
                secret_value = vault.resolve_source(source)

                # The secret's key in the environment is the final part of the reference
                env_key = key.split('/')[-1].upper()
                env_overrides[env_key] = secret_value

                self.logger.verbose(f"Secret '{key}' retrieved and mapped to env var '{env_key}'.")

        # 3. Prepare the Kinetic Rite
        command_list = request.command
        if not command_list:
            return self.failure("No command provided to execute.")

        # We must reconstruct the command string for the KineticTitan's shell execution
        command_str = " ".join(shlex.quote(arg) for arg in command_list)

        self.logger.info(f"Executing rite within the Ephemeral Vault: [yellow]$ {command_str}[/yellow]")

        # 4. The Divine Delegation to the Titan
        # The KineticTitan is the raw, physical hand. It takes a full command string.
        # We summon it directly for this low-level, high-security operation.
        titan = KineticTitan()

        # We conduct the rite, passing the ephemeral secrets via `env_overrides`.
        # The result contains the exit code and full output.
        # We use verbose_ui=False to get a raw stream, and a simple callback to print it.
        result = titan.perform(
            command=command_str,
            edict=None,  # No edict context needed for this raw rite
            sanctum=self.project_root,
            inputs=[],
            live_context=None,
            stream_callback=lambda ctx, line: print(line, end=''),
            verbose_ui=False,  # Use raw streaming
            env_overrides=env_overrides
        )

        if result.returncode == 0:
            return self.success("The rite was conducted successfully within the Ephemeral Vault.")
        else:
            # We must not leak the secret environment in the failure message.
            # The output, however, is necessary for debugging.
            raise ArtisanHeresy(
                f"The rite failed with exit code {result.returncode}.",
                details=f"Output:\n{result.output}"
            )

    def _parse_secret_ref(self, ref: str, default_provider: str) -> tuple[str, str]:
        """Parses 'provider:key' or 'op://...' syntax."""
        if ref.startswith("op://"):
            return "1password", ref

        if ":" in ref:
            parts = ref.split(":", 1)
            # Check if the first part is a known provider
            known_providers = ["1password", "doppler", "aws", "env"]
            if parts[0] in known_providers:
                return parts[0], parts[1]

        return default_provider, ref