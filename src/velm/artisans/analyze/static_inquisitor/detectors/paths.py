# Path: artisans/analyze/static_inquisitor/detectors/paths.py
# -----------------------------------------------------------

import re
import os
from typing import List, Dict, Any, Set, Tuple

from .base import BaseDetector
from .....contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticLineType
from .....creator.security import PathSentinel


class PathDetector(BaseDetector):
    """
    =============================================================================
    == THE GEOMETRIC WARDEN (V-Ω-PATH-TOPOLOGY-ULTIMA)                         ==
    =============================================================================
    LIF: 10,000,000,000,000

    The Sovereign Guardian of Filesystem Geometry.
    It validates every path against the Laws of Physics, OS Constraints, and
    Gnostic Best Practices.

    ### THE PANTHEON OF 8 DETECTIONS:
    1.  **The Whitespace Ward:** Detects spaces in filenames (Critical Heresy).
    2.  **The Doppelgänger Gaze:** Detects duplicate path definitions.
    3.  **The Root Anchor:** Detects absolute paths or drive letters.
    4.  **The Traversal Sentinel:** Detects `../` escape attempts.
    5.  **The Windows Curse:** Detects reserved names (`CON`, `NUL`, `PRN`).
    6.  **The Length Watcher:** Detects paths approaching the MAX_PATH limit.
    7.  **The Character Purifier:** Detects profane glyphs (`<`, `>`, `:`, `"`).
    8.  **The Separator Harmonizer:** Detects mixed slashes (`\`).
    """

    # Windows Reserved Names (The Forbidden Utterances)
    RESERVED_NAMES = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # Characters forbidden in NTFS/FAT32 (and generally bad ideas)
    PROFANE_CHARS_REGEX = re.compile(r'[<>:"|?*]')

    # Heuristic for variable placeholders to avoid false positives
    VARIABLE_REGEX = re.compile(r'\{\{.*?\}\}')

    def detect(self, content: str, variables: Dict, items: List[ScaffoldItem], edicts: List, dossier: GnosticDossier) -> \
    List[Dict[str, Any]]:
        diagnostics = []
        seen_paths: Set[str] = set()

        for item in items:
            # We only judge Forms (Files/Dirs) that have a path defined
            if item.line_type != GnosticLineType.FORM or not item.path:
                continue

            path_str = str(item.path)
            # Normalize for logic checks, but keep original for reporting
            clean_path = path_str.replace('\\', '/')

            # Skip detection if the path is purely a Jinja variable (too dynamic to judge)
            if self.VARIABLE_REGEX.fullmatch(path_str):
                continue

            # --- 1. THE DOPPELGÄNGER GAZE ---
            if path_str in seen_paths:
                diagnostics.append(self._forge_diagnostic(
                    key="ARCHITECTURAL_HERESY_DUPLICATE",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"The path '{path_str}' is defined multiple times. Reality allows only one origin.",
                        "severity_override": "CRITICAL"
                    }
                ))
            seen_paths.add(path_str)

            # --- 2. THE WHITESPACE WARD (ELEVATED) ---
            # We treat this as CRITICAL to force the IDE to show the Lightbulb.
            if " " in path_str:
                diagnostics.append(self._forge_diagnostic(
                    key="WHITESPACE_IN_FILENAME_HERESY",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path '{path_str}' contains profane whitespace.",
                        "severity_override": "CRITICAL",
                        # ★★★ THE GOLDEN THREAD ★★★
                        # We explicitly name the cure. No guessing.
                        "healing_rite": "snake_case_fix"
                    }
                ))

            # --- 3. THE ROOT ANCHOR (ABSOLUTE PATHS) ---
            if clean_path.startswith("/") or re.match(r'^[a-zA-Z]:', path_str):
                diagnostics.append(self._forge_diagnostic(
                    key="ABSOLUTE_PATH_HERESY",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path '{path_str}' is absolute. Blueprints must be relative to the Sanctum.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # --- 4. THE TRAVERSAL SENTINEL ---
            if ".." in path_str.split('/'):  # Only match segment traversal
                diagnostics.append(self._forge_diagnostic(
                    key="DANGEROUS_PATH_TRAVERSAL_HERESY",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path '{path_str}' attempts to escape the Sanctum via '..'.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # --- 5. THE WINDOWS CURSE ---
            # Check every segment of the path for reserved names
            for part in clean_path.split('/'):
                # Strip extension for check (e.g. con.txt is invalid on Windows)
                stem = part.split('.')[0].upper()
                if stem in self.RESERVED_NAMES:
                    diagnostics.append(self._forge_diagnostic(
                        key="PROFANE_PATH_HERESY",
                        line=item.line_num - 1,
                        item=item,
                        data={
                            "details": f"Segment '{part}' is a reserved Windows device name ('{stem}').",
                            "severity_override": "CRITICAL"
                        }
                    ))

                # Check for trailing dots or spaces in segment
                if part.endswith('.') or part.endswith(' '):
                    diagnostics.append(self._forge_diagnostic(
                        key="PROFANE_PATH_HERESY",
                        line=item.line_num - 1,
                        item=item,
                        data={
                            "details": f"Segment '{part}' ends with a dot or space, which is heresy in Windows.",
                            "severity_override": "WARNING"
                        }
                    ))

            # --- 6. THE CHARACTER PURIFIER ---
            if self.PROFANE_CHARS_REGEX.search(path_str):
                diagnostics.append(self._forge_diagnostic(
                    key="PROFANE_PATH_HERESY",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path '{path_str}' contains illegal characters (< > : \" | ? *).",
                        "severity_override": "CRITICAL"
                    }
                ))

            # --- 7. THE SEPARATOR HARMONIZER ---
            if "\\" in path_str:
                diagnostics.append(self._forge_diagnostic(
                    key="STYLISTIC_HERESY_PATH",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path '{path_str}' uses backslashes. Use forward slashes '/' for universal harmony.",
                        "severity_override": "INFO",
                        "suggestion": f"Replace with '{path_str.replace(os.sep, '/')}'"
                    }
                ))

            # --- 8. THE LENGTH WATCHER ---
            if len(path_str) > 200:
                diagnostics.append(self._forge_diagnostic(
                    key="ARCHITECTURAL_HERESY_PATH_LENGTH",
                    line=item.line_num - 1,
                    item=item,
                    data={
                        "details": f"Path is dangerously long ({len(path_str)} chars). Approaching MAX_PATH limit.",
                        "severity_override": "WARNING"
                    }
                ))

        return diagnostics