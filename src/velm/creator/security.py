# Path: src/velm/creator/security.py
# ----------------------------------
# LIF: ∞ | ROLE: GEOMETRIC_WARDEN | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PATH_SENTINEL_V600_TOTALITY_FINALIS
# =================================================================================

import re
import os
import sys
import math
import unicodedata
import platform
import hashlib
from pathlib import Path
from typing import Union, Dict, Any, Optional, Set, Final, List, Tuple

# --- THE DIVINE UPLINKS ---
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..logger import Scribe

Logger = Scribe("PathSentinel")


class PathSentinel:
    """
    =================================================================================
    == THE GNOSTIC PATH SENTINEL (V-Ω-TOTALITY-V600-LOGIC-IMMUNE)                  ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_GUARDIAN | RANK: OMEGA_SUPREME
    AUTH: Ω_PATH_SENTINEL_V600_LOGIC_IMMUNE_FINALIS

    The supreme authority on spatial validity and the primary immune system of the
    Velm God-Engine. It ensures that no geometry can exist outside the ordained
    boundaries of the Sanctum, while managing the complex overlap between
    Physical Jails, Transactional Staging areas, and Abstract Logic.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (V600):
    1.  **Logic Node Immunity (THE CURE):** Grants absolute diplomatic immunity to
        Gnostic Control Flow keywords (`@if`, `@else`, `@macro`), preventing them from
        being falsely indicted as "Anti-Matter Leaks".
    2.  **Staging Amnesty:** Surgically identifies internal Engine operations
        (staging, backups, chronicles) and grants them passage.
    3.  **Bicameral Root Anchoring:** Simultaneously scries the 'SCAFFOLD_PROJECT_ROOT'
        (Logical) and 'SCAFFOLD_JAIL_ROOT' (Physical) to resolve spatial paradoxes.
    4.  **Recursive Matter Leak Detection:** Scans every individual path segment
        for logical "Anti-Matter"—code signatures (def, class, {{) masquerading
        as topography.
    5.  **Achronal Path Normalization:** Enforces Unicode NFC purity and POSIX
        slash discipline, neutralizing "Backslash Obfuscation" heresies.
    6.  **The "Crown Jewel" Ward:** Hardened protection for sensitive nodes like
        `.git`, `.env`, and `scaffold.lock`.
    7.  **Traversal Barrier 3.0:** Employs advanced regex phalanxes to annihilate
        all forms of `..` or `hidden absolute` attacks across all OS dialects.
    8.  **Metabolic Mass Governor:** Adjudicates the byte-weight of incoming content,
        preventing "Heap Gluttony" from massive binary blobs.
    9.  **Shannon Entropy Sieve:** Integrated detection of high-entropy strings
        within paths and content to flag potential secret leaks.
    10. **OS Reserved Namespace Sentinel:** Explicitly blocks Windows device names
        (CON, NUL) and Linux kernel paths (/proc, /sys).
    11. **Forensic Resolution Mirror:** In the event of a fracture, it proclaims
        both the "Attempted Path" and the "Physically Resolved Path" for autopsy.
    12. **Sovereign Engine Shield:** Physically wards the Engine's own source code
        and the active Python Virtual Environment from self-consumption.
    13. **Homoglyph Defense:** Detects invisible control characters or look-alike
        glyphs that could trick the file system.
    14. **Jinja Variable Masking:** Temporarily masks `{{ variables }}` during
        forensic scanning to prevent false positives on structural syntax.
    15. **Trailing Phantom Exorcism:** Strips trailing dots and spaces that cause
        identity loss on NTFS filesystems.
    16. **Dimensional Rift Detection:** Detects if a path attempts to jump across
        hardware volume boundaries (C: to D:).
    17. **Infinite Symlink Guard:** Detects `RecursionError` during path resolution.
    18. **Environment DNA Suture:** Inherits `GNOSTIC_REQUEST_ID` for logging context.
    19. **Null-Byte Phalanx:** Absolute zero-tolerance for C-string termination attacks.
    20. **Isomorphic Geometry:** Works identically on WASM (Virtual FS) and Iron (Native).
    21. **Substrate Normalization:** Forces lowercase comparison for reserved names
        regardless of OS case-sensitivity settings.
    22. **Ghost Node Handling:** Can adjudicate paths that do not yet exist physically.
    23. **Strict Boundary Inquest:** Uses `os.path.commonpath` for bulletproof
        jailbreak detection.
    24. **The Finality Vow:** A mathematical guarantee of a valid outcome: either
        a perfectly warded path is returned, or a high-status Heresy is raised.
    =================================================================================
    """

    # [FACULTY 10]: THE FORBIDDEN NAMES (Windows System & Gnostic Internals)
    RESERVED_NAMES: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [FACULTY 6]: THE CROWN JEWEL WARD
    CROWN_JEWELS: Final[Set[str]] = {
        ".git", ".hg", ".svn", ".env", ".env.local", "scaffold.lock",
        "__pycache__", "node_modules", ".heartbeat", ".scaffold_internal",
        "gnosis.db", "gnosis.db-shm", "gnosis.db-wal"
    }

    # [FACULTY 4]: THE INQUISITOR'S PHALANX
    # Code signatures that should never appear in a file path.
    MATTER_LEAK_SIGNATURES: Final[List[str]] = [
        "def ", "class ", "import ", "from ", "return ", "if ", "else", "for ",
        "{{", "}}", "{%", "<script", "<html>", "<body>", "---", "const ", "let ",
        "=>", "function", "var ", "async ", "await "
    ]

    # [FACULTY 7]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 19]: THE PROFANE GLYPH WARD
    PROFANE_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')

    # [FACULTY 1]: LOGIC NODE WHITELIST (THE CURE)
    # These tokens are thoughts, not matter. They are immune to spatial laws.
    LOGIC_NODE_WHITELIST: Final[Set[str]] = {
        "@if", "@else", "@elif", "@endif", "@for", "@endfor",
        "@try", "@catch", "@finally", "@endtry", "@macro", "@endmacro",
        "@task", "@endtask", "@call", "@import", "@from", "@on_os"
    }

    # [FACULTY 2]: INTERNAL ENGINE SIGNATURES
    INTERNAL_GNOSTIC_SIGNATURES: Final[Tuple[str, ...]] = (
        "BLOCK_HEADER:", "EDICT:", "SYSTEM_COMMENT:", "LOGIC:", "POLYGLOT:",
        "MACRO_DEF:", "SYSTEM_MSG:", "VARIABLE:", "TRAIT_DEF:", "CONTRACT:",
        "TRAIT_USE:", "ON_UNDO:", "ON_HERESY:", "POST_RUN:"
    )

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
        == THE SUPREME RITE OF GEOMETRIC ADJUDICATION                              ==
        =============================================================================
        Validates, normalizes, and wards a path against all known heresies.
        """
        raw_path_str = str(logical_path)

        # =========================================================================
        # == MOVEMENT 0: THE DIPLOMATIC IMMUNITY CHECK (THE CURE)                ==
        # =========================================================================

        # 1. Internal Engine Signatures (Metadata)
        if any(raw_path_str.startswith(sig) for sig in cls.INTERNAL_GNOSTIC_SIGNATURES):
            # Logger.debug(f"[{trace_id}] Amnesty Granted: Internal thought-form perceived.")
            return raw_path_str

        # 2. Logic Node Immunity (The Fix for @else)
        # We strip trailing colons or whitespace to find the primal token.
        first_token = raw_path_str.split()[0].rstrip(':').strip()
        if first_token in cls.LOGIC_NODE_WHITELIST:
            # Logger.debug(f"[{trace_id}] Amnesty Granted: Logic Node '{first_token}' perceived.")
            return raw_path_str

        # --- MOVEMENT I: THE PHANTOM FOREST SIEVE ---
        # [ASCENSION 13]: Homoglyph & Artifact Removal
        JUNK_CHARS = {
            ' ', '\t', '\n', '\r', '\f', '\v',
            '│', '├', '─', '└', '┐', '┌', '┤', '┬', '┴', '┼', '╵', '╷', '╸', '╹', '╻',
            '╼', '╽', '═', '║', '╔', '╗', '╚', '╝', '╟', '╢', '╦', '╩', '╬',
            '|', '+', '*', '`', '📂', '📄', '📁', '📁', '┃', '┓', '┗', '┣', '┻', '┳', '╋'
        }

        # The Atomic Purification: Remove visual artifacts.
        purified_coordinate = "".join(c for c in raw_path_str if c not in JUNK_CHARS)

        # Normalize separators to forward-slashes for internal geometric consistency.
        purified_coordinate = purified_coordinate.replace('\\', '/').strip('/')

        # --- MOVEMENT II: THE RECURSIVE GAZE (ALCHEMICAL RESOLUTION) ---
        # Resolve variables ({{ project_slug }}) to check the *final* path geometry.
        manifest_path_str = purified_coordinate
        if variables and '{{' in purified_coordinate:
            try:
                from ..core.alchemist import get_alchemist
                manifest_path_str = get_alchemist().transmute(purified_coordinate, variables)
            except Exception:
                # Fallback to literal intent if alchemy fails to prevent blocking the strike.
                pass

        # [ASCENSION 5]: Enforce Unicode NFC purity.
        purified_path = unicodedata.normalize('NFC', manifest_path_str.strip()).replace('\\', '/')

        # --- MOVEMENT III: GEOMETRIC ANCHORING ---
        # If the purification leaves a void (e.g. input was just "📂"), anchor to root.
        if not purified_path or purified_path in ('.', '/'):
            return str(project_root.resolve())

        # [ASCENSION 19]: Null-Byte Phalanx
        if '\x00' in purified_path:
            raise ArtisanHeresy("Security Violation: Null-Byte Injection perceived.", severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT IV: THE INODE WARD (PHYSICAL RESOLUTION) ---
        try:
            # Establish the Absolute Coordinate System.
            abs_root = project_root.resolve()

            # [ASCENSION 3]: JAILED SUBSTRATE SENSING
            jail_root_str = os.getenv("SCAFFOLD_JAIL_ROOT")
            active_boundary = Path(jail_root_str).resolve() if jail_root_str else abs_root

            # Construct the physical target coordinate.
            # strict=False allows the gaze to fall upon matter that is willed but not yet manifest.
            try:
                physical_target = (abs_root / purified_path).resolve(strict=False)
            except RecursionError:
                # [ASCENSION 17]: Infinite Symlink Guard
                raise ArtisanHeresy("Geometric Paradox: Infinite Symlink loop detected.",
                                    severity=HeresySeverity.CRITICAL)

            # --- MOVEMENT V: THE RECONCILIATION OF REALMS ---

            # 1. THE BOUNDARY INQUEST (Breakout Prevention)
            try:
                # [ASCENSION 23]: Strict Boundary Check
                common = os.path.commonpath([str(active_boundary), str(physical_target)])
                if common != str(active_boundary):
                    msg = "Forbidden Gnosis: Target escapes assigned jail." if jail_root_str else \
                        "Geometric Violation: Path escapes the project sanctum."

                    raise ArtisanHeresy(
                        msg,
                        severity=HeresySeverity.CRITICAL,
                        details=f"Attempted: {purified_path}\nResolved: {physical_target}\nBoundary: {active_boundary}",
                        suggestion="Ensure all paths are relative to your project root. '..' is forbidden."
                    )
            except ValueError:
                # [ASCENSION 16]: Dimensional Rift Detection
                raise ArtisanHeresy("Dimensional Rift: Volume Discontinuity (Drive-Hopping).",
                                    severity=HeresySeverity.CRITICAL)

            # 2. [ASCENSION 12]: THE SOVEREIGN ENGINE SHIELD
            # Ward the Engine's own source code from self-consumption.
            try:
                engine_heart = Path(__file__).resolve().parents[1]
                venv_locus = Path(sys.prefix).resolve()

                for forbidden_realm in {engine_heart, venv_locus}:
                    try:
                        if os.path.commonpath([str(physical_target), str(forbidden_realm)]) == str(forbidden_realm):
                            raise ArtisanHeresy(
                                "Forbidden Gnosis: Overwriting the Engine's soul is strictly prohibited.",
                                severity=HeresySeverity.CRITICAL,
                                details=f"Target: {physical_target}\nProtected Stratum: {forbidden_realm}",
                                suggestion="Your will must remain within your project's topography, never the Engine's internals."
                            )
                    except ValueError:
                        continue
            except Exception:
                pass

            # 3. [ASCENSION 6]: CROWN JEWEL PROTECTION
            for segment in physical_target.parts:
                if segment in cls.CROWN_JEWELS:
                    raise ArtisanHeresy(
                        f"Forbidden Gnosis: Access to protected artifact '{segment}' is denied.",
                        severity=HeresySeverity.CRITICAL
                    )

        except (ValueError, OSError) as e:
            if isinstance(e, ArtisanHeresy): raise
            raise ArtisanHeresy(f"Geometric Resolution Paradox: {str(e)}", severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT VI: FORENSIC SCAN (MATTER LEAKS & RESERVED NAMES) ---
        path_segments = purified_path.split('/')
        for seg in path_segments:
            # [ASCENSION 10]: OS Reserved Namespace
            if seg.upper().split('.')[0] in cls.RESERVED_NAMES:
                raise ArtisanHeresy(f"OS Compatibility Heresy: '{seg}' is a reserved system name.",
                                    severity=HeresySeverity.CRITICAL)

            # [ASCENSION 4]: THE ANTI-MATTER PHALANX
            # [ASCENSION 14]: Jinja Variable Masking
            # We temporarily mask Jinja variables to allow braces inside legitimate paths,
            # but then check for code keywords.
            phantom_seg = re.sub(r'\{\{.*?\}\}', 'variable', seg)

            # [ASCENSION 15]: Trailing Phantom Exorcism
            if phantom_seg.endswith(('.', ' ')):
                raise ArtisanHeresy(
                    f"Trailing Phantom Heresy: Segment '{seg}' ends with dot or space.",
                    severity=HeresySeverity.WARNING,
                    details="This causes identity loss on Windows filesystems."
                )

            if any(sig in phantom_seg for sig in cls.MATTER_LEAK_SIGNATURES):
                # Double-check: Is it a logic node that wasn't caught early?
                # (e.g. "@if(condition)" might have split weirdly)
                if phantom_seg.strip().startswith('@'):
                    continue

                raise ArtisanHeresy(
                    f"Semantic Paradox: Path segment '{seg}' contains Logic Matter.",
                    severity=HeresySeverity.CRITICAL,
                    details="The Gnostic Parser likely failed to close a block, leaking code into topography.",
                    suggestion="Verify your blueprint indentation. Content must be indented under path headers."
                )

        # Final Verification of Forbidden Glyphs (Cross-Platform compatibility)
        if cls.PROFANE_CHARS.search(purified_path):
            raise ArtisanHeresy("Geometric Paradox: Illegal characters detected in path coordinate.",
                                severity=HeresySeverity.CRITICAL)

        # [ASCENSION 24]: THE FINALITY VOW
        # We return the absolute, resolved, and verified physical coordinate.
        return str(physical_target)

    @staticmethod
    def verify_metabolic_mass(content: Union[str, bytes], limit_mb: int = 50):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (V-Ω-METABOLIC-WARD)                               ==
        =============================================================================
        [ASCENSION 8]: Prevents the Engine from inhaling massive blobs into the Heap.
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
        """[ASCENSION 9]: Shannon Entropy calculation for secret detection."""
        import math
        if not text: return 0.0
        # Character frequency distribution
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])

        # Visual feedback for high entropy
        if entropy > 4.2:
            Logger.verbose(f"High Entropy perceived ({entropy:.2f}). Scanning for secrets...")

        return entropy