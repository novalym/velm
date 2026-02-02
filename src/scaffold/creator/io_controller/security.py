# Path: scaffold/creator/io_controller/security.py
import re
from pathlib import Path
from typing import Union

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("SecurityWards")

class SecurityWards:
    """
    =================================================================================
    == THE CITADEL OF SECURITY (V-Ω-UNBREAKABLE-WARD)                              ==
    =================================================================================
    The unified command center for all I/O security adjudication. It houses the
    PathSentinel and the ResourceQuotaWard, forming an unbreakable shield around
    the mortal realm of the filesystem.
    =================================================================================
    """

    # --- THE PATH SENTINEL'S GRIMOIRE ---
    FORBIDDEN_NAMES = {'.git', '.hg', '.svn', '.DS_Store', 'Thumbs.db'}
    TRAVERSAL_REGEX = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    def adjudicate_path(self, logical_path: Union[str, Path]) -> str:
        """
        The Rite of Path Adjudication. Enforces the Law of Containment.
        Raises Heresy if the path is profane. Returns the pure, normalized path.
        """
        path_str = str(logical_path)
        clean_path = path_str.replace('\\', '/')

        if not clean_path or clean_path.strip() == '.':
            return ""

        if self.TRAVERSAL_REGEX.search(clean_path):
            raise ArtisanHeresy(
                f"Security Heresy: Path Traversal detected in '{path_str}'.",
                suggestion="All paths must be relative. '..' is forbidden."
            )

        if Path(clean_path).is_absolute() or re.match(r'^[a-zA-Z]:', clean_path):
            raise ArtisanHeresy(
                f"Security Heresy: Absolute path detected in '{path_str}'.",
                suggestion="Paths must be relative to the Sanctum."
            )

        parts = clean_path.split('/')
        for part in parts:
            if part in self.FORBIDDEN_NAMES:
                Logger.warn(f"Accessing sensitive artifact '{part}' in path '{clean_path}'.")

        return clean_path

    def verify_resource_quota(self, content: Union[str, bytes], limit_mb: int = 50):
        """
        The Ward of Gluttony. Prevents inscription of oversized artifacts.
        """
        size_bytes = len(content)
        limit_bytes = limit_mb * 1024 * 1024

        if size_bytes > limit_bytes:
            raise ArtisanHeresy(
                f"Resource Quota Exceeded: Payload is {size_bytes} bytes (Limit: {limit_bytes}).",
                suggestion="Use a reference to an external asset (`<<`) instead of embedding massive files."
            )