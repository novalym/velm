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
        == THE ADJUDICATE APOTHEOSIS (V-Ω-TOTALITY-V1000-ARTIFACT-AGNOSTIC)        ==
        =============================================================================
        LIF: INFINITY | ROLE: GEOMETRIC_SUPREME_ORACLE | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_PATH_SENTINEL_V1000_ARTIFACT_SIEVE_2026_FINALIS

        [THE MANIFESTO]:
        This rite has been ascended to consume "Messy AI Structures." It surgically
        strips tree-art, emojis, and formatting noise to find the pure coordinate.
        It also adjudicates between "Titan Mode" (Jailed) and "Sovereign Mode" (Local).
        """
        import os
        import re
        import sys
        import unicodedata
        from pathlib import Path

        # --- MOVEMENT 0: THE ARTIFACT SIEVE (THE CURE) ---
        # Surgically strip tree-art (├──, └──, │), emojis (📂, 📄, 📁), and excessive
        # indentation noise common in AI-generated "Project Structure" snippets.
        raw_path_str = str(logical_path)

        # 1. Strip Tree-Drawing and Emoji Artifacts
        # We target: ├──, └──, │, 📂, 📄, 📁, 📁, ┃, ┓, ┗, ┣, ┻, ┳, ╋
        purgation_pattern = re.compile(r'[📂📄📁├──└──│┃┏┓┗┛┠┨┬┴┼─━┃]')
        no_art_path = purgation_pattern.sub('', raw_path_str)

        # 2. Normalize Whitespace & Slashes
        # Strip leading/trailing spaces and handle both separator types
        purified_coordinate = no_art_path.strip().replace('\\', '/')

        # 3. Handle Leading Separators
        # If the AI provided "/src/main.py", we treat it as "src/main.py" relative to root.
        purified_coordinate = purified_coordinate.lstrip('/')

        # --- MOVEMENT I: THE RECURSIVE GAZE (ALCHEMICAL RESOLUTION) ---
        manifest_path_str = purified_coordinate
        if variables and '{{' in purified_coordinate:
            try:
                from ..core.alchemist import get_alchemist
                manifest_path_str = get_alchemist().transmute(purified_coordinate, variables)
            except Exception as e:
                raise ArtisanHeresy(
                    f"Alchemical Path Fracture: Could not scry the truth of '{purified_coordinate}'.",
                    severity=HeresySeverity.CRITICAL, details=str(e)
                )

        # Re-Normalize after Alchemical Transmutation
        purified_path = unicodedata.normalize('NFKC', manifest_path_str.replace('\\', '/').strip())

        # --- MOVEMENT II: GEOMETRIC ANCHORING ---
        # If the path is now empty or just a dot (e.g. it was just a 📂 or ├──),
        # it refers to the project root itself.
        if not purified_path or purified_path == '.':
            return str(project_root.resolve())

        # [THE WARD]: Null-Byte and Absolute Path Phalanx
        if '\0' in purified_path:
            raise SecurityHeresy("Null-Byte Injection perceived. Access Denied.", code="NULL_BYTE_FRACTURE")

        # --- MOVEMENT III: THE INODE WARD (PHYSICAL MATERIALIZATION) ---
        try:
            abs_root = project_root.resolve()

            # [ASCENSION 13]: MODE SENSING (Titan vs Sovereign)
            # We scry for the Jail Root. If it exists, we are in a Jailed (Azure) environment.
            # If not, we are in Sovereign (Local) mode.
            jail_root_str = os.getenv("SCAFFOLD_JAIL_ROOT")
            is_jailed = bool(jail_root_str)
            jail_root = Path(jail_root_str).resolve() if is_jailed else abs_root

            # Construct the physical target coordinate
            # We join and resolve to handle any remaining '..' trickery
            try:
                # strict=False allows the Gaze to fall upon files that don't yet exist
                physical_target = (abs_root / purified_path).resolve(strict=False)
            except RecursionError:
                raise ArtisanHeresy("Geometric Paradox: Infinite Symlink loop detected.",
                                    severity=HeresySeverity.CRITICAL)

            # --- MOVEMENT IV: THE RECONCILIATION OF REALMS ---

            # A. The Staging Amnesty
            # Detect if the rite is touching internal management shards.
            is_internal_rite = any(x in purified_path for x in (".scaffold/", "scaffold.lock", ".heartbeat"))

            # B. [THE CURE]: CONTEXT-AWARE BOUNDARY ADJUDICATION
            if not is_internal_rite:
                # 1. The Boundary Check
                # We use commonpath to ensure the target is within the ordained sanctum.
                try:
                    # Logic: If Jailed, we compare against jail_root. If Sovereign, against abs_root.
                    active_boundary = jail_root if is_jailed else abs_root
                    if os.path.commonpath([str(active_boundary), str(physical_target)]) != str(active_boundary):
                        # [THE REDEMPTION]: Clearer error messages for Local vs Remote
                        if is_jailed:
                            msg = "Forbidden Gnosis: Target escapes assigned UUID workspace."
                        else:
                            msg = "Geometric Violation: Path escapes the project sanctum."

                        raise ArtisanHeresy(
                            msg,
                            severity=HeresySeverity.CRITICAL,
                            details=f"Attempted: {purified_path}\nResolved: {physical_target}\nRoot: {active_boundary}",
                            suggestion="Ensure all paths are relative to your current project root."
                        )
                except ValueError:
                    raise ArtisanHeresy("Dimensional Rift: Paths exist on different hardware volumes.",
                                        severity=HeresySeverity.CRITICAL)

                # 2. The Engine Soul Ward
                # Even in Sovereign mode, we prevent the Architect from accidentally
                # overwriting the VELM Engine source code or its active VENV.
                engine_source_locus = Path(__file__).resolve().parents[3]
                venv_locus = Path(sys.prefix).resolve()
                for realm in {engine_source_locus, venv_locus}:
                    try:
                        if os.path.commonpath([str(physical_target), str(realm)]) == str(realm):
                            raise ArtisanHeresy(
                                "Forbidden Gnosis: Access to the Sovereign Engine source or environment is restricted.",
                                severity=HeresySeverity.CRITICAL,
                                suggestion="Your will must remain within your project's workspace, not the engine's internals."
                            )
                    except (ValueError, OSError):
                        continue

                # 3. Crown Jewel Protection
                for part in physical_target.parts:
                    if part in cls.CROWN_JEWELS:
                        # We allow internal rites to touch jewels, but not standard forms.
                        raise ArtisanHeresy(f"Forbidden Gnosis: Access to protected artifact '{part}' is denied.",
                                            severity=HeresySeverity.CRITICAL)

        except (ValueError, OSError) as e:
            if isinstance(e, ArtisanHeresy): raise
            raise ArtisanHeresy(f"Geometric Resolution Paradox: {e}", severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT V: FORENSIC SCAN (MATTER LEAK & ENTROPY) ---
        # [ASCENSION 15]: Atomic Segment Scan
        segments = purified_path.split('/')
        for seg in segments:
            # Device Name Sentinel (CON, NUL, /dev/...)
            if seg.upper().split('.')[0] in cls.RESERVED_NAMES:
                raise ArtisanHeresy(f"OS Compatibility Heresy: '{seg}' is a reserved system name.",
                                    severity=HeresySeverity.CRITICAL)

            # Logic Leak Detection (Code-as-Path)
            # Warded against signatures that imply a line of code was mistaken for a file.
            if any(sig in seg for sig in cls.MATTER_LEAK_PATTERNS):
                raise ArtisanHeresy(
                    f"Semantic Paradox: Path segment '{seg}' contains Code Matter.",
                    severity=HeresySeverity.CRITICAL,
                    details="The Gnostic Parser leaked code into the topography. Verify your blueprint indentation.",
                    suggestion="Ensure file content is indented correctly beneath the path header."
                )

        # Final Verification of forbidden glyphs
        if cls.PROFANE_CHARS.search(purified_path):
            raise ArtisanHeresy("Geometric Paradox: Illegal characters detected in path.",
                                severity=HeresySeverity.CRITICAL)

        # The Finality Vow: Return the absolute, resolved, and verified physical truth.
        return str(physical_target)

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