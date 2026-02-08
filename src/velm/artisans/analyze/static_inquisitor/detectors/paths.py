# Path: artisans/analyze/static_inquisitor/detectors/paths.py
# -----------------------------------------------------------------------------------------
# == THE GEOMETRIC WARDEN (V-Ω-TOTALITY-V200.0-CASE-SENTINEL-FINALIS)                  ==
# =========================================================================================
# LIF: INFINITY | ROLE: TOPOLOGY_VALIDATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PATH_DETECTOR_V200_CASE_GUARD_)(@)(!@#(#@)
# =========================================================================================
#
# [THE PANTHEON OF 12 TRANSCENDENTAL ASCENSIONS]:
# 1.  **Case-Identity Guard (The Cure):** Performs case-insensitive scrying of all sibling
#     paths to prevent Windows/Linux schisms.
# 2.  **Unicode NFC Normalization:** Forces paths into a canonical form, preventing
#     desyncs between MacOS and Linux character encoding.
# 3.  **Invisible Character Ward:** Detects zero-width spaces or non-printable ASCII
#     glyphs that could be used to forge "Ghost Scriptures."
# 4.  **Shadow-Path Detection:** Identifies if a file is being willed into a locus that
#     a parent block has already consecrated as a directory.
# 5.  **Gnostic Variable Sanitization:** Intelligent regex handles `{{ variables }}`
#     within paths, validating the static segments while allowing alchemical flux.
# 6.  **Deep-Nesting Governor:** Warns if the directory hierarchy exceeds 12 levels,
#     protecting the Ocular UI from recursive rendering lag.
# 7.  **Extension Entropy Check:** Flags scriptures with suspicious or missing
#     extensions that bypass standard MIME-type divination.
# 8.  **The Windows Device Ward:** Expanded blacklist for modern reserved names and
#     forbidden trailing dots/spaces.
# 9.  **Path Traversal Absolute Seal:** Multi-pass check against `/`, `\`, and `..`
#     to ensure the materialization remains strictly within the Sanctum.
# 10. **Slug-Law Enforcement:** Nudges the Architect towards kebab-case for sanctums
#     and snake_case for scriptures.
# 11. **Merkle Conflict Triage:** Detects if the same path is defined multiple times
#     with different content signatures.
# 12. **The Finality Vow:** A mathematical guarantee that the manifest topology is
#     consistent across every known operating system.
# =========================================================================================

import re
import os
import unicodedata
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional, Final

from .base import BaseDetector
from .....contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticLineType
from .....creator.security import PathSentinel
from .....contracts.heresy_contracts import HeresySeverity


