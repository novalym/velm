# Path: scaffold/artisans/definition/alchemist.py
# ----------------------------------------------

import os
import urllib.parse
from pathlib import Path


class URIAlchemist:
    """
    =============================================================================
    == THE URI ALCHEMIST (V-Ω-PATH-CANONICALIZER)                              ==
    =============================================================================
    A specialist artisan for transmuting between the Ethereal URI (VS Code)
    and the Mortal Path (Filesystem).

    Functions:
    1. Handles `file:///` and `file://` prefixes.
    2. Heals Windows drive letter anomalies (e.g., `/c:/` -> `C:/`).
    3. Unifies slashes to POSIX standard.
    4. Decodes URI characters (e.g., `%20` -> ` `).
    """

    @staticmethod
    def to_absolute_path(uri_str: str) -> Path:
        """Transmutes a raw URI string into a pure, absolute Path object."""
        # 1. Strip the protocol
        clean = uri_str.replace('file:///', '').replace('file://', '')

        # 2. URL Decode (e.g. handle spaces in paths)
        clean = urllib.parse.unquote(clean)

        # 3. Windows Surgery: /C:/dev -> C:/dev
        if os.name == 'nt' and clean.startswith('/') and ':' in clean:
            clean = clean.lstrip('/')

        # 4. Resolve and Normalize
        return Path(clean).resolve()

    @staticmethod
    def normalize_posix(path_obj: Path) -> str:
        """Returns a POSIX-compliant string for internal Daemon consistency."""
        return str(path_obj).replace('\\', '/')

    @staticmethod
    def to_uri(path_obj: Path) -> str:
        """Transmutes a Path object back into a Celestial URI."""
        return path_obj.as_uri()