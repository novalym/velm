# Path: src/velm/creator/security.py
# ----------------------------------
# LIF: ∞ | ROLE: GEOMETRIC_WARDEN | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PATH_SENTINEL_V501_RECURSIVE_FINALIS
# =================================================================================

import re
import os
import unicodedata
from pathlib import Path
from typing import Union, Dict, Any, Optional, Set, Final, List

# --- THE DIVINE UPLINKS ---
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..logger import Scribe

Logger = Scribe("PathSentinel")


class PathSentinel:
    """
    =================================================================================
    == THE GNOSTIC PATH SENTINEL (V-Ω-TOTALITY-V501-RECURSIVE)                     ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_GUARDIAN | RANK: OMEGA

    The supreme authority on spatial validity. It ensures that no geometry can exist
    outside the ordained boundaries of the Sanctum.
    """

    # [FACULTY 8]: THE FORBIDDEN NAMES (Windows System Device Names)
    RESERVED_NAMES: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [FACULTY 1]: THE INQUISITOR'S PHALANX
    # Detecting logic leaks masquerading as filenames.
    MATTER_LEAK_PATTERNS: Final[List[str]] = [
        "def ", "class ", "import ", "from ", "return ", "if ", "else", "for ",
        "{{", "}}", "{%", "<script", "<html>", "<body>", "---"
    ]

    # [FACULTY 1]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 9]: THE PROFANE GLYPH WARD
    # Blocks control characters, non-printables, and illegal OS characters.
    PROFANE_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')

    @classmethod
    def adjudicate(
            cls,
            logical_path: Union[str, Path],
            project_root: Path,
            variables: Optional[Dict[str, Any]] = None,
            trace_id: str = "tr-void"
    ) -> str:
        """
        =============================================================================
        == THE RITE OF ADJUDICATION (V-Ω-RECURSIVE-GAZE)                           ==
        =============================================================================
        LIF: ∞ | The absolute authority on path safety.

        [THE FIX]: This method now performs a pre-emptive dry-run of the alchemical
        transmutation to ensure the final path is secure.
        """
        raw_path_str = str(logical_path)
        manifest_path_str = raw_path_str

        # --- MOVEMENT I: THE RECURSIVE GAZE (THE CURE) ---
        # [ASCENSION 1]: If the path is a prophecy, we must resolve it to see the truth.
        if variables and '{{' in raw_path_str:
            try:
                from ..core.alchemist import get_alchemist
                alchemist = get_alchemist()
                manifest_path_str = alchemist.transmute(raw_path_str, variables)
                Logger.verbose(f"[{trace_id}] Recursive Gaze: '{raw_path_str}' -> '{manifest_path_str}'")
            except Exception as e:
                # If alchemy fails, we cannot judge. We default to safe restriction.
                raise ArtisanHeresy(
                    f"Alchemical Path Fracture: Could not scry the truth of '{raw_path_str}'.",
                    severity=HeresySeverity.CRITICAL,
                    details=str(e)
                )

        # --- MOVEMENT II: THE RITE OF NORMALIZATION ---
        # [ASCENSION 2 & 4]: POSIX discipline + Unicode NFC Purity.
        clean_path = unicodedata.normalize('NFC', manifest_path_str.replace('\\', '/').strip())

        # --- MOVEMENT III: THE GEOMETRIC ADJUDICATION ---

        # 1. The Gaze of the Void
        if not clean_path or clean_path == '.':
            return ""

        # 2. The Gaze of the Traversal (THE CURE)
        if cls.TRAVERSAL_REGEX.search(clean_path):
            raise ArtisanHeresy(
                f"Security Breach: Path Traversal detected in '{manifest_path_str}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"The resolved coordinate attempts to escape the Sanctum via '..' operations.",
                suggestion="Align your path variables to remain within the project hierarchy."
            )

        # 3. The Gaze of the Absolute (THE CURE)
        if clean_path.startswith('/') or re.match(r'^[a-zA-Z]:', clean_path):
            raise ArtisanHeresy(
                f"Security Breach: Absolute path detected in '{manifest_path_str}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"Coordinate '{clean_path}' is an absolute anchor. Only relative paths are warded.",
                suggestion="Remove leading slashes or drive letters from your path definitions."
            )

        # --- MOVEMENT IV: THE FORENSIC SCAN ---

        # 4. Matter Leak Detection (Faculty 6)
        # If the path looks like code, the parser has leaked.
        if any(sig in clean_path for sig in cls.MATTER_LEAK_PATTERNS):
            raise ArtisanHeresy(
                f"Semantic Paradox: Path '{clean_path}' contains Code Matter.",
                severity=HeresySeverity.CRITICAL,
                details="A line of code was misinterpreted as a file path. Check your blueprint indentation.",
                suggestion="Ensure all code blocks are indented relative to their path headers."
            )

        # 5. Profane Character Scan (Faculty 9)
        if cls.PROFANE_CHARS.search(clean_path):
            raise ArtisanHeresy(
                f"Geometric Paradox: Illegal characters detected in path '{clean_path}'.",
                severity=HeresySeverity.CRITICAL,
                details="The path contains control characters or OS-forbidden symbols."
            )

        # --- MOVEMENT V: OS & STRATUM VALIDATION ---

        # 6. Windows Reserved Name Ward (Faculty 8)
        segments = [s.upper().split('.')[0] for s in clean_path.split('/')]
        for seg in segments:
            if seg in cls.RESERVED_NAMES:
                raise ArtisanHeresy(
                    f"OS Compatibility Heresy: '{seg}' is a reserved Windows device name.",
                    severity=HeresySeverity.CRITICAL
                )

        # 7. Bound Verification (Faculty 2)
        # We ensure the physical resolution is still inside the root.
        # This is the "Great Wall" of logic.
        try:
            abs_root = project_root.resolve()
            abs_target = (abs_root / clean_path).resolve()

            # Using commonpath to ensure no symlink trickery occurred.
            if os.path.commonpath([str(abs_root), str(abs_target)]) != str(abs_root):
                raise ArtisanHeresy(
                    f"Boundary Fracture: '{clean_path}' escaped the Root Sanctum.",
                    severity=HeresySeverity.CRITICAL
                )
        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise
            raise ArtisanHeresy(f"Geometric Resolution Paradox: {e}", severity=HeresySeverity.CRITICAL)

        return clean_path

    @staticmethod
    def verify_metabolic_mass(content: Union[str, bytes], limit_mb: int = 50):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (V-Ω-METABOLIC-WARD)                               ==
        =============================================================================
        [THE FIX 3]: Prevents the Engine from inhaling massive blobs into the Heap.
        """
        size_bytes = len(content)
        limit_bytes = limit_mb * 1024 * 1024

        if size_bytes > limit_bytes:
            raise ArtisanHeresy(
                f"Metabolic Tax Overflow: Payload is {size_bytes / (1024 * 1024):.2f}MB (Limit: {limit_mb}MB).",
                severity=HeresySeverity.CRITICAL,
                details="A single block of scripture is too heavy for the current Gnostic Strata.",
                suggestion="Use the '<<' seed sigil to pull data from external artifacts instead of embedding."
            )

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """[FACULTY 3]: Shannon Entropy calculation for secret detection."""
        import math
        if not text: return 0.0
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return - sum([p * math.log(p) / math.log(2.0) for p in probabilities])

# == SCRIPTURE SEALED: THE BORDERS ARE ABSOLUTE AND UNBREAKABLE ==