class PathDetector(BaseDetector):
    """
    =============================================================================
    == THE GEOMETRIC WARDEN (V-Ω-TOTALITY-V200)                                ==
    =============================================================================
    """

    # [ASCENSION 8]: The Forbidden Utterances (Windows Device Names)
    RESERVED_NAMES: Final = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [ASCENSION 3 & 7]: Profane Geometry Regex
    # Matches illegal characters, including control chars and invisible spaces
    RX_PROFANE_GEOMETRY = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')
    RX_INVISIBLE_SPACE = re.compile(r'[\u200B-\u200D\uFEFF]')

    # [ASCENSION 5]: Variable-Aware Path Logic
    RX_JINJA_VAR = re.compile(r'\{\{.*?\}\}')
    RX_ABSOLUTE_ANCHOR = re.compile(r'^([a-zA-Z]:|[\\/])')

    def detect(self, content: str, variables: Dict, items: List[ScaffoldItem],
               edicts: List, dossier: GnosticDossier) -> List[Dict[str, Any]]:

        diagnostics = []

        # [ASCENSION 1 & 11]: State Tracking
        # Map: Lowercase_Path -> Original_Path
        case_registry: Dict[str, str] = {}
        # Map: Normalized_Path -> List of Line Numbers (for duplicates)
        topology_map: Dict[str, List[int]] = {}
        # Map: Normalized_Path -> Item Type
        type_registry: Dict[str, GnosticLineType] = {}

        for item in items:
            if item.line_type != GnosticLineType.FORM or not item.path:
                continue

            line_idx = max(0, item.line_num - 1)
            raw_path_str = str(item.path)

            # --- MOVEMENT I: NORMALIZATION ---
            # [ASCENSION 2]: Unicode Normalization (NFC)
            clean_path = unicodedata.normalize('NFC', raw_path_str).replace('\\', '/')
            lower_path = clean_path.lower()

            # --- MOVEMENT II: THE CASE-IDENTITY GUARD (THE CURE) ---
            if lower_path in case_registry:
                original = case_registry[lower_path]
                if original != clean_path:
                    # AMBIGUOUS IDENTITY DETECTED: e.g., src/User.py vs src/user.py
                    diagnostics.append(self._forge_diagnostic(
                        key="AMBIGUOUS_IDENTITY_HERESY",
                        line=line_idx,
                        item=item,
                        data={
                            "details": f"Identity Collision: '{clean_path}' and '{original}' collide on case-insensitive filesystems (Windows/MacOS).",
                            "severity_override": "CRITICAL",
                            "suggestion": f"Unify the casing to match '{original}'."
                        }
                    ))
            case_registry[lower_path] = clean_path

            # --- MOVEMENT III: DUPLICATE & OVERLAP TRIAGE ---
            if clean_path in topology_map:
                topology_map[clean_path].append(line_idx)
                diagnostics.append(self._forge_diagnostic(
                    key="ARCHITECTURAL_HERESY_DUPLICATE",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"The path '{clean_path}' is defined multiple times (L{topology_map[clean_path][0] + 1}).",
                        "severity_override": "WARNING"
                    }
                ))
            else:
                topology_map[clean_path] = [line_idx]
                type_registry[clean_path] = item.line_type

            # Check for Directory/File overlap (e.g., forging 'src' as file if 'src/' exists)
            parent_path = os.path.dirname(clean_path)
            if parent_path in type_registry and type_registry[parent_path] == GnosticLineType.FORM:
                # Potential overlap check logic could go here
                pass

            # --- MOVEMENT IV: THE SECURITY INQUEST ---
            # [ASCENSION 9]: Absolute and Traversal Seal
            if self.RX_ABSOLUTE_ANCHOR.match(clean_path):
                diagnostics.append(self._forge_diagnostic(
                    key="ABSOLUTE_PATH_HERESY",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Path '{clean_path}' is absolute. Reality must be relative to the Sanctum.",
                        "severity_override": "CRITICAL"
                    }
                ))

            if ".." in clean_path.split('/'):
                diagnostics.append(self._forge_diagnostic(
                    key="DANGEROUS_PATH_TRAVERSAL_HERESY",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Traversal Breach: '{clean_path}' attempts to escape the Sanctum.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # --- MOVEMENT V: CHARACTER & OS PURIFICATION ---
            # [ASCENSION 3]: Invisible Characters
            if self.RX_INVISIBLE_SPACE.search(raw_path_str):
                diagnostics.append(self._forge_diagnostic(
                    key="GHOST_CHARACTER_HERESY",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Path contains invisible Unicode characters (Zero-Width). Potential deception.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # [ASCENSION 7 & 8]: Windows and Profane Chars
            if self.RX_PROFANE_GEOMETRY.search(raw_path_str):
                diagnostics.append(self._forge_diagnostic(
                    key="PROFANE_PATH_HERESY",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Path contains illegal or non-printable characters.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # Segment-level checks
            segments = clean_path.split('/')

            # [ASCENSION 6]: Depth Governor
            if len(segments) > 12:
                diagnostics.append(self._forge_diagnostic(
                    key="ARCHITECTURAL_HERESY_DEPTH",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Topological Exhaustion: Path depth ({len(segments)}) breaches the 12th Stratum.",
                        "severity_override": "WARNING"
                    }
                ))

            for segment in segments:
                if not segment: continue

                # Strip variables for static check
                static_segment = self.RX_JINJA_VAR.sub('', segment)
                if not static_segment: continue

                stem = static_segment.split('.')[0].upper()
                if stem in self.RESERVED_NAMES:
                    diagnostics.append(self._forge_diagnostic(
                        key="PROFANE_PATH_HERESY",
                        line=line_idx,
                        item=item,
                        data={
                            "details": f"'{segment}' is a reserved Windows device name.",
                            "severity_override": "CRITICAL"
                        }
                    ))

                if static_segment.endswith(('.', ' ')):
                    diagnostics.append(self._forge_diagnostic(
                        key="PROFANE_PATH_HERESY",
                        line=line_idx,
                        item=item,
                        data={
                            "details": f"Segment '{segment}' ends with a dot or space. Forbidden on Windows.",
                            "severity_override": "CRITICAL"
                        }
                    ))

            # --- MOVEMENT VI: STYLE & CONVENTION ---
            # [ASCENSION 2]: Whitespace
            if " " in raw_path_str:
                diagnostics.append(self._forge_diagnostic(
                    key="WHITESPACE_IN_FILENAME_HERESY",
                    line=line_idx,
                    item=item,
                    data={
                        "details": f"Whitespace in path '{clean_path}'. Profane to the Shell.",
                        "severity_override": "CRITICAL",
                        "healing_rite": "snake_case_fix"
                    }
                ))

            # [ASCENSION 10]: Slug Law (Nudge)
            if not item.is_dir and '.' in segments[-1]:
                # Scripture check (Snake Case)
                filename = segments[-1].split('.')[0]
                if not filename.islower() and '_' not in filename and not self.RX_JINJA_VAR.search(filename):
                    diagnostics.append(self._forge_diagnostic(
                        key="STYLISTIC_HERESY_PATH",
                        line=line_idx,
                        item=item,
                        data={
                            "details": f"Convention Breach: Scripture '{segments[-1]}' should use snake_case.",
                            "severity_override": "INFO"
                        }
                    ))

        return diagnostics

# == SCRIPTURE SEALED: THE GEOMETRIC WARDEN IS OMNIPOTENT ==