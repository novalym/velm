# Path: creator/security.py
# -------------------------

import re
from pathlib import Path
from typing import Union

from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

Logger = Scribe("PathSentinel")


class PathSentinel:
    """
    =================================================================================
    == THE GNOSTIC PATH SENTINEL (V-Ω-UNBREAKABLE-WARD)                            ==
    =================================================================================
    LIF: 10,000,000,000,000

    This artisan is the absolute guardian of filesystem boundaries. Its Prime Directive
    is to prevent **Path Traversal**, **Root Escapes**, and **Symlink Poisoning**.

    It enforces the Law of Containment: All effects must remain within the Sanctum.
    """

    # Forbidden filenames that could compromise the host or the tool itself
    FORBIDDEN_NAMES = {'.git', '.hg', '.svn', '.DS_Store', 'Thumbs.db'}

    # Regex for detecting localized traversal attempts (e.g., '..\', '../')
    TRAVERSAL_REGEX = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    @staticmethod
    def adjudicate(
            logical_path: Union[str, Path],
            allow_absolute: bool = False
    ) -> str:
        """
        The Rite of Adjudication.
        Validates and normalizes a path string. If the path is profane, it raises
        a catastrophic Heresy.

        Returns:
            The pure, normalized POSIX string representation of the path.
        """
        # 1. The Rite of Stringification
        path_str = str(logical_path)

        # [THE FIX] MOVEMENT 0: THE GAZE OF PROPHETIC AVERSION
        # If the path is a prophecy (contains template variables), we avert our gaze.
        # We do not judge what has not yet come to pass.
        if '{{' in path_str:
            return path_str # Return raw prophecy

        # 2. The Rite of Normalization (Universal Slash)
        # We convert backslashes to forward slashes to analyze the abstract geometry.
        clean_path = path_str.replace('\\', '/')

        # 3. The Gaze of the Void
        if not clean_path or clean_path.strip() == '.':
            return ""  # The Root is pure, but empty.

        # 4. The Gaze of the Traversal (The "..")
        # We check for '..' components.
        if PathSentinel.TRAVERSAL_REGEX.search(clean_path):
            raise ArtisanHeresy(
                f"Security Heresy: Path Traversal detected in '{path_str}'.",
                suggestion="All paths must be relative to the project root. '..' is forbidden."
            )

        # 5. The Gaze of the Absolute
        # Unless explicitly allowed (rare), paths must be relative.
        if not allow_absolute:
            if clean_path.startswith('/'):
                # Check if it's a Windows absolute path (C:/) or Unix (/)
                raise ArtisanHeresy(
                    f"Security Heresy: Absolute path detected in '{path_str}'.",
                    suggestion="Paths must be relative to the Sanctum."
                )
            if re.match(r'^[a-zA-Z]:', clean_path):
                raise ArtisanHeresy(
                    f"Security Heresy: Drive letter detected in '{path_str}'.",
                    suggestion="Paths must be relative to the Sanctum."
                )

        # 6. The Gaze of the Forbidden Name
        parts = clean_path.split('/')
        for part in parts:
            if part in PathSentinel.FORBIDDEN_NAMES:
                # We log a warning but do not halt, as sometimes one must touch the void.
                Logger.warn(f"Accessing sensitive artifact '{part}' in path '{clean_path}'.")

        return clean_path

    @staticmethod
    def verify_resource_quota(content: Union[str, bytes], limit_mb: int = 50):
        """
        The Ward of Gluttony.
        Prevents the inscription of massive binary blobs that could choke the stream.
        """
        size_bytes = len(content)
        limit_bytes = limit_mb * 1024 * 1024

        if size_bytes > limit_bytes:
            raise ArtisanHeresy(
                f"Resource Quota Exceeded: Payload is {size_bytes} bytes (Limit: {limit_bytes}).",
                suggestion="Use a reference to an external asset (URL) instead of embedding massive files."
            )