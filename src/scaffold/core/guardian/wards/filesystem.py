# Path: scaffold/core/guardian/wards/filesystem.py
# ------------------------------------------------

import re
from pathlib import Path
from typing import List, Optional

from ..contracts import SecurityViolation, ThreatLevel
from ..grimoire import CROWN_JEWELS


class FilesystemWard:
    """
    =============================================================================
    == THE WARD OF MATTER (V-Ω-PATH-CANONICALIZER)                             ==
    =============================================================================
    Ensures no rite escapes the Sanctum or touches the Crown Jewels.
    """

    # Matches ".." only if it acts as a directory traversal token.
    TRAVERSAL_REGEX = re.compile(r'(?:^|[/\\])\.\.(?:[/\\]|$)')

    def __init__(self, sanctum_root: Path):
        self.sanctum_root = sanctum_root.resolve()

    def adjudicate(self, path_arg: str, line_num: int) -> Optional[SecurityViolation]:
        """
        Judges a path string against the Laws of Physics.
        Returns a Violation if heresy is found, else None.
        """
        # 1. The Gaze of Prophecy (Skip templates)
        if '{{' in path_arg:
            return None

        # 2. The Gaze of the Void
        if not path_arg or path_arg.strip() in ('/', '\\', '.'):
            return None

        # 3. The Gaze of Traversal (Regex)
        if self.TRAVERSAL_REGEX.search(path_arg):
            return SecurityViolation(
                ward="Filesystem",
                reason=f"Path Traversal ('..') detected in '{path_arg}'.",
                threat_level=ThreatLevel.CRITICAL,
                context=f"Line {line_num}"
            )

        try:
            # 4. The Gaze of Absolute Truth (Canonicalization)
            # We resolve relative to the sanctum
            target_path = (self.sanctum_root / path_arg).resolve()

            # 5. The Vow of Containment
            # Must start with the sanctum root
            if not str(target_path).startswith(str(self.sanctum_root)):
                return SecurityViolation(
                    ward="Filesystem",
                    reason=f"Root Escape: '{path_arg}' resolves to '{target_path}', outside '{self.sanctum_root}'.",
                    threat_level=ThreatLevel.CRITICAL,
                    context=f"Line {line_num}"
                )

            # 6. The Ward of the Crown Jewels
            # Check if any part of the path is protected
            for part in target_path.parts:
                if part in CROWN_JEWELS or f".{part}" in CROWN_JEWELS:  # Simple check
                    return SecurityViolation(
                        ward="Filesystem",
                        reason=f"Sacred Artifact Access: '{part}' is a protected Crown Jewel.",
                        threat_level=ThreatLevel.CRITICAL,
                        context=f"Line {line_num}"
                    )

            # Check full path against jewels (for absolute paths in list)
            for jewel in CROWN_JEWELS:
                if str(target_path).endswith(jewel) or jewel in str(target_path):
                    return SecurityViolation(
                        ward="Filesystem",
                        reason=f"Sacred Artifact Access: Path touches '{jewel}'.",
                        threat_level=ThreatLevel.CRITICAL,
                        context=f"Line {line_num}"
                    )

        except Exception as e:
            # If we can't resolve it, we can't trust it.
            return SecurityViolation(
                ward="Filesystem",
                reason=f"Path Paradox: Could not resolve '{path_arg}'. {e}",
                threat_level=ThreatLevel.HIGH,
                context=f"Line {line_num}"
            )

        return None