# Path: scaffold/artisans/tool/keyring_artisan.py
# -----------------------------------------------
import os
from pathlib import Path
import subprocess
from ...core.artisan import BaseArtisan
from ...interfaces.requests import KeyringRequest
from ...interfaces.base import ScaffoldResult
from ...contracts.heresy_contracts import ArtisanHeresy


class KeyringArtisan(BaseArtisan[KeyringRequest]):
    """
    =============================================================================
    == THE KEEPER OF THE SEALS (GPG KEYRING)                                   ==
    =============================================================================
    Manages the Gnostic Keyring of trusted blueprint authors.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.gnupghome = Path.home() / ".scaffold" / "gnupg"
        self.gnupghome.mkdir(parents=True, exist_ok=True)
        # Set permissions to private
        if os.name != 'nt':
            self.gnupghome.chmod(0o700)

    def execute(self, request: KeyringRequest) -> ScaffoldResult:
        if request.keyring_command == "list":
            return self._list_keys()
        elif request.keyring_command == "add":
            if not request.key_file: return self.failure("A path to a public key file is required.")
            return self._add_key(request.key_file)
        # Future: remove command
        return self.failure("Unknown Keyring rite.")

    def _run_gpg(self, args: list) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["gpg", f"--homedir={self.gnupghome}"] + args,
            capture_output=True, text=True
        )

    def _list_keys(self) -> ScaffoldResult:
        result = self._run_gpg(["--list-keys", "--with-colons"])
        # Parse and display keys
        self.console.print(result.stdout)
        return self.success("Keyring proclaimed.")

    def _add_key(self, key_path: Path) -> ScaffoldResult:
        if not key_path.exists():
            return self.failure(f"Key file not found: {key_path}")
        result = self._run_gpg(["--import", str(key_path)])
        if result.returncode != 0:
            return self.failure(f"Failed to import key: {result.stderr}")
        return self.success("Key has been added to the Gnostic Keyring.")