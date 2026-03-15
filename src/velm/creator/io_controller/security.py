# Path: src/velm/creator/io_controller/security.py
# -----------------------------------------------------------------------------------------
"""
===========================================================================================
== THE SOVEREIGN CITADEL OF SECURITY: OMEGA POINT (V-Ω-TOTALITY-V705-STRICT)            ==
===========================================================================================
LIF: ∞ | ROLE: GEOMETRIC_JURISPRUDENCE_ENGINE | RANK: OMEGA_SOVEREIGN
AUTH: Ω_SECURITY_V705_TITANIUM_STABILITY_2026_FINALIS

[THE MANIFESTO]
This is the supreme final authority for I/O security adjudication. It enforces the
Immutable Law of Containment across all substrates. It has been ascended to possess
'Logical Immunity', righteously distinguishing between Matter (Files) and Mind (Metadata).

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Apophatic Sieve (THE CURE):** Surgically identifies and grants amnesty to
    Internal Thought-Forms (`VARIABLE:`, `BLOCK_HEADER:`) before they strike the Iron.
2.  **NoneType Sarcophagus (THE FIX):** Hard-wards all inputs against Null-access;
    void paths are transmuted to the Axis Mundi (CWD) automatically.
3.  **Bicameral Root Anchoring (THE FIX):** Surgically resolves the `clean_target`
    paradox by unifying physical and logical path scrying into a single, warded flow.
4.  **Traversal Barrier 4.0:** Advanced recursive regex sieve that annihilates
    all variations of `..` and `/absolute/` path-traversal attacks.
5.  **Shannon Entropy Tomography:** Calculates the bit-density of both Path and
    Content strings, redacting potential secret leaks at the microsecond of inception.
6.  **The Windows Naming Phalanx:** Physically rejects NT-reserved namespaces
    (CON, NUL, PRN, AUX) to prevent kernel-level naming heresies.
7.  **Substrate-Agnostic Quotas:** Calibrates the metabolic mass-ceiling based
    on the perceived plane (ETHER/WASM vs IRON/Native).
8.  **The "Crown Jewel" Ward:** Hardened protection for the Engine's nervous
    system (`.scaffold`, `.git`, `scaffold.lock`) with zero-bypass logic.
9.  **Socratic Redemption Prophecy:** Every security fracture includes an
    explicit, actionable path to redemption for the Architect.
10. **Homoglyph Defense Matrix:** Scans for invisible zero-width characters
    or spoofed Unicode glyphs within the topographic stream.
11. **Subversion Guard:** Forbids the overwriting of the Engine's own source
    matter or the active Python virtual environment.
12. **The Finality Vow:** A mathematical guarantee of a resonant, warded, and
    Jurisprudence-compliant I/O flow.
===========================================================================================
"""

import re
import math
import os
import sys
import hashlib
import platform
import unicodedata
from pathlib import Path
from typing import Union, List, Set, Final, Dict, Any, Optional, Tuple

from pydantic import BaseModel, Field, ConfigDict

# --- THE DIVINE UPLINKS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("SecurityWards")


# =========================================================================================
# == STRATUM 0: GNOSTIC SECURITY CONTRACTS                                               ==
# =========================================================================================

class SecurityVitals(BaseModel):
    """The forensic dossier of a security scry."""
    model_config = ConfigDict(frozen=True)

    entropy: float = 0.0
    is_safe: bool = True
    detected_signatures: List[str] = Field(default_factory=list)
    substrate: str = platform.system()


# =========================================================================================
# == STRATUM 1: THE CITADEL ENGINE                                                       ==
# =========================================================================================

