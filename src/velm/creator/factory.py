# Path: scaffold/creator/factory.py
# ---------------------------------

from pathlib import Path
from typing import Union

from ..core.sanctum.base import SanctumInterface
from ..core.sanctum.local import LocalSanctum
from ..core.sanctum.memory import MemorySanctum
from ..core.sanctum.s3 import S3Sanctum
from ..core.sanctum.ssh import SSHSanctum


def forge_sanctum(target: Union[str, Path]) -> SanctumInterface:
    """
    =================================================================================
    == THE SANCTUM FACTORY (V-Ω-REALITY-ROUTER)                                    ==
    =================================================================================
    The Gateway to all Realities.
    Parses the target string and summons the correct Sanctum Artisan.

    Schemas:
    - /local/path         -> LocalSanctum
    - .                   -> LocalSanctum (CWD)
    - ssh://user@host...  -> SSHSanctum
    - s3://bucket/prefix  -> S3Sanctum
    - memory://           -> MemorySanctum (Ephemeral)
    """
    target_str = str(target)

    if target_str.startswith("memory://"):
        return MemorySanctum()

    if target_str.startswith("s3://"):
        # Parse s3://bucket/prefix
        parts = target_str[5:].split("/", 1)
        bucket = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""
        # Future: Extract region/profile from query params if needed (s3://...?region=us-west-1)
        return S3Sanctum(bucket=bucket, prefix=prefix)

    if target_str.startswith("ssh://"):
        return SSHSanctum(connection_string=target_str)

    # Fallback: Mortal Realm
    return LocalSanctum(root=Path(target))