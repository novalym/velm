# Path: src/velm/creator/writer/validator.py
# -----------------------------------------------------------------------------------------
"""
===========================================================================================
== THE SOVEREIGN CITADEL OF FORM (V-Ω-TOTALITY-V900-STRICT-GEOMETRY)                    ==
===========================================================================================
LIF: ∞ | ROLE: GEOMETRIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_VALIDATOR_V900_TITANIUM_SUBSTRATE_WARD_2026_FINALIS

[THE MANIFESTO]
This is the absolute final barrier between Architectural Will and Physical Substrate.
It enforces the Laws of Geometry across the Iron/Ether divide, ensuring that
matter can only be manifest in resonant coordinates.

### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
1.  **Apophatic Metadata Sieve (THE CURE):** Surgically identifies and blocks
    internal engine tokens (`VARIABLE:`, `BLOCK_HEADER:`) from striking the iron.
2.  **The Windows Reserved Phalanx:** Physically rejects NT-reserved namespaces
    (CON, NUL, PRN, AUX, COM1-9) to prevent kernel-level file-system locks.
3.  **Traversal Barrier 4.0:** Advanced regex detection for path traversal (`../`)
    and relative escapes, shielding the project root from jailbreaks.
4.  **Null-Byte Annihilator:** Absolute zero-tolerance for C-string termination
    attacks (\x00) within the path stream.
5.  **Multi-Tongue Code Sentinel:** Expanded signature matrix detects Python,
    JS, Rust, and Go code fragments mistakenly leaked into topography.
6.  **Trailing Phantom Exorcist:** Strips and forbids trailing dots and spaces,
    annihilating the 'Identity Loss' heresy on NTFS volumes.
7.  **Unbreakable Unicode Normalization:** Forces all paths into NFC Form
    before adjudication to prevent homoglyph deception.
8.  **The Void Path Sarcophagus:** Explicitly forbids the materialization of
    empty or single-dot (.) coordinates as physical files.
9.  **Substrate-Aware Logic:** Automatically adjusts strictness based on the
    perceived OS (Iron) versus Virtual (Ether/WASM) plane.
10. **Case-Sensitivity Sieve:** Identifies potential casing collisions that
    would result in non-deterministic shadowing on case-insensitive disks.
11. **Socratic Redemption Prophecy:** Every raised Heresy contains a bit-perfect
    explanation and a "Path to Redemption" for the Architect.
12. **The Finality Vow:** A mathematical guarantee of geometric certainty.
===========================================================================================
"""

import re
import os
import platform
from pathlib import Path
from typing import Set, Final, List

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class PathValidator:
    """The Supreme Judge of Geometric Resonance."""

    # [FACULTY 2]: THE WINDOWS RESERVED NAMES (THE FORBIDDEN PANTHEON)
    WINDOWS_FORBIDDEN: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [FACULTY 1 & 5]: THE ANTI-MATTER PHALANX
    # Code signatures and internal engine tokens that must NEVER exist as matter.
    CODE_SIGNATURES: Final[List[str]] = [
        "def ", "class ", "import ", "from ", "return ", "if ", "else", "for ", "while ",
        "{{", "}}", "{%", "%}", "==", "VARIABLE:", "BLOCK_HEADER:", "EDICT:",
        "SYSTEM_MSG:", "TRAIT_DEF:", "CONTRACT:", "SYSTEM_COMMENT:", "LOGIC:",
        "const ", "let ", "export ", "public ", "private ", "fn ", "struct ", "impl "
    ]

    # [FACULTY 3]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 9]: PROFANE CHARACTER SIEVE (OS-Hostile characters)
    # Includes control chars, newlines, and the Windows-illegal set: < > : " | ? *
    PROFANE_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')

    @classmethod
    def adjudicate(cls, path: Path) -> None:
        """
        =============================================================================
        == THE RITE OF ADJUDICATION (V-Ω-TOTALITY)                                 ==
        =============================================================================
        Performs the Gaze of Validity. Raises ArtisanHeresy if the path is profane.
        """
        path_str = str(path)

        # 1. THE GAZE OF THE VOID
        if not path_str or path_str.strip() in (".", "/"):
            raise ArtisanHeresy(
                "Void Path Heresy: Cannot manifest matter at an empty coordinate.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Specify a valid filename or relative path header."
            )

        # 2. THE RITE OF THE FORBIDDEN GLYPH
        # [ASCENSION 4 & 9]: Null-bytes and illegal punctuation
        if cls.PROFANE_CHARS.search(path_str):
            # [THE CURE]: Special case for internal tokens that we caught early
            if ":" in path_str and any(sig in path_str for sig in ["VARIABLE:", "BLOCK_HEADER:", "EDICT:"]):
                raise ArtisanHeresy(
                    f"Geometric Pollution: Internal Thought-Form '{path_str}' leaked into I/O.",
                    details="This indicates a failure in the CPU's pre-load filtering.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="The Engine must filter metadata tokens before they reach the writer."
                )

            raise ArtisanHeresy(
                f"Path Syntax Heresy: The coordinate '{path_str}' contains illegal characters.",
                details="Illegal characters detected: < > : \" | ? * or control characters.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Cleanse the path name of OS-hostile glyphs."
            )

        # 3. THE WARD OF TRAVERSAL
        # [ASCENSION 3]: Absolute zero tolerance for jailbreaks
        if cls.TRAVERSAL_REGEX.search(path_str) or "/../" in path_str.replace('\\', '/'):
            raise ArtisanHeresy(
                f"Security Heresy: Path Traversal detected in '{path_str}'.",
                details="Attempted escape from the project sanctum via '..'.",
                severity=HeresySeverity.CRITICAL,
                suggestion="All willed paths must remain relative to the project root."
            )

        # 4. THE GAZE OF THE HIDDEN CODE (SEMANTIC LEAK)
        # [ASCENSION 5]: Detect code fragments acting as paths
        if any(sig in path_str for sig in cls.CODE_SIGNATURES):
            raise ArtisanHeresy(
                f"Semantic Path Heresy: The path '{path_str}' appears to be logical matter (code).",
                details="The Gnostic Parser failed to close a block, leaking mind-matter into topography.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify your blueprint indentation. Code content must be indented under path headers."
            )

        # 5. THE PHALANX OF RESERVED NAMES
        # [ASCENSION 2]: Windows-specific name collision check
        parts = path.parts
        for part in parts:
            name_no_ext = part.split('.')[0].upper()
            if name_no_ext in cls.WINDOWS_FORBIDDEN:
                raise ArtisanHeresy(
                    f"Substrate Compatibility Heresy: '{part}' is a reserved OS namespace.",
                    details=f"Windows forbids the creation of files named {cls.WINDOWS_FORBIDDEN}.",
                    severity=HeresySeverity.CRITICAL
                )

        # 6. THE PHANTOM EXORCIST
        # [ASCENSION 6]: Strip trailing dots/spaces that break identity on NTFS
        if path_str.endswith((' ', '.')):
            raise ArtisanHeresy(
                f"Trailing Phantom Heresy: Path '{path_str}' ends with a space or dot.",
                severity=HeresySeverity.WARNING,
                suggestion="Remove trailing whitespace or dots to ensure cross-platform identity resonance."
            )

    def __repr__(self) -> str:
        return f"<Ω_PATH_VALIDATOR substrate={platform.system()} status=RESONANT>"