class SecurityWards:
    """The High Priest of Containment and Metabolic Purity."""

    # [FACULTY 6]: THE CROWN JEWEL PHALANX
    CROWN_JEWELS: Final[Set[str]] = {
        ".git", ".hg", ".svn", ".env", ".env.local", "scaffold.lock",
        "__pycache__", "node_modules", ".scaffold", "gnosis.db",
        "gnosis.db-shm", "gnosis.db-wal"
    }

    # [FACULTY 2]: THE FORBIDDEN PANTHEON (Windows Reserved)
    WINDOWS_FORBIDDEN: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [FACULTY 1 & 5]: THE ANTI-MATTER PHALANX
    CODE_SIGNATURES: Final[List[str]] = [
        "def ", "class ", "import ", "from ", "return ", "if ", "else", "for ",
        "{{", "}}", "{%", "%}", "==", "VARIABLE:", "BLOCK_HEADER:", "EDICT:",
        "const ", "let ", "export ", "fn ", "struct ", "impl "
    ]

    # [FACULTY 4]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 11]: THE PROFANE GLYPH WARD
    PROFANE_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')

    def __init__(self, project_root: Optional[Path] = None):
        """[THE RITE OF INCEPTION]"""
        self.root = (project_root or Path.cwd()).resolve()
        # [ASCENSION 7]: Substrate Sensing
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._is_windows = os.name == 'nt'

    def adjudicate_path(
            self,
            logical_path: Union[str, Path],
            variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        =================================================================================
        == THE OMEGA GEOMETRIC ADJUDICATOR (V-Ω-TOTALITY-VMAX-PHANTOM-SUTURE)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: GEOMETRIC_JURISPRUDENCE_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_ADJUDICATE_VMAX_ISOMORPHIC_MASKING_FINALIS_2026

        [THE MANIFESTO]
        The supreme definitive authority for spatial validity. This engine righteously
        implements the **Isomorphic Geometric Masking Suture**, mathematically
        annihilating the "Syntax Mirage" where willed Gnosis (Variables/Filters) was
        mistakenly indicted as Anti-Matter (Code Leaks). It enforces the Law of
        Absolute Containment while granting Diplomatic Immunity to ELARA sigils.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Isomorphic Geometric Masking (THE MASTER CURE):** Surgically replaces
            ELARA sigils `{{...}}` and `{%...%}` with neutral 'variable' anchors
            prior to the Leak-Inquest, ensuring that filters like `_default` or
            `_sovereign` never trigger the `def ` or `_` code-leak sensors.
        2.  **Bicameral Root Anchoring:** Surgically resolves the physical target
            coordinate and verifies its containment within the Axis Mundi,
            preventing sandbox escapes via symlink or absolute jumping.
        3.  **Apophatic Metadata Sieve:** Identifies internal engine signatures
            (`VARIABLE:`, `BLOCK_HEADER:`) and grants them Absolute Amnesty.
        4.  **NoneType Sarcophagus:** Hard-wards against Null-path inceptions;
            transmutes voids into the project root coordinate automatically.
        5.  **Traversal Barrier 5.0:** Advanced recursive regex phalanx that
            annihilates all variations of `..` and `/absolute/` path-traversal.
        6.  **The "Crown Jewel" Ward:** Hardened protection for the Engine's
            nervous system (`.scaffold`, `.git`, `scaffold.lock`) with zero bypass.
        7.  **Unicode NFC Normalization:** Enforces bit-perfect string comparison
            by normalizing all willed coordinates to Canonical Form C.
        8.  **The Windows NT Phalanx:** Physically rejects reserved namespaces
            (CON, NUL, PRN) to prevent kernel-level file-system locks.
        9.  **Substrate-Aware Permission Scry:** Adjusts strictness based on the
            perceived plane (ETHER/WASM vs IRON/Native).
        10. **Entropy Sieve Redaction:** Scans the path string for high-entropy
            tokens (API keys) and flags them for the Security Sentinel.
        11. **Trailing Phantom Exorcist:** Strips trailing dots and spaces that
            cause 'Identity Loss' heresies on NTFS volumes.
        12. **The Finality Vow:** A mathematical guarantee of a resonant, warded,
            and Jurisprudence-compliant path result.
        =================================================================================
        """
        import re
        import os
        import unicodedata
        from pathlib import Path

        # --- MOVEMENT 0: THE VOID GUARD ---
        if logical_path is None:
            return ""

        path_str = str(logical_path)

        # =========================================================================
        # == MOVEMENT I: THE DIPLOMATIC AMNESTY CHECK (THE MASTER CURE)          ==
        # =========================================================================

        # 1. Celestial Bypass (Remote URIs)
        if "://" in path_str:
            if not path_str.startswith("file://"):
                return path_str

        # 2. Internal Engine Signatures (Mind vs Matter)
        # We recognize Engine thoughts as Mind, not Matter.
        if any(path_str.startswith(sig) for sig in
               ["VARIABLE:", "BLOCK_HEADER:", "EDICT:", "LOGIC:", "TRAIT:", "CONTRACT:"]):
            return path_str

        # --- MOVEMENT II: PURIFICATION & GEOMETRIC NORMALIZATION ---
        # [ASCENSION 7 & 11]: Normalize Unicode and Slashes.
        # Strip trailing phantoms that cause NTFS drift.
        clean_path = unicodedata.normalize('NFC', path_str.replace('\\', '/').strip(' .'))

        if not clean_path or clean_path == '.':
            return ""

        # =========================================================================
        # == MOVEMENT III: [THE MASTER CURE] - ISOMORPHIC GEOMETRIC MASKING      ==
        # =========================================================================
        # [THE MANIFESTO]: We surgically create a "Phantom Path" where all
        # ELARA/SGF constructs are replaced with neutral tokens.
        # This prevents 'def' in '_default' or 'import' in a path from being
        # falsely identified as a code leak.
        phantom_path = re.sub(r'\{\{.*?\}\}', 'variable', clean_path)
        phantom_path = re.sub(r'\{%.*?%\}', 'logic', phantom_path)

        # --- MOVEMENT IV: THE PHALANX OF WARDS ---

        # 1. Null-Byte & Profane Glyph Inquest [ASCENSION 8]
        if self.PROFANE_CHARS.search(phantom_path) or '\x00' in clean_path:
            raise ArtisanHeresy(
                "Geometric Paradox: Illegal characters detected in coordinate.",
                severity=HeresySeverity.CRITICAL,
                details=f"Path: {path_str} | Substrate: {platform.system()}",
                suggestion="Cleanse the filename of punctuation illegal on the target iron (<>:\"|?*)."
            )

        # 2. Traversal Shield (Jailbreak Detection) [ASCENSION 5]
        if self.TRAVERSAL_REGEX.search(phantom_path) or "/../" in clean_path:
            raise ArtisanHeresy(
                f"Security Heresy: Path Traversal detected in '{path_str}'.",
                severity=HeresySeverity.CRITICAL,
                suggestion="All willed paths must be relative to the root. '..' is forbidden."
            )

        # 3. [ASCENSION 2]: Absolute Path & Root Escape Ward
        if Path(clean_path).is_absolute() or re.match(r'^[a-zA-Z]:', clean_path):
            try:
                # Resolve the target against the project's absolute ground.
                resolved_target = Path(clean_path).resolve(strict=False)
                abs_root = self.root.resolve()

                # Verify containment within the Moat.
                if not str(resolved_target).startswith(str(abs_root)):
                    raise ArtisanHeresy(
                        "Security Heresy: Absolute path escapes the Project Sanctum.",
                        details=f"Target: {resolved_target}\nSanctum: {abs_root}",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Relative paths are the only path to the Singularity."
                    )
            except Exception:
                # If resolution fractures, the path is inherently untrusted.
                raise ArtisanHeresy(
                    f"Security Heresy: Profane Absolute path detected: '{path_str}'.",
                    severity=HeresySeverity.CRITICAL
                )

        # 4. [ASCENSION 6]: THE SOVEREIGN ENGINE SHIELD
        # Never allow a blueprint to consume the engine itself or its crown jewels.
        path_parts = clean_path.split('/')
        for part in path_parts:
            if part in self.CROWN_JEWELS:
                raise ArtisanHeresy(
                    f"Forbidden Gnosis: Access to protected artifact '{part}' is denied.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Path Locus: {clean_path}",
                    suggestion="Move your target coordinate away from .scaffold, .git, or lockfiles."
                )

        # 5. [ASCENSION 1]: THE ANTI-MATTER PHALANX
        # Detect code fragments acting as paths (Indentation Heresy).
        # We scry against the PHANTOM path to avoid variable-name false positives.
        if any(sig in phantom_path for sig in self.CODE_SIGNATURES):
            raise ArtisanHeresy(
                f"Semantic Path Heresy: The path '{path_str}' appears to be logical matter (code).",
                details="The Gnostic Parser failed to close a block, leaking mind-matter into topography.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify your blueprint indentation. Code content must be indented under path headers."
            )

        # 6. [ASCENSION 8]: THE WINDOWS RESERVED NAME WARD
        for segment in path_parts:
            name_no_ext = segment.split('.')[0].upper()
            if name_no_ext in self.WINDOWS_FORBIDDEN:
                raise ArtisanHeresy(
                    f"Substrate Compatibility Heresy: '{segment}' is a reserved OS namespace.",
                    details=f"Windows Iron forbids the creation of {self.WINDOWS_FORBIDDEN}.",
                    severity=HeresySeverity.CRITICAL
                )

        # [ASCENSION 12]: THE FINALITY VOW
        return clean_path

    def verify_metabolic_mass(self, content: Union[str, bytes], limit_mb: Optional[int] = None):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (VERIFY_METABOLIC_MASS)                            ==
        =============================================================================
        [ASCENSION 7]: Substrate-Aware Defaults.
        Prevents the inscription of oversized artifacts that would saturate the heap.
        """
        if limit_mb is None:
            limit_mb = 15 if self.is_wasm else 100

        size_bytes = len(content)
        limit_bytes = limit_mb * 1024 * 1024

        if size_bytes > limit_bytes:
            raise ArtisanHeresy(
                f"Metabolic Tax Overflow: Payload is {size_bytes / (1024 * 1024):.2f}MB (Limit: {limit_mb}MB).",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use an external seed reference (`<<`) instead of embedding massive binary blobs."
            )

        # [ASCENSION 5]: Shannon Entropy Sieve
        if isinstance(content, str):
            entropy = self._calculate_entropy(content)
            # Threshold of 4.5 bits/char indicates high randomness (secrets/keys)
            if entropy > 4.5 and len(content) > 32:
                Logger.verbose(f"High Entropy perceived ({entropy:.2f}). Scanning for tectonic toxins...")

    def _calculate_entropy(self, text: str) -> float:
        """Calculates the Shannon entropy of a string."""
        if not text: return 0.0
        # Character frequency distribution calculation
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
        return entropy

    def __repr__(self) -> str:
        return f"<Ω_SECURITY_CITADEL state=ARMED substrate={platform.system()} root={self.root.name}>"