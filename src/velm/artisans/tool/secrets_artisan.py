# Path: scaffold/artisans/tool/secrets_artisan.py
# -----------------------------------------------

import re
import secrets
from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.requests import SecretsRequest
from ...interfaces.base import ScaffoldResult
from ...utils import atomic_write
from rich.prompt import Confirm





class SecretsArtisan(BaseArtisan[SecretsRequest]):
    """
    =============================================================================
    == THE KEYMASTER                                                           ==
    =============================================================================
    Manages the lifecycle of development secrets.
    """

    def execute(self, request: SecretsRequest) -> ScaffoldResult:
        if request.action == "rotate":
            return self._conduct_rotation_rite(request)
        return self.failure("Unknown rite for the Keymaster.")

    def _conduct_rotation_rite(self, request: SecretsRequest) -> ScaffoldResult:
        env_path = self.project_root / request.target
        if not env_path.exists():
            return self.failure(f"The scripture of secrets '{request.target}' is a void.")

        content = env_path.read_text(encoding='utf-8')
        new_content = content
        rotated_keys = []

        # Regex to find secrets and replace their values
        # Looks for keys containing 'SECRET', 'TOKEN', 'KEY', 'PASSWORD'
        secret_pattern = re.compile(
            r"^(?P<key>(?:[A-Z0-9_]+_)?(?:SECRET|TOKEN|KEY|PASSWORD|PASSWD)(?:_[A-Z0-9_]+)?\s*=\s*)(?P<value>.*)$",
            re.MULTILINE | re.IGNORECASE)

        def _replacer(match):
            key_part = match.group('key')
            new_secret = secrets.token_hex(24)  # Forge a new 48-char secret
            rotated_keys.append(key_part.split('=')[0].strip())
            return f"{key_part}{new_secret}"

        new_content, num_subs = secret_pattern.subn(_replacer, content)

        if num_subs == 0:
            return self.success("No recognizable secrets found to rotate.")

        self.console.print(
            f"The Keymaster will rotate [bold yellow]{num_subs}[/bold yellow] secret(s) in [cyan]{request.target}[/cyan]:")
        for key in rotated_keys:
            self.console.print(f"  - {key}")

        if not request.force and not Confirm.ask("\n[bold question]Is this your will?[/bold question]"):
            return self.success("The Rite of Rotation was stayed.")

        atomic_write(env_path, new_content, self.logger, self.project_root)

        return self.success(f"{num_subs} secret(s) have been rotated.")