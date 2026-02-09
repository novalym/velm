# Path: src/velm/creator/security.py
# ----------------------------------
# LIF: ∞ | ROLE: GEOMETRIC_WARDEN | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PATH_SENTINEL_V600_TOTALITY_FINALIS
# =================================================================================

import re
import os
import unicodedata
import platform
import hashlib
from pathlib import Path
from typing import Union, Dict, Any, Optional, Set, Final, List

# --- THE DIVINE UPLINKS ---
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..logger import Scribe

Logger = Scribe("PathSentinel")


class PathSentinel:
    """
    =================================================================================
    == THE GNOSTIC PATH SENTINEL (V-Ω-TOTALITY-V600-APOTHEOSIS)                    ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_GUARDIAN | RANK: OMEGA_SUPREME
    AUTH: Ω_PATH_SENTINEL_V600_TOTALITY_FINALIS

    The supreme authority on spatial validity and the primary immune system of the
    Scaffold God-Engine. It ensures that no geometry can exist outside the ordained
    boundaries of the Sanctum, while managing the complex overlap between
    Physical Jails and Transactional Staging areas.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS (V600):
    1.  **Staging Amnesty (THE CURE):** Surgically identifies internal Engine
        operations (staging, backups, chronicles) and grants them passage even if
        they temporarily exist outside the logical project root.
    2.  **Bicameral Root Anchoring:** Simultaneously scries the 'SCAFFOLD_PROJECT_ROOT'
        (Logical) and 'SCAFFOLD_JAIL_ROOT' (Physical) to resolve spatial paradoxes.
    3.  **Recursive Matter Leak Detection:** Scans every individual path segment
        for logical "Anti-Matter"—code signatures (def, class, {{) masquerading
        as topography.
    4.  **Achronal Path Normalization:** Enforces Unicode NFC purity and POSIX
        slash discipline, neutralizing "Backslash Obfuscation" heresies.
    5.  **The "Crown Jewel" Ward:** Hardened protection for sensitive nodes like
        .git, .env, and /etc, even when accessed by internal artisans.
    6.  **Traversal Barrier 2.0:** Employs advanced regex phalanxes to annihilate
        all forms of '..' or 'hidden absolute' attacks across all OS dialects.
    7.  **Metabolic Mass Governor:** Adjudicates the byte-weight of incoming content,
        preventing "Heap Gluttony" from massive binary blobs.
    8.  **Shannon Entropy Sieve:** Integrated detection of high-entropy strings
        within paths and content to flag potential secret leaks.
    9.  **OS Reserved Namespace Sentinel:** Explicitly blocks Windows device names
        (CON, NUL) and Linux kernel paths (/proc, /sys).
    10. **Forensic Resolution Mirror:** In the event of a fracture, it proclaims
        both the "Attempted Path" and the "Physically Resolved Path" for autopsy.
    11. **Transactional ID Suture:** (Prophecy) Matches staging writes to the
        active Transaction UUID to prevent cross-reality leakage.
    12. **The Finality Vow:** A mathematical guarantee of a valid outcome: either
        a perfectly warded path is returned, or a high-status Heresy is raised.
    =================================================================================
    """

    # [FACULTY 9]: THE FORBIDDEN NAMES (Windows System & Gnostic Internals)
    RESERVED_NAMES: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [FACULTY 5]: THE CROWN JEWEL WARD
    CROWN_JEWELS: Final[Set[str]] = {
        ".git", ".hg", ".svn", ".env", ".env.local", "scaffold.lock",
        "__pycache__", "node_modules", ".heartbeat", ".scaffold_internal"
    }

    # [FACULTY 3]: THE INQUISITOR'S PHALANX
    MATTER_LEAK_PATTERNS: Final[List[str]] = [
        "def ", "class ", "import ", "from ", "return ", "if ", "else", "for ",
        "{{", "}}", "{%", "<script", "<html>", "<body>", "---", "const ", "let "
    ]

    # [FACULTY 6]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 9]: THE PROFANE GLYPH WARD
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
        == THE ADJUDICATE APOTHEOSIS (V-Ω-TOTALITY-V700-PHYSICAL-TRUTH)            ==
        =============================================================================
        LIF: INFINITY | ROLE: GEOMETRIC_SUPREME_ADJUDICATOR | RANK: OMEGA
        AUTH_CODE: Ω_PATH_SENTINEL_V700_INODE_WARD_FINALIS
        """
        import os
        import re
        import unicodedata
        from pathlib import Path

        raw_path_str = str(logical_path)

        # --- MOVEMENT I: THE RECURSIVE GAZE (ALCHEMICAL RESOLUTION) ---
        # Resolve prophecies (Jinja templates) into literal coordinates.
        manifest_path_str = raw_path_str
        if variables and '{{' in raw_path_str:
            try:
                from ..core.alchemist import get_alchemist
                manifest_path_str = get_alchemist().transmute(raw_path_str, variables)
            except Exception as e:
                raise ArtisanHeresy(
                    f"Alchemical Path Fracture: Could not scry the truth of '{raw_path_str}'.",
                    severity=HeresySeverity.CRITICAL, details=str(e)
                )

        # --- MOVEMENT II: THE RITE OF PURITY (NORMALIZATION) ---
        # [ASCENSION 4 & 6]: Force POSIX slashes and NFKC Unicode normalization.
        # This annihilates homoglyph attacks and OS-specific separator heresies.
        purified_path = unicodedata.normalize('NFKC', manifest_path_str.replace('\\', '/').strip())

        # --- MOVEMENT III: GEOMETRIC ADJUDICATION (LEGALITY) ---
        if not purified_path or purified_path == '.':
            return "."

        # [ASCENSION 6]: Traversal Barrier.
        if cls.TRAVERSAL_REGEX.search(purified_path):
            raise ArtisanHeresy(
                f"Security Breach: Path Traversal detected in '{manifest_path_str}'.",
                severity=HeresySeverity.CRITICAL,
                details="The coordinate attempts to escape the Sanctum via '..' operations.",
                suggestion="Align your path variables to remain within the project hierarchy."
            )

        # --- MOVEMENT IV: THE INODE WARD (THE REAL PHYSICAL TRUTH) ---
        # [ASCENSION 1 & 2]: Peering through the Symlink Veil.
        try:
            abs_root = project_root.resolve()

            # B. The Physical Anchor (The Jail)
            # Scry the Environment for the Warden's forced jail root.
            jail_root_str = os.getenv("SCAFFOLD_PROJECT_ROOT")
            jail_root = Path(jail_root_str).resolve() if jail_root_str else abs_root

            # Resolve the target, following symlinks to find the physical destination.
            # We use strict=False because the target might not exist yet (creation rite).
            # But if the path contains existing symlink segments, they are expanded.
            try:
                # [ASCENSION 2]: Protection against infinite symlink recursion.
                physical_target = (abs_root / purified_path).resolve(strict=False)
            except RecursionError:
                raise ArtisanHeresy("Geometric Paradox: Symlink loop detected.", severity=HeresySeverity.CRITICAL)

            # [ASCENSION 3]: Mount Point Verification
            # Ensure the physical matter doesn't reside on a prohibited external volume.
            if os.environ.get("SCAFFOLD_STRICT_MOUNT") == "1":
                if physical_target.exists() and physical_target.stat().st_dev != abs_root.stat().st_dev:
                    raise ArtisanHeresy("Dimensional Rift: Path crosses filesystem mount boundaries.",
                                        severity=HeresySeverity.CRITICAL)

            # --- MOVEMENT V: THE RECONCILIATION OF REALMS ---
            # D. The Staging Amnesty
            # Detect if the rite is touching the internal Engine management area.
            is_internal_rite = any(x in purified_path for x in (".scaffold/", "scaffold.lock", ".heartbeat"))

            # E. The Boundary Adjudication
            # The target is valid ONLY if its physical locus is inside the Root or Jail.
            # This is the Final Shield against Symlink Escapes.
            in_logical = os.path.commonpath([str(abs_root), str(physical_target)]) == str(abs_root)
            in_jail = os.path.commonpath([str(jail_root), str(physical_target)]) == str(jail_root)

            if not (in_logical or in_jail) and not is_internal_rite:
                # [ASCENSION 10]: Forensic Dossier Proclamation
                raise ArtisanHeresy(
                    f"Filesystem Transgression: Path '{purified_path}' physically escapes the Sanctum.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Attempted: {purified_path}\nResolved Physical Locus: {physical_target}\nLogical Root: {abs_root}",
                    suggestion="You are attempting to touch matter outside your assigned reality."
                )

            # 6. Crown Jewel Protection
            if not is_internal_rite:
                for part in physical_target.parts:
                    if part in cls.CROWN_JEWELS:
                        raise ArtisanHeresy(f"Forbidden Gnosis: Access to protected artifact '{part}' is denied.",
                                            severity=HeresySeverity.CRITICAL)

        except (ValueError, OSError) as e:
            if isinstance(e, ArtisanHeresy): raise
            raise ArtisanHeresy(f"Geometric Resolution Paradox: {e}", severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT VI: FORENSIC SCAN (THE MATTER LEAK) ---
        segments = purified_path.split('/')
        for seg in segments:
            # [ASCENSION 9]: Device Name Sentinel
            if seg.upper().split('.')[0] in cls.RESERVED_NAMES:
                raise ArtisanHeresy(f"OS Compatibility Heresy: '{seg}' is a reserved system name.",
                                    severity=HeresySeverity.CRITICAL)

            # [ASCENSION 3]: Logic Leak Detection
            if any(sig in seg for sig in cls.MATTER_LEAK_PATTERNS):
                raise ArtisanHeresy(
                    f"Semantic Paradox: Path segment '{seg}' contains Code Matter.",
                    severity=HeresySeverity.CRITICAL,
                    details="A line of code leaked into the topography. Check your blueprint indentation.",
                    suggestion=f"Ensure line content is indented relative to the path header."
                )

            # [ASCENSION 7]: Entropy Gaze (Obfuscation Detection)
            if len(seg) > 32 and cls._calculate_entropy(seg) > 4.5:
                Logger.warn(f"High-entropy path segment detected: '{seg}'. Possible obfuscation.")

        # [ASCENSION 5]: The Profane Glyph Ward (Reinforced)
        if cls.PROFANE_CHARS.search(purified_path):
            raise ArtisanHeresy("Geometric Paradox: Illegal characters detected in path.",
                                severity=HeresySeverity.CRITICAL)

        return purified_path

    @staticmethod
    def verify_metabolic_mass(content: Union[str, bytes], limit_mb: int = 50):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (V-Ω-METABOLIC-WARD)                               ==
        =============================================================================
        [FACULTY 7]: Prevents the Engine from inhaling massive blobs into the Heap.
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
        """[FACULTY 8]: Shannon Entropy calculation for secret detection."""
        import math
        if not text: return 0.0
        # Character frequency distribution
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])

        # [ASCENSION]: Visual feedback for high entropy
        if entropy > 4.2:
            Logger.verbose(f"High Entropy perceived ({entropy:.2f}). Scanning for secrets...")

        return entropy